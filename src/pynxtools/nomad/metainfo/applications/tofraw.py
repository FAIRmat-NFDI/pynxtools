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
# Run `pynx nomad generate-metainfo --nxdl NXtofraw` to regenerate.
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

__all__ = ["Tofraw"]


class Tofraw(Entry):
    """
    This is an application definition for raw data from a generic TOF
    instrument
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtofraw",
            category="application",
            symbols={
                "nDet": "Number of detectors",
                "nTimeChan": "nTimeChan description",
            },
        ),
    )

    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawUser",
        repeats=False,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawSample",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawMonitor",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXtofraw"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtofraw"],
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-duration-field"
        ],
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    run_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-run-number-field"
        ],
        a_nexus_field=NeXusField(
            name="run_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-pre-sample-flightpath-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the flight path before the sample position. This can be "
            "determined by a chopper, by the moderator, or the source itself. In "
            "other words: it is the distance to the component which gives the T0 "
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


class TofrawUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-user-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-user-name-field"
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


class TofrawInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tofraw.TofrawInstrumentDetector",
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


class TofrawInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-data-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-detector-number-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-distance-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-time-of-flight-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-polar-angle-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-instrument-detector-azimuthal-angle-field"
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


class TofrawSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-sample-name-field"
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
        type=MEnum(["powder", "liquid", "single crystal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-sample-nature-field"
        ],
        a_nexus_field=NeXusField(
            name="nature",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["powder", "liquid", "single crystal"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofrawMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-preset-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-distance-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-data-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-time-of-flight-field"
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
    integral_counts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-monitor-integral-counts-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="integral_counts",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TofrawData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-data-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-data-data-link"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-data-detector-number-link"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-data-time-of-flight-link"
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
