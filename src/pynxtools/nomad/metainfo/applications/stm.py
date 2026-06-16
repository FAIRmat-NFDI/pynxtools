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
# Run `pynx nomad generate-metainfo --nxdl NXstm` to regenerate.
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
from pynxtools.nomad.metainfo.applications.spm import (
    Spm,
    SpmInstrument,
    SpmReproducibilityIndicators,
    SpmResolutionIndicators,
)
from pynxtools.nomad.metainfo.base_classes.lockin import Lockin

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Stm"]


class Stm(Spm):
    """
    An application definition to describe Scanning Tunneling Microscopy (STM).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXstm",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stm.StmInstrument",
        repeats=True,
        variable=True,
    )
    reproducibility_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stm.StmReproducibilityIndicators",
        repeats=False,
        description=(
            "The group's concepts hold the link to the related concepts that "
            "define the reproducibility of the STM experiment."
        ),
    )
    resolution_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stm.StmResolutionIndicators",
        repeats=False,
        description=(
            "The group's concepts hold the link to the related concepts that "
            "define the resolution of the STM experiment."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXstm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-definition-field"
        ],
        description=("Name of the definition that is used for the STM technique."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXstm"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXstm",
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
    scan_mode = Quantity(
        type=MEnum(["constant height", "constant current"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-scan-mode-field"
        ],
        description=(
            "The mode of the scan that is performed. Two commonly used modes are "
            "constant height mode and constant current mode."
        ),
        a_nexus_field=NeXusField(
            name="scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["constant height", "constant current"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    experiment_technique = Quantity(
        type=MEnum(["STM"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-experiment-technique-field"
        ],
        description=("The specific to STM experiment."),
        a_nexus_field=NeXusField(
            name="experiment_technique",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["STM"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="STM",
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


class StmInstrument(SpmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    lockin_amplifier = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stm.StmInstrumentLockinAmplifier",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StmInstrumentLockinAmplifier(Lockin):
    """
    The lock-in amplifier information. The device is being used to extract the
    very weak signal buried in noisy signals.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-instrument-lockin-amplifier-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
            optionality="required",
        ),
    )

    modulation_signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-instrument-lockin-amplifier-modulation-signal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The type of the signal (voltage or current) subject to modulation."
        ),
        a_nexus_field=NeXusField(
            name="modulation_signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
            enumeration=["voltage", "current", "bias"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StmReproducibilityIndicators(SpmReproducibilityIndicators):
    """
    The group's concepts hold the link to the related concepts that define the
    reproducibility of the STM experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-reproducibility-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="reproducibility_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    BIAS_SWEEP = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_control.SpmScanControl",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name="BIAS_SWEEP",
            name_type="specified",
            optionality="optional",
        ),
    )

    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-reproducibility-indicators-current-field"
        ],
        description=(
            "The tunneling current between tip and sample after application of "
            "bias voltage. This should be a link to "
            "/entry/instrument/current_sensor/current"
        ),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    current_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-reproducibility-indicators-current-offset-field"
        ],
        description=(
            "The offset in tunneling current between tip and sample after "
            "application of bias voltage. This should be a link to "
            "/entry/instrument/current_sensor/current_offset"
        ),
        a_nexus_field=NeXusField(
            name="current_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    modulation_signal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-reproducibility-indicators-modulation-signal-type-field"
        ],
        description=(
            "This is the signal on which the modulation voltage or current will "
            "be added. This should be a link to "
            "/entry/instrument/phase_lock_loop/modulation_signal"
        ),
        a_nexus_field=NeXusField(
            name="modulation_signal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-reproducibility-indicators-reference-frequency-field"
        ],
        description=(
            "The frequency of the sine modulation that is used as a carrier "
            "signal of input signal in lock-in. This should be a link to "
            "/entry/instrument/lockin_amplifier/reference_frequency"
        ),
        a_nexus_field=NeXusField(
            name="reference_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StmResolutionIndicators(SpmResolutionIndicators):
    """
    The group's concepts hold the link to the related concepts that define the
    resolution of the STM experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="resolution_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    spm_scan_control = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_control.SpmScanControl",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    head_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-head-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/head_temperature"
        ),
        a_nexus_field=NeXusField(
            name="head_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    cryo_bottom_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-cryo-bottom-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/cryo_bottom_temperature"
        ),
        a_nexus_field=NeXusField(
            name="cryo_bottom_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    cryo_shield_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-cryo-shield-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/cryo_shield_temperature"
        ),
        a_nexus_field=NeXusField(
            name="cryo_shield_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    modulation_signal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-modulation-signal-type-field"
        ],
        description=(
            "This is the signal on which the modulation voltage or current will "
            "be added. This should be a link to "
            "/entry/instrument/lockin_amplifier/modulation_signal_type"
        ),
        a_nexus_field=NeXusField(
            name="modulation_signal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXstm.html#nxstm-entry-resolution-indicators-reference-frequency-field"
        ],
        description=(
            "The frequency of the sine modulation that is used to modulate the "
            "signal in lock-in. This should be a link to "
            "/entry/instrument/lockin_amplifier/reference_frequency"
        ),
        a_nexus_field=NeXusField(
            name="reference_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
