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
# Run `pynx nomad generate-metainfo --nx-class NXmanipulator` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.actuator import Actuator
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Manipulator"]


class Manipulator(Component):
    """
    Base class to describe the use of manipulators and sample stages.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmanipulator",
            category="base",
        ),
    )

    cryostat = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorCryostat",
        repeats=False,
        description=(
            "Cryostat for cooling the sample (and, potentially, the whole manipulator)."
        ),
    )
    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorTemperatureSensor",
        repeats=False,
        description=("Temperature sensor measuring the sample temperature."),
    )
    sample_heater = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorSampleHeater",
        repeats=False,
        description=("Device to heat the sample."),
    )
    drain_current_ammeter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorDrainCurrentAmmeter",
        repeats=False,
        description=(
            "Ammeter measuring the drain current of the sample and sample holder."
        ),
    )
    sample_bias_potentiostat = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorSampleBiasPotentiostat",
        repeats=False,
        description=("Actuator applying a voltage between sample holder and sample."),
    )
    sample_bias_voltmeter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.ManipulatorSampleBiasVoltmeter",
        repeats=False,
        description=(
            "Sensor measuring the voltage applied to sample and sample holder."
        ),
    )
    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        description=(
            "Any additional actuator on the manipulator used to control an "
            "external condition."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        description=(
            "Any additional sensors on the manipulator used to monitor an "
            "external condition."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=True,
        variable=True,
        description=("Class to describe the motors that are used in the manipulator."),
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-name-field"
        ],
        description=("Name of the manipulator."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-description-field"
        ],
        description=("A description of the manipulator."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-type-field"
        ],
        description=("Type of manipulator, Hexapod, Rod, etc."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class ManipulatorCryostat(Actuator):
    """
    Cryostat for cooling the sample (and, potentially, the whole manipulator).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-cryostat-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="cryostat",
            name_type="specified",
            optionality="optional",
        ),
    )

    actuation_target = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-cryostat-actuation-target-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["temperature"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ManipulatorTemperatureSensor(Sensor):
    """
    Temperature sensor measuring the sample temperature.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-temperature-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    measurement = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-temperature-sensor-measurement-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["temperature"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-temperature-sensor-value-field"
        ],
        dimensionality="[temperature]",
        shape=["*"],
        description=(
            "In case of a single or averaged temperature measurement, this is "
            "the scalar temperature measured by the sample temperature sensor. "
            "It can also be a 1D array of measured temperatures (without time "
            "stamps)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ManipulatorSampleHeater(Actuator):
    """
    Device to heat the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-heater-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )

    actuation_target = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-heater-actuation-target-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["temperature"],
        ),
    )
    output_heater_power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-heater-output-heater-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        description=(
            "In case of a fixed or averaged heating power, this is the scalar "
            "heater power. It can also be a 1D array of heater powers (without "
            "time stamps)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="output_heater_power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ManipulatorDrainCurrentAmmeter(Sensor):
    """
    Ammeter measuring the drain current of the sample and sample holder.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-drain-current-ammeter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="drain_current_ammeter",
            name_type="specified",
            optionality="optional",
        ),
    )

    measurement = Quantity(
        type=MEnum(["current"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-drain-current-ammeter-measurement-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["current"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-drain-current-ammeter-value-field"
        ],
        dimensionality="[current]",
        shape=["*"],
        description=(
            "In case of a single or averaged drain current measurement, this is "
            "the scalar drain current measured between the sample and sample "
            "holder. It can also be an 1D array of measured currents (without "
            "time stamps)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ManipulatorSampleBiasPotentiostat(Actuator):
    """
    Actuator applying a voltage between sample holder and sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-bias-potentiostat-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_bias_potentiostat",
            name_type="specified",
            optionality="optional",
        ),
    )

    actuation_target = Quantity(
        type=MEnum(["voltage"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-bias-potentiostat-actuation-target-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["voltage"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ManipulatorSampleBiasVoltmeter(Sensor):
    """
    Sensor measuring the voltage applied to sample and sample holder.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-bias-voltmeter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltmeter",
            name_type="specified",
            optionality="optional",
        ),
    )

    measurement = Quantity(
        type=MEnum(["voltage"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-bias-voltmeter-measurement-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["voltage"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmanipulator.html#nxmanipulator-sample-bias-voltmeter-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        shape=["*"],
        description=(
            "In case of a single or averaged bias measurement, this is the "
            "scalar voltage measured between sample and sample holder. It can "
            "also be an 1D array of measured voltages (without time stamps)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
