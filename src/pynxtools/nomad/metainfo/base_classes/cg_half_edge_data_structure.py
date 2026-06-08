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
# Run `pynx nomad generate-metainfo --nxdl NXcg_half_edge_data_structure` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import MEnum, Quantity, Section

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgHalfEdgeDataStructure"]


class CgHalfEdgeDataStructure(CgPrimitive):
    """
    Computational geometry description of a half-edge data structure.

    Such a data structure can be used to efficiently circulate around faces and
    iterate over vertices of a planar graph. The data structure is also known
    as a doubly connected edge list.

    Indices can be used as identifier and thus names for individual instances.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_half_edge_data_structure",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 2.",
                "n_v": "The number of vertices.",
                "n_f": "The number of faces.",
                "n_he": "The number of half-edges.",
            },
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-dimensionality-field"
        ],
        dimensionality="dimensionless",
        description=("Dimensionality of the primitives described."),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
    )
    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-number-of-vertices-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-number-of-edges-field"
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
    index_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-index-offset-vertex-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "vertices differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of :ref:`NXcg_primitive` for "
            "further details."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-index-offset-edge-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "edges differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of :ref:`NXcg_primitive` for "
            "further details."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-index-offset-face-field"
        ],
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "faces differs from zero. Identifier can be defined explicitly or "
            "implicitly. Inspect the definition of :ref:`NXcg_primitive` for "
            "further details."
        ),
        a_nexus_field=NeXusField(
            name="index_offset_face",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-position-field"
        ],
        shape=["*", "*"],
        description=("The position of the vertices."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    vertex_incident_half_edge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-vertex-incident-half-edge-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Identifier of the incident half-edge."),
        a_nexus_field=NeXusField(
            name="vertex_incident_half_edge",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    face_half_edge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-face-half-edge-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Identifier of the (starting)/associated half-edge of the face."),
        a_nexus_field=NeXusField(
            name="face_half_edge",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    half_edge_vertex_origin = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-half-edge-vertex-origin-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The identifier of the vertex from which this half-edge is outwards "
            "pointing."
        ),
        a_nexus_field=NeXusField(
            name="half_edge_vertex_origin",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    half_edge_twin = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-half-edge-twin-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Identifier of the associated oppositely pointing half-edge."),
        a_nexus_field=NeXusField(
            name="half_edge_twin",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    half_edge_incident_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-half-edge-incident-face-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "If the half-edge is a boundary half-edge the incident face "
            "identifier is NULL, i.e. 0."
        ),
        a_nexus_field=NeXusField(
            name="half_edge_incident_face",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    half_edge_next = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-half-edge-next-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Identifier of the next half-edge."),
        a_nexus_field=NeXusField(
            name="half_edge_next",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    half_edge_prev = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-half-edge-prev-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Identifier of the previous half-edge."),
        a_nexus_field=NeXusField(
            name="half_edge_prev",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    weinberg_vector = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_half_edge_data_structure.html#nxcg_half_edge_data_structure-weinberg-vector-field"
        ],
        description=(
            "Users are referred to the literature for the background of L. "
            "Weinberg's work about topological characterization of planar "
            "graphs: * `L. Weinberg 1966a, "
            "<https://dx.doi.org/10.1109/TCT.1964.1082216>`_ * `L. Weinberg, "
            "1966b, <https://dx.doi.org/10.1137/0114062>`_ * `E. A. Lazar et al. "
            "<https://doi.org/10.1103/PhysRevLett.109.095505>`_ and how this "
            "work can e.g. be applied in space-filling tessellations of "
            "microstructural objects like crystals/grains."
        ),
        a_nexus_field=NeXusField(
            name="weinberg_vector",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
