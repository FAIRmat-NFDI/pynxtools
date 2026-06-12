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
# Run `pynx nomad generate-metainfo --nxdl NXsts` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.spm import (
    Spm,
    SpmInstrument,
    SpmReproducibilityIndicators,
    SpmResolutionIndicators,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Sts"]


class Sts(Spm):
    """
    An application definition to describe Scanning Tunneling Spectroscopy
    (STS).

    NXsts is an extension of NXspm.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsts",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sts.StsInstrument",
        repeats=True,
        variable=True,
    )
    reproducibility_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sts.StsReproducibilityIndicators",
        repeats=False,
        description=(
            "The group's concepts hold the link to the related concepts that "
            "define the reproducibility of the STM experiment."
        ),
    )
    resolution_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sts.StsResolutionIndicators",
        repeats=False,
        description=(
            "The group's concepts hold the link to the related concepts that "
            "define the resolution of the STM experiment."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXsts"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-definition-field"
        ],
        description=("Name of the definition that is used for the application."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsts"],
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
        type=MEnum(["STS"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-experiment-technique-field"
        ],
        description=("The specific to STM experiment."),
        a_nexus_field=NeXusField(
            name="experiment_technique",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["STS"],
        ),
    )
    scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-scan-mode-field"
        ],
        description=(
            "The mode between the tip and sample of the tunneling spectroscopy "
            "experiment."
        ),
        a_nexus_field=NeXusField(
            name="scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["constant height", "constant current", "constant spacing"],
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


class StsInstrument(SpmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-instrument-group"
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
        section_def="pynxtools.nomad.metainfo.base_classes.lockin.Lockin",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StsReproducibilityIndicators(SpmReproducibilityIndicators):
    """
    The group's concepts hold the link to the related concepts that define the
    reproducibility of the STM experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="reproducibility_indicators",
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

    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-current-field"
        ],
        description=(
            "The tunneling current between tip and sample after application of "
            "bias voltage. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/current_sensorTAG/current Note: group name "
            "(could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the square bracket would be the `exact` name "
            "of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    current_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-current-offset-field"
        ],
        description=(
            "The offset in tunneling current between tip and sample after "
            "application of bias voltage. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/current_sensorTAG[current_sensor*]/current_offset "
            "Note: group name (could be any meaningful and relevant name e.g. "
            "entry in ENTRY[entry]) inside the square bracket would be the "
            "`exact` name of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="current_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    current_gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-current-gain-field"
        ],
        description=(
            "Proportional relationship between the probe output voltage and the "
            "actual tunneling current when measuring the tunneling current. This "
            "should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/current_sensorTAG[current_sensor*]/amplifier/current_gain "
            "Note: group name (could be any meaningful and relevant name e.g. "
            "entry in ENTRY[entry]) inside the square bracket would be the "
            "`exact` name of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="current_gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    modulation_signal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-modulation-signal-type-field"
        ],
        description=(
            "This is the signal on which the modulation voltage or current will "
            "be added. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/lockin_amplifier/modulation_signal_type "
            "Note: group name (could be any meaningful and relevant name e.g. "
            "entry in ENTRY[entry]) inside the square bracket would be the "
            "`exact` name of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="modulation_signal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-reproducibility-indicators-reference-frequency-field"
        ],
        description=(
            "The frequency of the sine modulation that is used as carrier signal "
            "of input signal in lock-in. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/lockin_amplifier/reference_frequency Note: "
            "group name (could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the square bracket would be the `exact` name "
            "of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="reference_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StsResolutionIndicators(SpmResolutionIndicators):
    """
    The group's concepts hold the link to the related concepts that define the
    resolution of the STM experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-head-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/head_temperature Note: group "
            "name (could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the square bracket would be the `exact` name "
            "of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="head_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    cryo_bottom_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-cryo-bottom-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/cryo_bottom_temperature Note: "
            "group name (could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the square bracket would be the `exact` name "
            "of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="cryo_bottom_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    cryo_shield_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-cryo-shield-temperature-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/scan_environment/cryo_shield_temperature Note: "
            "group name (could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the square bracket would be the `exact` name "
            "of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="cryo_shield_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    modulation_signal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-modulation-signal-type-field"
        ],
        description=(
            "This is the signal on which the modulation voltage or current will "
            "be added. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/lockin_amplifier/modulation_signal_type "
            "Note: group name (could be any meaningful and relevant name e.g. "
            "entry in ENTRY[entry]) inside the square bracket would be the "
            "`exact` name of the NXentry group."
        ),
        a_nexus_field=NeXusField(
            name="modulation_signal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    modulation_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts-entry-resolution-indicators-modulation-frequency-field"
        ],
        description=(
            "The frequency of the sine modulation that is used to modulate the "
            "signal in lock-in. This should be a link to "
            "/ENTRY[*]/INSTRUMENT[*]/lockin_amplifier/modulation_frequency Note: "
            "group name (could be any meaningful and relevant name e.g. entry in "
            "ENTRY[entry]) inside the"
        ),
        a_nexus_field=NeXusField(
            name="modulation_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
