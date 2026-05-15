# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Public API for ``pynxtools.nomad.parsers``.

Requires ``nomad-lab`` to be installed.

NomadVisitor
    NexusVisitor implementation that populates a NOMAD EntryArchive from a
    NeXus/HDF5 file.  Used internally by NexusParser.
NexusParser
    NOMAD MatchingParser that parses ``.nxs`` files and writes NeXus data
    into a NOMAD archive.
"""

try:
    from nomad.config.models.plugins import ParserEntryPoint
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

__all__ = ["NomadVisitor", "NexusParser"]

from pynxtools.nomad.parsers.parser import NexusParser, NomadVisitor

class NexusParserEntryPoint(ParserEntryPoint):
    def load(self):
        from pynxtools.nomad.parsers.parser import NexusParser

        return NexusParser(**self.dict())


nexus_parser = NexusParserEntryPoint(
    name="pynxtools parser",
    description="A parser for nexus files.",
    mainfile_name_re=r".*\.nxs",
    mainfile_mime_re="application/x-hdf*",
    aliases=[
        "pynxtools.nomad.entrypoints:nexus_parser",
    ],
)


class NexusParserV2EntryPoint(ParserEntryPoint):
    def load(self):
        from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

        return NexusParserV2(**self.dict())


nexus_parser_v2 = NexusParserV2EntryPoint(
    name="pynxtools parser v2",
    description=(
        "Annotation-based NeXus parser using generated Python metainfo. "
        "Produces archives with new schema structure (no __field suffix, lowercase paths)."
    ),
    mainfile_name_re=r".*\.nxs",
    mainfile_mime_re="application/x-hdf*",
)
