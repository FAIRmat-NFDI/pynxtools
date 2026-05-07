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
"""CLI commands for NeXus data conversion and validation.

Exposes two top-level symbols consumed by the ``pynx`` group:

``convert``
    Click group for all conversion-related sub-commands (``pynx convert``).
    Invoking it without a sub-command runs the conversion directly.
    Sub-commands: ``generate-template``, ``get-readers``, ``reader-info``.

``validate``
    Standalone command to validate a NeXus HDF5 file (``pynx validate``).
"""

import json
import logging
import os
import sys
from gettext import gettext
from typing import Literal

import click
from click_default_group import DefaultGroup

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.convert import (
    ValidationFailed,
    get_names_of_all_readers,
    get_reader,
    parse_params_file,
)
from pynxtools.dataconverter.convert import convert as _convert
from pynxtools.dataconverter.nexus_tree import generate_tree_from
from pynxtools.dataconverter.validate_file import validate as _validate

logger = logging.getLogger("pynxtools")


class CustomClickGroup(DefaultGroup):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx) + ctx.command.commands["run"].params:  # type: ignore
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section(gettext("Options")):
                formatter.write_dl(opts)
        self.format_commands(ctx, formatter)
        with formatter.section(gettext("Info")):
            formatter.write_text(
                "You can see more options by using --help for specific commands. "
                "For example: pynx convert generate-template --help"
            )


@click.group(
    cls=CustomClickGroup,
    default="run",
    default_if_no_args=True,
)
def convert():
    """Convert data to NeXus."""
    ctx = click.get_current_context()
    if ctx.info_name == "dataconverter":
        click.echo(
            "DeprecationWarning: 'dataconverter' is deprecated. "
            "Use 'pynx convert' instead.",
            err=True,
        )


@convert.command("run")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--input-file",
    default=[],
    multiple=True,
    help=(
        "Deprecated: Please use the positional file arguments instead. The path to the "
        "input data file to read. Repeat for more than one file. default=[] This option "
        "is required if no '--params-file' is supplied."
    ),
)
@click.option(
    "--reader",
    default="json_map",
    type=click.Choice(get_names_of_all_readers(), case_sensitive=False),
    help=(
        "The reader to use. Examples are json_map or readers from a pynxtools plugin. "
        "default='json_map' This option is required if no '--params-file' is supplied."
    ),
)
@click.option(
    "--nxdl",
    default=None,
    help=(
        "The name of the NeXus application definition file to use without the extension "
        "nxdl.xml. This option is required if no '--params-file' is supplied."
    ),
)
@click.option(
    "--output",
    default="output.nxs",
    help="The path to the output NeXus file to be generated. default='output.nxs'",
)
@click.option(
    "--params-file",
    type=click.File("r"),
    default=None,
    help="Allows to pass a .yaml file with all the parameters the converter supports.",
)
@click.option(
    "--ignore-undocumented",
    is_flag=True,
    default=False,
    help="Ignore all undocumented concepts during validation.",
)
@click.option(
    "--fail",
    is_flag=True,
    default=False,
    help="Fail conversion and don't create an output file if the validation fails.",
)
@click.option(
    "--skip-verify",
    is_flag=True,
    default=False,
    help="Skips the verification routine during conversion.",
)
@click.option(
    "--mapping",
    help=(
        "Takes a <name>.mapping.json file and converts data from given input files. "
        "Deprecated. Will be removed in a future release. The --config flag can be used instead."
    ),
)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True),
    default=None,
    help="A json config file for the reader",
)
# pylint: disable=too-many-arguments
def run(
    files: tuple[str, ...],
    input_file: tuple[str, ...],
    reader: str,
    nxdl: str,
    output: str,
    params_file: str,
    ignore_undocumented: bool,
    skip_verify: bool,
    config_file: str,
    fail: bool,
    mapping: str | None,
    **kwargs,
):
    """Convert input files to a NeXus HDF5 file."""
    if params_file:
        try:
            _convert(**parse_params_file(params_file))
            return
        except TypeError as exc:
            sys.tracebacklimit = 0
            raise click.UsageError(
                "Please make sure you have the following entries in your "
                "parameter file:\n\n# NeXusParser Parameter File - v0.0.1"
                "\n\ndataconverter:\n\treader: value\n\tnxdl: value\n\tin"
                "put-file: value"
            ) from exc
    if nxdl is None:
        raise click.UsageError("Missing option '--nxdl'")
    if mapping:
        logger.warning(
            "The --mapping option is deprecated. Please use a config file with the -c argument instead."
        )
        reader = "json_map"
        input_file = input_file + tuple([mapping])

    if config_file:
        kwargs["config_file"] = config_file

    file_list = []
    for file in files:
        if os.path.isdir(file):
            from pathlib import Path

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
        _convert(
            tuple(file_list) + input_file,
            reader,
            nxdl,
            output,
            skip_verify,
            ignore_undocumented=ignore_undocumented,
            fail=fail,
            **kwargs,
        )
    except FileNotFoundError as exc:
        raise click.BadParameter(str(exc)) from exc
    except ValidationFailed as exc:
        raise click.ClickException(
            "Validation failed: No file written because '--fail' was requested."
        ) from exc


@convert.command("generate-template")
@click.argument("nxdl")
@click.option(
    "--required",
    help="Include only required fields.",
    is_flag=True,
)
@click.option(
    "--pythonic",
    help="Print a Python dict instead of JSON.",
    is_flag=True,
)
@click.option(
    "--output",
    help="Write output to this file instead of stdout.",
    type=click.Path(),
)
def generate_template(nxdl: str, required: bool, pythonic: bool, output: str):
    """Print a conversion template for a NeXus application definition.

    NXDL: application definition name, e.g. NXmpes
    """

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


@convert.command("get-readers")
def get_readers():
    """List all installed readers."""
    readers = get_names_of_all_readers()
    logger.info(f"The following readers are currently installed: {readers}.")


@convert.command("reader-info")
@click.argument(
    "reader", type=click.Choice(get_names_of_all_readers(), case_sensitive=False)
)
def reader_info(reader: str):
    """Show supported NXDLs and file extensions for a reader.

    READER: name of the reader to inspect, e.g. json_map
    """
    reader_cls = get_reader(reader)
    instance = reader_cls()  # type: ignore[operator]
    click.echo(f"Reader:  {reader}")
    click.echo(f"Class:   {reader_cls.__name__}")

    nxdls = getattr(reader_cls, "supported_nxdls", [])
    click.echo("\nSupported NXDL definitions:")
    for n in nxdls:
        click.echo(f"  {n}")

    exts = getattr(reader_cls, "supported_file_extensions", None)
    if exts is None:
        exts = sorted(getattr(instance, "extensions", {}).keys())
    if exts:
        click.echo("\nSupported file extensions:")
        for e in sorted(exts):
            click.echo(f"  {e}")

    doc = (reader_cls.__doc__ or "").strip()
    if doc:
        click.echo(f"\nDescription: {doc}")


@click.command()
@click.argument(
    "file",
    type=click.Path(exists=True),
)
@click.option(
    "--ignore-undocumented",
    is_flag=True,
    default=False,
    help="Ignore all undocumented concepts during validation.",
)
def validate(file: str, ignore_undocumented: bool = False):
    """Validate a NeXus HDF5 file against its application definition."""
    ctx = click.get_current_context()
    if ctx.info_name == "validate_nexus":
        click.echo(
            "DeprecationWarning: 'validate_nexus' is deprecated. "
            "Use 'pynx validate' instead.",
            err=True,
        )
    _validate(file, ignore_undocumented)
