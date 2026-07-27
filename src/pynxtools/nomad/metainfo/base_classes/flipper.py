# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXflipper (see
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
# Run `pynx nomad generate-metainfo --nxdl NXflipper` to regenerate.
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

__all__ = ["Flipper"]


class Flipper(Component):
    """
    A spin flipper.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXflipper",
            category="base",
        ),
    )

    type = Quantity(
        type=MEnum(["coil", "current-sheet"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["coil", "current-sheet"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    flip_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-flip-turns-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Linear density of turns (such as number of turns/cm) in flipping "
            "field coils"
        ),
        a_nexus_field=NeXusField(
            name="flip_turns",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    comp_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-comp-turns-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Linear density of turns (such as number of turns/cm) in "
            "compensating field coils"
        ),
        a_nexus_field=NeXusField(
            name="comp_turns",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    guide_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-guide-turns-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Linear density of turns (such as number of turns/cm) in guide field coils"
        ),
        a_nexus_field=NeXusField(
            name="guide_turns",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    flip_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-flip-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=('Flipping field coil current in "on" state"'),
        a_nexus_field=NeXusField(
            name="flip_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    comp_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-comp-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=('Compensating field coil current in "on" state"'),
        a_nexus_field=NeXusField(
            name="comp_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    guide_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-guide-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=('Guide field coil current in "on" state'),
        a_nexus_field=NeXusField(
            name="guide_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("thickness along path of neutron travel"),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a spin flipper."
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
