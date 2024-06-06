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
import json
import logging
import os
import sys
from gettext import gettext
from pathlib import Path
from typing import List, Literal, Optional, Tuple

import click
import lxml.etree as ET
import yaml
from click_default_group import DefaultGroup

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.nexus_tree import generate_tree_from
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against
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


def transfer_data_into_template(
    input_file,
    reader,
    nxdl_name,
    nxdl_root: Optional[ET._Element] = None,
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

    if "ignore_undocumented" in kwargs:
        ignore_undocumented = kwargs["ignore_undocumented"]
        del kwargs["ignore_undocumented"]
    else:
        ignore_undocumented = False

    data = data_reader().read(  # type: ignore[operator]
        template=Template(template), file_paths=input_file, **kwargs
    )
    entry_names = data.get_all_entry_names()
    for entry_name in entry_names:
        helpers.write_nexus_def_to_entry(data, entry_name, nxdl_name)
    if not skip_verify:
        validate_dict_against(
            nxdl_name,
            data,
            ignore_undocumented=ignore_undocumented,
        )
    return data


# pylint: disable=too-many-arguments,too-many-locals,W1203
def convert(
    input_file: Tuple[str, ...],
    reader: str,
    nxdl: str,
    output: str,
    fair: bool = False,
    undocumented: bool = False,
    skip_verify: bool = False,
    required: bool = False,
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

    nxdl_root, nxdl_f_path = helpers.get_nxdl_root_and_path(nxdl)

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


class CustomClickGroup(DefaultGroup):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx) + ctx.command.commands["convert"].params:  # type: ignore
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section(gettext("Options")):
                formatter.write_dl(opts)
        self.format_commands(ctx, formatter)
        with formatter.section(gettext("Info")):
            formatter.write_text(
                "You can see more options by using --help for specific commands. For example: dataconverter generate-template --help"
            )


@click.group(cls=CustomClickGroup, default="convert", default_if_no_args=True)
def main_cli():
    pass


@main_cli.command("convert")
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
    "--ignore-undocumented",
    is_flag=True,
    default=False,
    help="Ignore all undocumented fields during validation.",
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
    fair: bool,
    params_file: str,
    ignore_undocumented: bool,
    undocumented: bool,
    skip_verify: bool,
    mapping: str,
):
    """This command allows you to use the converter functionality of the dataconverter."""
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

    try:
        convert(
            tuple(file_list) + input_file,
            reader,
            nxdl,
            output,
            fair,
            undocumented,
            skip_verify,
            ignore_undocumented=ignore_undocumented,
        )
    except FileNotFoundError as exc:
        raise click.BadParameter(
            f"{nxdl} is not a valid application definition", param_hint="--nxdl"
        ) from exc


@main_cli.command()
@click.option(
    "--nxdl",
    default=None,
    help=("The name of the NXDL file to use without extension. For example: NXmpes"),
    required=True,
)
@click.option(
    "--required",
    help="Use this flag to only get the required template.",
    is_flag=True,
)
@click.option(
    "--pythonic",
    help="Prints a valid Python dictionary instead of JSON",
    is_flag=True,
)
@click.option(
    "--output",
    help="Writes the output into the filepath provided.",
    type=click.Path(),
)
def generate_template(nxdl: str, required: bool, pythonic: bool, output: str):
    "Generates and prints a template to use for your nxdl."

    def write_to_file(text):
        f = open(output, "w")
        f.write(text)
        f.close()

    tree = generate_tree_from(nxdl)

    print_or_write = lambda txt: write_to_file(txt) if output else print(txt)

    level: Literal["required", "recommended", "optional"] = "optional"
    if required:
        level = "required"
    reqs = tree.required_fields_and_attrs_names(level=level)
    template = {
        helpers.convert_nxdl_path_dict_to_data_converter_dict(req): None for req in reqs
    }

    if pythonic:
        print_or_write(str(template))
        return
    print_or_write(
        json.dumps(
            template,
            indent=4,
            sort_keys=True,
            ensure_ascii=False,
        )
    )
