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
# Run `pynx nomad generate-metainfo --nxdl NXcg_primitive` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgPrimitive"]


class CgPrimitive(Object):
    """
    Computational geometry description of a set of primitives in Euclidean
    space.

    Primitives must neither be degenerated nor self-intersect. Individual
    primitives can differ in their properties (e.g. size, shape, rotation).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_primitive",
            category="base",
            symbols={
                "d": "The dimensionality of the embedding space.",
                "c": "The cardinality of the set, i.e. the number of members.",
            },
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

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-depends-on-field"
        ],
        description=(
            "Reference to an instance of :ref:`NXcoordinate_system` in which "
            "these primitives are defined."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The dimensionality of the primitive set with value up to d."),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The cardinality of the primitive set. Value should be equal to c."
        ),
        a_nexus_field=NeXusField(
            name="cardinality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer offset whereby the identifier of the first member of the "
            "set differs from zero. Indices can be used as identifiers and thus "
            "names of instances. Identifiers can be defined either implicitly or "
            "explicitly. For implicit indexing identifiers are defined on the "
            "interval :math:`[index\\_offset, index\\_offset + c - 1]`. "
            "Therefore, implicit identifier are completely defined by the value "
            "of index_offset and cardinality. For example if identifier run from "
            "-2 to 3 the value for index_offset is -2. For explicit indexing the "
            "field identifier has to be used. Fortran-/Matlab- and "
            "C-/Python-style indexing have specific implicit identifier "
            "conventions where index_offset is 1 and 0 respectively."
        ),
        a_nexus_field=NeXusField(
            name="index_offset",
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
    indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-indices-field"
        ],
        shape=["*"],
        description=("Identifier of each member for explicit indexing."),
        a_nexus_field=NeXusField(
            name="indices",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-center-field"
        ],
        shape=["*", "*"],
        description=("The center of each primitive"),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    is_center_of_mass = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-center-of-mass-field"
        ],
        shape=["*"],
        description=("True if the center is a center of mass."),
        a_nexus_field=NeXusField(
            name="is_center_of_mass",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    shape = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-shape-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Shape of each primitive"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Length of each primitive Often the term is associated with the "
            "assumption that one edge is parallel to an axis of the coordinate "
            "system."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-width-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Width of each primitive Often the term is associated with the "
            "assumption that one edge is parallel to an axis of the coordinate "
            "system."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Height of each primitive Often the term is associated with the "
            "assumption that one edge is parallel to an axis of the coordinate "
            "system."
        ),
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    is_closed = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-closed-field"
        ],
        shape=["*"],
        description=(
            "True if primitive is closed such that it has properties like area "
            "or volume."
        ),
        a_nexus_field=NeXusField(
            name="is_closed",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-volume-field"
        ],
        shape=["*"],
        description=(
            "Volume of each primitive. Set to NaN if does not apply for "
            "primitives for which is_closed is False. Volume is an N-D concept "
            "for values of dimensionality larger than 1, Area is an alias for "
            "the two-dimensional case."
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=(
            "Alias for surface_area of each primitive. Set to NaN if does not "
            "apply for primitives for which is_closed is False."
        ),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    orientation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Direction unit vector which points along the longest principal axis "
            "of each primitive. Use the depends_on attribute to specify in which "
            "coordinate system these direction unit vectors are defined."
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    is_mesh = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-mesh-field"
        ],
        description=("Do the primitives define a mesh."),
        a_nexus_field=NeXusField(
            name="is_mesh",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    is_triangle_mesh = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-triangle-mesh-field"
        ],
        description=("Do the primitives define a triangle mesh or not."),
        a_nexus_field=NeXusField(
            name="is_triangle_mesh",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    is_surface_mesh = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-surface-mesh-field"
        ],
        description=("Do the primitives discretize the surface of an object or not."),
        a_nexus_field=NeXusField(
            name="is_surface_mesh",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    is_geodesic_mesh = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-is-geodesic-mesh-field"
        ],
        description=(
            "Do the primitives define a geodesic mesh or not. A geodesic surface "
            "mesh is a triangulated surface mesh with metadata which can be used "
            "as an approximation to describe the surface of a sphere. "
            "Triangulation of spheres are commonly used in Materials Science for "
            "quantifying texture of materials, i.e. the relative rotation of "
            "crystals to sample directions. For additional details or an "
            "introduction into the topic of geodesic meshes see (from which "
            "specifically the section on subdivision schemes is relevant). * `E. "
            "S. Popko and C. J. Kitrick "
            "<https://doi.org/10.1201/9781003134114>`_ Earth scientists have "
            "specific demands and different views about what should be included "
            "in such a base class, given that nested geodesic meshes are a key "
            "component of climate modelling software. For now we propose to use "
            "this base class as a container for organizing data related to "
            "geodesic meshes. Specifically an instance of this base class should "
            "detail the rule set how e.g. a geodesic (surface) mesh was "
            "instantiated as there are many possibilities to do so."
        ),
        a_nexus_field=NeXusField(
            name="is_geodesic_mesh",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_primitive.html#nxcg_primitive-description-field"
        ],
        description=(
            "Possibility to store details such as when primitives form a "
            "(specific) type of mesh such as geodesic meshes."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
