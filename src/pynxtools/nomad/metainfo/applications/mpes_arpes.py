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
# Run `pynx nomad generate-metainfo --nxdl NXmpes_arpes` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.applications.mpes import Mpes
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MpesArpes"]


class MpesArpes(Mpes):
    """
    This is a general application definition for angle-resolved
    (multidimensional) photoelectron spectroscopy (ARPES).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmpes_arpes",
            category="application",
        ),
    )

    arpes_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesArpesGeometry",
        repeats=False,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesData",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXmpes_arpes"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmpes_arpes"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-method-field"
        ],
        description=(
            "Name of the experimental method. If applicable, this name should "
            "match the terms given by `Clause 11`_ of the `ISO 18115-1:2023`_ "
            "specification. Examples include: * angle-resolved photoelectron "
            "spectroscopy (ARPES) * time-resolved angle-resolved X-ray "
            "photoelectron spectroscopy (trARPES) * spin-resolved angle-resolved "
            "X-ray photoelectron spectroscopy (spin-ARPES) .. _ISO 18115-1:2023: "
            "https://www.iso.org/standard/74811.html .. _Clause 11: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:sec:11"
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
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


class MpesArpesArpesGeometry(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-arpes-geometry-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="arpes_geometry",
            name_type="specified",
            optionality="required",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-arpes-geometry-depends-on-field"
        ],
        description=(
            "Link to transformations defining an ARPES base coordinate system, "
            "which is defined such that the positive z-axis points towards the "
            "analyzer entry, and the x-axis lies within the beam/analyzer plane."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    situation = Quantity(
        type=MEnum(["vacuum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-situation-field"
        ],
        a_nexus_field=NeXusField(
            name="situation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["vacuum"],
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-depends-on-field"
        ],
        description=(
            "Reference to the end of the transformation chain, orienting the "
            "sample surface within the arpes_geometry coordinate system "
            "(sample_azimuth or anything depending on it)."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
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
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-signal-attribute"
        ],
        description=("There is a field named data that contains the signal."),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["data"],
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-axes-attribute"
        ],
        shape=["*"],
        description=(
            "There are three dimensions, one energy and two angular coordinates. "
            "Any coordinates that do not move, are represented by one point."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    energy_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-energy-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="energy_indices",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    angular0_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-angular0-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="angular0_indices",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    angular1_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-angular1-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="angular1_indices",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("Values on the energy axis."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
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
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="energy",
            enumeration=["kinetic", "binding"],
        ),
    )
    angular0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-angular0-field"
        ],
        dimensionality="[angle]",
        description=("Trace of the first angular axis."),
        a_nexus_field=NeXusField(
            name="angular0",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    angular1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-angular1-field"
        ],
        dimensionality="[angle]",
        description=(
            "Trace of the second axis. Could be linked from the respective "
            "``@reference`` field."
        ),
        a_nexus_field=NeXusField(
            name="angular1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-data-data-field"
        ],
        description=(
            "Represents a measurement of photoemission counts over a "
            "three-dimensional space where the varied axes are energy, and one "
            "or more angular coordinates. Axes traces should be linked to the "
            "actual encoder position in NXinstrument or calibrated axes in "
            "NXprocess."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="k_perpendicular",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
