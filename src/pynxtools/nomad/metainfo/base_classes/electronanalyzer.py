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
# Run `pynx nomad generate-metainfo --nx-class NXelectronanalyzer` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.collectioncolumn import Collectioncolumn
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.deflector import Deflector
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.electromagnetic_lens import (
    ElectromagneticLens,
)
from pynxtools.nomad.metainfo.base_classes.energydispersion import Energydispersion
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution
from pynxtools.nomad.metainfo.base_classes.spindispersion import Spindispersion

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Electronanalyzer"]


class Electronanalyzer(BaseSection):
    """
    Basic class for describing an electron analyzer.

    This concept is related to term `12.59`_ of the ISO 18115-1:2023 standard.

    .. _12.59:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.59
    """

    m_def = Section(
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
        repeats=True,
    )
    momentum_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerMomentumResolution",
        repeats=True,
    )
    angular_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerAngularResolution",
        repeats=True,
    )
    spatial_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerSpatialResolution",
        repeats=True,
    )
    transmission_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerTransmissionFunction",
        repeats=True,
    )
    collectioncolumn = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerCollectioncolumn",
        repeats=True,
        variable=True,
    )
    energydispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerEnergydispersion",
        repeats=True,
        variable=True,
    )
    spindispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerSpindispersion",
        repeats=True,
        variable=True,
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerDetector",
        repeats=True,
        variable=True,
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerDeflector",
        repeats=True,
        variable=True,
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerElectromagneticLens",
        repeats=True,
        variable=True,
    )
    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerFabrication",
        repeats=True,
        variable=True,
    )
    resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.ElectronanalyzerResolution",
        repeats=True,
        variable=True,
    )

    description_field = Quantity(
        type=str,
        description=("Free text description of the type of the detector"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_field = Quantity(
        type=str,
        description=("Name or model of the equipment"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_field__short_name = Quantity(
        type=str,
        description=("Acronym or other shorthand name"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )
    work_function = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="work_function",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    voltage_range = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Voltage range of the power supply. This influences the noise of the "
            "supply and thereby the energy resolution."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="voltage_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    fast_axes = Quantity(
        type=str,
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="fast_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    slow_axes = Quantity(
        type=str,
        shape=["*"],
        description=(
            "List of the axes that are acquired by scanning a physical "
            "parameter, listed in order of decreasing speed. See fast_axes for "
            "examples."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="slow_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — one Section class per group defined in NXelectronanalyzer.
# These are referenced by the SubSections above via string FQNs and resolved
# lazily by NOMAD at __init_metainfo__() time.
# =============================================================================


class ElectronanalyzerEnergyResolution(Resolution):
    """
    Energy resolution of the analyzer with the current setting. May be linked
    from an NXcalibration.
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="energy_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["energy"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "Minimum distinguishable energy separation in the energy spectra. "
            "This concept is related to term `10.24`_ of the ISO 18115-1:2023 "
            "standard. .. _10.24: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.24"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    relative_resolution = Quantity(
        type=np.float64,
        description=(
            "Ratio of the energy resolution of the electron analyzer at a "
            "specified energy value to that energy value. This concept is "
            "related to term `10.7`_ of the ISO 18115-1:2023 standard. .. _10.7: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.7"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )


class ElectronanalyzerMomentumResolution(Resolution):
    """
    Momentum resolution of the electron analyzer (FWHM)
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="momentum_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["momentum"]),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["momentum"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        dimensionality="1 / [length]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        dimensionality="1 / [length]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )


class ElectronanalyzerAngularResolution(Resolution):
    """
    Angular resolution of the electron analyzer (FWHM)
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="angular_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["angle"]),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["angle"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        dimensionality="[angle]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        dimensionality="[angle]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )


class ElectronanalyzerSpatialResolution(Resolution):
    """
    Spatial resolution of the electron analyzer (Airy disk radius)

    This concept is related to term `10.14`_ of the ISO 18115-1:2023 standard.

    .. _10.14:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:10.15
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spatial_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["length"]),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["length"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        dimensionality="[length]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        dimensionality="[length]",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )


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
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission_function",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=MEnum(["relative_intensity"]),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["relative_intensity"],
        ),
    )
    axes = Quantity(
        type=MEnum([["kinetic_energy"]]),
        shape=["*"],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[["kinetic_energy"]],
        ),
    )
    kinetic_energy = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Kinetic energy values"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="kinetic_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    relative_intensity = Quantity(
        type=np.float64,
        dimensionality="dimensionless",
        shape=["*"],
        description=("Relative transmission efficiency for the given kinetic energies"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )


class ElectronanalyzerCollectioncolumn(Collectioncolumn):
    """
    Describes the electron collection (spatial and momentum imaging) column
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerEnergydispersion(Energydispersion):
    """
    Describes the energy dispersion section
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerSpindispersion(Spindispersion):
    """
    Describes the spin dispersion section
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspindispersion",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerDetector(Detector):
    """
    Describes the electron detector
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerDeflector(Deflector):
    """
    Deflectors outside the main optics ensembles described by the subclasses
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerElectromagneticLens(ElectromagneticLens):
    """
    Individual lenses outside the main optics ensembles described by the
    subclasses
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerFabrication(Fabrication):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class ElectronanalyzerResolution(Resolution):
    """
    Any other resolution not explicitly named in this base class.
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
