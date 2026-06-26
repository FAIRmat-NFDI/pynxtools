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
# Run `pynx nomad generate-metainfo --nxdl NXactivity` to regenerate.
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

__all__ = ["Activity"]


class Activity(Object):
    """
    A planned or unplanned action that has a temporal extension and for some
    time depends on some entity.

    This class is a super class for all other activities.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactivity.html#nxactivity"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXactivity",
            category="base",
        ),
    )

    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "This can be any data or other descriptor acquired during the "
            "activity (NXnote allows to add pictures, audio, movies). "
            "Alternatively, a reference to the location or a unique identifier "
            "or other metadata file. In the case these are not available, "
            "free-text description. Any number of instances of :ref:`NXnote` are "
            "allowed for describing extra details of this activity."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactivity.html#nxactivity-start-time-field"
        ],
        description=(
            "Start time of this activity. It is recommended to include local "
            "time zone information."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactivity.html#nxactivity-end-time-field"
        ],
        description=(
            "End time of this activity. It is recommended to include local time "
            "zone information."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time__estimated = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactivity.html#nxactivity-end-time-estimated-attribute"
        ],
        description=(
            "In some cases, the end time of an activity can only be estimated. "
            "In this case, this attribute shall be True."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="estimated",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            parent_field="end_time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXactivity.html#nxactivity-description-field"
        ],
        description=("Short description of the activity."),
        a_nexus_field=NeXusField(
            name="description",
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
