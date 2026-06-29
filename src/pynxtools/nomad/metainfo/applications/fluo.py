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
# Run `pynx nomad generate-metainfo --nxdl NXfluo` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Fluo"]


class Fluo(Entry):
    """
    This is an application definition for raw data from an X-ray fluorescence
    experiment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfluo",
            category="application",
            symbols={"nE": "Number of energies"},
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoSample",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoMonitor",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-start-time-field"
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
        type=MEnum(["NXfluo"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXfluo"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXfluo",
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


class FluoInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-group"
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
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoInstrumentSource",
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
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoInstrumentMonochromator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator",
            name_type="specified",
            optionality="required",
        ),
    )
    fluorescence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.fluo.FluoInstrumentFluorescence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="fluorescence",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FluoInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-source-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-source-name-field"
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
        type=MEnum(["x-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["x-ray"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="x-ray",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FluoInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-monochromator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator",
            name_type="specified",
            optionality="required",
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-monochromator-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FluoInstrumentFluorescence(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-fluorescence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="fluorescence",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-fluorescence-data-field"
        ],
        flexible_unit=True,
        shape=["*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-instrument-fluorescence-energy-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FluoSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-sample-name-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FluoMonitor(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-monitor-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-monitor-mode-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-monitor-preset-field"
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
    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-monitor-data-field"
        ],
        flexible_unit=True,
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
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


class FluoData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    energy = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-data-energy-link"
        ],
        a_nexus_link=NeXusLink(
            name="energy",
            target="/entry/instrument/fluorescence/energy",
            optionality="required",
        ),
    )
    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXfluo.html#nxfluo-entry-data-data-link"
        ],
        a_nexus_link=NeXusLink(
            name="data",
            target="/entry/instrument/fluorescence/data",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
