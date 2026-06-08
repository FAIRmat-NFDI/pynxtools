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
# Run `pynx nomad generate-metainfo --nxdl NXamplifier` to regenerate.
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

__all__ = ["Amplifier"]


class Amplifier(Component):
    """
    Base classed definition for amplifier devices.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXamplifier",
            category="base",
        ),
    )

    hardware = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        description=("(IC, device) (NXmanufacturer?)"),
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="hardware",
            name_type="specified",
            optionality="optional",
        ),
    )

    classification = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-classification-field"
        ],
        description=("Type of the amplifier base on the response on frequency."),
        a_nexus_field=NeXusField(
            name="classification",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "low-pass",
                "high-pass",
                "band-pass",
                "band-stop",
                "broadband",
            ],
            open_enum=True,
        ),
    )
    num_of_channels = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-num-of-channels-field"
        ],
        description=("The number of preamplifier channels are assigned."),
        a_nexus_field=NeXusField(
            name="num_of_channels",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    active_channels = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-active-channels-field"
        ],
        description=(
            "The number of preamplifier channels are ready to be used. (array "
            "for active channels)"
        ),
        a_nexus_field=NeXusField(
            name="active_channels",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    openloop_amplification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-openloop-amplification-field"
        ],
        description=(
            "The output signal does not go through a feedback loop to adjust the "
            "amplification of the amplifier. (array for active channels)"
        ),
        a_nexus_field=NeXusField(
            name="openloop_amplification",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    signal_over_noise = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-signal-over-noise-field"
        ],
        description=(
            "The ratio of the amplitude of the target signal to the amplitude of "
            "the noise in the output signal of the amplifier. "
            "S/N=V_signal/V_noise. (array for active channels)"
        ),
        a_nexus_field=NeXusField(
            name="signal_over_noise",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    crosstalk_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-crosstalk-factor-field"
        ],
        dimensionality="[length] ** 2",
        description=(
            "The unwanted coupling between different channels (if active >1). In "
            "ideal amplifier, channels are independent of each other, But due to "
            "different resources sharing (e.g., same power supply, "
            "electromagnetic interference), there may have some unwanted "
            "coupling between different channels, which is called crosstalk."
        ),
        a_nexus_field=NeXusField(
            name="crosstalk_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="db",
        ),
    )
    crosstalk_compensation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-crosstalk-compensation-field"
        ],
        description=(
            "If measures are taken for reducing interferences between different "
            "signalling pathways."
        ),
        a_nexus_field=NeXusField(
            name="crosstalk_compensation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The spectrum of frequency it can amplify, from its lowest to "
            "highest frequency limits. If it is difference of the frequencies, "
            "please also provide :ref: `center_frequency "
            "</NXamplifier/center_frequency-field>`."
        ),
        a_nexus_field=NeXusField(
            name="bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    center_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-center-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=("The frequency in the middle of the bandwidth."),
        a_nexus_field=NeXusField(
            name="center_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    lower_cutoff_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-lower-cutoff-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The lower frequency point of the bandwidth where gain drops "
            "significantly (e.g., -3dB point)."
        ),
        a_nexus_field=NeXusField(
            name="lower_cutoff_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    upper_cutoff_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-upper-cutoff-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "The upper frequency point of the bandwidth where gain drops "
            "significantly (e.g., -3dB point)."
        ),
        a_nexus_field=NeXusField(
            name="upper_cutoff_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXamplifier.html#nxamplifier-gain-field"
        ],
        description=(
            "The ratio of the output signal to the input signal of the amplifier."
        ),
        a_nexus_field=NeXusField(
            name="gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
