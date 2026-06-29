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
# Run `pynx nomad generate-metainfo --nxdl NXafm` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.spm_cantilever import SpmCantilever
from pynxtools.nomad.metainfo.base_classes.spm_cantilever_oscillator import (
    SpmCantileverOscillator,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Afm"]


class Afm(Spm):
    """
    An application definition to describe atomic force microscopy (AFM).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXafm",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmInstrument",
        repeats=True,
        variable=True,
    )
    reproducibility_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmReproducibilityIndicators",
        repeats=False,
        description=(
            "The group of indicators (links to the existing fields in different "
            "groups) that measure the reproducibility of the experiment."
        ),
    )
    resolution_indicators = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmResolutionIndicators",
        repeats=False,
        description=(
            "The group of indicators (links to the existing fields in different "
            "groups) that"
        ),
    )

    definition = Quantity(
        type=MEnum(["NXafm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-definition-field"
        ],
        description=("Name of the definition that is used for the application."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXafm"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXafm",
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
        type=MEnum(["AFM"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-experiment-technique-field"
        ],
        description=("The AFM technique."),
        a_nexus_field=NeXusField(
            name="experiment_technique",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["AFM"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="AFM",
        ),
    )
    scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-scan-mode-field"
        ],
        description=(
            "The mode of the scan. contact mode: Cantilever attempts to move on "
            "the sample surface in very close contact with the sample. The "
            "cantilever deflection is usually employed to control the cantilever "
            "position using a PID feedback loop. non-contact mode: Cantilever "
            "attempts to oscillate above the sample surface. Cantilever attempts "
            "to stay in the interaction (atomic force) zone therefore cantilever "
            "oscillator amplitude and frequency are deformed. The cantilever "
            "frequency or oscillation amplitude is usually employed to control "
            "the cantilever position using a PID feedback loop. tapping mode: "
            "Resembles to the non-contact mode, but at every point of scan the "
            'cantilever tip comes closer to the sample surface ("taps it"). '
            "The cantilever oscillation amplitude is usually employed to control "
            "the cantilever position using a PID feedback loop. peak force "
            "tapping mode: Like the tapping mode, but at each point of the scan "
            "force-distance curve is recorded. The maximum force is usually "
            "employed to control the cantilever position using a PID feedback "
            "loop."
        ),
        a_nexus_field=NeXusField(
            name="scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "contact mode",
                "tapping mode",
                "non-contact mode",
                "peak force tapping mode",
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
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class AfmInstrument(SpmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    photo_detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmInstrumentPhotoDetector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="photo_detector",
            name_type="specified",
            optionality="optional",
        ),
    )
    spm_cantilever = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmInstrumentSpmCantilever",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    phase_lock_loop = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.phase_lock_loop.PhaseLockLoop",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXphase_lock_loop",
            name="phase_lock_loop",
            name_type="specified",
            optionality="recommended",
        ),
    )
    scan_environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmInstrumentScanEnvironment",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="SCAN_ENVIRONMENT",
            name_type="any",
            optionality="required",
        ),
    )
    head_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="head_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmInstrumentPhotoDetector(Detector):
    """
    Information about the quadrant photodiode deflection detector or
    interferometer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-photo-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="photo_detector",
            name_type="specified",
            optionality="optional",
        ),
    )

    sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmInstrumentSpmCantilever(SpmCantilever):
    """
    The cantilever information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-spm-cantilever-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    cantilever_oscillator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.afm.AfmInstrumentSpmCantileverCantileverOscillator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever_oscillator",
            name="cantilever_oscillator",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmInstrumentSpmCantileverCantileverOscillator(SpmCantileverOscillator):
    """
    When a cantilever is oscillated close to its resonance, this describes the
    oscillator properties.

    A cantilever can be used in direct contact mode to detect interaction
    forces or oscillated close to its resonance frequency. Changes in the
    oscillation amplitude, phase (between oscillated tail and moving tip) or
    resonance frequency are very sensitive to changes in the interaction
    potential field, giving rise of various measurement modes, such as
    non-contact or intermittent-contact (tapping) modes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-spm-cantilever-cantilever-oscillator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever_oscillator",
            name="cantilever_oscillator",
            name_type="specified",
            optionality="recommended",
        ),
    )

    reference_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-spm-cantilever-cantilever-oscillator-reference-amplitude-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="reference_amplitude",
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
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-spm-cantilever-cantilever-oscillator-reference-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        a_nexus_field=NeXusField(
            name="reference_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    reference_phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-spm-cantilever-cantilever-oscillator-reference-phase-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="reference_phase",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmInstrumentScanEnvironment(Environment):
    """
    The environment information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-instrument-scan-environment-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="SCAN_ENVIRONMENT",
            name_type="any",
            optionality="required",
        ),
    )

    XYpiezo_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_sensor.SpmPiezoSensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_sensor",
            name="XYpiezo_sensor",
            name_type="partial",
            optionality="optional",
        ),
    )
    head_temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="head_temperature_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmReproducibilityIndicators(SpmReproducibilityIndicators):
    """
    The group of indicators (links to the existing fields in different groups)
    that measure the reproducibility of the experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-reproducibility-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="reproducibility_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    cantilever_oscillator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_cantilever_oscillator.SpmCantileverOscillator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever_oscillator",
            name="cantilever_oscillator",
            name_type="specified",
            optionality="optional",
        ),
    )

    head_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-reproducibility-indicators-head-temperature-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-reproducibility-indicators-cryo-bottom-temperature-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-reproducibility-indicators-cryo-shield-temperature-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class AfmResolutionIndicators(SpmResolutionIndicators):
    """
    The group of indicators (links to the existing fields in different groups)
    that
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="resolution_indicators",
            name_type="specified",
            optionality="optional",
        ),
    )

    head_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-head-temperature-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-cryo-bottom-temperature-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-cryo-shield-temperature-field"
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
    cantilever_config = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-cantilever-config-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/cantilever_spm/cantilever_config"
        ),
        a_nexus_field=NeXusField(
            name="cantilever_config",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    amplitude_excitation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXafm.html#nxafm-entry-resolution-indicators-amplitude-excitation-field"
        ],
        description=(
            "This should be a link to "
            "/entry/instrument/phase_lock_loop/amplitude_excitation"
        ),
        a_nexus_field=NeXusField(
            name="amplitude_excitation",
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
