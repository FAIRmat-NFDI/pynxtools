"""This module Generate ELN in a hierarchical format according to NEXUS definition."""
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

import click
from pynxtools.eln_mapper.eln import generate_eln
from pynxtools.eln_mapper.scheme_eln import generate_scheme_eln


@click.command()
@click.option(
    "--nxdl",
    required=True,
    help="Name of NeXus definition without extension (.nxdl.xml).",
)
@click.option(
    "--skip-top-levels",
    default=1,
    required=False,
    type=int,
    show_default=True,
    help=(
        "To skip the level of parent hierarchy level. E.g. for default 1 the part "
        "Entry[ENTRY] from /Entry[ENTRY]/Instrument[INSTRUMENT]/... will be skiped."
    ),
)
@click.option(
    "--output-file",
    required=False,
    default="eln_data",
    help=("Name of file that is neede to generated output file."),
)
@click.option(
    "--eln-type",
    required=True,
    type=click.Choice(["eln", "scheme_eln"], case_sensitive=False),
    default="eln",
    help=("Choose a type of ELN output (eln or scheme_eln)."),
)
def get_eln(nxdl: str, skip_top_levels: int, output_file: str, eln_type: str):
    """Helper tool for generating ELN files in YAML format."""
    eln_type = eln_type.lower()
    if eln_type == "eln":
        generate_eln(nxdl, output_file, skip_top_levels)
    elif eln_type == "scheme_eln":
        generate_scheme_eln(nxdl, eln_file_name=output_file)


if __name__ == "__main__":
    get_eln().parse()  # pylint: disable=no-value-for-parameter
