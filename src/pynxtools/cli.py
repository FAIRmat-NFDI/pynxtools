# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
    pynx nomad generate-metainfo      # generate Python NOMAD metainfo classes from NXDL

Legacy entry points (``read_nexus``, ``dataconverter``, ``generate_eln``,
``validate_nexus``) remain installed and emit a deprecation warning.
"""

import click

from pynxtools.annotator.cli import read
from pynxtools.dataconverter.cli import convert, validate
from pynxtools.eln_mapper.cli import generate_eln
from pynxtools.nexus.cli import inspect_appdef
from pynxtools.nomad.cli import nomad


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
pynx.add_command(nomad, name="nomad")
