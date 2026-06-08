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
# Run `pynx nomad generate-metainfo --nxdl NXsolenoid_magnet` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.log import Log

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SolenoidMagnet"]


class SolenoidMagnet(Component):
    """
    definition for a solenoid magnet.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsolenoid_magnet",
            category="base",
        ),
    )

    read_current = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.solenoid_magnet.SolenoidMagnetReadCurrent",
        repeats=False,
        description=("current read from supply."),
    )
    read_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.solenoid_magnet.SolenoidMagnetReadVoltage",
        repeats=False,
        description=("voltage read from supply."),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-description-field"
        ],
        description=("extended description of the magnet."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    beamline_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-beamline-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "define position of beamline element relative to production target"
        ),
        a_nexus_field=NeXusField(
            name="beamline_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    set_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-set-current-field"
        ],
        dimensionality="[current]",
        description=("current set on supply."),
        a_nexus_field=NeXusField(
            name="set_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class SolenoidMagnetReadCurrent(Log):
    """
    current read from supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-current-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_current",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-current-value-field"
        ],
        dimensionality="[current]",
        a_nexus_field=NeXusField(
            name="value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SolenoidMagnetReadVoltage(Log):
    """
    voltage read from supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-voltage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_voltage",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-voltage-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        a_nexus_field=NeXusField(
            name="value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
