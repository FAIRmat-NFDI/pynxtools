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
    ApmParaprobeToolConfigApmParaprobeToolParameters,
)

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
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_spatstat_config.ApmParaprobeSpatstatConfigSpatial_statisticsID",
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


class ApmParaprobeSpatstatConfigSpatial_statisticsID(
    ApmParaprobeToolConfigApmParaprobeToolParameters
):
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

    random_number_generator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_prng.CsPrng",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_prng",
            name="random_number_generator",
            name_type="specified",
            optionality="recommended",
        ),
    )
    statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
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
    )
    ion_query_nuclide_source = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-nuclide-source-field"
        ],
        dimensionality="dimensionless",
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
    )
    ion_query_nuclide_target = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_spatstat_config.html#nxapm_paraprobe_spatstat_config-entry-spatial-statisticsid-ion-query-nuclide-target-field"
        ],
        dimensionality="dimensionless",
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
