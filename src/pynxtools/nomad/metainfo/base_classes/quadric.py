# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXquadric (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXquadric` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import ArchiveSection
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


class Quadric(Object, ArchiveSection):
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
