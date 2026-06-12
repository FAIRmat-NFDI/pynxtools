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
# Run `pynx nomad generate-metainfo --nxdl NXazint2d` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Azint2d"]


class Azint2d(Entry):
    """
    Application definition for data from two-dimensional area detectors that
    has been integrated azimuthally, with a certain radial binning in units of
    q or 2theta and with a binning around the azimuthal angle eta.

    An example application that creates these files is documented here:
    https://maxiv-science.github.io/azint_writer/
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXazint2d",
            category="application",
            symbols={
                "nImg": "Number of integrated images",
                "nRad": "Number of radial bins",
                "nRadEdge": "Number of radial bin edges (nRad+1)",
                "nEta": "Number of azimuthal bins",
                "nEtaEdge": "Number of azimuthal bin edges (nEta+1)",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dInstrument",
        repeats=True,
        variable=True,
    )
    reduction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dReduction",
        repeats=False,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dMonitor",
        repeats=True,
        variable=True,
        description=("Monitor data for example `I_zero`."),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dData",
        repeats=True,
        variable=True,
        description=(
            "Azimuthally integrated data with radial binning in q or 2theta and "
            "with azimuthal binning."
        ),
    )

    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which :ref:`NXdata` group contains the "
            "data to be shown by default. It is needed to resolve ambiguity when "
            "more than one :ref:`NXdata` group exists. The value is the name of "
            "the default :ref:`NXdata` group."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXazint2d"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXazint2d"],
        ),
    )
    solid_angle_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-solid-angle-applied-field"
        ],
        description=("is solid angle correction applied or not."),
        a_nexus_field=NeXusField(
            name="solid_angle_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    polarization_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-polarization-applied-field"
        ],
        description=("is polarization correction applied or not."),
        a_nexus_field=NeXusField(
            name="polarization_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    normalization_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-normalization-applied-field"
        ],
        description=(
            "is a normalization correction applied or not. It indicates that "
            "integrated intensities and their errors were already divided by the "
            "appropriate normalization factors accounting for the effective "
            "number or weighted contribution of detector pixels to each "
            "integration bin."
        ),
        a_nexus_field=NeXusField(
            name="normalization_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    monitor_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-monitor-applied-field"
        ],
        description=(
            "is a monitor correction applied or not. The monitor correction "
            "accounts for external factors that are independent of the azimuthal "
            "integration process. Most commonly, this involves normalizing for "
            "fluctuations in the incident beam intensity or, where applicable, "
            "variations in exposure time."
        ),
        a_nexus_field=NeXusField(
            name="monitor_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
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


class Azint2dInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dInstrumentMonochromator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.azint2d.Azint2dInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-name-field"
        ],
        description=("Name of instrument (beamline) where data was collected."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class Azint2dInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-monochromator-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-monochromator-wavelength-field"
        ],
        dimensionality="[length]",
        unit="angstrom",
        description=("Wavelength in angstrom."),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="angstrom",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-monochromator-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="keV",
        description=("Energy in keV."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="keV",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class Azint2dInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-source-name-field"
        ],
        description=("Name of laboratory where data was collected."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-source-type-field"
        ],
        description=("Type of laboratory where data was collected."),
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
        type=MEnum(
            [
                "neutron",
                "photon",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-instrument-source-probe-field"
        ],
        description=("Type of probe."),
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "neutron",
                "photon",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class Azint2dReduction(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="reduction",
            name_type="specified",
            optionality="required",
        ),
    )

    input = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="input",
            name_type="specified",
            optionality="required",
        ),
    )

    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-program-field"
        ],
        description=("Name of the program that made this file."),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-version-field"
        ],
        description=("Version of the program that made this file."),
        a_nexus_field=NeXusField(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-date-field"
        ],
        description=("Date the file was created."),
        a_nexus_field=NeXusField(
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    reference = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-reference-field"
        ],
        description=(
            "Citation or other references for the algorithm used in the processing."
        ),
        a_nexus_field=NeXusField(
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    note_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-reduction-note-field"
        ],
        description=(
            "Notes required to help interpret the data, e.g. on coordinate systems."
        ),
        a_nexus_field=NeXusField(
            name="note",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class Azint2dMonitor(Monitor):
    """
    Monitor data for example `I_zero`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-monitor-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-monitor-data-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class Azint2dData(Data):
    """
    Azimuthally integrated data with radial binning in q or 2theta and with
    azimuthal binning.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    interpretation = Quantity(
        type=MEnum(["image"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["image"],
        ),
    )
    signal = Quantity(
        type=MEnum(["I"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["I"],
        ),
    )
    I = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-field"
        ],
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="I",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    I__long_name = Quantity(
        type=MEnum(["intensity"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="I",
            enumeration=["intensity"],
        ),
    )
    I__units = Quantity(
        type=MEnum(["arbitrary units"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="I",
            enumeration=["arbitrary units"],
        ),
    )
    I_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-errors-field"
        ],
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="I_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    I_errors__long_name = Quantity(
        type=MEnum(["estimated intensity error"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-errors-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="I_errors",
            enumeration=["estimated intensity error"],
        ),
    )
    I_errors__units = Quantity(
        type=MEnum(["arbitrary units"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-i-errors-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="I_errors",
            enumeration=["arbitrary units"],
        ),
    )
    radial_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="radial_axis",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    radial_axis__long_name = Quantity(
        type=MEnum(["q", "2theta"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="radial_axis",
            enumeration=["q", "2theta"],
        ),
    )
    radial_axis__units = Quantity(
        type=MEnum(["NX_PER_LENGHT", "NX_WAVENUMBER", "NX_ANGLE"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="radial_axis",
            enumeration=["NX_PER_LENGHT", "NX_WAVENUMBER", "NX_ANGLE"],
        ),
    )
    radial_axis_edges = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-edges-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="radial_axis_edges",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    radial_axis_edges__long_name = Quantity(
        type=MEnum(["q bin edges", "2theta bin edges"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-edges-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="radial_axis_edges",
            enumeration=["q bin edges", "2theta bin edges"],
        ),
    )
    radial_axis_edges__units = Quantity(
        type=MEnum(["NX_PER_LENGTH", "NX_WAVENUMBER", "NX_ANGLE"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-radial-axis-edges-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="radial_axis_edges",
            enumeration=["NX_PER_LENGTH", "NX_WAVENUMBER", "NX_ANGLE"],
        ),
    )
    norm = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-norm-field"
        ],
        shape=["*", "*"],
        description=(
            "Values of the normalization correction. The normalization "
            "correction accounts for the effective number or weighted "
            "contribution of detector pixels to each integration bin. Note: An "
            "important aspect of the normalization strategy is how polarization "
            "and solid angle corrections are incorporated, which can vary "
            "depending on the specific application, software, and its "
            "configuration options (see, for example, PyFAI documentation). "
            "Additionally, the normalization strategy may include a relative or "
            "absolute calibration factor. Two common normalization approaches "
            'are: "Relative normalization" to the PONI (Point Of Normal '
            'Incidence) pixel, and "Absolute calibration", which yields the '
            "number of photons scattered by the sample in a given direction per "
            "unit solid angle. The type of the normalization strategy is not "
            "indicated on this level. It must be concluded from the software "
            "used or its parameters. The monitor correction is not included in "
            "the normalization correction and it is specified separately."
        ),
        a_nexus_field=NeXusField(
            name="norm",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    norm__long_name = Quantity(
        type=MEnum(
            ["effective number of pixels contributing to the corresponding bin"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-norm-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="norm",
            enumeration=[
                "effective number of pixels contributing to the corresponding bin"
            ],
        ),
    )
    norm__units = Quantity(
        type=MEnum(["arbitrary units"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-norm-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="norm",
            enumeration=["arbitrary units"],
        ),
    )
    azimuthal_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="azimuthal_axis",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    azimuthal_axis__long_name = Quantity(
        type=MEnum(["azimuthal bin center"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuthal_axis",
            enumeration=["azimuthal bin center"],
        ),
    )
    azimuthal_axis__units = Quantity(
        type=MEnum(["NX_ANGLE"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuthal_axis",
            enumeration=["NX_ANGLE"],
        ),
    )
    azimuthal_axis_edges = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-edges-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="azimuthal_axis_edges",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    azimuthal_axis_edges__long_name = Quantity(
        type=MEnum(["azimuthal bin edges"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-edges-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuthal_axis_edges",
            enumeration=["azimuthal bin edges"],
        ),
    )
    azimuthal_axis_edges__units = Quantity(
        type=MEnum(["NX_ANGLE"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXazint2d.html#nxazint2d-entry-data-azimuthal-axis-edges-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuthal_axis_edges",
            enumeration=["NX_ANGLE"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
