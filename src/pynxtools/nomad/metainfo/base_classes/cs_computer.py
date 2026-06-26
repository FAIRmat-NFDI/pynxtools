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
# Run `pynx nomad generate-metainfo --nxdl NXcs_computer` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CsComputer"]


class CsComputer(Object):
    """
    Base class for reporting the description of a computer
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_computer.html#nxcs_computer"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_computer",
            category="base",
        ),
    )

    processorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_processor.CsProcessor",
        repeats=True,
        variable=True,
        description=("Multiple instances should be named processor1, processor2, etc."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_processor",
            name="processorID",
            name_type="partial",
            optionality="optional",
        ),
    )
    memoryID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_memory.CsMemory",
        repeats=True,
        variable=True,
        description=("Multiple instances should be named memory1, memory2, etc."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_memory",
            name="memoryID",
            name_type="partial",
            optionality="optional",
        ),
    )
    storageID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_storage.CsStorage",
        repeats=True,
        variable=True,
        description=("Multiple instances should be named storage1, storage2, etc."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_storage",
            name="storageID",
            name_type="partial",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_computer.html#nxcs_computer-name-field"
        ],
        description=("Given name/alias to the computing system, e.g. MyDesktop."),
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
    operating_system = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_computer.html#nxcs_computer-operating-system-field"
        ],
        description=(
            "Name of the operating system, e.g. Windows, Linux, Mac, Android."
        ),
        a_nexus_field=NeXusField(
            name="operating_system",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    operating_system__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_computer.html#nxcs_computer-operating-system-version-attribute"
        ],
        description=(
            "Version plus build number, commit hash, or description of an ever "
            "persistent resource where the source code of the program and build "
            "instructions can be found so that the program can be configured in "
            "such a manner that the result file is ideally recreatable yielding "
            "the same results."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="operating_system",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    uuid = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_computer.html#nxcs_computer-uuid-field"
        ],
        description=(
            "A globally unique persistent identifier of the computer, i.e. the "
            "Universally Unique Identifier (UUID) of the computing node."
        ),
        a_nexus_field=NeXusField(
            name="uuid",
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
