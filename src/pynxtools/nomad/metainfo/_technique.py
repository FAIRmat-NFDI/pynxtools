# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Ontology technique metadata for generated NeXus entries.

Hand-written (not generated from NXDL): ``Entry.techniques`` points here and
``Entry.normalize`` calls ``add_techniques``. The section is added to the base
classes package in ``_package.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity

from pynxtools.nomad.ontology import (
    add_technique_to_results_eln,
    add_to_results_eln,
    fetch_methods,
    fetch_technique,
    get_ontology_service_info,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

    from pynxtools.nomad.metainfo.base_classes.entry import Entry


class Technique(ArchiveSection):
    """Ontology metadata for the NeXus application definition of an entry,
    fetched from nomad-ontology-service."""

    name = Quantity(
        type=str,
        description="""Name of the resolved NeXus application definition
            (e.g. NXmpes_arpes).""",
    )
    description = Quantity(
        type=str,
        description="""Ontology comment (rdfs:comment) for the resolved NeXus
            application definition.""",
    )
    see_also = Quantity(
        type=str,
        description="""Ontology see-also link (rdfs:seeAlso) for the resolved
            NeXus application definition.""",
    )
    alt_labels = Quantity(
        type=str,
        shape=["*"],
        description="""Alternate labels/synonyms for the resolved NeXus
            application definition.""",
    )
    properties = Quantity(
        type=str,
        shape=["*"],
        description="""Object-property restriction axioms (e.g. ESRFET's
            'can_be_used_for_technique') on the resolved NeXus application
            definition, as 'property: value' strings.""",
    )


def add_techniques(entry: Entry, archive: EntryArchive, logger: BoundLogger) -> None:
    """Fill ``entry.techniques`` and ``archive.results.eln`` from
    nomad-ontology-service, based on the entry's ``definition``.

    Does nothing if the entry has no definition or the service is not available.
    """
    entry.techniques = []
    if not entry.definition:
        return
    info = get_ontology_service_info(logger)
    if info is None:
        return

    class_name = entry.definition.strip()
    methods = fetch_methods(info, class_name, logger)
    add_to_results_eln(
        archive, methods=methods if methods is not None else [class_name]
    )

    technique = fetch_technique(info, class_name, logger)
    if technique is not None:
        entry.techniques.append(Technique(**technique))
        add_technique_to_results_eln(archive, technique)
