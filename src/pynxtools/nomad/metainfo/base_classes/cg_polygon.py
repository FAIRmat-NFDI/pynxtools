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
# Run `pynx nomad generate-metainfo --nxdl NXcg_polygon` to regenerate.
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

__all__ = ["CgPolygon"]


class CgPolygon(CgPrimitive):
    """
    Computational geometry description of a set of polygons in Euclidean space.

    Polygons are specialized polylines:

    * A polygon is a geometric primitive that is bounded by a closed polyline *
    All vertices of this polyline lay in the d-1 dimensional plane. whereas
    vertices of a polyline do not necessarily lay on a plane. * A polygon has
    at least three vertices.

    Each polygon is built from a sequence of vertices (points with
    identifiers). The members of a set of polygons may have a different number
    of vertices. Sometimes a collection/set of polygons is referred to as a
    soup of polygons.

    As three-dimensional objects, a set of polygons can be used to define the
    hull of what is effectively a polyhedron; however users are advised to use
    the specific :ref:`NXcg_polyhedron` base class if they wish to describe
    closed polyhedra. Even more general complexes can be thought of. An example
    are the so-called piecewise-linear complexes used in the TetGen library.

    As these complexes can have holes though, polyhedra without holes are one
    subclass of such complexes, users should rather design their own base class
    e.g. NXcg_polytope to describe such even more complex primitives instead of
    abusing this base class for such purposes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polygon.html#nxcg_polygon"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_polygon",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be either 2 or 3.",
                "c": "The cardinality of the set, i.e. the number of polygons.",
                "n_total": "The total number of vertices when visiting every polygon.",
            },
        ),
    )

    polygons = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=("Combined storage of all primitives of all polygons."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polygons",
            name_type="specified",
            optionality="optional",
        ),
    )
    polygonID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of the mesh of each polygon."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polygonID",
            name_type="partial",
            optionality="optional",
        ),
    )
    polygon_half_edgeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_half_edge_data_structure.CgHalfEdgeDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each polygon as a graph."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_half_edge_data_structure",
            name="polygon_half_edgeID",
            name_type="partial",
            optionality="optional",
        ),
    )

    number_of_total_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polygon.html#nxcg_polygon-number-of-total-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The total number of vertices in the set."),
        a_nexus_field=NeXusField(
            name="number_of_total_vertices",
            type="NX_UINT",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polygon.html#nxcg_polygon-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("For each polygon its accumulated length along its edges."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polygon.html#nxcg_polygon-interior-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Interior angles for each polygon. There are as many values per "
            "polygon as there are number_of_vertices. The angle is the angle at "
            "the specific vertex, i.e. between the adjoining edges of the vertex "
            "according to the sequence in the polygons array. Usually, the "
            "winding_order field is required to interpret the value."
        ),
        a_nexus_field=NeXusField(
            name="interior_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    shape = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polygon.html#nxcg_polygon-shape-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Curvature type: * 0 - unspecified, * 1 - convex, * 2 - concave"),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
