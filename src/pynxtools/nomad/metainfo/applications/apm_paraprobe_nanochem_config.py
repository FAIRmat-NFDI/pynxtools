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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_nanochem_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
    ApmParaprobeToolConfigTaskconfig,
)
from pynxtools.nomad.metainfo.base_classes.cg_cylinder import CgCylinder
from pynxtools.nomad.metainfo.base_classes.match_filter import MatchFilter
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.roi_process import RoiProcess

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeNanochemConfig"]


class ApmParaprobeNanochemConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-nanochem
    tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_nanochem_config",
            category="application",
            symbols={
                "n_ityp_deloc_cand": "How many iontypes does the delocalization filter specify.",
                "n_grid": "How many grid_resolutions values.",
                "n_var": "How many kernel_variance values.",
                "n_control_pts": "How many disjoint control points are defined.",
                "n_fct_filter_cand": "How many iontypes does the interface meshing iontype filter specify.",
                "n_fct_iterations": "How many DCOM iterations.",
                "n_ivec_max": "Maximum number of atoms per molecular ion.",
                "n_rois": "Number of cylinder ROIs to place for oned_profile if no feature mesh is used.",
            },
        ),
    )

    delocalizationID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationID",
        repeats=True,
        variable=True,
        description=(
            "Discretization and distributing of the ion point cloud on a 3D grid "
            "to enable analyses at the continuum scale. By default, the tool "
            "computes a full kernel density estimation of decomposed ions to "
            "create one discretized field for each element. One delocalization "
            "task configures a parameter sweep with at least one delocalization. "
            "The total number of runs depends on the number of grid_resolution "
            "and kernel_variance values. For example, setting two "
            "grid_resolutions and three kernel_variance will compute six runs. "
            "Two sets of three with the first set using the first "
            "grid_resolutions and in sequence the kernel_variance respectively."
        ),
    )
    interface_meshingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigInterfaceMeshingID",
        repeats=True,
        variable=True,
        description=(
            "Use a principle component analysis (PCA) to mesh a single "
            "free-standing interface patch within the reconstructed volume that "
            "is decorated by ions of specific iontypes (e.g. solute atoms). "
            "Interface_meshing is a typical starting point for the "
            "quantification of Gibbsian interfacial excess in cases when closed "
            "objects constructed from patches e.g. iso-surfaces are not "
            "available or when there is no substantial or consistently oriented "
            "concentration gradients across an interface patch. The "
            "functionality can also be useful when the amount of latent "
            "crystallographic information within the point cloud is insufficient "
            "or when combined with interface_meshing based on ion density traces "
            "in field-desorption maps (see `Y. Wei et al. "
            "<https://doi.org/10.1371/journal.pone.0225041>`_ and `A. Breen et "
            "al. <https://github.com/breen-aj/detector>`_ for details). "
            "Noteworthy to mention is that the method used is conceptually "
            "similar to the work of `Z. Peng et al. "
            "<https://doi.org/10.1017/S1431927618016112>`_ and related work "
            "(DCOM algorithm) by `P. Felfer et al. "
            "<https://doi.org/10.1016/j.ultramic.2015.06.002>`_. Compared to "
            "these implementations paraprobe-nanochem uses inspection "
            "functionalities which detect potential geometric inconsistencies or "
            "self-interactions of the evolved DCOM mesh."
        ),
    )
    oned_profileID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileID",
        repeats=True,
        variable=True,
        description=(
            "Analysis of one-dimensional profiles in ROIs placed in the dataset. "
            "Such analyses are useful for quantifying interfacial excess or for "
            "performing classical composition analyses. The tool will test for "
            "each ROIs if it is completely embedded in the dataset. "
            "Specifically, each such test evaluates if the ROI cuts at least one "
            "triangle of the triangulated surface mesh that is referred to by "
            "surface. If this is the case the ROI is marked as one close to the "
            "surface and not analyzed further. Otherwise, the ROI is marked as "
            "one far from the surface and processed further. For each ROI the "
            "tool computes atomically decomposed profiles. This means, molecular "
            "ions are split into nuclides as many times as their respective "
            "multiplicity. For each processed ROI the tool stores a sorted list "
            "of signed distance values to enable post-processing with other "
            "software like e.g. reporter to perform classical "
            "Krakauer/Seidman-style interfacial excess analyses. Users should be "
            "aware that the latter intersection analysis is not a volumetric "
            "intersection analysis. Given that the triangulated mesh referred to "
            "in surface is not required to mesh neither a watertight nor convex "
            "polyhedron a rigorous testing of volumetric intersection is much "
            "more involved. If the mesh is watertight one could use split the "
            "task in first tessellating the mesh into convex polyhedra (e.g. "
            "tetrahedra and apply a volumetric intersection method like the "
            "Gilbert-Johnson-Keerthi algorithm (GJK). In cases when the mesh is "
            "not even watertight distance-based segmentation in combination with "
            "again intersection of triangles and convex polyhedra is a robust "
            "but currently not implemented method to quantify intersections."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_nanochem_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_nanochem_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_nanochem_config",
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
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class ApmParaprobeNanochemConfigDelocalizationID(ApmParaprobeToolConfigTaskconfig):
    """
    Discretization and distributing of the ion point cloud on a 3D grid to
    enable analyses at the continuum scale.

    By default, the tool computes a full kernel density estimation of
    decomposed ions to create one discretized field for each element.

    One delocalization task configures a parameter sweep with at least one
    delocalization. The total number of runs depends on the number of
    grid_resolution and kernel_variance values. For example, setting two
    grid_resolutions and three kernel_variance will compute six runs. Two sets
    of three with the first set using the first grid_resolutions and in
    sequence the kernel_variance respectively.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="delocalizationID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    surface = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationIDSurface",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="required",
        ),
    )
    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationIDSurfaceDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="recommended",
        ),
    )
    decomposition = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationIDDecomposition",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="decomposition",
            name_type="specified",
            optionality="required",
        ),
    )
    input = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationIDInput",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="required",
        ),
    )
    isosurfacing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigDelocalizationIDIsosurfacing",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="isosurfacing",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    method = Quantity(
        type=MEnum(["compute", "load_existent"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-method-field"
        ],
        description=("Compute delocalization or load an existent one from input."),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["compute", "load_existent"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    nuclide_whitelist = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-nuclide-whitelist-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of nuclides representing how iontypes should be accounted "
            "for during the delocalization. This is the most general approach to "
            "define if and how many times an ion is to be counted. The tool "
            "performs a so-called atomic decomposition of all iontypes, i.e. the "
            "tool analyses from how many atoms of each nuclide or element "
            "respectively an (molecular) ion is built from. Taking the "
            "hydroxonium H3O+ molecular ion as an example: It contains hydrogen "
            "and oxygen atoms. The multiplicity of hydrogen is three whereas "
            "that of oxygen is one. Therefore, the respective atomic "
            "decomposition analysis prior to the iso-surface computation adds "
            "three hydrogen counts for each H3O+ ion. This is a practical "
            "solution which accepts that on the one hand not every bond is "
            "broken during an atom probe experiment but also that ions may react "
            "further during their flight to the detector. The exact details "
            "depend on the local field conditions, quantum mechanics of possible "
            "electron transfer and thus the detailed trajectory of the system "
            "and its electronic state. The detection of molecular ions instead "
            "of always single atom ions only is the reason that an atom probe "
            "experiment tells much about field evaporation physics but also "
            "faces an inherent loss of information with respect to the detailed "
            "spatial arrangement that is independent of other imprecisions such "
            "as effect of limited accuracy of reconstruction protocols and their "
            "parameterization. Unused values in each row of the matrix are "
            "nullified. Nuclides are identified as hashed nuclide (see "
            ":ref:`NXatom`) for further details."
        ),
        a_nexus_field=NeXusField(
            name="nuclide_whitelist",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    grid_resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-grid-resolution-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Array of edge lengths of the cubic cells used for discretizing the "
            "reconstructed dataset on a cuboidal 3D grid (:ref:`NXcg_grid`). The "
            "tool performs as many delocalization computations as values are "
            "specified in grid_resolution."
        ),
        a_nexus_field=NeXusField(
            name="grid_resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    kernel_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-kernel-size-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Half the width of a :math:`{(2 \\cdot n + 1)}^3` cubic kernel of "
            "cubic voxel beyond which the Gaussian Ansatz function will be "
            "truncated. Intensity outside the kernel is factorized into the "
            "kernel via a normalization procedure."
        ),
        a_nexus_field=NeXusField(
            name="kernel_size",
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
    kernel_variance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-kernel-variance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Array of variance values :math:`\\sigma` of the Gaussian Ansatz "
            "kernel (:math:`\\sigma_x := \\sigma`, :math:`\\sigma_x = \\sigma_y "
            "= 2 \\cdot \\sigma_z`). The tool performs as many delocalization "
            "computations as values are specified in kernel_variance."
        ),
        a_nexus_field=NeXusField(
            name="kernel_variance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    normalization = Quantity(
        type=MEnum(["none", "composition", "concentration"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-normalization-field"
        ],
        description=(
            "How should the results of the kernel-density estimation be "
            "normalized into quantities. By default, the tool computes the total "
            "number (intensity) of ions or elements. Alternatively, the tool can "
            "compute the total intensity, the composition, or the concentration "
            "of the ions/elements specified by the nuclide_whitelist."
        ),
        a_nexus_field=NeXusField(
            name="normalization",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["none", "composition", "concentration"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    has_scalar_fields = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-has-scalar-fields-field"
        ],
        description=(
            "Specifies if the tool should report the delocalization 3D field values."
        ),
        a_nexus_field=NeXusField(
            name="has_scalar_fields",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigDelocalizationIDSurface(Note):
    """
    A precomputed triangulated surface mesh representing a model (of the
    surface) of the edge of the dataset. This model can be used to detect and
    control various sources of bias in the analyses.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-algorithm-field"
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
    vertices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-vertices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "positions for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-indices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "indices for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="indices",
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


class ApmParaprobeNanochemConfigDelocalizationIDSurfaceDistance(Note):
    """
    Distance between each ion and triangulated surface mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="recommended",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-distance-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-distance-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-distance-algorithm-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-surface-distance-distance-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigDelocalizationIDDecomposition(MatchFilter):
    """
    Configuration for the algorithm that defines the multiplicity of each
    reconstructed position during the delocalization.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-decomposition-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="decomposition",
            name_type="specified",
            optionality="required",
        ),
    )

    method = Quantity(
        type=MEnum(
            [
                "resolve_unknown",
                "resolve_point",
                "resolve_atom",
                "resolve_element",
                "resolve_element_charge",
                "resolve_isotope",
                "resolve_isotope_charge",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-decomposition-method-field"
        ],
        description=(
            "The multiplicity of an ion at a reconstructed position is defined "
            "as follows: * resolve_unknown, multiplicity equals 1 for all ions "
            "of the unknown_type This mode is useful for segmenting regions with "
            "poor ranging. * resolve_point, multiplicity equals 1 for all ions "
            "This mode is useful for segmenting point density. * resolve_atom, "
            "multiplicity equals the number of atoms per ion This mode is useful "
            "for segmenting atomic density. * resolve_element, multiplicity "
            "equals the number of elements in the whitelist per ion This mode is "
            "useful for segmenting regions of specific elemental composition "
            "(ignoring nuclids) * resolve_element_charge, ???multiplicity like "
            "resolve_element when charge is met * resolve_isotope, multiplicity "
            "equals the number of nuclides in the whitelist per ion This mode is "
            "useful for segmenting regions of specific isotopic composition * "
            "resolve_isotope_charge, ??? Other multiplicities are 0."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "resolve_unknown",
                "resolve_point",
                "resolve_atom",
                "resolve_element",
                "resolve_element_charge",
                "resolve_isotope",
                "resolve_isotope_charge",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    nuclide_whitelist = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-decomposition-nuclide-whitelist-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("TODO"),
        a_nexus_field=NeXusField(
            name="nuclide_whitelist",
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
    charge_state_whitelist = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-decomposition-charge-state-whitelist-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("TODO"),
        a_nexus_field=NeXusField(
            name="charge_state_whitelist",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigDelocalizationIDInput(Note):
    """
    Serialized result of an already computed delocalization which is for
    performance reasons here just loaded and not computed again.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-input-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-input-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-input-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-input-algorithm-field"
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
    results = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-input-results-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the group within "
            "which individual delocalization results are stored."
        ),
        a_nexus_field=NeXusField(
            name="results",
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


class ApmParaprobeNanochemConfigDelocalizationIDIsosurfacing(Process):
    """
    Configuration of the set of iso-surfaces to compute using that
    delocalization. Such iso-surfaces are the starting point for a
    reconstruction of so-called objects or (microstructural) features. Examples
    of scientific relevant are (line features e.g. dislocations poles, surface
    features such as interfaces, i.e. phase and grain boundaries, or volumetric
    features such as precipitates. Users should be aware that reconstructed
    datasets in atom probe are a model and may face inaccuracies and artifacts
    that can be mistaken incorrectly as microstructural features.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="isosurfacing",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    edge_method = Quantity(
        type=MEnum(["default", "keep_edge_triangles"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-edge-method-field"
        ],
        description=(
            "As it is detailed in `M. Kühbach et al. "
            "<https://arxiv.org/abs/2205.13510>`_, the handling of triangles at "
            "the surface (edge) of the dataset requires special attention "
            "especially for composition-normalized delocalization. Here, it is "
            "possible that the composition increases towards the edge of the "
            "dataset because the quotient of two numbers that are both smaller "
            "than one is larger instead of smaller than the counter. By default, "
            "the tool uses a modified marching cubes algorithm of Lewiner et al. "
            "which detects if voxels face such a situation. In this case, no "
            "triangles are generated for such voxels. Alternatively, "
            "keep_edge_triangles instructs the tool to not remove triangles at "
            "the edge of the dataset at the cost of bias. When using this "
            "keep_edge_triangles users should understand that all features in "
            "contact with the edge of the dataset get usually artificial "
            "enlarged. Consequently, triangulated surface meshes of these "
            "objects are closed during the marching. However, this closure is "
            "artificial and can bias shape analyses for those objects. This also "
            "holds for such practices that are offered in proprietary software "
            "like IVAS / AP Suite. The situation is comparable to analyses of "
            "grain shapes via orientation microscopy from electron microscopy or "
            "X-ray diffraction tomography. Features at the edge of the dataset "
            "may have not been captured fully. Thanks to collaboration with V. "
            "V. Rielli and S. Primig from the Sydney atom probe group, "
            "paraprobe-nanochem implements a complete pipeline to process "
            "features at the edge of the dataset. Specifically, these are "
            "modelled and replaced with closed polyhedral objects using an "
            "iterative mesh and hole-filling procedures with fairing operations. "
            "The tool bookkeeps such objects separately to lead the decision "
            "whether or not to consider these objects to the user. Users should "
            "be aware that results from fairing operations should be compared to "
            "results from analyses where all objects at the edge of the dataset "
            "have been removed. Furthermore, users should be careful with "
            "overestimating the statistical significance of their dataset "
            "especially when using atom probe when they use their atom probe "
            "result to compare different descriptors. Even though a dataset may "
            "deliver statistically significant results for compositions, this "
            "does not necessarily mean that same dataset will also yield "
            "statistically significant and insignificantly biased results for 3D "
            "object analyses! Being able to quantify these effects and making "
            "atom probers aware of these subtleties was one of the main reasons "
            "why the paraprobe-nanochem tool was implemented."
        ),
        a_nexus_field=NeXusField(
            name="edge_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["default", "keep_edge_triangles"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    edge_threshold = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-edge-threshold-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The ion-to-surface distance that is used in the analyses of "
            "features to identify whether these are laying inside the dataset or "
            "close to the surface (edge) of the dataset. If an object has at "
            "least one ion with an ion-to-surface-distance below this threshold, "
            "the object is considered close to the edge of the dataset. The tool "
            "uses a distance-based approach to solve the in general complicated "
            "and involved treatment of computing volumetric intersections "
            "between closed 2-manifolds that are not necessarily convex. The "
            "main practical reason is that such computational geometry analyses "
            "face numerical robustness issues as a consequence of which a mesh "
            "can be detected as being completely inside another mesh although in "
            "reality it is only :math:`\\epsilon`-close only, i.e. almost "
            "touching only the edge (e.g. from inside). Practically, humans "
            "would likely still state in such case that the object is close to "
            "the edge of the dataset; however mathematically the object is "
            "indeed completely inside. In short, a distance-based approach is "
            "rigorous and flexible."
        ),
        a_nexus_field=NeXusField(
            name="edge_threshold",
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
    phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-phi-field"
        ],
        flexible_unit=True,
        description=(
            "Iso-contour values. For each value, the tool computes an "
            "iso-surface and performs subsequent analyses for each iso-surface. "
            "The unit depends on the choice for the normalization of the "
            "accumulated ion intensity values per voxel: * total, total number "
            "of ions, irrespective their iontype * candidates, total number of "
            "ions with type in the isotope_whitelist. * composition, candidates "
            "but normalized by composition, i.e. at.-% * concentration, "
            "candidates but normalized by voxel volume, i.e. ions/nm^3"
        ),
        a_nexus_field=NeXusField(
            name="phi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    has_triangle_soup = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-triangle-soup-field"
        ],
        description=(
            "Specifies if the tool should report the triangle soup which "
            "represents each triangle of the iso-surface complex. The resulting "
            "set of triangles is colloquially referred to as a soup because "
            "different sub-set may not be connected. Each triangle is reported "
            "with an ID specifying to which triangle cluster (with IDs starting "
            "at zero) the triangle belongs. The clustering of triangles within "
            "the soup is performed with a modified DBScan algorithm."
        ),
        a_nexus_field=NeXusField(
            name="has_triangle_soup",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-field"
        ],
        description=(
            "Specifies if the tool should analyze for each cluster of triangles "
            "how they can be combinatorially processed to describe a closed "
            "polyhedron. Such a closed polyhedron (not-necessarily convex!) can "
            "be used to describe objects with relevance in the microstructure. "
            "Users should be aware that the resulting mesh does not necessarily "
            "represent the original precipitate. In fact, inaccuracies in the "
            "reconstructed positions cause inaccuracies in all downstream "
            "processing operations. Especially the effect on one-dimensional "
            "spatial statistics like nearest neighbor correlation functions were "
            "discussed in the literature `B. Gault et al. "
            "<https://doi.org/10.1017/S1431927621012952>`_. In continuation of "
            "these thoughts, this applies also to reconstructed objects. A "
            "well-known example is the discussion of shape deviations of "
            "scandium-rich precipitates in aluminum alloys which in "
            "reconstructions may appear as ellipsoids although they should be "
            "indeed almost spherical provided their size is larger than the "
            "atomic length scale."
        ),
        a_nexus_field=NeXusField(
            name="has_object",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_geometry = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-geometry-field"
        ],
        description=(
            "Specifies if the tool should report a triangulated surface mesh for "
            "each identified closed polyhedron. It is common that a marching "
            "cubes algorithm creates iso-surfaces with a fraction of tiny "
            "sub-complexes (e.g. small isolated tetrahedra). These can be small "
            "tetrahedra/polyhedra about the center of a voxel of the support "
            "grid on which marching cubes operates. Such objects may not contain "
            "an ion; especially when considering that delocalization procedures "
            "smoothen the positions of the ions. Although these small objects "
            "are interesting from a numerical point of view, scientists may "
            "argue they are not worth to be reported because a microstructural "
            "feature should contain at least a few atoms to become relevant. "
            "Therefore, paraprobe-nanochem by default does not report closed "
            "objects which bound a volume that contains no ion."
        ),
        a_nexus_field=NeXusField(
            name="has_object_geometry",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_properties = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-properties-field"
        ],
        description=(
            "Specifies if the tool should report properties of each closed "
            "polyhedron, such as volume and other details."
        ),
        a_nexus_field=NeXusField(
            name="has_object_properties",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_obb = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-obb-field"
        ],
        description=(
            "Specifies if the tool should report for each closed polyhedron an "
            "approximately optimal bounding box fitted to all triangles of the "
            "surface mesh of the object and ion positions inside or on the "
            "surface of the mesh. This bounding box informs about the closed "
            "object's shape (aspect ratios). Users should be aware that the "
            "choice of the algorithm to compute the bounding box can have an "
            "effect on aspect ratio statistics. It is known that computing the "
            "true optimal bounding box of in 3D is an "
            ":math:`\\mathcal{O}^3`-time-complex task. The tool uses "
            "well-established approximate algorithms of the Computational "
            "Geometry Algorithms Library (CGAL)."
        ),
        a_nexus_field=NeXusField(
            name="has_object_obb",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_ions = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-ions-field"
        ],
        description=(
            "Specifies if the tool should report for each closed polyhedron all "
            "evaporation IDs of those ions which lay inside or on the boundary "
            "of the polyhedron. This information is used by the "
            "paraprobe-intersector tool to infer if two objects share common "
            "ions, which is then understood as that the two objects intersect. "
            "Users should be aware that two arbitrarily closed polyhedra in "
            "three-dimensional space can intersect but not share a common ion. "
            "In fact, the volume bounded by the polyhedron has sharp edges and "
            "flat face(t)s. When taking two objects, an edge of one object may "
            "for instance pierce into the surface of another object. In this "
            "case the objects partially overlap / intersect volumetrically; "
            "however this piercing might be so small or happening in the volume "
            "between two reconstructed ion positions. Consequently, sharing ions "
            "is a sufficient but not a necessary condition for interpreting "
            "(volumetric) intersections between objects. Paraprobe-intersector "
            "implements a rigorous alternative to handle such intersections "
            "using a tetrahedralization of closed objects. However, in many "
            "practical cases, we found through examples that there are polyhedra "
            "(especially when they are non-convex and have almost point-like) "
            "connected channels, where tetrahedralization libraries have "
            "challenges dealing with. In this case, checking intersections via "
            "shared_ions is a more practical alternative."
        ),
        a_nexus_field=NeXusField(
            name="has_object_ions",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_edge_contact = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-edge-contact-field"
        ],
        description=(
            "Specifies if the tool should report if a (closed) object has "
            "contact with the surface aka edge of the dataset. For this the tool "
            "currently inspects if the shortest distance between the set of "
            "triangles of the triangulated surface mesh and the triangles of the "
            "edge model is larger than edge_threshold. If this is the case, the "
            "object is assumed to be deeply embedded in the interior of the "
            "dataset. Otherwise, the object is considered to have an edge "
            "contact, i.e. it shape is likely affected by the edge."
        ),
        a_nexus_field=NeXusField(
            name="has_object_edge_contact",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-field"
        ],
        description=(
            "Specifies if the tool should analyze a closed polyhedron (aka "
            "proxy) for each cluster of triangles whose combinatorial analysis "
            "according to has_object returned that the object is not a closed "
            "polyhedron. Such proxies are closed via iterative hole-filling, "
            "mesh refinement, and fairing operations. Users should be aware that "
            "the resulting mesh does not necessarily represent the original "
            "feature. In most cases objects, precipitates in atom probe end up "
            "as open objects because they have been clipped by the edge of the "
            "dataset. Using a proxy is in this case a strategy to still be able "
            "to account for these objects. However, users should make themselves "
            "familiar with the consequences and potential bias which this can "
            "introduce into the analysis."
        ),
        a_nexus_field=NeXusField(
            name="has_proxy",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy_geometry = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-geometry-field"
        ],
        description=("Like has_object_geometry but for the proxies."),
        a_nexus_field=NeXusField(
            name="has_proxy_geometry",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy_properties = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-properties-field"
        ],
        description=("Like has_object_properties but for the proxies."),
        a_nexus_field=NeXusField(
            name="has_proxy_properties",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy_obb = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-obb-field"
        ],
        description=("Like has_object_obb but for the proxies."),
        a_nexus_field=NeXusField(
            name="has_proxy_obb",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy_ions = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-ions-field"
        ],
        description=("Like has_object_ions but for the proxies."),
        a_nexus_field=NeXusField(
            name="has_proxy_ions",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_proxy_edge_contact = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-proxy-edge-contact-field"
        ],
        description=("Like has_object_edge_contact but for the proxies."),
        a_nexus_field=NeXusField(
            name="has_proxy_edge_contact",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_proxigram = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-proxigram-field"
        ],
        description=(
            "Specifies if the tool should report for each closed object a "
            "(cylindrical) region-of-interest (ROI) that gets placed, centered, "
            "and aligned with the local normal for each triangle of the object."
        ),
        a_nexus_field=NeXusField(
            name="has_object_proxigram",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_object_proxigram_edge_contact = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-isosurfacing-has-object-proxigram-edge-contact-field"
        ],
        description=(
            "Specifies if the tool should report for each ROI that was placed at "
            "a triangle of each object if this ROI intersects with the edge the "
            "dataset. Currently, the tool supports cylindrical ROIs. A "
            "computational geometry test is performed to check for a possible "
            "intersection of each ROI with the triangulated surface mesh that is "
            "defined via surface. Results of this cylinder-set-of-triangles "
            "intersection are interpreted as follows: If the cylinder intersects "
            "with at least one triangle of the surface (mesh) the ROI is assumed "
            "to make edge contact. Otherwise, the ROI is assumed to make no edge "
            "contact. Users should note that this approach does not work if the "
            "ROI is laying completely outside the dataset as also in this case "
            "the cylinder intersects with any triangle. However, for atom probe "
            "this case is practically irrelevant provided constructions such as "
            "alpha shapes or alpha wrappings (such as paraprobe-surfacer does) "
            "about the ions of the entire reconstructed volume are used."
        ),
        a_nexus_field=NeXusField(
            name="has_object_proxigram_edge_contact",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigInterfaceMeshingID(ApmParaprobeToolConfigTaskconfig):
    """
    Use a principle component analysis (PCA) to mesh a single free-standing
    interface patch within the reconstructed volume that is decorated by ions
    of specific iontypes (e.g. solute atoms).

    Interface_meshing is a typical starting point for the quantification of
    Gibbsian interfacial excess in cases when closed objects constructed from
    patches e.g. iso-surfaces are not available or when there is no substantial
    or consistently oriented concentration gradients across an interface patch.
    The functionality can also be useful when the amount of latent
    crystallographic information within the point cloud is insufficient or when
    combined with interface_meshing based on ion density traces in
    field-desorption maps (see `Y. Wei et al.
    <https://doi.org/10.1371/journal.pone.0225041>`_ and `A. Breen et al.
    <https://github.com/breen-aj/detector>`_ for details).

    Noteworthy to mention is that the method used is conceptually similar to
    the work of `Z. Peng et al. <https://doi.org/10.1017/S1431927618016112>`_
    and related work (DCOM algorithm) by `P. Felfer et al.
    <https://doi.org/10.1016/j.ultramic.2015.06.002>`_. Compared to these
    implementations paraprobe-nanochem uses inspection functionalities which
    detect potential geometric inconsistencies or self-interactions of the
    evolved DCOM mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="interface_meshingID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    surface = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigInterfaceMeshingIDSurface",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="optional",
        ),
    )
    control_point = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigInterfaceMeshingIDControlPoint",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="control_point",
            name_type="specified",
            optionality="required",
        ),
    )
    decoration_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigInterfaceMeshingIDDecorationFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="decoration_filter",
            name_type="specified",
            optionality="required",
        ),
    )

    initialization = Quantity(
        type=MEnum(["default", "control_point_file"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-initialization-field"
        ],
        description=(
            "How is the PCA initialized: * default, means based on segregated "
            "solutes in the ROI * control_point_file, means based on reading an "
            "external list of control points, currently coming from the Leoben "
            "APT_Analyzer. The control_point_file is currently expected with a "
            "specific format. The Leoben group lead by L. Romaner has developed "
            "a GUI tool `A. Reichmann et al. "
            "<https://github.com/areichm/APT_analyzer>`_ creates a "
            "control_point_file that can be parsed by "
            "paraprobe-parmsetup-nanochem to match the here required formatting "
            "in control_points."
        ),
        a_nexus_field=NeXusField(
            name="initialization",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["default", "control_point_file"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    method = Quantity(
        type=MEnum(["pca_plus_dcom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-method-field"
        ],
        description=(
            "Method used for identifying and refining the location of the "
            "interface. Currently, paraprobe-nanochem implements a PCA followed "
            "by an iterative loop of isotropic mesh refinement and DCOM step(s), "
            "paired with self-intersection detection."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["pca_plus_dcom"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="pca_plus_dcom",
        ),
    )
    number_of_iterations = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-number-of-iterations-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("How many times should the DCOM and mesh refinement be applied?"),
        a_nexus_field=NeXusField(
            name="number_of_iterations",
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
    target_edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-target-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Array of decreasing positive not smaller than one nanometer real "
            "values which specify how the initial triangles of the mesh should "
            "be iteratively refined by edge splitting and related mesh "
            "refinement operations."
        ),
        a_nexus_field=NeXusField(
            name="target_edge_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    target_dcom_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-target-dcom-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Array of decreasing positive not smaller than one nanometer real "
            "values which specify the radius of the spherical region of interest "
            "within which the DCOM algorithm decides for each vertex how the "
            "vertex might be relocated. The larger it is the DCOM radius in "
            "relation to the target_edge_length the more likely it becomes that "
            "vertices will be relocated so substantially that triangle "
            "self-intersections may occur. The tool detects these and stops in a "
            "controlled manner so that the user can repeat the analyses with "
            "using a different parameterization."
        ),
        a_nexus_field=NeXusField(
            name="target_dcom_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    target_smoothing_step = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-target-smoothing-step-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Array of integers which specify for each DCOM step how many times "
            "the mesh should be iteratively smoothened. Users should be aware "
            "that all three arrays target_edge_length, target_dcom_radius, and "
            "target_smoothing_step are interpreted in the same sequence, i.e. "
            "the zeroth entry of each array specifies the respective parameter "
            "values to be used in the first DCOM iteration. The first entry of "
            "each array those for the second DCOM iteration and so on and so "
            "forth."
        ),
        a_nexus_field=NeXusField(
            name="target_smoothing_step",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigInterfaceMeshingIDSurface(Note):
    """
    A precomputed triangulated surface mesh representing a model (of the
    surface) of the edge of the dataset. This model can be used to detect and
    control various sources of bias in the analyses.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-algorithm-field"
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
    vertices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-vertices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "positions for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-surface-indices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "indices for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="indices",
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


class ApmParaprobeNanochemConfigInterfaceMeshingIDControlPoint(Note):
    """
    Details about the control point file used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-control-point-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="control_point",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-control-point-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-control-point-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-control-point-algorithm-field"
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
    control_points = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-control-point-control-points-field"
        ],
        description=("X, Y, Z position matrix of disjoint control points."),
        a_nexus_field=NeXusField(
            name="control_points",
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


class ApmParaprobeNanochemConfigInterfaceMeshingIDDecorationFilter(MatchFilter):
    """
    Specify those nuclides which the tool should inspect iontypes for if they
    contain such nuclides. If this is the case ions of such type are taken with
    the number of nuclides of this multiplicity found. The atoms of these ions
    are assumed to serve as useful markers for locating the interface and
    refining the interface mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-decoration-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="decoration_filter",
            name_type="specified",
            optionality="required",
        ),
    )

    method = Quantity(
        type=MEnum(["whitelist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-decoration-filter-method-field"
        ],
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["whitelist"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="whitelist",
        ),
    )
    match = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-decoration-filter-match-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=("Array of nuclide iontypes to filter."),
        a_nexus_field=NeXusField(
            name="match",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigOnedProfileID(ApmParaprobeToolConfigTaskconfig):
    """
    Analysis of one-dimensional profiles in ROIs placed in the dataset. Such
    analyses are useful for quantifying interfacial excess or for performing
    classical composition analyses.

    The tool will test for each ROIs if it is completely embedded in the
    dataset. Specifically, each such test evaluates if the ROI cuts at least
    one triangle of the triangulated surface mesh that is referred to by
    surface. If this is the case the ROI is marked as one close to the surface
    and not analyzed further. Otherwise, the ROI is marked as one far from the
    surface and processed further.

    For each ROI the tool computes atomically decomposed profiles. This means,
    molecular ions are split into nuclides as many times as their respective
    multiplicity. For each processed ROI the tool stores a sorted list of
    signed distance values to enable post-processing with other software like
    e.g. reporter to perform classical Krakauer/Seidman-style interfacial
    excess analyses.

    Users should be aware that the latter intersection analysis is not a
    volumetric intersection analysis. Given that the triangulated mesh referred
    to in surface is not required to mesh neither a watertight nor convex
    polyhedron a rigorous testing of volumetric intersection is much more
    involved. If the mesh is watertight one could use split the task in first
    tessellating the mesh into convex polyhedra (e.g. tetrahedra and apply a
    volumetric intersection method like the Gilbert-Johnson-Keerthi algorithm
    (GJK). In cases when the mesh is not even watertight distance-based
    segmentation in combination with again intersection of triangles and convex
    polyhedra is a robust but currently not implemented method to quantify
    intersections.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="oned_profileID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    surface = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDSurface",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="optional",
        ),
    )
    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDSurfaceDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="recommended",
        ),
    )
    feature = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDFeature",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="feature",
            name_type="specified",
            optionality="optional",
        ),
    )
    feature_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDFeatureDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="feature_distance",
            name_type="specified",
            optionality="optional",
        ),
    )
    user_defined_roi = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDUserDefinedRoi",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXroi_process",
            name="user_defined_roi",
            name_type="specified",
            optionality="optional",
        ),
    )

    distancing_model = Quantity(
        type=MEnum(["project_to_triangle_plane"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-distancing-model-field"
        ],
        description=("Which type of distance should be reported for the profile."),
        a_nexus_field=NeXusField(
            name="distancing_model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["project_to_triangle_plane"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="project_to_triangle_plane",
        ),
    )
    roi_orientation = Quantity(
        type=MEnum(["triangle_outer_unit_normal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-roi-orientation-field"
        ],
        description=(
            "For each ROI, along which direction should the cylindrical ROI be "
            "oriented if ROIs are placed at triangles of the feature mesh."
        ),
        a_nexus_field=NeXusField(
            name="roi_orientation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["triangle_outer_unit_normal"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="triangle_outer_unit_normal",
        ),
    )
    roi_cylinder_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-roi-cylinder-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "For each ROI, how high (projected onto the cylinder axis) should "
            "the cylindrical ROI be if ROIs are placed at triangles of the "
            "feature mesh."
        ),
        a_nexus_field=NeXusField(
            name="roi_cylinder_height",
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
    roi_cylinder_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-roi-cylinder-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "For each ROI, how wide (in radius) should the cylindrical ROI be if "
            "ROIs are placed at triangles of the feature mesh."
        ),
        a_nexus_field=NeXusField(
            name="roi_cylinder_radius",
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


class ApmParaprobeNanochemConfigOnedProfileIDSurface(Note):
    """
    A precomputed triangulated surface mesh representing a model (of the
    surface) of the edge of the dataset. This model can be used to detect and
    control various sources of bias in the analyses.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-algorithm-field"
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
    vertices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-vertices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "positions for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-indices-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the array of vertex "
            "indices for the triangles in that triangle_set."
        ),
        a_nexus_field=NeXusField(
            name="indices",
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


class ApmParaprobeNanochemConfigOnedProfileIDSurfaceDistance(Note):
    """
    Distance between each ion and triangulated surface mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="recommended",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-distance-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-distance-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-distance-algorithm-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-surface-distance-distance-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the distance "
            "values. The tool assumes that the values are stored in the same "
            "order as points (ions)."
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigOnedProfileIDFeature(Note):
    """
    A precomputed triangulated mesh of the feature representing a model of the
    interface at which to place ROIs to profile. This can be the mesh of an
    interface as returned e.g. by a previous interface_meshing task or the mesh
    of an iso-surface from a previous delocalization task.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="feature",
            name_type="specified",
            optionality="optional",
        ),
    )

    patch_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDFeaturePatchFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="patch_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-algorithm-field"
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
    vertices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-vertices-field"
        ],
        description=(
            "Absolute HDF5 path to the dataset that specifies the array of "
            "vertex positions."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-indices-field"
        ],
        description=(
            "Absolute HDF5 path to the dataset that specifies the array of facet "
            "indices which refer to vertices."
        ),
        a_nexus_field=NeXusField(
            name="indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    facet_normals = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-facet-normals-field"
        ],
        description=(
            "Absolute HDF5 path to the dataset that specifies the array of facet "
            "signed unit normals."
        ),
        a_nexus_field=NeXusField(
            name="facet_normals",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    vertex_normals = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-vertex-normals-field"
        ],
        description=(
            "Absolute HDF5 path to the dataset that specifies the array of "
            "vertex signed unit normals."
        ),
        a_nexus_field=NeXusField(
            name="vertex_normals",
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


class ApmParaprobeNanochemConfigOnedProfileIDFeaturePatchFilter(MatchFilter):
    """
    If interface_model is isosurface this filter can be used to restrict the
    analysis to specific patches of an iso-surface.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-patch-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="patch_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    method = Quantity(
        type=MEnum(["whitelist", "blacklist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-patch-filter-method-field"
        ],
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["whitelist", "blacklist"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    match = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-patch-filter-match-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="match",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigOnedProfileIDFeatureDistance(Note):
    """
    To enable an additional filtration of specific parts of the feature mesh it
    is recommended to feed precomputed distances of each ion to the triangles
    of the feature mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-distance-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-distance-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-distance-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-distance-algorithm-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-feature-distance-distance-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the distance "
            "values. The tool assumes that the values are stored in the same "
            "order as points (ions)."
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigOnedProfileIDUserDefinedRoi(RoiProcess):
    """
    As an alternative mode the tool can be instructed to place ROIs at specific
    locations into the dataset. This is the programmatic equivalent to the
    classical approach in atom probe to place ROIs for composition analyses via
    positioning and rotating them via a graphical user interface (such as in
    IVAS / AP Suite).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXroi_process",
            name="user_defined_roi",
            name_type="specified",
            optionality="optional",
        ),
    )

    cylinder_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOnedProfileIDUserDefinedRoiCylinderSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name="cylinder_set",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigOnedProfileIDUserDefinedRoiCylinderSet(CgCylinder):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-cylinder-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name="cylinder_set",
            name_type="specified",
            optionality="required",
        ),
    )

    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-cylinder-set-index-offset-field"
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
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-cylinder-set-center-field"
        ],
        flexible_unit=True,
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-cylinder-set-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-user-defined-roi-cylinder-set-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
