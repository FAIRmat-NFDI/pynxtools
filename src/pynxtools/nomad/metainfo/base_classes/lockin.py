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
# Run `pynx nomad generate-metainfo --nx-class NXlockin` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Lockin"]


class Lockin(Object):
    """
    A base class definition for a lock-in amplifier.

    The lock-in amplifier information: the device is being used to extract a
    (potentially) very weak input signal buried in the noisy background, where
    the input signal has the same frequency (or its harmonic) as carrier signal
    or reference signal, using heterodyne detection.

    This method extracts the amplitude and phase shift between input signal and
    reference signal.

    In single phase lock-in amplifiers used in high signal-to-noise ratio
    applications, only the amplitude is measured and phase difference is set to
    zero.

    In two phase lock-in amplifiers used in low signal-to-noise ratio
    applications, both the amplitude and phase difference are measured.

    Fields with partial names like low_passN, high_passN, etc., can be repeated
    for each channel of the lockin amplifier. It is envisioned that these
    fields are named low_pass_0, low_pass_1, and so on.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXlockin",
            category="base",
        ),
    )

    hardware = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        description=(
            "Hardware manufacturers and type (product number) of lock-in amplifier."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="hardware",
            name_type="specified",
            optionality="optional",
        ),
    )

    bias_divider = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-bias-divider-field"
        ],
        description=(
            "Bias divider for lock-in channel. math: `Bias divider $= "
            "\\frac{V_{\\mathrm{ref}}}{V_{\\mathrm{ref}} + "
            "V_{\\mathrm{input}}}$`"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="bias_divider",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    modulation_status = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-modulation-status-field"
        ],
        description=("Switch the lock-in modulation on or off."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="modulation_status",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    modulation_signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-modulation-signal-field"
        ],
        description=(
            "Type of the modulation or reference signal, voltage | current | "
            "bias. The name of the current or voltage signal can be also "
            "specified according to their purpose (e.g., `bias` voltage)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="modulation_signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["voltage", "current", "bias"],
            open_enum=True,
        ),
    )
    modulation_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-modulation-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The frequency of the sine modulation that is used to modulate the "
            "signal in lock-in."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="modulation_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    reference_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-reference-amplitude-field"
        ],
        description=(
            "Amplitude of the reference signal for the lock-in amplifier. Unit "
            "could be NX_VOLTAGE or NX_CURRENT depending on the type of the "
            "reference signal."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="reference_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-reference-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=("Frequency of the reference signal for the lock-in amplifier."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="reference_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    reference_phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-reference-phase-field"
        ],
        dimensionality="[angle]",
        description=("Phase of the reference signal set in the lock-in amplifier."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="reference_phase",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    phase_difference = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-phase-difference-field"
        ],
        dimensionality="[angle]",
        description=(
            "Phase difference between the input signal and the reference signal. "
            "This is used in two phase lock-in amplifiers. In single phase "
            "lock-in amplifiers, this value is set to zero."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="phase_difference",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    demodulated_signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-demodulated-signal-field"
        ],
        description=(
            "Type of the demodulated signal, current | voltage | bias. The name "
            "of the current or voltage signal can be also specified according to "
            "their purpose (e.g., `bias` voltage)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="demodulated_signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["current", "voltage", "bias"],
            open_enum=True,
        ),
    )
    demodulated_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-demodulated-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=("The frequency of the demodulated signal."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="demodulated_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    frequency_modulation_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-frequency-modulation-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        description=("The bandwidth of the modulating signal."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="frequency_modulation_bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    phase_modulation_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-phase-modulation-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The bandwidth of the modulating signal over which modulated signal "
            "spreads."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="phase_modulation_bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    amplitude_modulation_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-amplitude-modulation-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The bandwidth of the modulating signal over which modulated signal "
            "spreads."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="amplitude_modulation_bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    demodulated_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-demodulated-amplitude-field"
        ],
        description=(
            "The amplitude of the demodulated signal. Unit could be NX_VOLTAGE "
            "or NX_CURRENT depending on the type of the demodulated signal."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="demodulated_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    demodulated_phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-demodulated-phase-field"
        ],
        dimensionality="[angle]",
        description=("The phase of the demodulated signal."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="demodulated_phase",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    demodulator_channels = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-demodulator-channels-field"
        ],
        description=("Comma separated list of the demodulator channels."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="demodulator_channels",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    low_passN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-low-passn-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "Frequency of the low-pass filter or cut-off frequency. Only signals "
            "below this frequency are passed through the filter. N is envisioned "
            "to represent the channel number e.g., low_pass1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="low_passN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    high_passN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-high-passn-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "Frequency of the high-pass filter or cut-off frequency. Only "
            "signals above this frequency are passed through the filter. N is "
            "envisioned to represent the channel number e.g., high_pass1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="high_passN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    lp_filter_orderN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-lp-filter-ordern-field"
        ],
        description=(
            "Order of the low-pass filter applied on the input or demodulated "
            "signals (X, Y). Reducing the bandwidth or increasing the order "
            "reduces noise on the demodulated signals, but increases settling "
            "and measurement times. N is envisioned to represent the channel "
            "number e.g., lp_filter_order1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lp_filter_orderN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    hp_filter_orderN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-hp-filter-ordern-field"
        ],
        description=(
            "Order of the high-pass filter applied on the input or demodulated "
            "signal. This is used mainly to suppress a DC component of the input "
            "signal noise. N is envisioned to represent the channel number e.g., "
            "hp_filter_order1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="hp_filter_orderN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    ref_offset_phaseN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-ref-offset-phasen-field"
        ],
        dimensionality="[angle]",
        description=(
            "An extra phase offset added to the reference signal in modulation "
            "step. N is envisioned to represent the channel number e.g., "
            "hp_filter_order1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ref_offset_phaseN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    harmonic_orderN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-harmonic-ordern-field"
        ],
        description=(
            "The reference signal can be a higher harmonic of the modulation "
            "signal. Here the order of the harmonic is stored. N is envisioned "
            "to represent the channel number e.g., harmonic_order1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="harmonic_orderN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    sensitivity_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-sensitivity-factor-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Ratio of output signal amplitude to input signal amplitude (V/V)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sensitivity_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    dc_offset_valueN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXlockin.html#nxlockin-dc-offset-valuen-field"
        ],
        description=(
            "The DC offset of the demodulated signal. This is used to remove the "
            "DC component from the demodulated signal. The same DC offset might "
            "be applied to the input signal in the modulation process. N is "
            "envisioned to represent the channel number e.g., dc_offset_value1."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="dc_offset_valueN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
