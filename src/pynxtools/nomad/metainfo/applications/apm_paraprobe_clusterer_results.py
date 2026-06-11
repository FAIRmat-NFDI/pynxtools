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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_clusterer_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.similarity_grouping import SimilarityGrouping

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
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_results.ApmParaprobeClustererResultsCluster_analysisID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_clusterer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
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


class ApmParaprobeClustererResultsCluster_analysisID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    dbscanID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_results.ApmParaprobeClustererResultsCluster_analysisIDDbscanID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsimilarity_grouping",
            name="dbscanID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeClustererResultsCluster_analysisIDDbscanID(SimilarityGrouping):
    """
    Results of a DBScan clustering analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsimilarity_grouping",
            name="dbscanID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_results.ApmParaprobeClustererResultsCluster_analysisIDDbscanIDStatistics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="statistics",
            name_type="specified",
            optionality="recommended",
        ),
    )

    eps = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-eps-field"
        ],
        dimensionality="[length]",
        description=("The epsilon (eps) parameter used."),
        a_nexus_field=NeXusField(
            name="eps",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    min_pts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-min-pts-field"
        ],
        dimensionality="dimensionless",
        description=("The minimum points (min_pts) parameter used."),
        a_nexus_field=NeXusField(
            name="min_pts",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-cardinality-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Number of members in the set which is partitioned into features. "
            "Specifically, this is the total number of targets filtered from the "
            "dataset, i.e. typically the number of clusters which is usually not "
            "and for sure not necessarily the total number of ions in the "
            "dataset."
        ),
        a_nexus_field=NeXusField(
            name="cardinality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-index-offset-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Which identifier is the first to be used to label a cluster. The "
            "value should be chosen in such a way that special values can be "
            "resolved: * index_offset - 1 indicates an object belongs to no "
            "cluster. * index_offset - 2 indicates an object belongs to the "
            "noise category. Setting for instance index_offset to 1 recovers the "
            "commonly used case that objects of the noise category get the value "
            "of -1 and points of the unassigned category get the value 0."
        ),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    targets = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-targets-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The evaporation (sequence) id (aka evaporation_id) to figure out "
            "which ions from the reconstruction were considered targets. The "
            "length of this array is not necessarily n_ions. Instead, it is the "
            "value of cardinality."
        ),
        a_nexus_field=NeXusField(
            name="targets",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_solutions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-number-of-solutions-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The number of solutions found for each target. Typically, this "
            "value is 1 in which case the field can be omitted. Otherwise, this "
            "array is the concatenated set of values of solution tuples for each "
            "target that can be used to decode model_labels, "
            "core_sample_indices, and weight."
        ),
        a_nexus_field=NeXusField(
            name="number_of_solutions",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    model_label = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-model-label-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The raw labels from the DBScan clustering backend process. The "
            "length of this array is not necessarily n_ions. Instead, it is "
            "typically the value of cardinality provided that each target has "
            "only one associated cluster. If targets are assigned to multiple "
            "cluster this array is as long as the total number of solutions "
            "found and"
        ),
        a_nexus_field=NeXusField(
            name="model_label",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    core_sample_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-core-sample-indices-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The raw array of core sample indices which specify which of the "
            "targets are core points."
        ),
        a_nexus_field=NeXusField(
            name="core_sample_indices",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    numerical_label = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-numerical-label-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Numerical label for each target (member in the set) aka cluster "
            "identifier."
        ),
        a_nexus_field=NeXusField(
            name="numerical_label",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-weight-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Weights for each target that specifies how probable the target is "
            "assigned to a specific cluster. For the DBScan algorithm and atom "
            "probe tomography this value is the multiplicity of each ion with "
            "respect to the cluster. That is how many times should the position "
            "of the ion be accounted for because the ion is e.g. a molecular ion "
            "with several elements or nuclides of requested type."
        ),
        a_nexus_field=NeXusField(
            name="weight",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    is_noise = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-is-noise-field"
        ],
        shape=["*"],
        description=("Are targets assigned to the noise category or not."),
        a_nexus_field=NeXusField(
            name="is_noise",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    is_core = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-is-core-field"
        ],
        shape=["*"],
        description=("Are targets assumed a core point."),
        a_nexus_field=NeXusField(
            name="is_core",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeClustererResultsCluster_analysisIDDbscanIDStatistics(Process):
    """
    In addition to the detailed storage which members were grouped to which
    feature here summary statistics are stored that communicate e.g. how many
    cluster were found.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="statistics",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_targets = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-number-of-targets-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Total number of targets in the set, i.e. ions that were filtered "
            "and considered in this cluster analysis."
        ),
        a_nexus_field=NeXusField(
            name="number_of_targets",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_noise_members = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-number-of-noise-members-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Total number of members in the set which are categorized as noise."
        ),
        a_nexus_field=NeXusField(
            name="number_of_noise_members",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_core_members = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-number-of-core-members-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Total number of members in the set which are categorized as a core point."
        ),
        a_nexus_field=NeXusField(
            name="number_of_core_members",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_features = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-number-of-features-field"
        ],
        dimensionality="dimensionless",
        description=("Total number of clusters (excluding noise and unassigned)."),
        a_nexus_field=NeXusField(
            name="number_of_features",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-indices-feature-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Numerical identifier of each feature aka cluster_id."),
        a_nexus_field=NeXusField(
            name="indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_members = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_results.html#nxapm_paraprobe_clusterer_results-entry-cluster-analysisid-dbscanid-statistics-number-of-members-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Number of members for each feature."),
        a_nexus_field=NeXusField(
            name="number_of_members",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
