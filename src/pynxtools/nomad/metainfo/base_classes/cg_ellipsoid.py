# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_ellipsoid (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_ellipsoid` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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

__all__ = ["CgEllipsoid"]


class CgEllipsoid(CgPrimitive):
    """
    Computational geometry description of a set of ellipsoids.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_ellipsoid",
            category="base",
            symbols={
                "d": "The dimensionality of the space in which the members are assumed embedded.",
                "c": "The cardinality of the set, i.e. the number of members.",
            },
        ),
    )

    semi_axes_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-semi-axes-value-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Length of the semi-axes (e.g. semi-major and semi-minor "
            "respectively for an ellipse). Use if all ellipsoids in the set have "
            "the same half-axes."
        ),
        a_nexus_field=NeXusField(
            name="semi_axes_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    semi_axes_values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-semi-axes-values-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Length of the semi-axes if ellipsoids have individually different lengths."
        ),
        a_nexus_field=NeXusField(
            name="semi_axes_values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("In the case that all ellipsoids are spheres."),
        a_nexus_field=NeXusField(
            name="radius",
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
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "In the case that all ellipsoids are spheres whose radii differ. For "
            "a mixture of spheres use semi_axes_values."
        ),
        a_nexus_field=NeXusField(
            name="radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
