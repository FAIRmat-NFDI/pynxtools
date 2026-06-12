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
from pynxtools.nomad.metainfo.applications.mpes import (
    Mpes,
    MpesData,
    MpesInstrument,
    MpesSample,
)
from pynxtools.nomad.metainfo.base_classes.aperture import Aperture
from pynxtools.nomad.metainfo.base_classes.collectioncolumn import Collectioncolumn
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.electronanalyzer import Electronanalyzer
from pynxtools.nomad.metainfo.base_classes.energydispersion import Energydispersion
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution
from pynxtools.nomad.metainfo.base_classes.transformations import Transformations

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
        categories=[ExperimentCategory],
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
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrument",
        repeats=True,
        variable=True,
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


class MpesArpesInstrument(MpesInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    electronanalyzer = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzer",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesInstrumentElectronanalyzer(Electronanalyzer):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    angularN_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzerAngularN_resolution",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="angularN_resolution",
            name_type="partial",
            optionality="recommended",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzerTransformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="required",
        ),
    )
    collectioncolumn = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzerCollectioncolumn",
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
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzerEnergydispersion",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-depends-on-field"
        ],
        description=(
            "Reference to the last transformation describing the orientation of "
            "the analyzer relative to the beam, e.g. "
            "transformations/analyzer_elevation."
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


class MpesArpesInstrumentElectronanalyzerAngularN_resolution(Resolution):
    """
    Analyzer angular resolution along the Nth angular axis. Create one such
    entry per relevant angular axis, corresponding to the angular axes in
    NXdata. For hemispherical analyzers, angular0_resolution corresponds to the
    direction along the analyzer slit, and angular1_resolution to the one
    perpendicular to it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-angularn-resolution-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="angularN_resolution",
            name_type="partial",
            optionality="recommended",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-angularn-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["angle"],
        ),
    )
    type = Quantity(
        type=MEnum(["estimated", "derived", "calibrated", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-angularn-resolution-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["estimated", "derived", "calibrated", "other"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-angularn-resolution-resolution-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesInstrumentElectronanalyzerTransformations(Transformations):
    """
    Set of transformations, describing the relative orientation of the analyzer
    with respect to the beam coordinate system (.).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="required",
        ),
    )

    analyzer_rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-rotation-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation about the analyzer lens axis. Its zero reference is "
            "defined such that the angular0 axis is increasing towards the "
            "positive y axis (analyzer slit vertical)."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    analyzer_rotation__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-rotation-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_rotation",
            enumeration=["rotation"],
        ),
    )
    analyzer_rotation__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-rotation-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_rotation",
        ),
    )
    analyzer_rotation__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-rotation-depends-on-attribute"
        ],
        description=(
            "Path to a transformation that places the analyzer origin system "
            "into the arpes_geometry coordinate system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_rotation",
        ),
    )
    analyzer_elevation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-elevation-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Elevation of the effective analyzer acceptance area, e.g. realized "
            "by deflectors, or as one angle in a TOF detector. If a resolved "
            "angle, place the calibrated axis coordinates here."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_elevation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    analyzer_elevation__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-elevation-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_elevation",
            enumeration=["rotation"],
        ),
    )
    analyzer_elevation__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-elevation-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_elevation",
        ),
    )
    analyzer_elevation__depends_on = Quantity(
        type=MEnum(["analyzer_dispersion"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-elevation-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_elevation",
            enumeration=["analyzer_dispersion"],
        ),
    )
    analyzer_dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-dispersion-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "In-plane analyzer coordinate along a dispersive direction, e.g. "
            "along an analyzer slit. If a resolved angle, place the calibrated "
            "coordinates here."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_dispersion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    analyzer_dispersion__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-dispersion-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_dispersion",
            enumeration=["rotation"],
        ),
    )
    analyzer_dispersion__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-dispersion-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_dispersion",
        ),
    )
    analyzer_dispersion__depends_on = Quantity(
        type=MEnum(["analyzer_rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-transformations-analyzer-dispersion-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_dispersion",
            enumeration=["analyzer_rotation"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesInstrumentElectronanalyzerCollectioncolumn(Collectioncolumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-collectioncolumn-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    scheme = Quantity(
        type=MEnum(["angular dispersive", "non-dispersive"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-collectioncolumn-scheme-field"
        ],
        description=("Scheme of the electron collection column."),
        a_nexus_field=NeXusField(
            name="scheme",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["angular dispersive", "non-dispersive"],
        ),
    )
    angular_acceptance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-collectioncolumn-angular-acceptance-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="angular_acceptance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesInstrumentElectronanalyzerEnergydispersion(Energydispersion):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-energydispersion-group"
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
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesInstrumentElectronanalyzerEnergydispersionEntranceSlit",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="entrance_slit",
            name_type="specified",
            optionality="recommended",
        ),
    )

    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-energydispersion-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesInstrumentElectronanalyzerEnergydispersionEntranceSlit(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-energydispersion-entrance-slit-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="entrance_slit",
            name_type="specified",
            optionality="recommended",
        ),
    )

    shape = Quantity(
        type=MEnum(["straight slit", "curved slit"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-instrument-electronanalyzer-energydispersion-entrance-slit-shape-field"
        ],
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["straight slit", "curved slit"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesSample(MpesSample):
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

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mpes_arpes.MpesArpesSampleTransformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesSampleTransformations(Transformations):
    """
    Set of transformations, describing the relative orientation of the sample
    with respect to the arpes_geometry coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="required",
        ),
    )

    sample_azimuth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-azimuth-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation about the z axis (azimuthal rotation within the sample plane)."
        ),
        a_nexus_field=NeXusField(
            name="sample_azimuth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    sample_azimuth__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-azimuth-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_azimuth",
            enumeration=["rotation"],
        ),
    )
    sample_azimuth__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-azimuth-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_azimuth",
        ),
    )
    sample_azimuth__depends_on = Quantity(
        type=MEnum(["offset_azimuth"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-azimuth-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_azimuth",
            enumeration=["offset_azimuth"],
        ),
    )
    offset_azimuth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-azimuth-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Offset of azimuthal rotation."),
        a_nexus_field=NeXusField(
            name="offset_azimuth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    offset_azimuth__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-azimuth-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_azimuth",
            enumeration=["rotation"],
        ),
    )
    offset_azimuth__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-azimuth-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="offset_azimuth",
        ),
    )
    offset_azimuth__depends_on = Quantity(
        type=MEnum(["sample_tilt"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-azimuth-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_azimuth",
            enumeration=["sample_tilt"],
        ),
    )
    sample_tilt = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-tilt-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation about the x axis (typically a manipulator tilt)."),
        a_nexus_field=NeXusField(
            name="sample_tilt",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    sample_tilt__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-tilt-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_tilt",
            enumeration=["rotation"],
        ),
    )
    sample_tilt__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-tilt-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_tilt",
        ),
    )
    sample_tilt__depends_on = Quantity(
        type=MEnum(["offset_tilt"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-tilt-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_tilt",
            enumeration=["offset_tilt"],
        ),
    )
    offset_tilt = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-tilt-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Offset of tilt rotation."),
        a_nexus_field=NeXusField(
            name="offset_tilt",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    offset_tilt__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-tilt-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_tilt",
            enumeration=["rotation"],
        ),
    )
    offset_tilt__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-tilt-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="offset_tilt",
        ),
    )
    offset_tilt__depends_on = Quantity(
        type=MEnum(["sample_polar"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-tilt-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_tilt",
            enumeration=["sample_polar"],
        ),
    )
    sample_polar = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-polar-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation about the y axis (typically the long manipulator axis)."
        ),
        a_nexus_field=NeXusField(
            name="sample_polar",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    sample_polar__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-polar-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_polar",
            enumeration=["rotation"],
        ),
    )
    sample_polar__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-polar-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_polar",
        ),
    )
    sample_polar__depends_on = Quantity(
        type=MEnum(["offset_polar"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-sample-polar-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_polar",
            enumeration=["offset_polar"],
        ),
    )
    offset_polar = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-polar-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Offset of polar rotation."),
        a_nexus_field=NeXusField(
            name="offset_polar",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    offset_polar__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-polar-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_polar",
            enumeration=["rotation"],
        ),
    )
    offset_polar__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-polar-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="offset_polar",
        ),
    )
    offset_polar__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes_arpes.html#nxmpes_arpes-entry-sample-transformations-offset-polar-depends-on-attribute"
        ],
        description=(
            "Path to a transformation that places the sample surface into the "
            "origin of the arpes_geometry coordinate system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="offset_polar",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MpesArpesData(MpesData):
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
        unit="joule",
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
        unit="radian",
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
        unit="radian",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
