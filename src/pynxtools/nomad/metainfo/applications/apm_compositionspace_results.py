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
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.atom import Atom
from pynxtools.nomad.metainfo.base_classes.cg_grid import CgGrid
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.data import Data
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
        categories=[ExperimentCategory],
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
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsEnvironment",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
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
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentation",
        repeats=False,
        description=(
            "Step during which the voxel set is segmented into voxel sets with "
            "different chemical composition."
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_compositionspace_results",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsEnvironmentProgram",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsEnvironmentProgram(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-environment-program-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-environment-program-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-environment-program-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsVoxelizationGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )
    ionID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsVoxelizationIonID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="ionID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-weight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
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


class ApmCompositionspaceResultsVoxelizationGrid(CgGrid):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="3",
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="cardinality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    origin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-origin-field"
        ],
        flexible_unit=True,
        shape=["*"],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    symmetry = Quantity(
        type=MEnum(["cubic"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-symmetry-field"
        ],
        a_nexus_field=NeXusField(
            name="symmetry",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["cubic"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="cubic",
        ),
    )
    cell_dimensions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-cell-dimensions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="cell_dimensions",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    extent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-extent-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Position of each cell in Euclidean space."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    coordinate = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-coordinate-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=("Discrete coordinate of each voxel."),
        a_nexus_field=NeXusField(
            name="coordinate",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    indices_voxel = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-grid-indices-voxel-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "For each ion, the identifier of the voxel into which the ion binned."
        ),
        a_nexus_field=NeXusField(
            name="indices_voxel",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsVoxelizationIonID(Atom):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-ionid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="ionID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-ionid-name-field"
        ],
        description=("Chemical symbol of the element from the periodic table."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-voxelization-ionid-weight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Element-specific weight (counts for discretization with a "
            "rectangular transfer function) for the occupancy of each voxel with "
            "atoms of this element."
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

    result = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsAutophaseResult",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="2",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsAutophaseResult(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axis_feature_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axis-feature-indices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Element identifier stored sorted in descending order of feature "
            "importance."
        ),
        a_nexus_field=NeXusField(
            name="axis_feature_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    axis_feature_indices__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axis-feature-indices-long-name-attribute"
        ],
        description=("Axis caption"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_feature_indices",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axis_feature_importance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axis-feature-importance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Element relative feature importance stored sorted in descending "
            "order of feature importance."
        ),
        a_nexus_field=NeXusField(
            name="axis_feature_importance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    axis_feature_importance__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-autophase-result-axis-feature-importance-long-name-attribute"
        ],
        description=("Axis caption"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_feature_importance",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentation(Process):
    """
    Step during which the voxel set is segmented into voxel sets with different
    chemical composition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="segmentation",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    pca = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentationPca",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pca",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )
    ic_opt = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentationIcOpt",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="ic_opt",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentationPca(Process):
    """
    PCA in the chemical space (essentially composition correlation analyses).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pca",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    result = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentationPcaResult",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=MEnum(["2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            enumeration=["2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentationPcaResult(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axis_explained_variance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-axis-explained-variance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Explained variance values"),
        a_nexus_field=NeXusField(
            name="axis_explained_variance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    axis_pca_dimension = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-pca-result-axis-pca-dimension-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Elements identifier matching those from ENTRY/voxelization/ionID "
            "used during the principal component analysis."
        ),
        a_nexus_field=NeXusField(
            name="axis_pca_dimension",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentationIcOpt(Process):
    """
    Information criterion minimization.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="ic_opt",
            name_type="specified",
            optionality="required",
        ),
    )

    cluster_analysisID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentationIcOptClusterAnalysisID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="cluster_analysisID",
            name_type="partial",
            optionality="required",
        ),
    )
    result = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsSegmentationIcOptResult",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=MEnum(["3", "4"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            enumeration=["3", "4"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentationIcOptClusterAnalysisID(Process):
    """
    Results of the Gaussian mixture analysis for n_components equal to
    n_ic_cluster.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-cluster-analysisid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="cluster_analysisID",
            name_type="partial",
            optionality="required",
        ),
    )

    n_ic_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-cluster-analysisid-n-ic-cluster-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("n_components argument of the Gaussian mixture model."),
        a_nexus_field=NeXusField(
            name="n_ic_cluster",
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
    y_pred = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-cluster-analysisid-y-pred-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("y_pred return values of the computation."),
        a_nexus_field=NeXusField(
            name="y_pred",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsSegmentationIcOptResult(Data):
    """
    Information criterion as a function of number of n_ic_cluster aka
    dimensions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="result",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axis_aic = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-axis-aic-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Akaike information criterion values"),
        a_nexus_field=NeXusField(
            name="axis_aic",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    axis_bic = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-axis-bic-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Bayes information criterion values"),
        a_nexus_field=NeXusField(
            name="axis_bic",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_dimension = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-segmentation-ic-opt-result-axis-dimension-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Actual n_ic_cluster values used"),
        a_nexus_field=NeXusField(
            name="axis_dimension",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
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

    ic_opt = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsClusteringIcOpt",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="ic_opt",
            name_type="specified",
            optionality="required",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsClusteringIcOpt(Process):
    """
    Respective DBScan clustering result for each segmentation/ic_opt case.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="ic_opt",
            name_type="specified",
            optionality="required",
        ),
    )

    cluster_analysisID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsClusteringIcOptClusterAnalysisID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsClusteringIcOptClusterAnalysisID(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    dbscanID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_results.ApmCompositionspaceResultsClusteringIcOptClusterAnalysisIDDbscanID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="dbscanID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceResultsClusteringIcOptClusterAnalysisIDDbscanID(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-dbscanid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="dbscanID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    epsilon = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-dbscanid-epsilon-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The maximum distance between voxel pairs in a neighborhood to be "
            "considered connected."
        ),
        a_nexus_field=NeXusField(
            name="epsilon",
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
    min_samples = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-dbscanid-min-samples-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The number of voxels in a neighborhood for a voxel to be considered "
            "as a core point."
        ),
        a_nexus_field=NeXusField(
            name="min_samples",
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
    label = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-dbscanid-label-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Raw label return values"),
        a_nexus_field=NeXusField(
            name="label",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    voxel = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_results.html#nxapm_compositionspace_results-entry-clustering-ic-opt-cluster-analysisid-dbscanid-voxel-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Voxel identifier Using these identifiers correlated element-wise "
            "with the values in the label array specifies for which voxel in the "
            "grid clusters from this process were found."
        ),
        a_nexus_field=NeXusField(
            name="voxel",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
