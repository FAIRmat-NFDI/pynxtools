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
# Run `pynx nomad generate-metainfo --nxdl NXpump` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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
    )
    base_pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpump.html#nxpump-base-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
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
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
