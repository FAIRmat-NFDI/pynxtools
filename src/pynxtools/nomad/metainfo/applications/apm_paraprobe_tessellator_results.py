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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tessellator_results` to regenerate.
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

__all__ = ["ApmParaprobeTessellatorResults"]


class ApmParaprobeTessellatorResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-tessellator
    tool.

    The tool paraprobe-tessellator computes a tessellation of the reconstructed
    positions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tessellator_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_f": "The total number of values required to represent all faces of each cell.",
                "n_f_xdmf": "The total number of values required to represent all faces of each cell\n                (polyhedron) using XDMF.",
            },
        ),
    )

    tessellationID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationID",
        repeats=True,
        variable=True,
        description=(
            "The tool can be used to compute a Voronoi tessellation the entire "
            "or of a sub-set of the reconstructed volume. Each point (ion) is "
            "wrapped in one (Voronoi) cell. The point cloud in the ROI is "
            "wrapped into an axis-aligned bounding box (AABB) that is tight. "
            "This means points at the edge of the point cloud can lay on the "
            "surface of the bounding box. The tool detects if cells make contact "
            "with the walls of this bounding box. The tessellation is computed "
            "without periodic boundary conditions."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_tessellator_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_tessellator_results"],
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


class ApmParaprobeTessellatorResultsTessellationID(ApmParaprobeToolProcess):
    """
    The tool can be used to compute a Voronoi tessellation the entire or of a
    sub-set of the reconstructed volume. Each point (ion) is wrapped in one
    (Voronoi) cell. The point cloud in the ROI is wrapped into an axis-aligned
    bounding box (AABB) that is tight. This means points at the edge of the
    point cloud can lay on the surface of the bounding box. The tool detects if
    cells make contact with the walls of this bounding box. The tessellation is
    computed without periodic boundary conditions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="tessellationID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    wall = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_hexahedron.CgHexahedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="wall",
            name_type="specified",
            optionality="recommended",
        ),
    )
    voronoi_cells = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="voronoi_cells",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
