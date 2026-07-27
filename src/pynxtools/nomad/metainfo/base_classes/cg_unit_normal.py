# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_unit_normal (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_unit_normal` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgUnitNormal"]


class CgUnitNormal(Object):
    """
    Computational geometry description of a set of (oriented) unit normal
    vectors.

    Store normal vector information as properties of primitives. Use only only
    as a child of an instance of :ref:`NXcg_primitive` so that this instance
    acts as the parent to define a context.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_unit_normal",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 2.",
                "c": "The cardinality of the set, i.e. the number of unit normals.",
            },
        ),
    )

    normals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal-normals-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Direction of each normal - a unit normal."),
        a_nexus_field=NeXusField(
            name="normals",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "An indicator which details the orientation of each normal vector in "
            "relation to its primitive, assuming the object is viewed from a "
            "position outside the object. * 0 - undefined * 1 - outer unit "
            "normal vector * 2 - inner unit normal vector"
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
