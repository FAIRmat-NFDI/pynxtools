# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_triangle (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_triangle` to regenerate.
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

__all__ = ["CgTriangle"]


class CgTriangle(CgPrimitive):
    """
    Computational geometry description of a set of triangles.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_triangle.html#nxcg_triangle"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_triangle",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 2.",
                "c": "The cardinality of the set, i.e. the number of triangles.",
                "n_unique": "The number of unique vertices supporting the triangles.",
            },
        ),
    )

    triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=(
            "Combined storage of all primitives of all triangles. This "
            "description resembles the typical representation of primitives in "
            "file formats such as OFF, PLY, VTK, or STL."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangles",
            name_type="specified",
            optionality="optional",
        ),
    )
    triangleID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=(
            "Individual storage of each triangle. Users are advised that using "
            "such individual storage of primitives may be less storage efficient "
            "than creating a combined storage."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangleID",
            name_type="partial",
            optionality="optional",
        ),
    )

    number_of_unique_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_triangle.html#nxcg_triangle-number-of-unique-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of unique vertices in the triangle set."),
        a_nexus_field=NeXusField(
            name="number_of_unique_vertices",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_triangle.html#nxcg_triangle-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Length of the edges of each triangle. For each triangle values are "
            "reported via traversing the vertices in the sequence as these are "
            "defined."
        ),
        a_nexus_field=NeXusField(
            name="edge_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    interior_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_triangle.html#nxcg_triangle-interior-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Interior angles of each triangle. For each triangle values are "
            "reported for the angle opposite to the respective edges in the "
            "sequence how vertices are defined."
        ),
        a_nexus_field=NeXusField(
            name="interior_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
