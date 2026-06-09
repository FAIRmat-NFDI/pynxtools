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
from pynxtools.nomad.metainfo.applications.sensor_scan import (
    SensorScan,
    SensorScanInstrument,
)
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.data import Data

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
        section_def="pynxtools.nomad.metainfo.base_classes.sample.Sample",
        repeats=True,
        variable=True,
        description=("The sample information."),
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
        ),
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
        section_def="pynxtools.nomad.metainfo.base_classes.lockin.Lockin",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlockin",
            name="lockin_amplifier",
            name_type="specified",
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
