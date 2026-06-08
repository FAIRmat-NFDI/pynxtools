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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_distancer_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters import (
    ApmParaprobeToolParameters,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeDistancerConfig"]


class ApmParaprobeDistancerConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-distancer
    tool.

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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_distancer_config",
            category="application",
        ),
    )

    point_to_triangleID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_distancer_config.ApmParaprobeDistancerConfigPoint_to_triangleID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_distancer_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_distancer_config"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-definition-version-attribute"
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


class ApmParaprobeDistancerConfigPoint_to_triangleID(ApmParaprobeToolParameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config-entry-point-to-triangleid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="point_to_triangleID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    method = Quantity(
        type=MEnum(["default", "skin"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config-entry-point-to-triangleid-method-field"
        ],
        description=(
            "Specifies for which point the tool will compute distances. The "
            "value *default* configures that distances are computed for all "
            "points. The value *skin* configures that distances are computed "
            "only for those points which are not farther away located to a "
            "triangle than threshold_distance."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["default", "skin"],
        ),
    )
    threshold_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config-entry-point-to-triangleid-threshold-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Maximum distance for which distances are computed when *method* is *skin*."
        ),
        a_nexus_field=NeXusField(
            name="threshold_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    number_of_triangle_sets = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_config.html#nxapm_paraprobe_distancer_config-entry-point-to-triangleid-number-of-triangle-sets-field"
        ],
        dimensionality="dimensionless",
        description=(
            "How many triangle sets to consider. Multiple triangle sets can be "
            "defined which are composed into one joint triangle set for the "
            "analysis."
        ),
        a_nexus_field=NeXusField(
            name="number_of_triangle_sets",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-point-to-triangleid-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
