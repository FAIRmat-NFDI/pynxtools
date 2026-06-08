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
# Run `pynx nomad generate-metainfo --nxdl NXapm_compositionspace_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmCompositionspaceResults"]


class ApmCompositionspaceResults(Entry):
    """
    Application definition for results of the CompositionSpace tool used in
    atom probe.

    * `A. Saxena et al.
    <https://www.github.com/eisenforschung/CompositionSpace.git>`_

    This is an application definition for the common NFDI-MatWerk/FAIRmat
    infrastructure use case IUC09 that explores how to improve the organization
    and results storage of the CompositionSpace software using NeXus.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_compositionspace_results",
            category="application",
            symbols={
                "grid_dim": "The dimensionality of the grid.",
                "n_voxels": "Total number of voxels.",
                "n_ions": "Total number of ions in the reconstructed dataset.",
            },
        ),
    )

    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsProfiling",
        repeats=False,
    )
    program1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsProgram1",
        repeats=False,
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsConfig",
        repeats=False,
        description=("Configuration file that was used in this analysis."),
    )
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="optional",
        ),
    )
    specimen = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSpecimen",
        repeats=False,
        description=(
            "Contextualize back to the specimen from which the dataset was "
            "collected that was here analyzed with CompositionSpace tool."
        ),
    )
    voxelization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsVoxelization",
        repeats=False,
        description=(
            "Step during which the point cloud is discretized to compute "
            "element-specific composition fields. Iontypes are atomically "
            "decomposed to correctly account for the multiplicity of each "
            "element that was ranged for each ion. Using a discretization grid "
            "that is larger than the average distance between reconstructed ion "
            "positions reduces computational costs. This is the key idea of the "
            "CompositionSpace tool compared to other methods used in atom probe "
            "for characterizing microstructural features that use the ion "
            "position data directly."
        ),
    )
    autophase = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsAutophase",
        repeats=False,
        description=(
            "Optional step during which the subsequent segmentation step is "
            "prepared to improve the segmentation."
        ),
    )
    segmentation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "Step during which the voxel set is segmented into voxel sets with "
            "different chemical composition."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="segmentation",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    clustering = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsClustering",
        repeats=False,
        description=(
            "Step during which the chemically segmented voxel sets are analyzed "
            "for their spatial organization into different spatial clusters of "
            "voxels in the same chemical set but representing individual "
            "objects. The objects are constructed from blobs of neighboring "
            "voxels. The objects are not necessarily watertight or topologically "
            "closed."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_compositionspace_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_compositionspace_results"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-identifier-analysis-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
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


class ApmCompositionspaceResultsProfiling(CsProfiling):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )

    current_working_directory = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-current-working-directory-field"
        ],
        a_nexus_field=NeXusField(
            name="current_working_directory",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsProgram1(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-program1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program1",
            name_type="specified",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-program1-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-program1-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsConfig(Note):
    """
    Configuration file that was used in this analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-config-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-config-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-config-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSpecimen(Sample):
    """
    Contextualize back to the specimen from which the dataset was collected
    that was here analyzed with CompositionSpace tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-specimen-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="specimen",
            name_type="specified",
            optionality="recommended",
        ),
    )

    is_simulation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-specimen-is-simulation-field"
        ],
        description=(
            "True, if the specimen that the reconstructed dataset describes is a "
            "simulated one. False, if the specimen that the reconstructed "
            "dataset describes is a real one."
        ),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-specimen-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the specimen. If the specimen substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`. The purpose of the field is to offer research data "
            "management systems an opportunity to parse the relevant elements "
            "without having to interpret these from the resources pointed to by "
            "identifier_parent or walk through eventually deeply nested groups "
            "in data instances."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsVoxelization(Process):
    """
    Step during which the point cloud is discretized to compute
    element-specific composition fields. Iontypes are atomically decomposed to
    correctly account for the multiplicity of each element that was ranged for
    each ion.

    Using a discretization grid that is larger than the average distance
    between reconstructed ion positions reduces computational costs. This is
    the key idea of the CompositionSpace tool compared to other methods used in
    atom probe for characterizing microstructural features that use the ion
    position data directly.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="voxelization",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    sequence_index = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            enumeration=["1"],
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-weight-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Total number of weight (counts for discretization with a "
            "rectangular transfer function) for the occupancy of each voxel with "
            "atoms."
        ),
        a_nexus_field=NeXusField(
            name="weight",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsAutophase(Process):
    """
    Optional step during which the subsequent segmentation step is prepared to
    improve the segmentation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="autophase",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    sequence_index = Quantity(
        type=MEnum(["2"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            enumeration=["2"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsClustering(Process):
    """
    Step during which the chemically segmented voxel sets are analyzed for
    their spatial organization into different spatial clusters of voxels in the
    same chemical set but representing individual objects. The objects are
    constructed from blobs of neighboring voxels. The objects are not
    necessarily watertight or topologically closed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="clustering",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    sequence_index = Quantity(
        type=MEnum(["4", "5"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            enumeration=["4", "5"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
