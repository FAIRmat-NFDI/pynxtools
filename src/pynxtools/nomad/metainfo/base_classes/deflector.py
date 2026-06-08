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
# Run `pynx nomad generate-metainfo --nx-class NXdeflector` to regenerate.
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

__all__ = ["Deflector"]


class Deflector(Component):
    """
    Component of an electron analyzer that deflects the paths of electrons.
    This includes electrostatic and electromagnetic deflectors.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdeflector",
            category="base",
        ),
    )

    type = Quantity(
        type=MEnum(["dipole", "quadrupole", "hexapole", "octupole"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-type-field"
        ],
        description=(
            "Qualitative type of deflector with respect to the number of pole pieces."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["dipole", "quadrupole", "hexapole", "octupole"],
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-name-field"
        ],
        description=(
            "Colloquial or short name for the deflector. For manufacturer names "
            "and identifiers use ``NXfabrication`` and ``identifierNAME``."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Excitation voltage of the deflector. For dipoles it is a single "
            "number. For higher order multipoles, it is an array."
        ),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Excitation current of the deflector. For dipoles it is a single "
            "number. For higher orders, it is an array."
        ),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    offset_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-offset-x-field"
        ],
        dimensionality="[length]",
        description=(
            "Spatial offset of the deflector in x direction (perpendicular to "
            "```offset_y```)."
        ),
        a_nexus_field=NeXusField(
            name="offset_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    offset_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdeflector.html#nxdeflector-offset-y-field"
        ],
        dimensionality="[length]",
        description=(
            "Spatial offset of the deflector in y direction (perpendicular to "
            "```offset_x```)."
        ),
        a_nexus_field=NeXusField(
            name="offset_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
