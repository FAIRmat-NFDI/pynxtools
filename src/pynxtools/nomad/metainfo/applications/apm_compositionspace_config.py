# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXapm_compositionspace_config (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXapm_compositionspace_config` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
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
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_compositionspace_config",
            category="application",
        ),
    )

    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigReconstruction",
        repeats=False,
    )
    ranging = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigRanging",
        repeats=False,
    )
    voxelization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigVoxelization",
        repeats=False,
    )
    segmentation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigSegmentation",
        repeats=False,
    )
    clustering = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigClustering",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXapm_compositionspace_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_compositionspace_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_compositionspace_config",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-definition-version-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-identifier-analysis-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-checksum-field"
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
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-algorithm-field"
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
    position = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-reconstruction-position-field"
        ],
        description=(
            "Name of the node which resolves the reconstructed ion position "
            "values to use for this analysis."
        ),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="mass_to_charge",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-checksum-field"
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
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-ranging-algorithm-field"
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
        a_nexus_field=NeXusField(
            name="ranging_definitions",
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

    autophase = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigVoxelizationAutophase",
        repeats=False,
    )

    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Edge length of cubic voxels building the 3D grid that is used for "
            "discretizing the point cloud."
        ),
        a_nexus_field=NeXusField(
            name="edge_length",
            type="NX_NUMBER",
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


class ApmCompositionspaceConfigVoxelizationAutophase(Process):
    """
    Optional step during which the subsequent segmentation step is prepared
    with the aim to eventually reduce the dimensionality of the chemical space
    in which the machine learning model works.

    In this step a supervised reduction of the dimensionality of the chemical
    space is quantified using the (Gini) feature importance of each element to
    suggest which columns of the composition matrix should be taken for the
    subsequent segmentation step.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-autophase-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="autophase",
            name_type="specified",
            optionality="required",
        ),
    )

    random_forest_classifier = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=("Configuration for the random forest classification model."),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="random_forest_classifier",
            name_type="specified",
            optionality="optional",
        ),
    )

    use = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-autophase-use-field"
        ],
        description=("Was the automated phase assignment used?"),
        a_nexus_field=NeXusField(
            name="use",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    initial_guess = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-autophase-initial-guess-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Estimated guess for which a Gaussian mixture model is evaluated to "
            "preprocess a result that is subsequently post-processed with a "
            "random_forest_classifier to lower the number of dimensions in the "
            "chemical space to the subset of trunc_species many elements with "
            "the highest feature importance."
        ),
        a_nexus_field=NeXusField(
            name="initial_guess",
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
    trunc_species = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-voxelization-autophase-trunc-species-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The number of elements to use for reducing the dimensionality."),
        a_nexus_field=NeXusField(
            name="trunc_species",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigSegmentation(Process):
    """
    Step during which the voxel set is segmented into voxel sets with different
    chemical composition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-segmentation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="segmentation",
            name_type="specified",
            optionality="required",
        ),
    )

    pca = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "A principal component analysis of the chemical space to guide a "
            "decision into how many sets of voxels with different chemical "
            "composition the machine learning algorithm suggests to split the "
            "voxel set."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pca",
            name_type="specified",
            optionality="optional",
        ),
    )
    ic_opt = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigSegmentationIcOpt",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigSegmentationIcOpt(Process):
    """
    The decision is guided through the evaluation of the information criterion
    minimization.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-segmentation-ic-opt-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="ic_opt",
            name_type="specified",
            optionality="required",
        ),
    )

    gaussian_mixture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "Configuration for the Gaussian mixture model that is used in the "
            "segmentation step."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="gaussian_mixture",
            name_type="specified",
            optionality="optional",
        ),
    )

    n_max_ic_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-segmentation-ic-opt-n-max-ic-cluster-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The maximum number of chemical classes to probe with the Gaussian "
            "mixture model with which the voxel set is segmented into a mixture "
            "of voxels with that many different chemical compositions."
        ),
        a_nexus_field=NeXusField(
            name="n_max_ic_cluster",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigClustering(Process):
    """
    Step during which the chemically segmented voxel sets are analyzed for
    their spatial organization.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-clustering-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="clustering",
            name_type="specified",
            optionality="required",
        ),
    )

    dbscan = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_compositionspace_config.ApmCompositionspaceConfigClusteringDbscan",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCompositionspaceConfigClusteringDbscan(Parameters):
    """
    Configuration for the DBScan algorithm that is used in the clustering step.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-clustering-dbscan-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="dbscan",
            name_type="specified",
            optionality="required",
        ),
    )

    eps = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-clustering-dbscan-eps-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The maximum distance between voxel pairs in a neighborhood to be "
            "considered connected."
        ),
        a_nexus_field=NeXusField(
            name="eps",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_compositionspace_config.html#nxapm_compositionspace_config-entry-clustering-dbscan-min-samples-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
