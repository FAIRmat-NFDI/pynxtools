"""This module Generate ELN in Hierarchical format according to NEXUS definition."""
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
from pynxtools.nexus_mapper.eln import generate_eln


@click.command()
@click.option(
    '--nxdl',
    required=True,
    help="Name of NeXus definition without extension (.nxdl.xml)."
)
@click.option(
    '--skip-top-levels',
    default=1,
    help=("To skip the level of parent hierarchy level. E.g. for default 1 the part"
          "Entry[ENTRY] from /Entry[ENTRY]/Instrument[INSTRUMENT]/... will be skiped.")
)
@click.option(
    '--output-file',
    required=True,
    help=('Name of file that is neede to generated output file.')
)
def get_eln_or_json(nxdl: str,
                    skip_top_levels: int,
                    output_file: str):
    """To generate ELN in yaml file format.

    Parameters
    ----------
    nxdl : str
        Name of NeXus definition e.g. NXmpes
    skip_top_levels : int
        To skip hierarchical levels
    output_file : str
        Name of the output file.
    """
    generate_eln(nxdl, output_file, skip_top_levels)


if __name__ == "__main__":
    get_eln_or_json().parse()  # pylint: disable=no-value-for-parameter
