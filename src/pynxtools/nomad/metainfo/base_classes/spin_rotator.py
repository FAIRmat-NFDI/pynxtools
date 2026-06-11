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
# Run `pynx nomad generate-metainfo --nxdl NXspin_rotator` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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

__all__ = ["SpinRotator"]


class SpinRotator(Component):
    """
    Base class for a spin rotator.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspin_rotator",
            category="base",
        ),
    )

    read_Bfield_current = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spin_rotator.SpinRotatorReadBfieldCurrent",
        repeats=False,
        description=("current read from magnet supply."),
    )
    read_Bfield_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spin_rotator.SpinRotatorReadBfieldVoltage",
        repeats=False,
        description=("voltage read from magnet supply."),
    )
    read_Efield_current = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spin_rotator.SpinRotatorReadEfieldCurrent",
        repeats=False,
        description=("current read from HT supply."),
    )
    read_Efield_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spin_rotator.SpinRotatorReadEfieldVoltage",
        repeats=False,
        description=("voltage read from HT supply."),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-description-field"
        ],
        description=("Extended description of the spin rotator."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-beamline-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Define position of beamline element relative to production target"
        ),
        a_nexus_field=NeXusField(
            name="beamline_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    set_Bfield_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-set-bfield-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("current set on magnet supply."),
        a_nexus_field=NeXusField(
            name="set_Bfield_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    set_Efield_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-set-efield-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("current set on HT supply."),
        a_nexus_field=NeXusField(
            name="set_Efield_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
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


class SpinRotatorReadBfieldCurrent(Log):
    """
    current read from magnet supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-bfield-current-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_Bfield_current",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-bfield-current-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
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


class SpinRotatorReadBfieldVoltage(Log):
    """
    voltage read from magnet supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-bfield-voltage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_Bfield_voltage",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-bfield-voltage-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
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


class SpinRotatorReadEfieldCurrent(Log):
    """
    current read from HT supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-efield-current-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_Efield_current",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-efield-current-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
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


class SpinRotatorReadEfieldVoltage(Log):
    """
    voltage read from HT supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-efield-voltage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_Efield_voltage",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspin_rotator.html#nxspin_rotator-read-efield-voltage-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
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
