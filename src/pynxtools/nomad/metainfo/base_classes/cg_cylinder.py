# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_cylinder (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_cylinder` to regenerate.
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

__all__ = ["CgCylinder"]


class CgCylinder(CgPrimitive):
    """
    Computational geometry description of a set of cylinders or (truncated)
    cones.

    The radius can either be defined in the radii field or by filling the
    upper_cap_radii and lower_cap_radii fields respectively. The latter field
    case can thus be used to represent (truncated) cones.

    It is possible to define only one of the cap_radii fields to represent
    half-open cylinder.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_cylinder",
            category="base",
            symbols={
                "d": "The dimensionality of the space in which the members are assumed embedded.",
                "c": "The cardinality of the set, i.e. the number of members.",
            },
        ),
    )

    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "A direction vector which is parallel to the cylinder/cone axis and "
            "whose magnitude is the height of the cylinder/cone. The upper_cap "
            "is assumed to represent the end while the lower_cap is assumed to "
            "represent the start of the respective cylinder instances when "
            "inspecting along the direction vector."
        ),
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Radius of the cylinder if all have the same radius."),
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Radii of the cylinder."),
        a_nexus_field=NeXusField(
            name="radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    upper_cap_radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-upper-cap-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Radii of the upper circular cap. This field, combined with "
            "lower_cap_radius can be used to describe (eventually truncated) "
            "circular cones."
        ),
        a_nexus_field=NeXusField(
            name="upper_cap_radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    lower_cap_radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-lower-cap-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Radii of the upper circular cap. This field, combined with "
            "upper_cap_radius can be used to describe (eventually truncated) "
            "circular cones."
        ),
        a_nexus_field=NeXusField(
            name="lower_cap_radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    lateral_surface_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-lateral-surface-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("Lateral surface area of each cylinder."),
        a_nexus_field=NeXusField(
            name="lateral_surface_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    upper_cap_surface_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-upper-cap-surface-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("Area of the upper cap of each cylinder."),
        a_nexus_field=NeXusField(
            name="upper_cap_surface_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    lower_cap_surface_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-lower-cap-surface-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("Area of the lower cap of each cylinder."),
        a_nexus_field=NeXusField(
            name="lower_cap_surface_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    total_surface_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-total-surface-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=(
            "Sum of upper and lower cap area and lateral surface area of each cylinder."
        ),
        a_nexus_field=NeXusField(
            name="total_surface_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
