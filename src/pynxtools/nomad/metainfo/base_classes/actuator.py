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
# Run `pynx nomad generate-metainfo --nxdl NXactuator` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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

__all__ = ["Actuator"]


class Actuator(Component):
    """
    An actuator used to control an external condition.

    The condition itself is described in :ref:`NXenvironment`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXactuator",
            category="base",
        ),
    )

    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pid_controller.PidController",
        repeats=True,
        variable=True,
        description=(
            "If the actuator is PID-controlled, the settings of the PID "
            "controller can be stored here."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-name-field"
        ],
        description=("Name of the actuator"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-short-name-field"
        ],
        description=("Short name of actuator used e.g. on monitor display program"),
        a_nexus_field=NeXusField(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    actuation_target = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-actuation-target-field"
        ],
        description=(
            "The physical component on which this actuator acts. This should be "
            "a path in the NeXus tree structure. For example, this could be an "
            "instance of NXsample or a device on NXinstrument."
        ),
        a_nexus_field=NeXusField(
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    physical_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-physical-quantity-field"
        ],
        description=(
            "Name for the physical quantity effected by the actuation Examples: "
            "temperature | pH | magnetic_field | electric_field | current | "
            "conductivity | resistance | voltage | pressure | flow | stress | "
            "strain | shear | surface_pressure"
        ),
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-type-field"
        ],
        description=(
            "The type of hardware used for the actuation. Examples (suggestions, "
            "but not restrictions): :Temperature: laser | gas lamp | filament | "
            "resistive :Pressure: anvil cell :Voltage: potentiostat"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    outputVALUE = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactuator.html#nxactuator-outputvalue-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "Any output that the actuator produces. For example, a heater can "
            "have the field output_power(NX_NUMBER)."
        ),
        a_nexus_field=NeXusField(
            name="outputVALUE",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
