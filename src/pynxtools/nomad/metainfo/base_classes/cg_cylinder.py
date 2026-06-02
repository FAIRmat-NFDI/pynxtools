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
# Run `pynx nomad generate-metainfo --nx-class NXcg_cylinder` to regenerate.
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
        shape=["*", "*"],
        description=(
            "A direction vector which is parallel to the cylinder/cone axis and "
            "whose magnitude is the height of the cylinder/cone. The upper_cap "
            "is assumed to represent the end while the lower_cap is assumed to "
            "represent the start of the respective cylinder instances when "
            "inspecting along the direction vector."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        description=("Radius of the cylinder if all have the same radius."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="radius",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_cylinder.html#nxcg_cylinder-radii-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Radii of the cylinder."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=(
            "Radii of the upper circular cap. This field, combined with "
            "lower_cap_radius can be used to describe (eventually truncated) "
            "circular cones."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=(
            "Radii of the upper circular cap. This field, combined with "
            "upper_cap_radius can be used to describe (eventually truncated) "
            "circular cones."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=("Lateral surface area of each cylinder."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=("Area of the upper cap of each cylinder."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=("Area of the lower cap of each cylinder."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description=(
            "Sum of upper and lower cap area and lateral surface area of each cylinder."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="total_surface_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
