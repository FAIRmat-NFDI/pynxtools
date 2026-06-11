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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_ranger_results` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeRangerResults"]


class ApmParaprobeRangerResults(ApmParaprobeToolResults):
    """
    Application definition for results files of the paraprobe-ranger tool.

    The tool paraprobe-ranger evaluates how mass-to-charge-state-ratio values
    map on (molecular) ion types.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_ranger_results.html#nxapm_paraprobe_ranger_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_ranger_results",
            category="application",
            symbols={"n_ions": "The total number of ions in the reconstructed volume."},
        ),
    )

    iontypesID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_ranger_results.ApmParaprobeRangerResultsIontypesID",
        repeats=True,
        variable=True,
        description=(
            "The tool loads ranging definitions from the configuration file and "
            "evaluates for each ion to which iontype it matches. If an ion "
            "matches on no type, the ion is assume of the default "
            "*unknown_type*. In this case, the value *iontypes* is 0. In other "
            "cases the value is larger than 0."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_ranger_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_ranger_results.html#nxapm_paraprobe_ranger_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_ranger_results"],
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


class ApmParaprobeRangerResultsIontypesID(ApmParaprobeToolProcess):
    """
    The tool loads ranging definitions from the configuration file and
    evaluates for each ion to which iontype it matches. If an ion matches on no
    type, the ion is assume of the default *unknown_type*. In this case, the
    value *iontypes* is 0. In other cases the value is larger than 0.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_ranger_results.html#nxapm_paraprobe_ranger_results-entry-iontypesid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="iontypesID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    iontypes = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_ranger_results.html#nxapm_paraprobe_ranger_results-entry-iontypesid-iontypes-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The iontype (identifier) for each ion that was best matching, "
            "stored in the order of the evaporation sequence ID."
        ),
        a_nexus_field=NeXusField(
            name="iontypes",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
