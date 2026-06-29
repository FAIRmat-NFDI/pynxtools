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
# Run `pynx nomad generate-metainfo --nxdl NXtomophase` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Tomophase"]


class Tomophase(Entry):
    """
    This is the application definition for x-ray or neutron tomography raw data
    with phase contrast variation at each point.

    In tomography first some dark field images are measured, some bright field
    images and, of course the sample. In order to properly sort the order of
    the images taken, a sequence number is stored with each image.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtomophase",
            category="application",
            symbols={
                "nBrightFrames": "Number of bright frames",
                "nDarkFrames": "Number of dark frames",
                "nSampleFrames": "Number of image (sample) frames",
                "nPhase": "Number of phase settings",
                "xSize": "Number of pixels in X direction",
                "ySize": "Number of pixels in Y direction",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseSample",
        repeats=False,
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseControl",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXtomophase"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtomophase"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXtomophase",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class TomophaseInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    bright_field = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseInstrumentBrightField",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="bright_field",
            name_type="specified",
            optionality="required",
        ),
    )
    dark_field = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseInstrumentDarkField",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="dark_field",
            name_type="specified",
            optionality="required",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomophase.TomophaseInstrumentSample",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomophaseInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-source-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-source-type-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-source-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    probe = Quantity(
        type=MEnum(["neutron", "x-ray", "electron"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["neutron", "x-ray", "electron"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomophaseInstrumentBrightField(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-bright-field-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="bright_field",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-bright-field-data-field"
        ],
        flexible_unit=True,
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    sequence_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-bright-field-sequence-number-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="sequence_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomophaseInstrumentDarkField(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-dark-field-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="dark_field",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-dark-field-data-field"
        ],
        flexible_unit=True,
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    sequence_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-dark-field-sequence-number-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="sequence_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomophaseInstrumentSample(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-data-field"
        ],
        flexible_unit=True,
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    sequence_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-sequence-number-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="sequence_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    x_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-x-pixel-size-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-y-pixel-size-field"
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
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-instrument-sample-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=("Distance between detector and sample"),
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


class TomophaseSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    x_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-x-translation-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="x_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-y-translation-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="y_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    z_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-sample-z-translation-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="z_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomophaseControl(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name="control",
            name_type="specified",
            optionality="required",
        ),
    )

    integral = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-control-integral-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Total integral monitor counts for each measured frame. Allows a "
            "correction for fluctuations in the beam between frames."
        ),
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


class TomophaseData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-data-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-data-data-link"
        ],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/sample:NXdetector/data",
            optionality="required",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomophase.html#nxtomophase-entry-data-rotation-angle-link"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="rotation_angle",
            target="/NXentry/NXsample/rotation_angle",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
