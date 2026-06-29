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
"""CLI commands for working with NOMAD metainfo.

Exposes one top-level symbol consumed by the ``pynx`` group:

``nomad``
    Click group for all NOMAD metainfo sub-commands (``pynx nomad``).
    Sub-commands: ``generate-metainfo``.
"""

import click

from pynxtools.nomad.converters.cli import generate_metainfo


@click.group()
def nomad():
    """NOMAD integration tools.

    Use ``pynx nomad COMMAND --help`` for details on each sub-command.
    """


nomad.add_command(generate_metainfo, name="generate-metainfo")
