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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_tool_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_common import (
    ApmParaprobeToolCommon,
)
from pynxtools.nomad.metainfo.base_classes.entry import Entry

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
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tool_results",
            category="application",
        ),
    )

    apm_paraprobe_tool_process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process.ApmParaprobeToolProcess",
        repeats=True,
        variable=True,
        description=("A specific processing result"),
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
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

    status = Quantity(
        type=MEnum(["success", "failure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-common-status-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
