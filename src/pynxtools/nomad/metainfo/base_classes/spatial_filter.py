# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXspatial_filter (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXspatial_filter` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
