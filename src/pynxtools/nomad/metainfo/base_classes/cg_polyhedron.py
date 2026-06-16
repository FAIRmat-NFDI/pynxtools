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
# Run `pynx nomad generate-metainfo --nxdl NXcg_polyhedron` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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

__all__ = ["CgPolyhedron"]


class CgPolyhedron(CgPrimitive):
    """
    Computational geometry description of a set of polyhedra in Euclidean
    space.

    Polyhedra or so-called cells (especially in the convex of tessellations)
    are constructed from polygon meshes. Polyhedra may make contact to allow a
    usage of this base class for a description of tessellations.

    For the description of more complicated manifolds and especially for
    polyhedra with holes, users are advised to check if their particular needs
    are described by creating customized instances of an :ref:`NXcg_polygon`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyhedron.html#nxcg_polyhedron"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_polyhedron",
            category="base",
            symbols={
                "c": "The cardinality of the set, i.e. the number of polyhedra.",
                "n_e_total": "The total number of edges for all polyhedra.",
                "n_f_total": "The total number of faces for all polyhedra.",
            },
        ),
    )

    polyhedra = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=("Combined storage of all primitives of all polyhedra."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedra",
            name_type="specified",
            optionality="optional",
        ),
    )
    polyhedronID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each polyhedron."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedronID",
            name_type="partial",
            optionality="optional",
        ),
    )
    polyhedron_half_edgeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_half_edge_data_structure.CgHalfEdgeDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each polygon as a graph."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_half_edge_data_structure",
            name="polyhedron_half_edgeID",
            name_type="partial",
            optionality="optional",
        ),
    )

    number_of_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyhedron.html#nxcg_polyhedron-number-of-faces-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The number of faces for each polyhedron. Faces of adjoining "
            "polyhedra are counted for each polyhedron."
        ),
        a_nexus_field=NeXusField(
            name="number_of_faces",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    face_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyhedron.html#nxcg_polyhedron-face-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("Area of each of faces."),
        a_nexus_field=NeXusField(
            name="face_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    number_of_edges = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyhedron.html#nxcg_polyhedron-number-of-edges-field"
        ],
        description=(
            "The number of edges for each polyhedron. Edges of adjoining "
            "polyhedra are counted for each polyhedron."
        ),
        a_nexus_field=NeXusField(
            name="number_of_edges",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyhedron.html#nxcg_polyhedron-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Length of each edge."),
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
