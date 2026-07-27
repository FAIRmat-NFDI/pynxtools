# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXisocontour (see
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
# Run `pynx nomad generate-metainfo --nxdl NXisocontour` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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

__all__ = ["Isocontour"]


class Isocontour(Object):
    """
    Base class for describing isocontouring/phase-fields in Euclidean space.

    Iso-contouring algorithms such as Marching Cubes and others are frequently
    used to segment d-dimensional regions at crossings of a threshold value,
    the so-called isovalue.

    In Computational Materials Science phase-field methods are frequently used.
    Phase-field variables are discretized frequently using regular grids.

    Isocontour algorithms are often used in such context to pinpoint the
    locations of microstructural features from this implicit phase-field-
    variable-value-based description.

    One of the key intentions of this base class is to provide a starting point
    for scientists from the phase-field community (condensed-matter physicists,
    and materials engineers) to incentivize that also phase-field (and other)
    simulation data can take advantage of NeXus base class to improve
    interoperability.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXisocontour.html#nxisocontour"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXisocontour",
            category="base",
            symbols={"d": "The dimensionality of the description."},
        ),
    )

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=False,
        description=(
            "The discretized grid on which the iso-contour algorithm operates."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXisocontour.html#nxisocontour-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The dimensionality of the space in which the isocontour is embedded."
        ),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    isovalue = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXisocontour.html#nxisocontour-isovalue-field"
        ],
        flexible_unit=True,
        description=("The threshold or iso-contour value."),
        a_nexus_field=NeXusField(
            name="isovalue",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
