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
# Run `pynx nomad generate-metainfo --nx-class NXfresnel_zone_plate` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["FresnelZonePlate"]


class FresnelZonePlate(Component):
    """
    A fresnel zone plate
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfresnel_zone_plate",
            category="base",
        ),
    )

    focus_parameters = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-focus-parameters-field"
        ],
        shape=["*"],
        description=(
            "list of polynomial coefficients describing the focal length of the "
            "zone plate, in increasing powers of photon energy, that describes "
            "the focal length of the zone plate (in microns) at an X-ray photon "
            "energy (in electron volts)."
        ),
        a_nexus_field=NeXusField(
            name="focus_parameters",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    outer_diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-outer-diameter-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="outer_diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    outermost_zone_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-outermost-zone-width-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="outermost_zone_width",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    central_stop_diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-central-stop-diameter-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="central_stop_diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    fabrication_quantity = Quantity(
        type=MEnum(["etched", "plated", "zone doubled", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-fabrication-field"
        ],
        description=("how the zone plate was manufactured"),
        a_nexus_field=NeXusField(
            name="fabrication",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["etched", "plated", "zone doubled", "other"],
        ),
    )
    zone_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-zone-height-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="zone_height",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    zone_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-zone-material-field"
        ],
        description=("Material of the zones themselves"),
        a_nexus_field=NeXusField(
            name="zone_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    zone_support_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-zone-support-material-field"
        ],
        description=(
            "Material present between the zones. This is usually only present "
            'for the "zone doubled" fabrication process'
        ),
        a_nexus_field=NeXusField(
            name="zone_support_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    central_stop_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-central-stop-material-field"
        ],
        a_nexus_field=NeXusField(
            name="central_stop_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    central_stop_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-central-stop-thickness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="central_stop_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    mask_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-mask-thickness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="mask_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    mask_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-mask-material-field"
        ],
        description=(
            "If no mask is present, set mask_thickness to 0 and omit the "
            "mask_material field"
        ),
        a_nexus_field=NeXusField(
            name="mask_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    support_membrane_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-support-membrane-material-field"
        ],
        a_nexus_field=NeXusField(
            name="support_membrane_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    support_membrane_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-support-membrane-thickness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="support_membrane_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfresnel_zone_plate.html#nxfresnel_zone_plate-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a fresnel "
            "zone plate."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
