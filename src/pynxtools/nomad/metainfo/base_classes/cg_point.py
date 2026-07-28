# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_point (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcg_point` to regenerate.
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

__all__ = ["CgPoint"]


class CgPoint(CgPrimitive):
    """
    Computational geometry description of a set of points.

    Points may have an associated time value. Users are advised though to store
    time data of point sets rather as instances of time events, where for each
    point in time there is an :ref:`NXcg_point` instance which specifies the
    points' locations.

    This is a frequent situation in experiments and computer simulations, where
    positions of points are taken at the same point in time (real time or
    simulated physical time). Thereby, the storage of redundant timestamp
    information per point is considered as obsolete.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_point.html#nxcg_point"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_point",
            category="base",
            symbols={
                "d": "The dimensionality.",
                "c": "The cardinality of the set, i.e. the number of points.",
            },
        ),
    )

    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_point.html#nxcg_point-position-field"
        ],
        flexible_unit=True,
        shape=["*", "*"],
        description=("Coordinates of the points."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_point.html#nxcg_point-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "(Elapsed) time for each point. If the field time is needed "
            "contextualize the time_offset relative to which time values are "
            "defined. Alternative store timestamp."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    timestamp = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_point.html#nxcg_point-timestamp-field"
        ],
        shape=["*"],
        description=("ISO8601 with local time zone offset for each point."),
        a_nexus_field=NeXusField(
            name="timestamp",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    time_offset = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_point.html#nxcg_point-time-offset-field"
        ],
        description=(
            "ISO8601 with local time zone offset that serves as the reference "
            "for values in the field time."
        ),
        a_nexus_field=NeXusField(
            name="time_offset",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
