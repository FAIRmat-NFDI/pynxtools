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
# Run `pynx nomad generate-metainfo --nxdl NXspm_cantilever_oscillator` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmCantileverOscillator"]


class SpmCantileverOscillator(Object):
    """
    In generally speaking a cantilever resembles a leaf-spring which can be
    treated as a harmonic oscillator as a first approximation.

    Note: If any field data in this group comes in an array as input or output
    in the scan process they will be stored in NXdata in scan_control group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_cantilever_oscillator",
            category="base",
        ),
    )

    reference_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-reference-amplitude-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The reference amplitude (also called drive amplitude) of the "
            "cantilever. This is the amplitude of the cantilever oscillation "
            "when no external forces are acting on it. Note: At least one from "
            "reference_amplitude, reference_frequency, or reference_phase is "
            "expected."
        ),
        a_nexus_field=NeXusField(
            name="reference_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    reference_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-reference-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "The reference frequency (also called drive frequency or resonance "
            "frequency) of the cantilever. Note: At least one from "
            "reference_amplitude, reference_frequency, or reference_phase is "
            "expected."
        ),
        a_nexus_field=NeXusField(
            name="reference_frequency",
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
    reference_phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-reference-phase-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "The reference phase of the cantilever oscillator. Note: At least "
            "one from reference_amplitude, reference_frequency, or "
            "reference_phase is expected."
        ),
        a_nexus_field=NeXusField(
            name="reference_phase",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    frequency_harmonic = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-frequency-harmonic-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The harmonic (e.g., second harmonic of the fundamental frequency) "
            "frequency of the cantilever."
        ),
        a_nexus_field=NeXusField(
            name="frequency_harmonic",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    phase_shift = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-phase-shift-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "The phase difference between the reference signal of cantilever and "
            "response signal."
        ),
        a_nexus_field=NeXusField(
            name="phase_shift",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    frequency_shift = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-frequency-shift-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("Shift in the resonance frequency of the cantilever."),
        a_nexus_field=NeXusField(
            name="frequency_shift",
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
    frequency_cutoff = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-frequency-cutoff-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("The cutoff frequency of the cantilever."),
        a_nexus_field=NeXusField(
            name="frequency_cutoff",
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
    frequency_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-frequency-bandwidth-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("The bandwidth of the resonance frequency."),
        a_nexus_field=NeXusField(
            name="frequency_bandwidth",
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
    target_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-target-amplitude-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The target amplitude of the cantilever to scan on each scan point. "
            "This field is same as the reference amplitude in the non-contact "
            "mode."
        ),
        a_nexus_field=NeXusField(
            name="target_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    target_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-target-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "The target frequency of the cantilever to scan on each scan point. "
            "This field is same as the reference frequency in the non-contact "
            "mode"
        ),
        a_nexus_field=NeXusField(
            name="target_frequency",
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
    active_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-active-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("The active frequency of the cantilever to start the experiment."),
        a_nexus_field=NeXusField(
            name="active_frequency",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
