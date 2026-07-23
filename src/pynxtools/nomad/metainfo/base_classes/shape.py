# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXshape (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXshape` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
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

__all__ = ["Shape"]


class Shape(Object, ArchiveSection):
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
