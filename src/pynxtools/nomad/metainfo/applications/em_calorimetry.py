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
# Run `pynx nomad generate-metainfo --nxdl NXem_calorimetry` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmCalorimetry"]


class EmCalorimetry(Entry):
    """
    Application definition for minimal example in-situ calorimetry.

    TODO:

    * What is the technique about. * General context. * Literature references.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_calorimetry",
            category="application",
            symbols={
                "n_p": "Number of diffraction pattern.",
                "n_f": "Number of radial integration bins.",
                "n_i": "Number of coordinates along i axis.",
                "n_j": "Number of coordinates along j axis.",
            },
        ),
    )

    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryProfiling",
        repeats=False,
        description=("Details about performance, profiling, etc."),
    )
    program1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryProgram1",
        repeats=False,
        description=("Name of the program whereby this config file was created."),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryEnvironment",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
        ),
    )
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetrySample",
        repeats=False,
    )
    citeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cite.Cite",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcite",
            name="citeID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    diffraction_space = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.coordinate_system.CoordinateSystem",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="diffraction_space",
            name_type="specified",
            optionality="optional",
        ),
    )
    diffraction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryDiffraction",
        repeats=False,
        description=(
            "Reference to the resource which stores acquired pattern from the "
            "experiment or simulation that are analyzed in this workflow. Can "
            "refer to the original EMD or MRC files or the parsed NXem in RDM "
            "e.g. NOMAD OASIS."
        ),
    )
    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryActuator",
        repeats=False,
        description=(
            "Reference to the resource which stores actuator log file from the "
            "experiment."
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryConfig",
        repeats=False,
        description=(
            "Configuration file that was used for parametrizing this analysis workflow."
        ),
    )
    synchronization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetrySynchronization",
        repeats=False,
        description=(
            "Assumptions and computations whereby timestamping data from the "
            "detector and actuator (e.g. heating chip) were synchronized."
        ),
    )
    pattern_center = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryPatternCenter",
        repeats=False,
        description=(
            "Computation of the center for each pattern using e.g. a Circular "
            "Hough Transformation."
        ),
    )
    distortion_correction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryDistortionCorrection",
        repeats=False,
        description=(
            "Elliptical distortion correction as a step when computing the "
            "center for patterns."
        ),
    )
    integration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryIntegration",
        repeats=False,
        description=(
            "Integrated diffraction pattern intensity as a function of radial "
            "distance from the center azimuthally integrated as a function of "
            "time."
        ),
    )
    background_subtraction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryBackgroundSubtraction",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXem_calorimetry"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXem_calorimetry"],
        ),
    )
    identifier_analysis = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-identifier-analysis-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_analysis",
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


class EmCalorimetryProfiling(CsProfiling):
    """
    Details about performance, profiling, etc.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-profiling-start-time-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-profiling-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryProgram1(Program):
    """
    Name of the program whereby this config file was created.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-program1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program1",
            name_type="specified",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-program1-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-program1-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryEnvironmentProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryEnvironmentProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-environment-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-environment-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-environment-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetrySample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="recommended",
        ),
    )

    is_simulation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-sample-is-simulation-field"
        ],
        description=(
            "Qualifier whether the sample is a real (in which case is_simulation "
            "should be set to false) or a virtual one (in which case "
            "is_simulation should be set to true)."
        ),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the specimen. If the specimen substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`. The purpose of the field is to offer research data "
            "management systems an opportunity to parse the relevant elements "
            "without having to interpret these from the resources."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryDiffraction(Note):
    """
    Reference to the resource which stores acquired pattern from the experiment
    or simulation that are analyzed in this workflow.

    Can refer to the original EMD or MRC files or the parsed NXem in RDM e.g.
    NOMAD OASIS.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-diffraction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="diffraction",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-diffraction-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-diffraction-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-diffraction-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryActuator(Note):
    """
    Reference to the resource which stores actuator log file from the
    experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-actuator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="actuator",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-actuator-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-actuator-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-actuator-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryConfig(Note):
    """
    Configuration file that was used for parametrizing this analysis workflow.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-config-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-config-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-config-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetrySynchronization(Process):
    """
    Assumptions and computations whereby timestamping data from the detector
    and actuator (e.g. heating chip) were synchronized.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-synchronization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="synchronization",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-synchronization-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-synchronization-start-time-field"
        ],
        description=(
            "ISO8601 with local time zone reference timestamp that tells with "
            "which delta_time can be converted in timestamp. The reference "
            "timestamp is defined as the time when the actuator started acting "
            "on the sample. Time differences to this timestamp when correlated "
            "signals such as diffraction pattern matching with a specific state "
            "of the sample (e.g. obtained temperature via the actuator) are "
            "reported through delta_time."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_pattern = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-synchronization-indices-pattern-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_pattern",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    delta_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-synchronization-delta-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Time difference to start_time. Collecting diffraction pattern also "
            "takes some time. It is assumed that the acquisition time for each "
            "pattern is substantial shorter than the time it takes the actuator "
            "to cause a change in stimulus (e.g. temperature)."
        ),
        a_nexus_field=NeXusField(
            name="delta_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryPatternCenter(Process):
    """
    Computation of the center for each pattern using e.g. a Circular Hough
    Transformation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-pattern-center-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pattern_center",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-pattern-center-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-pattern-center-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        description=("Computed center for each pattern."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryDistortionCorrection(Process):
    """
    Elliptical distortion correction as a step when computing the center for
    patterns.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-distortion-correction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="distortion_correction",
            name_type="specified",
            optionality="optional",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-distortion-correction-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-distortion-correction-center-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        description=("Computed center for each pattern."),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryIntegration(Process):
    """
    Integrated diffraction pattern intensity as a function of radial distance
    from the center azimuthally integrated as a function of time.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="integration",
            name_type="specified",
            optionality="required",
        ),
    )

    resultBACKGROUND = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em_calorimetry.EmCalorimetryIntegrationResultBACKGROUND",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="resultBACKGROUND",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryIntegrationResultBACKGROUND(Data):
    """
    The integrated intensities:

    * result_with_background * result_without_background
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="resultBACKGROUND",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-intensity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Integrated intensity as a function of time and the radial distance "
            "from the pattern center."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    indices_pattern = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-indices-pattern-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Identifier for each pattern."),
        a_nexus_field=NeXusField(
            name="indices_pattern",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_pattern__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-indices-pattern-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_pattern",
        ),
    )
    s = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-s-field"
        ],
        shape=["*"],
        description=("Positions in reciprocal space."),
        a_nexus_field=NeXusField(
            name="s",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    s__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-s-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="s",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-integration-resultbackground-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("Time since start of the in-situ experiment"),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmCalorimetryBackgroundSubtraction(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-background-subtraction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="background_subtraction",
            name_type="specified",
            optionality="optional",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem_calorimetry.html#nxem_calorimetry-entry-background-subtraction-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
