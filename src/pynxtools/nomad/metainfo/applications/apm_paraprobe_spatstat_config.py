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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_spatstat_config` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
    ApmParaprobeToolConfigTaskconfig,
)
from pynxtools.nomad.metainfo.base_classes.cs_prng import CsPrng
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeSpatstatConfig"]


class ApmParaprobeSpatstatConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-spatstat
    tool.

    The tool paraprobe-spatstat evaluates spatial distribution functions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_spatstat_config",
            category="application",
            symbols={
                "n_ivec_max": "Maximum number of atoms per molecular ion. Should be 32 for paraprobe.",
                "n_ion_source": "Number of different source iontypes to distinguish.",
                "n_ion_target": "Number of different target iontypes to distinguish.",
            },
        ),
    )

    spatial_statisticsID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_spatstat_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_spatstat_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_spatstat_config",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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


class ApmParaprobeSpatstatConfigSpatialStatisticsID(ApmParaprobeToolConfigTaskconfig):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="spatial_statisticsID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDSurfaceDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )
    feature_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDFeatureDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="feature_distance",
            name_type="specified",
            optionality="optional",
        ),
    )
    random_number_generator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDRandomNumberGenerator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_prng",
            name="random_number_generator",
            name_type="specified",
            optionality="recommended",
        ),
    )
    statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDStatistics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="statistics",
            name_type="specified",
            optionality="required",
        ),
    )

    randomize_iontypes = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-randomize-iontypes-field"
        ],
        description=(
            "Specifies, if the iontypes are randomized for the point cloud or "
            "not. Internally, paraprobe uses a sequentially executed "
            "deterministic MT19987 (MersenneTwister) pseudo-random number "
            "generator to shuffle the iontypes randomly across the entire set of "
            "ions. That is the total number of ions of either type remain the "
            "same but the information about their location is randomized."
        ),
        a_nexus_field=NeXusField(
            name="randomize_iontypes",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    ion_query_type_source = Quantity(
        type=MEnum(
            [
                "resolve_all",
                "resolve_unknown",
                "resolve_ion",
                "resolve_element",
                "resolve_isotope",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-type-source-field"
        ],
        description=(
            "How should the iontype be interpreted on the source-side, i.e. all "
            "these ion positions where a regions-of-interest (ROI) around "
            "so-called source ions will be placed. Different options exist how "
            "iontypes are interpreted given an iontype represents in general a "
            "(molecular) ion with different isotopes that have individually "
            "different multiplicity. The value resolve_all will set an ion "
            "active in the analysis regardless of which iontype it is. Each "
            "active ion is accounted for once. The value resolve_unknown will "
            "set an ion active when the ion is of the UNKNOWNTYPE type. Each "
            "active ion is accounted for once. The value resolve_ion will set an "
            "ion active if it is of the specific iontype, irregardless of its "
            "elemental or isotopic details. Each active ion is counted once. The "
            "value resolve_element will set an ion active, and most importantly, "
            "account for each as many times as the (molecular) ion contains "
            "atoms of elements in the whitelist ion_query_isotope_vector. The "
            "value resolve_isotope will set an ion active, and most importantly, "
            "account for each as many times as the (molecular) ion contains "
            "isotopes in the whitelist ion_query_isotope_vector. In effect, "
            "ion_query_isotope_vector acts as a whitelist to filter which ions "
            "are considered as source ions of the correlation statistics and how "
            "the multiplicity of each ion will be factorized, i.e. how often it "
            "is accounted for."
        ),
        a_nexus_field=NeXusField(
            name="ion_query_type_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "resolve_all",
                "resolve_unknown",
                "resolve_ion",
                "resolve_element",
                "resolve_isotope",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    ion_query_nuclide_source = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-nuclide-source-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of isotope vectors, as many as rows as different candidates "
            "for iontypes should be distinguished as possible source iontypes. "
            "In the simplest case, the matrix contains only the proton number of "
            "the element in the row, all other values set to zero. Combined with "
            "ion_query_type_source set to resolve_element this will recover "
            "usual spatial correlation statistics like the 1NN C-C spatial "
            "statistics."
        ),
        a_nexus_field=NeXusField(
            name="ion_query_nuclide_source",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    ion_query_type_target = Quantity(
        type=MEnum(
            [
                "resolve_all",
                "resolve_unknown",
                "resolve_ion",
                "resolve_element",
                "resolve_isotope",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-type-target-field"
        ],
        description=(
            "Similarly as ion_query_type_source how should iontypes be "
            "interpreted on the target-side, i.e. how many counts will be "
            "bookkept for ions which are neighbors of source ions within or on "
            "the surface of each inspection/ROI about each source ion. Source "
            "ion in the center of the ROI are not accounted for during counting "
            "the summary statistics. For details about the resolve values "
            "consider the explanations in ion_query_type_source. These account "
            "for ion_query_type_target as well."
        ),
        a_nexus_field=NeXusField(
            name="ion_query_type_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "resolve_all",
                "resolve_unknown",
                "resolve_ion",
                "resolve_element",
                "resolve_isotope",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    ion_query_nuclide_target = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-nuclide-target-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of isotope vectors, as many as rows as different candidates "
            "for iontypes to distinguish as possible targets. See additional "
            "comments under ion_query_isotope_vector_source."
        ),
        a_nexus_field=NeXusField(
            name="ion_query_nuclide_target",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDSurfaceDistance(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    distance = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-distance-field"
        ],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    edge_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-surface-distance-edge-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Threshold to define how far an ion has to lay at least from the "
            "edge of the dataset so that the ion can act as a source. This means "
            "that an ROI is placed at the location of the ion and its neighbors "
            "are analyzed how they contribute to the computed statistics. The "
            "edge_distance threshold can be combined with the feature_distance "
            "threshold. This threshold defines defines up to which distance to a "
            "microstructural feature an ROI is placed. The threshold is useful "
            "to process the dataset such that ROIs do not protrude out of the "
            "dataset as this would add bias."
        ),
        a_nexus_field=NeXusField(
            name="edge_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDFeatureDistance(Note):
    """
    Distance between each ion and triangulated mesh of microstructural
    features. In addition to spatial filtering and considering how far ions lie
    to the edge of the dataset, it is possible to restrict the analyses to a
    sub-set of ions within a distance not farther away to a feature than the
    feature_distance threshold value.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="feature_distance",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    distance = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-distance-field"
        ],
        description=(
            "Absolute path in the (HDF5) file which points to the distance of "
            "each ion to the closest feature."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    feature_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-feature-distance-feature-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Threshold to define how close an ion has to lay to a feature so "
            "that the ion can at all qualify as a source, i.e. that an ROI is "
            "placed at the location of the ion and its neighbors are then "
            "analyzed how they contribute to the computed statistics. Recall "
            "that this feature_distance threshold is used in combination with "
            "the edge_distance threshold when placing ROI about source ions."
        ),
        a_nexus_field=NeXusField(
            name="feature_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDRandomNumberGenerator(CsPrng):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-random-number-generator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_prng",
            name="random_number_generator",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=MEnum(["physical", "system_clock", "mt19937", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-random-number-generator-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["physical", "system_clock", "mt19937", "other"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    seed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-random-number-generator-seed-field"
        ],
        a_nexus_field=NeXusField(
            name="seed",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    warmup = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-random-number-generator-warmup-field"
        ],
        a_nexus_field=NeXusField(
            name="warmup",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDStatistics(Process):
    """
    Specifies which spatial statistics to compute.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="statistics",
            name_type="specified",
            optionality="required",
        ),
    )

    knn = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDStatisticsKnn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="knn",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    rdf = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatialStatisticsIDStatisticsRdf",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rdf",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDStatisticsKnn(Process):
    """
    Compute k-th nearest neighbour statistics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-knn-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="knn",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    kth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-knn-kth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Order k."),
        a_nexus_field=NeXusField(
            name="kth",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-knn-min-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Minimum value of the histogram binning."),
        a_nexus_field=NeXusField(
            name="min",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    increment = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-knn-increment-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Increment of the histogram binning."),
        a_nexus_field=NeXusField(
            name="increment",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-knn-max-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Maximum value of the histogram binning."),
        a_nexus_field=NeXusField(
            name="max",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatConfigSpatialStatisticsIDStatisticsRdf(Process):
    """
    Compute radial distribution function.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-rdf-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rdf",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-rdf-min-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Minimum value of the histogram binning."),
        a_nexus_field=NeXusField(
            name="min",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    increment = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-rdf-increment-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Increment value of the histogram binning."),
        a_nexus_field=NeXusField(
            name="increment",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-statistics-rdf-max-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Maximum value of the histogram binning."),
        a_nexus_field=NeXusField(
            name="max",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
