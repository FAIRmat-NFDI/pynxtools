#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""This script runs the conversion routine using a selected reader and write out a Nexus file."""

import glob
import importlib.machinery
import importlib.util
import logging
import os
import sys
from typing import List, Tuple, Any
import xml.etree.ElementTree as ET

import click

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
from nexusparser.tools.dataconverter import helpers
from nexusparser.tools.dataconverter.writer import Writer
from nexusparser.tools.dataconverter.template import Template
from nexusparser.tools import nexus


logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_reader(reader_name) -> BaseReader:
    """Helper function to get the reader object from it's given name"""
    path_prefix = f"{os.path.dirname(__file__)}{os.sep}" if os.path.dirname(__file__) else ""
    path = os.path.join(path_prefix, "readers", reader_name, "reader.py")
    spec = importlib.util.spec_from_file_location("reader.py", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module.READER  # type: ignore[attr-defined]


def get_names_of_all_readers() -> List[str]:
    """Helper function to populate a list of all available readers"""
    path_prefix = f"{os.path.dirname(__file__)}{os.sep}" if os.path.dirname(__file__) else ""
    files = glob.glob(os.path.join(path_prefix, "readers", "*", "reader.py"))
    all_readers = []
    for file in files:
        if f"{os.sep}base{os.sep}" not in file:
            index_of_readers_folder_name = file.rindex(f"readers{os.sep}") + len(f"readers{os.sep}")
            index_of_last_path_sep = file.rindex(os.sep)
            all_readers.append(file[index_of_readers_folder_name:index_of_last_path_sep])
    return all_readers


def convert(input_file: Tuple[str],  # pylint: disable=too-many-arguments
            reader: str,
            nxdl: str,
            output: str,
            generate_template: bool,
            fair: bool,
            objects: Tuple[Any] = None):
    """The conversion routine that takes the input parameters and calls the necessary functions."""
    # Reading in the NXDL and generating a template
    if nxdl == "NXtest":
        nxdl_path = os.path.join("tests", "data", "tools", "dataconverter", "NXtest.nxdl.xml")
    else:
        definitions_path = nexus.get_nexus_definitions_path()
        nxdl_path = os.path.join(definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml")
        if not os.path.exists(nxdl_path):
            nxdl_path = os.path.join(definitions_path, "applications", f"{nxdl}.nxdl.xml")
        if not os.path.exists(nxdl_path):
            raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

    nxdl_root = ET.parse(nxdl_path).getroot()

    # template: Dict[str, str] = {}
    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)
    if generate_template:
        logger.info(template)
        return

    # Setting up all the input data
    bulletpoint = "\n\u2022 "
    logger.info("Using %s reader to convert the given files: %s ",
                reader,
                bulletpoint.join((" ", *input_file)))

    data_reader = get_reader(reader)
    if nxdl not in data_reader.supported_nxdls:
        raise Exception("The chosen NXDL isn't supported by the selected reader.")

    if objects is not None:
        data = data_reader().read(template=Template(template),
                                  file_paths=input_file,
                                  objects=objects)  # type: ignore[operator]
    else:
        data = data_reader().read(template=Template(template),
                                  file_paths=input_file)  # type: ignore[operator]

    helpers.validate_data_dict(template, data, nxdl_root)

    if fair and data.undocumented.keys():
        logger.warning("There are undocumented paths in the template. This is not acceptable!")
        return

    for path in data.undocumented.keys():
        logger.warning("The path, %s, is being written but has no documentation.", path)

    # Writing the data to output file
    Writer(data=data, nxdl_path=nxdl_path, output_path=output).write()

    logger.info("The output file generated: %s", output)


@click.command()
@click.option(
    '--input-file',
    default=[],
    multiple=True,
    help='The path to the input data file to read. (Repeat for more than one file.)'
)
@click.option(
    '--reader',
    default='example',
    type=click.Choice(get_names_of_all_readers(), case_sensitive=False),
    help='The reader to use. default="example"'
)
@click.option(
    '--nxdl',
    default=None,
    required=True,
    help='The name of the NXDL file to use without extension.'
)
@click.option(
    '--output',
    default='output.nxs',
    help='The path to the output Nexus file to be generated.'
)
@click.option(
    '--generate-template',
    is_flag=True,
    default=False,
    help='Just print out the template generated from given NXDL file.'
)
@click.option(  # pylint: disable=too-many-arguments
    '--fair',
    is_flag=True,
    default=False,
    help='Let the converter know to be stricter in checking the documentation.'
)
def convert_cli(input_file: Tuple[str],
                reader: str,
                nxdl: str,
                output: str,
                generate_template: bool,
                fair: bool):
    """The CLI entrypoint for the convert function"""
    convert(input_file, reader, nxdl, output, generate_template, fair)


if __name__ == '__main__':
    convert_cli()  # pylint: disable=no-value-for-parameter
