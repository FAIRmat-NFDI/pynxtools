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
# Run `pynx nomad generate-metainfo --nx-class NXapm_paraprobe_nanochem_results` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeNanochemResults"]


class ApmParaprobeNanochemResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-nanochem tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_nanochem_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_atomic": "The total number of atoms in the atomic_decomposition match filter.",
                "n_isotopic": "The total number of isotopes in the isotopic_decomposition match filter.",
                "d": "The dimensionality of the delocalization grid.",
                "c": "The cardinality/total number of cells/grid points in the delocalization grid.",
                "n_f_tri": "The total number of faces of triangles.",
                "n_f_tri_xdmf": "The total number of XDMF values to represent all faces of triangles via XDMF.",
                "n_feature_dict": "The total number of entries in a feature dictionary.",
                "n_v_feat": "The total number of volumetric features.",
                "n_speci": "The total number of member distinguished when reporting composition.",
                "n_rois": "The total number of ROIs placed in a oned_profile task.",
            },
        ),
    )

    delocalizationID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.delocalization.Delocalization",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdelocalization",
            name="delocalizationID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    interface_meshingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsInterface_meshingID",
        repeats=True,
        variable=True,
    )
    oned_profileID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process.ApmParaprobeToolProcess",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="oned_profileID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_nanochem_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_nanochem_results"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-definition-version-attribute"
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


class ApmParaprobeNanochemResultsInterface_meshingID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="interface_meshingID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    ion_multiplicity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-ion-multiplicity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The multiplicity whereby the ion position is accounted for "
            "irrespective whether the ion is considered as a decorator of the "
            "interface or not. As an example, with atom probe it is typically "
            "not possible to resolve the positions of the atoms which arrive at "
            "the detector as molecular ions. Therefore, an exemplar molecular "
            "ion of two carbon atoms can be considered to have a multiplicity of "
            "two to account that this molecular ion contributes two carbon atoms "
            "at the reconstructed location considering that the spatial "
            "resolution of atom probe experiments is limited."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ion_multiplicity",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    decorator_multiplicity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-decorator-multiplicity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The multiplicity whereby the ion position is accounted for when the "
            "ion is considered one which is a decorator of the interface."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="decorator_multiplicity",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
