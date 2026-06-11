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
# Run `pynx nomad generate-metainfo --nxdl NXbeam` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.transformations import Transformations

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Beam"]


class Beam(Object):
    """
    Properties of the neutron or X-ray beam at a given location.

    This group is intended to be referenced by beamline component groups within
    the :ref:`NXinstrument` group or by the :ref:`NXsample` group. This group
    is especially valuable in storing the results of instrument simulations in
    which it is useful to specify the beam profile, time distribution etc. at
    each beamline component. Otherwise, its most likely use is in the
    :ref:`NXsample` group in which it defines the results of the neutron
    scattering by the sample, e.g., energy transfer, polarizations. Finally,
    There are cases where the beam is considered as a beamline component and
    this group may be defined as a subgroup directly inside
    :ref:`NXinstrument`, in which case it is recommended that the position of
    the beam is specified by an :ref:`NXtransformations` group, unless the beam
    is at the origin (which is the sample).

    Note that ``incident_wavelength``, ``incident_energy``, and related fields
    can be a scalar values or arrays, depending on the use case. To support
    these use cases, the explicit dimensionality of these fields is not
    specified, but it can be inferred by the presence of and shape of
    accompanying fields, such as incident_wavelength_weights for a
    polychromatic beam.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXbeam",
            category="base",
            symbols={
                "nP": "Number of scan points.",
                "m": "Number of channels in the incident beam spectrum, if known",
                "c": "Number of moments representing beam divergence (x, y, xy, etc.)",
            },
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            "Distribution of beam with respect to relevant variable e.g. "
            "wavelength. This is mainly useful for simulations which need to "
            "store plottable information at each beamline component."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.BeamTransformations",
        repeats=True,
        variable=True,
        description=(
            "Direction (and location) for the beam. The location of the beam can "
            "be given by any point which it passes through as its offset "
            "attribute."
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance from sample. Note, it is recommended to use "
            "NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    incident_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=(
            "Energy carried by each particle of the beam on entering the given "
            "location. Several use cases are permitted, depending on the "
            "presence or absence of other ``incident_energy_X`` fields. The "
            "usage should follow that of :ref:`incident_wavelength "
            "</NXbeam/incident_wavelength-field>`."
        ),
        a_nexus_field=NeXusField(
            name="incident_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    incident_energy_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-energy-spread-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "The energy spread FWHM for the corresponding energy(ies) in "
            "incident_energy. The usage of this field should follow that of "
            ":ref:`incident_wavelength </NXbeam/incident_wavelength-field>`."
        ),
        a_nexus_field=NeXusField(
            name="incident_energy_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    incident_energy_weights = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-energy-weights-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Relative weights of the corresponding energies in "
            "``incident_energy``. The usage of this field should follow that of "
            ":ref:`incident_wavelength </NXbeam/incident_wavelength-field>`."
        ),
        a_nexus_field=NeXusField(
            name="incident_energy_weights",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    final_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=(
            "Energy carried by each particle of the beam on leaving the given location"
        ),
        a_nexus_field=NeXusField(
            name="final_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    energy_transfer = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-energy-transfer-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=("Change in particle energy caused by the beamline component"),
        a_nexus_field=NeXusField(
            name="energy_transfer",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    incident_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "In the case of a monochromatic beam this is the scalar wavelength. "
            "Several other use cases are permitted, depending on the presence or "
            "absence of other incident_wavelength_X fields. In the case of a "
            "polychromatic beam this is an array of length **m** of wavelengths, "
            "with the relative weights in ``incident_wavelength_weights``. In "
            "the case of a monochromatic beam that varies shot- to-shot, this is "
            "an array of wavelengths, one for each recorded shot. Here, "
            "``incident_wavelength_weights`` and incident_wavelength_spread are "
            "not set. In the case of a polychromatic beam that varies shot-to- "
            "shot, this is an array of length **m** with the relative weights in "
            "``incident_wavelength_weights`` as a 2D array. In the case of a "
            "polychromatic beam that varies shot-to- shot and where the channels "
            "also vary, this is a 2D array of dimensions **nP** by **m** (slow "
            "to fast) with the relative weights in "
            "``incident_wavelength_weights`` as a 2D array. Note, :ref:`variants "
            "<Design-Variants>` are a good way to represent several of these use "
            "cases in a single dataset, e.g. if a calibrated, single-value "
            "wavelength value is available along with the original spectrum from "
            "which it was calibrated. Wavelength on entering beamline component"
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    incident_wavelength_weights = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-wavelength-weights-field"
        ],
        description=(
            "In the case of a polychromatic beam this is an array of length "
            "**m** of the relative weights of the corresponding wavelengths in "
            "``incident_wavelength``. In the case of a polychromatic beam that "
            "varies shot-to- shot, this is a 2D array of dimensions **nP** by "
            "**m** (slow to fast) of the relative weights of the corresponding "
            "wavelengths in ``incident_wavelength``."
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength_weights",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    incident_wavelength_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-wavelength-spread-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The wavelength spread FWHM for the corresponding wavelength(s) in "
            "incident_wavelength. In the case of shot-to-shot variation in the "
            "wavelength spread, this is a 2D array of dimension **nP** by **m** "
            "(slow to fast) of the spreads of the corresponding wavelengths in "
            "incident_wavelength."
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength_spread",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    incident_beam_divergence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-beam-divergence-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*"],
        description=(
            "Beam crossfire in degrees parallel to the laboratory X axis The "
            "dimension **c** is a series of moments of that represent the "
            "standard uncertainty (e.s.d.) of the directions of of the beam. The "
            "first and second moments are in the XZ and YZ planes around the "
            "mean source beam direction, respectively. Further moments in **c** "
            "characterize co-variance terms, so the next moment is the product "
            "of the first two, and so on."
        ),
        a_nexus_field=NeXusField(
            name="incident_beam_divergence",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        description=(
            "Size of the beam entering this component. Note this represents a "
            "rectangular beam aperture, and values represent FWHM. If "
            "applicable, the first dimension shall represent the extent in the "
            "direction parallel to the azimuthal reference plane (by default it "
            "is [1,0,0]), and the second dimension shall be the normal to the "
            "reference plane (by default it is [0,1,0])."
        ),
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    final_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Wavelength on leaving beamline component"),
        a_nexus_field=NeXusField(
            name="final_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    incident_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-polarization-field"
        ],
        shape=["*", 2],
        description=("Polarization vector on entering beamline component"),
        a_nexus_field=NeXusField(
            name="incident_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    final_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-polarization-field"
        ],
        shape=["*", 2],
        description=("Polarization vector on leaving beamline component"),
        a_nexus_field=NeXusField(
            name="final_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    incident_polarization_stokes = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-incident-polarization-stokes-field"
        ],
        shape=["*", 4],
        description=(
            "Polarization vector on entering beamline component using Stokes "
            "notation The Stokes parameters are four components labelled I,Q,U,V "
            "or S_0,S_1,S_2,S_3. These are defined with the standard Nexus "
            "coordinate frame unless it is overridden by an NXtransformations "
            "field pointed to by a depends_on attribute. The last component, "
            "describing the circular polarization state, is positive for a "
            "right-hand circular state - that is the electric field vector "
            "rotates clockwise at the sample and over time when observed from "
            "the source. I (S_0) is the beam intensity (often normalized to 1). "
            "Q, U, and V scale linearly with the total degree of polarization, "
            "and indicate the relative magnitudes of the pure linear and "
            "circular orientation contributions. Q (S_1) is linearly polarized "
            "along the x axis (Q > 0) or y axis (Q < 0). U (S_2) is linearly "
            "polarized along the x==y axis (U > 0) or the -x==y axis (U < 0). V "
            "(S_3) is circularly polarized. V > 0 when the electric field vector "
            "rotates clockwise at the sample with respect to time when observed "
            "from the source; V < 0 indicates the opposite rotation."
        ),
        a_nexus_field=NeXusField(
            name="incident_polarization_stokes",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    final_polarization_stokes = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-polarization-stokes-field"
        ],
        shape=["*", 4],
        description=(
            "Polarization vector on leaving beamline component using Stokes "
            "notation (see incident_polarization_stokes)."
        ),
        a_nexus_field=NeXusField(
            name="final_polarization_stokes",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    final_wavelength_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-wavelength-spread-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Wavelength spread FWHM of beam leaving this component"),
        a_nexus_field=NeXusField(
            name="final_wavelength_spread",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    final_beam_divergence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-final-beam-divergence-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 2],
        description=("Divergence FWHM of beam leaving this component"),
        a_nexus_field=NeXusField(
            name="final_beam_divergence",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    flux = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-flux-field"
        ],
        dimensionality="1 / [time] / [length] ** 2",
        unit="1 / second / m ** 2",
        shape=["*"],
        description=("flux incident on beam plane area"),
        a_nexus_field=NeXusField(
            name="flux",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FLUX",
        ),
    )
    pulse_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-pulse-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("Energy of a single pulse at the given location."),
        a_nexus_field=NeXusField(
            name="pulse_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    average_power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-average-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        description=("Average power at the at the given location."),
        a_nexus_field=NeXusField(
            name="average_power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
    )
    fluence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-fluence-field"
        ],
        dimensionality="[mass] / [time] ** 2",
        unit="mJ/cm^2",
        description=("Incident energy fluence at the given location."),
        a_nexus_field=NeXusField(
            name="fluence",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="mJ/cm^2",
        ),
    )
    pulse_duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-pulse-duration-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("FWHM duration of the pulses at the given location."),
        a_nexus_field=NeXusField(
            name="pulse_duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    pulse_delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-pulse-delay-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Delay time between two pulses of a pulsed beam."),
        a_nexus_field=NeXusField(
            name="pulse_delay",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    pulse_delay__reference_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-pulse-delay-reference-beam-attribute"
        ],
        description=(
            "A reference to the beam in relation to which the delay is. This "
            "should be the path to another instance of ``NXbeam``. The use of "
            "this attribute should be similar to that of the :ref:`depends_on "
            "attribute </NXtransformations/AXISNAME@depends_on-attribute>`. in "
            "NXtransformations."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="reference_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="pulse_delay",
        ),
    )
    frog_trace = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-frog-trace-field"
        ],
        shape=["*", "*"],
        description=(
            "FROG (frequency-resolved optical gating) trace of the pulse. This "
            "is to be used for ultrashort laser pulses in a FROG "
            "(frequency-resolved optical gating) setup."
        ),
        a_nexus_field=NeXusField(
            name="frog_trace",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    frog_delays = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-frog-delays-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Horizontal axis of a FROG trace, i.e. delay. This is to be used for "
            "ultrashort laser pulses in a FROG (frequency-resolved optical "
            "gating) setup."
        ),
        a_nexus_field=NeXusField(
            name="frog_delays",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    frog_frequencies = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-frog-frequencies-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        shape=["*"],
        description=(
            "Vertical axis of a FROG trace, i.e. frequency. This is to be used "
            "for ultrashort laser pulses in a FROG (frequency-resolved optical "
            "gating) setup."
        ),
        a_nexus_field=NeXusField(
            name="frog_frequencies",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    chirp_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-chirp-type-field"
        ],
        description=("The type of chirp implemented"),
        a_nexus_field=NeXusField(
            name="chirp_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    chirp_GDD = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-chirp-gdd-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Group delay dispersion of the pulse for linear chirp"),
        a_nexus_field=NeXusField(
            name="chirp_GDD",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-depends-on-field"
        ],
        description=(
            "The NeXus coordinate system defines the Z axis to be along the "
            "nominal beam direction. This is the same as the McStas coordinate "
            "system (see :ref:`Design-CoordinateSystem`). However, the "
            "additional transformations needed to represent an altered beam "
            "direction can be provided using this depends_on field that contains "
            "the path to a NXtransformations group. This could represent "
            "redirection of the beam, or a refined beam direction."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
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


class BeamTransformations(Transformations):
    """
    Direction (and location) for the beam. The location of the beam can be
    given by any point which it passes through as its offset attribute.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    BEAMdirection = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-beamdirection-field"
        ],
        variable=True,
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Direction of beam vector, its value is ignored. If missing, then "
            "the beam direction is defined as [0,0,1] and passes through the "
            "origin. Note, this field should be referenced by the parent group's "
            "``depends_on`` field; also, as this field is a direction, its "
            "``transformation_type`` attribute should be omitted."
        ),
        a_nexus_field=NeXusField(
            name="BEAMdirection",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    BEAMdirection__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-beamdirection-vector-attribute"
        ],
        shape=[3],
        description=("Three values that define the direction of beam vector"),
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="BEAMdirection",
        ),
    )
    BEAMdirection__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-beamdirection-offset-attribute"
        ],
        shape=[3],
        description=(
            "Three values that define the location of a point through which the "
            "beam passes"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="BEAMdirection",
        ),
    )
    BEAMdirection__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-beamdirection-depends-on-attribute"
        ],
        description=(
            "Points to the path to a field defining the location on which this "
            'depends or the string "." for origin.'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="BEAMdirection",
        ),
    )
    reference_plane = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-reference-plane-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Direction of normal to reference plane used to measure azimuth "
            "relative to the beam, its value is ignored. This also defines the "
            "parallel and perpendicular components of the beam's polarization. "
            "If missing, then the reference plane normal is defined as [0,1,0]. "
            "Note, as this field is a direction, its ``transformation_type`` "
            "attribute should be omitted."
        ),
        a_nexus_field=NeXusField(
            name="reference_plane",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    reference_plane__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-reference-plane-vector-attribute"
        ],
        shape=[3],
        description=(
            "Three values that define the direction of reference plane normal"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="reference_plane",
        ),
    )
    reference_plane__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam-transformations-reference-plane-depends-on-attribute"
        ],
        description=(
            "Points to the path to a field defining the location on which this "
            'depends or the string "." for origin.'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="reference_plane",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
