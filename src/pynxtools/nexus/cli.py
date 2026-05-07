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
"""CLI commands for NeXus file inspection.

Exposes two commands consumed by the top-level ``pynx`` group:

``read``
    Inspect a NeXus/HDF5 file, resolve NXDL schema matches, and report
    information about groups, fields, and attributes.
    (``pynx read NEXUS_FILE``).

``inspect_appdef``
    List fields of a NeXus application definition by optionality level
    (``pynx inspect-appdef NXDL``).
"""

import logging
from typing import Literal

import click

from pynxtools.nexus.annotation import Annotator
from pynxtools.nexus.handler import NexusFileHandler


@click.command()
@click.argument("nexus_file", required=False, default=None, metavar="NEXUS_FILE")
@click.option(
    "-d",
    "--documentation",
    required=False,
    default=None,
    help=(
        "Definition path in nexus output (.nxs) file. Returns debug "
        "log relevant with that definition path. Example input: /entry/data/delays"
    ),
)
@click.option(
    "-c",
    "--concept",
    required=False,
    default=None,
    help=(
        "Concept path from application definition file (.nxdl.xml). Finds out "
        "all the available concept definition (IS-A relation) for a given "
        "concept path. Example input: /NXarpes/ENTRY/INSTRUMENT/analyser"
    ),
)
def read(nexus_file, documentation, concept):
    """Annotate each group, field, and attribute in a NeXus/HDF5 file with the
    matching NXDL concept path, optionality, and documentation string.

    Without options, the full annotation log for the file is printed.
    Use -d to restrict output to a single HDF5 path, or -c to find all
    instances in the file that correspond to a given NXDL concept path.
    """
    ctx = click.get_current_context()
    if ctx.info_name == "read_nexus":
        click.echo(
            "DeprecationWarning: 'read_nexus' is deprecated. Use 'pynx read' instead.",
            err=True,
        )
    if documentation and concept:
        raise click.UsageError(
            "Only one option either documentation (-d) or is_a relation "
            "with a concept (-c) can be requested."
        )
    logger = logging.getLogger("pynxtools")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    NexusFileHandler(nexus_file).process(
        Annotator(logger, documentation=documentation, concept=concept)
    )


@click.command("inspect-appdef")
@click.argument("nxdl")
@click.option(
    "--level",
    type=click.Choice(["required", "recommended", "optional"]),
    default="required",
    show_default=True,
    help="Minimum optionality level to include.",
)
def inspect_appdef(
    nxdl: str, level: Literal["required", "recommended", "optional"] = "required"
):
    """List the concept paths defined in a NeXus application definition.

    Prints all paths at or above the requested optionality level (required,
    recommended, or optional). Useful for understanding what data must be
    provided before converting with ``pynx convert``, or as a lightweight
    alternative to ``pynx convert generate-template`` when you only need
    the field names rather than a fillable JSON skeleton.

    NXDL: application definition name, e.g. NXmpes
    """
    from pynxtools.dataconverter.nexus_tree import generate_tree_from
    from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_app_defs_names

    available = get_app_defs_names()
    if nxdl not in available:
        raise click.BadParameter(
            f"'{nxdl}' is not a known application definition.\n"
            f"Available: {', '.join(sorted(available))}",
            param_hint="NXDL",
        )
    tree = generate_tree_from(nxdl)
    fields = tree.required_fields_and_attrs_names(level=level)
    click.echo(f"{nxdl}  [{level}+]")
    for field in fields:
        click.echo(f"  {field}")
