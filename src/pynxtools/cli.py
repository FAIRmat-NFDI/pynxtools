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


class _LazyNomadGroup(click.Group):
    """``pynx nomad`` sub-group, loaded on first use.

    ``pynxtools.nomad`` requires the ``nomad`` extra (``nomad-lab``). Importing
    it eagerly here would make every ``pynx`` invocation, including commands
    unrelated to NOMAD, fail for users who only installed the base package.
    """

    def __init__(self) -> None:
        super().__init__(name="nomad", help="NOMAD integration tools.")

    def _resolve(self) -> click.Group:
        try:
            from pynxtools.nomad.cli import nomad
        except ImportError as exc:
            raise click.ClickException(
                "'pynx nomad' requires the 'nomad' extra. "
                "Install it with: pip install 'pynxtools[nomad]'"
            ) from exc
        return nomad

    def list_commands(self, ctx: click.Context) -> list[str]:
        return self._resolve().list_commands(ctx)

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        return self._resolve().get_command(ctx, cmd_name)


@click.group()
def pynx():
    """pynxtools NeXus file tools.

    Use ``pynx COMMAND --help`` for details on each sub-command.
    """


pynx.add_command(read, name="read")
pynx.add_command(convert, name="convert")
pynx.add_command(validate, name="validate")
pynx.add_command(generate_eln, name="generate-eln")
pynx.add_command(inspect_appdef, name="inspect-appdef")
pynx.add_command(_LazyNomadGroup(), name="nomad")
