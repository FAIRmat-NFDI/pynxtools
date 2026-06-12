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
# Run `pynx nomad generate-metainfo --nxdl NXtofnpd` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Tofnpd"]


class Tofnpd(Entry):
    """
    This is a application definition for raw data from a TOF neutron powder
    diffractometer
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtofnpd",
            category="application",
            symbols={
                "nDet": "Number of detectors",
                "nTimeChan": "nTimeChan description",
            },
        ),
    )

    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdUser",
        repeats=False,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdSample",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdMonitor",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXtofnpd"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtofnpd"],
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-pre-sample-flightpath-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the flight path before the sample position. This can be "
            "determined by a chopper, by the moderator or the source itself. In "
            "other words: it the distance to the component which gives the T0 "
            "signal to the detector electronics. If another component in the "
            "NXinstrument hierarchy provides this information, this should be a "
            "link."
        ),
        a_nexus_field=NeXusField(
            name="pre_sample_flightpath",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
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


class TofnpdUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-user-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="user",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-user-name-field"
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


class TofnpdInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofnpd.TofnpdInstrumentDetector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofnpdInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-data-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    detector_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-detector-number-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="detector_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("distance to sample for each detector"),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("polar angle for each detector element"),
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-instrument-detector-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("azimuthal angle for each detector element"),
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofnpdSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofnpdMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-mode-field"
        ],
        description=(
            "Count to a preset value based on either clock time (timer) or "
            "received monitor counts (monitor)."
        ),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["monitor", "timer"],
        ),
    )
    preset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-preset-field"
        ],
        description=("preset value for time or monitor"),
        a_nexus_field=NeXusField(
            name="preset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-distance-field"
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
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-data-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-monitor-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME_OF_FLIGHT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofnpdData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-data-data-link"
        ],
        shape=["*", "*"],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )
    detector_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-data-detector-number-link"
        ],
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="detector_number",
            target="/NXentry/NXinstrument/NXdetector/detector_number",
            optionality="required",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofnpd.html#nxtofnpd-entry-data-time-of-flight-link"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/time_of_flight",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
