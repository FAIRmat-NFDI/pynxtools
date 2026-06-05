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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_intersector_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters import (
    ApmParaprobeToolParameters,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeIntersectorConfig"]


class ApmParaprobeIntersectorConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the
    paraprobe-intersector tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_intersector_config",
            category="application",
            symbols={"n_variable": "Number of entries"},
        ),
    )

    v_v_spatial_correlationID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_config.ApmParaprobeIntersectorConfigV_v_spatial_correlationID",
        repeats=True,
        variable=True,
        description=(
            "Tracking volume_volume_spatial_correlations (v_v) is the process of "
            "building logical relations between objects, their proximity and "
            "eventual volumetric intersections. Here, objects are assumed to be "
            "represented as a set of triangulated surface meshes. Volumetric "
            "overlap and proximity of volumetric features is identified for "
            "members of sets of features to members of other sets of volumetric "
            "features. Specifically, for each time step :math:`k` pairs of sets "
            "are compared: Members of a so-called current_set to members of a "
            "so-called next_set. Members can be different types of volumetric "
            "features."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_intersector_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_intersector_config"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-definition-version-attribute"
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


class ApmParaprobeIntersectorConfigV_v_spatial_correlationID(
    ApmParaprobeToolParameters
):
    """
    Tracking volume_volume_spatial_correlations (v_v) is the process of
    building logical relations between objects, their proximity and eventual
    volumetric intersections. Here, objects are assumed to be represented as a
    set of triangulated surface meshes.

    Volumetric overlap and proximity of volumetric features is identified for
    members of sets of features to members of other sets of volumetric
    features. Specifically, for each time step :math:`k` pairs of sets are
    compared: Members of a so-called current_set to members of a so-called
    next_set. Members can be different types of volumetric features.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="v_v_spatial_correlationID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    intersection_detection_method = Quantity(
        type=MEnum(["shared_ion"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-intersection-detection-method-field"
        ],
        description=(
            "Specifies the method whereby to decide if two objects intersect "
            "volumetrically. For reasons which are detailed in the supplementary "
            "material of `M. Kühbach et al. "
            "<https://arxiv.org/abs/2205.13510>`_, it is assumed by default that "
            "two objects intersect if they share at least one ion with the same "
            "evaporation ID (shared_ion). Alternatively, with specifying "
            "tetrahedra_intersections, the tool can perform an intersection "
            "analysis which attempts to tetrahedralize first each polyhedron. If "
            "successful, the tool then checks for at least one pair of "
            "intersecting tetrahedra to identify if two objects intersect or "
            "not. However, we found that these geometrical analyses can result "
            "in corner cases which the tetrahedralization library used in the "
            "tests (TetGen) was not unable to tetrahedralize successfully. These "
            "cases were virtually always associated with complicated non-convex "
            "polyhedra which had portions of the mesh that were connected by "
            "almost point like tubes of triangles. Finding more robust methods "
            "for computing intersections between not necessarily convex "
            "polyhedra might improve the situation in the future. For practical "
            "reasons we have thus deactivated the functionality of "
            "tetrahedra-tetrahedron intersections in paraprobe-intersector."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intersection_detection_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["shared_ion"],
        ),
    )
    analyze_intersection = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-analyze-intersection-field"
        ],
        description=(
            "Specifies if the tool evaluates if objects intersect volumetrically."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="analyze_intersection",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    analyze_proximity = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-analyze-proximity-field"
        ],
        description=(
            "Specifies if the tool evaluates if objects lay closer to one "
            "another than threshold_proximity."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="analyze_proximity",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    analyze_coprecipitation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-analyze-coprecipitation-field"
        ],
        description=(
            "Specifies if the tool evaluates, provided that all (preprocessing "
            "tasks were successful), how intersecting or proximity related "
            "objects build sub-graphs. This is the feature that was used in `M. "
            "Kühbach et al. <https://arxiv.org/abs/2205.13510>`_ for the "
            "high-throughput analyses of how many objects are coprecipitates in "
            "the sense that they are single, duplet, triplet, or high-order "
            "local groups."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="analyze_coprecipitation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    threshold_proximity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-threshold-proximity-field"
        ],
        dimensionality="[length]",
        description=(
            "The maximum Euclidean distance between two objects below which they "
            "are considered within proximity."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="threshold_proximity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    has_current_to_next_links = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-has-current-to-next-links-field"
        ],
        description=(
            "Specifies if the tool stores the so-called forward relations "
            "between nodes representing members of the current_set to nodes "
            "representing members of the next_set."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="has_current_to_next_links",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    has_next_to_current_links = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-has-next-to-current-links-field"
        ],
        description=(
            "Specifies if the tool stores the so-called backward relations "
            "between nodes representing members of the next_set to nodes "
            "representing members of the current_set."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="has_next_to_current_links",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-v-v-spatial-correlationid-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
