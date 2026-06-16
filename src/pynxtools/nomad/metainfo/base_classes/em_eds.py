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
# Run `pynx nomad generate-metainfo --nxdl NXem_eds` to regenerate.
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
        description=(
            "Details about computational steps how peaks were indexed as elements."
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

    summary = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingSummary",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="summary",
            name_type="specified",
            optionality="optional",
        ),
    )
    peak = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingPeak",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    image = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingImage",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
        ),
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
        unit="joule",
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
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
        ),
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
        unit="joule",
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
        unit="joule",
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
        a_display={"unit": "joule"},
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


class EmEdsIndexingImage(Image):
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
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexingImageProcess",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    description_quantity = Quantity(
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
            component=ELNComponentEnum.StringEditQuantity,
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
        unit="joule",
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


class EmEdsIndexingImageProcess(Process):
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
