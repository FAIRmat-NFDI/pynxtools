# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXxas_tey (see
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
# Run `pynx nomad generate-metainfo --nxdl NXxas_tey` to regenerate.
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
from pynxtools.nomad.metainfo.applications.xas import Xas
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["XasTey"]


class XasTey(Xas):
    r"""
    In total electron yield (TEY), the XAS spectrum is measured by collecting
    all secondary electrons emitted from the sample surface. The drain current
    or total electron current :math:`I_{ey}` is proportional to the absorption
    coefficient:

    .. math:: \mu(E) \propto I_{ey}/I_0

    TEY is inherently surface-sensitive because electrons are readily absorbed
    by most materials, limiting the probing depth to a few nanometers.

    The top-level :ref:`intensity </NXxas/ENTRY/intensity-field>` field stores
    the ratio :math:`I_{ey}/I_0`. When the raw detector data and processing
    steps are available, they can be stored in the optional ``NXinstrument``
    and ``NXprocess`` groups, enabling full reproducibility of the data
    reduction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxas_tey",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_tey.XasTeyInstrument",
        repeats=True,
        variable=True,
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_tey.XasTeyProcess",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXxas_tey"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxas_tey"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxas_tey",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-intensity-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "The absorption coefficient :math:`\\mu(E) \\propto I_{ey}/I_0`, "
            "where :math:`I_{ey}` is the total electron yield signal."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
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


class XasTeyInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    i0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_tey.XasTeyInstrumentI0",
        repeats=False,
    )
    iey = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_tey.XasTeyInstrumentIey",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTeyInstrumentI0(Detector):
    """
    Detector measuring the incident beam intensity :math:`I_0`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-instrument-i0-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="i0",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-instrument-i0-data-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTeyInstrumentIey(Detector):
    """
    Detector measuring the total electron yield :math:`I_{ey}` (drain current).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-instrument-iey-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="iey",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-instrument-iey-data-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTeyProcess(Process):
    """
    Description of how :ref:`intensity </NXxas/ENTRY/intensity-field>` was
    obtained from the raw detector data (i0, iey).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-process-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_tey.html#nxxas_tey-entry-process-version-field"
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
