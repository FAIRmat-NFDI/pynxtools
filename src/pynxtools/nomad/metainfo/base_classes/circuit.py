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
# Run `pynx nomad generate-metainfo --nxdl NXcircuit` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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

__all__ = ["Circuit"]


class Circuit(Component):
    """
    Base class for documenting circuit devices.

    Electronic circuits are hardware components that connect several electronic
    components to achieve specific functionality, e.g. amplifying a voltage or
    convert a voltage to binary numbers, etc.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcircuit",
            category="base",
        ),
    )

    hardware = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        description=(
            "Hardware where the circuit is implanted; includes information about "
            "the hardware manufacturers and type (e.g. part number) All the "
            "elements below may be single numbers of an array of values with "
            "length N_channel describing multiple input and output channels."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="hardware",
            name_type="specified",
            optionality="optional",
        ),
    )
    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=False,
        description=("Calibration data for the circuit."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    components = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-components-field"
        ],
        description=(
            "List of components used in the circuit, e.g., resistors, "
            "capacitors, transistors or any other complex components."
        ),
        a_nexus_field=NeXusField(
            name="components",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    connections = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-connections-field"
        ],
        description=(
            "Description of how components are interconnected, including "
            "connection points and wiring."
        ),
        a_nexus_field=NeXusField(
            name="connections",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    power_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-power-source-field"
        ],
        description=(
            "Details of the power source for the circuit, including voltage and "
            "current ratings."
        ),
        a_nexus_field=NeXusField(
            name="power_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    signal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-signal-type-field"
        ],
        description=(
            "Type of signal (input signal) the circuit is designed to handle, "
            "e.g., analog, digital, mixed-signal."
        ),
        a_nexus_field=NeXusField(
            name="signal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    operating_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-operating-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "The operating frequency of the circuit, see also bandwidth, which "
            "is possibly but not necessarily centered around this frequency "
            "(e.g. running a 100 kHz bandwidth amplifier at low, audio "
            "frequencies 1 - 20,000 Hz)."
        ),
        a_nexus_field=NeXusField(
            name="operating_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("The bandwidth of the frequency response of the circuit."),
        a_nexus_field=NeXusField(
            name="bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    input_impedance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-input-impedance-field"
        ],
        flexible_unit=True,
        description=("Input impedance of the circuit."),
        a_nexus_field=NeXusField(
            name="input_impedance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    output_impedance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-output-impedance-field"
        ],
        flexible_unit=True,
        description=("Output impedance of the circuit."),
        a_nexus_field=NeXusField(
            name="output_impedance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-gain-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Gain of the circuit, if applicable, usually all instruments have a "
            "gain which might be important or not."
        ),
        a_nexus_field=NeXusField(
            name="gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    noise_level = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-noise-level-field"
        ],
        flexible_unit=True,
        description=(
            "Root-mean-square (RMS) noise level (in current or voltage) in the "
            "circuit in voltage or current."
        ),
        a_nexus_field=NeXusField(
            name="noise_level",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    temperature_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-temperature-range-field"
        ],
        flexible_unit=True,
        description=("Operating temperature range of the circuit."),
        a_nexus_field=NeXusField(
            name="temperature_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-offset-field"
        ],
        flexible_unit=True,
        description=("Offset value for current or voltage."),
        a_nexus_field=NeXusField(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    output_channels = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-output-channels-field"
        ],
        description=(
            "Number of output channels connected to this circuit. Most probably "
            "N_channel."
        ),
        a_nexus_field=NeXusField(
            name="output_channels",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    output_signal = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-output-signal-field"
        ],
        flexible_unit=True,
        description=("Type of output signal, e.g., voltage, current, digital."),
        a_nexus_field=NeXusField(
            name="output_signal",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    power_consumption = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-power-consumption-field"
        ],
        flexible_unit=True,
        description=("Power consumption of the circuit per unit time."),
        a_nexus_field=NeXusField(
            name="power_consumption",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    status_indicators = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-status-indicators-field"
        ],
        description=(
            "Status indicators for the circuit, e.g., LEDs, display readouts."
        ),
        a_nexus_field=NeXusField(
            name="status_indicators",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    protection_features = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-protection-features-field"
        ],
        description=(
            "Protection features built into the circuit, e.g., overvoltage "
            "protection, thermal shutdown."
        ),
        a_nexus_field=NeXusField(
            name="protection_features",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    acquisition_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-acquisition-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Updated rate for several processes using the input signal, e.g., "
            "History Graph, the circuit uses for any such process."
        ),
        a_nexus_field=NeXusField(
            name="acquisition_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    output_slew_rate = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcircuit.html#nxcircuit-output-slew-rate-field"
        ],
        description=(
            "The rate at which the signal changes when ramping from the starting value."
        ),
        a_nexus_field=NeXusField(
            name="output_slew_rate",
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
