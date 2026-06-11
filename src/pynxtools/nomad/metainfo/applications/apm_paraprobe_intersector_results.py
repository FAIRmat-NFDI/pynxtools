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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_intersector_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeIntersectorResults"]


class ApmParaprobeIntersectorResults(ApmParaprobeToolResults):
    """
    Application definition for results files of the paraprobe-intersector tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_intersector_results",
            category="application",
            symbols={
                "n_c2n": "The total number of links pointing from current to next.",
                "n_n2c": "The total number of links pointing from next to current.",
                "n_features_curr": "The total number of members in the current_set.",
                "n_features_next": "The total number of members in the next_set.",
                "n_cluster": "The total number of cluster found for coprecipitation analysis.",
                "n_total": "The number of rows in the table/matrix for coprecipitation statistics.",
            },
        ),
    )

    v_v_spatial_correlationID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_results.ApmParaprobeIntersectorResultsV_v_spatial_correlationID",
        repeats=True,
        variable=True,
        description=("The results of an overlap/intersection analysis."),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_intersector_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_intersector_results"],
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


class ApmParaprobeIntersectorResultsV_v_spatial_correlationID(ApmParaprobeToolProcess):
    """
    The results of an overlap/intersection analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="v_v_spatial_correlationID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    coprecipitation_analysis = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_results.ApmParaprobeIntersectorResultsV_v_spatial_correlationIDCoprecipitationAnalysis",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="coprecipitation_analysis",
            name_type="specified",
            optionality="optional",
        ),
    )

    current_to_next_link = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-current-to-next-link-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "A matrix of indices_feature that specifies which named features "
            "from the current_set have directed link(s) pointing to which named "
            "feature(s) from the next_set."
        ),
        a_nexus_field=NeXusField(
            name="current_to_next_link",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    current_to_next_link_type = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-current-to-next-link-type-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "For each link/pair in current_to_next a characterization whether "
            "the link is due to volumetric overlap (0x00 == 0), proximity (0x01 "
            "== 1), or something else unknown (0xFF == 255)."
        ),
        a_nexus_field=NeXusField(
            name="current_to_next_link_type",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    next_to_current_link = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-next-to-current-link-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "A matrix of indices_feature which specifies which named feature(s) "
            "from the next_set have directed link(s) pointing to which named "
            "feature(s) from the current_set. Only if the mapping whereby the "
            "links are defined is symmetric it holds that next_to_current maps "
            "the links for current_to_next in just the opposite direction."
        ),
        a_nexus_field=NeXusField(
            name="next_to_current_link",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    next_to_current_link_type = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-next-to-current-link-type-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "For each link/pair in next_to_current a characterization whether "
            "the link is due to a volumetric overlap (0x00 == 0), proximity "
            "(0x01 == 1), or something else unknown (0xFF == 255)."
        ),
        a_nexus_field=NeXusField(
            name="next_to_current_link_type",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intersection_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-intersection-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
        description=(
            "For each pair of links in current_to_next the volume of the "
            "intersection, i.e. how much volume do the two features share. If "
            "features do not intersect the volume is zero."
        ),
        a_nexus_field=NeXusField(
            name="intersection_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeIntersectorResultsV_v_spatial_correlationIDCoprecipitationAnalysis(
    Process
):
    """
    During coprecipitation analysis the current and next set are analyzed for
    links in a special way. Three set comparisons are made. Members of the set
    in each comparison are analyzed for overlap and proximity:

    The first comparison is the current_set against the current_set. The second
    comparison is the next_set against the next_set. The third comparison is
    the current_set against the next_set.

    Once the (forward) links for these comparisons are ready, pair relations
    are analyzed with respect to which objects with indices_feature cluster in
    identifier space. Thereby, a logical connection (link) is established
    between the features in the current_set and the next_set. Recall that these
    two sets typically represent different features within an observed system
    for otherwise the same parameterization.

    Examples include two sets of e.g. precipitates with differing chemical
    composition that were characterized in the same material volume
    representing a snapshot of an e.g. microstructure at the same point in
    time. Researchers may have performed two analyses, one to characterize
    precipitates A and another one for precipitates B.

    Coprecipitation analysis now logically connects these independent
    characterization results to establish spatial correlations of e.g. the
    precipitates' spatial arrangement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="coprecipitation_analysis",
            name_type="specified",
            optionality="optional",
        ),
    )

    current_set_feature_to_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-current-set-feature-to-cluster-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "Matrix of indices_feature and cluster_id pairs which encodes the "
            "cluster to which each indices_feature was assigned. Here for "
            "features of the current_set."
        ),
        a_nexus_field=NeXusField(
            name="current_set_feature_to_cluster",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    next_set_feature_to_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-next-set-feature-to-cluster-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "Matrix of indices_feature and cluster_id pairs which encodes the "
            "cluster to which each indices_feature was assigned. Here for "
            "features of the next_set."
        ),
        a_nexus_field=NeXusField(
            name="next_set_feature_to_cluster",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cluster_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-cluster-id-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("The identifier (names) of the cluster."),
        a_nexus_field=NeXusField(
            name="cluster_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cluster_composition = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-cluster-composition-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 3],
        description=(
            "Pivot table as a matrix. The first column encodes how many members "
            "from the current_set are in each cluster, one row per cluster. The "
            "second column encodes how many members from the next_set are in "
            "each cluster, in the same row per cluster respectively. The third "
            "column encodes the total number of members in the cluster."
        ),
        a_nexus_field=NeXusField(
            name="cluster_composition",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cluster_statistics = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_results.html#nxapm_paraprobe_intersector_results-entry-v-v-spatial-correlationid-coprecipitation-analysis-cluster-statistics-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "Pivot table as a matrix. The first column encodes the different "
            "types of clusters based on their number of members in the "
            "sub-graph. The second column encodes how many clusters with as many "
            "members exist."
        ),
        a_nexus_field=NeXusField(
            name="cluster_statistics",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
