# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXxas_trans (see
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
# Run `pynx nomad generate-metainfo --nxdl NXxas_trans` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.crystal import Crystal
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.subentry import Subentry

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["XasTrans"]


class XasTrans(Xas):
    r"""
    In transmission, the linear attenuation coefficient or absorption
    coefficient :math:`\mu(E)` is given by the Beer-Lambert law:

    .. math:: \mu(E)t = -\ln(I/I_0)

    where :math:`I` is the intensity of the transmitted beam, :math:`I_0` is
    the intensity of the incident beam, and :math:`t` is the thickness of the
    sample.

    The top-level :ref:`intensity </NXxas/ENTRY/intensity-field>` field
    contains the processed absorption coefficient. When the raw detector data
    and processing steps are available, they can be stored in the optional
    ``NXinstrument``, ``NXcollection``, and ``NXprocess`` groups, enabling full
    reproducibility of the data reduction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxas_trans",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrument",
        repeats=True,
        variable=True,
    )
    reference = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransReference",
        repeats=False,
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        description=(
            "Raw data as written by the acquisition software, preserved without "
            "modification to allow independent reprocessing."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransProcess",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXxas_trans"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxas_trans"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxas_trans",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-intensity-field"
        ],
        flexible_unit=True,
        description=("The absorption coefficient :math:`\\mu(E)t = -\\ln(I/I_0)`."),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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


class XasTransInstrument(Instrument):
    """
    The ``data`` field of each detector below holds the intensity used to
    compute the absorption coefficient and may already include corrections. If
    the uncorrected values are kept, they are archived in the ``NXcollection``
    group and the corrections are described in ``NXprocess``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentSource",
        repeats=True,
        variable=True,
    )
    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentMonochromator",
        repeats=False,
    )
    i0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentI0",
        repeats=False,
    )
    itrans = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentItrans",
        repeats=False,
    )
    iref = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentIref",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTransInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-source-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-source-probe-field"
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


class XasTransInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromator",
            name_type="specified",
            optionality="recommended",
        ),
    )

    crystal = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransInstrumentMonochromatorCrystal",
        repeats=False,
    )

    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTransInstrumentMonochromatorCrystal(Crystal):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-crystal-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name="crystal",
            name_type="specified",
            optionality="recommended",
        ),
    )

    d_spacing = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-crystal-d-spacing-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The spacing between crystal planes of the reflection"),
        a_nexus_field=NeXusField(
            name="d_spacing",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-crystal-type-field"
        ],
        description=(
            "Type or material of monochromating substance (Si, Ge, Multilayer)."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reflection = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-monochromator-crystal-reflection-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[3],
        description=("Miller indices (hkl) values of nominal reflection"),
        a_nexus_field=NeXusField(
            name="reflection",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTransInstrumentI0(Detector):
    """
    Detector measuring the incident beam intensity :math:`I_0`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-i0-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-i0-data-field"
        ],
        flexible_unit=True,
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


class XasTransInstrumentItrans(Detector):
    """
    Detector measuring the transmitted beam intensity :math:`I`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-itrans-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="itrans",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-itrans-data-field"
        ],
        flexible_unit=True,
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


class XasTransInstrumentIref(Detector):
    """
    Detector measuring the reference intensity :math:`I_{ref}`, placed after a
    reference sample (typically a metal foil). For a reference that is an
    independent spectrum probing a different absorbing element or absorption
    edge, use the ``reference`` subentry instead.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-iref-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="iref",
            name_type="specified",
            optionality="recommended",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-instrument-iref-data-field"
        ],
        flexible_unit=True,
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


class XasTransReference(Subentry):
    """
    An independent reference spectrum, for example a metal-foil standard used
    for energy calibration. Use this group instead of the ``iref`` detector
    when the reference is a complete spectrum in its own right, in particular
    when it probes a different absorbing element or absorption edge, so that
    the element, edge, energy axis, and intensity of the reference can be
    described in full.

    Provide the ``iref`` detector when the reference is a simultaneous
    transmission channel that shares the main energy axis. Provide this
    ``reference`` subentry when the reference is an independent measurement. Do
    not provide both for the same reference.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-reference-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsubentry",
            name="reference",
            name_type="specified",
            optionality="optional",
        ),
    )

    definition = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-reference-definition-field"
        ],
        description=(
            "Official NeXus NXDL schema to which this subentry conforms. Should "
            "be an ``NXxas``-family definition (for example ``NXxas`` or "
            "``NXxas_trans``)."
        ),
        a_nexus_field=NeXusField(
            name="definition",
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


class XasTransProcess(Process):
    """
    Description of how :ref:`intensity </NXxas/ENTRY/intensity-field>` was
    obtained from the raw detector data (i0, itrans, and iref). When present,
    it allows a third party to fully reproduce the data reduction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=False,
        description=(
            "Validated parameters of the corrections applied, for example energy "
            "calibration, deglitching, incident-beam normalization, or scan "
            "merging. Each parameter should carry a units attribute where "
            "applicable."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="parameters",
            name_type="specified",
            optionality="optional",
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas_trans.XasTransProcessNote",
        repeats=False,
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-version-field"
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
    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-sequence-index-field"
        ],
        description=(
            "Order of this step when several NXprocess groups describe a "
            "sequence of corrections."
        ),
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasTransProcessNote(Note):
    """
    Code or notes reproducing the top-level :ref:`intensity
    </NXxas/ENTRY/intensity-field>` from the raw data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-note-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-note-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas_trans.html#nxxas_trans-entry-process-note-data-field"
        ],
        description=("The reproduction code or notes."),
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
