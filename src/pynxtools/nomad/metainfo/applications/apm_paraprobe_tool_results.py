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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tool_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_common import (
    ApmParaprobeToolCommon,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeToolResults"]


class ApmParaprobeToolResults(Entry):
    """
    Application definition for storing processing results of a tool from the
    paraprobe-toolbox.

    The paraprobe-toolbox is a collection of open-source tools for performing
    efficient analyses of point cloud data where each point can represent atoms
    or (molecular) ions. A key application of the toolbox has been for research
    in the field of Atom Probe Tomography (APT) and related Field Ion
    Microscopy (FIM):

    * `paraprobe-toolbox <https://www.gitlab.com/paraprobe/paraprobe-toolbox>`_
    * `M. Kühbach et al. <https://paraprobe-toolbox.readthedocs.io/en/main/>`_

    The toolbox does not replace but complements existent software tools in
    this research field. Given its capabilities of handling points as objects
    with properties and enabling analyses of the spatial arrangement of and
    inter- sections between geometric primitives, the software can equally be
    used for analyzing data in Materials Science and Materials Engineering.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tool_results",
            category="application",
        ),
    )

    apm_paraprobe_tool_process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsApmParaprobeToolProcess",
        repeats=True,
        variable=True,
        description=("A specific processing result"),
    )
    common = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommon",
        repeats=False,
    )

    definition = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
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


class ApmParaprobeToolResultsApmParaprobeToolProcess(ApmParaprobeToolProcess):
    """
    A specific processing result
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-taskprocessed-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    window = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsApmParaprobeToolProcessWindow",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolResultsApmParaprobeToolProcessWindow(CsFilterBooleanMask):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-taskprocessed-window-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window",
            name_type="specified",
            optionality="required",
        ),
    )

    number_of_ions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-taskprocessed-window-number-of-ions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_ions",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-taskprocessed-window-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-taskprocessed-window-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolResultsCommon(ApmParaprobeToolCommon):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_common",
            name="common",
            name_type="specified",
            optionality="required",
        ),
    )

    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommonConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )
    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommonProgramID",
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
    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommonProfiling",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="recommended",
        ),
    )
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommonUserID",
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
    paraprobe_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results.ApmParaprobeToolResultsCommonParaprobeReferenceFrame",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="paraprobe_reference_frame",
            name_type="specified",
            optionality="required",
        ),
    )

    status = Quantity(
        type=MEnum(["success", "failure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-status-field"
        ],
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["success", "failure"],
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolResultsCommonConfig(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-config-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-config-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-config-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-config-algorithm-field"
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


class ApmParaprobeToolResultsCommonProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-programid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-programid-program-version-attribute"
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


class ApmParaprobeToolResultsCommonProfiling(CsProfiling):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="recommended",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    max_processes = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-max-processes-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="max_processes",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    max_threads = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-max-threads-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="max_threads",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    max_gpus = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-profiling-max-gpus-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="max_gpus",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolResultsCommonUserID(User):
    """
    If used, metadata of at least the person who performed this analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-userid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-userid-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolResultsCommonParaprobeReferenceFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="paraprobe_reference_frame",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["undefined", "cartesian"],
            open_enum=True,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    x_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-x-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="x_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-y-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="y_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    z_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-paraprobe-reference-frame-z-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="z_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
