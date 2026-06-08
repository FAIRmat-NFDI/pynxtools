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
# Run `pynx nomad generate-metainfo --nx-class NXcrystal` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Crystal"]


class Crystal(Component):
    """
    A crystal monochromator or analyzer.

    Permits double bent monochromator comprised of multiple segments with
    anisotropic Gaussian mosaic.

    If curvatures are set to zero or are absent, array is considered to be
    flat.

    Scattering vector is perpendicular to surface. Crystal is oriented parallel
    to beam incident on crystal before rotation, and lies in vertical plane.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcrystal",
            category="base",
            symbols={
                "n_comp": "number of different unit cells to be described",
                "i": "number of wavelengths",
            },
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("Position of crystal"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the crystal and NXoff_geometry to describe its shape instead",
        ),
    )
    temperature_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("log file of crystal temperature"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="temperature_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    reflectivity = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("crystal reflectivity versus wavelength"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectivity",
            name_type="specified",
            optionality="optional",
        ),
    )
    transmission = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("crystal transmission versus wavelength"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission",
            name_type="specified",
            optionality="optional",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.shape.Shape",
        repeats=False,
        description=("A NXshape group describing the shape of the crystal arrangement"),
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="optional",
            deprecated="Use NXoff_geometry instead to describe the shape of the monochromator",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    usage = Quantity(
        type=MEnum(["Bragg", "Laue"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-usage-field"
        ],
        description=("How this crystal is used. Choices are in the list."),
        a_nexus_field=NeXusField(
            name="usage",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Bragg", "Laue"],
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-type-field"
        ],
        description=(
            "Type or material of monochromating substance. Chemical formula can "
            'be specified separately. Use the "reflection" field to indicate '
            'the (hkl) orientation. Use the "d_spacing" field to record the '
            "lattice plane spacing. This field was changed (2010-11-17) from an "
            "enumeration to a string since common usage showed a wider variety "
            "of use than a simple list. These are the items in the list at the "
            "time of the change: PG (Highly Oriented Pyrolytic Graphite) | Ge | "
            "Si | Cu | Fe3Si | CoFe | Cu2MnAl (Heusler) | Multilayer | Diamond."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-chemical-formula-field"
        ],
        description=(
            "The chemical formula specified using CIF conventions. Abbreviated "
            "version of CIF standard: * Only recognized element symbols may be "
            "used. * Each element symbol is followed by a 'count' number. A "
            "count of '1' may be omitted. * A space or parenthesis must separate "
            "each cluster of (element symbol + count). * Where a group of "
            "elements is enclosed in parentheses, the multiplier for the group "
            "must follow the closing parentheses. That is, all element and group "
            "multipliers are assumed to be printed as subscripted numbers. * "
            "Unless the elements are ordered in a manner that corresponds to "
            "their chemical structure, the order of the elements within any "
            "group or moiety depends on whether or not carbon is present. * If "
            "carbon is present, the order should be: C, then H, then the other "
            "elements in alphabetical order of their symbol. If carbon is not "
            "present, the elements are listed purely in alphabetic order of "
            "their symbol. * This is the *Hill* system used by Chemical "
            "Abstracts."
        ),
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    order_no = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-order-no-field"
        ],
        description=(
            "A number which describes if this is the first, second,.. "
            ":math:`n^{th}` crystal in a multi crystal monochromator"
        ),
        a_nexus_field=NeXusField(
            name="order_no",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    cut_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-cut-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "Cut angle of reflecting Bragg plane and plane of crystal surface"
        ),
        a_nexus_field=NeXusField(
            name="cut_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-space-group-field"
        ],
        description=("Space group of crystal structure"),
        a_nexus_field=NeXusField(
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    unit_cell = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-field"
        ],
        dimensionality="[length]",
        shape=["*", 6],
        description=("Unit cell parameters (lengths and angles)"),
        a_nexus_field=NeXusField(
            name="unit_cell",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-a-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side a"),
        a_nexus_field=NeXusField(
            name="unit_cell_a",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-b-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side b"),
        a_nexus_field=NeXusField(
            name="unit_cell_b",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-c-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side c"),
        a_nexus_field=NeXusField(
            name="unit_cell_c",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-alpha-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle alpha"),
        a_nexus_field=NeXusField(
            name="unit_cell_alpha",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_beta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-beta-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle beta"),
        a_nexus_field=NeXusField(
            name="unit_cell_beta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_gamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-gamma-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle gamma"),
        a_nexus_field=NeXusField(
            name="unit_cell_gamma",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-unit-cell-volume-field"
        ],
        dimensionality="[length] ** 3",
        description=("Volume of the unit cell"),
        a_nexus_field=NeXusField(
            name="unit_cell_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    orientation_matrix = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-orientation-matrix-field"
        ],
        shape=[3, 3],
        description=(
            "Orientation matrix of single crystal sample using Busing-Levy "
            "convention: W. R. Busing and H. A. Levy (1967). Acta Cryst. 22, "
            "457-464"
        ),
        a_nexus_field=NeXusField(
            name="orientation_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-wavelength-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Optimum diffracted wavelength"),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    d_spacing = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-d-spacing-field"
        ],
        dimensionality="[length]",
        description=("spacing between crystal planes of the reflection"),
        a_nexus_field=NeXusField(
            name="d_spacing",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    scattering_vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-scattering-vector-field"
        ],
        dimensionality="1 / [length]",
        description=("Scattering vector, Q, of nominal reflection"),
        a_nexus_field=NeXusField(
            name="scattering_vector",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    reflection = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-reflection-field"
        ],
        dimensionality="dimensionless",
        shape=[3],
        description=("Miller indices (hkl) values of nominal reflection"),
        a_nexus_field=NeXusField(
            name="reflection",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-thickness-field"
        ],
        dimensionality="[length]",
        description=(
            "Thickness of the crystal. (Required for Laue orientations - see "
            '"usage" field)'
        ),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        description=("mass density of the crystal"),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    segment_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-width-field"
        ],
        dimensionality="[length]",
        description=("Horizontal width of individual segment"),
        a_nexus_field=NeXusField(
            name="segment_width",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    segment_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-height-field"
        ],
        dimensionality="[length]",
        description=("Vertical height of individual segment"),
        a_nexus_field=NeXusField(
            name="segment_height",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    segment_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of individual segment"),
        a_nexus_field=NeXusField(
            name="segment_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    segment_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-gap-field"
        ],
        dimensionality="[length]",
        description=("Typical gap between adjacent segments"),
        a_nexus_field=NeXusField(
            name="segment_gap",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    segment_columns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-columns-field"
        ],
        dimensionality="[length]",
        description=("number of segment columns in horizontal direction"),
        a_nexus_field=NeXusField(
            name="segment_columns",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    segment_rows = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-segment-rows-field"
        ],
        dimensionality="[length]",
        description=("number of segment rows in vertical direction"),
        a_nexus_field=NeXusField(
            name="segment_rows",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    mosaic_horizontal = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-mosaic-horizontal-field"
        ],
        dimensionality="[angle]",
        description=("horizontal mosaic Full Width Half Maximum"),
        a_nexus_field=NeXusField(
            name="mosaic_horizontal",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    mosaic_vertical = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-mosaic-vertical-field"
        ],
        dimensionality="[angle]",
        description=("vertical mosaic Full Width Half Maximum"),
        a_nexus_field=NeXusField(
            name="mosaic_vertical",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    curvature_horizontal = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-curvature-horizontal-field"
        ],
        dimensionality="[angle]",
        description=("Horizontal curvature of focusing crystal"),
        a_nexus_field=NeXusField(
            name="curvature_horizontal",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    curvature_vertical = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-curvature-vertical-field"
        ],
        dimensionality="[angle]",
        description=("Vertical curvature of focusing crystal"),
        a_nexus_field=NeXusField(
            name="curvature_vertical",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    is_cylindrical = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-is-cylindrical-field"
        ],
        description=("Is this crystal bent cylindrically?"),
        a_nexus_field=NeXusField(
            name="is_cylindrical",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    cylindrical_orientation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-cylindrical-orientation-angle-field"
        ],
        dimensionality="[angle]",
        description=("If cylindrical: cylinder orientation angle"),
        a_nexus_field=NeXusField(
            name="cylindrical_orientation_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-polar-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=(
            "Polar (scattering) angle at which crystal assembly is positioned. "
            "Note: some instrument geometries call this term 2theta. Note: it is "
            "recommended to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=(
            "Azimuthal angle at which crystal assembly is positioned. Note: it "
            "is recommended to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    bragg_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-bragg-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=("Bragg angle of nominal reflection"),
        a_nexus_field=NeXusField(
            name="bragg_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-temperature-field"
        ],
        dimensionality="[temperature]",
        description=("average/nominal crystal temperature"),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    temperature_coefficient = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-temperature-coefficient-field"
        ],
        description=("how lattice parameter changes with temperature"),
        a_nexus_field=NeXusField(
            name="temperature_coefficient",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcrystal.html#nxcrystal-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a crystal."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
