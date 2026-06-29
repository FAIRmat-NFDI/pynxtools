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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tessellator_results` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)
from pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure import (
    CgFaceListDataStructure,
)
from pynxtools.nomad.metainfo.base_classes.cg_hexahedron import CgHexahedron
from pynxtools.nomad.metainfo.base_classes.cg_polyhedron import CgPolyhedron
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeTessellatorResults"]


class ApmParaprobeTessellatorResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-tessellator
    tool.

    The tool paraprobe-tessellator computes a tessellation of the reconstructed
    positions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tessellator_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_f": "The total number of values required to represent all faces of each cell.",
                "n_f_xdmf": "The total number of values required to represent all faces of each cell\n                (polyhedron) using XDMF.",
            },
        ),
    )

    tessellationID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationID",
        repeats=True,
        variable=True,
        description=(
            "The tool can be used to compute a Voronoi tessellation the entire "
            "or of a sub-set of the reconstructed volume. Each point (ion) is "
            "wrapped in one (Voronoi) cell. The point cloud in the ROI is "
            "wrapped into an axis-aligned bounding box (AABB) that is tight. "
            "This means points at the edge of the point cloud can lay on the "
            "surface of the bounding box. The tool detects if cells make contact "
            "with the walls of this bounding box. The tessellation is computed "
            "without periodic boundary conditions."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_tessellator_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_tessellator_results"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_tessellator_results",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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


class ApmParaprobeTessellatorResultsTessellationID(ApmParaprobeToolProcess):
    """
    The tool can be used to compute a Voronoi tessellation the entire or of a
    sub-set of the reconstructed volume. Each point (ion) is wrapped in one
    (Voronoi) cell. The point cloud in the ROI is wrapped into an axis-aligned
    bounding box (AABB) that is tight. This means points at the edge of the
    point cloud can lay on the surface of the bounding box. The tool detects if
    cells make contact with the walls of this bounding box. The tessellation is
    computed without periodic boundary conditions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="tessellationID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    wall = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWall",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="wall",
            name_type="specified",
            optionality="recommended",
        ),
    )
    voronoi_cells = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDVoronoiCells",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="voronoi_cells",
            name_type="specified",
            optionality="optional",
        ),
    )
    wall_contact_global = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactGlobal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_global",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_left = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactLeft",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_left",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_right = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactRight",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_right",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_front = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactFront",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_front",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_rear = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactRear",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_rear",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_bottom = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactBottom",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_bottom",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wall_contact_top = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDWallContactTop",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_top",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeTessellatorResultsTessellationIDWall(CgHexahedron):
    """
    The (tight) axis-aligned bounding box about the point cloud.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="wall",
            name_type="specified",
            optionality="recommended",
        ),
    )

    closest_corner = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-closest-corner-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Coordinate triplet of the corner that lays closest to the origin of "
            "the *paraprobe* coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="closest_corner",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    farthest_corner = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-farthest-corner-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Coordinate triplet of the corner that lays farthest away from the "
            "origin of the *paraprobe* coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="farthest_corner",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeTessellatorResultsTessellationIDVoronoiCells(CgPolyhedron):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="voronoi_cells",
            name_type="specified",
            optionality="optional",
        ),
    )

    polyhedra = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_results.ApmParaprobeTessellatorResultsTessellationIDVoronoiCellsPolyhedra",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-dimensionality-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The number of points (and thus cells)."),
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
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        shape=["*"],
        description=("Volume of each Voronoi cell."),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLUME",
        ),
    )
    process_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-process-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Which MPI process computed which Voronoi cell."),
        a_nexus_field=NeXusField(
            name="process_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    thread_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-thread-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Which OpenMP thread computed which Voronoi cell."),
        a_nexus_field=NeXusField(
            name="thread_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-index-offset-field"
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
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Sequence of tuples, concatenated in the order of the Voronoi cells. "
            "Each tuple contains encodes information to visualize using XDMF: "
            "Firstly, an XDMF geometric primitive type key. Secondly, the number "
            "of vertices of the polygon. Third, the sequence of indices_vertex "
            "which define the facet. Tuples encode faces faster than cells."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    xdmf_cell_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-xdmf-cell-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Sequence of cell identifier, concatenated such that each face is "
            "associated with its cell. Given that paraprobe-tessellator assigns "
            "each cell the evaporation_id of the ion that the cell wraps this "
            "information enables the segmentation of the tessellation and thus "
            "correlate per-ion properties with the volume that each cell "
            "represents."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_cell_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeTessellatorResultsTessellationIDVoronoiCellsPolyhedra(
    CgFaceListDataStructure
):
    """
    A simple approach to describe the entire set of polyhedra when the main
    intention is to store the shape of the polyhedra for visualization
    purposes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-number-of-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-number-of-faces-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_faces",
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
    indices_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-indices-offset-vertex-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_vertex",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    indices_offset_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-indices-offset-face-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_offset_face",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-voronoi-cells-polyhedra-vertices-field"
        ],
        flexible_unit=True,
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeTessellatorResultsTessellationIDWallContactGlobal(
    CsFilterBooleanMask
):
    """
    A bitmask that documents which of the cells are likely truncated because
    they share at least one face with the *aabb* of the point cloud. This field
    encodes the result of the boolean or operator applied to the value of all
    six wall_contact groups that document contact in specific outer unit normal
    directions of the *aabb*.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-global-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_global",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-global-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-global-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-global-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactLeft(CsFilterBooleanMask):
    """
    In the spirit of wall_contact_global, the left face of *aabb*. Its outer
    unit normal points in the opposite direction of the x-axis of the
    *paraprobe* coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-left-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_left",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-left-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-left-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-left-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactRight(CsFilterBooleanMask):
    """
    In the spirit of wall_contact_global, the right face of *aabb*. Its outer
    unit normal points in the direction of the x-axis of the *paraprobe*
    coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-right-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_right",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-right-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-right-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-right-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactFront(CsFilterBooleanMask):
    """
    In the spirit of wall_contact_global, the front face of *aabb*. Its outer
    unit normal points in the opposite direction of the y-axis of the
    *paraprobe* coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-front-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_front",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-front-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-front-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-front-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactRear(CsFilterBooleanMask):
    """
    In the spirit of wall_contact_global, the rear face of *aabb*. Its outer
    unit normal points in the direction of the y-axis of the *paraprobe*
    coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-rear-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_rear",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-rear-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-rear-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-rear-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactBottom(
    CsFilterBooleanMask
):
    """
    In the spirit of wall_contact_global, the front face of *aabb*. Its outer
    unit normal points in the opposite direction of the z-axis of the
    *paraprobe* coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-bottom-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_bottom",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-bottom-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-bottom-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-bottom-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeTessellatorResultsTessellationIDWallContactTop(CsFilterBooleanMask):
    """
    In the spirit of wall_contact_global, the front face of *aabb*. Its outer
    unit normal points in the direction of the z-axis of the *paraprobe*
    coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-top-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="wall_contact_top",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-top-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-top-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_results.html#nxapm_paraprobe_tessellator_results-entry-tessellationid-wall-contact-top-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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
