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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_tool_common` to regenerate.
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

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeToolCommon"]


class ApmParaprobeToolCommon(Object):
    """
    Base class documenting organizational metadata used by all tools of the
    paraprobe-toolbox.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tool_common",
            category="base",
        ),
    )

    config = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "The configuration file that was used to parameterize the algorithms "
            "that this tool has executed."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="optional",
        ),
    )
    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
        ),
    )
    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_common.ApmParaprobeToolCommonProfiling",
        repeats=False,
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
        ),
    )
    NAMED_reference_frameID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.coordinate_system.CoordinateSystem",
        repeats=True,
        variable=True,
        description=(
            "Details about coordinate systems (reference frames) used. In atom "
            "probe several coordinate systems have to be distinguished. Names of "
            "instances of such :ref:`NXcoordinate_system` should be documented "
            "explicitly and doing so by picking from the following controlled "
            "set of names: * paraprobe_reference_frame * lab_reference_frame * "
            "specimen_reference_frame * laser_reference_frame * "
            "instrument_reference_frame * detector_reference_frame * "
            "reconstruction_reference_frame The aim of this convention is to "
            "support users with contextualizing which reference frame each "
            "instance (coordinate system) is. If needed, instances of "
            ":ref:`NXtransformations` are used to detail the explicit affine "
            "transformations whereby one can convert representations between "
            "different reference frames. Inspect :ref:`NXtransformations` for "
            "further details."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="NAMED_reference_frameID",
            name_type="partial",
            optionality="optional",
        ),
    )

    status = Quantity(
        type=MEnum(["success", "failure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-status-field"
        ],
        description=(
            "A statement whether the tool executable managed to process the "
            "analysis or whether this failed. Status is written to the results "
            "file after the end_time beyond which point in time the tool must no "
            "longer compute any further analysis results but exit. Only when "
            "this status message is present and its value is `success`, one "
            "should consider the results of the tool. In all other cases it "
            "might be that the tool has terminated prematurely or another error "
            "occurred."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["success", "failure"],
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Internal identifier used by the tool to refer to an analysis. "
            "Simulation ID is an alias."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
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


class ApmParaprobeToolCommonProfiling(CsProfiling):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )

    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        description=("Wall-clock time."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="total_elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
