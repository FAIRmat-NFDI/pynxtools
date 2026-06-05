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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_clusterer_results` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeClustererResults"]


class ApmParaprobeClustererResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-clusterer tool.

    The tool paraprobe-clusterer evaluates how points cluster in space.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_clusterer_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_feat": "Number of clusters found.",
            },
        ),
    )

    cameca_to_nexus = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process.ApmParaprobeToolProcess",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="cameca_to_nexus",
            name_type="specified",
            optionality="optional",
        ),
    )
    cluster_analysisID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process.ApmParaprobeToolProcess",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_clusterer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_clusterer_results"],
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
