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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_nanochem_results` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.atom import Atom
from pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure import (
    CgFaceListDataStructure,
)
from pynxtools.nomad.metainfo.base_classes.cg_grid import CgGrid
from pynxtools.nomad.metainfo.base_classes.cg_hexahedron import CgHexahedron
from pynxtools.nomad.metainfo.base_classes.cg_polyhedron import CgPolyhedron
from pynxtools.nomad.metainfo.base_classes.cg_roi import CgRoi
from pynxtools.nomad.metainfo.base_classes.cg_triangle import CgTriangle
from pynxtools.nomad.metainfo.base_classes.cg_unit_normal import CgUnitNormal
from pynxtools.nomad.metainfo.base_classes.chemical_composition import (
    ChemicalComposition,
)
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.delocalization import Delocalization
from pynxtools.nomad.metainfo.base_classes.isocontour import Isocontour
from pynxtools.nomad.metainfo.base_classes.process import Process

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
        categories=[ExperimentCategory],
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
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationID",
        repeats=True,
        variable=True,
    )
    interface_meshingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsInterfaceMeshingID",
        repeats=True,
        variable=True,
    )
    oned_profileID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsOnedProfileID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_nanochem_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_nanochem_results"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_nanochem_results",
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


class ApmParaprobeNanochemResultsDelocalizationID(Delocalization):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdelocalization",
            name="delocalizationID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    window = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDWindow",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window",
            name_type="specified",
            optionality="required",
        ),
    )
    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDWindow(CsFilterBooleanMask):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-window-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-window-number-of-ions-field"
        ],
        a_nexus_field=NeXusField(
            name="number_of_ions",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-window-bitdepth-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-window-mask-field"
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


class ApmParaprobeNanochemResultsDelocalizationIDGrid(CgGrid):
    """
    The discretized domain/grid on which the delocalization is applied.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    bounding_box = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridBoundingBox",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="bounding_box",
            name_type="specified",
            optionality="required",
        ),
    )
    scalar_field_magn_SUFFIX = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridScalarFieldMagnSUFFIX",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="scalar_field_magn_SUFFIX",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    scalar_field_grad_SUFFIX = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridScalarFieldGradSUFFIX",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="scalar_field_grad_SUFFIX",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    iso_surfaceID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXisocontour",
            name="iso_surfaceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The total number of cells/voxels of the grid."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-origin-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-symmetry-field"
        ],
        description=(
            "The symmetry of the lattice defining the shape of the unit cell."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-cell-dimensions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The unit cell dimensions according to the coordinate system defined "
            "under coordinate_system."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-extent-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Number of unit cells along each of the d-dimensional base vectors. "
            "The total number of cells, or grid points has to be the "
            "cardinality. If the grid has an irregular number of grid positions "
            "in each direction, as it could be for instance the case of a grid "
            "where all grid points outside some masking primitive are removed, "
            "this extent field should not be used. Instead use the coordinate "
            "field."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer which specifies the first index to be used for "
            "distinguishing identifiers for cells. Identifiers are defined "
            "either implicitly or explicitly. For implicit indexing the "
            "identifiers are defined on the interval "
            ":math:`[identifier\\_offset, identifier\\_offset + c - 1]`. For "
            "explicit indexing the identifier array has to be defined."
        ),
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
    kernel_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-kernel-size-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[3],
        description=(
            "Halfwidth of the kernel about the central voxel. The shape of the "
            "kernel is that of a cuboid of extent 2*kernel_extent[i] + 1 in each "
            "dimension i."
        ),
        a_nexus_field=NeXusField(
            name="kernel_size",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    kernel_type = Quantity(
        type=MEnum(["gaussian"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-kernel-type-field"
        ],
        description=("Functional form of the kernel (Ansatz function)."),
        a_nexus_field=NeXusField(
            name="kernel_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["gaussian"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="gaussian",
        ),
    )
    kernel_sigma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-kernel-sigma-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Standard deviation :math:`\\sigma_i` of the kernel in each "
            "dimension in the paraprobe coordinate_system with i = 0 is x, i = 1 "
            "is y, i = 2 is z."
        ),
        a_nexus_field=NeXusField(
            name="kernel_sigma",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    kernel_mu = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-kernel-mu-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Expectation value :math:`\\mu_i` of the kernel in each dimension in "
            "the paraprobe coordinate_system with i = 0 is x, i = 1 is y, i = 2 "
            "is z."
        ),
        a_nexus_field=NeXusField(
            name="kernel_mu",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    normalization = Quantity(
        type=MEnum(["total", "candidates", "composition", "concentration"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-normalization-field"
        ],
        description=(
            "How were results of the kernel-density estimation normalized: * "
            "total, the total number (intensity) of ions or elements. * "
            "candidates, the total number (intensity) of ions matching "
            "weighting_model * composition, the value for candidates divided by "
            "the value for total, * concentration, the value for candidates "
            "divided by the volume of the cell."
        ),
        a_nexus_field=NeXusField(
            name="normalization",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["total", "candidates", "composition", "concentration"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridBoundingBox(CgHexahedron):
    """
    A tight axis-aligned bounding box about the grid.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="bounding_box",
            name_type="specified",
            optionality="required",
        ),
    )

    hexahedron = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridBoundingBoxHexahedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedron",
            name_type="specified",
            optionality="required",
        ),
    )

    is_axis_aligned = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-is-axis-aligned-field"
        ],
        shape=["*"],
        description=("For atom probe should be set to true."),
        a_nexus_field=NeXusField(
            name="is_axis_aligned",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer which specifies the first index to be used for "
            "distinguishing hexahedra. Identifiers are defined either implicitly "
            "or explicitly. For implicit indexing the identifiers are defined on "
            "the interval :math:`[identifier\\_offset, identifier\\_offset + c - "
            "1]`. For explicit indexing the identifier array has to be defined."
        ),
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridBoundingBoxHexahedron(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedron",
            name_type="specified",
            optionality="required",
        ),
    )

    vertex_index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-vertex-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer which specifies the first index to be used for "
            "distinguishing identifiers for vertices. Identifiers are defined "
            "either implicitly or explicitly. For implicit indexing the "
            "identifiers are defined on the interval "
            ":math:`[identifier\\_offset, identifier\\_offset + c - 1]`. For "
            "explicit indexing the identifier array has to be defined."
        ),
        a_nexus_field=NeXusField(
            name="vertex_index_offset",
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
    face_index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-face-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer which specifies the first index to be used for "
            "distinguishing identifiers for faces. Identifiers are defined "
            "either implicitly or explicitly. For implicit indexing the "
            "identifiers are defined on the interval "
            ":math:`[identifier\\_offset, identifier\\_offset + c - 1]`. For "
            "explicit indexing the identifier array has to be defined."
        ),
        a_nexus_field=NeXusField(
            name="face_index_offset",
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
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[8, 3],
        description=(
            "Positions of the vertices. Users are encouraged to reduce the "
            "vertices to unique set of positions and vertices as this supports a "
            "more efficient storage of the geometry data. It is also possible "
            "though to store the vertex positions naively in which case "
            "vertices_are_unique is likely False. Naively here means that one "
            "for example stores each vertex of a triangle mesh even though many "
            "vertices are shared between triangles and thus the positions of "
            "these vertices do not have to be duplicated."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    faces = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-faces-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6, 4],
        description=(
            "Array of identifiers from vertices which describe each face. The "
            "first entry is the identifier of the start vertex of the first "
            "face, followed by the second vertex of the first face, until the "
            "last vertex of the first face. Thereafter, the start vertex of the "
            "second face, the second vertex of the second face, and so on and so "
            "forth. Therefore, summating over the number_of_vertices, allows to "
            "extract the vertex identifiers for the i-th face on the following "
            "index interval of the faces array: :math:`[\\sum_{i = 0}^{i = n-1}, "
            "\\sum_{i=0}^{i = n}]`."
        ),
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[36],
        description=(
            "Six equally formatted sextets chained together. For each sextett "
            "the first entry is an XDMF primitive topology key (here 5 for "
            "polygon), the second entry the XDMF primitive count value (here 4 "
            "because each face is a quad). The remaining four values are the "
            "vertex indices."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    number_of_boundaries = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-number-of-boundaries-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many distinct boundaries are distinguished? Most grids "
            "discretize a cubic or cuboidal region. In this case six sides can "
            "be distinguished, each making an own boundary."
        ),
        a_nexus_field=NeXusField(
            name="number_of_boundaries",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    boundaries = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-boundaries-field"
        ],
        shape=[6],
        description=(
            "Name of the boundaries. E.g. left, right, front, back, bottom, top, "
            "The field must have as many entries as there are "
            "number_of_boundaries."
        ),
        a_nexus_field=NeXusField(
            name="boundaries",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    boundary_conditions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-bounding-box-hexahedron-boundary-conditions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6],
        description=(
            "The boundary conditions for each boundary: 0 - undefined 1 - open 2 "
            "- periodic 3 - mirror 4 - von Neumann 5 - Dirichlet"
        ),
        a_nexus_field=NeXusField(
            name="boundary_conditions",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridScalarFieldMagnSUFFIX(Data):
    r"""
    The result of the delocalization :math:`\Phi = f(x, y, z)` based on which
    subsequent iso-surfaces will be computed. In commercial software so far
    there is no possibility to export this information.

    If the intensity for all matches of the weighting_model are summarized,
    name this NXdata instance scalar_field_magn_total.

    If the intensity is reported for each iontype, one can avoid many
    subsequent computations as individual intensities can be reinterpreted
    using a different weighting_model in down-stream usage of the here reported
    values (e.g. with Python scripting). In this case name the individual
    NXdata instances scalar_field_magn_ionID using the ID of the ion as per the
    configuration of the ranging definitions used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-magn-suffix-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="scalar_field_magn_SUFFIX",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    xdmf_intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-magn-suffix-xdmf-intensity-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Intensity of the field at given point"),
        a_nexus_field=NeXusField(
            name="xdmf_intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    xdmf_xyz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-magn-suffix-xdmf-xyz-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Center of mass positions of each voxel for rendering the scalar "
            "field via XDMF in e.g. Paraview."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_xyz",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    xdmf_topology = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-magn-suffix-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "XDMF topology for rendering in combination with xdmf_xyz the scalar "
            "field via XDMF in e.g. Paraview."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridScalarFieldGradSUFFIX(Data):
    """
    The three-dimensional gradient :math:`\nabla \\Phi`. Follow the naming
    convention of scalar_field_magn_SUFFIX to report parallel structures.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-grad-suffix-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="scalar_field_grad_SUFFIX",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    xdmf_gradient = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-grad-suffix-xdmf-gradient-field"
        ],
        flexible_unit=True,
        shape=["*", 3],
        description=(
            "The gradient vector formatted for direct visualization via XDMF in "
            "e.g. Paraview."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_gradient",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    xdmf_xyz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-grad-suffix-xdmf-xyz-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Center of mass positions of each voxel for rendering the scalar "
            "field gradient via XDMF in e.g. Paraview."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_xyz",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    xdmf_topology = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-scalar-field-grad-suffix-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "XDMF topology for rendering in combination with xdmf_xyz the scalar "
            "field via XDMF in e.g. Paraview."
        ),
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceID(Isocontour):
    """
    An iso-surface is the boundary between two regions across which the
    magnitude of a scalar field falls below/exceeds a threshold magnitude
    :math:`\varphi`.

    For applications in atom probe microscopy, the location and shape of such a
    boundary (set) is typically approximated by discretization - triangulation
    to be specific.

    This yields a complex of not necessarily connected geometric primitives.
    Paraprobe-nanochem approximates this complex with a soup of triangles.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXisocontour",
            name="iso_surfaceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    triangle_soup = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoup",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="triangle_soup",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    isovalue = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-isovalue-field"
        ],
        flexible_unit=True,
        description=("The threshold or iso-contour value :math:`\\varphi`."),
        a_nexus_field=NeXusField(
            name="isovalue",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    marching_cubes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-marching-cubes-field"
        ],
        description=(
            "Reference to the specific implementation of marching cubes used. "
            "The value placed here should be a DOI. If there are no specific DOI "
            "or details write not_further_specified, or give at least a "
            "free-text description. The program and version used is the specific "
            "paraprobe-nanochem."
        ),
        a_nexus_field=NeXusField(
            name="marching_cubes",
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


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoup(
    CgTriangle
):
    """
    The resulting triangle soup computed via marching cubes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="triangle_soup",
            name_type="specified",
            optionality="optional",
        ),
    )

    triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTriangles",
        repeats=False,
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-cardinality-field"
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
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-index-offset-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTriangles(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangles",
            name_type="specified",
            optionality="required",
        ),
    )

    vertex_normal = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVertexNormal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="vertex_normal",
            name_type="specified",
            optionality="optional",
        ),
    )
    face_normal = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesFaceNormal",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="face_normal",
            name_type="specified",
            optionality="optional",
        ),
    )
    volumetric_features = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeatures",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="volumetric_features",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-number-of-vertices-field"
        ],
        a_nexus_field=NeXusField(
            name="number_of_vertices",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    number_of_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-number-of-faces-field"
        ],
        a_nexus_field=NeXusField(
            name="number_of_faces",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    vertex_index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-vertex-index-offset-field"
        ],
        a_nexus_field=NeXusField(
            name="vertex_index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    face_index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-index-offset-field"
        ],
        a_nexus_field=NeXusField(
            name="face_index_offset",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Positions of the vertices. Users are encouraged to reduce the "
            "vertices to a unique set as this may result in a more efficient "
            "storage of the geometry data. It is also possible though to store "
            "the vertex positions naively in which case vertices_are_unique is "
            "likely False. Naively here means that each vertex is stored even "
            "though many share the same positions."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-faces-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Array of identifiers from vertices which describe each face. The "
            "first entry is the identifier of the start vertex of the first "
            "face, followed by the second vertex of the first face, until the "
            "last vertex of the first face. Thereafter, the start vertex of the "
            "second face, the second vertex of the second face, and so on and so "
            "forth. Therefore, summating over the number_of_vertices, allows to "
            "extract the vertex identifiers for the i-th face on the following "
            "index interval of the faces array: :math:`[\\sum_{i = 0}^{i = n-1}, "
            "\\sum_{i=0}^{i = n}]`."
        ),
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
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
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Array of edge length values. For each triangle the edge length is "
            "reported for the edges traversed according to the sequence in which "
            "vertices are indexed in triangles."
        ),
        a_nexus_field=NeXusField(
            name="edge_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    interior_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-interior-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 4],
        description=(
            "Array of interior angle values. For each triangle the angle is "
            "reported for the angle opposite to the edges which are traversed "
            "according to the sequence in which vertices are indexed in "
            "triangles."
        ),
        a_nexus_field=NeXusField(
            name="interior_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-center-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=("The center of mass of each triangle."),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVertexNormal(
    CgUnitNormal
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-vertex-normal-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="vertex_normal",
            name_type="specified",
            optionality="optional",
        ),
    )

    normals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-vertex-normal-normals-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=("Direction of each normal."),
        a_nexus_field=NeXusField(
            name="normals",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-vertex-normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Qualifier how which specifically oriented normal to its primitive "
            "each normal represents. * 0 - undefined * 1 - outer * 2 - inner"
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesFaceNormal(
    CgUnitNormal
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-normal-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_unit_normal",
            name="face_normal",
            name_type="specified",
            optionality="optional",
        ),
    )

    normals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-normal-normals-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=("Direction of each normal."),
        a_nexus_field=NeXusField(
            name="normals",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Qualifier how which specifically oriented normal to its primitive "
            "each normal represents. * 0 - undefined * 1 - outer * 2 - inner"
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    gradient_guide_magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-normal-gradient-guide-magnitude-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Triangle normals are oriented in the direction of the gradient "
            "vector of the local delocalized scalar field. :math:`\\sum_{x, y, "
            "z} {\\nabla{c}_i}^2`."
        ),
        a_nexus_field=NeXusField(
            name="gradient_guide_magnitude",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    gradient_guide_projection = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-face-normal-gradient-guide-projection-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Triangle normals are oriented in the direction of the gradient "
            "vector of the local delocalized scalar field. The projection "
            "variable here describes the cosine of the angle between the "
            "gradient direction and the normal direction vector. This is a "
            "descriptor of how parallel the projection is that is especially "
            "useful to document those triangles for whose the projection is "
            "almost perpendicular."
        ),
        a_nexus_field=NeXusField(
            name="gradient_guide_projection",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeatures(
    Process
):
    """
    Iso-surfaces of arbitrary scalar three-dimensional fields can show a
    complicated topology. Paraprobe-nanochem can run a DBScan-like clustering
    algorithm which performs a connectivity analysis on the triangle soup
    representation of such iso-surface. This may yield a set of connected
    features whose individual surfaces are discretized by a triangulated mesh
    each. Such volumetric features can be processed further using
    paraprobe-nanochem using a workflow with at most two steps.

    In the first step, the tool distinguishes three types of (v) i.e.
    volumetric features:

    1. So-called objects, i.e. necessarily watertight features represented by
    polyhedra. These objects were already watertight within the triangulated
    iso-surface. 2. So-called proxies, i.e. features that were not necessarily
    watertight within the triangulated iso-surface but were subsequently
    replaced by a watertight mesh using polyhedral mesh processing operations
    (hole filling, refinement, fairing operations). 3. Remaining triangle
    surface meshes or parts of these of arbitrary shape and cardinality that
    are not transformable into proxies or for which no transformation into
    proxies was instructed.

    These features can be interpreted as microstructural features. Some of them
    may be precipitates, some of them may be poles, some of them may be
    segments of dislocation lines or other crystal defects which are decorated
    (or not) with solutes.

    In the second step, the tool can be used to analyze the proximity of these
    objects to a model of the surface (edge) of the dataset.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="volumetric_features",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    FEATURE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeature",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="FEATURE",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=6,
        ),
    )

    indices_triangle_cluster = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-indices-triangle-cluster-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The identifier which the triangle_soup connectivity analysis "
            "returned, which constitutes the first step of the "
            "volumetric_feature identification process."
        ),
        a_nexus_field=NeXusField(
            name="indices_triangle_cluster",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    feature_type_dict_keyword = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-type-dict-keyword-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("The array of keywords of feature_type dictionary."),
        a_nexus_field=NeXusField(
            name="feature_type_dict_keyword",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    feature_type_dict_value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-type-dict-value-field"
        ],
        shape=["*"],
        description=(
            "The array of values for each keyword of the feature_type dictionary."
        ),
        a_nexus_field=NeXusField(
            name="feature_type_dict_value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    feature_type = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-type-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The array of controlled keywords, need to be from "
            "feature_type_dict_keyword, which specify which type each feature "
            "triangle cluster belongs to. Keep in mind that not each feature is "
            "an object or proxy."
        ),
        a_nexus_field=NeXusField(
            name="feature_type",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-indices-feature-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("The explicit identifier of features."),
        a_nexus_field=NeXusField(
            name="indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeature(
    Process
):
    """
    In all situations instances of the parent NXprocess group are returned with
    a very similar information structuring and thus we here replace the
    template name FEATURE with one of the following types feature-specific
    group names:

    * objects, objects, irrespective their distance to the surface *
    objects_close_to_edge, sub-set of v_feature_object close surface *
    objects_far_from_edge, sub-set of v_feature_object not close to the surface
    * proxies, proxies, irrespective their distance to the surface *
    proxies_close_to_edge, sub-set of v_feature_proxies, close to surface *
    proxies_far_from_edge, sub-set of v_feature_proxies, not close to surface
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="FEATURE",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=6,
        ),
    )

    obb = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObb",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="obb",
            name_type="specified",
            optionality="optional",
        ),
    )
    objectID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObjectID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="objectID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    composition = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureComposition",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXchemical_composition",
            name="composition",
            name_type="specified",
            optionality="optional",
        ),
    )

    indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-indices-feature-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Explicit identifier of the feature a sub-set of the indices_feature "
            "in the parent group."
        ),
        a_nexus_field=NeXusField(
            name="indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        shape=["*"],
        description=("Volume of the feature. NaN for non-watertight objects."),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObb(
    CgHexahedron
):
    """
    An oriented bounding box (OBB) to each object.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="obb",
            name_type="specified",
            optionality="optional",
        ),
    )

    hexahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObbHexahedra",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Edge length of the oriented bounding box from largest to smallest value."
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    aspect = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-aspect-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        description=(
            "Oriented bounding box aspect ratio. YX versus ZY or second-largest "
            "over largest and smallest over second largest."
        ),
        a_nexus_field=NeXusField(
            name="aspect",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-center-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Position of the geometric center, which often is but not "
            "necessarily has to be the center_of_mass of the hexahedrally-shaped "
            "sample/sample part."
        ),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObbHexahedra(
    CgFaceListDataStructure
):
    """
    A simple approach to describe the entire set of hexahedra when the main
    intention is to store the shape of the hexahedra for visualization.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-hexahedra-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedra",
            name_type="specified",
            optionality="optional",
        ),
    )

    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-hexahedra-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-hexahedra-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_feature_xdmf = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-obb-hexahedra-indices-feature-xdmf-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_feature_xdmf",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObjectID(
    CgPolyhedron
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="objectID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    polyhedron = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObjectIDPolyhedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedron",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureObjectIDPolyhedron(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="polyhedron",
            name_type="specified",
            optionality="required",
        ),
    )

    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-faces-field"
        ],
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    face_normals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-face-normals-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="face_normals",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="xdmf_topology",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    xdmf_indices_feature = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-xdmf-indices-feature-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="xdmf_indices_feature",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    ion_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-objectid-polyhedron-ion-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Array of evaporation_id / identifier_ion which details which ions "
            "lie inside or on the surface of the feature."
        ),
        a_nexus_field=NeXusField(
            name="ion_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureComposition(
    ChemicalComposition
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXchemical_composition",
            name="composition",
            name_type="specified",
            optionality="optional",
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureCompositionAtom",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    total = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-total-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Total (count) of ions inside or on the surface of the feature "
            "relevant for normalization. NaN for non watertight objects."
        ),
        a_nexus_field=NeXusField(
            name="total",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsDelocalizationIDGridIsoSurfaceIDTriangleSoupTrianglesVolumetricFeaturesFeatureCompositionAtom(
    Atom
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-atom-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    charge_state = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-atom-charge-state-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="charge_state",
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
    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-atom-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    nuclide_list = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-atom-nuclide-list-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="nuclide_list",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    count = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-delocalizationid-grid-iso-surfaceid-triangle-soup-triangles-volumetric-features-feature-composition-atom-count-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Count or weight which, when divided by total, yields the "
            "composition of this element, nuclide, or (molecular) ion within the "
            "volume of the feature/object."
        ),
        a_nexus_field=NeXusField(
            name="count",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsInterfaceMeshingID(ApmParaprobeToolProcess):
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

    initial_interface = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsInterfaceMeshingIDInitialInterface",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="initial_interface",
            name_type="specified",
            optionality="optional",
        ),
    )
    mesh_stateID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsInterfaceMeshingIDMeshStateID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="mesh_stateID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    ion_multiplicity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-ion-multiplicity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
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
        a_nexus_field=NeXusField(
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
        unit="dimensionless",
        shape=["*"],
        description=(
            "The multiplicity whereby the ion position is accounted for when the "
            "ion is considered one which is a decorator of the interface."
        ),
        a_nexus_field=NeXusField(
            name="decorator_multiplicity",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsInterfaceMeshingIDInitialInterface(Process):
    """
    The equation of the plane that is fitted initially.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-initial-interface-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="initial_interface",
            name_type="specified",
            optionality="optional",
        ),
    )

    point_normal_form = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-initial-interface-point-normal-form-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[4],
        description=(
            "The four parameter :math:`ax + by + cz + d = 0` which define the plane."
        ),
        a_nexus_field=NeXusField(
            name="point_normal_form",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsInterfaceMeshingIDMeshStateID(CgTriangle):
    """
    The triangle surface mesh representing the interface model. Exported at
    state before or after the next DCOM step.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="mesh_stateID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsInterfaceMeshingIDMeshStateIDTriangles",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="triangles",
            name_type="specified",
            optionality="required",
        ),
    )

    state = Quantity(
        type=MEnum(["before", "after"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-state-field"
        ],
        description=("Was this state exported before or after the next DCOM step."),
        a_nexus_field=NeXusField(
            name="state",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["before", "after"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-cardinality-field"
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
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-index-offset-field"
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
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_AREA",
        ),
    )
    edge_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-edge-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Array of edge length values. For each triangle the edge length is "
            "reported for the edges traversed according to the sequence in which "
            "vertices are indexed in triangles."
        ),
        a_nexus_field=NeXusField(
            name="edge_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    interior_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-interior-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 4],
        description=(
            "Array of interior angle values. For each triangle the angle is "
            "reported for the angle opposite to the edges which are traversed "
            "according to the sequence in which vertices are indexed in "
            "triangles."
        ),
        a_nexus_field=NeXusField(
            name="interior_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsInterfaceMeshingIDMeshStateIDTriangles(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-number-of-vertices-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-number-of-faces-field"
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
    index_offset_vertex = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-index-offset-vertex-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset_vertex",
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
    index_offset_edge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-index-offset-edge-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset_edge",
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
    index_offset_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-index-offset-face-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset_face",
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
    indices_face = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-indices-face-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_face",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    vertex_normal_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-vertex-normal-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=("Direction of each vertex normal."),
        a_nexus_field=NeXusField(
            name="vertex_normal",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    vertex_normal_orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-vertex-normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Qualifier which details how specifically oriented the face normal "
            "is with respect to its primitive (triangle): * 0 - undefined * 1 - "
            "outer * 2 - inner"
        ),
        a_nexus_field=NeXusField(
            name="vertex_normal_orientation",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-faces-field"
        ],
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    face_normal_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-face-normal-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=("Direction of each face normal."),
        a_nexus_field=NeXusField(
            name="face_normal",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    face_normal_orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-face-normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Qualifier which details how specifically oriented the face normal "
            "is with respect to its primitive (triangle): * 0 - undefined * 1 - "
            "outer * 2 - inner"
        ),
        a_nexus_field=NeXusField(
            name="face_normal_orientation",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    xdmf_topology = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-interface-meshingid-mesh-stateid-triangles-xdmf-topology-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
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


class ApmParaprobeNanochemResultsOnedProfileID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-group"
        ],
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

    xdmf_cylinder = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinder",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="xdmf_cylinder",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinder(CgPolyhedron):
    """
    The ROIs are defined as cylinders for the computations. To visualize these
    we discretize them into regular n-gons. Using for instance 360-gons, i.e. a
    regular n-gon with 360 edges, resolves the lateral surface of each cylinder
    such that their renditions are smooth in visualization software like
    Paraview.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="xdmf_cylinder",
            name_type="specified",
            optionality="required",
        ),
    )

    rois_far_from_edge = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinderRoisFarFromEdge",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rois_far_from_edge",
            name_type="specified",
            optionality="required",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-cardinality-field"
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
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-center-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "Position of the geometric center, which often is but not "
            "necessarily has to be the center_of_mass of the polyhedra."
        ),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    orientation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-orientation-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "The orientation of the ROI defined via a vector which points along "
            "the cylinder axis and whose length is the height of the cylinder."
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    roi_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-roi-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("XDMF support to enable coloring each ROI by its identifier."),
        a_nexus_field=NeXusField(
            name="roi_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    edge_contact = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-edge-contact-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "XDMF support to enable coloring each ROI whether it has edge "
            "contact or not."
        ),
        a_nexus_field=NeXusField(
            name="edge_contact",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_atoms = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-number-of-atoms-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "XDMF support to enable coloring each ROI by its number of atoms."
        ),
        a_nexus_field=NeXusField(
            name="number_of_atoms",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_ions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-number-of-ions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("XDMF support to enable coloring each ROI by its number of ions."),
        a_nexus_field=NeXusField(
            name="number_of_ions",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinderRoisFarFromEdge(Process):
    """
    Distance and iontype-specific processed data for each ROI. Arrays
    signed_distance and nuclide_hash are sorted by increasing distance. Array
    nuclide_hash reports one hash for each atom of each isotope. Effectively,
    this can yield to groups of values on signed_distance with the same
    distance value as molecular ions are reported decomposed into their atoms.
    Therefore, the XDMF support fields number_of_atoms and number_of_ions are
    only expected to display pairwise the same values respectively, if all ions
    are built from a single atom only.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-rois-far-from-edge-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="rois_far_from_edge",
            name_type="specified",
            optionality="required",
        ),
    )

    roiID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_nanochem_results.ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinderRoisFarFromEdgeRoiID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_roi",
            name="roiID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeNanochemResultsOnedProfileIDXdmfCylinderRoisFarFromEdgeRoiID(CgRoi):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-rois-far-from-edge-roiid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_roi",
            name="roiID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    signed_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-rois-far-from-edge-roiid-signed-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Sorted in increasing order projected along the positive direction "
            "of the ROI as defined by orientation in the parent group."
        ),
        a_nexus_field=NeXusField(
            name="signed_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_nanochem_results.html#nxapm_paraprobe_nanochem_results-entry-oned-profileid-xdmf-cylinder-rois-far-from-edge-roiid-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Hashvalue as defined in :ref:`NXatom`."),
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
