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
# Run `pynx nomad generate-metainfo --nxdl NXcg_hexahedron` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgHexahedron"]


class CgHexahedron(CgPrimitive):
    """
    Computational geometry description of a set of hexahedra in Euclidean
    space.

    This class can also be used to describe cuboids or cubes, axis-aligned or
    not. The class represents different access and description levels to offer
    both applied scientists and computational geometry experts an approach
    whereby different specific views can be implemented using the same base
    class:

    * In the simplest case experimentalists may use this base class to describe
    the dimensions or size of a specimen. In this case the alignment with axes
    is not relevant as eventually only the volume of the specimen is of
    interest. * In many cases, take for example an experiment where a specimen
    was cut out from a specifically deformed piece of material, the orientation
    of the specimen's edges with the experiment coordinate system is of high
    relevance. Examples include knowledge about the specimen edge, whether it
    is parallel to the rolling, the transverse, or the normal direction. *
    While the above-mentioned use cases are sufficient to pinpoint the sample
    within a known laboratory/experiment coordinate system, these descriptions
    are not detailed enough to specify e.g. a CAD model of the specimen. *
    Therefore, groups and fields for an additional, computational-geometry-
    based view of hexahedra is offered to serve additional computational tasks:
    storage-oriented simple views or detailed topological/graph-based
    descriptions.

    Hexahedra are important geometrical primitives, which are among the most
    frequently used elements in finite element meshing/modeling.

    As a specialization of the :ref:`NXcg_primitive` base class hexahedra are
    assumed non-degenerated, closed, and built of polygons that are not
    self-intersecting.

    The term hexahedra will be used throughout this base class but includes the
    special cases cuboid, cube, box, axis-aligned bounding box (AABB), and
    optimal bounding box (OBB).

    An axis-aligned bounding box is a common data object in computational
    science and simulation codes to represent a cuboid whose edges are aligned
    with the base vectors of a coordinate system. As a part of binary trees,
    these data objects are important for making time- as well as
    space-efficient queries of geometric primitives in techniques like
    kd-trees.

    An optimal bounding box is a common data object which provides the best
    tightly fitting box about an arbitrary object. In general, such boxes are
    rotated. Exact and substantially faster in practice approximate algorithms
    exist to compute optimal or near optimal bounding boxes for sets of points.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_hexahedron",
            category="base",
            symbols={"c": "The cardinality of the set, i.e. the number of hexahedra."},
        ),
    )

    vertex_normal = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_unit_normal.CgUnitNormal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="vertex_normal",
            name_type="specified",
            optionality="optional",
        ),
    )
    edge_normal = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_unit_normal.CgUnitNormal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="edge_normal",
            name_type="specified",
            optionality="optional",
        ),
    )
    face_normal = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_unit_normal.CgUnitNormal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="face_normal",
            name_type="specified",
            optionality="optional",
        ),
    )
    hexahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=("Combined storage of all primitives of all hexahedra."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedra",
            name_type="specified",
            optionality="optional",
        ),
    )
    hexahedronID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each hexahedron."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedronID",
            name_type="partial",
            optionality="optional",
        ),
    )
    hexahedron_half_edgeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_half_edge_data_structure.CgHalfEdgeDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each hexahedron as a graph."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_half_edge_data_structure",
            name="hexahedron_half_edgeID",
            name_type="partial",
            optionality="optional",
        ),
    )

    shape = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-shape-field"
        ],
        dimensionality="[length]",
        shape=["*", 3],
        description=("Qualifier for the shape of each hexahedron."),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-length-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "Qualifier that is useful in cases when one edge is longer than all "
            "other edges of the hexahedra. Often the term length is associated "
            "with the assumption that one edge is parallel to an axis of the "
            "coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-width-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "Qualifier often used to describe the extent of an object in the "
            "horizontal direction assuming a specific coordinate system. For the "
            "sake of explicitness quantities like length, width, and height "
            "should not be reported without specifying also the assumed "
            "reference frame."
        ),
        a_nexus_field=NeXusField(
            name="width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-height-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "Qualifier often used to describe the extent of an object in the "
            "vertical direction assuming a specific coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
        description=("Volume of each hexahedron."),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-area-field"
        ],
        dimensionality="[length] ** 2",
        shape=["*"],
        description=("Total (surface) area (of all six faces) of each hexahedron."),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    face_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-face-area-field"
        ],
        dimensionality="[length] ** 2",
        shape=["*", 6],
        description=("Area of each of the six faces of each hexahedron."),
        a_nexus_field=NeXusField(
            name="face_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    is_box = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-is-box-field"
        ],
        shape=["*"],
        description=(
            "Specifies if the hexahedra represent cuboids or cubes eventually "
            "rotated ones but at least not too exotic six-faced polyhedra."
        ),
        a_nexus_field=NeXusField(
            name="is_box",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    is_axis_aligned = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_hexahedron.html#nxcg_hexahedron-is-axis-aligned-field"
        ],
        shape=["*"],
        description=(
            "Only to be used if is_box is present. In this case, this field "
            "describes whether hexahedra are boxes whose primary edges are "
            "parallel to the axes of the coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="is_axis_aligned",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
