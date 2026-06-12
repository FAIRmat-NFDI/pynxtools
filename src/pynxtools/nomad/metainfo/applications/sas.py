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
# Run `pynx nomad generate-metainfo --nxdl NXsas` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.shape import Shape
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Sas"]


class Sas(Entry):
    """
    Raw, monochromatic 2-D SAS data with an area detector.

    This is an application definition for raw data (not processed or reduced
    data) from a 2-D small angle scattering instrument collected with a
    monochromatic beam and an area detector. It is meant to be suitable both
    for neutron SANS and X-ray SAXS data.

    It covers all raw data from any monochromatic SAS techniques that use an
    area detector: SAS, WSAS, grazing incidence, GISAS

    It covers all raw data from any SAS techniques that use an area detector
    and a monochromatic beam.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsas",
            category="application",
            symbols={
                "nXPixel": "Number of pixels in x direction.",
                "nYPixel": "Number of pixels in y direction.",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasSample",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasMonitor",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasData",
        repeats=True,
        variable=True,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-start-time-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsas"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsas"],
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


class SasInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentMonochromator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    collimator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentCollimator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-name-field"
        ],
        description=("Name of the instrument actually used to perform the experiment."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-source-type-field"
        ],
        description=("Type of radiation source."),
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
    probe = Quantity(
        type=MEnum(["neutron", "x-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-source-probe-field"
        ],
        description=(
            "Name of radiation probe, necessary to compute the sample contrast."
        ),
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


class SasInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-monochromator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-monochromator-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The wavelength (:math:`\\lambda`) of the radiation."),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
    )
    wavelength_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-monochromator-wavelength-spread-field"
        ],
        description=(
            "delta_lambda/lambda (:math:`\\Delta\\lambda/\\lambda`): Important "
            "for resolution calculations."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_spread",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasInstrumentCollimator(Collimator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-collimator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentCollimatorGeometry",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasInstrumentCollimatorGeometry(Geometry):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-collimator-geometry-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sas.SasInstrumentCollimatorGeometryShape",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasInstrumentCollimatorGeometryShape(Shape):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-collimator-geometry-shape-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    shape = Quantity(
        type=MEnum(["nxcylinder", "nxbox"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-collimator-geometry-shape-shape-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-collimator-geometry-shape-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("The collimation length."),
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


class SasInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-data-field"
        ],
        shape=["*", "*"],
        description=(
            "This is area detector data, number of x-pixel versus number of "
            "y-pixels. Since the beam center is to be determined as a step of "
            "data reduction, it is not necessary to document or assume the "
            "position of the beam center in acquired data. It is necessary to "
            "define which are the x and y directions, to coordinate with the "
            "pixel size and compute Q."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=("The distance between detector and sample."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-x-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Physical size of a pixel in x-direction."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-y-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Physical size of a pixel in y-direction."),
        a_nexus_field=NeXusField(
            name="y_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    aequatorial_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-instrument-detector-aequatorial-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="aequatorial_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-sample-name-field"
        ],
        description=("Descriptive name of sample."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-sample-aequatorial-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="aequatorial_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-monitor-group"
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

    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-monitor-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-monitor-preset-field"
        ],
        description=("Preset value for time or monitor."),
        a_nexus_field=NeXusField(
            name="preset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    integral = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-monitor-integral-field"
        ],
        description=("Total integral monitor counts."),
        a_nexus_field=NeXusField(
            name="integral",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SasData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=MEnum(["data"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-data-signal-attribute"
        ],
        description=(
            "Name the *plottable* field. The link here defines this name as ``data``."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["data"],
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsas.html#nxsas-entry-data-data-link"
        ],
        shape=["*", "*"],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
