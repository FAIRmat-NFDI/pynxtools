# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXapm_paraprobe_tool_common (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tool_common` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["success", "failure"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Internal identifier used by the tool to refer to an analysis. "
            "Simulation ID is an alias."
        ),
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
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


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
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

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-profiling-start-time-field"
        ],
        description=(
            "ISO 8601 formatted time code with local time zone offset to UTC "
            "information included when the analysis in this results file was "
            "started, i.e. when the respective executable/tool was started as a "
            "process."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-profiling-end-time-field"
        ],
        description=(
            "ISO 8601 formatted time code with local time zone offset to UTC "
            "information included when the analysis in this results file were "
            "completed and the respective process of the tool exited."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_common.html#nxapm_paraprobe_tool_common-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Wall-clock time."),
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
