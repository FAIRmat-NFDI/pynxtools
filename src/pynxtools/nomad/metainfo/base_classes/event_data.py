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
# Run `pynx nomad generate-metainfo --nx-class NXevent_data` to regenerate.
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

__all__ = ["EventData"]


class EventData(Object):
    """
    NXevent_data is a special group for storing data from neutron detectors in
    event mode. In this mode, the detector electronics emits a stream of
    detectorID, timestamp pairs. With detectorID describing the detector
    element in which the neutron was detected and timestamp the timestamp at
    which the neutron event was detected. In NeXus detectorID maps to event_id,
    event_time_offset to the timestamp.

    As this kind of data is common at pulsed neutron sources, the timestamp is
    almost always relative to the start of a neutron pulse. Thus the pulse
    timestamp is recorded too together with an index in the event_id,
    event_time_offset pair at which data for that pulse starts. At reactor
    source the same pulsed data effect may be achieved through the use of
    choppers or in stroboscopic measurement setups.

    In order to make random access to timestamped data faster there is an
    optional array pair of cue_timestamp_zero and cue_index. The
    cue_timestamp_zero will contain courser timestamps then in the time array,
    say every five minutes. The cue_index will then contain the index into the
    event_id,event_time_offset pair of arrays for that courser
    cue_timestamp_zero.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXevent_data",
            category="base",
        ),
    )

    event_time_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-event-time-offset-field"
        ],
        dimensionality="[time]",
        shape=["*"],
        description=("A list of timestamps for each event as it comes in."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="event_time_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-event-id-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "There will be extra information in the NXdetector to convert "
            "event_id to detector_number."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="event_id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    event_time_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-event-time-zero-field"
        ],
        dimensionality="[time]",
        shape=["*"],
        description=("The time that each pulse started with respect to the offset"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="event_time_zero",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    event_time_zero__offset = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-event-time-zero-offset-attribute"
        ],
        description=("ISO8601"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="offset",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="event_time_zero",
        ),
    )
    event_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-event-index-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The index into the event_time_offset, event_id pair for the pulse "
            "occurring at the matching entry in event_time_zero."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="event_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    pulse_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-pulse-height-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "If voltages from the ends of the detector are read out this is "
            "where they go. This list is for all events with information to "
            "attach to a particular pulse height. The information to attach to a "
            "particular pulse is located in events_per_pulse."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="pulse_height",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    cue_timestamp_zero = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-cue-timestamp-zero-field"
        ],
        dimensionality="[time]",
        description=(
            "Timestamps matching the corresponding cue_index into the event_id, "
            "event_time_offset pair."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="cue_timestamp_zero",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    cue_timestamp_zero__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-cue-timestamp-zero-start-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="cue_timestamp_zero",
        ),
    )
    cue_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXevent_data.html#nxevent_data-cue-index-field"
        ],
        description=(
            "Index into the event_id, event_time_offset pair matching the "
            "corresponding cue_timestamp."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="cue_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
