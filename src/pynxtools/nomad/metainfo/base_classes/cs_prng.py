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
# Run `pynx nomad generate-metainfo --nxdl NXcs_prng` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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

__all__ = ["CsPrng"]


class CsPrng(Object):
    """
    Computer science description of pseudo-random number generator.

    The purpose of this base class is to identify if exactly the same sequence
    can be reproduced, like for a PRNG or not, like for a true physically
    random source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_prng.html#nxcs_prng"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_prng",
            category="base",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        description=(
            "Name of the PRNG implementation and version. If such information is "
            "not available or if the PRNG type was set to other the DOI to the "
            "publication or the source code should be given."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["physical", "system_clock", "mt19937", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_prng.html#nxcs_prng-type-field"
        ],
        description=(
            "Physical approach or algorithm whereby random numbers are "
            "generated. Different approaches for generating random numbers with "
            "a computer exists. Some use a dedicated physical device whose the "
            "state is unpredictable physically. Some use a strategy of mangling "
            "information from the system clock. Also in this case the sequence "
            "is not reproducible without having additional pieces of "
            "information. In most cases though so-called pseudo-random number "
            "generator (PRNG) algorithms are used. These yield a deterministic "
            "sequence of practically randomly appearing numbers. These "
            "algorithms differ in their quality in how random the resulting "
            "sequences actually are, i.e. sequentially uncorrelated. Nowadays "
            "one of the most commonly used algorithm is the MersenneTwister "
            "(mt19937)."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["physical", "system_clock", "mt19937", "other"],
        ),
    )
    seed = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_prng.html#nxcs_prng-seed-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Parameter of the PRNG controlling its initialization and thus "
            "controlling the specific sequence generated."
        ),
        a_nexus_field=NeXusField(
            name="seed",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    warmup = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_prng.html#nxcs_prng-warmup-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Number of initial draws from the PRNG after its initialized with "
            "the seed. These initial draws are typically discarded in an effort "
            "to equilibrate the sequence. If no warmup was performed or if "
            "warmup procedures are unclear, users should set the value to zero."
        ),
        a_nexus_field=NeXusField(
            name="warmup",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
