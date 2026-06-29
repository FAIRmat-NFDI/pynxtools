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
# Run `pynx nomad generate-metainfo --nxdl NXapm_charge_state_analysis` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmChargeStateAnalysis"]


class ApmChargeStateAnalysis(Process):
    """
    Base class to document the parameters, configuration, and results of a
    processing for recovering the charge state and nuclide composition of an
    ion from ranging definitions as used in the research field of atom probe
    microscopy.

    A ranging definition classically reports only the
    mass-to-charge-state-ratio interval plus the elemental composition, but not
    necessarily the nuclide that compose the ion.

    As the mass-resolving-power in an atom probe instrument is finite and
    typically lower than for cutting edge tandem mass spectrometry it is
    possible that different combinations of nuclides are indistinguishable and
    thus multiple ions in eventually even different charge states can be valid
    labels for a given mass-to-charge-state-ratio peak. Enumerating the
    possible combinations is a programmatic approach that can help with peak
    identification.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_charge_state_analysis",
            category="base",
            symbols={
                "n_cand": "The number of ion candidates.",
                "n_ivec_max": "Maximum number of allowed atoms per ion.",
                "n_variable": "Number of entries",
            },
        ),
    )

    config = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_charge_state_analysis.ApmChargeStateAnalysisConfig",
        repeats=False,
        description=(
            "Parameters for the algorithm used to recover which combinations of "
            "nuclides have a mass and charge that matches a set of constraints. "
            "Each parameter in this group is defines one constraint."
        ),
    )

    charge_state = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-charge-state-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Signed charge, i.e. integer multiple of the elementary charge of "
            "each candidate."
        ),
        a_nexus_field=NeXusField(
            name="charge_state",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Table of nuclide instances of which each candidate is composed. "
            "Each row vector is sorted in descending order. Unused entries in "
            "the matrix should be set to 0. Use the hashing rule that is defined "
            "in nuclide_hash of :ref:`NXatom`."
        ),
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-mass-field"
        ],
        dimensionality="[mass]",
        unit="kilogram",
        shape=["*"],
        description=(
            "Accumulated mass of the nuclides in each candidate. Not corrected "
            "for quantum effects."
        ),
        a_nexus_field=NeXusField(
            name="mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )
    natural_abundance_product = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-natural-abundance-product-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The product of the natural abundances of the nuclides for each candidate."
        ),
        a_nexus_field=NeXusField(
            name="natural_abundance_product",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    shortest_half_life = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-shortest-half-life-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "For each candidate the half life of the nuclide that has the "
            "shortest half life."
        ),
        a_nexus_field=NeXusField(
            name="shortest_half_life",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
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


class ApmChargeStateAnalysisConfig(Parameters):
    """
    Parameters for the algorithm used to recover which combinations of nuclides
    have a mass and charge that matches a set of constraints.

    Each parameter in this group is defines one constraint.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="optional",
        ),
    )

    nuclides = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-nuclides-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Parameter that defines the elements considered in the combinatorial "
            "search. The array contains nuclides as many times as their "
            "multiplicity and must not be empty. Nuclides are encoded using the "
            "hashing rule that is defined in by nuclide_hash of :ref:`NXatom`. "
            "Constraining the elements or nuclides instead of providing all "
            "nuclides reduces the time to perform an exhaustive combinatorial "
            "search."
        ),
        a_nexus_field=NeXusField(
            name="nuclides",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mass_to_charge_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-mass-to-charge-range-field"
        ],
        flexible_unit=True,
        shape=[2],
        description=(
            "Parameter that defines the interval :math:`[{\\frac{m}{q}}_{min}, "
            "{\\frac{m}{q}}_{max}]` within which ions with given "
            "mass-to-charge-state-ratio qualify as candidates."
        ),
        a_nexus_field=NeXusField(
            name="mass_to_charge_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    min_half_life = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-min-half-life-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Parameter that defines the minimum half life for how long each "
            "nuclide of each ion needs to be stable such that the ion qualifies "
            "as a candidate."
        ),
        a_nexus_field=NeXusField(
            name="min_half_life",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    min_abundance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-min-abundance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Parameter that defines the minimum natural abundance of each "
            "nuclide of each ion such that the ion qualifies as a candidate."
        ),
        a_nexus_field=NeXusField(
            name="min_abundance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    sacrifice_isotopic_uniqueness = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_charge_state_analysis.html#nxapm_charge_state_analysis-config-sacrifice-isotopic-uniqueness-field"
        ],
        description=(
            "If the value is false, it means that non-unique solutions are "
            "accepted. These are solutions where multiple candidates have been "
            "built from different nuclide instances but the charge_state of all "
            "the ions is the same."
        ),
        a_nexus_field=NeXusField(
            name="sacrifice_isotopic_uniqueness",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
