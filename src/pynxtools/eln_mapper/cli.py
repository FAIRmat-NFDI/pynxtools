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
"""CLI command for ELN file generation.

Exposes ``generate_eln``, consumed by the top-level ``pynx`` group as
``pynx generate-eln``.
"""

from pathlib import Path

import click

from pynxtools.eln_mapper.eln_mapper import _generate_eln


@click.command()
@click.argument("nxdl")
@click.option(
    "--skip-top-levels",
    default=0,
    required=False,
    type=int,
    show_default=True,
    help=(
        "To skip the level of parent hierarchy level. For example, by default the part "
        "Entry[ENTRY] from /Entry[ENTRY]/Instrument[INSTRUMENT]/... will be skipped."
    ),
)
@click.option(
    "--output-file",
    required=False,
    default=None,
    help=("Name of file that is needed to generated output file."),
)
@click.option(
    "--eln-type",
    required=True,
    type=click.Choice(["reader", "schema"], case_sensitive=False),
    default="eln",
    help=("Choose a type of ELN output (reader or schema)."),
)
@click.option(
    "--optionality",
    required=False,
    type=click.Choice(["required", "recommended", "optional"], case_sensitive=False),
    default="required",
    help=(
        "Level of requiredness to generate. If any of ('required', 'recommended', 'optional', "
        "only those concepts matching this requiredness level are created."
    ),
)
@click.option(
    "--filter-file",
    required=False,
    default=None,
    help=(
        "JSON configuration file to filter NeXus concepts (based on the presence of the '@eln' keyword). "
        "This is a positive filter, i.e., all concepts in the filter file will be included in the ELN."
    ),
)
def generate_eln(
    nxdl: str,
    skip_top_levels: int,
    output_file: str | None,
    eln_type: str,
    optionality: str | None,
    filter_file: str | Path | None,
):
    """Generate an ELN YAML scaffold for a NeXus application definition.

    NXDL: application definition name, e.g. NXmpes
    """
    ctx = click.get_current_context()
    if ctx.info_name == "generate_eln":
        click.echo(
            "DeprecationWarning: 'generate_eln' is deprecated. "
            "Use 'pynx generate-eln' instead.",
            err=True,
        )
    _generate_eln(
        nxdl, skip_top_levels, output_file, eln_type, optionality, filter_file
    )
