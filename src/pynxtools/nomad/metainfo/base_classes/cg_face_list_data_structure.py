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
# Run `pynx nomad generate-metainfo --nx-class NXcg_face_list_data_structure` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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

__all__ = ["CgFaceListDataStructure"]


class CgFaceListDataStructure(CgPrimitive):
    """
    Computational geometry of primitives via a face-and-edge-list data
    structure.

    Primitives must neither be degenerated nor self-intersect but can have
    different properties. A face-and-edge-list-based description of primitives
    is frequently used for triangles and polyhedra to store them on disk for
    visualization purposes (see OFF, PLY, VTK, or STL file formats).

    Although this description is storage efficient, it is not well-suited for
    topological analyses. In this case using a half-edge data structure is an
    alternative.

    Having an own base class for the data structure how primitives are stored
    is useful to embrace both users with small or detailed specification
    demands.

    Indices can be used as identifier and thus names for individual instances.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_face_list_data_structure",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 2.",
                "n_v": "The number of vertices.",
                "n_e": "The number of edges.",
                "n_f": "The number of faces.",
                "n_total": "The total number of vertices of all faces. Faces are polygons.",
            },
        ),
    )

    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-number-of-vertices-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Number of vertices for each face. Each entry represents the total "
            "number of vertices for that face, irrespectively whether vertices "
            "are shared among faces or not."
        ),
        a_nexus_field=NeXusField(
            name="number_of_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_edges = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-number-of-edges-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Number of edges for each face. Each entry represents the total "
            "number of edges for that face, irrespectively whether edges are "
            "shared across faces or not."
        ),
        a_nexus_field=NeXusField(
            name="number_of_edges",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-number-of-faces-field"
        ],
        dimensionality="dimensionless",
        description=("Number of faces of the primitives."),
        a_nexus_field=NeXusField(
            name="number_of_faces",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-index-offset-vertex-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "vertices differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of NXcg_primitive for further "
            "details."
        ),
        a_nexus_field=NeXusField(
            name="index_offset_vertex",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset_edge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-index-offset-edge-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "edges differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of NXcg_primitive for further "
            "details."
        ),
        a_nexus_field=NeXusField(
            name="index_offset_edge",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-index-offset-face-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "faces differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of NXcg_primitive for further "
            "details."
        ),
        a_nexus_field=NeXusField(
            name="index_offset_face",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-indices-vertex-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Integer identifier to distinguish all vertices explicitly."),
        a_nexus_field=NeXusField(
            name="indices_vertex",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_edge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-indices-edge-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Integer used to distinguish all edges explicitly."),
        a_nexus_field=NeXusField(
            name="indices_edge",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-indices-face-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Integer used to distinguish all faces explicitly."),
        a_nexus_field=NeXusField(
            name="indices_face",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-vertices-field"
        ],
        shape=["*", "*"],
        description=(
            "Positions of the vertices. Users are encouraged to reduce the "
            "vertices to a unique set as this may result in more efficient "
            "storage. Alternatively, storing vertex positions naively should be "
            "indicated with setting vertices_are_unique to False. Naively means "
            "that each vertex is stored even though many vertices may share the "
            "same positions."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    edges = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-edges-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=("The edges are stored as pairs of vertex identifier."),
        a_nexus_field=NeXusField(
            name="edges",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-faces-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The faces are stored as a concatenated array of vertex identifier "
            "tuples. The first entry is the identifier of the start vertex of "
            "the first face, followed by the second vertex of the first face, "
            "until the last vertex of the first face. Thereafter, the start "
            "vertex of the second face, the second vertex of the second face, "
            "and so on and so forth. Therefore, summating over the "
            "number_of_vertices, allows to extract the vertex identifiers for "
            "the i-th face on the following index interval of the faces array: "
            ":math:`[\\sum_{i = 0}^{i = n-1}, \\sum_{i=0}^{i = n}]`."
        ),
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    vertices_are_unique = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-vertices-are-unique-field"
        ],
        description=(
            "If true, indicates that the vertices are all placed at different "
            "positions and have different identifiers, i.e. no points overlap or "
            "are counted more than once."
        ),
        a_nexus_field=NeXusField(
            name="vertices_are_unique",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    edges_are_unique = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-edges-are-unique-field"
        ],
        description=(
            "If true, indicates that no edge is stored more than once. Users are "
            "encouraged to consider using a half_edge_data_structure instead."
        ),
        a_nexus_field=NeXusField(
            name="edges_are_unique",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    faces_are_unique = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-faces-are-unique-field"
        ],
        description=("If true, indicates that no face is stored more than once."),
        a_nexus_field=NeXusField(
            name="faces_are_unique",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    winding_order = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_face_list_data_structure.html#nxcg_face_list_data_structure-winding-order-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Specifies for each face which winding order was used if any: * 0 - "
            "undefined * 1 - counter-clockwise (CCW) * 2 - clock-wise (CW)"
        ),
        a_nexus_field=NeXusField(
            name="winding_order",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
