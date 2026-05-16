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
import importlib.util
import logging
import os

import lxml.etree as ET
import yaml

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against
from pynxtools.dataconverter.writer import Writer
from pynxtools.nexus.nexus_tree import generate_tree_from

logger = logging.getLogger("pynxtools")


from importlib.metadata import entry_points


class ValidationFailed(Exception):
    pass


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


def get_names_of_all_readers() -> list[str]:
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


def transfer_data_into_template(
    input_file,
    reader,
    nxdl_name,
    nxdl_root: ET._Element | None = None,
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
        If the dataconverter is configured with append = True,
        verification is currently always skipped, use validate
        on the resulting HDF5 file instead

    Returns
    -------
    Template
        Template filled with data from raw file and eln file.

    """
    if nxdl_root is None:
        nxdl_root, _ = helpers.get_nxdl_root_and_path(nxdl=nxdl_name)

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

    ignore_undocumented = kwargs.pop("ignore_undocumented", False)
    fail = kwargs.pop("fail", False)
    append = kwargs.pop("append", False)

    data = data_reader().read(  # type: ignore[operator]
        template=Template(template), file_paths=input_file, **kwargs
    )
    entry_names = data.get_all_entry_names()
    for entry_name in entry_names:
        helpers.write_nexus_def_to_entry(data, entry_name, nxdl_name)
    if not append and not skip_verify:
        valid = validate_dict_against(
            nxdl_name,
            data,
            ignore_undocumented=ignore_undocumented,
        )

        if fail and not valid:
            raise ValidationFailed(
                "The data does not match the given NXDL. "
                "Please check the log for more information."
            )
    return data


# pylint: disable=too-many-arguments,too-many-locals,W1203
def convert(
    input_file: tuple[str, ...],
    reader: str,
    nxdl: str,
    output: str,
    skip_verify: bool = False,
    **kwargs,
):
    """The conversion routine that takes the input parameters and calls the necessary functions.

    Parameters
    ----------
    input_file : tuple[str]
        Tuple of files or file
    reader: str
        Name of reader such as xps
    nxdl : str
        Root name of nxdl file, e.g. NXmpes for NXmpes.nxdl.xml
    output : str
        Output file name.
    skip_verify: bool, default False
        Skips verification routine if set to True
    generate_template : bool, default False
        True if user wants template in logger info.
    fair : bool, default False
        If True, a warning is given that there are undocumented paths
        in the template.
    ignore_undocumented : bool, default False
        If True, all undocumented items are ignored in the validation.
    append : bool, default False
        If True, allows adding instances. Currently, resizing existent datasets
        (e.g. using chunked storage layout) is not supported
        It is the users responsibility to prepare the template dictionary
        such that one does not instantiate any HDF5 object type that already
        exists. If happening nonetheless, the HDF5 libraries ValueError is caught
        and the program emits a log message warning that the instance has not been
        added. This is in an attempt to prevent an invalidating of the file.
    Returns
    -------
    None.
    """
    nxdl_root, nxdl_f_path = helpers.get_nxdl_root_and_path(nxdl)

    data = transfer_data_into_template(
        input_file=input_file,
        reader=reader,
        nxdl_name=nxdl,
        nxdl_root=nxdl_root,
        skip_verify=skip_verify,
        **kwargs,
    )
    helpers.add_default_root_attributes(
        data=data,
        filename=os.path.basename(output),
        append=kwargs.get("append", False),
    )

    write_docs = kwargs.pop("write_docs", False)
    docs_format = kwargs.pop("docs_format", "default")
    Writer(
        data=data,
        nxdl_f_path=nxdl_f_path,
        output_path=output,
        append=kwargs.get("append", False),
    ).write(write_docs=write_docs, docs_format=docs_format)

    logger.info(f"The output file generated: {output}.")


def parse_params_file(params_file):
    """Parses the parameters from a given dictionary and returns them"""
    params = yaml.load(params_file, Loader=yaml.SafeLoader)["dataconverter"]
    for param in list(params.keys()):
        params[param.replace("-", "_")] = params.pop(param)
    return params
