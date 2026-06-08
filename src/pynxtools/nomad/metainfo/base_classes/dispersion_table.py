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
# Run `pynx nomad generate-metainfo --nxdl NXdispersion_table` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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

__all__ = ["DispersionTable"]


class DispersionTable(Object):
    """
    A dispersion table denoting energy, dielectric function tabulated values.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdispersion_table",
            category="base",
            symbols={"n_points": "The number of energy and dielectric function points"},
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-convention-field"
        ],
        description=("The sign convention being used (n + or - ik)"),
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-wavelength-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "The wavelength array of the tabulated dataset. This is essentially "
            "a duplicate of the energy field. There should be one or both of "
            "them present."
        ),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=(
            "The energy array of the tabulated dataset. This is essentially a "
            "duplicate of the wavelength field. There should be one or both of "
            "them present."
        ),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    refractive_index = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-refractive-index-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("The refractive index array of the tabulated dataset."),
        a_nexus_field=NeXusField(
            name="refractive_index",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    dielectric_function = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_table.html#nxdispersion_table-dielectric-function-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("The dielectric function of the tabulated dataset."),
        a_nexus_field=NeXusField(
            name="dielectric_function",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
