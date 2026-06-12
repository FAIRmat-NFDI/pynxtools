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
# Run `pynx nomad generate-metainfo --nxdl NXarpes` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Arpes"]


class Arpes(Entry):
    """
    This is an application definition for angular resolved photo electron
    spectroscopy.

    It has been drawn up with hemispherical electron analysers in mind.

    This definition is a legacy support for older NXarpes experiments. There
    is, however, a newer definition to collect data & metadata for general
    photoemission experiments, called :ref:`NXmpes`, as well as a
    specialization for ARPES experiments, called :ref:`NXmpes_arpes`."
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXarpes",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.arpes.ArpesInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.arpes.ArpesSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXarpes"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXarpes"],
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


class ArpesInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-group"
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
        section_def="pynxtools.nomad.metainfo.applications.arpes.ArpesInstrumentSource",
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
        section_def="pynxtools.nomad.metainfo.applications.arpes.ArpesInstrumentMonochromator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator",
            name_type="specified",
            optionality="required",
        ),
    )
    analyser = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.arpes.ArpesInstrumentAnalyser",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="analyser",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArpesInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-source-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-source-type-field"
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
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-source-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    probe = Quantity(
        type=MEnum(["x-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["x-ray"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArpesInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-monochromator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator",
            name_type="specified",
            optionality="required",
        ),
    )

    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-monochromator-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArpesInstrumentAnalyser(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="analyser",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-data-field"
        ],
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    lens_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-lens-mode-field"
        ],
        description=("setting for the electron analyser lens"),
        a_nexus_field=NeXusField(
            name="lens_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    acquisition_mode = Quantity(
        type=MEnum(["swept", "fixed"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-acquisition-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="acquisition_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["swept", "fixed"],
        ),
    )
    entrance_slit_shape = Quantity(
        type=MEnum(["curved", "straight"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-entrance-slit-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="entrance_slit_shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["curved", "straight"],
        ),
    )
    entrance_slit_setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-entrance-slit-setting-field"
        ],
        description=("dial setting of the entrance slit"),
        a_nexus_field=NeXusField(
            name="entrance_slit_setting",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    entrance_slit_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-entrance-slit-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("size of the entrance slit"),
        a_nexus_field=NeXusField(
            name="entrance_slit_size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    pass_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-pass-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy of the electrons on the mean path of the analyser"),
        a_nexus_field=NeXusField(
            name="pass_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    time_per_channel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-time-per-channel-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("todo: define more clearly"),
        a_nexus_field=NeXusField(
            name="time_per_channel",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    angles = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-angles-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angular axis of the analyser data which dimension the axis applies "
            "to is defined using the normal NXdata methods."
        ),
        a_nexus_field=NeXusField(
            name="angles",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    energies = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-energies-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Energy axis of the analyser data which dimension the axis applies "
            "to is defined using the normal NXdata methods."
        ),
        a_nexus_field=NeXusField(
            name="energies",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    sensor_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-sensor-size-field"
        ],
        shape=[2],
        description=("number of raw active elements in each dimension"),
        a_nexus_field=NeXusField(
            name="sensor_size",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    region_origin = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-region-origin-field"
        ],
        shape=[2],
        description=("origin of rectangular region selected for readout"),
        a_nexus_field=NeXusField(
            name="region_origin",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    region_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-instrument-analyser-region-size-field"
        ],
        shape=[2],
        description=("size of rectangular region selected for readout"),
        a_nexus_field=NeXusField(
            name="region_size",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArpesSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarpes.html#nxarpes-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
