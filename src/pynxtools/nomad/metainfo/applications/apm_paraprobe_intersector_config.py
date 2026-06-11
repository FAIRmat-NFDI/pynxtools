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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_intersector_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
    ApmParaprobeToolConfigApmParaprobeToolParameters,
)
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

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
        a_nexus_field=NeXusField(
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


class ApmParaprobeIntersectorConfigV_v_spatial_correlationID(
    ApmParaprobeToolConfigApmParaprobeToolParameters
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

    current_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_config.ApmParaprobeIntersectorConfigV_v_spatial_correlationIDCurrentSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="current_set",
            name_type="specified",
            optionality="required",
        ),
    )
    next_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_config.ApmParaprobeIntersectorConfigV_v_spatial_correlationIDNextSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="next_set",
            name_type="specified",
            optionality="required",
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        unit="m",
        description=(
            "The maximum Euclidean distance between two objects below which they "
            "are considered within proximity."
        ),
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="has_next_to_current_links",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeIntersectorConfigV_v_spatial_correlationIDCurrentSet(Parameters):
    """
    Current set stores a set of members, meshes of volumetric features, which
    will be checked for proximity and/or volumetric intersection, to members of
    the current_set. The meshes were generated as a result of some other
    meshing process.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="current_set",
            name_type="specified",
            optionality="required",
        ),
    )

    objectID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_config.ApmParaprobeIntersectorConfigV_v_spatial_correlationIDCurrentSetObjectID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="objectID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=4,
        ),
    )

    set_identifier = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-set-identifier-field"
        ],
        description=(
            "This identifier can be used to label the current set. The label "
            "effectively can be interpreted as the time/iteration (i.e. "
            ":math:`k`) step when the current set was taken (see `M. Kühbach et "
            "al. 2022 <https://arxiv.org/abs/2205.13510>`_)."
        ),
        a_nexus_field=NeXusField(
            name="set_identifier",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    number_of_feature_types = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-number-of-feature-types-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The total number of distinguished feature sets featureID. It is "
            "assumed that the members within all these featureID sets are "
            "representing a set together. As an example this set might represent "
            "all volumetric_features. However, users might have formed a subset "
            "of this set where individuals were regrouped. For "
            "paraprobe-nanochem this is the case for objects and proxies. "
            "Specifically, objects are distinguished further into those far from "
            "and those close to the edge of the dataset. Similarly, proxies are "
            "distinguished further into those far from and those close to the "
            "edge of the dataset. So while these four sub-sets contain different "
            "so-called types of features, key is that they were all generated "
            "for one set, here the current_set."
        ),
        a_nexus_field=NeXusField(
            name="number_of_feature_types",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeIntersectorConfigV_v_spatial_correlationIDCurrentSetObjectID(Note):
    """
    Name of the (NeXus)/HDF5 file which contains triangulated surface meshes of
    the members of the set as instances of NXcg_polyhedron.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="objectID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=4,
        ),
    )

    feature_type = Quantity(
        type=MEnum(
            [
                "objects_far_from_edge",
                "objects_close_to_edge",
                "proxies_far_from_edge",
                "proxies_close_to_edge",
                "other",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-feature-type-field"
        ],
        description=("Descriptive category explaining what these features are."),
        a_nexus_field=NeXusField(
            name="feature_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "objects_far_from_edge",
                "objects_close_to_edge",
                "proxies_far_from_edge",
                "proxies_close_to_edge",
                "other",
            ],
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    geometry = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-geometry-field"
        ],
        description=(
            "Absolute path to the group with geometry data in the HDF5 file "
            "referred to by path."
        ),
        a_nexus_field=NeXusField(
            name="geometry",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-current-set-objectid-indices-feature-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Array of identifier whereby the path to the geometry data can be "
            "inferred automatically."
        ),
        a_nexus_field=NeXusField(
            name="indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeIntersectorConfigV_v_spatial_correlationIDNextSet(Parameters):
    """
    Next set stores a set of members, meshes of volumetric features, which will
    be checked for proximity and/or volumetric intersection, to members of the
    next_set. The meshes were generated as a result of some other meshing
    process.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="next_set",
            name_type="specified",
            optionality="required",
        ),
    )

    objectID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_intersector_config.ApmParaprobeIntersectorConfigV_v_spatial_correlationIDNextSetObjectID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="objectID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=4,
        ),
    )

    set_identifier = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-set-identifier-field"
        ],
        description=(
            "This identifier can be used to label the current set. The label "
            "effectively can be interpreted as the time/iteration (i.e. :math:`k "
            "+ 1`) step when the current set was taken (see `M. Kühbach et al. "
            "2022 <https://arxiv.org/abs/2205.13510>`_)."
        ),
        a_nexus_field=NeXusField(
            name="set_identifier",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    number_of_feature_types = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-number-of-feature-types-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The total number of distinguished feature sets featureID. It is "
            "assumed that the members within all these featureID sets are "
            "representing a set together. As an example this set might represent "
            "all volumetric_features. However, users might have formed a subset "
            "of this set where individuals were regrouped. For "
            "paraprobe-nanochem this is the case for objects and proxies. "
            "Specifically, objects are distinguished further into those far from "
            "and those close to the edge of the dataset. Similarly, proxies are "
            "distinguished further into those far from and those close to the "
            "edge of the dataset. So while these four sub-sets contain different "
            "so-called types of features key is that they were all generated for "
            "one set, here the next_set."
        ),
        a_nexus_field=NeXusField(
            name="number_of_feature_types",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeIntersectorConfigV_v_spatial_correlationIDNextSetObjectID(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="objectID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=4,
        ),
    )

    feature_type = Quantity(
        type=MEnum(
            [
                "objects_far_from_edge",
                "objects_close_to_edge",
                "proxies_far_from_edge",
                "proxies_close_to_edge",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-feature-type-field"
        ],
        description=("Descriptive category explaining what these features are."),
        a_nexus_field=NeXusField(
            name="feature_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "objects_far_from_edge",
                "objects_close_to_edge",
                "proxies_far_from_edge",
                "proxies_close_to_edge",
            ],
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    geometry = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-geometry-field"
        ],
        description=(
            "Absolute path to the group with geometry data in the HDF5 file "
            "referred to by path."
        ),
        a_nexus_field=NeXusField(
            name="geometry",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_intersector_config.html#nxapm_paraprobe_intersector_config-entry-v-v-spatial-correlationid-next-set-objectid-indices-feature-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Array of identifier whereby the path to the geometry data can be "
            "inferred automatically."
        ),
        a_nexus_field=NeXusField(
            name="indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
