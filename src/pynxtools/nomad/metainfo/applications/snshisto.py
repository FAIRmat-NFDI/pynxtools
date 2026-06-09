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
# Run `pynx nomad generate-metainfo --nxdl NXsnshisto` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Snshisto"]


class Snshisto(Entry):
    """
    This is a definition for histogram data from Spallation Neutron Source
    (SNS) at ORNL.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsnshisto",
            category="application",
        ),
    )

    DASlogs = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoDaslogs",
        repeats=False,
        description=(
            "Details of all logs, both from cvinfo file and from HistoTool "
            "(frequency and proton_charge)."
        ),
    )
    SNSHistoTool = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoSnshistotool",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoData",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoInstrument",
        repeats=False,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoMonitor",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoSample",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.snshisto.SnshistoUser",
        repeats=True,
        variable=True,
    )

    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-collection-identifier-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-collection-title-field"
        ],
        a_nexus_field=NeXusField(
            name="collection_title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsnshisto"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-definition-field"
        ],
        description=("Official NXDL schema after this file goes to applications."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsnshisto"],
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-duration-field"
        ],
        dimensionality="[time]",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-end-time-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-entry-identifier-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-experiment-identifier-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-notes-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-proton-charge-field"
        ],
        dimensionality="[current] * [time]",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-raw-frames-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-run-number-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-start-time-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-total-counts-field"
        ],
        dimensionality="dimensionless",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-total-uncounted-counts-field"
        ],
        dimensionality="dimensionless",
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


class SnshistoDaslogs(Collection):
    """
    Details of all logs, both from cvinfo file and from HistoTool (frequency
    and proton_charge).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-daslogs-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="DASlogs",
            name_type="specified",
            optionality="required",
        ),
    )

    log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
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
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
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


class SnshistoSnshistotool(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-snsbanking-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-snsmapping-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-author-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-command1-field"
        ],
        description=("Command string for event2histo_nxl."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-date-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-description-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-snshistotool-version-field"
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


class SnshistoData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-group"
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

    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-data-link"
        ],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )
    data_x_time_of_flight = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-data-x-time-of-flight-link"
        ],
        a_nexus_link=NeXusLink(
            name="data_x_time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/data_x_time_of_flight",
            optionality="required",
        ),
    )
    data_x_y = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-data-x-y-link"
        ],
        a_nexus_link=NeXusLink(
            name="data_x_y",
            target="/NXentry/NXinstrument/NXdetector/data_x_y",
            optionality="required",
        ),
    )
    data_y_time_of_flight = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-data-y-time-of-flight-link"
        ],
        a_nexus_link=NeXusLink(
            name="data_y_time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/data_y_time_of_flight",
            optionality="required",
        ),
    )
    pixel_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-pixel-id-link"
        ],
        a_nexus_link=NeXusLink(
            name="pixel_id",
            target="/NXentry/NXinstrument/NXdetector/pixel_id",
            optionality="required",
        ),
    )
    time_of_flight = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-time-of-flight-link"
        ],
        a_nexus_link=NeXusLink(
            name="time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/time_of_flight",
            optionality="required",
        ),
    )
    total_counts = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-total-counts-link"
        ],
        a_nexus_link=NeXusLink(
            name="total_counts",
            target="/NXentry/NXinstrument/NXdetector/total_counts",
            optionality="required",
        ),
    )
    x_pixel_offset = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-x-pixel-offset-link"
        ],
        a_nexus_link=NeXusLink(
            name="x_pixel_offset",
            target="/NXentry/NXinstrument/NXdetector/x_pixel_offset",
            optionality="required",
        ),
    )
    y_pixel_offset = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-data-y-pixel-offset-link"
        ],
        a_nexus_link=NeXusLink(
            name="y_pixel_offset",
            target="/NXentry/NXinstrument/NXdetector/y_pixel_offset",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SnshistoInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    SNSdetector_calibration_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-snsdetector-calibration-id-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-snsgeometry-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-snstranslation-service-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-beamline-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-instrument-name-field"
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


class SnshistoMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-monitor-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-monitor-data-field"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-monitor-distance-field"
        ],
        dimensionality="[length]",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-monitor-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-monitor-time-of-flight-field"
        ],
        dimensionality="[time]",
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


class SnshistoSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-changer-position-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-holder-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-identifier-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-sample-nature-field"
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


class SnshistoUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-user-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-user-facility-user-id-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-user-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsnshisto.html#nxsnshisto-entry-user-role-field"
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
