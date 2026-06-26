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
# Run `pynx nomad generate-metainfo --nxdl NXmpes` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.activity import Activity
from pynxtools.nomad.metainfo.base_classes.actuator import Actuator
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.collectioncolumn import Collectioncolumn
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.electron_detector import ElectronDetector
from pynxtools.nomad.metainfo.base_classes.electronanalyzer import Electronanalyzer
from pynxtools.nomad.metainfo.base_classes.energydispersion import Energydispersion
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.history import History
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.log import Log
from pynxtools.nomad.metainfo.base_classes.manipulator import Manipulator
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.pid_controller import PidController
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor
from pynxtools.nomad.metainfo.base_classes.source import Source
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
        categories=[ExperimentCategory],
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
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrument",
        repeats=True,
        variable=True,
        description=(
            "Description of the photoemission spectrometer and its individual "
            "parts. This concept is related to term `12.58`_ of the ISO "
            "18115-1:2023 standard. .. _12.58: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58"
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
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesTransmissionCorrection",
        repeats=False,
        description=(
            "In the transmission correction, each intensity measurement for "
            "electrons of a given kinetic energy is multiplied by the "
            "corresponding value in the relative_intensity field of the "
            "transmission_function. This calibration procedure is used to "
            "account for energy-dependent transmission efficiencies in certain "
            "lens modes."
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
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmpes"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXmpes",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="transitions",
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

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-user-name-field"
        ],
        description=("Name of the user."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="affiliation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrument(Instrument):
    """
    Description of the photoemission spectrometer and its individual parts.

    This concept is related to term `12.58`_ of the ISO 18115-1:2023 standard.

    .. _12.58:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    energy_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentEnergyResolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="energy_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )
    resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.resolution.Resolution",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )
    source_probe = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSourceProbe",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_probe",
            name_type="specified",
            optionality="recommended",
        ),
    )
    source_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSourcePump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    source_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSource_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )
    beam_probe = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentBeamProbe",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_probe",
            name_type="specified",
            optionality="required",
        ),
    )
    beam_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentBeamPump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    beam_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentBeam_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )
    electronanalyzer = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzer",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    manipulator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    pressure_gauge = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentPressureGauge",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_gauge",
            name_type="specified",
            optionality="recommended",
        ),
    )
    flood_gun = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentFloodGun",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="flood_gun",
            name_type="specified",
            optionality="optional",
        ),
    )
    monochromator_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentMonochromator_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentEnergyResolution(Resolution):
    """
    Overall energy resolution of the photoemission instrument.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-energy-resolution-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-energy-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="energy",
        ),
    )
    type = Quantity(
        type=MEnum(["estimated", "derived", "calibrated", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-energy-resolution-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["estimated", "derived", "calibrated", "other"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-energy-resolution-resolution-field"
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
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSourceProbe(Source):
    """
    The source used to generate the :ref:`beam_probe
    </NXmpes/ENTRY/INSTRUMENT/beam_probe-group>`.

    Properties refer strictly to parameters of the source, not of the output
    beam. For example, the energy of the source is not the optical power of the
    beam, but the energy of the electron beam in a synchrotron or similar.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_probe",
            name_type="specified",
            optionality="recommended",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSourceProbeDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "Synchrotron X-ray Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Free-Electron Laser",
                "Optical Laser",
                "UV Plasma Source",
                "Metal Jet X-ray",
                "HHG laser",
                "UV lamp",
                "Monochromatized electron source",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    associated_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-associated-beam-field"
        ],
        description=(
            "A reference to a beam emitted by this source. Should be named with "
            "the same suffix, e.g., for ``source_probe`` it should refer to "
            "``beam_probe``. Example: * "
            "/entry/instrument/source_probe/associated_beam = "
            "/entry/instrument/beam_probe"
        ),
        a_nexus_field=NeXusField(
            name="associated_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSourceProbeDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-probe-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSourcePump(Source):
    """
    The source used to generate the :ref:`beam_pump
    </NXmpes/ENTRY/INSTRUMENT/beam_pump-group>` in pump-probe experiments.

    Properties refer strictly to parameters of the source, not of the output
    beam.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSourcePumpDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
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
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    associated_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-associated-beam-field"
        ],
        description=(
            "A reference to a beam emitted by this source. Should be named with "
            "the same suffix, e.g., for ``source_pump`` it should refer to "
            "``beam_pump``. Example: * "
            "/entry/instrument/source_pump/associated_beam = "
            "/entry/instrument/beam_pump"
        ),
        a_nexus_field=NeXusField(
            name="associated_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSourcePumpDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-pump-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSource_TYPE(Source):
    """
    Any other source used to generate a beam.

    This group is to be used for any additional beams that are not described by
    :ref:`source_probe </NXmpes/ENTRY/INSTRUMENT/source_probe-group>` or
    :ref:`source_pump </NXmpes/ENTRY/INSTRUMENT/source_pump-group>`.

    Examples could be a low energy electron source for charge neutralization
    (see also :ref:`flood_gun </NXmpes/ENTRY/INSTRUMENT/flood_gun-group>`) or
    an additional laser source.

    Properties refer strictly to parameters of the source, not of the output
    beam.

    Note that the uppercase notation in ``source_TYPE`` means that multiple
    sources can be provided. The uppercase part can be substituted with any
    string that consists of alphanumeric characters, including both uppercase
    and lowercase letters from A to Z and numerical digits from 0 to 9. For
    example, in pump-probe experiments, it is possible to have both a
    ``source_laser`` and a ``source_electron``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentSource_TYPEDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
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
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    associated_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-associated-beam-field"
        ],
        description=(
            "A reference to a beam emitted by this source. Should be named with "
            "the same suffix, e.g., for ``source_laser`` it should refer to "
            "``beam_laser``. Example: * "
            "/entry/instrument/source_laser/associated_beam = "
            "/entry/instrument/beam_laser"
        ),
        a_nexus_field=NeXusField(
            name="associated_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentSource_TYPEDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-source-type-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentBeamProbe(Beam):
    """
    Properties of the probe beam at a given location.

    This is the beam that is used to facilitate the photoemission during MPES
    experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_probe",
            name_type="specified",
            optionality="required",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance between the point where the current NXbeam instance is "
            "evaluating the beam properties and the point where the beam "
            "interacts with the sample. For photoemission, the latter is the "
            "point where the the centre of the beam touches the sample surface."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    incident_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-incident-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="incident_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    incident_energy_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-incident-energy-spread-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="incident_energy_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    incident_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-incident-polarization-field"
        ],
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="incident_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    associated_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-probe-associated-source-field"
        ],
        description=(
            "The source that emitted this beam. Should be named with the same "
            "suffix, e.g., for ``beam_probe`` it should refer to "
            "``source_probe``. This should be specified if an associated source "
            "exists. Example: * /entry/instrument/beam_probe/associated_source = "
            "/entry/instrument/source_probe"
        ),
        a_nexus_field=NeXusField(
            name="associated_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentBeamPump(Beam):
    """
    Properties of the pump beam at a given location.

    In pump-probe experiments, this is the beam that excites the system,
    initiating a change in its state. It sets the timing for the experiment by
    defining time zero in a pump-probe setup.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance between the point where the current NXbeam instance is "
            "evaluating the beam properties and the point where the beam "
            "interacts with the sample. For photoemission, the latter is the "
            "point where the the centre of the beam touches the sample surface."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    incident_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-incident-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="incident_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    incident_energy_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-incident-energy-spread-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="incident_energy_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    incident_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-incident-polarization-field"
        ],
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="incident_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    associated_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-pump-associated-source-field"
        ],
        description=(
            "The source that emitted this beam. Should be named with the same "
            "suffix, e.g., for ``beam_pump`` it should refer to ``source_pump``. "
            "This should be specified if an associated source exists. Example: * "
            "/entry/instrument/beam_pump/associated_source = "
            "/entry/instrument/source_pump"
        ),
        a_nexus_field=NeXusField(
            name="associated_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentBeam_TYPE(Beam):
    """
    Properties of any other beam at a given location.

    This group is to be used for any additional beams that are not described by
    :ref:`beam_probe </NXmpes/ENTRY/INSTRUMENT/beam_probe-group>` or
    :ref:`beam_pump </NXmpes/ENTRY/INSTRUMENT/beam_pump-group>`.

    Should be named with the same suffix as ``source_TYPE``, e.g., for
    ``source_laser`` it should refer to ``beam_laser``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance between the point where the current NXbeam instance is "
            "evaluating the beam properties and the point where the beam "
            "interacts with the sample. For photoemission, the latter is the "
            "point where the the centre of the beam touches the sample surface."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    incident_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-incident-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="incident_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    incident_energy_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-incident-energy-spread-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="incident_energy_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    incident_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-incident-polarization-field"
        ],
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="incident_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    associated_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-beam-type-associated-source-field"
        ],
        description=(
            "The source that emitted this beam. Should be named with the same "
            "suffix, e.g., for ``beam_laser`` it should refer to "
            "``source_laser``. This should be specified if an associated source "
            "exists. Example: * /entry/instrument/beam_laser/associated_source = "
            "/entry/instrument/source_laser"
        ),
        a_nexus_field=NeXusField(
            name="associated_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzer(Electronanalyzer):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )
    energy_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerEnergyResolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="energy_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )
    collectioncolumn = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerCollectioncolumn",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    energydispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerEnergydispersion",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    electron_detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerElectronDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectron_detector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    work_function = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-work-function-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="work_function",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    fast_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-fast-axes-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="fast_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    slow_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-slow-axes-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="slow_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerEnergyResolution(Resolution):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energy-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="energy_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["estimated", "derived", "calibrated", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energy-resolution-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["estimated", "derived", "calibrated", "other"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energy-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="energy",
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energy-resolution-resolution-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerCollectioncolumn(Collectioncolumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    field_aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="field_aperture",
            name_type="specified",
            optionality="optional",
        ),
    )
    contrast_aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="contrast_aperture",
            name_type="specified",
            optionality="optional",
        ),
    )
    iris = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="iris",
            name_type="specified",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerCollectioncolumnDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    scheme = Quantity(
        type=MEnum(
            [
                "angular dispersive",
                "spatial dispersive",
                "momentum dispersive",
                "non-dispersive",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-scheme-field"
        ],
        description=("Scheme of the electron collection column."),
        a_nexus_field=NeXusField(
            name="scheme",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "angular dispersive",
                "spatial dispersive",
                "momentum dispersive",
                "non-dispersive",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    lens_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-lens-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="lens_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    projection = Quantity(
        type=MEnum(["real", "reciprocal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-projection-field"
        ],
        a_nexus_field=NeXusField(
            name="projection",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["real", "reciprocal"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerCollectioncolumnDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-collectioncolumn-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerEnergydispersion(Energydispersion):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    entrance_slit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="entrance_slit",
            name_type="specified",
            optionality="optional",
        ),
    )
    exit_slit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="exit_slit",
            name_type="specified",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerEnergydispersionDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    scheme = Quantity(
        type=MEnum(
            [
                "tof",
                "hemispherical",
                "double hemispherical",
                "cylindrical mirror",
                "display mirror",
                "retarding grid",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-scheme-field"
        ],
        a_nexus_field=NeXusField(
            name="scheme",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "tof",
                "hemispherical",
                "double hemispherical",
                "cylindrical mirror",
                "display mirror",
                "retarding grid",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    pass_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-pass-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Only one of ``pass_energy`` or ``drift_energy`` should be supplied. "
            "``pass_energy`` should be used when working with hemispherical "
            "analyzers."
        ),
        a_nexus_field=NeXusField(
            name="pass_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    drift_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-drift-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Only one of ``pass_energy`` or ``drift_energy`` should be supplied. "
            "``drift_energy`` should be used if a TOF is used in the energy "
            "dispersive part of the electron analyzer."
        ),
        a_nexus_field=NeXusField(
            name="drift_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy_scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-energy-scan-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="energy_scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "fixed_analyzer_transmission",
                "fixed_retardation_ratio",
                "fixed_energy",
                "snapshot",
                "dither",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerEnergydispersionDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-energydispersion-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerElectronDetector(ElectronDetector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectron_detector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerElectronDetectorDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )
    raw_data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentElectronanalyzerElectronDetectorRawData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="raw_data",
            name_type="specified",
            optionality="recommended",
        ),
    )

    amplifier_type = Quantity(
        type=MEnum(["MCP", "channeltron"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-amplifier-type-field"
        ],
        description=("Type of electron amplifier in the first amplification step."),
        a_nexus_field=NeXusField(
            name="amplifier_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["MCP", "channeltron"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    detector_type = Quantity(
        type=MEnum(
            ["DLD", "Phosphor+CCD", "Phosphor+CMOS", "ECMOS", "Anode", "Multi-anode"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-detector-type-field"
        ],
        description=("Description of the detector type."),
        a_nexus_field=NeXusField(
            name="detector_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "DLD",
                "Phosphor+CCD",
                "Phosphor+CMOS",
                "ECMOS",
                "Anode",
                "Multi-anode",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerElectronDetectorDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentElectronanalyzerElectronDetectorRawData(Data):
    """
    Contains the raw data collected by the detector before calibration. The
    data which is considered raw might change from experiment to experiment due
    to hardware pre-processing of the data. This group ideally collects the
    data with the lowest level of processing possible.

    Axes should be named according to the conventions defined below. Note that
    this list is a glossary with explicitly named axis names, which is only
    intended to cover the most common measurement axes and is therefore not
    complete. It is possible to add axes with other names at any time.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="raw_data",
            name_type="specified",
            optionality="recommended",
        ),
    )

    signal = Quantity(
        type=MEnum(["raw"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["raw"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="raw",
        ),
    )
    raw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-raw-field"
        ],
        description=("Raw data before calibration."),
        a_nexus_field=NeXusField(
            name="raw",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    pixel_x = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-pixel-x-field"
        ],
        description=("Detector pixel number in x direction."),
        a_nexus_field=NeXusField(
            name="pixel_x",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    pixel_y = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-pixel-y-field"
        ],
        description=("Detector pixel number in y direction."),
        a_nexus_field=NeXusField(
            name="pixel_y",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("(Un)calibrated energy axis."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy__type = Quantity(
        type=MEnum(["kinetic", "binding"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-energy-type-attribute"
        ],
        description=(
            "The energy can be either stored as kinetic or as binding energy."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="energy",
            enumeration=["kinetic", "binding"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    photon_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-photon-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "(Un)calibrated photon energy of the incoming probe beam. Could be a "
            "link to /entry/instrument/beam_probe/incident_energy."
        ),
        a_nexus_field=NeXusField(
            name="photon_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    kx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-kx-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "(Un)calibrated k-space coordinate in x direction. It is envisioned "
            "that the axes in momentum space are named ``kx``, ``ky``, and "
            "``kz``. Typically, the vectors in momentum space are defined such "
            "that ``kx`` and ``ky`` comprise the parallel component, while "
            "``kz`` is the perpendicular component. It is also possible to "
            "define ``k_parallel`` and ``k_perpendicular`` for the parallel and "
            "perpendicular momenta, respectively. Units are typically "
            "1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="kx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    ky = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-ky-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "(Un)calibrated k-space coordinate in y direction. For more "
            "information, see the definition of the :ref:`kx "
            "</NXmpes/ENTRY/INSTRUMENT/ELECTRONANALYZER/ELECTRON_DETECTOR/raw_data/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="ky",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    kz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-kz-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "(Un)calibrated k-space coordinate in z direction. For more "
            "information, see the definition of the :ref:`kx "
            "</NXmpes/ENTRY/INSTRUMENT/ELECTRONANALYZER/ELECTRON_DETECTOR/raw_data/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="kz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    k_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-k-parallel-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "(Un)calibrated parallel component in k-space. ``k_parallel`` and "
            ":ref:`k_perpendicular "
            "</NXmpes/ENTRY/INSTRUMENT/ELECTRONANALYZER/ELECTRON_DETECTOR/raw_data/k_perpendicular-field>` "
            "describe how the electron's wave vector ``k`` is split into "
            "components relative to the surface. ``k_parallel`` is the component "
            "of the electron's wave vector that is parallel to the surface. It "
            "is conserved during the photoemission process. This means that the "
            "electron's momentum along the surface inside the material is "
            "directly related to its measured momentum outside the material. "
            "Units are typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="k_parallel",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    k_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-k-perpendicular-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "(Un)calibrated perpendicular component in k-space. "
            "``k_perpendicular`` is the component that is normal (perpendicular) "
            "to the surface. It is not conserved during photoemission because "
            "the electron experiences a potential change when it exits the "
            "material into vacuum. To determine ``k_perpendicular`` inside the "
            "material, one typically needs to estimate the inner potential "
            ":math:`\\phi_0`, which accounts for the energy shift due to the "
            "material's work function and electronic structure. Units are "
            "typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="k_perpendicular",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    angular0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-angular0-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "First (un)calibrated angular coordinate. It is envisioned that the "
            "axes in angular space are named ``angular0`` and ``angular1``. The "
            "angular axes should be named in order of decreasing speed, i.e., "
            "``angular0`` should be the fastest scan axis and ``angular1`` "
            "should be the slow-axis angular coordinate. However, ``angular0`` "
            "may also be second slowest axis if the measurement is angularly "
            "integrated and ``angular1`` could also be the second fastest axis "
            "in the case of simultaneous dispersion in two angular dimensions."
        ),
        a_nexus_field=NeXusField(
            name="angular0",
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
    angular1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-angular1-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Second (un)calibrated angular coordinate. For more information, see "
            "the definition of the :ref:`angular0 "
            "</NXmpes/ENTRY/INSTRUMENT/ELECTRONANALYZER/ELECTRON_DETECTOR/raw_data/angular0-field>` "
            "axis. This is typically the slower scan axis compared to "
            "``angular0``."
        ),
        a_nexus_field=NeXusField(
            name="angular1",
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
    spatial0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-spatial0-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "First (un)calibrated spatial coordinate. It is envisioned that the "
            "axes in regular space are named ``spatial0`` and ``spatial1``. The "
            "spatial axes should be named in order of decreasing speed, i.e., "
            "``spatial0`` should be the fastest scan axis and `spatial1`` should "
            "be the slow-axis spatial coordinate. However, ``spatial`` may also "
            "be second slow axis if the measurement is spatially integrated and "
            "``spatial1`` could also be the second fast axis in the case of "
            "simultaneous dispersion in two spatial dimensions."
        ),
        a_nexus_field=NeXusField(
            name="spatial0",
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
    spatial1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-spatial1-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Second (un)calibrated spatial coordinate. For more information, see "
            "the definition of the :ref:`spatial0 "
            "</NXmpes/ENTRY/INSTRUMENT/ELECTRONANALYZER/ELECTRON_DETECTOR/raw_data/spatial0-field>` "
            "axis. This is typically the slower scan axis compared to "
            "``spatial0``."
        ),
        a_nexus_field=NeXusField(
            name="spatial1",
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
    delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-delay-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "(Un)calibrated delay time. This is to be used for time-resolved "
            "pump-probe experiments and describes the delay between "
            ":ref:`beam_pump </NXmpes/ENTRY/INSTRUMENT/beam_pump-group>` and "
            ":ref:`beam_probe </NXmpes/ENTRY/INSTRUMENT/beam_probe-group>`."
        ),
        a_nexus_field=NeXusField(
            name="delay",
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
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-electronanalyzer-electron-detector-raw-data-temperature-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "(Un)calibrated temperature axis in case of experiments where the "
            "temperature was scanned. This is typically the sample temperature "
            "and could be linked from "
            "/entry/sample/temperature_env/temperature_sensor/value."
        ),
        a_nexus_field=NeXusField(
            name="temperature",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulator(Manipulator):
    """
    Manipulator for positioning of the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    sample_heater = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorSampleHeater",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )
    cryostat = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorCryostat",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="cryostat",
            name_type="specified",
            optionality="optional",
        ),
    )
    drain_current_ammeter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorDrainCurrentAmmeter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="drain_current_ammeter",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_bias_voltmeter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorSampleBiasVoltmeter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltmeter",
            name_type="specified",
            optionality="recommended",
        ),
    )
    sample_bias_potentiostat = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorSampleBiasPotentiostat",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_bias_potentiostat",
            name_type="specified",
            optionality="recommended",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorTemperatureSensor(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-temperature-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-temperature-sensor-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-temperature-sensor-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="temperature",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-temperature-sensor-value-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorSampleHeater(Actuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )

    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorSampleHeaterPidController",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    actuation_target = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-actuation-target-field"
        ],
        a_nexus_field=NeXusField(
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="temperature",
        ),
    )
    output_heater_power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-output-heater-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        a_nexus_field=NeXusField(
            name="output_heater_power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_POWER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "watt"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorSampleHeaterPidController(PidController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-pid-controller-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-heater-pid-controller-setpoint-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        a_nexus_field=NeXusField(
            name="setpoint",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorCryostat(Actuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-cryostat-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="cryostat",
            name_type="specified",
            optionality="optional",
        ),
    )

    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorCryostatPidController",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-cryostat-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    actuation_target = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-cryostat-actuation-target-field"
        ],
        a_nexus_field=NeXusField(
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="temperature",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorCryostatPidController(PidController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-cryostat-pid-controller-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-cryostat-pid-controller-setpoint-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        a_nexus_field=NeXusField(
            name="setpoint",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorDrainCurrentAmmeter(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-drain-current-ammeter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="drain_current_ammeter",
            name_type="specified",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-drain-current-ammeter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement = Quantity(
        type=MEnum(["current"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-drain-current-ammeter-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["current"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="current",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-drain-current-ammeter-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorSampleBiasVoltmeter(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-voltmeter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sample_bias_voltmeter",
            name_type="specified",
            optionality="recommended",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-voltmeter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement = Quantity(
        type=MEnum(["voltage"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-voltmeter-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["voltage"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="voltage",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-voltmeter-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorSampleBiasPotentiostat(Actuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-potentiostat-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_bias_potentiostat",
            name_type="specified",
            optionality="recommended",
        ),
    )

    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentManipulatorSampleBiasPotentiostatPidController",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-potentiostat-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    actuation_target = Quantity(
        type=MEnum(["voltage"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-potentiostat-actuation-target-field"
        ],
        a_nexus_field=NeXusField(
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["voltage"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorSampleBiasPotentiostatPidController(PidController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-potentiostat-pid-controller-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-sample-bias-potentiostat-pid-controller-setpoint-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="setpoint",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentManipulatorDeviceInformation(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-manipulator-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentPressureGauge(Sensor):
    """
    Device to measure the gas pressure in the instrument.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_gauge",
            name_type="specified",
            optionality="recommended",
        ),
    )

    value_log = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentPressureGaugeValueLog",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="value_log",
            name_type="specified",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement = Quantity(
        type=MEnum(["pressure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["pressure"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="pressure",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-value-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        shape=["*"],
        description=(
            "In case of a single or averaged gas pressure measurement, this is "
            "the scalar gas pressure. It can also be an 1D array of measured "
            "pressures (without time stamps)."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_PRESSURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentPressureGaugeValueLog(Log):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-value-log-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="value_log",
            name_type="specified",
            optionality="optional",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-pressure-gauge-value-log-value-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        description=(
            "In the case of an experiment in which the gas pressure changes and "
            "is recorded, this is an array of length m of gas pressures."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_PRESSURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "pascal"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentFloodGun(Actuator):
    """
    Device to bring low-energy electrons to the sample for charge
    neutralization
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="flood_gun",
            name_type="specified",
            optionality="optional",
        ),
    )

    current_log = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesInstrumentFloodGunCurrentLog",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="current_log",
            name_type="specified",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    actuation_target = Quantity(
        type=MEnum(["current"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-actuation-target-field"
        ],
        a_nexus_field=NeXusField(
            name="actuation_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["current"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="current",
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=(
            "In case of a fixed or averaged electron current, this is the scalar "
            "current. It can also be an 1D array of output current (without time "
            "stamps)."
        ),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentFloodGunCurrentLog(Log):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-current-log-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="current_log",
            name_type="specified",
            optionality="optional",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-flood-gun-current-log-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=(
            "In the case of an experiment in which the electron current is "
            "changed and recorded with time stamps, this is an array of length m "
            "of current setpoints."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesInstrumentMonochromator_TYPE(Monochromator):
    """
    If any of the beams is monochromatized, an ``NXmonochromator`` can be used
    to describe the properties of the monochromator.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-monochromator-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-monochromator-type-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    associated_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-instrument-monochromator-type-associated-beam-field"
        ],
        description=(
            "A reference to a beam emitted by this source. Should be named with "
            "the same suffix, e.g., for ``monochromator_probe`` it should refer "
            "to ``beam_probe``. Example: * "
            "/entry/instrument/monochromator_probe/associated_beam = "
            "/entry/instrument/beam_probe"
        ),
        a_nexus_field=NeXusField(
            name="associated_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="energy",
        ),
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-axis-calibration-calibrated-axis-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=(
            "This is the calibrated energy axis to be used for data plotting."
        ),
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="energy",
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
        a_nexus_field=NeXusField(
            name="level",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="reference_peak",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    binding_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-binding-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "The binding energy (in units of eV) that the specified emission "
            "line appeared at, after adjusting the binding energy scale. This "
            "concept is related to term `12.16`_ of the ISO 18115-1:2023 "
            "standard. .. _12.16: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.16"
        ),
        a_nexus_field=NeXusField(
            name="binding_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-offset-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Offset between measured binding energy and calibrated binding "
            "energy of the emission line."
        ),
        a_nexus_field=NeXusField(
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-calibrated-axis-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=(
            "This is the calibrated energy axis to be used for data plotting. "
            "This could be a link to /entry/data/energy."
        ),
        a_nexus_field=NeXusField(
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesTransmissionCorrection(Calibration):
    """
    In the transmission correction, each intensity measurement for electrons of
    a given kinetic energy is multiplied by the corresponding value in the
    relative_intensity field of the transmission_function. This calibration
    procedure is used to account for energy-dependent transmission efficiencies
    in certain lens modes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="transmission_correction",
            name_type="specified",
            optionality="optional",
        ),
    )

    transmission_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesTransmissionCorrectionTransmissionFunction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission_function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesTransmissionCorrectionTransmissionFunction(Data):
    """
    Transmission function of the electron analyzer.

    The transmission function (TF) specifies the detection efficiency for
    electrons of different kinetic energy passing through the electron
    analyzer.

    This can be a link to
    /entry/instrument/electronanalyzer/transmission_function.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-transmission-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission_function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    signal = Quantity(
        type=MEnum(["relative_intensity"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-transmission-function-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["relative_intensity"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="relative_intensity",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-transmission-function-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    kinetic_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-transmission-function-kinetic-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        description=("Kinetic energy values"),
        a_nexus_field=NeXusField(
            name="kinetic_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    relative_intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-transmission-correction-transmission-function-relative-intensity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Relative transmission efficiency for the given kinetic energies"),
        a_nexus_field=NeXusField(
            name="relative_intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
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

    history = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleHistory",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name="history",
            name_type="specified",
            optionality="recommended",
        ),
    )
    temperature_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleTemperatureEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="recommended",
        ),
    )
    gas_pressure_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleGasPressureEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="gas_pressure_env",
            name_type="specified",
            optionality="recommended",
        ),
    )
    bias_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleBiasEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="bias_env",
            name_type="specified",
            optionality="recommended",
        ),
    )
    drain_current_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleDrainCurrentEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="drain_current_env",
            name_type="specified",
            optionality="optional",
        ),
    )
    flood_gun_current_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleFloodGunCurrentEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="flood_gun_current_env",
            name_type="specified",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-chemical-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-physical-form-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_nexus_field=NeXusField(
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleHistory(History):
    """
    A set of activities that occurred to the sample prior to/during
    photoemission experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-history-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name="history",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sample_preparation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes.MpesSampleHistorySamplePreparation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactivity",
            name="sample_preparation",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleHistorySamplePreparation(Activity):
    """
    Details about the sample preparation for the photoemission experiment (e.g.
    UHV cleaving, in-situ growth, sputtering/annealing, etc.).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-history-sample-preparation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactivity",
            name="sample_preparation",
            name_type="specified",
            optionality="recommended",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-history-sample-preparation-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-history-sample-preparation-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-history-sample-preparation-method-field"
        ],
        description=(
            "Details about the method of sample preparation before the "
            "photoemission experiment."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleTemperatureEnv(Environment):
    """
    Sample temperature (either controlled or just measured) and
    actuators/sensors controlling/measuring it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-temperature-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="recommended",
        ),
    )

    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    sample_heater = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )
    cryostat = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="cryostat",
            name_type="specified",
            optionality="optional",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-temperature-env-value-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the temperature. An example would be a room "
            "temperature experiment where the temperature is not actively "
            "measured, but rather estimated. Note that this method for recording "
            "the temperature is not advised, but using NXsensor and NXactuator "
            "is strongly recommended instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleGasPressureEnv(Environment):
    """
    Gas pressure surrounding the sample and actuators/sensors
    controlling/measuring it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-gas-pressure-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="gas_pressure_env",
            name_type="specified",
            optionality="recommended",
        ),
    )

    pressure_gauge = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_gauge",
            name_type="specified",
            optionality="recommended",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-gas-pressure-env-value-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the gas pressure around the sample. An example "
            "would be a UHV experiment where the gas pressure is not monitored. "
            "Note that this method for recording the gas pressure is not "
            "advised, but using NXsensor and NXactuator is strongly recommended "
            "instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleBiasEnv(Environment):
    """
    Bias of the sample with respect to analyzer ground and actuators/sensors
    controlling/measuring it.

    This concept is related to term `8.41`_ of the ISO 18115-1:2023 standard.

    .. _8.41:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:8.41
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-bias-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="bias_env",
            name_type="specified",
            optionality="recommended",
        ),
    )

    voltmeter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="voltmeter",
            name_type="specified",
            optionality="recommended",
        ),
    )
    potentiostat = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="potentiostat",
            name_type="specified",
            optionality="optional",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-bias-env-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the bias. Note that this method for recording the "
            "bias is not advised, but using NXsensor and NXactuator is strongly "
            "recommended instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleDrainCurrentEnv(Environment):
    """
    Drain current of the sample and sample holder.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-drain-current-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="drain_current_env",
            name_type="specified",
            optionality="optional",
        ),
    )

    ammeter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="ammeter",
            name_type="specified",
            optionality="recommended",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-drain-current-env-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the drain current. Note that this method for "
            "recording the drain current is not advised, but using NXsensor and "
            "NXactuator is strongly recommended instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesSampleFloodGunCurrentEnv(Environment):
    """
    Current of low-energy electrons to the sample (for charge neutralization)
    and actuators/sensors controlling/measuring it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-flood-gun-current-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="flood_gun_current_env",
            name_type="specified",
            optionality="optional",
        ),
    )

    flood_gun = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="flood_gun",
            name_type="specified",
            optionality="recommended",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-flood-gun-current-env-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the flood_gun_current. Note that this method for "
            "recording the flood gun current is not advised, but using NXsensor "
            "and NXactuator is strongly recommended instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
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
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["data"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="data",
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
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("Calibrated axis for the energy of the measured electrons."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy__type = Quantity(
        type=MEnum(["kinetic", "binding"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-type-attribute"
        ],
        description=(
            "The energy can be either stored as kinetic or as binding energy."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="energy",
            enumeration=["kinetic", "binding"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    energy_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="energy_indices",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    photon_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-photon-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Calibrated photon energy of the incoming probe beam. Could be a "
            "link to /entry/instrument/beam_probe/incident_energy."
        ),
        a_nexus_field=NeXusField(
            name="photon_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    kx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kx-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Calibrated k-space coordinate in x direction. It is envisioned that "
            "the axes in momentum space are named ``kx``, ``ky``, and ``kz``. "
            "Typically, the vectors in momentum space are defined such that "
            "``kx`` and ``ky`` comprise the parallel component, while ``kz`` is "
            "the perpendicular component. It is also possible to define "
            "``k_parallel`` and ``k_perp`` for the parallel and perpendicular "
            "momenta, respectively. Units are typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="kx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    ky = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-ky-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Calibrated k-space coordinate in y direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="ky",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    kz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kz-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Calibrated k-space coordinate in z direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="kz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    k_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-parallel-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
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
        a_nexus_field=NeXusField(
            name="k_parallel",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    k_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-perpendicular-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
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
        a_nexus_field=NeXusField(
            name="k_perpendicular",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )
    angular0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular0-field"
        ],
        dimensionality="[angle]",
        unit="radian",
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
        a_nexus_field=NeXusField(
            name="angular0",
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
    angular1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular1-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Second calibrated angular coordinate. For more information, see the "
            "definition of the :ref:`angular0 "
            "</NXmpes/ENTRY/DATA/angular0-field>` axis. This is typically the "
            "slower scan axis compared to ``angular0``."
        ),
        a_nexus_field=NeXusField(
            name="angular1",
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
    spatial0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial0-field"
        ],
        dimensionality="[length]",
        unit="m",
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
        a_nexus_field=NeXusField(
            name="spatial0",
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
    spatial1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial1-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Second calibrated spatial coordinate. For more information, see the "
            "definition of the :ref:`spatial0 "
            "</NXmpes/ENTRY/DATA/spatial0-field>` axis. This is typically the "
            "slower scan axis compared to ``spatial0``."
        ),
        a_nexus_field=NeXusField(
            name="spatial1",
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
    delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-delay-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Calibrated pump-probe delay time. Could be a link to "
            "/entry/instrument/beam_pump/pulse_delay."
        ),
        a_nexus_field=NeXusField(
            name="delay",
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
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-temperature-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Calibrated temperature axis in case of experiments where the "
            "temperature was scanned. This is typically the sample temperature "
            "and could be linked from "
            "/entry/sample/temperature_env/temperature_sensor/value."
        ),
        a_nexus_field=NeXusField(
            name="temperature",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
