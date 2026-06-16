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
# Run `pynx nomad generate-metainfo --nxdl NXquadric` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Quadric"]


class Quadric(Object):
    """
    Definition of a quadric surface.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXquadric.html#nxquadric"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXquadric",
            category="base",
        ),
    )

    parameters_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXquadric.html#nxquadric-parameters-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        shape=[10],
        description=(
            "Ten real values of the matrix that defines the quadric surface in "
            "projective space. Ordered Q11, Q12, Q13, Q22, Q23, Q33, P1, P2, P3, "
            "R. Takes a units attribute of dimension reciprocal length. R is "
            "scalar. P has dimension reciprocal length, and the given units. Q "
            "has dimension reciprocal length squared, and units the square of "
            "those given."
        ),
        a_nexus_field=NeXusField(
            name="parameters",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    surface_type = Quantity(
        type=MEnum(
            [
                "ELLIPSOID",
                "ELLIPTIC_PARABOLOID",
                "HYPERBOLIC_PARABOLOID",
                "ELLIPTIC_HYPERBOLOID_OF_1_SHEET",
                "ELLIPTIC_HYPERBOLOID_OF_2_SHEETS",
                "ELLIPTIC_CONE",
                "ELLIPTIC_CYLINDER",
                "HYPERBOLIC_CYLINDER",
                "PARABOLIC_CYLINDER",
                "SPHEROID",
                "SPHERE",
                "PARABOLOID",
                "HYPERBOLOID_1_SHEET",
                "HYPERBOLOID_2_SHEET",
                "CONE",
                "CYLINDER",
                "PLANE",
                "IMAGINARY",
                "UNKNOWN",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXquadric.html#nxquadric-surface-type-field"
        ],
        description=("An optional description of the form of the quadric surface:"),
        a_nexus_field=NeXusField(
            name="surface_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "ELLIPSOID",
                "ELLIPTIC_PARABOLOID",
                "HYPERBOLIC_PARABOLOID",
                "ELLIPTIC_HYPERBOLOID_OF_1_SHEET",
                "ELLIPTIC_HYPERBOLOID_OF_2_SHEETS",
                "ELLIPTIC_CONE",
                "ELLIPTIC_CYLINDER",
                "HYPERBOLIC_CYLINDER",
                "PARABOLIC_CYLINDER",
                "SPHEROID",
                "SPHERE",
                "PARABOLOID",
                "HYPERBOLOID_1_SHEET",
                "HYPERBOLOID_2_SHEET",
                "CONE",
                "CYLINDER",
                "PLANE",
                "IMAGINARY",
                "UNKNOWN",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXquadric.html#nxquadric-depends-on-field"
        ],
        description=(
            "Path to an :ref:`NXtransformations` that defining the axis on which "
            "the orientation of the surface depends."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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
