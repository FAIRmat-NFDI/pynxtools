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
# Run `pynx nomad generate-metainfo --nxdl NXatom` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Atom"]


class Atom(Object):
    """
    Base class for documenting a set of atoms.

    Atoms in the set may be bonded. The set may have a net charge to represent
    an ion. An ion can be a molecular ion.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXatom",
            category="base",
            symbols={
                "n_pos": "Number of atom positions.",
                "d": "Dimensionality",
                "n_ivec_max": "Maximum number of atoms/isotopes allowed per ion.",
                "n_ranges": "Number of mass-to-charge-state-ratio range intervals for ion type.",
            },
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-name-field"
        ],
        description=(
            "Given name for the set. This field could for example be used in the "
            "research field of atom probe tomography to store a standardized "
            "human-readable name of the element or ion like such as Al +++ or "
            "12C +."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Given numerical identifier for the set. The identifier zero is "
            "reserved for the special unknown ion type."
        ),
        a_nexus_field=NeXusField(
            name="id",
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
    identifier_chemical = Quantity(
        type=MEnum(["inchi"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-identifier-chemical-field"
        ],
        description=(
            "Identifier used to refer to if the set of atoms represents a substance."
        ),
        a_nexus_field=NeXusField(
            name="identifier_chemical",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["inchi"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="inchi",
        ),
    )
    charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-charge-field"
        ],
        dimensionality="[current] * [time]",
        unit="coulomb",
        description=(
            "Signed net (partial) charge of the (molecular) ion. Different "
            "methods for computing charge are in use. Care needs to be exercised "
            "with respect to the integration. `T. A. Manz <10.1039/c6ra04656h>`_ "
            "and `N. G. Limas <10.1039/C6RA05507A>`_ discuss computational "
            "details."
        ),
        a_nexus_field=NeXusField(
            name="charge",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CHARGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "coulomb"},
    )
    charge_state = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-charge-state-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Charge reported in multiples of the charge of an electron. For "
            "research using atom probe tomography the value should be set to "
            "zero if the charge_state is unknown and irrecoverable. This can "
            "happen when classical ranging definition files in formats like RNG, "
            "RRNG are used. These file formats do not document the charge state "
            "explicitly but only the number of atoms of each element per "
            "molecular ion surplus the respective mass-to-charge-state-ratio "
            "interval. Details on ranging definition files in the literature are "
            "`M. K. Miller <https://doi.org/10.1002/sia.1719>`_."
        ),
        a_nexus_field=NeXusField(
            name="charge_state",
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
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        description=(
            "Assumed volume affected by the set of atoms. Neither individual "
            "atoms nor a set of cluster of these have a volume that is unique as "
            "a some cut-off criterion is required."
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m ** 3"},
    )
    indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-indices-field"
        ],
        shape=["*"],
        description=(
            "Index for each atom at locations as detailed by position. Indices "
            "can be used as identifier and thus names for individual atoms."
        ),
        a_nexus_field=NeXusField(
            name="indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-type-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Nuclide information for each atom at locations as detailed by "
            "position. One `approach "
            "<https://doi.org/10.1017/S1431927621012241>`_ for storing nuclide "
            "information efficiently is via individual hash values. Consult the "
            "docstring of ``nuclide_hash`` for further details."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-position-field"
        ],
        shape=["*", "*"],
        description=("Position of each atom."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    position__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-position-depends-on-attribute"
        ],
        description=(
            "Path to an instance of :ref:`NXcoordinate_system` to document the "
            "reference frame in which the positions are defined. This resolves "
            "ambiguity when the reference frame is different to the NeXus "
            "default reference frame (McStas)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="position",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    occupancy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-occupancy-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Relative occupancy of the atom position. This field is useful for "
            "specifying the atomic motif in instances of :ref:`NXunit_cell`."
        ),
        a_nexus_field=NeXusField(
            name="occupancy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Vector of nuclide hash values. The vector is sorted in decreasing "
            "order. Individual hash values :math:`H` `encode "
            "<https://doi.org/10.1017/S1431927621012241>`_ for each nuclide or "
            "element the number of protons :math:`Z` and a constant :math:`c` "
            "via the following hashing rule :math:`H = Z + c \\cdot 256`. "
            ":math:`Z` and :math:`c` must be 8-bit unsigned integers. The "
            "constant :math:`c` is either set to number of neutrons :math:`N` or "
            "to the special value 255. The special value 255 is used to refer to "
            "all isotopes of an element from the IUPAC periodic table. Some "
            "examples: * The element hydrogen (meaning irrespective which "
            "isotope), its hash value is :math:`H = 1 + 255 \\cdot 256 = 65281`. "
            "* The :math:`^{1}H` hydrogen isotope (:math:`Z = 1, N = 0`), its "
            "hash value is :math:`H = 1 + 0 \\cdot 256 = 1`. * The :math:`^{2}H` "
            "deuterium isotope (:math:`Z = 1, N = 1`), its hash value is "
            ":math:`H = 1 + 1 \\cdot 256 = 257`. * The :math:`^{3}H` tritium "
            "isotope (:math:`Z = 1, N = 2`), its hash value is :math:`H = 1 + 2 "
            "\\cdot 256 = 513`. * The :math:`^{99}Tc` technetium isotope "
            "(:math:`Z = 43, N = 56`), its hash value is :math:`H = 43 + 56 "
            "\\cdot 256 = 14379`. The special hash value :math:`0` is a "
            "placeholder. This hashing rule implements a bitshift operation. The "
            "benefit is that this enables encoding of all currently known "
            "nuclides and elements efficiently into an 16-bit unsigned integer. "
            "Sufficient unused indices remain to case situations when new "
            "elements will be discovered."
        ),
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    nuclide_list = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-nuclide-list-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        description=(
            "Table which decodes the entries in nuclide_hash into a "
            "human-readable matrix instances for either nuclides or elements. "
            "Specifically, the first row specifies the nuclide mass number. When "
            "the nuclide_hash values are used this means the row should report "
            "the sum :math:`Z + N` or 0. The value 0 documents that an element "
            "from the IUPAC periodic table is meant. The second row specifies "
            "the number of protons :math:`Z`. The value 0 in this case documents "
            "a placeholder or that no element-specific information is relevant. "
            "Taking a carbon-14 nuclide as an example the mass number is 14. "
            "That is encoded as a column vector (14, 6). The array is stored "
            "matching the order of nuclide_hash."
        ),
        a_nexus_field=NeXusField(
            name="nuclide_list",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mass_to_charge_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXatom.html#nxatom-mass-to-charge-range-field"
        ],
        shape=["*", 2],
        description=(
            "Associated lower :math:`{\\frac{m}{q}}_{min}` and upper "
            ":math:`{\\frac{m}{q}}_{max}` bounds of the mass-to-charge-state "
            "ratio interval(s) :math:`[{\\frac{m}{q}}_{min}, "
            "{\\frac{m}{q}}_{max}]`. (boundaries inclusive). This field is "
            "primarily of interest for documenting :ref:`NXprocess` steps of "
            "indexing a ToF/mass-to-charge-state ratio histogram."
        ),
        a_nexus_field=NeXusField(
            name="mass_to_charge_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
