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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_surfacer_results` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)
from pynxtools.nomad.metainfo.base_classes.cg_alpha_complex import CgAlphaComplex
from pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure import (
    CgFaceListDataStructure,
)
from pynxtools.nomad.metainfo.base_classes.cg_tetrahedron import CgTetrahedron
from pynxtools.nomad.metainfo.base_classes.cg_triangle import CgTriangle
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeSurfacerResults"]


class ApmParaprobeSurfacerResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-surfacer tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_surfacer_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_v_tri": "The number of vertices of the alpha complex.",
                "n_f_tri": "The number of faces of the alpha complex.",
                "n_f_tri_xdmf": "The total number of XDMF values to represent all faces of triangles via XDMF.",
                "n_f_tet_xdmf": "The total number of XDMF values to represent all faces of tetrahedra via XDMF.",
            },
        ),
    )

    point_set_wrappingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingID",
        repeats=True,
        variable=True,
        description=(
            "Paraprobe-surfacer can be used to load a ROI that is the entire or "
            "a sub-set of the ion point cloud. In the point_cloud_wrapping "
            "process the tool computes a triangulated surface mesh which "
            "encloses the ROI/point cloud. This mesh can be seen as a model for "
            "the edge of the dataset. Different algorithms can be used with "
            "paraprobe-surfacer to create this mesh such as convex hulls, "
            "alpha-shapes as their generalization, or alpha wrappings. Ideally, "
            "the resulting mesh should be a watertight polyhedron. This "
            "polyhedron is not necessarily convex. For some algorithms there is "
            "no guarantee that the resulting mesh yields a watertight mesh."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_surfacer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_surfacer_results"],
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


class ApmParaprobeSurfacerResultsPoint_set_wrappingID(ApmParaprobeToolProcess):
    """
    Paraprobe-surfacer can be used to load a ROI that is the entire or a
    sub-set of the ion point cloud. In the point_cloud_wrapping process the
    tool computes a triangulated surface mesh which encloses the ROI/point
    cloud. This mesh can be seen as a model for the edge of the dataset.

    Different algorithms can be used with paraprobe-surfacer to create this
    mesh such as convex hulls, alpha-shapes as their generalization, or alpha
    wrappings.

    Ideally, the resulting mesh should be a watertight polyhedron. This
    polyhedron is not necessarily convex. For some algorithms there is no
    guarantee that the resulting mesh yields a watertight mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="point_set_wrappingID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    alpha_complexID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_alpha_complex",
            name="alpha_complexID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexID(CgAlphaComplex):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_alpha_complex",
            name="alpha_complexID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    window = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDWindow",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window",
            name_type="specified",
            optionality="required",
        ),
    )
    triangle_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDTriangleSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="triangle_set",
            name_type="specified",
            optionality="optional",
        ),
    )
    interior_tetrahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDInteriorTetrahedra",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_tetrahedron",
            name="interior_tetrahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["2", "3"],
        ),
    )
    type = Quantity(
        type=MEnum(
            ["convex_hull", "alpha_shape", "alpha_wrapping", "other", "undefined"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "convex_hull",
                "alpha_shape",
                "alpha_wrapping",
                "other",
                "undefined",
            ],
        ),
    )
    mode = Quantity(
        type=MEnum(["general", "regularized"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["general", "regularized"],
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-alpha-field"
        ],
        a_nexus_field=NeXusField(
            name="alpha",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDWindow(
    CsFilterBooleanMask
):
    """
    A bitmask which identifies exactly all those ions whose positions were
    considered when defining the filtered point set from which that
    alpha_complex instance was computed.

    This window can be different to the window of the *point_set_wrapping*
    parent group because irrelevant ions might have been filtered out in
    addition to the window defined in *point_set_wrapping* to reduce e.g.
    computational costs of the alpha complex computation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-window-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window",
            name_type="specified",
            optionality="required",
        ),
    )

    number_of_ions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-window-number-of-ions-field"
        ],
        dimensionality="dimensionless",
        description=("Number of ions covered by the mask."),
        a_nexus_field=NeXusField(
            name="number_of_ions",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-window-bitdepth-field"
        ],
        dimensionality="dimensionless",
        description=("Number of bits assumed matching on a default datatype."),
        a_nexus_field=NeXusField(
            name="bitdepth",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-window-mask-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The bitfield of the mask. See :ref:`NXcs_filter_boolean_mask` for "
            "how this bitfield is to be interpreted."
        ),
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDTriangleSet(
    CgTriangle
):
    """
    The set of triangles in the coordinate system paraprobe which discretizes
    the exterior surface of the alpha complex.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="triangle_set",
            name_type="specified",
            optionality="optional",
        ),
    )

    triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDTriangleSetTriangles",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangles",
            name_type="specified",
            optionality="required",
        ),
    )

    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDTriangleSetTriangles(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangles",
            name_type="specified",
            optionality="required",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-dimensionality-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
    )
    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-number-of-vertices-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-number-of-faces-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_faces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-indices-offset-vertex-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_vertex",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_offset_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-indices-offset-face-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_face",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-vertices-field"
        ],
        dimensionality="[length]",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-faces-field"
        ],
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "A list of as many tuples of XDMF topology key, XDMF number of "
            "vertices and a triple of vertex indices specifying each triangle. "
            "The total number of entries is n_f_tri * (1+1+3)."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    is_watertight = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-is-watertight-field"
        ],
        description=(
            "Do the triangles define a triangulated surface mesh that is watertight?"
        ),
        a_nexus_field=NeXusField(
            name="is_watertight",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-triangle-set-triangles-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
        description=(
            "The volume which the triangulated surface mesh encloses if that "
            "mesh is watertight."
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDInteriorTetrahedra(
    CgTetrahedron
):
    """
    The set of tetrahedra which represent the interior volume of the complex if
    that is a closed two-manifold.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_tetrahedron",
            name="interior_tetrahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    tetrahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDInteriorTetrahedraTetrahedra",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="tetrahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
        description=("The accumulated volume of all interior tetrahedra."),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeSurfacerResultsPoint_set_wrappingIDAlpha_complexIDInteriorTetrahedraTetrahedra(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="tetrahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-number-of-vertices-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-number-of-faces-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_faces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-indices-offset-vertex-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_vertex",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_offset_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-indices-offset-face-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_face",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-vertices-field"
        ],
        dimensionality="[length]",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-alpha-complexid-interior-tetrahedra-tetrahedra-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "A list of as many tuples of XDMF topology key, XDMF number of "
            "vertices and a triple of vertex indices specifying each triangle. "
            "The total number of entries is n_f_tet * (1+1+4)."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
