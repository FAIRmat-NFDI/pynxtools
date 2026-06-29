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
# Run `pynx nomad generate-metainfo --nxdl NXcg_grid` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgGrid"]


class CgGrid(CgPrimitive):
    """
    Computational geometry description of a grid of Wigner-Seitz cells in
    Euclidean space.

    Three-dimensional grids with cubic cells are if not the most frequently
    used example of such grids. Numerical methods and models that use grids are
    used in many cases in the natural sciences and engineering disciplines.
    Examples are discretizations in space and time used for phase-field,
    cellular automata, or Monte Carlo modeling.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_grid",
            category="base",
            symbols={
                "d": "The dimensionality of the grid.",
                "c": "The cardinality or total number of cells aka grid points.",
                "n_b": "Number of boundaries of the bounding box or primitive housing the grid.",
            },
        ),
    )

    bounding_box = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=False,
        description=("A tight bounding box about the grid."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="bounding_box",
            name_type="specified",
            optionality="optional",
        ),
    )

    origin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-origin-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Location of the origin of the grid. Use the depends_on field that "
            "is inherited from the :ref:`NXcg_primitive` class to specify the "
            "coordinate system in which the origin location is defined."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    symmetry = Quantity(
        type=MEnum(["cubic"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-symmetry-field"
        ],
        description=(
            "The symmetry of the lattice defining the shape of the unit cell."
        ),
        a_nexus_field=NeXusField(
            name="symmetry",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-cell-dimensions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("The unit cell dimensions using crystallographic notation."),
        a_nexus_field=NeXusField(
            name="cell_dimensions",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    extent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-extent-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Number of unit cells along each of the d unit vectors. The total "
            "number of cells or grid points has to be the cardinality. If the "
            "grid has an irregular number of grid positions in each direction, "
            "as it could be for instance the case of a grid where all grid "
            "points outside some masking primitive are removed, this extent "
            "field should not be used. Instead, use the coordinate field."
        ),
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-position-field"
        ],
        flexible_unit=True,
        shape=["*", "*"],
        description=("Position of each cell in Euclidean space."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    coordinate = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-coordinate-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=("Coordinate of each cell with respect to the discrete grid."),
        a_nexus_field=NeXusField(
            name="coordinate",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    number_of_boundaries = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-number-of-boundaries-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Number of boundaries distinguished Most grids discretize a cubic or "
            "cuboidal region. In this case six sides can be distinguished, each "
            "making an own boundary."
        ),
        a_nexus_field=NeXusField(
            name="number_of_boundaries",
            type="NX_UINT",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-boundaries-field"
        ],
        shape=["*"],
        description=(
            "Name of domain boundaries of the simulation box/ROI e.g. left, "
            "right, front, back, bottom, top."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-boundary-conditions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
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
    surface_reconstruction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_grid.html#nxcg_grid-surface-reconstruction-field"
        ],
        description=(
            "Details about the computational geometry method and implementation "
            "used for discretizing internal surfaces as e.g. obtained with "
            "marching methods, like marching squares or marching cubes. "
            "Documenting which specific version was used helps with "
            "understanding how robust the results are with respect to the "
            "topology of the triangulation. Reference to the specific "
            "implementation of marching cubes used. See for example the "
            "following papers for details about how to identify a DOI which "
            "specifies the implementation used: * `W. E. Lorensen "
            "<https://doi.org/10.1109/MCG.2020.2971284>`_ * `T. S. Newman and H. "
            "Yi <https://doi.org/10.1016/j.cag.2006.07.021>`_ The value placed "
            "here should ideally be an identifier of a program. If not possible, "
            "an identifier for a paper, technical report, or free-text "
            "description can be used instead."
        ),
        a_nexus_field=NeXusField(
            name="surface_reconstruction",
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
