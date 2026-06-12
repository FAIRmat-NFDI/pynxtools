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
# Run `pynx nomad generate-metainfo --nxdl NXreftof` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.disk_chopper import DiskChopper
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Reftof"]


class Reftof(Entry):
    """
    This is an application definition for raw data from a TOF reflectometer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXreftof",
            category="application",
            symbols={
                "xSize": "xSize description",
                "ySize": "ySize description",
                "nTOF": "nTOF description",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofSample",
        repeats=False,
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofControl",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXreftof"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXreftof"],
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


class ReftofInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofInstrumentChopper",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name="chopper",
            name_type="specified",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.reftof.ReftofInstrumentDetector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-name-field"
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


class ReftofInstrumentChopper(DiskChopper):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-chopper-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name="chopper",
            name_type="specified",
            optionality="required",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-chopper-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Distance between chopper and sample"),
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


class ReftofInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-data-field"
        ],
        shape=["*", "*", "*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Array of time values for each bin in a time-of-flight measurement"
        ),
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    x_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-x-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="x_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-instrument-detector-y-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="y_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ReftofSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ReftofControl(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name="control",
            name_type="specified",
            optionality="required",
        ),
    )

    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-preset-field"
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
    integral = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-integral-field"
        ],
        description=("Total integral monitor counts"),
        a_nexus_field=NeXusField(
            name="integral",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Time channels"),
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-control-data-field"
        ],
        description=("Monitor counts in each time channel"),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ReftofData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-data-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-data-data-link"
        ],
        shape=["*", "*", "*"],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXreftof.html#nxreftof-entry-data-time-of-flight-link"
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
