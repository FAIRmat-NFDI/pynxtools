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
# Run `pynx nomad generate-metainfo --nxdl NXsnsevent` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.aperture import Aperture
from pynxtools.nomad.metainfo.base_classes.attenuator import Attenuator
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.crystal import Crystal
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.disk_chopper import DiskChopper
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.event_data import EventData
from pynxtools.nomad.metainfo.base_classes.geometry import Geometry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.log import Log
from pynxtools.nomad.metainfo.base_classes.moderator import Moderator
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.orientation import Orientation
from pynxtools.nomad.metainfo.base_classes.positioner import Positioner
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.shape import Shape
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.translation import Translation
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Snsevent"]


class Snsevent(Entry):
    """
    This is a definition for event data from Spallation Neutron Source (SNS) at
    ORNL.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsnsevent",
            category="application",
        ),
    )

    DASlogs = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventDaslogs",
        repeats=False,
        description=(
            "Details of all logs, both from cvinfo file and from HistoTool "
            "(frequency and proton_charge)."
        ),
    )
    SNSHistoTool = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventSnshistotool",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventData",
        repeats=True,
        variable=True,
    )
    event_data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventEventData",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrument",
        repeats=False,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventMonitor",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventSample",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventUser",
        repeats=True,
        variable=True,
    )

    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-collection-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    collection_title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-collection-title-field"
        ],
        a_nexus_field=NeXusField(
            name="collection_title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsnsevent"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-definition-field"
        ],
        description=("Official NXDL schema after this file goes to applications."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsnsevent"],
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-duration-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    entry_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-entry-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-experiment-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    notes_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-notes-field"
        ],
        a_nexus_field=NeXusField(
            name="notes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    proton_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-proton-charge-field"
        ],
        dimensionality="[current] * [time]",
        unit="coulomb",
        a_nexus_field=NeXusField(
            name="proton_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_CHARGE",
        ),
    )
    raw_frames = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-raw-frames-field"
        ],
        a_nexus_field=NeXusField(
            name="raw_frames",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    run_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-run-number-field"
        ],
        a_nexus_field=NeXusField(
            name="run_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    total_counts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-total-counts-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="total_counts",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    total_uncounted_counts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-total-uncounted-counts-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="total_uncounted_counts",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
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


class SnseventDaslogs(Collection):
    """
    Details of all logs, both from cvinfo file and from HistoTool (frequency
    and proton_charge).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="DASlogs",
            name_type="specified",
            optionality="required",
        ),
    )

    log = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventDaslogsLog",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventDaslogsPositioner",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventDaslogsLog(Log):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    average_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-average-value-field"
        ],
        a_nexus_field=NeXusField(
            name="average_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    average_value_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-average-value-errors-field"
        ],
        a_nexus_field=NeXusField(
            name="average_value_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-duration-field"
        ],
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    maximum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-maximum-value-field"
        ],
        a_nexus_field=NeXusField(
            name="maximum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    minimum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-minimum-value-field"
        ],
        a_nexus_field=NeXusField(
            name="minimum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-log-value-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventDaslogsPositioner(Positioner):
    """
    Motor logs from cvinfo file.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    average_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-average-value-field"
        ],
        a_nexus_field=NeXusField(
            name="average_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    average_value_error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-average-value-error-field"
        ],
        a_nexus_field=NeXusField(
            name="average_value_error",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="see https://github.com/nexusformat/definitions/issues/821",
        ),
    )
    average_value_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-average-value-errors-field"
        ],
        a_nexus_field=NeXusField(
            name="average_value_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-duration-field"
        ],
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    maximum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-maximum-value-field"
        ],
        a_nexus_field=NeXusField(
            name="maximum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    minimum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-minimum-value-field"
        ],
        a_nexus_field=NeXusField(
            name="minimum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-time-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-daslogs-positioner-value-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventSnshistotool(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="SNSHistoTool",
            name_type="specified",
            optionality="required",
        ),
    )

    SNSbanking_file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-snsbanking-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="SNSbanking_file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    SNSmapping_file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-snsmapping-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="SNSmapping_file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    author = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-author-field"
        ],
        a_nexus_field=NeXusField(
            name="author",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    command1 = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-command1-field"
        ],
        description=("Command string for event2nxl."),
        a_nexus_field=NeXusField(
            name="command1",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    date = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-date-field"
        ],
        a_nexus_field=NeXusField(
            name="date",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-snshistotool-version-field"
        ],
        a_nexus_field=NeXusField(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    data_x_y = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-data-data-x-y-link"
        ],
        shape=["*", "*"],
        a_nexus_link=NeXusLink(
            name="data_x_y",
            target="/NXentry/NXinstrument/NXdetector/data_x_y",
            optionality="required",
        ),
    )
    x_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-data-x-pixel-offset-link"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="x_pixel_offset",
            target="/NXentry/NXinstrument/NXdetector/x_pixel_offset",
            optionality="required",
        ),
    )
    y_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-data-y-pixel-offset-link"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="y_pixel_offset",
            target="/NXentry/NXinstrument/NXdetector/y_pixel_offset",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventEventData(EventData):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-event-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXevent_data",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    event_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-event-data-event-index-link"
        ],
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="event_index",
            target="/NXentry/NXinstrument/NXdetector/event_index",
            optionality="required",
        ),
    )
    event_pixel_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-event-data-event-pixel-id-link"
        ],
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="event_pixel_id",
            target="/NXentry/NXinstrument/NXdetector/event_pixel_id",
            optionality="required",
        ),
    )
    event_time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-event-data-event-time-of-flight-link"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="event_time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/event_time_of_flight",
            optionality="required",
        ),
    )
    pulse_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-event-data-pulse-time-link"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="pulse_time",
            target="/NXentry/NXinstrument/NXdetector/pulse_time",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    SNS = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentSns",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="SNS",
            name_type="specified",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )
    disk_chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDiskChopper",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    moderator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentModerator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmoderator",
            name="moderator",
            name_type="specified",
            optionality="required",
        ),
    )
    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentAperture",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentAttenuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    crystal = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentCrystal",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    SNSdetector_calibration_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-snsdetector-calibration-id-field"
        ],
        description=("Detector calibration id from DAS."),
        a_nexus_field=NeXusField(
            name="SNSdetector_calibration_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    SNSgeometry_file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-snsgeometry-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="SNSgeometry_file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    SNStranslation_service = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-snstranslation-service-field"
        ],
        a_nexus_field=NeXusField(
            name="SNStranslation_service",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    beamline = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-beamline-field"
        ],
        a_nexus_field=NeXusField(
            name="beamline",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentSns(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-sns-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="SNS",
            name_type="specified",
            optionality="required",
        ),
    )

    frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-sns-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        a_nexus_field=NeXusField(
            name="frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_FREQUENCY",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-sns-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    probe = Quantity(
        type=MEnum(
            [
                "neutron",
                "photon",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-sns-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "neutron",
                "photon",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ],
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-sns-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Pulsed Muon Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Free-Electron Laser",
                "Optical Laser",
                "Ion Source",
                "UV Plasma Source",
                "Metal Jet X-ray",
                "Laser",
                "Dye Laser",
                "Broadband Tunable Light Source",
                "Halogen Lamp",
                "LED",
                "Mercury Cadmium Telluride Lamp",
                "Deuterium Lamp",
                "Xenon Lamp",
                "Globar",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    origin = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDetectorOrigin",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    data_x_y = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-data-x-y-field"
        ],
        shape=["*", "*"],
        description=('expect ``signal=2 axes="x_pixel_offset,y_pixel_offset``"'),
        a_nexus_field=NeXusField(
            name="data_x_y",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    event_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-event-index-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="event_index",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_pixel_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-event-pixel-id-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="event_pixel_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-event-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="event_time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    pixel_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-pixel-id-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="pixel_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    pulse_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-pulse-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="pulse_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    total_counts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-total-counts-field"
        ],
        a_nexus_field=NeXusField(
            name="total_counts",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    x_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-x-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="x_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-y-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="y_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDetectorOrigin(Geometry):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDetectorOriginOrientation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDetectorOriginShape",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )
    translation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentDetectorOriginTranslation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDetectorOriginOrientation(Orientation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-orientation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-orientation-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6],
        description=("Six out of nine rotation parameters."),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDetectorOriginShape(Shape):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-shape-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-shape-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = Quantity(
        type=MEnum(
            [
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-shape-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-shape-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDetectorOriginTranslation(Translation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-translation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-detector-origin-translation-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentDiskChopper(DiskChopper):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-disk-chopper-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-disk-chopper-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentModerator(Moderator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-moderator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmoderator",
            name="moderator",
            name_type="specified",
            optionality="required",
        ),
    )

    coupling_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-moderator-coupling-material-field"
        ],
        a_nexus_field=NeXusField(
            name="coupling_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-moderator-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-moderator-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    type = Quantity(
        type=MEnum(
            [
                "H20",
                "D20",
                "Liquid H2",
                "Liquid CH4",
                "Liquid D2",
                "Solid D2",
                "C",
                "Solid CH4",
                "Solid H2",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-moderator-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "H20",
                "D20",
                "Liquid H2",
                "Liquid CH4",
                "Liquid D2",
                "Solid D2",
                "C",
                "Solid CH4",
                "Solid H2",
            ],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentAperture(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    origin = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentApertureOrigin",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    x_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-x-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="x_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentApertureOrigin(Geometry):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentApertureOriginOrientation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentApertureOriginShape",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )
    translation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentApertureOriginTranslation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentApertureOriginOrientation(Orientation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-orientation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-orientation-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6],
        description=("Six out of nine rotation parameters."),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentApertureOriginShape(Shape):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-shape-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-shape-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = Quantity(
        type=MEnum(
            [
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-shape-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-shape-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentApertureOriginTranslation(Translation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-translation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-aperture-origin-translation-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentAttenuator(Attenuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-attenuator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-attenuator-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentCrystal(Crystal):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    origin = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentCrystalOrigin",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentCrystalOrigin(Geometry):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="origin",
            name_type="specified",
            optionality="required",
        ),
    )

    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentCrystalOriginOrientation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentCrystalOriginShape",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )
    translation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snsevent.SnseventInstrumentCrystalOriginTranslation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentCrystalOriginOrientation(Orientation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-orientation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="orientation",
            name_type="specified",
            optionality="required",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-orientation-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6],
        description=("Six out of nine rotation parameters."),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentCrystalOriginShape(Shape):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-shape-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-shape-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    shape = Quantity(
        type=MEnum(
            [
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-shape-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "nxflat",
                "nxcylinder",
                "nxbox",
                "nxsphere",
                "nxcone",
                "nxelliptical",
                "nxtoroidal",
                "nxparabolic",
                "nxpolynomial",
            ],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-shape-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventInstrumentCrystalOriginTranslation(Translation):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-translation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name="translation",
            name_type="specified",
            optionality="required",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-instrument-crystal-origin-translation-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-monitor-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-monitor-data-field"
        ],
        shape=["*"],
        description=('expect ``signal=1 axes="time_of_flight"``'),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-monitor-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-monitor-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["monitor", "timer"],
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-monitor-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    changer_position = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-changer-position-field"
        ],
        a_nexus_field=NeXusField(
            name="changer_position",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    holder = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-holder-field"
        ],
        a_nexus_field=NeXusField(
            name="holder",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    nature = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-sample-nature-field"
        ],
        a_nexus_field=NeXusField(
            name="nature",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnseventUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-user-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    facility_user_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-user-facility-user-id-field"
        ],
        a_nexus_field=NeXusField(
            name="facility_user_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-user-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    role = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnsevent.html#nxsnsevent-entry-user-role-field"
        ],
        a_nexus_field=NeXusField(
            name="role",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
