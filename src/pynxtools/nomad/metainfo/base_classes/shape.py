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
# Run `pynx nomad generate-metainfo --nxdl NXshape` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Shape"]


class Shape(Object):
    """
    legacy class - (used by :ref:`NXgeometry`) - the shape and size of a
    component.

    This is the description of the general shape and size of a component, which
    may be made up of ``numobj`` separate elements - it is used by the
    :ref:`NXgeometry` class
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXshape.html#nxshape"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXshape",
            category="base",
        ),
    )

    shape = Quantity(
        type=MEnum(
            [
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXshape.html#nxshape-shape-field"
        ],
        description=("general shape of a component"),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXshape.html#nxshape-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "physical extent of the object along its local axes (after "
            "NXorientation) with the center of mass at the local origin (after "
            "NXtranslation). The meaning and location of these axes will vary "
            'according to the value of the "shape" variable. ``nshapepar`` '
            'defines how many parameters: - For "nxcylinder" type the '
            "parameters are (diameter,height) and a three value orientation "
            'vector of the cylinder. - For the "nxbox" type the parameters are '
            '(length,width,height). - For the "nxsphere" type the parameters '
            "are (diameter). - For nxcone cone half aperture - For nxelliptical, "
            "semi-major axis, semi-minor-axis, angle of major axis and pole - "
            "For nxtoroidal, major radius, minor radius - For nxparabolic, "
            "parabolic parameter a - For nxpolynomial, an array of polynom "
            "coefficients, the dimension of the array encodes the degree of the "
            "polynom"
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    direction = Quantity(
        type=MEnum(["concave", "convex"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXshape.html#nxshape-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["concave", "convex"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
