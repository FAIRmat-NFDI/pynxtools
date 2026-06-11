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
# Run `pynx nomad generate-metainfo --nxdl NXsastof` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.collimator import Collimator
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.geometry import Geometry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.shape import Shape
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Sastof"]


class Sastof(Entry):
    """
    raw, 2-D SAS data with an area detector with a time-of-flight source

    It covers all raw data from any SAS techniques that use an area detector at
    a time-of-flight source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsastof",
            category="application",
            symbols={
                "nXPixel": "nXPixel description",
                "nYPixel": "nYPixel description",
                "nTOF": "nTOF description",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofSample",
        repeats=False,
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofControl",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsastof"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsastof"],
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


class SastofInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrumentSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )
    collimator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrumentCollimator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name="collimator",
            name_type="specified",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrumentDetector",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-name-field"
        ],
        description=("Name of the instrument actually used to perform the experiment"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-source-type-field"
        ],
        description=("type of radiation source"),
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
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-source-name-field"
        ],
        description=("Name of the radiation source"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    probe = Quantity(
        type=MEnum(["neutron", "x-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["neutron", "x-ray"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofInstrumentCollimator(Collimator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-collimator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name="collimator",
            name_type="specified",
            optionality="required",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrumentCollimatorGeometry",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofInstrumentCollimatorGeometry(Geometry):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-collimator-geometry-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="required",
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sastof.SastofInstrumentCollimatorGeometryShape",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofInstrumentCollimatorGeometryShape(Shape):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-collimator-geometry-shape-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="required",
        ),
    )

    shape = Quantity(
        type=MEnum(["nxcylinder", "nxbox"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-collimator-geometry-shape-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["nxcylinder", "nxbox"],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-collimator-geometry-shape-size-field"
        ],
        dimensionality="[length]",
        shape=["*", "*"],
        description=("The collimation length"),
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


class SastofInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-data-field"
        ],
        shape=["*", "*", "*"],
        description=(
            "This is area detector data, of number of x-pixel versus number of "
            "y-pixels. Since the beam center is to be determined as a step of "
            "data reduction, it is not necessary to document or assume the "
            "position of the beam center in acquired data."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-time-of-flight-field"
        ],
        dimensionality="[time]",
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        shape=["*", "*", "*"],
        description=("The distance between detector and sample"),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    x_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-x-pixel-size-field"
        ],
        dimensionality="[length]",
        shape=["*", "*"],
        description=("Physical size of a pixel in x-direction"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-y-pixel-size-field"
        ],
        dimensionality="[length]",
        shape=["*", "*"],
        description=("Size of a pixel in y direction"),
        a_nexus_field=NeXusField(
            name="y_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*", "*", "*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-rotation-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    aequatorial_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-aequatorial-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="aequatorial_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    beam_center_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-beam-center-x-field"
        ],
        dimensionality="[length]",
        description=(
            "This is the x position where the direct beam would hit the "
            "detector. This is a length, not a pixel position, and can be "
            "outside of the actual detector."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    beam_center_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-instrument-detector-beam-center-y-field"
        ],
        dimensionality="[length]",
        description=(
            "This is the y position where the direct beam would hit the "
            "detector. This is a length, not a pixel position, and can be "
            "outside of the actual detector."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    aequatorial_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-sample-aequatorial-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="aequatorial_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SastofControl(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-control-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-control-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-control-preset-field"
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
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-control-data-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-control-time-of-flight-field"
        ],
        dimensionality="[time]",
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


class SastofData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-data-data-link"
        ],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )
    time_of_flight = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsastof.html#nxsastof-entry-data-time-of-flight-link"
        ],
        a_nexus_link=NeXusLink(
            name="time_of_flight",
            target="/NXentry/NXinstrument/NXdetector/time_of_flight",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
