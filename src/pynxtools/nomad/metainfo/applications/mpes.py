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
# Run `pynx nomad generate-metainfo --nx-class NXmpes` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Mpes"]


class Mpes(Entry):
    """
    This is the most general application definition for photoemission
    experiments.

    Groups and fields are named according to the `ISO 18115-1:2023`_
    specification as well as the `IUPAC Recommendations 2020`_.

    .. _ISO 18115-1:2023: https://www.iso.org/standard/74811.html .. _IUPAC
    Recommendations 2020: https://doi.org/10.1515/pac-2019-0404
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmpes",
            category="application",
            symbols={
                "n_transmission_function": "Number of data points in the transmission function."
            },
        ),
    )

    coordinate_system = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.coordinate_system.CoordinateSystem",
        repeats=True,
        variable=True,
        description=(
            "Description of one coordinate systems that are specific to the "
            "setup and the measurement geometry. Multiple coordinate systems can "
            "be used if necessary."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesUser",
        repeats=True,
        variable=True,
        description=(
            "Contact information of at least the user of the instrument or the "
            "investigator who performed this experiment. Adding multiple users "
            "if relevant is recommended."
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=True,
        variable=True,
        description=(
            "Description of the photoemission spectrometer and its individual "
            "parts. This concept is related to term `12.58`_ of the ISO "
            "18115-1:2023 standard. .. _12.58: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    energy_axis_calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesEnergyAxisCalibration",
        repeats=False,
        description=(
            "Calibration event on the energy axis. For XPS, the calibration "
            "should ideally be performed according to `ISO 15472:2010`_ "
            "specification. .. _ISO 15472:2010: "
            "https://www.iso.org/standard/74811.html"
        ),
    )
    AXIS_axis_calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesAXIS_axis_calibration",
        repeats=True,
        variable=True,
        description=(
            "Calibration event for one of the axes in the :ref:`NXdata "
            "</NXmpes/ENTRY/data-group>`. The naming of these calibrations "
            "should follow those in the :ref:`NXdata "
            "</NXmpes/ENTRY/data-group>`. For example, for the momentum axis "
            "``kx``, the corresponding calibration should be called "
            "``kx_axis_calibration``."
        ),
    )
    energy_referencing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesEnergyReferencing",
        repeats=False,
        description=(
            "For energy referencing, the measured energies are corrected for the "
            "charging potential (i.e., the electrical potential of the surface "
            "region of an insulating sample, caused by irradiation) such that "
            "those energies correspond to a sample with no surface charge. "
            "Usually, the energy axis is adjusted by shifting all energies "
            "uniformly until one well-defined emission line peak (or the Fermi "
            "edge) is located at a known _correct_ energy. This concept is "
            "related to term `12.74 ff.`_ of the ISO 18115-1:2023 standard. .. "
            "_12.74 ff.: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.74"
        ),
    )
    transmission_correction = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=False,
        description=(
            "In the transmission correction, each intensity measurement for "
            "electrons of a given kinetic energy is multiplied by the "
            "corresponding value in the relative_intensity field of the "
            "transmission_function. This calibration procedure is used to "
            "account for energy-dependent transmission efficiencies in certain "
            "lens modes."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="transmission_correction",
            name_type="specified",
            optionality="optional",
        ),
    )
    registration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.registration.Registration",
        repeats=True,
        variable=True,
        description=(
            "Describes the operations of image registration (i.e. affine "
            "transformations like rotations or translations)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXregistration",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    distortion = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.distortion.Distortion",
        repeats=True,
        variable=True,
        description=("Describes the operations of image distortion correction."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdistortion",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=True,
        variable=True,
        description=(
            "Any further calibration procedures. For example, a calibration "
            "event for the photoemission counts (e.g., by dividing by some base "
            "line intensity :math:`I_0`.)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    fit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit.Fit",
        repeats=True,
        variable=True,
        description=("Any fit procedures."),
        a_nexus_group=NeXusGroup(
            nx_class="NXfit",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesData",
        repeats=True,
        variable=True,
        description=(
            "The NXdata group containing a view on the measured data. This "
            "NXdata group contains a collection of the main relevant fields "
            "(axes). Axes should be named according to the conventions defined "
            "below. Note that this list is a glossary with explicitly named axis "
            "names, which is only intended to cover the most common measurement "
            "axes and is therefore not complete. It is possible to add axes with "
            "other names at any time. In NXmpes, it is recommended to provide an "
            "energy axis."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXmpes"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmpes"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-definition-version-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-title-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-start-time-field"
        ],
        description=(
            "Datetime of the start of the measurement. Should be an ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-end-time-field"
        ],
        description=(
            "Datetime of the end of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-method-field"
        ],
        description=(
            "Name of the experimental method. If applicable, this name should "
            "match the terms given by `Clause 11`_ of the `ISO 18115-1:2023`_ "
            "specification. Examples include: * X-ray photoelectron spectroscopy "
            "(XPS) * angle-resolved X-ray photoelectron spectroscopy (ARXPS) * "
            "ultraviolet photoelectron spectroscopy (UPS) * angle-resolved "
            "photoelectron spectroscopy (ARPES) * hard X-ray photoemission "
            "spectroscopy (HAXPES) * near ambient pressure X-ray photoelectron "
            "spectroscopy (NAPXPS) * photoelectron emission microscopy (PEEM) * "
            "electron spectroscopy for chemical analysis (ESCA) * time-resolved "
            "angle-resolved X-ray photoelectron spectroscopy (trARPES) * "
            "spin-resolved angle-resolved X-ray photoelectron spectroscopy "
            "(spin-ARPES) * momentum microscopy .. _ISO 18115-1:2023: "
            "https://www.iso.org/standard/74811.html .. _Clause 11: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:sec:11"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    transitions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transitions-field"
        ],
        description=(
            "Array of strings representing the electronic core levels and Auger "
            "transitions probed in this MPES experiment. In order for "
            "experiments to be comparable, the notation must follow a strict "
            "convention. **For core levels:** - The element symbol (chemical "
            "symbol) is written first. - It is followed by a whitespace and then "
            'the electronic level (e.g., "1s", "2p", "3d", etc.) - '
            "Fine-structure splitting levels must include the total angular "
            "momentum quantum number **J**, written as a fraction after the "
            'orbital label (e.g., "3d5/2", "4f7/2"). - When relevant, '
            "fine-structure levels should be specified. If multiple "
            "fine-structure levels are probed, they should either be given "
            'explicitly or the generic level (e.g., "3d", "4f") can be used. '
            'Examples of correct core level notation: - "C 1s" - "O 1s" - '
            '"Fe 2p" - "Fe 2p3/2" - "Fe 2p1/2" - "Au 4f" - "Au 4f5/2" '
            '- "Au 4f7/2" **For Auger transitions:** - The element symbol '
            "(chemical symbol) is written first. - It is followed by a "
            "whitespace and the Auger transitions, which can include: - Explicit "
            'transitions (e.g., "KLL", "LMM") without fine-structure '
            'splitting - Explicit transitions (e.g., "KL1L2", "LM1M2") with '
            "fine-structure splitting - Simplified valence notation (e.g., "
            '"KVV", "KLV"). - Combinations of the above (e.g. "KL1V"). '
            'Examples of correct Auger transition notation: - "C KLL" - "O '
            'KLL" - "O KVV" - "O KL1L2" **Additional Allowed Entries:** '
            "Besides specific core levels and Auger transitions, the following "
            'broader spectral regions can also be listed: - "Fermi Edge" - '
            '"Valence Band" - "Survey" **Incorrect Notation Examples (Do Not '
            'Use):** - "C1s" (missing space) - "O-1s" (incorrect separator) '
            '- "Fe2p" (missing space) - "Au4f7/2" (missing space) - '
            '"O-KVV" (incorrect separator) - "Fe 2p_3/2" (incorrect '
            'underscore) - "Fe 2p 3/2" (extra space between "p" and "3/2")'
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="transitions",
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


class MpesUser(User):
    """
    Contact information of at least the user of the instrument or the
    investigator who performed this experiment. Adding multiple users if
    relevant is recommended.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-user-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-user-name-field"
        ],
        description=("Name of the user."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    affiliation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-user-affiliation-field"
        ],
        description=(
            "Name of the affiliation of the user at the time when the experiment "
            "was performed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="affiliation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesEnergyAxisCalibration(Calibration):
    """
    Calibration event on the energy axis.

    For XPS, the calibration should ideally be performed according to `ISO
    15472:2010`_ specification.

    .. _ISO 15472:2010: https://www.iso.org/standard/74811.html
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-axis-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="energy_axis_calibration",
            name_type="specified",
            optionality="recommended",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-axis-calibration-physical-quantity-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-axis-calibration-calibrated-axis-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=(
            "This is the calibrated energy axis to be used for data plotting."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesAXIS_axis_calibration(Calibration):
    """
    Calibration event for one of the axes in the :ref:`NXdata
    </NXmpes/ENTRY/data-group>`.

    The naming of these calibrations should follow those in the :ref:`NXdata
    </NXmpes/ENTRY/data-group>`. For example, for the momentum axis ``kx``, the
    corresponding calibration should be called ``kx_axis_calibration``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-axis-axis-calibration-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="AXIS_axis_calibration",
            name_type="partial",
            optionality="optional",
        ),
    )

    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-axis-axis-calibration-calibrated-axis-field"
        ],
        shape=["*"],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesEnergyReferencing(Calibration):
    """
    For energy referencing, the measured energies are corrected for the
    charging potential (i.e., the electrical potential of the surface region of
    an insulating sample, caused by irradiation) such that those energies
    correspond to a sample with no surface charge. Usually, the energy axis is
    adjusted by shifting all energies uniformly until one well-defined emission
    line peak (or the Fermi edge) is located at a known _correct_ energy.

    This concept is related to term `12.74 ff.`_ of the ISO 18115-1:2023
    standard.

    .. _12.74 ff.:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.74
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="energy_referencing",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-physical-quantity-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
    )
    level = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-level-field"
        ],
        description=(
            "Electronic core or valence level that was used for the calibration. "
            "This should be single string defining the core or valence level "
            "that was used for energy referencing. The notation should be the "
            "same as the one described in the :ref:`NXmpes/ENTRY/transitions "
            "</NXmpes/ENTRY/transitions-field>` field."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="level",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    reference_peak = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-reference-peak-field"
        ],
        description=(
            "Reference peak that was used for the calibration. For example: "
            "adventitious carbon | C-C | metallic Au | elemental Si | Fermi edge "
            "| vacuum level"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="reference_peak",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    binding_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-binding-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "The binding energy (in units of eV) that the specified emission "
            "line appeared at, after adjusting the binding energy scale. This "
            "concept is related to term `12.16`_ of the ISO 18115-1:2023 "
            "standard. .. _12.16: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.16"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="binding_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-offset-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "Offset between measured binding energy and calibrated binding "
            "energy of the emission line."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-calibrated-axis-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=(
            "This is the calibrated energy axis to be used for data plotting. "
            "This could be a link to /entry/data/energy."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-name-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-identifier-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-chemical-formula-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-atom-types-field"
        ],
        description=(
            "Array of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-physical-form-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    situation = Quantity(
        type=MEnum(
            [
                "vacuum",
                "inert atmosphere",
                "oxidizing atmosphere",
                "reducing atmosphere",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-situation-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="situation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "vacuum",
                "inert atmosphere",
                "oxidizing atmosphere",
                "reducing atmosphere",
            ],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesData(Data):
    """
    The NXdata group containing a view on the measured data.

    This NXdata group contains a collection of the main relevant fields (axes).
    Axes should be named according to the conventions defined below. Note that
    this list is a glossary with explicitly named axis names, which is only
    intended to cover the most common measurement axes and is therefore not
    complete. It is possible to add axes with other names at any time.

    In NXmpes, it is recommended to provide an energy axis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=MEnum(["data"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-signal-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["data"],
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-data-field"
        ],
        description=(
            "Represents a measure of one- or more-dimensional photoemission "
            "counts, where the varied axis may be for example energy, momentum, "
            "spatial coordinate, pump-probe delay, spin index, temperature, etc. "
            "The axes traces should be linked to the actual encoder position in "
            "NXinstrument or calibrated axes in NXprocess (or classes inheriting "
            "from NXprocess)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("Calibrated axis for the energy of the measured electrons."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    energy__type = Quantity(
        type=MEnum(["kinetic", "binding"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-type-attribute"
        ],
        description=(
            "The energy can be either stored as kinetic or as binding energy."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["kinetic", "binding"],
            parent_field="energy",
        ),
    )
    energy_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-indices-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="energy_indices",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    photon_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-photon-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "Calibrated photon energy of the incoming probe beam. Could be a "
            "link to /entry/instrument/beam_probe/incident_energy."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="photon_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    kx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kx-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in x direction. It is envisioned that "
            "the axes in momentum space are named ``kx``, ``ky``, and ``kz``. "
            "Typically, the vectors in momentum space are defined such that "
            "``kx`` and ``ky`` comprise the parallel component, while ``kz`` is "
            "the perpendicular component. It is also possible to define "
            "``k_parallel`` and ``k_perp`` for the parallel and perpendicular "
            "momenta, respectively. Units are typically 1/angstrom."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="kx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    ky = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-ky-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in y direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ky",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    kz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kz-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in z direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="kz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    k_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-parallel-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated parallel component in k-space. ``k_parallel`` and "
            ":ref:`k_perpendicular </NXmpes/ENTRY/DATA/k_perpendicular-field>` "
            "describe how the electron's wave vector ``k`` is split into "
            "components relative to the surface. ``k_parallel`` is the component "
            "of the electron's wave vector that is parallel to the surface. It "
            "is conserved during the photoemission process. This means that the "
            "electron's momentum along the surface inside the material is "
            "directly related to its measured momentum outside the material. "
            "Units are typically 1/angstrom."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="k_parallel",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    k_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-perpendicular-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated perpendicular component in k-space. ``k_perpendicular`` "
            "is the component that is normal (perpendicular) to the surface. It "
            "is not conserved during photoemission because the electron "
            "experiences a potential change when it exits the material into "
            "vacuum. To determine ``k_perpendicular`` inside the material, one "
            "typically needs to estimate the inner potential :math:`V_0`, which "
            "accounts for the energy shift due to the material's work function "
            "and electronic structure. Units are typically 1/angstrom."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="k_perpendicular",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    angular0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular0-field"
        ],
        dimensionality="[angle]",
        description=(
            "First calibrated angular coordinate. It is envisioned that the axes "
            "in angular space are named ``angular0`` and ``angular1``. The "
            "angular axes should be named in order of decreasing speed, i.e., "
            "``angular0`` should be the fastest scan axis and ``angular1`` "
            "should be the slow-axis angular coordinate. However, ``angular0`` "
            "may also be second slow axis if the measurement is angularly "
            "integrated and ``angular1`` could also be the second fast axis in "
            "the case of simultaneous dispersion in two angular dimensions."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="angular0",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angular1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular1-field"
        ],
        dimensionality="[angle]",
        description=(
            "Second calibrated angular coordinate. For more information, see the "
            "definition of the :ref:`angular0 "
            "</NXmpes/ENTRY/DATA/angular0-field>` axis. This is typically the "
            "slower scan axis compared to ``angular0``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="angular1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    spatial0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial0-field"
        ],
        dimensionality="[length]",
        description=(
            "First calibrated spatial coordinate. It is envisioned that the axes "
            "in angular space are named ``spatial0`` and ``spatial1``. The "
            "spatial axes should be named in order of decreasing speed, i.e., "
            "``spatial0`` should be the fastest scan axis and `spatial1`` should "
            "be the slow-axis spatial coordinate. However, ``spatial`` may also "
            "be second slow axis if the measurement is spatially integrated and "
            "``spatial1`` could also be the second fast axis in the case of "
            "simultaneous dispersion in two spatial dimensions."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="spatial0",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    spatial1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial1-field"
        ],
        dimensionality="[length]",
        description=(
            "Second calibrated spatial coordinate. For more information, see the "
            "definition of the :ref:`spatial0 "
            "</NXmpes/ENTRY/DATA/spatial0-field>` axis. This is typically the "
            "slower scan axis compared to ``spatial0``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="spatial1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-delay-field"
        ],
        dimensionality="[time]",
        description=(
            "Calibrated pump-probe delay time. Could be a link to "
            "/entry/instrument/beam_pump/pulse_delay."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="delay",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-temperature-field"
        ],
        dimensionality="[time]",
        description=(
            "Calibrated temperature axis in case of experiments where the "
            "temperature was scanned. This is typically the sample temperature "
            "and could be linked from "
            "/entry/sample/temperature_env/temperature_sensor/value."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
