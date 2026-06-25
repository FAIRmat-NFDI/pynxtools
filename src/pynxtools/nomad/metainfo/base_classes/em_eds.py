# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXem_eds (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXem_eds` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo.base_classes.atom import Atom
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.image import Image
from pynxtools.nomad.metainfo.base_classes.peak import Peak
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmEds"]


class EmEds(Process):
    """
    Base class method-specific for energy-dispersive X-ray spectroscopy
    (EDS/EDXS).

    `IUPAC instead of Siegbahn notation
    <https://doi.org/10.1002/xrs.1300200308>`_ should be used.

    X-ray spectroscopy is a surface-sensitive technique. Therefore,
    three-dimensional elemental characterization requires typically a sequence
    of characterization and preparation of the surface to expose new surface
    layer that can be characterized in the next acquisition. In effect, the
    resulting three-dimensional elemental information mappings are truly the
    result of a correlation and post-processing of several measurements which
    is the field of correlative tomographic usage of electron microscopy.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_eds",
            category="base",
            symbols={
                "n_photon_energy": "Number of X-ray photon energy (bins)",
                "n_elements": "Number of identified elements",
                "n_peaks": "Number of peaks detected",
                "n_iupac_line_names": "Number of IUPAC line names",
            },
        ),
    )

    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexing",
        repeats=False,
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


class EmEdsIndexing(Process):
    """
    Details about computational steps how peaks were indexed as elements.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    program_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        description=("The program with which the indexing was performed."),
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    summary = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingSummary",
        repeats=False,
    )
    peak = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingPeak",
        repeats=True,
        variable=True,
    )
    element_specific_map = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingElementSpecificMap",
        repeats=True,
        variable=True,
    )

    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-atom-types-field"
        ],
        description=(
            "Comma-separated list of symbols for elements from the periodic "
            "table that have been confirmed present by the here reported EDS "
            "analysis. This field can be used when creating instances of "
            ":ref:`NXpeak` is not desired. However, a collection of instances of "
            "NXpeak with individual NXatom can be used to add isotopic "
            "information and other relevant context."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
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


class EmEdsIndexingSummary(Data):
    """
    Accumulated intensity over all pixels of the region-of-interest.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-summary-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="summary",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-summary-intensity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Accumulated counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__min = Quantity(
        type=np.float64,
        description="Minimum of intensity, computed over the full array at parse time.",
    )
    intensity__max = Quantity(
        type=np.float64,
        description="Maximum of intensity, computed over the full array at parse time.",
    )
    intensity__size = Quantity(
        type=np.int64,
        description="Number of elements of intensity in the HDF5 file.",
    )
    intensity__ndim = Quantity(
        type=np.int8,
        description="Number of dimensions of intensity in the HDF5 file.",
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-summary-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-summary-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__min = Quantity(
        type=np.float64,
        description="Minimum of axis_energy, computed over the full array at parse time.",
    )
    axis_energy__max = Quantity(
        type=np.float64,
        description="Maximum of axis_energy, computed over the full array at parse time.",
    )
    axis_energy__size = Quantity(
        type=np.int64,
        description="Number of elements of axis_energy in the HDF5 file.",
    )
    axis_energy__ndim = Quantity(
        type=np.int8,
        description="Number of dimensions of axis_energy in the HDF5 file.",
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-summary-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEdsIndexingPeak(Peak):
    """
    Details about individual indexed peaks.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-peak-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingPeakAtom",
        repeats=True,
        variable=True,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEdsIndexingPeakAtom(Atom):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-peak-atom-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    energy_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-peak-atom-energy-range-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        shape=[2],
        description=(
            "Associated lower :math:`[e_{min}, e_{max}]` bounds of the energy "
            "which is assumed associated with this peak."
        ),
        a_nexus_field=NeXusField(
            name="energy_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-peak-atom-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("Theoretical energy of the line according to IUPAC."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    iupac_line_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-peak-atom-iupac-line-name-field"
        ],
        shape=["*"],
        description=(
            "IUPAC notation identifier of the line which the peak represents. "
            "This can be a list of IUPAC notations for (the seldom) case that "
            "multiple lines are grouped with the same peak."
        ),
        a_nexus_field=NeXusField(
            name="iupac_line_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEdsIndexingElementSpecificMap(Image):
    """
    Individual element-specific EDS/EDX/EDXS/SXES mapping

    A composition map is an image whose intensities for each pixel are the
    accumulated X-ray quanta *under the curve(s)* of a set of peaks.

    These element-specific EDS maps are instances of :ref:`NXimage` that should
    be named by the element from the atom_types field.

    When signal contributions from several peaks were decomposed users should
    ideally use a respective number of NXpeak instances to give further context
    about the individual signal contributions are summarized and shown
    together, e.g. the combined signal under the curve of carbon and oxygen.

    In this case specify the processing details use peak and weight.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="ELEMENT_SPECIFIC_MAP",
            name_type="any",
            optionality="optional",
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingElementSpecificMapProcess",
        repeats=True,
        variable=True,
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-description-field"
        ],
        description=("Discouraged free-text field to add additional information."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.RichTextEditQuantity,
        ),
    )
    iupac_line_candidates = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-iupac-line-candidates-field"
        ],
        description=(
            "Comma-separated list of chemical_symbol-IUPAC X-ray (emission) line "
            "name that documents which elements and their specific lines are "
            "theoretically located within the energy_range of the spectrum from "
            "which the EDS (element) map was computed."
        ),
        a_nexus_field=NeXusField(
            name="iupac_line_candidates",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    energy_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-energy-range-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        shape=[2],
        description=(
            "Associated :math:`[e_{min}, e_{max}]` bounds of the energy range "
            "for which spectrum counts were accumulated."
        ),
        a_nexus_field=NeXusField(
            name="energy_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEdsIndexingElementSpecificMapProcess(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    peak = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-process-peak-field"
        ],
        shape=["*"],
        description=(
            "A list of :ref:`NXpeak` instance names whose X-ray quanta were "
            "accumulated for each pixel to obtain an element-specific EDS map."
        ),
        a_nexus_field=NeXusField(
            name="peak",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-element-specific-map-process-weight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "A list of weights by how much the intensity of each peak "
            "contributes to the intensity of the EDS map."
        ),
        a_nexus_field=NeXusField(
            name="weight",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
