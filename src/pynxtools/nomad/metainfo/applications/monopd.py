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
# Run `pynx nomad generate-metainfo --nxdl NXmonopd` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.crystal import Crystal
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

__all__ = ["Monopd"]


class Monopd(Entry):
    """
    Monochromatic Neutron and X-Ray Powder diffractometer

    Instrument definition for a powder diffractometer at a monochromatic
    neutron or X-ray beam. This is both suited for a powder diffractometer with
    a single detector or a powder diffractometer with a position sensitive
    detector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmonopd",
            category="application",
            symbols={
                "i": "i is the number of wavelengths",
                "nDet": "Number of detectors",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdSample",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdMonitor",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdData",
        repeats=True,
        variable=True,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-start-time-field"
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
    definition = Quantity(
        type=MEnum(["NXmonopd"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmonopd"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXmonopd",
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


class MonopdInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-group"
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
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    crystal = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdInstrumentCrystal",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.monopd.MonopdInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MonopdInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-source-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-source-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-source-probe-field"
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


class MonopdInstrumentCrystal(Crystal):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-crystal-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-crystal-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Optimum diffracted wavelength"),
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


class MonopdInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-instrument-detector-data-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "detector signal (usually counts) are already corrected for detector "
            "efficiency"
        ),
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


class MonopdSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-sample-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Optional rotation angle for the case when the powder diagram has "
            "been obtained through an omega-2theta scan like from a traditional "
            "single detector powder diffractometer"
        ),
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MonopdMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-monitor-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-monitor-mode-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    preset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-monitor-preset-field"
        ],
        flexible_unit=True,
        description=("preset value for time or monitor"),
        a_nexus_field=NeXusField(
            name="preset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    integral = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-monitor-integral-field"
        ],
        flexible_unit=True,
        description=("Total integral monitor counts"),
        a_nexus_field=NeXusField(
            name="integral",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MonopdData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-data-polar-angle-link"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("Link to polar angle in /NXentry/NXinstrument/NXdetector"),
        a_nexus_link=NeXusLink(
            name="polar_angle",
            target="/NXentry/NXinstrument/NXdetector/polar_angle",
            optionality="required",
        ),
    )
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-data-data-link"
        ],
        shape=["*"],
        flexible_unit=True,
        description=("Link to data in /NXentry/NXinstrument/NXdetector"),
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
