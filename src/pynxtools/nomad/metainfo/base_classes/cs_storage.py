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
# Run `pynx nomad generate-metainfo --nx-class NXcs_storage` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.circuit import Circuit
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CsStorage"]


class CsStorage(Component):
    """
    Base class for reporting the description of the I/O of a computer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_storage",
            category="base",
        ),
    )

    circuit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_storage.CsStorageCircuit",
        repeats=True,
        variable=True,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class CsStorageCircuit(Circuit):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage-circuit-group"
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
        type=MEnum(["solid_state_disk", "hard_disk", "optical", "tape"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage-circuit-type-field"
        ],
        description=("Qualifier for the type of storage medium used."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["solid_state_disk", "hard_disk", "optical", "tape"],
        ),
    )
    max_physical_capacity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage-circuit-max-physical-capacity-field"
        ],
        description=("Total amount of data which the medium can hold."),
        a_nexus_field=NeXusField(
            name="max_physical_capacity",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    max_read_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage-circuit-max-read-rate-field"
        ],
        description=("Maximum read rate of the storage medium."),
        a_nexus_field=NeXusField(
            name="max_read_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    max_write_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_storage.html#nxcs_storage-circuit-max-write-rate-field"
        ],
        description=("Maximum write rate of the storage medium."),
        a_nexus_field=NeXusField(
            name="max_write_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
