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
# Run `pynx nomad generate-metainfo --nxdl NXunit_cell` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["UnitCell"]


class UnitCell(Object):
    """
    Base class to describe structural aspects of an arrangement of atoms or
    ions including a crystallographic unit cell.

    Following recommendations of `CIF
    <https://www.iucr.org/resources/cif/spec/version1.1>`_ and `International
    Tables of Crystallography <https://it.iucr.org/>`_.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXunit_cell",
            category="base",
            symbols={"d": "Dimensionality of the lattice."},
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.atom.Atom",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    reference_frame = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-reference-frame-field"
        ],
        description=(
            "Path to a reference frame in which the unit cell is defined to "
            "resolve ambiguity in cases when e.g. a different reference frame "
            "than the NeXus default reference frame (McStas) was chosen."
        ),
        a_nexus_field=NeXusField(
            name="reference_frame",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-dimensionality-field"
        ],
        description=("Dimensionality of the structure."),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    a_b_c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-a-b-c-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Geometry of the unit cell quantified via parameters a, b, and c."
        ),
        a_nexus_field=NeXusField(
            name="a_b_c",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-a-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Geometry of the unit cell quantified individually via parameter a."
        ),
        a_nexus_field=NeXusField(
            name="a",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-b-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Geometry of the unit cell quantified individually via parameter b."
        ),
        a_nexus_field=NeXusField(
            name="b",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-c-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Geometry of the unit cell quantified individually via parameter c."
        ),
        a_nexus_field=NeXusField(
            name="c",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    alpha_beta_gamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-alpha-beta-gamma-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Geometry of the unit cell quantified via parameters alpha, beta, "
            "and gamma."
        ),
        a_nexus_field=NeXusField(
            name="alpha_beta_gamma",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-alpha-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Geometry of the unit cell quantified individually via parameter alpha."
        ),
        a_nexus_field=NeXusField(
            name="alpha",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    beta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-beta-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Geometry of the unit cell quantified individually via parameter beta."
        ),
        a_nexus_field=NeXusField(
            name="beta",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    gamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-gamma-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Geometry of the unit cell quantified individually via parameter gamma."
        ),
        a_nexus_field=NeXusField(
            name="gamma",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    crystal_system = Quantity(
        type=MEnum(
            [
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "rhombohedral",
                "hexagonal",
                "cubic",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-crystal-system-field"
        ],
        description=(
            "Crystal system. For a crystal system in 2D space monoclinic is an "
            "exact synonym for oblique. For a crystal system in 2D space "
            "orthorhombic is an exact synonym for rectangular. For a crystal "
            "system in 2D space tetragonal is an exact synonym for square."
        ),
        a_nexus_field=NeXusField(
            name="crystal_system",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "rhombohedral",
                "hexagonal",
                "cubic",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    laue_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-laue-group-field"
        ],
        description=(
            "Laue group using International Table of Crystallography notation."
        ),
        a_nexus_field=NeXusField(
            name="laue_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-point-group-field"
        ],
        description=(
            "Point group using International Table of Crystallography notation."
        ),
        a_nexus_field=NeXusField(
            name="point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-space-group-field"
        ],
        description=(
            "Space group from the International Table of Crystallography notation."
        ),
        a_nexus_field=NeXusField(
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    is_centrosymmetric = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-is-centrosymmetric-field"
        ],
        description=(
            "True if space group is considered a centrosymmetric one. False if "
            "space group is considered a non-centrosymmetric one. "
            "Centrosymmetric has all types and combinations of symmetry elements "
            "(translation, rotational axis, mirror planes, center of inversion) "
            "Non-centrosymmetric compared to centrosymmetric is constrained (no "
            "inversion). Chiral compared to non-centrosymmetric is constrained "
            "(no mirror planes)."
        ),
        a_nexus_field=NeXusField(
            name="is_centrosymmetric",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    is_chiral = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-is-chiral-field"
        ],
        description=(
            "True if space group is considered a chiral one. False if space "
            "group is consider a non-chiral one."
        ),
        a_nexus_field=NeXusField(
            name="is_chiral",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        description=("Area of the unit cell if dimensionality is 2."),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m ** 2"},
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXunit_cell.html#nxunit_cell-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        description=("Volume of the unit cell if dimensionality is 3."),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m ** 3"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
