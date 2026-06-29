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
# Run `pynx nomad generate-metainfo --nxdl NXapm_ranging` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmRanging"]


class ApmRanging(Process):
    """
    Base class for the configuration and results of ranging definitions.

    Ranging is a data post-processing step used in the research field of atom
    probe during which elemental, isotopic, and/or molecular identities are
    assigned to mass-to-charge-state ratios within certain intervals. The
    documentation of these steps is based on ideas that have been described in
    the literature:

    * `M. K. Miller <https://doi.org/10.1002/sia.1719>`_ * `D. Haley et al.
    <https://doi.org/10.1017/S1431927620024290>`_ * `M. Kühbach et al.
    <https://doi.org/10.1017/S1431927621012241>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_ranging",
            category="base",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    mass_to_charge_distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_ranging.ApmRangingMassToChargeDistribution",
        repeats=False,
        description=("Specifies the mass-to-charge-state ratio histogram."),
    )
    background_quantification = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_ranging.ApmRangingBackgroundQuantification",
        repeats=False,
        description=(
            "Details of the background model that was used to correct the total "
            "counts per bin into counts."
        ),
    )
    peak_search_and_deconvolution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_ranging.ApmRangingPeakSearchAndDeconvolution",
        repeats=False,
        description=(
            "How were peaks in the mass-to-charge-state ratio histogram identified."
        ),
    )
    peak_identification = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_ranging.ApmRangingPeakIdentification",
        repeats=False,
        description=(
            "Details about how peaks, with taking into account error models, "
            "were interpreted as ion types or not."
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


class ApmRangingMassToChargeDistribution(Process):
    """
    Specifies the mass-to-charge-state ratio histogram.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-mass-to-charge-distribution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="mass_to_charge_distribution",
            name_type="specified",
            optionality="optional",
        ),
    )

    mass_spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="mass_spectrum",
            name_type="specified",
            optionality="optional",
        ),
    )

    min_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-mass-to-charge-distribution-min-mass-to-charge-field"
        ],
        flexible_unit=True,
        description=(
            "Smallest :math:`{\\frac{m}{q}}_{min}` mass-to-charge-state ratio "
            "value. The lower (left-hand side) inclusive bound of the interval "
            ":math:`[{\\frac{m}{q}}_{min}, {\\frac{m}{q}}_{max}]`."
        ),
        a_nexus_field=NeXusField(
            name="min_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    max_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-mass-to-charge-distribution-max-mass-to-charge-field"
        ],
        flexible_unit=True,
        description=(
            "Largest :math:`{\\frac{m}{q}}_{max}` mass-to-charge-state ratio "
            "value. The upper (right-hand side) inclusive bound of the interval "
            ":math:`[{\\frac{m}{q}}_{min}, {\\frac{m}{q}}_{max}]`."
        ),
        a_nexus_field=NeXusField(
            name="max_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    n_mass_to_charge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-mass-to-charge-distribution-n-mass-to-charge-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The number of bins on the interval :math:`[{\\frac{m}{q}}_{min}, "
            "{\\frac{m}{q}}_{max}]`."
        ),
        a_nexus_field=NeXusField(
            name="n_mass_to_charge",
            type="NX_POSINT",
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


class ApmRangingBackgroundQuantification(Process):
    """
    Details of the background model that was used to correct the total counts
    per bin into counts.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-background-quantification-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="background_quantification",
            name_type="specified",
            optionality="optional",
        ),
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-background-quantification-description-field"
        ],
        description=(
            "Free-text field to describe how atom probers define a background "
            "model. Thereby, community feedback can be collected to inform an "
            "improved version of this base class in the future."
        ),
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmRangingPeakSearchAndDeconvolution(Process):
    """
    How were peaks in the mass-to-charge-state ratio histogram identified.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-peak-search-and-deconvolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_search_and_deconvolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    peak = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.peak.Peak",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmRangingPeakIdentification(Process):
    """
    Details about how peaks, with taking into account error models, were
    interpreted as ion types or not.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-peak-identification-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_identification",
            name_type="specified",
            optionality="optional",
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.atom.Atom",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    number_of_ion_types = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-peak-identification-number-of-ion-types-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many ion types are distinguished. If no ranging was performed, "
            "each ion is of the special unknown type. The iontype ID of this "
            "unknown type is 0 representing a reserved value. Consequently, "
            "start counting iontypes from 1."
        ),
        a_nexus_field=NeXusField(
            name="number_of_ion_types",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    maximum_number_of_atoms_per_molecular_ion = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_ranging.html#nxapm_ranging-peak-identification-maximum-number-of-atoms-per-molecular-ion-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Assumed maximum value that suffices to store all relevant molecular "
            "ions, even the most complicated ones that one can typically observe "
            "and distinguish typically. Currently, a value of 32 is used (see M. "
            "Kühbach et al. <https://doi.org/10.1017/S1431927621012241>`_)."
        ),
        a_nexus_field=NeXusField(
            name="maximum_number_of_atoms_per_molecular_ion",
            type="NX_UINT",
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
