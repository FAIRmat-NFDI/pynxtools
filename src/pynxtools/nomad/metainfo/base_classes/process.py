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
# Run `pynx nomad generate-metainfo --nx-class NXprocess` to regenerate.
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

__all__ = ["Process"]


class Process(Object, basesections.ActivityStep):
    """
    The :ref:`NXprocess` class describes an operation used to process data as
    part of an analysis workflow, providing information such as the software
    used, the date of the operation, the input parameters, and the resulting
    data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXprocess.html#nxprocess"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXprocess",
            category="base",
        ),
    )

    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "The note will contain information about how the data was processed "
            "or anything about the data provenance. The contents of the note can "
            "be anything that the processing code can understand, or simple "
            "text. The name will be numbered to allow for ordering of steps."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=True,
        variable=True,
        description=("Parameters used in performing the data analysis."),
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=("The data resulting from the operation."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXprocess.html#nxprocess-program-field"
        ],
        description=("Name of the program used"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXprocess.html#nxprocess-sequence-index-field"
        ],
        description=(
            "Sequence index of processing, for determining the order of multiple "
            "**NXprocess** steps. Starts with 1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXprocess.html#nxprocess-version-field"
        ],
        description=("Version of the program used"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXprocess.html#nxprocess-date-field"
        ],
        description=("Date and time of processing."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
