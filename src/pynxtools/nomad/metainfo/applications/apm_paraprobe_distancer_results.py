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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_distancer_results` to regenerate.
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

__all__ = ["ApmParaprobeDistancerResults"]


class ApmParaprobeDistancerResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-distancer tool.

    The tool paraprobe-distancer tool evaluates exactly the shortest Euclidean
    distance for each member of a set of points against a set of triangles.

    Triangles can represent for instance the facets of a triangulated surface
    mesh like those returned by paraprobe-surfacer or any other set of
    triangles. Triangles do not have to be connected.

    Currently, paraprobe-distancer does not check if the respectively specified
    triangle sets are consistent, what their topology is, or whether or not
    these triangles are consistently oriented.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_distancer_results",
            category="application",
            symbols={
                "n_ions": "The total number of points, i.e. ions in the reconstruction.",
                "n_tri": "The total number of triangles in the set.",
            },
        ),
    )

    point_to_triangleID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_distancer_results.ApmParaprobeDistancerResultsPoint_to_triangleID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_distancer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_distancer_results"],
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


class ApmParaprobeDistancerResultsPoint_to_triangleID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="point_to_triangleID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-distance-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "The shortest analytical distance of each point to their "
            "respectively closest triangle from the joint triangle set."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    indices_triangle = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-indices-triangle-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "For each point the identifier of the triangle for which the "
            "shortest distance was found."
        ),
        a_nexus_field=NeXusField(
            name="indices_triangle",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_point = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-indices-point-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "A support field to enable the visualization of each point by an "
            "explicit identifier on the interval [0, n_ions - 1]. The field can "
            "be used to visualize the points as a function of their distance to "
            "the triangle set (e.g. via XDMF/Paraview)."
        ),
        a_nexus_field=NeXusField(
            name="indices_point",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
