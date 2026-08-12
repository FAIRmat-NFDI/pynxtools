# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
