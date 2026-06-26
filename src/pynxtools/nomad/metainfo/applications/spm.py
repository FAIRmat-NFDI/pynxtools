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
from pynxtools.nomad.metainfo._category import ExperimentCategory
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
from pynxtools.nomad.metainfo.base_classes.spm_bias_spectroscopy import (
    SpmBiasSpectroscopy,
)
from pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor import SpmPiezoSensor
from pynxtools.nomad.metainfo.base_classes.spm_scan_control import SpmScanControl
from pynxtools.nomad.metainfo.base_classes.spm_scan_pattern import SpmScanPattern
from pynxtools.nomad.metainfo.base_classes.spm_scan_region import SpmScanRegion

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
        categories=[ExperimentCategory],
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXspm",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
    scan_environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentScanEnvironment",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="SCAN_ENVIRONMENT",
            name_type="any",
            optionality="required",
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
    bias_spectroscopy_environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentBiasSpectroscopyEnvironment",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="bias_spectroscopy_environment",
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

    name = Quantity(
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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

    name = Quantity(
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentScanEnvironment(Environment):
    """
    Information of the scan environment holding concept for temperature,
    setpoint (current or height), scan area and scan data.

    Note: At least one field from head_temperature, cryo_bottom_temperature and
    cryo_shield_temperature must be provided.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="SCAN_ENVIRONMENT",
            name_type="any",
            optionality="required",
        ),
    )

    current_sensorTAG = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
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
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
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
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor.SpmPiezoSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="piezo_sensor",
            name_type="specified",
            optionality="optional",
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
    height_piezo_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor.SpmPiezoSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="height_piezo_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )
    spm_scan_control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentScanEnvironmentSpmScanControl",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    head_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-head-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "Temperature (stabilized or target value) of STM head. For array "
            "data of head_temperature, use head_temperature_sensor group."
        ),
        a_nexus_field=NeXusField(
            name="head_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )
    identifier_environment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-identifier-environment-field"
        ],
        description=(
            "Unique identifier for the scan environment defined by the user or "
            "lab. When multiple scans are performed in a single environment "
            "conditions or settings, the entire scan environment can be "
            "differentiated by this identifier. For example, scan on a sample of "
            "TiSe2 with layered of evaporated pyrene and annealed at 300K "
            "temperature for 5 min process."
        ),
        a_nexus_field=NeXusField(
            name="identifier_environment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    cryo_bottom_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-cryo-bottom-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "Temperature (stabilized or targeted single value) of the cold tail "
            "of the cryostat. For array data of cryo_bottom_temperature, use "
            "cryo_bottom_temperature_sensor group."
        ),
        a_nexus_field=NeXusField(
            name="cryo_bottom_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )
    cryo_shield_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-cryo-shield-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "Temperature (stabilized or targeted single value) of liquid "
            "nitrogen shield. For array data of cryo_shield_temperature, use "
            "cryo_shield_temperature_sensor group."
        ),
        a_nexus_field=NeXusField(
            name="cryo_shield_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentScanEnvironmentSpmScanControl(SpmScanControl):
    """
    The scan control information like scan region or phase space, type of scan
    (e.g. mesh, spiral, etc.), and scan speed, etc. This group mainly stores
    the scan settings data. For processed data or final experimental data would
    go to NXdata group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    scan_region = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentScanEnvironmentSpmScanControlScanRegion",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="required",
        ),
    )
    meshSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentScanEnvironmentSpmScanControlMeshSCAN",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="meshSCAN",
            name_type="partial",
            optionality="required",
        ),
    )

    scanTAG = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scantag-field"
        ],
        variable=True,
        description=(
            "If there are multiple scans performed under the same environment, "
            "use this field to differentiate among them."
        ),
        a_nexus_field=NeXusField(
            name="scanTAG",
            type="NX_CHAR",
            name_type="partial",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentScanEnvironmentSpmScanControlScanRegion(SpmScanRegion):
    """
    The scan region (phase space or sub-phase space) is the region where the
    scan is performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="required",
        ),
    )

    scan_range_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-range-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The range of the scan in x direction."),
        a_nexus_field=NeXusField(
            name="scan_range_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_range_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-range-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The range of the scan in y direction."),
        a_nexus_field=NeXusField(
            name="scan_range_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_offset_value_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-offset-value-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The offset of the scan in x direction."),
        a_nexus_field=NeXusField(
            name="scan_offset_value_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_offset_value_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-offset-value-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The offset of the scan in y direction."),
        a_nexus_field=NeXusField(
            name="scan_offset_value_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_angle_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-angle-x-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("The angle of the scan region in x direction."),
        a_nexus_field=NeXusField(
            name="scan_angle_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    scan_angle_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-angle-y-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("The angle of the scan region in y direction."),
        a_nexus_field=NeXusField(
            name="scan_angle_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    scan_start_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-start-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The start of the scan in x direction."),
        a_nexus_field=NeXusField(
            name="scan_start_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_start_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-start-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The start of the scan in y direction."),
        a_nexus_field=NeXusField(
            name="scan_start_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_end_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-end-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The end of the scan in x direction."),
        a_nexus_field=NeXusField(
            name="scan_end_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    scan_end_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-scan-region-scan-end-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The end of the scan in y direction."),
        a_nexus_field=NeXusField(
            name="scan_end_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentScanEnvironmentSpmScanControlMeshSCAN(SpmScanPattern):
    """
    The mesh scan is a common technique used in SPM to scan the surface of the
    sample in a grid pattern.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-meshscan-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="meshSCAN",
            name_type="partial",
            optionality="required",
        ),
    )

    scan_points_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-meshscan-scan-points-x-field"
        ],
        description=("The number of points scanned in x direction."),
        a_nexus_field=NeXusField(
            name="scan_points_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    scan_points_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-meshscan-scan-points-y-field"
        ],
        description=("The number of points scanned in y direction."),
        a_nexus_field=NeXusField(
            name="scan_points_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    step_size_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-meshscan-step-size-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The step size in x direction."),
        a_nexus_field=NeXusField(
            name="step_size_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    step_size_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-scan-environment-spm-scan-control-meshscan-step-size-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The step size in y direction."),
        a_nexus_field=NeXusField(
            name="step_size_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
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
        unit="ampere",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-current-sensortag-offset-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("The offset in the tunneling current between tip and sample."),
        a_nexus_field=NeXusField(
            name="offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        unit="dimensionless",
        description=("The gain of the current sensor."),
        a_nexus_field=NeXusField(
            name="current_gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
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
        unit="volt",
        description=("Voltage measured by sensor."),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-voltage-sensortag-offset-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        unit="dimensionless",
        description=("The gain of the voltage sensor."),
        a_nexus_field=NeXusField(
            name="voltage_gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
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
        unit="m",
        description=("The x position of the piezo."),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The y position of the piezo."),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-piezo-sensor-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The z position of the piezo."),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentBiasSpectroscopyEnvironment(Environment):
    """
    To explain bias and current behavior (sweep measurement especially in STS
    experiment) due to voltage applied to the sample.

    In some experiments, e.g., STM, bias spectroscopy could also be part of the
    measurement setup.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="bias_spectroscopy_environment",
            name_type="specified",
            optionality="optional",
        ),
    )

    spm_bias_spectroscopy = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopy",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_bias_spectroscopy",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopy(SpmBiasSpectroscopy):
    """
    Setup and scan data for continuous measurement of bias voltage on the
    subject of experiment vs tunneling current from probe.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_bias_spectroscopy",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    bias_sweep = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweep",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name="BIAS_SWEEP",
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweep(
    SpmScanControl
):
    """
    The bias voltage sweep is a common technique used to study properties (in
    this case current) in the sample or environment due to change in applied
    bias voltage.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name="BIAS_SWEEP",
            name_type="any",
            optionality="required",
        ),
    )

    scan_region = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweepScanRegion",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="required",
        ),
    )
    linear_sweep = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.spm.SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweepLinearSweep",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="linear_sweep",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweepScanRegion(
    SpmScanRegion
):
    """
    The scan region (phase space or sub-phase space) is the region where the
    scan is performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-scan-region-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="required",
        ),
    )

    scan_start_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-scan-region-scan-start-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="scan_start_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    scan_end_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-scan-region-scan-end-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="scan_end_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    scan_offset_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-scan-region-scan-offset-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("The offset of the bias scan voltage."),
        a_nexus_field=NeXusField(
            name="scan_offset_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    scan_range_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-scan-region-scan-range-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="scan_range_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmInstrumentBiasSpectroscopyEnvironmentSpmBiasSpectroscopyBiasSweepLinearSweep(
    SpmScanPattern
):
    """
    The linear sweep is a common technique used on the substance or sample or
    environment to study the change in the behavior of the sample or substance
    or environment due to change in applied bias voltage.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-linear-sweep-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="linear_sweep",
            name_type="specified",
            optionality="required",
        ),
    )

    scan_points_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-linear-sweep-scan-points-bias-field"
        ],
        a_nexus_field=NeXusField(
            name="scan_points_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    step_size_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-bias-spectroscopy-environment-spm-bias-spectroscopy-bias-sweep-linear-sweep-step-size-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="step_size_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
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
        unit="volt",
        description=("The bias voltage (DC) applied to the sample."),
        a_nexus_field=NeXusField(
            name="bias_voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    bias_offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm.html#nxspm-entry-instrument-sample-bias-voltage-bias-offset-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("Offset value of the bias voltage."),
        a_nexus_field=NeXusField(
            name="bias_offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        unit="kelvin",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
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

    link_to_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="LINK_TO_GROUP",
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

    link_to_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="LINK_TO_GROUP",
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
