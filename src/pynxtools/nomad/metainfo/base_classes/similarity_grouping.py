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
# Run `pynx nomad generate-metainfo --nxdl NXsimilarity_grouping` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SimilarityGrouping"]


class SimilarityGrouping(Object):
    """
    Base class to store results obtained from applying a similarity grouping
    (clustering) algorithm.

    Similarity grouping algorithms are segmentation or machine learning
    algorithms for partitioning the members of a set of objects (e.g. geometric
    primitives) into (sub-)groups aka features of different kind/type. A
    plethora of algorithms exists.

    This base class considers metadata and results of having a similarity
    grouping algorithm applied to a set in which objects are either categorized
    as noise or belonging to a cluster, i.e. members of a cluster. The
    algorithm assigns each similarity group (feature/cluster) at least one
    identifier (numerical or categorical labels) to distinguish different
    cluster.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsimilarity_grouping",
            category="base",
            symbols={
                "c": "Cardinality of the set.",
                "n_lbl_num": "Number of numerical labels per object.",
                "n_lbl_cat": "Number of categorical labels per object.",
                "n_features": "Total number of similarity groups aka features/clusters.",
            },
        ),
    )

    statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.similarity_grouping.SimilarityGroupingStatistics",
        repeats=False,
        description=(
            "In addition to the detailed storage which objects were grouped to "
            "which feature/group summary statistics are stored under this group."
        ),
    )

    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Number of members in the set which gets partitioned into features."
        ),
        a_nexus_field=NeXusField(
            name="cardinality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_numeric_labels = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-number-of-numeric-labels-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("How many numerical labels does each feature have."),
        a_nexus_field=NeXusField(
            name="number_of_numeric_labels",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_categorical_labels = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-number-of-categorical-labels-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("How many categorical labels does each feature have."),
        a_nexus_field=NeXusField(
            name="number_of_categorical_labels",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Which numerical index is the first to be used to label a feature. "
            "The value should be chosen in such a way that special values can be "
            "resolved: * index_offset - 1 indicates that an object belongs to no "
            "cluster. * index_offset - 2 indicates that an object belongs to the "
            "noise category. Setting for instance index_offset to 1 recovers the "
            "commonly used case that objects of the noise category get values to "
            "-1 and unassigned points to 0. Numerical identifier have to be "
            "strictly increasing."
        ),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    numerical_label = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-numerical-label-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of numerical label for each member in the set. For classical "
            "clustering algorithms this can for instance encode the "
            "indices_cluster."
        ),
        a_nexus_field=NeXusField(
            name="numerical_label",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    categorical_label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-categorical-label-field"
        ],
        shape=["*", "*"],
        description=(
            "Matrix of categorical attribute data for each member in the set."
        ),
        a_nexus_field=NeXusField(
            name="categorical_label",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class SimilarityGroupingStatistics(Process):
    """
    In addition to the detailed storage which objects were grouped to which
    feature/group summary statistics are stored under this group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="statistics",
            name_type="specified",
            optionality="optional",
        ),
    )

    unassigned = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-unassigned-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Total number of features categorized as unassigned."),
        a_nexus_field=NeXusField(
            name="unassigned",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    noise = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-noise-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Total number of features categorized as noise."),
        a_nexus_field=NeXusField(
            name="noise",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    total = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-total-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Total number of features."),
        a_nexus_field=NeXusField(
            name="total",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-indices-cluster-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Array of numerical identifier of each feature."),
        a_nexus_field=NeXusField(
            name="indices_cluster",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    member_count = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsimilarity_grouping.html#nxsimilarity_grouping-statistics-member-count-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=("Array of number of objects for each feature."),
        a_nexus_field=NeXusField(
            name="member_count",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
