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
# Run `pynx nomad generate-metainfo --nx-class NXapm_compositionspace_config` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmCompositionspaceConfig"]


class ApmCompositionspaceConfig(Entry):
    """
    Application definition for a configuration of the CompositionSpace tool
    used in atom probe.

    * `A. Saxena et al.
    <https://www.github.com/eisenforschung/CompositionSpace.git>`_

    This is an application definition for the common NFDI-MatWerk/FAIRmat
    infrastructure use case IUC09 that explores how to improve the organization
    and results storage of the CompositionSpace tool by using the NeXus data
    model and semantics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_compositionspace_config",
            category="application",
        ),
    )

    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigReconstruction",
        repeats=False,
        description=(
            "Specification of the tomographic reconstruction used for this "
            "analysis. Reconstructions in the field of atom probe tomography are "
            "communicated via a file which stores the reconstructed position and "
            "mass-to-charge-state-ratio value for each ion. Container file "
            "formats like HDF5, such as NeXus/HDF5 files using :ref:`NXapm`, can "
            "store multiple reconstructions. In this case, the position and "
            "mass_to_charge concepts point to specific instances in the file "
            "referred to by file_name for the analysis with CompositionSpace."
        ),
    )
    ranging = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigRanging",
        repeats=False,
        description=(
            "Specification of the ranging definitions used for this analysis. "
            "Ranging definitions in the field of atom probe tomography are "
            "communicated via a file which stores the mass-to-charge-state-ratio "
            "interval and the number of elements of which each (molecular) ion "
            "is composed. These values are stored for each ion. Container file "
            "formats like HDF5, such as NeXus/HDF5 files using :ref:`NXapm`, can "
            "store multiple ranging definitions. Indices of ions start from 1. "
            "The value 0 is reserved for the null model of unranged positions "
            "whose iontype is referred to as the unknown_type. The value 0 is "
            "also reserved for voxels that lie outside the dataset."
        ),
    )
    voxelization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigVoxelization",
        repeats=False,
        description=(
            "Step during which the point cloud is discretized to compute "
            "element-specific composition fields. Iontypes are atomically "
            "decomposed to correctly account for the multiplicity of each "
            "element that was ranged for each ion."
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
            optionality="required",
        ),
    )
    clustering = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "Step during which the chemically segmented voxel sets are analyzed "
            "for their spatial organization."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="clustering",
            name_type="specified",
            optionality="required",
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_compositionspace_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_compositionspace_config"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-definition-version-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-identifier-analysis-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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


class ApmCompositionspaceConfigReconstruction(Note):
    """
    Specification of the tomographic reconstruction used for this analysis.

    Reconstructions in the field of atom probe tomography are communicated via
    a file which stores the reconstructed position and
    mass-to-charge-state-ratio value for each ion.

    Container file formats like HDF5, such as NeXus/HDF5 files using
    :ref:`NXapm`, can store multiple reconstructions. In this case, the
    position and mass_to_charge concepts point to specific instances in the
    file referred to by file_name for the analysis with CompositionSpace.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="reconstruction",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-file-name-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-checksum-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-algorithm-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    position = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-position-field"
        ],
        description=(
            "Name of the node which resolves the reconstructed ion position "
            "values to use for this analysis."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="position",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    mass_to_charge = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-mass-to-charge-field"
        ],
        description=(
            "Name of the node which resolves the mass-to-charge-state-ratio "
            "values for each reconstructed ion to use for this analysis."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="mass_to_charge",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigRanging(Note):
    """
    Specification of the ranging definitions used for this analysis.

    Ranging definitions in the field of atom probe tomography are communicated
    via a file which stores the mass-to-charge-state-ratio interval and the
    number of elements of which each (molecular) ion is composed. These values
    are stored for each ion.

    Container file formats like HDF5, such as NeXus/HDF5 files using
    :ref:`NXapm`, can store multiple ranging definitions.

    Indices of ions start from 1. The value 0 is reserved for the null model of
    unranged positions whose iontype is referred to as the unknown_type. The
    value 0 is also reserved for voxels that lie outside the dataset.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ranging",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-file-name-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-checksum-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-algorithm-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    ranging_definitions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-ranging-definitions-field"
        ],
        description=(
            "Name of that (parent) node whose child stores the ranging "
            "definitions that are applied in this analysis with "
            "CompositionSpace."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ranging_definitions",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigVoxelization(Process):
    """
    Step during which the point cloud is discretized to compute
    element-specific composition fields. Iontypes are atomically decomposed to
    correctly account for the multiplicity of each element that was ranged for
    each ion.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="voxelization",
            name_type="specified",
            optionality="required",
        ),
    )

    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-edge-length-field"
        ],
        dimensionality="[length]",
        description=(
            "Edge length of cubic voxels building the 3D grid that is used for "
            "discretizing the point cloud."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="edge_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
