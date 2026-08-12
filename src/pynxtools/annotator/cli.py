# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""CLI command for NeXus file annotation.

Exposes one command consumed by the top-level ``pynx`` group:

``read``
    Inspect a NeXus/HDF5 file, resolve NXDL schema matches, and report
    information about groups, fields, and attributes.
    (``pynx read NEXUS_FILE``).
"""

import logging
import sys

import click

from pynxtools.annotator.annotator import Annotator
from pynxtools.nexus.handler import NexusFileHandler


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
        "NXDL concept path. Finds all HDF5 nodes satisfying an IS-A relation "
        "with the given concept. Two forms: (1) bare class name, e.g. 'NXbeam' "
        "— matches groups by NX_class attribute; (2) appdef path, e.g. "
        "'NXarpes/ENTRY/INSTRUMENT/analyser' — matches groups and fields "
        "via the file's application definition. Fields in base-class-only files "
        "are not supported by form (1). "
    ),
)
def read(nexus_file, documentation, concept):
    """Annotate each group, field, and attribute in a NeXus/HDF5 file with the
    matching NXDL concept path, optionality, and documentation string.

    Without options, the full annotation log for the file is printed.
    Use -d to restrict output to a single HDF5 path, or -c to find all
    instances in the file that correspond to a given NXDL concept path.
    """
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
    logger = logging.getLogger(__file__)
    logger.handlers.clear()
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    NexusFileHandler(nexus_file).process(
        Annotator(logger, documentation=documentation, concept=concept)
    )
