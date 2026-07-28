# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXpump (see
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
# Run `pynx nomad generate-metainfo --nxdl NXpump` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Pump"]


class Pump(Component):
    """
    Device to reduce an atmosphere to a controlled pressure.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpump.html#nxpump"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXpump",
            category="base",
        ),
    )

    design = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpump.html#nxpump-design-field"
        ],
        description=("Principle type of the pump."),
        a_nexus_field=NeXusField(
            name="design",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "membrane",
                "rotary_vane",
                "roots",
                "turbo_molecular",
                "ion",
                "cryo",
                "diffusion",
                "scroll",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    base_pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpump.html#nxpump-base-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        description=(
            "The minimum pressure achievable in a chamber after it has been "
            "pumped down for an extended period."
        ),
        a_nexus_field=NeXusField(
            name="base_pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "pascal"},
    )
    medium = Quantity(
        type=MEnum(["vacuum", "liquid", "gas", "slurry", "powder"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpump.html#nxpump-medium-field"
        ],
        description=(
            "The material being moved by the pump. Pumps intending to create a "
            'vacuum should state "vacuum" as the medium, while pumps having '
            "the primary purpose of creating a flow or pressure of gas should "
            'state "gas" as the medium.'
        ),
        a_nexus_field=NeXusField(
            name="medium",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["vacuum", "liquid", "gas", "slurry", "powder"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
