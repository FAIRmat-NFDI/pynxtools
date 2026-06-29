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
# Run `pynx nomad generate-metainfo --nxdl NXsource` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Source"]


class Source(Component):
    """
    Radiation source emitting a beam.

    Examples include particle sources (electrons, neutrons, protons) or sources
    for electromagnetic radiation (photons). This base class can also be used
    to describe neutron or x-ray storage ring/facilities.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsource",
            category="base",
        ),
    )

    notes = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "any source/facility related messages/events that occurred during "
            "the experiment"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="notes",
            name_type="specified",
            optionality="optional",
        ),
    )
    bunch_pattern = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=(
            "For storage rings, description of the bunch pattern. This is useful "
            "to describe irregular bunch patterns."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="bunch_pattern",
            name_type="specified",
            optionality="optional",
        ),
    )
    pulse_shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("source pulse shape"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_shape",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        description=('"Engineering" location of source.'),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the source and NXoff_geometry to describe its shape instead",
        ),
    )
    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=True,
        variable=True,
        description=("The size and position of an aperture inside the source."),
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        description=("Individual electromagnetic lenses inside the source."),
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=("Deflectors inside the source."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("The wavelength or energy distribution of the source"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="distribution",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Effective distance from sample Distance as seen by radiation from "
            "sample. This number should be negative to signify that it is "
            "upstream of the sample."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-name-field"
        ],
        description=("Name of source"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-name-short-name-attribute"
        ],
        description=("short name for source, perhaps the acronym"),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-type-field"
        ],
        description=(
            "type of radiation source (pick one from the enumerated list and "
            "spell exactly)"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-probe-field"
        ],
        description=(
            "type of radiation probe (pick one from the enumerated list and "
            "spell exactly)"
        ),
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        description=("Source power"),
        a_nexus_field=NeXusField(
            name="power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "watt"},
    )
    emittance_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-emittance-x-field"
        ],
        dimensionality="[length] * [angle]",
        unit="m * radian",
        description=("Source emittance (nm-rad) in X (horizontal) direction."),
        a_nexus_field=NeXusField(
            name="emittance_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_EMITTANCE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m * radian"},
    )
    emittance_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-emittance-y-field"
        ],
        dimensionality="[length] * [angle]",
        unit="m * radian",
        description=("Source emittance (nm-rad) in Y (horizontal) direction."),
        a_nexus_field=NeXusField(
            name="emittance_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_EMITTANCE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m * radian"},
    )
    sigma_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-sigma-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("particle beam size in x"),
        a_nexus_field=NeXusField(
            name="sigma_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    sigma_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-sigma-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("particle beam size in y"),
        a_nexus_field=NeXusField(
            name="sigma_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    flux = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-flux-field"
        ],
        dimensionality="1 / [time] / [length] ** 2",
        unit="1 / second / m ** 2",
        description=("Source intensity/area (example: s-1 cm-2)"),
        a_nexus_field=NeXusField(
            name="flux",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FLUX",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / second / m ** 2"},
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Source energy. Typically, this would be the energy of the emitted "
            "beam. For storage rings, this would be the particle beam energy."
        ),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("Accelerator, X-ray tube, or storage ring current"),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("Accelerator voltage"),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("Frequency of pulsed source"),
        a_nexus_field=NeXusField(
            name="frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    period = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-period-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Period of pulsed source"),
        a_nexus_field=NeXusField(
            name="period",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PERIOD",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    target_material = Quantity(
        type=MEnum(["Ta", "W", "depleted_U", "enriched_U", "Hg", "Pb", "C"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-target-material-field"
        ],
        description=("Pulsed source target material"),
        a_nexus_field=NeXusField(
            name="target_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Ta", "W", "depleted_U", "enriched_U", "Hg", "Pb", "C"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    number_of_bunches = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-number-of-bunches-field"
        ],
        description=("For storage rings, the number of bunches in use."),
        a_nexus_field=NeXusField(
            name="number_of_bunches",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    bunch_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-bunch-length-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("For storage rings, temporal length of the bunch"),
        a_nexus_field=NeXusField(
            name="bunch_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    bunch_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-bunch-distance-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("For storage rings, time between bunches"),
        a_nexus_field=NeXusField(
            name="bunch_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    pulse_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-pulse-width-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("temporal width of source pulse"),
        a_nexus_field=NeXusField(
            name="pulse_width",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-mode-field"
        ],
        description=("source operating mode"),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Single Bunch", "Multi Bunch"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    top_up = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-top-up-field"
        ],
        description=("Is the synchrotron operating in top_up mode?"),
        a_nexus_field=NeXusField(
            name="top_up",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    last_fill = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-last-fill-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=(
            "For storage rings, the current at the end of the most recent injection."
        ),
        a_nexus_field=NeXusField(
            name="last_fill",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    last_fill__time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-last-fill-time-attribute"
        ],
        description=("date and time of the most recent injection."),
        a_nexus_attribute=NeXusAttribute(
            name="time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="last_fill",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The wavelength of the radiation emitted by the source."),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    pulse_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-pulse-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("For pulsed sources, the energy of a single pulse."),
        a_nexus_field=NeXusField(
            name="pulse_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    peak_power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-peak-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        description=(
            "For pulsed sources, the pulse energy divided by the pulse duration"
        ),
        a_nexus_field=NeXusField(
            name="peak_power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "watt"},
    )
    anode_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-anode-material-field"
        ],
        description=("Material of the anode (for X-ray tubes)."),
        a_nexus_field=NeXusField(
            name="anode_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    filament_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-filament-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("Filament current (for X-ray tubes)."),
        a_nexus_field=NeXusField(
            name="filament_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    emission_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-emission-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("Emission current of the generated beam."),
        a_nexus_field=NeXusField(
            name="emission_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    gas_pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-gas-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        description=("Gas pressure inside ionization source."),
        a_nexus_field=NeXusField(
            name="gas_pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "pascal"},
    )
    previous_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-previous-source-field"
        ],
        description=(
            "Single instance or list of instances of NXsource pointing to the "
            "sources from which a beam originated to reach this source. This can "
            "be used, for example, for secondary sources to describe which other "
            "source(s) they are derived from. An example is the white light "
            "source in transient absorption spectroscopy, which is a "
            "supercontinuum crystal that is pumped by a another laser. In case "
            "of a primary source, this field should not be filled."
        ),
        a_nexus_field=NeXusField(
            name="previous_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsource.html#nxsource-depends-on-field"
        ],
        description=(
            "The reference point of the source plane is its center in the x and "
            "y axis. The source is considered infinitely thin in the z axis. .. "
            "image:: source/source.png :width: 40%"
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
