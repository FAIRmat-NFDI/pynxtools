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
# Run `pynx nomad generate-metainfo --nxdl NXcs_processor` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.circuit import Circuit
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CsProcessor"]


class CsProcessor(Component):
    """
    Base class for reporting the description of processing units of a computer.

    Examples are e.g. classical so-called central processing units (CPUs),
    coprocessors, graphic cards, accelerator processing units or a system of
    these.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_processor.html#nxcs_processor"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_processor",
            category="base",
        ),
    )

    circuit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_processor.CsProcessorCircuit",
        repeats=True,
        variable=True,
        description=(
            "Typical examples for the granularization of processing units are: * "
            "A desktop computer with a single CPU; describe using one instance "
            "of NXcircuit. * A dual-socket server; describe using two instances "
            "of NXcircuit. * A server with two dual-socket server nodes; "
            "describe with four instances of NXcircuit surplus a field that "
            "defines their level in the hierarchy."
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class CsProcessorCircuit(Circuit):
    """
    Typical examples for the granularization of processing units are:

    * A desktop computer with a single CPU; describe using one instance of
    NXcircuit. * A dual-socket server; describe using two instances of
    NXcircuit. * A server with two dual-socket server nodes; describe with four
    instances of NXcircuit surplus a field that defines their level in the
    hierarchy.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_processor.html#nxcs_processor-circuit-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcircuit",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_processor.html#nxcs_processor-circuit-type-field"
        ],
        description=(
            "General type of the processing unit e.g. * pu, processing core or "
            "hyper-threading core * cpu, (multi-)core central processing unit * "
            "gpu, (multi-)core general purpose processing unit * fpga, field "
            "programmable gate array"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["pu", "cpu", "gpu", "fpga"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    clock_speed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_processor.html#nxcs_processor-circuit-clock-speed-field"
        ],
        description=("Clock speed of the circuit"),
        a_nexus_field=NeXusField(
            name="clock_speed",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
