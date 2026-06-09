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
# Run `pynx nomad generate-metainfo --nxdl NXapm_event_data` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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

__all__ = ["ApmEventData"]


class ApmEventData(Object):
    """
    Base class to store state and (meta)data of events over the course of an
    atom probe experiment.

    Having at least one instance for an instance of NXapm is recommended.

    This base class applies the concept of the :ref:`NXem_event_data` base
    class to the specific needs of atom probe research. Again static and
    dynamic quantities are split to avoid a duplication of information.
    Specifically, the time interval considered is the entire time starting at
    start_time until end_time during which we assume the pulser triggered
    pulses. These pulses are identified via the pulse_id field. The point in
    time when each pulse was fired can be recovered from analyzing start_time
    and delta_time.

    Which temporal granularity is adequate depends on the situation and
    research question. Using a model which enables a collection of events
    offers the most flexible way to cater for both atom probe experiments or
    simulation. To monitor the course of an ion extraction experiment (or
    simulation) it makes sense to track time explicitly via time stamps or
    implicitly via e.g. a clock inside the instrument, such as the clock of the
    pulser and respective pulse_id.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_event_data",
            category="base",
            symbols={
                "p": "Number of pulses collected in between start_time and end_time."
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrument",
        repeats=False,
        description=(
            "Place to store dynamic metadata of the instrument to document as "
            "close as possible the state of the instrument during the event, "
            "i.e. in between start_time and end_time."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name="instrument",
            name_type="specified",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the snapshot time interval started. If users wish to "
            "specify an interval of time that the snapshot should represent "
            "during which the instrument was stable and configured using "
            "specific settings and calibrations, the start_time is the start, "
            "the left bound of the time interval, while the end_time specifies "
            "the end, the right bound of the time interval."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the snapshot time interval ended."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    delta_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data-delta-time-field"
        ],
        dimensionality="[time]",
        shape=["*"],
        description=(
            "Delta time array which resolves for each pulse_id the time "
            "difference between when that pulse was fired and start_time. In "
            "summary, using start_time, end_time, delta_time, pulse_id_offset, "
            "and pulse_id provides temporal context information when a pulse was "
            "fired relative to start_time and when it is relevant to translate "
            "this into coordinated world time UTC. Note that pulses in reality "
            "have a shape and thus additional documentation is required to "
            "assure that the entries in delta_time are always taken at at points "
            "in time that, relative to the triggering of the pulse, represent an "
            "as close as possible state of the pulse."
        ),
        a_nexus_field=NeXusField(
            name="delta_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    pulse_id_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data-pulse-id-offset-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Integer which defines the first pulse_id. Typically, this is either "
            "zero or one."
        ),
        a_nexus_field=NeXusField(
            name="pulse_id_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    pulse_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_event_data.html#nxapm_event_data-pulse-id-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "An integer to identify a specific pulse in a sequence. There are "
            "two possibilities to report pulse_id values: If pulse_id_offset is "
            "provided, the pulse_id values are defined by the sequence "
            ":math:`[pulse\\_id\\_offset, pulse\\_id\\_offset + p]` with "
            ":math:`p` the number of pulses collected in between start_time and "
            "end_time. Alternatively, pulse_id_offset is not provided but "
            "instead a sequence of :math:`p` values is defined. These integer "
            "values do not need to be sorted."
        ),
        a_nexus_field=NeXusField(
            name="pulse_id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
