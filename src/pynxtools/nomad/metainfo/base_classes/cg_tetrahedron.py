# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_tetrahedron (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_tetrahedron` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgTetrahedron"]


class CgTetrahedron(CgPrimitive):
    """
    Computational geometry description of a set of tetrahedra.

    Among hexahedral elements, tetrahedral elements are one of the most
    frequently used geometric primitive for meshing and describing volumetric
    objects in continuum-field simulations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_tetrahedron.html#nxcg_tetrahedron"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_tetrahedron",
            category="base",
            symbols={"c": "The cardinality of the set, i.e. the number of tetrahedra."},
        ),
    )

    tetrahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=("Combined storage of all primitives of all tetrahedra."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="tetrahedra",
            name_type="specified",
            optionality="optional",
        ),
    )
    tetrahedronID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each tetrahedron."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="tetrahedronID",
            name_type="partial",
            optionality="optional",
        ),
    )
    tetrahedron_half_edgeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_half_edge_data_structure.CgHalfEdgeDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each tetrahedron as a graph."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_half_edge_data_structure",
            name="tetrahedron_half_edgeID",
            name_type="partial",
            optionality="optional",
        ),
    )

    face_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_tetrahedron.html#nxcg_tetrahedron-face-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*", 4],
        description=("Area of each of the four triangular faces of each tetrahedron."),
        a_nexus_field=NeXusField(
            name="face_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_tetrahedron.html#nxcg_tetrahedron-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 6],
        description=("Length of each edge of each tetrahedron."),
        a_nexus_field=NeXusField(
            name="edge_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
