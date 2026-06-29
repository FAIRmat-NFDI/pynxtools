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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_spatstat_results` to regenerate.
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

__all__ = ["ApmParaprobeSpatstatResults"]


class ApmParaprobeSpatstatResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-spatstat tool.

    The tool paraprobe-spatstat evaluates spatial distribution functions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_spatstat_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_knn": "The total number of bins in the histogram for the k-th nearest neighbor.",
                "n_rdf": "The total number of bins in the histogram for the radial distribution function.",
            },
        ),
    )

    spatial_statisticsID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_results.ApmParaprobeSpatstatResultsSpatialStatisticsID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_spatstat_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_spatstat_results"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_spatstat_results",
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


class ApmParaprobeSpatstatResultsSpatialStatisticsID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="spatial_statisticsID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    knn = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_results.ApmParaprobeSpatstatResultsSpatialStatisticsIDKnn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="knn",
            name_type="specified",
            optionality="optional",
        ),
    )
    rdf = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_results.ApmParaprobeSpatstatResultsSpatialStatisticsIDRdf",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rdf",
            name_type="specified",
            optionality="optional",
        ),
    )

    iontypes_randomized = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-iontypes-randomized-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The iontype ID for each ion that was assigned to each ion during "
            "the randomization of the ionlabels. Iontype labels are just "
            "permuted but the total number of values for each iontype remain the "
            "same. The order matches the iontypes array from a given ranging "
            "results as it is specified in the configuration settings inside the "
            "specific config_filename that was used for this paraprobe-spatstat "
            "analysis."
        ),
        a_nexus_field=NeXusField(
            name="iontypes_randomized",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatResultsSpatialStatisticsIDKnn(Process):
    """
    K-nearest neighbor statistics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-knn-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="knn",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-knn-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Right boundary of the binning."),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    probability_mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-knn-probability-mass-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="probability_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    cumulated = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-knn-cumulated-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Cumulated not normalized by total counts."),
        a_nexus_field=NeXusField(
            name="cumulated",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cumulated_normalized = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-knn-cumulated-normalized-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Cumulated and normalized by total counts."),
        a_nexus_field=NeXusField(
            name="cumulated_normalized",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSpatstatResultsSpatialStatisticsIDRdf(Process):
    """
    Radial distribution statistics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-rdf-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rdf",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-rdf-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Right boundary of the binning."),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    probability_mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-rdf-probability-mass-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="probability_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    cumulated = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-rdf-cumulated-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Cumulated not normalized by total counts."),
        a_nexus_field=NeXusField(
            name="cumulated",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cumulated_normalized = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_results.html#nxapm_paraprobe_spatstat_results-entry-spatial-statisticsid-rdf-cumulated-normalized-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Cumulated and normalized by total counts."),
        a_nexus_field=NeXusField(
            name="cumulated_normalized",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
