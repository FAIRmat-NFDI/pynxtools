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
# Run `pynx nomad generate-metainfo --nx-class NXnote` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Note"]


class Note(Object):
    """
    Any additional freeform information not covered by the other base classes.

    This class can be used to store additional information in a NeXus file e.g.
    pictures, movies, audio, additional text logs
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXnote",
            category="base",
        ),
    )

    author = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-author-field"
        ],
        description=("Author or creator of note"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="author",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-date-field"
        ],
        description=("Date note created/added"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-type-field"
        ],
        description=(
            "Mime content type of note data field e.g. image/jpeg, text/plain, "
            "text/html"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-file-name-field"
        ],
        description=(
            "Name of original file name if note was read from an external source"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-identifiername-field"
        ],
        variable=True,
        description=(
            "Identifier of the resource if that resource that has been "
            "serialized. For example, the identifier to a resource in another "
            "database."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-checksum-field"
        ],
        description=(
            "Value of the hash that is obtained when running algorithm on the "
            "content of the resource referred to by ``identifierNAME``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-algorithm-field"
        ],
        description=(
            "Name of the algorithm whereby the ``checksum`` was computed. "
            "Examples: md5, sha256"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-description-field"
        ],
        description=("Title of an image or other details of the note"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-sequence-index-field"
        ],
        description=(
            "Sequence index of note, for placing a sequence of multiple "
            "**NXnote** groups in an order. Starts with 1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    data_quantity = Quantity(
        type=Bytes,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXnote.html#nxnote-data-field"
        ],
        description=("Binary note data - if text, line terminator is [CR][LF]."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="data",
            type="NX_BINARY",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
