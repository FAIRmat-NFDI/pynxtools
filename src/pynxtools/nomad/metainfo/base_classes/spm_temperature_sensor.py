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
# Run `pynx nomad generate-metainfo --nxdl NXspm_temperature_sensor` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmTemperatureSensor"]


class SpmTemperatureSensor(Sensor):
    """
    The :ref:`NXspm_temperature_sensor` class describes a temperature sensor
    used in scanning probe microscopy (SPM) experiments. It includes fields for
    the temperature measurement, calibration, and associated data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_temperature_sensor",
            category="base",
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensorCalibration",
        repeats=False,
        description=("Calibration of the temperature measurement."),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensorData",
        repeats=True,
        variable=True,
        description=(
            "Data related to the temperature measurement, such as time series "
            "data or voltage-temperature data."
        ),
    )

    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=("The obtained average temperature of the sensor."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    target_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-target-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "The target temperature of the sensor, which is the desired "
            "temperature to be maintained during the experiment."
        ),
        a_nexus_field=NeXusField(
            name="target_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    temp_offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-temp-offset-value-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "The offset temperature of the sensor, which will be added to "
            "obtained correct the measured temperature."
        ),
        a_nexus_field=NeXusField(
            name="temp_offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    TEMPERATUREchannel = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-temperaturechannel-field"
        ],
        variable=True,
        description=(
            "The name of the channel that handles the temperature measurement."
        ),
        a_nexus_field=NeXusField(
            name="TEMPERATUREchannel",
            type="NX_CHAR",
            name_type="partial",
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


class SpmTemperatureSensorCalibration(Calibration):
    """
    Calibration of the temperature measurement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensorCalibrationCalibrationParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="calibration_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmTemperatureSensorCalibrationCalibrationParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-calibration-calibration-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="calibration_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    coefficient = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-calibration-calibration-parameters-coefficient-field"
        ],
        description=("The coefficient of the calibration."),
        a_nexus_field=NeXusField(
            name="coefficient",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmTemperatureSensorData(Data):
    """
    Data related to the temperature measurement, such as time series data or
    voltage-temperature data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    DATA = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-data-data-field"
        ],
        variable=True,
        dimensionality="[temperature]",
        unit="kelvin",
        description=("Temperature data collected during the scan."),
        a_nexus_field=NeXusField(
            name="DATA",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    AXISNAME = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_temperature_sensor.html#nxspm_temperature_sensor-data-axisname-field"
        ],
        variable=True,
        description=("independent axis data like time or position or bias voltage."),
        a_nexus_field=NeXusField(
            name="AXISNAME",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
