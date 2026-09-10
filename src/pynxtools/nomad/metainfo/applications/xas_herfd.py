# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXxas_herfd (see
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
# Run `pynx nomad generate-metainfo --nxdl NXxas_herfd` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.xas import Xas, XasSample
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.crystal import Crystal
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.emission_line import EmissionLine
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.transformations import Transformations

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["XasHerfd"]


class XasHerfd(Xas):
    r"""
    High-energy resolution fluorescence detection (HERFD) is a particular case
    of partial fluorescence yield measured with a crystal analyzer spectrometer
    with an energy bandwidth of approximately 1-2 eV.

    The HERFD spectrum corresponds to a constant-emission-energy cut through
    the Resonant Inelastic X-ray Scattering (RIXS) plane. The spectral shape
    depends on the emission energy, making the emission line and emission
    energy mandatory metadata.

    The top-level :ref:`intensity </NXxas/ENTRY/intensity-field>` field stores
    the ratio :math:`I_f/I_0`, where :math:`I_f` is the fluorescence intensity
    diffracted by the crystal analyzer(s) and :math:`I_0` is the incident beam
    intensity. This ratio is proportional to the absorption coefficient:

    .. math:: \mu(E) \propto I_f/I_0

    The spectrometer uses Rowland circle geometry (Johann or Johansson type).
    Multiple crystal analyzers may be arranged at different horizontal angles
    around the sample to increase solid angle coverage.

    When the raw detector data and processing steps are available, they can be
    stored in the optional ``NXinstrument``, ``NXcollection``, and
    ``NXprocess`` groups, enabling full reproducibility of the data reduction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxas_herfd",
            category="application",
            symbols={
                "nEnergy": "Number of energy data points",
                "nAnalyzers": "Number of crystal analyzers in the spectrometer",
            },
        ),
    )

    emission_line = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdEmissionLine",
        repeats=False,
    )
    beamline_coordinate_system = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdBeamlineCoordinateSystem",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdSample",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrument",
        repeats=True,
        variable=True,
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdCollection",
        repeats=True,
        variable=True,
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdProcess",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXxas_herfd"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxas_herfd"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxas_herfd",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-intensity-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "The ratio :math:`I_f/I_0`, where :math:`I_f` is the fluorescence "
            "intensity diffracted by the crystal analyzer(s) and :math:`I_0` is "
            "the incident beam intensity."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    emission_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-emission-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("The emission energy at which the spectrometer is set."),
        a_nexus_field=NeXusField(
            name="emission_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    is_experimental = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-is-experimental-field"
        ],
        description=(
            "Specify if the data comes from an experiment. Use ``true`` for data "
            "acquired at a beamline or laboratory instrument, and ``false`` for "
            "spectra calculated/simulated using a computational tool, "
            "reconstructed from a linear combination of reference components, "
            "etc."
        ),
        a_nexus_field=NeXusField(
            name="is_experimental",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        shape=["*"],
        description=("The energy axis of the spectrum."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    intensity_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-intensity-errors-field"
        ],
        flexible_unit=True,
        description=("The errors associated with the intensity of the spectrum."),
        a_nexus_field=NeXusField(
            name="intensity_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class XasHerfdEmissionLine(EmissionLine):
    """
    The emission line at which the HERFD spectrum is measured.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-emission-line-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXemission_line",
            name="emission_line",
            name_type="specified",
            optionality="required",
        ),
    )

    name = Quantity(
        type=MEnum(
            [
                "K-L1",
                "K-L2",
                "K-L3",
                "K-M1",
                "K-M2",
                "K-M3",
                "K-M4",
                "K-M5",
                "K-N1",
                "K-N2",
                "K-N3",
                "K-N4",
                "K-N5",
                "K-N6",
                "K-N7",
                "K-O",
                "K-O1",
                "K-O2",
                "K-O3",
                "K-O4",
                "K-O5",
                "K-O6",
                "K-O7",
                "K-P",
                "K-P1",
                "K-P2",
                "K-P3",
                "K-P4",
                "K-P5",
                "L1-L2",
                "L1-L3",
                "L1-M1",
                "L1-M2",
                "L1-M3",
                "L1-M4",
                "L1-M5",
                "L1-N1",
                "L1-N2",
                "L1-N3",
                "L1-N4",
                "L1-N5",
                "L1-N6",
                "L1-N6,7",
                "L1-N7",
                "L1-O1",
                "L1-O2",
                "L1-O3",
                "L1-O4",
                "L1-O4,5",
                "L1-O5",
                "L1-O6",
                "L1-O7",
                "L1-P1",
                "L1-P2",
                "L1-P2,3",
                "L1-P3",
                "L1-P4",
                "L1-P5",
                "L2-L3",
                "L2-M1",
                "L2-M2",
                "L2-M3",
                "L2-M4",
                "L2-M5",
                "L2-N1",
                "L2-N2",
                "L2-N3",
                "L2-N4",
                "L2-N5",
                "L2-N6",
                "L2-N6,7",
                "L2-N7",
                "L2-O1",
                "L2-O2",
                "L2-O3",
                "L2-O4",
                "L2-O5",
                "L2-O6",
                "L2-O7",
                "L2-P1",
                "L2-P2",
                "L2-P2,3",
                "L2-P3",
                "L2-P4",
                "L2-P5",
                "L2-Q1",
                "L3-M1",
                "L3-M2",
                "L3-M3",
                "L3-M4",
                "L3-M5",
                "L3-N1",
                "L3-N2",
                "L3-N3",
                "L3-N4",
                "L3-N5",
                "L3-N6",
                "L3-N6,7",
                "L3-N7",
                "L3-O1",
                "L3-O2",
                "L3-O3",
                "L3-O4",
                "L3-O4,5",
                "L3-O5",
                "L3-O6",
                "L3-O7",
                "L3-P1",
                "L3-P2",
                "L3-P2,3",
                "L3-P3",
                "L3-P4",
                "L3-P4,5",
                "L3-P5",
                "L3-Q1",
                "M1-M2",
                "M1-M3",
                "M1-M4",
                "M1-M5",
                "M1-N1",
                "M1-N2",
                "M1-N3",
                "M1-N4",
                "M1-N5",
                "M1-N6",
                "M1-N7",
                "M1-O1",
                "M1-O2",
                "M1-O3",
                "M1-O4",
                "M1-O5",
                "M1-O6",
                "M1-O7",
                "M1-P1",
                "M1-P2",
                "M1-P3",
                "M1-P4",
                "M1-P5",
                "M2-M3",
                "M2-M4",
                "M2-M5",
                "M2-N1",
                "M2-N2",
                "M2-N3",
                "M2-N4",
                "M2-N5",
                "M2-N6",
                "M2-N7",
                "M2-O1",
                "M2-O2",
                "M2-O3",
                "M2-O4",
                "M2-O5",
                "M2-O6",
                "M2-O7",
                "M2-P1",
                "M2-P2",
                "M2-P3",
                "M2-P4",
                "M2-P5",
                "M3-M4",
                "M3-M5",
                "M3-N1",
                "M3-N2",
                "M3-N3",
                "M3-N4",
                "M3-N5",
                "M3-N6",
                "M3-N7",
                "M3-O1",
                "M3-O2",
                "M3-O3",
                "M3-O4",
                "M3-O5",
                "M3-O6",
                "M3-O7",
                "M3-P1",
                "M3-P2",
                "M3-P3",
                "M3-P4",
                "M3-P5",
                "M3-Q1",
                "M4-M5",
                "M4-N1",
                "M4-N2",
                "M4-N3",
                "M4-N4",
                "M4-N5",
                "M4-N6",
                "M4-N7",
                "M4-O1",
                "M4-O2",
                "M4-O3",
                "M4-O4",
                "M4-O5",
                "M4-O6",
                "M4-O7",
                "M4-P1",
                "M4-P2",
                "M4-P3",
                "M4-P4",
                "M4-P5",
                "M5-N1",
                "M5-N2",
                "M5-N3",
                "M5-N4",
                "M5-N5",
                "M5-N6",
                "M5-N7",
                "M5-O1",
                "M5-O2",
                "M5-O3",
                "M5-O4",
                "M5-O5",
                "M5-O6",
                "M5-O7",
                "M5-P1",
                "M5-P2",
                "M5-P3",
                "M5-P4",
                "M5-P5",
                "M4,5-N2,3",
                "N1-N2",
                "N1-N3",
                "N1-N4",
                "N1-N5",
                "N1-N6",
                "N1-N7",
                "N1-O1",
                "N1-O2",
                "N1-O3",
                "N1-O4",
                "N1-O5",
                "N1-O6",
                "N1-O7",
                "N1-P1",
                "N1-P2",
                "N1-P3",
                "N1-P4",
                "N1-P5",
                "N2-N3",
                "N2-N4",
                "N2-N5",
                "N2-N6",
                "N2-N7",
                "N2-O1",
                "N2-O2",
                "N2-O3",
                "N2-O4",
                "N2-O5",
                "N2-O6",
                "N2-O7",
                "N2-P1",
                "N2-P2",
                "N2-P3",
                "N2-P4",
                "N2-P5",
                "N3-N4",
                "N3-N5",
                "N3-N6",
                "N3-N7",
                "N3-O1",
                "N3-O2",
                "N3-O3",
                "N3-O4",
                "N3-O5",
                "N3-O6",
                "N3-O7",
                "N3-P1",
                "N3-P2",
                "N3-P3",
                "N3-P4",
                "N3-P5",
                "N4-N5",
                "N4-N6",
                "N4-N7",
                "N4-O1",
                "N4-O2",
                "N4-O3",
                "N4-O4",
                "N4-O5",
                "N4-O6",
                "N4-O7",
                "N4-P1",
                "N4-P2",
                "N4-P3",
                "N4-P4",
                "N4-P5",
                "N5-N6",
                "N5-N7",
                "N5-O1",
                "N5-O2",
                "N5-O3",
                "N5-O4",
                "N5-O5",
                "N5-O6",
                "N5-O7",
                "N5-P1",
                "N5-P2",
                "N5-P3",
                "N5-P4",
                "N5-P5",
                "N6-N7",
                "N6-O1",
                "N6-O2",
                "N6-O3",
                "N6-O4",
                "N6-O5",
                "N6-O6",
                "N6-O7",
                "N6-P1",
                "N6-P2",
                "N6-P3",
                "N6-P4",
                "N6-P5",
                "N7-O1",
                "N7-O2",
                "N7-O3",
                "N7-O4",
                "N7-O5",
                "N7-O6",
                "N7-O7",
                "N7-P1",
                "N7-P2",
                "N7-P3",
                "N7-P4",
                "N7-P5",
                "O1-O2",
                "O1-O3",
                "O1-O4",
                "O1-O5",
                "O1-O6",
                "O1-O7",
                "O1-P1",
                "O1-P2",
                "O1-P3",
                "O1-P4",
                "O1-P5",
                "O2-O3",
                "O2-O4",
                "O2-O5",
                "O2-O6",
                "O2-O7",
                "O2-P1",
                "O2-P2",
                "O2-P3",
                "O2-P4",
                "O2-P5",
                "O3-O4",
                "O3-O5",
                "O3-O6",
                "O3-O7",
                "O3-P1",
                "O3-P2",
                "O3-P3",
                "O3-P4",
                "O3-P5",
                "O4-O5",
                "O4-O6",
                "O4-O7",
                "O4-P1",
                "O4-P2",
                "O4-P3",
                "O4-P4",
                "O4-P5",
                "O5-O6",
                "O5-O7",
                "O5-P1",
                "O5-P2",
                "O5-P3",
                "O5-P4",
                "O5-P5",
                "O6-O7",
                "O6-P4",
                "O6-P5",
                "O7-P4",
                "O7-P5",
                "P1-P2",
                "P1-P3",
                "P1-P4",
                "P1-P5",
                "P2-P3",
                "P2-P4",
                "P2-P5",
                "P3-P4",
                "P3-P5",
                "Ka1",
                "Ka2",
                "Ka3",
                "Kb1",
                "Kb2'",
                "Kb2''",
                "Kb3",
                "Kb4'",
                "Kb4''",
                "Kb4x",
                "Kb5'",
                "Kb5''",
                "La1",
                "La2",
                "Lb1",
                "Lb2",
                "Lb3",
                "Lb4",
                "Lb5",
                "Lb6",
                "Lb7",
                "Lb7'",
                "Lb9",
                "Lb10",
                "Lb15",
                "Lb17",
                "Lg1",
                "Lg2",
                "Lg3",
                "Lg4",
                "Lg4'",
                "Lg5",
                "Lg6",
                "Lg8",
                "Lg8'",
                "Ln",
                "Ll",
                "Ls",
                "Lt",
                "Lu",
                "Lv",
                "Ma1",
                "Ma2",
                "Mb",
                "Mg",
                "Mz",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-emission-line-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "K-L1",
                "K-L2",
                "K-L3",
                "K-M1",
                "K-M2",
                "K-M3",
                "K-M4",
                "K-M5",
                "K-N1",
                "K-N2",
                "K-N3",
                "K-N4",
                "K-N5",
                "K-N6",
                "K-N7",
                "K-O",
                "K-O1",
                "K-O2",
                "K-O3",
                "K-O4",
                "K-O5",
                "K-O6",
                "K-O7",
                "K-P",
                "K-P1",
                "K-P2",
                "K-P3",
                "K-P4",
                "K-P5",
                "L1-L2",
                "L1-L3",
                "L1-M1",
                "L1-M2",
                "L1-M3",
                "L1-M4",
                "L1-M5",
                "L1-N1",
                "L1-N2",
                "L1-N3",
                "L1-N4",
                "L1-N5",
                "L1-N6",
                "L1-N6,7",
                "L1-N7",
                "L1-O1",
                "L1-O2",
                "L1-O3",
                "L1-O4",
                "L1-O4,5",
                "L1-O5",
                "L1-O6",
                "L1-O7",
                "L1-P1",
                "L1-P2",
                "L1-P2,3",
                "L1-P3",
                "L1-P4",
                "L1-P5",
                "L2-L3",
                "L2-M1",
                "L2-M2",
                "L2-M3",
                "L2-M4",
                "L2-M5",
                "L2-N1",
                "L2-N2",
                "L2-N3",
                "L2-N4",
                "L2-N5",
                "L2-N6",
                "L2-N6,7",
                "L2-N7",
                "L2-O1",
                "L2-O2",
                "L2-O3",
                "L2-O4",
                "L2-O5",
                "L2-O6",
                "L2-O7",
                "L2-P1",
                "L2-P2",
                "L2-P2,3",
                "L2-P3",
                "L2-P4",
                "L2-P5",
                "L2-Q1",
                "L3-M1",
                "L3-M2",
                "L3-M3",
                "L3-M4",
                "L3-M5",
                "L3-N1",
                "L3-N2",
                "L3-N3",
                "L3-N4",
                "L3-N5",
                "L3-N6",
                "L3-N6,7",
                "L3-N7",
                "L3-O1",
                "L3-O2",
                "L3-O3",
                "L3-O4",
                "L3-O4,5",
                "L3-O5",
                "L3-O6",
                "L3-O7",
                "L3-P1",
                "L3-P2",
                "L3-P2,3",
                "L3-P3",
                "L3-P4",
                "L3-P4,5",
                "L3-P5",
                "L3-Q1",
                "M1-M2",
                "M1-M3",
                "M1-M4",
                "M1-M5",
                "M1-N1",
                "M1-N2",
                "M1-N3",
                "M1-N4",
                "M1-N5",
                "M1-N6",
                "M1-N7",
                "M1-O1",
                "M1-O2",
                "M1-O3",
                "M1-O4",
                "M1-O5",
                "M1-O6",
                "M1-O7",
                "M1-P1",
                "M1-P2",
                "M1-P3",
                "M1-P4",
                "M1-P5",
                "M2-M3",
                "M2-M4",
                "M2-M5",
                "M2-N1",
                "M2-N2",
                "M2-N3",
                "M2-N4",
                "M2-N5",
                "M2-N6",
                "M2-N7",
                "M2-O1",
                "M2-O2",
                "M2-O3",
                "M2-O4",
                "M2-O5",
                "M2-O6",
                "M2-O7",
                "M2-P1",
                "M2-P2",
                "M2-P3",
                "M2-P4",
                "M2-P5",
                "M3-M4",
                "M3-M5",
                "M3-N1",
                "M3-N2",
                "M3-N3",
                "M3-N4",
                "M3-N5",
                "M3-N6",
                "M3-N7",
                "M3-O1",
                "M3-O2",
                "M3-O3",
                "M3-O4",
                "M3-O5",
                "M3-O6",
                "M3-O7",
                "M3-P1",
                "M3-P2",
                "M3-P3",
                "M3-P4",
                "M3-P5",
                "M3-Q1",
                "M4-M5",
                "M4-N1",
                "M4-N2",
                "M4-N3",
                "M4-N4",
                "M4-N5",
                "M4-N6",
                "M4-N7",
                "M4-O1",
                "M4-O2",
                "M4-O3",
                "M4-O4",
                "M4-O5",
                "M4-O6",
                "M4-O7",
                "M4-P1",
                "M4-P2",
                "M4-P3",
                "M4-P4",
                "M4-P5",
                "M5-N1",
                "M5-N2",
                "M5-N3",
                "M5-N4",
                "M5-N5",
                "M5-N6",
                "M5-N7",
                "M5-O1",
                "M5-O2",
                "M5-O3",
                "M5-O4",
                "M5-O5",
                "M5-O6",
                "M5-O7",
                "M5-P1",
                "M5-P2",
                "M5-P3",
                "M5-P4",
                "M5-P5",
                "M4,5-N2,3",
                "N1-N2",
                "N1-N3",
                "N1-N4",
                "N1-N5",
                "N1-N6",
                "N1-N7",
                "N1-O1",
                "N1-O2",
                "N1-O3",
                "N1-O4",
                "N1-O5",
                "N1-O6",
                "N1-O7",
                "N1-P1",
                "N1-P2",
                "N1-P3",
                "N1-P4",
                "N1-P5",
                "N2-N3",
                "N2-N4",
                "N2-N5",
                "N2-N6",
                "N2-N7",
                "N2-O1",
                "N2-O2",
                "N2-O3",
                "N2-O4",
                "N2-O5",
                "N2-O6",
                "N2-O7",
                "N2-P1",
                "N2-P2",
                "N2-P3",
                "N2-P4",
                "N2-P5",
                "N3-N4",
                "N3-N5",
                "N3-N6",
                "N3-N7",
                "N3-O1",
                "N3-O2",
                "N3-O3",
                "N3-O4",
                "N3-O5",
                "N3-O6",
                "N3-O7",
                "N3-P1",
                "N3-P2",
                "N3-P3",
                "N3-P4",
                "N3-P5",
                "N4-N5",
                "N4-N6",
                "N4-N7",
                "N4-O1",
                "N4-O2",
                "N4-O3",
                "N4-O4",
                "N4-O5",
                "N4-O6",
                "N4-O7",
                "N4-P1",
                "N4-P2",
                "N4-P3",
                "N4-P4",
                "N4-P5",
                "N5-N6",
                "N5-N7",
                "N5-O1",
                "N5-O2",
                "N5-O3",
                "N5-O4",
                "N5-O5",
                "N5-O6",
                "N5-O7",
                "N5-P1",
                "N5-P2",
                "N5-P3",
                "N5-P4",
                "N5-P5",
                "N6-N7",
                "N6-O1",
                "N6-O2",
                "N6-O3",
                "N6-O4",
                "N6-O5",
                "N6-O6",
                "N6-O7",
                "N6-P1",
                "N6-P2",
                "N6-P3",
                "N6-P4",
                "N6-P5",
                "N7-O1",
                "N7-O2",
                "N7-O3",
                "N7-O4",
                "N7-O5",
                "N7-O6",
                "N7-O7",
                "N7-P1",
                "N7-P2",
                "N7-P3",
                "N7-P4",
                "N7-P5",
                "O1-O2",
                "O1-O3",
                "O1-O4",
                "O1-O5",
                "O1-O6",
                "O1-O7",
                "O1-P1",
                "O1-P2",
                "O1-P3",
                "O1-P4",
                "O1-P5",
                "O2-O3",
                "O2-O4",
                "O2-O5",
                "O2-O6",
                "O2-O7",
                "O2-P1",
                "O2-P2",
                "O2-P3",
                "O2-P4",
                "O2-P5",
                "O3-O4",
                "O3-O5",
                "O3-O6",
                "O3-O7",
                "O3-P1",
                "O3-P2",
                "O3-P3",
                "O3-P4",
                "O3-P5",
                "O4-O5",
                "O4-O6",
                "O4-O7",
                "O4-P1",
                "O4-P2",
                "O4-P3",
                "O4-P4",
                "O4-P5",
                "O5-O6",
                "O5-O7",
                "O5-P1",
                "O5-P2",
                "O5-P3",
                "O5-P4",
                "O5-P5",
                "O6-O7",
                "O6-P4",
                "O6-P5",
                "O7-P4",
                "O7-P5",
                "P1-P2",
                "P1-P3",
                "P1-P4",
                "P1-P5",
                "P2-P3",
                "P2-P4",
                "P2-P5",
                "P3-P4",
                "P3-P5",
                "Ka1",
                "Ka2",
                "Ka3",
                "Kb1",
                "Kb2'",
                "Kb2''",
                "Kb3",
                "Kb4'",
                "Kb4''",
                "Kb4x",
                "Kb5'",
                "Kb5''",
                "La1",
                "La2",
                "Lb1",
                "Lb2",
                "Lb3",
                "Lb4",
                "Lb5",
                "Lb6",
                "Lb7",
                "Lb7'",
                "Lb9",
                "Lb10",
                "Lb15",
                "Lb17",
                "Lg1",
                "Lg2",
                "Lg3",
                "Lg4",
                "Lg4'",
                "Lg5",
                "Lg6",
                "Lg8",
                "Lg8'",
                "Ln",
                "Ll",
                "Ls",
                "Lt",
                "Lu",
                "Lv",
                "Ma1",
                "Ma2",
                "Mb",
                "Mg",
                "Mz",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdBeamlineCoordinateSystem(CoordinateSystem):
    """
    Beamline coordinate system with the sample at the origin: x along the beam,
    y horizontal, z opposite to gravity.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="beamline_coordinate_system",
            name_type="specified",
            optionality="optional",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdBeamlineCoordinateSystemTransformations",
        repeats=False,
    )

    origin = Quantity(
        type=MEnum(["sample"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-origin-field"
        ],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["sample"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="sample",
        ),
    )
    x_direction = Quantity(
        type=MEnum(["along incident beam"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-x-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["along incident beam"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="along incident beam",
        ),
    )
    y_direction = Quantity(
        type=MEnum(["horizontal perpendicular to beam"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-y-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["horizontal perpendicular to beam"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="horizontal perpendicular to beam",
        ),
    )
    z_direction = Quantity(
        type=MEnum(["opposite to gravity"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-z-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["opposite to gravity"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="opposite to gravity",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-depends-on-field"
        ],
        description=("Should point to ``transformations/beam``."),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdBeamlineCoordinateSystemTransformations(Transformations):
    """
    Two rotations relating the beamline frame to the NeXus laboratory frame,
    plus direction vectors labeling beam and gravity.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="required",
        ),
    )

    beam = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-beam-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Direction of the incident beam in the beamline coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="beam",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    beam__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-beam-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="beam",
        ),
    )
    beam__depends_on = Quantity(
        type=MEnum(["gravity"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-beam-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam",
            enumeration=["gravity"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="gravity",
        ),
    )
    gravity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-gravity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Direction of gravity in the beamline coordinate system."),
        a_nexus_field=NeXusField(
            name="gravity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    gravity__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-gravity-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="gravity",
        ),
    )
    gravity__depends_on = Quantity(
        type=MEnum(["rotate_gravity_to_minus_y"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-gravity-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="gravity",
            enumeration=["rotate_gravity_to_minus_y"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotate_gravity_to_minus_y",
        ),
    )
    rotate_gravity_to_minus_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-gravity-to-minus-y-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Active rotation moving gravity from the beamline direction (-z) to "
            "the NeXus direction (-y)."
        ),
        a_nexus_field=NeXusField(
            name="rotate_gravity_to_minus_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    rotate_gravity_to_minus_y__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-gravity-to-minus-y-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="rotate_gravity_to_minus_y",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    rotate_gravity_to_minus_y__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-gravity-to-minus-y-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="rotate_gravity_to_minus_y",
        ),
    )
    rotate_gravity_to_minus_y__depends_on = Quantity(
        type=MEnum(["rotate_beam_to_plus_z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-gravity-to-minus-y-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="rotate_gravity_to_minus_y",
            enumeration=["rotate_beam_to_plus_z"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotate_beam_to_plus_z",
        ),
    )
    rotate_beam_to_plus_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-beam-to-plus-z-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Active rotation moving the beam from the beamline direction (+x) to "
            "the NeXus direction (+z)."
        ),
        a_nexus_field=NeXusField(
            name="rotate_beam_to_plus_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    rotate_beam_to_plus_z__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-beam-to-plus-z-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="rotate_beam_to_plus_z",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    rotate_beam_to_plus_z__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-beam-to-plus-z-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="rotate_beam_to_plus_z",
        ),
    )
    rotate_beam_to_plus_z__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-beamline-coordinate-system-transformations-rotate-beam-to-plus-z-depends-on-attribute"
        ],
        description=("Should point to ``.`` (the NeXus laboratory frame)."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="rotate_beam_to_plus_z",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdSample(XasSample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-group"
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
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdSampleTransformations",
        repeats=False,
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-depends-on-field"
        ],
        description=(
            "The sample is at the origin of the beamline coordinate system, "
            "rotated about the vertical axis. Should point to "
            "``transformations/sample_rotation``."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdSampleTransformations(Transformations):
    """
    Orientation of the sample in the beamline coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )

    sample_rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-transformations-sample-rotation-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation of the sample about the vertical axis, orienting the "
            "sample surface between the incident beam and the crystal analyzers."
        ),
        a_nexus_field=NeXusField(
            name="sample_rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    sample_rotation__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-transformations-sample-rotation-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    sample_rotation__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-transformations-sample-rotation-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation",
        ),
    )
    sample_rotation__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-sample-transformations-sample-rotation-depends-on-attribute"
        ],
        description=("Should point to ``/entry/beamline_coordinate_system``."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentBeam",
        repeats=False,
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentSource",
        repeats=True,
        variable=True,
    )
    i0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentI0",
        repeats=False,
    )
    analyzerCRYSTAL = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentAnalyzerCRYSTAL",
        repeats=True,
        variable=True,
    )
    ifluor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentIfluor",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrumentBeam(Beam):
    """
    The incident X-ray beam.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam",
            name_type="specified",
            optionality="optional",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentBeamTransformations",
        repeats=False,
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-depends-on-field"
        ],
        description=("Should point to ``transformations/beam_direction``."),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdInstrumentBeamTransformations(Transformations):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )

    beam_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-transformations-beam-direction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Beam direction in the beamline coordinate system. The beam travels "
            "along +x."
        ),
        a_nexus_field=NeXusField(
            name="beam_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    beam_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-transformations-beam-direction-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="beam_direction",
        ),
    )
    beam_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-beam-transformations-beam-direction-depends-on-attribute"
        ],
        description=("Should point to ``/entry/beamline_coordinate_system``."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-source-name-field"
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
    probe = Quantity(
        type=MEnum(["x-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["x-ray"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="x-ray",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrumentI0(Detector):
    """
    Detector measuring the incident beam intensity :math:`I_0`, positioned
    upstream of the sample along the beam direction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="i0",
            name_type="specified",
            optionality="recommended",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentI0Transformations",
        repeats=False,
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-data-field"
        ],
        flexible_unit=True,
        shape=["*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-depends-on-field"
        ],
        description=("Should point to ``transformations/i0_distance``."),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdInstrumentI0Transformations(Transformations):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )

    i0_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-transformations-i0-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance from the sample to the I0 detector, measured upstream "
            "along the beam (negative x direction in the beamline frame)."
        ),
        a_nexus_field=NeXusField(
            name="i0_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    i0_distance__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-transformations-i0-distance-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="i0_distance",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    i0_distance__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-transformations-i0-distance-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="i0_distance",
        ),
    )
    i0_distance__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-i0-transformations-i0-distance-depends-on-attribute"
        ],
        description=("Should point to ``/entry/beamline_coordinate_system``."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="i0_distance",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrumentAnalyzerCRYSTAL(Crystal):
    """
    Crystal analyzer on the Rowland circle. For multi-crystal spectrometers,
    use one group per crystal (e.g. ``analyzer1``, ``analyzer2``).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name="analyzerCRYSTAL",
            name_type="partial",
            optionality="required",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentAnalyzerCRYSTALTransformations",
        repeats=False,
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-type-field"
        ],
        description=("Type or material of the analyzer crystal (Si, Ge, etc.)."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reflection = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-reflection-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[3],
        description=("Miller indices (hkl) values of the nominal reflection."),
        a_nexus_field=NeXusField(
            name="reflection",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    d_spacing = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-d-spacing-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The spacing between crystal planes of the reflection."),
        a_nexus_field=NeXusField(
            name="d_spacing",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    bragg_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-bragg-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("Bragg angle :math:`\\theta_B` of the nominal reflection."),
        a_nexus_field=NeXusField(
            name="bragg_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    bending_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-bending-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Bending radius of the spherically bent crystal analyzer. In Johann "
            "geometry this is :math:`2R_R` (twice the Rowland radius)."
        ),
        a_nexus_field=NeXusField(
            name="bending_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    rowland_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-rowland-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Radius of the Rowland circle :math:`R_R`. The sample, crystal "
            "center, and detector focus all lie on this circle."
        ),
        a_nexus_field=NeXusField(
            name="rowland_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    energy_resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-energy-resolution-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("The energy bandwidth or resolution of the crystal analyzer."),
        a_nexus_field=NeXusField(
            name="energy_resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    geometry_type = Quantity(
        type=MEnum(["Johann", "Johansson"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-geometry-type-field"
        ],
        description=("The type of crystal analyzer geometry."),
        a_nexus_field=NeXusField(
            name="geometry_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Johann", "Johansson"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Diameter of the crystal analyzer wafer."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-depends-on-field"
        ],
        description=(
            "Should point to the last transformation in the chain, i.e. "
            "``transformations/analyzer_distance``."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdInstrumentAnalyzerCRYSTALTransformations(Transformations):
    """
    Transformation chain placing the analyzer relative to the sample: azimuthal
    angle, polar angle, then distance.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )

    analyzer_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Sample-to-analyzer distance."),
        a_nexus_field=NeXusField(
            name="analyzer_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    analyzer_distance__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-distance-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_distance",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    analyzer_distance__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-distance-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_distance",
        ),
    )
    analyzer_distance__depends_on = Quantity(
        type=MEnum(["analyzer_polar_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-distance-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_distance",
            enumeration=["analyzer_polar_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="analyzer_polar_angle",
        ),
    )
    analyzer_polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Polar angle of the analyzer in the vertical Rowland plane. "
            "Elevation from the horizontal beam plane to the sample-analyzer "
            "direction."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_polar_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    analyzer_polar_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-polar-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_polar_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    analyzer_polar_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-polar-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_polar_angle",
        ),
    )
    analyzer_polar_angle__depends_on = Quantity(
        type=MEnum(["analyzer_azimuthal_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-polar-angle-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_polar_angle",
            enumeration=["analyzer_azimuthal_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="analyzer_azimuthal_angle",
        ),
    )
    analyzer_azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Azimuthal (horizontal) angle of the spectrometer arm from the "
            "incident beam direction. Rotation around the vertical z-axis. "
            "Typically around 90 degrees to minimize elastic scattering."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_azimuthal_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    analyzer_azimuthal_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-azimuthal-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_azimuthal_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    analyzer_azimuthal_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-azimuthal-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_azimuthal_angle",
        ),
    )
    analyzer_azimuthal_angle__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-analyzercrystal-transformations-analyzer-azimuthal-angle-depends-on-attribute"
        ],
        description=("Should point to ``/entry/beamline_coordinate_system``."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_azimuthal_angle",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdInstrumentIfluor(Detector):
    """
    Detector measuring the fluorescence intensity :math:`I_f` diffracted by the
    crystal analyzer(s).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="ifluor",
            name_type="specified",
            optionality="recommended",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdInstrumentIfluorTransformations",
        repeats=False,
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-data-field"
        ],
        flexible_unit=True,
        shape=["*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-depends-on-field"
        ],
        description=(
            "Should point to the last transformation in the chain, i.e. "
            "``transformations/if_distance``."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class XasHerfdInstrumentIfluorTransformations(Transformations):
    """
    Transformation chain placing the detector relative to the sample: azimuthal
    angle, polar angle, then distance.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )

    if_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Distance from the sample to the detector."),
        a_nexus_field=NeXusField(
            name="if_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    if_distance__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-distance-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_distance",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    if_distance__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-distance-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="if_distance",
        ),
    )
    if_distance__depends_on = Quantity(
        type=MEnum(["if_polar_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-distance-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_distance",
            enumeration=["if_polar_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="if_polar_angle",
        ),
    )
    if_polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Polar angle of the detector in the vertical Rowland plane."),
        a_nexus_field=NeXusField(
            name="if_polar_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    if_polar_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-polar-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_polar_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    if_polar_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-polar-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="if_polar_angle",
        ),
    )
    if_polar_angle__depends_on = Quantity(
        type=MEnum(["if_azimuthal_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-polar-angle-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_polar_angle",
            enumeration=["if_azimuthal_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="if_azimuthal_angle",
        ),
    )
    if_azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Azimuthal (horizontal) angle of the detector from the incident beam "
            "direction. Should match the analyzer azimuthal angle for on-Rowland "
            "focusing."
        ),
        a_nexus_field=NeXusField(
            name="if_azimuthal_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    if_azimuthal_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-azimuthal-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_azimuthal_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    if_azimuthal_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-azimuthal-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="if_azimuthal_angle",
        ),
    )
    if_azimuthal_angle__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-instrument-ifluor-transformations-if-azimuthal-angle-depends-on-attribute"
        ],
        description=("Should point to ``/entry/beamline_coordinate_system``."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="if_azimuthal_angle",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdCollection(Collection):
    """
    Raw data as written by the acquisition software, preserved without
    modification to allow independent reprocessing.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-collection-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    raw_data = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-collection-raw-data-field"
        ],
        shape=["*", "*"],
        description=(
            "Raw fluorescence counts per incident energy point for each crystal "
            "analyzer, before normalization by the incident beam intensity and "
            "summation over analyzers. Axis 0 is the energy scan axis; axis 1 "
            "enumerates the crystal analyzers, in the same order as the "
            "``analyzerCRYSTAL`` groups."
        ),
        a_nexus_field=NeXusField(
            name="raw_data",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasHerfdProcess(Process):
    """
    Description of how :ref:`intensity </NXxas/ENTRY/intensity-field>` was
    obtained from the raw detector data (i0, if).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    note = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_herfd.XasHerfdProcessNote",
        repeats=False,
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-program-field"
        ],
        description=("Name of the program used for processing."),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-version-field"
        ],
        description=("Version of the program used for processing."),
        a_nexus_field=NeXusField(
            name="version",
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


class XasHerfdProcessNote(Note):
    """
    Python code reproducing the top-level :ref:`intensity
    </NXxas/ENTRY/intensity-field>` from the raw data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-note-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="note",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["text/x-python"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-note-type-field"
        ],
        description=("Mime content type of the note data field."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["text/x-python"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="text/x-python",
        ),
    )
    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_herfd.html#nxxas_herfd-entry-process-note-data-field"
        ],
        description=("The Python code."),
        a_nexus_field=NeXusField(
            name="data",
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
