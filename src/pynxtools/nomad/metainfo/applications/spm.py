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
# Run `pynx nomad generate-metainfo --nxdl NXspm` to regenerate.
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
from pynxtools.nomad.metainfo.applications.sensor_scan import (
    SensorScan,
    SensorScanInstrument,
    SensorScanSample,
)
from pynxtools.nomad.metainfo.base_classes.amplifier import Amplifier
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.lockin import Lockin
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor
from pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor import SpmPiezoSensor

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Spm"]


class Spm(SensorScan):
    """
    Scanning Probe Microscopy (SPM) is a branch of microscopy that utilizes a
    physical probe to scan the surface of sample and image it at the atomic
    level.

    The application class NXspm is designed as a skeleton and contains common
    technical concepts for specific SPM sub-techniques such as STM, STS, AFM
    etc. In addition, it can be utilized to describe the SPM experiments
    without further specialization for each sub-technique.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm",
            category="application",
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=True,
        variable=True,
        description=(
            "Define data processing (e.g., data analysis, image processing) "
            "program and associated workflow, software and store results."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmSample",
        repeats=True,
        variable=True,
        description=("The sample information."),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmData",
        repeats=True,
        variable=True,
        description=("The data group."),
    )
    reproducibility_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmReproducibilityIndicators",
        repeats=False,
        description=(
            "The group of indicators (links to the existing fields in different "
            "groups) that measure the reproducibility of the experiment."
        ),
    )
    resolution_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmResolutionIndicators",
        repeats=False,
        description=(
            "The group of indicators (links to the existing fields in different "
            "groups) that are used to measure the resolution of the experiment "
            "results."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXspm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-definition-field"
        ],
        description=("Name of the definition that is used for the application."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXspm"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    experiment_technique = Quantity(
        type=MEnum(["STM", "STS", "AFM"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-experiment-technique-field"
        ],
        description=("The technique of the experiment like STM, STS, AFM."),
        a_nexus_field=NeXusField(
            name="experiment_technique",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["STM", "STS", "AFM"],
        ),
    )
    scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-scan-mode-field"
        ],
        description=(
            "The mode of the scan. The possible options depend on the type of "
            "experiment. For example, in STM, the scan mode could be constant "
            "height or constant current, in AFM, the scan mode could be contact "
            "mode, tapping mode or non-contact mode. For general purpose usage, "
            "all scan modes from its sub-techniques are listed."
        ),
        a_nexus_field=NeXusField(
            name="scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "constant height",
                "constant current",
                "contact mode",
                "tapping mode",
                "peak force tapping mode",
                "non-contact mode",
            ],
            open_enum=True,
        ),
    )
    scan_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-scan-type-field"
        ],
        description=(
            "The type of the scan. It mainly describes how scan probe moves in "
            "the scan region, e.g. forward, backward, or both (if scan is "
            "repeated). Any lab defined scan type"
        ),
        a_nexus_field=NeXusField(
            name="scan_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_experiment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-identifier-experiment-field"
        ],
        description=(
            "The identifier for the experiment which should be unique at least in lab."
        ),
        a_nexus_field=NeXusField(
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which child group contains a path "
            "leading to a :ref:`NXdata` group. It is recommended (as of "
            "NIAC2014) to use this attribute to help define the path to the "
            "default dataset to be visualized upon entry. See "
            "https://www.nexusformat.org/2014_How_to_find_default_data.html for "
            "a summary of the discussion."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_collection = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-identifier-collection-field"
        ],
        description=(
            "The unique identifier for the collection. The identifier is used to "
            "group a number of the experiments run upon the same setup and/or "
            "same sample."
        ),
        a_nexus_field=NeXusField(
            name="identifier_collection",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-experiment-description-field"
        ],
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-start-time-field"
        ],
        description=("The start time of the experiment."),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-end-time-field"
        ],
        description=("The end time of the experiment."),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
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


class SpmInstrument(SensorScanInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    hardware = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentHardware",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="hardware",
            name_type="specified",
            optionality="required",
        ),
    )
    software = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentSoftware",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="software",
            name_type="specified",
            optionality="required",
        ),
    )
    real_time_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.rcs.Rcs",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXrcs",
            name="real_time_controller",
            name_type="specified",
            optionality="recommended",
        ),
    )
    lockin_amplifier = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentLockinAmplifier",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
            optionality="optional",
        ),
    )
    current_sensorTAG = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentCurrent_sensorTAG",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="current_sensorTAG",
            name_type="partial",
            optionality="optional",
        ),
    )
    voltage_sensorTAG = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentVoltage_sensorTAG",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="voltage_sensorTAG",
            name_type="partial",
            optionality="optional",
        ),
    )
    piezo_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentPiezoSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="piezo_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )
    height_piezo_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor.SpmPiezoSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="height_piezo_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    XYZpiezo_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor.SpmPiezoSensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="XYZpiezo_sensor",
            name_type="partial",
            optionality="optional",
        ),
    )
    head_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_temperature_sensor",
            name="head_temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    cryo_bottom_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_temperature_sensor",
            name="cryo_bottom_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )
    cryo_shield_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_temperature_sensor",
            name="cryo_shield_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_temperature_sensor",
            name="sample_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_bias_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentSampleBiasVoltage",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltage",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentHardware(Fabrication):
    """
    The hardware description of core instrument setup of experiment. Usually,
    the entire instrument is supplied by a single manufacturer. To describe the
    hardware from any sub-components, use the ``hardware`` group of that
    sub-component (child group of the NXinstrument group) group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-hardware-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="hardware",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-hardware-name-field"
        ],
        description=("Name of the hardware."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-hardware-vendor-field"
        ],
        description=("Company name of the manufacturer."),
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-hardware-model-field"
        ],
        description=(
            "Version or model of the hardware setup provided by the manufacturer."
        ),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentSoftware(Fabrication):
    """
    The software description of core instrument setup of experiment. Usually,
    the entire instrument is supplied by a single name/manufacturer/model/etc.
    To describe the software from any sub-components, use the ``software``
    group of that component.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-software-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="software",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-software-name-field"
        ],
        description=("Name of the software."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-software-vendor-field"
        ],
        description=("Company name of the manufacturer."),
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-software-model-field"
        ],
        description=("Version or model of the component named by the manufacturer."),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentLockinAmplifier(Lockin):
    """
    The lock-in amplifier information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-lockin-amplifier-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
            optionality="optional",
        ),
    )

    flip_sign = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-lockin-amplifier-flip-sign-field"
        ],
        description=(
            "The sign (1 or -1) that renders the values of the lock-in current "
            "positive. The calibration procedure with retracted tip is normally "
            "performed to compensate for the signal phase delay in SPM. The "
            "procedure yields two possible solutions corresponding to the chosen "
            "phase, this number should be equal to 1 or -1 depending on which "
            "solution is chosen (this concept mainly used in STS experiments)."
        ),
        a_nexus_field=NeXusField(
            name="flip_sign",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    active_channel = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-lockin-amplifier-active-channel-field"
        ],
        description=(
            "The name of the active channel of the lock-in amplifier which is "
            "used for the measurement."
        ),
        a_nexus_field=NeXusField(
            name="active_channel",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentCurrent_sensorTAG(Sensor):
    """
    Information for current sensor. Any current sensor such as a
    current-voltage transimpedance amplifier involved in the experiment or in
    any special measurement or in any specialized experiment component can be
    registered under this group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="current_sensorTAG",
            name_type="partial",
            optionality="optional",
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentCurrent_sensorTAGCalibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )
    amplifier = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentCurrent_sensorTAGAmplifier",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXamplifier",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    NAMEcurrent = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-namecurrent-field"
        ],
        variable=True,
        description=(
            "The name of the current sensor used for specific measurement or in "
            "component."
        ),
        a_nexus_field=NeXusField(
            name="NAMEcurrent",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Name of the current according to the purpose of the measurement. "
            "E.g., the field can be named as tip_current defining the current "
            "measured at the tip."
        ),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_CURRENT",
        ),
    )
    offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-offset-value-field"
        ],
        dimensionality="[current]",
        description=("The offset in the tunneling current between tip and sample."),
        a_nexus_field=NeXusField(
            name="offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentCurrent_sensorTAGCalibration(Calibration):
    """
    Calibration data of the current sensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentCurrent_sensorTAGCalibrationCalibrationParameters",
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


class SpmInstrumentCurrent_sensorTAGCalibrationCalibrationParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-calibration-calibration-parameters-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-calibration-calibration-parameters-coefficient-field"
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


class SpmInstrumentCurrent_sensorTAGAmplifier(Amplifier):
    """
    An amplifier information that amplifies the input signal.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-amplifier-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXamplifier",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    current_gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-amplifier-current-gain-field"
        ],
        dimensionality="dimensionless",
        description=("The gain of the current sensor."),
        a_nexus_field=NeXusField(
            name="current_gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentVoltage_sensorTAG(Sensor):
    """
    The sensor information for the voltage device. Any voltage sensor involved
    in the experiment or in any special measurement or in any specialized
    experiment component can be registered under this group.

    For this purpose, replace the TAG with the specific name or ID of the
    voltage sensor.

    Do not register this group for sample bias voltage (DC), for that we have
    :ref:`sample_bias_voltage
    </NXspm/entry/instrument/sample_bias_voltage-group>` group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="voltage_sensorTAG",
            name_type="partial",
            optionality="optional",
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentVoltage_sensorTAGCalibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )
    amplifier = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentVoltage_sensorTAGAmplifier",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXamplifier",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    NAMEvoltage = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-namevoltage-field"
        ],
        variable=True,
        description=(
            "The name of the voltage according to the purpose of the "
            "measurement. E.g., the field can be named as "
            "x_source_drain_bias_voltage defining the applied bias along the "
            "x-axis as source-drain channel, while current (tip current) will be "
            "measured along the z-axis."
        ),
        a_nexus_field=NeXusField(
            name="NAMEvoltage",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Voltage measured by sensor."),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-offset-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The offset voltage. The real voltage is the sum of the voltage and "
            "the offset voltage."
        ),
        a_nexus_field=NeXusField(
            name="offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentVoltage_sensorTAGCalibration(Calibration):
    """
    Calibration data of the voltage sensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentVoltage_sensorTAGCalibrationCalibrationParameters",
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


class SpmInstrumentVoltage_sensorTAGCalibrationCalibrationParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-calibration-calibration-parameters-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-calibration-calibration-parameters-coefficient-field"
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


class SpmInstrumentVoltage_sensorTAGAmplifier(Amplifier):
    """
    An amplifier information that amplifies the input signal.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-amplifier-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXamplifier",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    voltage_gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-amplifier-voltage-gain-field"
        ],
        dimensionality="dimensionless",
        description=("The gain of the voltage sensor."),
        a_nexus_field=NeXusField(
            name="voltage_gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentPiezoSensor(SpmPiezoSensor):
    """
    This piezo sensor group refers to the XYZ (in all directions) piezo sensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="piezo_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-x-field"
        ],
        dimensionality="[length]",
        description=("The x position of the piezo."),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-y-field"
        ],
        dimensionality="[length]",
        description=("The y position of the piezo."),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-z-field"
        ],
        dimensionality="[length]",
        description=("The z position of the piezo."),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentSampleBiasVoltage(Sensor):
    """
    The DC bias voltage that is applied to the sample (for example in constant-
    current mode in STM).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltage",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentSampleBiasVoltageCalibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    bias_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-bias-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("The bias voltage (DC) applied to the sample."),
        a_nexus_field=NeXusField(
            name="bias_voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )
    bias_offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-bias-offset-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Offset value of the bias voltage."),
        a_nexus_field=NeXusField(
            name="bias_offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentSampleBiasVoltageCalibration(Calibration):
    """
    Calibration of the bias voltage measurement (V/V).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentSampleBiasVoltageCalibrationCalibrationParameters",
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


class SpmInstrumentSampleBiasVoltageCalibrationCalibrationParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-calibration-calibration-parameters-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-calibration-calibration-parameters-coefficient-field"
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


class SpmSample(SensorScanSample):
    """
    The sample information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    sample_environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmSampleSampleEnvironment",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="sample_environment",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmSampleSampleEnvironment(Environment):
    """
    Information of environment around the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-sample-sample-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="sample_environment",
            name_type="specified",
            optionality="optional",
        ),
    )

    sample_bias_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltage",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_temperature_sensor.SpmTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_temperature_sensor",
            name="sample_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-sample-sample-environment-temperature-field"
        ],
        dimensionality="[temperature]",
        description=(
            "The single-valued temperature of the sample, also referred to as "
            "the tip temperature (not head temperature), since the tip and "
            "sample are in contact or in close proximity. For array like "
            "temperature data use sample_temperature_sensor group."
        ),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmData(Data):
    """
    The data group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    DATA = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-data-data-field"
        ],
        variable=True,
        description=(
            "The data (e.g. current, voltage, temperature) field that can be "
            "plotted against the axes."
        ),
        a_nexus_field=NeXusField(
            name="DATA",
            type="NX_NUMBER",
            name_type="any",
            optionality="required",
            units="NX_ANY",
        ),
    )
    AXISNAME = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-data-axisname-field"
        ],
        variable=True,
        description=("The name of the axis that corresponds to the data field."),
        a_nexus_field=NeXusField(
            name="AXISNAME",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmReproducibilityIndicators(Collection):
    """
    The group of indicators (links to the existing fields in different groups)
    that measure the reproducibility of the experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-reproducibility-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="reproducibility_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    LINK_TO_FIELD = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-reproducibility-indicators-link-to-field-field"
        ],
        variable=True,
        description=(
            "A place holder to create link to any field relevant considered as "
            "reproducibility indicators (defined by laboratory)."
        ),
        a_nexus_field=NeXusField(
            name="LINK_TO_FIELD",
            type="NX_CHAR",
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmResolutionIndicators(Collection):
    """
    The group of indicators (links to the existing fields in different groups)
    that are used to measure the resolution of the experiment results.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-resolution-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="resolution_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    LINK_TO_FIELD = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-resolution-indicators-link-to-field-field"
        ],
        variable=True,
        description=(
            "A place holder to create link to any field relevant considered as "
            "reproducibility indicators (defined by laboratory)."
        ),
        a_nexus_field=NeXusField(
            name="LINK_TO_FIELD",
            type="NX_CHAR",
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
