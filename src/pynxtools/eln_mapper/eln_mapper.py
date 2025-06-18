"""This module generates ELN file in a hierarchical format according to a NeXus application definition."""
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

from pathlib import Path
from typing import Optional, Union

import click

from pynxtools.eln_mapper.reader_eln import ReaderElnGenerator
from pynxtools.eln_mapper.schema_eln import NomadElnGenerator


@click.command()
@click.option(
    "--nxdl",
    required=True,
    help="Name of NeXus definition without extension (.nxdl.xml).",
)
@click.option(
    "--skip-top-levels",
    default=0,
    required=False,
    type=int,
    show_default=True,
    help=(
        "To skip the level of parent hierarchy level. For example, by default the part "
        "Entry[ENTRY] from /Entry[ENTRY]/Instrument[INSTRUMENT]/... will be skiped."
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
def get_eln(
    nxdl: str,
    skip_top_levels: int,
    output_file: Optional[str],
    eln_type: str,
    optionality: Optional[str],
    filter_file: Optional[Union[str, Path]],
):
    """Helper tool for generating ELN files in YAML format."""
    filter = None
    if filter_file:
        filter = []
        from pynxtools.dataconverter.readers.utils import parse_flatten_json

        filter_dict = parse_flatten_json(filter_file)
        for key, value in filter_dict.items():
            if isinstance(value, list):
                if any(
                    isinstance(item, str) and item.startswith("@eln") for item in value
                ):
                    filter += [key]
            elif isinstance(value, str):
                if value.startswith("@eln"):
                    filter += [key]

    eln_type = eln_type.lower()

    eln_generator: Union[ReaderElnGenerator, NomadElnGenerator]

    if eln_type == "reader":
        eln_generator = ReaderElnGenerator(
            nxdl, output_file, skip_top_levels, optionality, filter
        )
    elif eln_type == "schema":
        eln_generator = NomadElnGenerator(
            nxdl, output_file, skip_top_levels, optionality, filter
        )

    eln_generator.generate_eln()


if __name__ == "__main__":
    get_eln().parse()  # pylint: disable=no-value-for-parameter
