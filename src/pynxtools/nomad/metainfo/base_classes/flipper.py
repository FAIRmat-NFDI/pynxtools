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
# Run `pynx nomad generate-metainfo --nxdl NXflipper` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import MEnum, Quantity, Section

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField
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
    )
    flip_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-flip-turns-field"
        ],
        dimensionality="1 / [length]",
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
    )
    comp_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-comp-turns-field"
        ],
        dimensionality="1 / [length]",
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
    )
    guide_turns = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-guide-turns-field"
        ],
        dimensionality="1 / [length]",
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
    )
    flip_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-flip-current-field"
        ],
        dimensionality="[current]",
        description=('Flipping field coil current in "on" state"'),
        a_nexus_field=NeXusField(
            name="flip_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    comp_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-comp-current-field"
        ],
        dimensionality="[current]",
        description=('Compensating field coil current in "on" state"'),
        a_nexus_field=NeXusField(
            name="comp_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    guide_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-guide-current-field"
        ],
        dimensionality="[current]",
        description=('Guide field coil current in "on" state'),
        a_nexus_field=NeXusField(
            name="guide_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXflipper.html#nxflipper-thickness-field"
        ],
        dimensionality="[length]",
        description=("thickness along path of neutron travel"),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
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
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
