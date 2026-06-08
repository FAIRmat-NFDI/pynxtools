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
# Run `pynx nomad generate-metainfo --nxdl NXpositioner` to regenerate.
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

__all__ = ["Positioner"]


class Positioner(Component):
    """
    A generic positioner such as a motor or piezo-electric transducer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXpositioner",
            category="base",
        ),
    )

    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        description=(
            "The actuator of the positioner which is responsible for the "
            "movement of the probe."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuator",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-name-field"
        ],
        description=("symbolic or mnemonic name (one word)"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-description-field"
        ],
        description=("description of positioner"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-value-field"
        ],
        shape=["*"],
        description=("best known value of positioner - need [n] as may be scanned"),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    raw_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-raw-value-field"
        ],
        shape=["*"],
        description=("raw value of positioner - need [n] as may be scanned"),
        a_nexus_field=NeXusField(
            name="raw_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    target_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-target-value-field"
        ],
        shape=["*"],
        description=(
            "targeted (commanded) value of positioner - need [n] as may be scanned"
        ),
        a_nexus_field=NeXusField(
            name="target_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    tolerance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-tolerance-field"
        ],
        shape=["*"],
        description=("maximum allowable difference between target_value and value"),
        a_nexus_field=NeXusField(
            name="tolerance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    soft_limit_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-soft-limit-min-field"
        ],
        description=("minimum allowed limit to set value"),
        a_nexus_field=NeXusField(
            name="soft_limit_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    soft_limit_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-soft-limit-max-field"
        ],
        description=("maximum allowed limit to set value"),
        a_nexus_field=NeXusField(
            name="soft_limit_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    velocity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-velocity-field"
        ],
        description=("velocity of the positioner (distance moved per unit time)"),
        a_nexus_field=NeXusField(
            name="velocity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    acceleration_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-acceleration-time-field"
        ],
        description=("time to ramp the velocity up to full speed"),
        a_nexus_field=NeXusField(
            name="acceleration_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    controller_record = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-controller-record-field"
        ],
        description=(
            "Hardware device record, e.g. EPICS process variable, taco/tango ..."
        ),
        a_nexus_field=NeXusField(
            name="controller_record",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpositioner.html#nxpositioner-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a positioner."
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
