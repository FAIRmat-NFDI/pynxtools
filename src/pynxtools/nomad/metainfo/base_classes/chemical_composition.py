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
# Run `pynx nomad generate-metainfo --nxdl NXchemical_composition` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ChemicalComposition"]


class ChemicalComposition(Object):
    """
    Chemical composition of a sample or a set of things.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXchemical_composition",
            category="base",
            symbols={"n": "The number of samples or things."},
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.chemical_composition.ChemicalCompositionAtom",
        repeats=True,
        variable=True,
        description=(
            "If this group is used to report the composition of elements from "
            "the periodic table, the group should use the chemical symbol of "
            "that element. For other case the group name is unconstrained."
        ),
    )

    normalization = Quantity(
        type=MEnum(["atom_percent", "weight_percent"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-normalization-field"
        ],
        description=(
            "Reporting compositions as atom and weight percent yields both "
            "dimensionless quantities but their conceptual interpretation "
            "differs. A normalization based on atom_percent counts relative to "
            "the total number of atoms which are of a particular type. By "
            "contrast, weight_percent normalization factorizes in the respective "
            "mass of the elements. Software libraries that work with units, like "
            "pint in Python, are challenged by these differences as at.-% and "
            "wt.-% are both fractional quantities."
        ),
        a_nexus_field=NeXusField(
            name="normalization",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["atom_percent", "weight_percent"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    total = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-total-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Total formula mass or number of atoms, depending on the "
            "normalization stated in the normalization field."
        ),
        a_nexus_field=NeXusField(
            name="total",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
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


class ChemicalCompositionAtom(Atom):
    """
    If this group is used to report the composition of elements from the
    periodic table, the group should use the chemical symbol of that element.
    For other case the group name is unconstrained.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-element-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    amount = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-element-amount-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Count or weight which, when divided by total yields the composition "
            "of this element, isotope, molecule, or ion."
        ),
        a_nexus_field=NeXusField(
            name="amount",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    composition = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-element-composition-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Composition value for the element/ion referred to under name. "
            "Composition is reported either normalized for atomic or weight "
            "percent. The field normalization should be used to communicate this "
            "explicitly. Composition should be reported consistently for all "
            "instances ELEMENT."
        ),
        a_nexus_field=NeXusField(
            name="composition",
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
    composition_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXchemical_composition.html#nxchemical_composition-element-composition-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Magnitude of the standard deviation of the composition."),
        a_nexus_field=NeXusField(
            name="composition_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
