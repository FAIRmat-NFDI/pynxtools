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
"""Top-level ``pynx`` CLI dispatcher.

All pynxtools command-line tools are available under this single entry point::

    pynx read NEXUS_FILE              # annotate and inspect a NeXus/HDF5 file
    pynx convert [files...]           # convert data to NeXus
    pynx convert generate-template    # generate and display a conversion template dictionary
    pynx convert get-readers          # lists all installed readers
    pynx convert reader-info          # show reader capabilities
    pynx validate NEXUS_FILE          # validate a NeXus file against its application definition
    pynx generate-eln                 # generate a reader or NOMAD ELN
    pynx inspect-appdef NXDL          # list fields of an application definition with specific presence constraint

Legacy entry points (``read_nexus``, ``dataconverter``, ``generate_eln``,
``validate_nexus``) remain installed and emit a deprecation warning.
"""

import click

from pynxtools.dataconverter.cli import convert, validate
from pynxtools.eln_mapper.cli import generate_eln
from pynxtools.nexus.cli import inspect_appdef, read


@click.group()
def pynx():
    """pynxtools – NeXus file tools.

    Use ``pynx COMMAND --help`` for details on each sub-command.
    """


pynx.add_command(read, name="read")
pynx.add_command(convert, name="convert")
pynx.add_command(validate, name="validate")
pynx.add_command(generate_eln, name="generate-eln")
pynx.add_command(inspect_appdef, name="inspect-appdef")
