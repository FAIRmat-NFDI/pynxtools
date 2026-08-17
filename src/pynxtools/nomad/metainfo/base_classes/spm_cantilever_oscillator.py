# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXspm_cantilever_oscillator (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXspm_cantilever_oscillator` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.hdf5 import HDF5Reference
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
        flexible_unit=True,
        description=(
            "The electrical (voltage) or mechanical (displacement) amplitude of "
            "the reference (drive) signal used to oscillate the cantilever. It "
            "is typically the interaction force or electrical voltage applied to "
            "the excitation piezo that drives the cantilever at or near its "
            "resonance frequency. Note: At least one from reference_amplitude, "
            "reference_frequency, or reference_phase is expected."
        ),
        a_nexus_field=NeXusField(
            name="reference_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
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
    amplitude_setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-amplitude-setpoint-field"
        ],
        flexible_unit=True,
        description=(
            "The amplitude setpoint is a target or desired electrical or "
            "mechanical amplitude obtained in the feedback loop of the "
            "cantilever's piezo system. It is constantly compared to the RMS "
            "amplitude of the cantilever's oscillation to adjust the drive "
            "voltage and maintain a stable oscillation amplitude. This field is "
            "same as the reference amplitude in the non-contact mode."
        ),
        a_nexus_field=NeXusField(
            name="amplitude_setpoint",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    frequency_setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_oscillator.html#nxspm_cantilever_oscillator-frequency-setpoint-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "The frequency setpoint is the target or desired frequency of the "
            "cantilever. This field is same as the reference frequency in the "
            "non-contact mode"
        ),
        a_nexus_field=NeXusField(
            name="frequency_setpoint",
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
