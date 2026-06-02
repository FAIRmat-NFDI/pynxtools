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
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nx-class NXcg_triangle` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
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
        description=("Number of unique vertices in the triangle set."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="number_of_unique_vertices",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_triangle.html#nxcg_triangle-edge-length-field"
        ],
        dimensionality="[length]",
        shape=["*", 3],
        description=(
            "Length of the edges of each triangle. For each triangle values are "
            "reported via traversing the vertices in the sequence as these are "
            "defined."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*", 3],
        description=(
            "Interior angles of each triangle. For each triangle values are "
            "reported for the angle opposite to the respective edges in the "
            "sequence how vertices are defined."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="interior_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
