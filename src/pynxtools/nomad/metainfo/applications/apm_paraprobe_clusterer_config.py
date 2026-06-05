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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_clusterer_config` to regenerate.
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

__all__ = ["ApmParaprobeClustererConfig"]


class ApmParaprobeClustererConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-clusterer
    tool.

    The tool paraprobe-clusterer evaluates how points cluster in space.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_clusterer_config",
            category="application",
            symbols={
                "n_ivec_max": "Maximum number of atoms per molecular ion. Should be 32 for paraprobe.",
                "n_clust_algos": "Number of clustering algorithms used.",
                "n_ions": "Number of different iontypes to distinguish during clustering.",
            },
        ),
    )

    cameca_to_nexus = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigCamecaToNexus",
        repeats=False,
        description=(
            "This process maps results from a cluster analysis made with IVAS / "
            "AP Suite into an interoperable representation. IVAS / AP Suite "
            "usually exports such results as a list of reconstructed ion "
            "positions with one cluster label per position. These labels are "
            "reported via the mass-to-charge-state-ratio column of what is "
            "effectively a binary file that is formatted like a POS file but "
            "cluster labels written out using floating point numbers."
        ),
    )
    cluster_analysisID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigCluster_analysisID",
        repeats=True,
        variable=True,
        description=(
            "This process performs a cluster analysis on a reconstructed dataset "
            "or a ROI within it."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_clusterer_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_clusterer_config"],
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


class ApmParaprobeClustererConfigCamecaToNexus(ApmParaprobeToolParameters):
    """
    This process maps results from a cluster analysis made with IVAS / AP Suite
    into an interoperable representation. IVAS / AP Suite usually exports such
    results as a list of reconstructed ion positions with one cluster label per
    position. These labels are reported via the mass-to-charge-state-ratio
    column of what is effectively a binary file that is formatted like a POS
    file but cluster labels written out using floating point numbers.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="cameca_to_nexus",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    recover_evaporation_id = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-recover-evaporation-id-field"
        ],
        description=(
            "Specifies if paraprobe-clusterer should use the evaporation_ids "
            "from reconstruction for recovering for each position in the "
            ":ref:`NXnote` results the closest matching position (within "
            "floating point accuracy). This can be useful when users wish to "
            "recover the original evaporation_id, which IVAS /AP Suite drops "
            "when writing their *.indexed.* cluster results POS files that is "
            "referred to results."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="recover_evaporation_id",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-cameca-to-nexus-identifier-analysis-field"
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


class ApmParaprobeClustererConfigCluster_analysisID(ApmParaprobeToolParameters):
    """
    This process performs a cluster analysis on a reconstructed dataset or a
    ROI within it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    ion_type_filter = Quantity(
        type=MEnum(["resolve_element"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-ion-type-filter-field"
        ],
        description=(
            "How should iontypes be considered during the cluster analysis. The "
            "value resolve_all will set an ion active in the analysis regardless "
            "of which iontype it is. The value resolve_unknown will set an ion "
            "active when it is of the UNKNOWNTYPE. The value resolve_ion will "
            "set an ion active if it is of the specific iontype, irregardless of "
            "its nuclide structure. The value resolve_element will set an ion "
            "active and account as many times for it, as the (molecular) ion "
            "contains atoms of elements in the whitelist "
            "ion_query_nuclide_vector. The value resolve_isotope will set an ion "
            "active and account as many times for it, as the (molecular) ion "
            "contains nuclides in the whitelist ion_query_nuclide_vector. In "
            "effect, ion_query_nuclide_vector acts as a whitelist to filter "
            "which ions are considered as source ions of the correlation "
            "statistics and how the multiplicity of each ion will be factorized. "
            "This is relevant as in atom probe we have the situation that an ion "
            "of a molecular ion with more than one nuclide, say Ti O for example "
            "is counted potentially several times because at that position "
            "(reconstructed) position it has been assumed that there was a Ti "
            "and an O atom. This multiplicity affects the size of the feature "
            "and its chemical composition."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ion_type_filter",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["resolve_element"],
        ),
    )
    ion_query_nuclide_vector = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-ion-query-nuclide-vector-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of nuclide vectors, as many as rows as different candidates "
            "for iontypes should be distinguished as possible source iontypes. "
            "In the simplest case, the matrix contains only the proton number of "
            "the element in the row, all other values set to zero."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ion_query_nuclide_vector",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-cluster-analysisid-identifier-analysis-field"
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
