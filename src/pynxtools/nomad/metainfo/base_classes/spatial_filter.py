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
# Run `pynx nomad generate-metainfo --nxdl NXspatial_filter` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpatialFilter"]


class SpatialFilter(Parameters):
    """
    Base class for a spatial filter for objects within a region-of-interest
    (ROI).

    Objects can be points, objects composed from other geometric primitives, or
    objects.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspatial_filter.html#nxspatial_filter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspatial_filter",
            category="base",
            symbols={
                "n_hexahedra": "Number of hexahedra.",
                "n_cylinders": "Number of cylinders.",
                "n_ellipsoids": "Number of ellipsoids.",
                "n_polyhedra": "Number of polyhedra.",
            },
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
    cs_filter_boolean_mask = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask.CsFilterBooleanMask",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    windowing_method = Quantity(
        type=MEnum(["entire_dataset", "union_of_primitives", "bitmask"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspatial_filter.html#nxspatial_filter-windowing-method-field"
        ],
        description=(
            "Qualitative statement which describes the logical operations that "
            "define which objects will be included and which excluded: * "
            "entire_dataset, no filter is applied, all objects are included. * "
            "union_of_primitives, a filter with (possibly non-axis-aligned) "
            "geometric primitives. Objects in or on the surface of the "
            "primitives are included. All other objects are excluded. * bitmask, "
            "a boolean array whose bits encode with 1 which objects are "
            "included. Bits set to zero encode which objects are excluded. Users "
            "of python can use the bitfield operations of the numpy package to "
            "work with bitfields. Multiple instances of NXcg base classes are "
            "used to compose a union_of_primitives."
        ),
        a_nexus_field=NeXusField(
            name="windowing_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["entire_dataset", "union_of_primitives", "bitmask"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
