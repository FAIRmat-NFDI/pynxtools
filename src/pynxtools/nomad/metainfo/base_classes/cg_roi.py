# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_roi (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXcg_roi` to regenerate.
# Hand edits are preserved across regeneration via the sidecar
# generated_manifest.json (add normalize() logic or helper quantities directly).
# See docs/learn/pynxtools/nexus-metainfo-generation.md (Provenance-tracked
# regeneration). `--force` overwrites and discards hand edits.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusChoice,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
    NeXusLink,
)
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgRoi"]


class CgRoi(Object):
    """
    Base class for a region-of-interest (ROI) bound by geometric primitives.

    So-called region-of-interest(s) (ROIs) are typically used to describe a
    region in space (and time) where an observation is made or for which a
    computer simulation is performed with given boundary conditions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_roi.html#nxcg_roi"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_roi",
            category="base",
        ),
    )

    cg_ellipsoid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_ellipsoid.CgEllipsoid",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_ellipsoid",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_cylinder = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_cylinder.CgCylinder",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_parallelogram = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_parallelogram.CgParallelogram",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_parallelogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_hexahedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_hexahedron.CgHexahedron",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_polyhedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
