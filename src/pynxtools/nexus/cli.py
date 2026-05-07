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
    Annotate and inspect a NeXus/HDF5 file (``pynx read NEXUS_FILE``).

``inspect_appdef``
    List fields of a NeXus application definition by optionality level
    (``pynx inspect-appdef NXDL``).
"""

import logging
import sys
from typing import Literal

import click

from pynxtools.nexus.nexus import HandleNexus


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
    """Annotate a NeXus/HDF5 file with NXDL schema documentation and concept paths."""
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
    logging_format = "%(levelname)s: %(message)s"
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.INFO, format=logging_format, handlers=[stdout_handler]
    )
    logger = logging.getLogger("pynxtools")
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    nexus_helper = HandleNexus(
        logger, nexus_file, d_inq_nd=documentation, c_inq_nd=concept
    )
    nexus_helper.process_nexus_master_file(None)


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
    """List fields of a NeXus application definition.

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
