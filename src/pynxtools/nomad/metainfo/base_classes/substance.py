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
# Run `pynx nomad generate-metainfo --nxdl NXsubstance` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Substance"]


class Substance(Object):
    """
    A form of matter with a constant, definite chemical composition.

    Examples can be single chemical elements, chemical compounds, or alloys.
    For further information, see
    https://en.wikipedia.org/wiki/Chemical_substance.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsubstance",
            category="base",
        ),
    )

    cas_image = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=("CAS REGISTRY image"),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="cas_image",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-name-field"
        ],
        description=("User-defined chemical name of the substance"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    molecular_mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-molecular-mass-field"
        ],
        dimensionality="[mass] / [substance]",
        description=("Molecular mass of the substance"),
        a_nexus_field=NeXusField(
            name="molecular_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MOLECULAR_WEIGHT",
        ),
    )
    molecular_formula_hill = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-molecular-formula-hill-field"
        ],
        description=(
            "The chemical formula specified using CIF conventions. Abbreviated "
            "version of CIF standard:107 This is the *Hill* system used by "
            "Chemical Abstracts. * Only recognized element symbols may be used. "
            "* Each element symbol is followed by a 'count' number. A count of "
            "'1' may be omitted. * A space or parenthesis must separate each "
            "cluster of (element symbol + count). * Where a group of elements is "
            "enclosed in parentheses, the multiplier for the group must follow "
            "the closing parentheses. That is, all element and group multipliers "
            "are assumed to be printed as subscripted numbers. * Unless the "
            "elements are ordered in a manner that corresponds to their chemical "
            "structure, the order of the elements within any group or moiety "
            "depends on whether or not carbon is present. * If carbon is "
            "present, the order should be: - C, then H, then the other elements "
            "in alphabetical order of their symbol. - If carbon is not present, "
            "the elements are listed purely in alphabetic order of their symbol."
        ),
        a_nexus_field=NeXusField(
            name="molecular_formula_hill",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_cas = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-cas-field"
        ],
        description=(
            "Unique CAS REGISTRY URI. For further information, see "
            "https://www.cas.org/."
        ),
        a_nexus_field=NeXusField(
            name="identifier_cas",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_cas__type = Quantity(
        type=MEnum(["URL"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-cas-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="identifier_cas",
            enumeration=["URL"],
        ),
    )
    identifier_cas__cas_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-cas-cas-number-attribute"
        ],
        description=("Numeric CAS REGISTRY number associated with this identifier."),
        a_nexus_attribute=NeXusAttribute(
            name="cas_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="identifier_cas",
        ),
    )
    identifier_cas__cas_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-cas-cas-name-attribute"
        ],
        description=("CAS REGISTRY name associated with this identifier."),
        a_nexus_attribute=NeXusAttribute(
            name="cas_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="identifier_cas",
        ),
    )
    identifier_inchi_str = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-inchi-str-field"
        ],
        description=(
            'Standard string InChi identifier" (as per v1.02). The InChI '
            "identifier expresses chemical structures in terms of atomic "
            "connectivity, tautomeric state, isotopes, stereochemistry and "
            "electronic charge in order to produce a string of machine-readable "
            "characters unique to the respective molecule. For further "
            "information, see "
            "https://iupac.org/who-we-are/divisions/division-details/inchi/."
        ),
        a_nexus_field=NeXusField(
            name="identifier_inchi_str",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_inchi_key = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-inchi-key-field"
        ],
        description=(
            "Condensed, 27 character InChI key. Hashed version of the full InChI "
            "(using the SHA-256 algorithm)."
        ),
        a_nexus_field=NeXusField(
            name="identifier_inchi_key",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_iupac_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-iupac-name-field"
        ],
        description=(
            "Name according to the IUPAC system (standard). For further "
            "information, see https://iupac.org/."
        ),
        a_nexus_field=NeXusField(
            name="identifier_iupac_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_smiles = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-smiles-field"
        ],
        description=(
            "Identifier in the SMILES (Simplified Molecular Input Line Entry "
            "System) system For further information, see "
            "https://www.daylight.com/smiles/."
        ),
        a_nexus_field=NeXusField(
            name="identifier_smiles",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_canonical_smiles = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-canonical-smiles-field"
        ],
        description=("Canonical version of the SMILES identifier"),
        a_nexus_field=NeXusField(
            name="identifier_canonical_smiles",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_pub_chem = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-pub-chem-field"
        ],
        description=(
            "Standard PubChem identifier (CID). The PubChem Compound Identifier "
            "(CID) is a unique numerical identifier assigned to a compound in "
            "the PubChem database, which contains information on the biological "
            "activities of small molecules. The CID allows users to access "
            "detailed data about compounds, including their chemical structure, "
            "molecular formula, and biological properties. For further "
            "information, see https://pubchem.ncbi.nlm.nih.gov/."
        ),
        a_nexus_field=NeXusField(
            name="identifier_pub_chem",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_pub_chem__pub_chem_link = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubstance.html#nxsubstance-identifier-pub-chem-pub-chem-link-attribute"
        ],
        description=("CAS REGISTRY name associated with this identifier."),
        a_nexus_attribute=NeXusAttribute(
            name="pub_chem_link",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="identifier_pub_chem",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
