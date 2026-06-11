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
# Run `pynx nomad generate-metainfo --nxdl NXelectronanalyzer` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Electronanalyzer"]


class Electronanalyzer(Component):
    """
    Basic class for describing an electron analyzer.

    This concept is related to term `12.59`_ of the ISO 18115-1:2023 standard.

    .. _12.59:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.59
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXelectronanalyzer",
            category="base",
            symbols={
                "nfa": "Number of fast axes (axes acquired simultaneously, without scanning a\n                physical quantity)",
                "nsa": "Number of slow axes (axes acquired while scanning a physical quantity)",
                "n_transmission_function": "Number of data points in the transmission function.",
            },
        ),
    )

    energy_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerEnergyResolution",
        repeats=False,
        description=(
            "Energy resolution of the analyzer with the current setting. May be "
            "linked from an NXcalibration."
        ),
    )
    momentum_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerMomentumResolution",
        repeats=False,
        description=("Momentum resolution of the electron analyzer (FWHM)"),
    )
    angular_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerAngularResolution",
        repeats=False,
        description=("Angular resolution of the electron analyzer (FWHM)"),
    )
    spatial_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerSpatialResolution",
        repeats=False,
        description=(
            "Spatial resolution of the electron analyzer (Airy disk radius) This "
            "concept is related to term `10.14`_ of the ISO 18115-1:2023 "
            "standard. .. _10.14: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.15"
        ),
    )
    transmission_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerTransmissionFunction",
        repeats=False,
        description=(
            "Transmission function of the electron analyzer. The transmission "
            "function (TF) specifies the detection efficiency per solid angle "
            "for electrons of different kinetic energy passing through the "
            "electron analyzer. It depends on the spectrometer geometry as well "
            "as operation settings such as lens mode and pass energy. The "
            "transmission function is usually given as relative intensity vs. "
            "kinetic energy. The TF is used for calibration of the intensity "
            "scale in quantitative XPS. Without proper transmission correction, "
            "a comparison of results measured from the same sample using "
            "different operating modes for an instrument would show significant "
            "variations in signal intensity for the same kinetic energies. This "
            "concept is related to term `7.15`_ of the ISO 18115-1:2023 "
            "standard. .. _7.15: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:7.15"
        ),
    )
    collectioncolumn = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collectioncolumn.Collectioncolumn",
        repeats=True,
        variable=True,
        description=(
            "Describes the electron collection (spatial and momentum imaging) column"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    energydispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.energydispersion.Energydispersion",
        repeats=True,
        variable=True,
        description=("Describes the energy dispersion section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    spindispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spindispersion.Spindispersion",
        repeats=True,
        variable=True,
        description=("Describes the spin dispersion section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXspindispersion",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector.Detector",
        repeats=True,
        variable=True,
        description=("Describes the electron detector"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=(
            "Deflectors outside the main optics ensembles described by the subclasses"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        description=(
            "Individual lenses outside the main optics ensembles described by "
            "the subclasses"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
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
    resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.resolution.Resolution",
        repeats=True,
        variable=True,
        description=("Any other resolution not explicitly named in this base class."),
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-description-field"
        ],
        description=("Free text description of the type of the detector"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-name-field"
        ],
        description=("Name or model of the equipment"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_quantity__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-name-short-name-attribute"
        ],
        description=("Acronym or other shorthand name"),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )
    work_function = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-work-function-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Work function of the electron analyzer. The work function of a "
            "uniform surface of a conductor is the minimum energy required to "
            "remove an electron from the interior of the solid to a vacuum level "
            "immediately outside the solid surface. The kinetic energy :math:E_K "
            "of a photoelectron emitted from an energy level with binding energy "
            ":math:`E_B` below the Fermi level is given by :math:`E_K = h\\nu - "
            "E_B - W = h\\nu - E_B - e \\phi_{\\mathrm{sample}}`. Here, :math:`W "
            "= e \\phi_{\\mathrm{sample}}` is the work function of the sample "
            "surface, which is directly proportional to the potential difference "
            ":math:`\\phi_{\\mathrm{sample}}` between the electrochemical "
            "potential of electrons in the bulk and the electrostatic potential "
            "of an electron in the vacuum just outside the surface. In PES "
            "measurements, the sample and the spectrometer (with work function "
            ":math:`W_{\\mathrm{spectr.}} = e \\phi_{\\mathrm{spectr.}}`) are "
            "electrically connected and therefore their Fermi levels are "
            "aligned. Due to the difference in local vacuum level between the "
            "sample and spectrometer, there however exists an electric potential "
            "difference (contact potential) :math:`\\Delta\\phi = "
            "\\phi_{\\mathrm{sample}} - \\phi_{\\mathrm{spectr.}}`. The measured "
            "kinetic energy of a photoelectron in PES is therefore given by "
            ":math:`E_K^{\\mathrm{meas.}} = E_K + e\\Delta\\phi = h\\nu - E_B - "
            "e\\phi_{\\mathrm{spectr.}}`. Hence, the measured kinetic energy "
            ":math:`E_K^{\\mathrm{meas.}}` of a photoelectron is independent of "
            "the sample work function. Nonetheless, the work function "
            ":math:`\\phi_{\\mathrm{spectr.}}` needs to be known to accurately "
            "determine the binding energy scale."
        ),
        a_nexus_field=NeXusField(
            name="work_function",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    voltage_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-voltage-range-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=(
            "Voltage range of the power supply. This influences the noise of the "
            "supply and thereby the energy resolution."
        ),
        a_nexus_field=NeXusField(
            name="voltage_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    fast_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-fast-axes-field"
        ],
        shape=["*"],
        description=(
            "List of the axes that are acquired simultaneously by the detector. "
            "These refer only to the experimental variables recorded by the "
            "electron analyzer. Other variables such as temperature, manipulator "
            "angles etc. can be labeled as fast or slow in the data. The fast "
            "axes should be listed in order of decreasing speed if they describe "
            "the same physical quantity or different components of the same "
            "quantity (e.g., ['kx', 'ky'] or ['detector_x', 'detector_y']). "
            "However, axes representing different physical quantities (e.g., "
            "['energy', 'kx']) do not need to be ordered by speed. .. "
            'csv-table:: Examples :header: "Mode", "fast_axes", '
            '"slow_axes" "Hemispherical in ARPES mode", "[\'energy\', '
            '\'kx\']","" "Hemispherical with channeltron, sweeping energy '
            'mode", "", [\\"energy\\"] "Tof", "[\'energy\', \'kx\', '
            '\'ky\']","" "Momentum microscope, spin-resolved", "[\'energy\', '
            "'kx', 'ky']\", \"['spin up-down', 'spin left-right']\" Axes may be "
            "less abstract than this, i.e. ['detector_x', 'detector_y']. If "
            "energy_scan_mode=sweep, fast_axes: ['energy', 'kx']; slow_axes: "
            "['energy'] is allowed."
        ),
        a_nexus_field=NeXusField(
            name="fast_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    slow_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-slow-axes-field"
        ],
        shape=["*"],
        description=(
            "List of the axes that are acquired by scanning a physical "
            "parameter, listed in order of decreasing speed. See fast_axes for "
            "examples."
        ),
        a_nexus_field=NeXusField(
            name="slow_axes",
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


class ElectronanalyzerEnergyResolution(Resolution):
    """
    Energy resolution of the analyzer with the current setting. May be linked
    from an NXcalibration.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-energy-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="energy_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-energy-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["energy"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-energy-resolution-resolution-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Minimum distinguishable energy separation in the energy spectra. "
            "This concept is related to term `10.24`_ of the ISO 18115-1:2023 "
            "standard. .. _10.24: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.24"
        ),
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-energy-resolution-resolution-errors-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ElectronanalyzerMomentumResolution(Resolution):
    """
    Momentum resolution of the electron analyzer (FWHM)
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-momentum-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="momentum_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["momentum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-momentum-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["momentum"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-momentum-resolution-resolution-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-momentum-resolution-resolution-errors-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        a_nexus_field=NeXusField(
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ElectronanalyzerAngularResolution(Resolution):
    """
    Angular resolution of the electron analyzer (FWHM)
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-angular-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="angular_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-angular-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["angle"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-angular-resolution-resolution-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-angular-resolution-resolution-errors-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ElectronanalyzerSpatialResolution(Resolution):
    """
    Spatial resolution of the electron analyzer (Airy disk radius)

    This concept is related to term `10.14`_ of the ISO 18115-1:2023 standard.

    .. _10.14:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.15
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-spatial-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spatial_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["length"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-spatial-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["length"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-spatial-resolution-resolution-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-spatial-resolution-resolution-errors-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ElectronanalyzerTransmissionFunction(Data):
    """
    Transmission function of the electron analyzer.

    The transmission function (TF) specifies the detection efficiency per solid
    angle for electrons of different kinetic energy passing through the
    electron analyzer. It depends on the spectrometer geometry as well as
    operation settings such as lens mode and pass energy. The transmission
    function is usually given as relative intensity vs. kinetic energy.

    The TF is used for calibration of the intensity scale in quantitative XPS.
    Without proper transmission correction, a comparison of results measured
    from the same sample using different operating modes for an instrument
    would show significant variations in signal intensity for the same kinetic
    energies.

    This concept is related to term `7.15`_ of the ISO 18115-1:2023 standard.

    .. _7.15:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:7.15
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-transmission-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission_function",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=MEnum(["relative_intensity"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-transmission-function-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["relative_intensity"],
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-transmission-function-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    kinetic_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-transmission-function-kinetic-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=("Kinetic energy values"),
        a_nexus_field=NeXusField(
            name="kinetic_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    relative_intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectronanalyzer.html#nxelectronanalyzer-transmission-function-relative-intensity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Relative transmission efficiency for the given kinetic energies"),
        a_nexus_field=NeXusField(
            name="relative_intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
