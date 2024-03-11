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
"""This script runs the conversion routine using a selected reader and write out a NeXus file."""
import glob
import importlib.machinery
import importlib.util
import logging
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Tuple

import click
import yaml

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.writer import Writer
from pynxtools.nexus import nexus

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points
else:
    try:
        from importlib_metadata import entry_points
    except ImportError:
        # If importlib_metadata is not present
        # we provide a dummy function just returning an empty list.
        # pylint: disable=W0613
        def entry_points(group):
            """Dummy function for importlib_metadata"""
            return []


def get_reader(reader_name) -> BaseReader:
    """Helper function to get the reader object from it's given name"""
    path_prefix = (
        f"{os.path.dirname(__file__)}{os.sep}" if os.path.dirname(__file__) else ""
    )
    path = os.path.join(path_prefix, "readers", reader_name, "reader.py")
    spec = importlib.util.spec_from_file_location("reader.py", path)
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    except FileNotFoundError as exc:
        # pylint: disable=unexpected-keyword-arg
        importlib_module = entry_points(group="pynxtools.reader")
        if importlib_module and reader_name in map(
            lambda ep: ep.name, importlib_module
        ):
            return importlib_module[reader_name].load()
        raise ValueError(f"The reader, {reader_name}, was not found.") from exc
    return module.READER  # type: ignore[attr-defined]


def get_names_of_all_readers() -> List[str]:
    """Helper function to populate a list of all available readers"""
    path_prefix = (
        f"{os.path.dirname(__file__)}{os.sep}" if os.path.dirname(__file__) else ""
    )
    files = glob.glob(os.path.join(path_prefix, "readers", "*", "reader.py"))
    all_readers = []
    for file in files:
        if f"{os.sep}base{os.sep}" not in file:
            index_of_readers_folder_name = file.rindex(f"readers{os.sep}") + len(
                f"readers{os.sep}"
            )
            index_of_last_path_sep = file.rindex(os.sep)
            all_readers.append(
                file[index_of_readers_folder_name:index_of_last_path_sep]
            )
    plugins = list(map(lambda ep: ep.name, entry_points(group="pynxtools.reader")))
    return sorted(all_readers + plugins)


def get_nxdl_root_and_path(nxdl: str):
    """Get xml root element and file path from nxdl name e.g. NXapm.

    Parameters
    ----------
    nxdl: str
        Name of nxdl file e.g. NXapm from NXapm.nxdl.xml.

    Returns
    -------
    ET.root
        Root element of nxdl file.
    str
        Path of nxdl file.

    Raises
    ------
    FileNotFoundError
        Error if no file with the given nxdl name is found.
    """
    # Reading in the NXDL and generating a template
    definitions_path = nexus.get_nexus_definitions_path()
    if nxdl == "NXtest":
        nxdl_f_path = os.path.join(
            f"{os.path.abspath(os.path.dirname(__file__))}/../../",
            "tests",
            "data",
            "dataconverter",
            "NXtest.nxdl.xml",
        )
    elif nxdl == "NXroot":
        nxdl_f_path = os.path.join(definitions_path, "base_classes", "NXroot.nxdl.xml")
    else:
        nxdl_f_path = os.path.join(
            definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml"
        )
        if not os.path.exists(nxdl_f_path):
            nxdl_f_path = os.path.join(
                definitions_path, "applications", f"{nxdl}.nxdl.xml"
            )
        if not os.path.exists(nxdl_f_path):
            nxdl_f_path = os.path.join(
                definitions_path, "base_classes", f"{nxdl}.nxdl.xml"
            )
        if not os.path.exists(nxdl_f_path):
            raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

    return ET.parse(nxdl_f_path).getroot(), nxdl_f_path


def transfer_data_into_template(
    input_file,
    reader,
    nxdl_name,
    nxdl_root: Optional[ET.Element] = None,
    skip_verify: bool = False,
    **kwargs,
):
    """Transfer parse and merged data from input experimental file, config file and eln.

    Experimental and eln files will be parsed and finally will be merged into template.
    Before returning the template validate the template data.

    Parameters
    ----------
    input_file : Union[tuple[str], str]
        Tuple of files or file
    reader: str
        Name of reader such as xps
    nxdl_name : str
        Root name of nxdl file, e.g. NXmpes from NXmpes.nxdl.xml
    nxdl_root : ET.element
        Root element of nxdl file, otherwise provide nxdl_name
    skip_verify: bool, default False
        Skips verification routine if set to True

    Returns
    -------
    Template
        Template filled with data from raw file and eln file.

    """
    if nxdl_root is None:
        nxdl_root, _ = get_nxdl_root_and_path(nxdl=nxdl_name)

    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)

    if isinstance(input_file, str):
        input_file = (input_file,)

    bulletpoint = "\n\u2022 "
    logger.info(
        f"Using {reader} reader to convert the given files:"
        f" {bulletpoint.join((' ', *input_file))}"
    )

    data_reader = get_reader(reader)
    if not (
        nxdl_name in data_reader.supported_nxdls or "*" in data_reader.supported_nxdls
    ):
        raise NotImplementedError(
            "The chosen NXDL isn't supported by the selected reader."
        )

    data = data_reader().read(  # type: ignore[operator]
        template=Template(template), file_paths=input_file, **kwargs
    )
    if not skip_verify:
        helpers.validate_data_dict(template, data, nxdl_root)
    return data


# pylint: disable=too-many-arguments,too-many-locals,W1203
def convert(
    input_file: Tuple[str, ...],
    reader: str,
    nxdl: str,
    output: str,
    generate_template: bool = False,
    fair: bool = False,
    undocumented: bool = False,
    skip_verify: bool = False,
    **kwargs,
):
    """The conversion routine that takes the input parameters and calls the necessary functions.

    Parameters
    ----------
    input_file : Tuple[str]
        Tuple of files or file
    reader: str
        Name of reader such as xps
    nxdl : str
        Root name of nxdl file, e.g. NXmpes for NXmpes.nxdl.xml
    output : str
        Output file name.
    generate_template : bool, default False
        True if user wants template in logger info.
    fair : bool, default False
        If True, a warning is given that there are undocumented paths
        in the template.
    undocumented : bool, default False
        If True, an undocumented warning is given.
    skip_verify: bool, default False
        Skips verification routine if set to True

    Returns
    -------
    None.
    """

    nxdl_root, nxdl_f_path = get_nxdl_root_and_path(nxdl)
    if generate_template:
        template = Template()
        helpers.generate_template_from_nxdl(nxdl_root, template)
        print(template)
        return

    data = transfer_data_into_template(
        input_file=input_file,
        reader=reader,
        nxdl_name=nxdl,
        nxdl_root=nxdl_root,
        skip_verify=skip_verify,
        **kwargs,
    )

    if fair and data.undocumented.keys():
        logger.warning(
            "There are undocumented paths in the template. This is not acceptable!"
        )
        return
    if undocumented:
        for path in data.undocumented.keys():
            if "/@default" in path:
                continue
            logger.info(
                f"NO DOCUMENTATION: The path, {path}, is being written but has no documentation."
            )

    helpers.add_default_root_attributes(data=data, filename=os.path.basename(output))
    Writer(data=data, nxdl_f_path=nxdl_f_path, output_path=output).write()

    logger.info(f"The output file generated: {output}.")


def parse_params_file(params_file):
    """Parses the parameters from a given dictionary and returns them"""
    params = yaml.load(params_file, Loader=yaml.Loader)["dataconverter"]
    for param in list(params.keys()):
        params[param.replace("-", "_")] = params.pop(param)
    return params


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--input-file",
    default=[],
    multiple=True,
    help=(
        "Deprecated: Please use the positional file arguments instead. "
        "The path to the input data file to read. (Repeat for more than one file.)"
    ),
)
@click.option(
    "--reader",
    default="json_map",
    type=click.Choice(get_names_of_all_readers(), case_sensitive=False),
    help='The reader to use. default="example"',
)
@click.option(
    "--nxdl",
    default=None,
    help=(
        "The name of the NXDL file to use without extension."
        "This option is required if no '--params-file' is supplied."
    ),
)
@click.option(
    "--output",
    default="output.nxs",
    help="The path to the output NeXus file to be generated.",
)
@click.option(
    "--generate-template",
    is_flag=True,
    default=False,
    help="Just print out the template generated from given NXDL file.",
)
@click.option(
    "--fair",
    is_flag=True,
    default=False,
    help="Let the converter know to be stricter in checking the documentation.",
)
@click.option(
    "--params-file",
    type=click.File("r"),
    default=None,
    help="Allows to pass a .yaml file with all the parameters the converter supports.",
)
@click.option(
    "--undocumented",
    is_flag=True,
    default=False,
    help="Shows a log output for all undocumented fields",
)
@click.option(
    "--skip-verify",
    is_flag=True,
    default=False,
    help="Skips the verification routine during conversion.",
)
@click.option(
    "--mapping",
    help="Takes a <name>.mapping.json file and converts data from given input files.",
)
# pylint: disable=too-many-arguments
def convert_cli(
    files: Tuple[str, ...],
    input_file: Tuple[str, ...],
    reader: str,
    nxdl: str,
    output: str,
    generate_template: bool,
    fair: bool,
    params_file: str,
    undocumented: bool,
    skip_verify: bool,
    mapping: str,
):
    """The CLI entrypoint for the convert function"""
    if params_file:
        try:
            convert(**parse_params_file(params_file))
            return
        except TypeError as exc:
            sys.tracebacklimit = 0
            raise click.UsageError(
                (
                    "Please make sure you have the following entries in your "
                    "parameter file:\n\n# NeXusParser Parameter File - v0.0.1"
                    "\n\ndataconverter:\n\treader: value\n\tnxdl: value\n\tin"
                    "put-file: value"
                )
            ) from exc
    if nxdl is None:
        raise click.UsageError("Missing option '--nxdl'")
    if mapping:
        reader = "json_map"
        input_file = input_file + tuple([mapping])

    file_list = []
    for file in files:
        if os.path.isdir(file):
            p = Path(file)
            for f in p.rglob("*"):
                if f.is_file():
                    file_list.append(str(f))
            continue
        file_list.append(file)

    if input_file:
        logger.warning(
            "The --input-file option is deprecated. Please use the positional arguments instead."
        )

    convert(
        tuple(file_list) + input_file,
        reader,
        nxdl,
        output,
        generate_template,
        fair,
        undocumented,
        skip_verify,
    )
