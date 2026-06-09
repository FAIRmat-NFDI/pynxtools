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
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigInterface_meshingID",
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
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_config.ApmParaprobeNanochemConfigOned_profileID",
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


class ApmParaprobeNanochemConfigDelocalizationID(
    ApmParaprobeToolConfigApmParaprobeToolParameters
):
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

    isosurfacing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
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
    )
    nuclide_whitelist = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-nuclide-whitelist-field"
        ],
        dimensionality="dimensionless",
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
    )
    kernel_variance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-delocalizationid-kernel-variance-field"
        ],
        dimensionality="[length]",
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
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemConfigInterface_meshingID(
    ApmParaprobeToolConfigApmParaprobeToolParameters
):
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
    )
    number_of_iterations = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-number-of-iterations-field"
        ],
        dimensionality="dimensionless",
        description=("How many times should the DCOM and mesh refinement be applied?"),
        a_nexus_field=NeXusField(
            name="number_of_iterations",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    target_edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-interface-meshingid-target-edge-length-field"
        ],
        dimensionality="[length]",
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


class ApmParaprobeNanochemConfigOned_profileID(
    ApmParaprobeToolConfigApmParaprobeToolParameters
):
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

    user_defined_roi = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.roi_process.RoiProcess",
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
    )
    roi_cylinder_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-roi-cylinder-height-field"
        ],
        dimensionality="[length]",
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
    )
    roi_cylinder_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_config.html#nxapm_paraprobe_nanochem_config-entry-oned-profileid-roi-cylinder-radius-field"
        ],
        dimensionality="[length]",
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
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
