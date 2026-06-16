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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_slip_system` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureSlipSystem"]


class MicrostructureSlipSystem(Object):
    """
    Base class for describing a set of crystallographic slip systems.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_slip_system.html#nxmicrostructure_slip_system"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_slip_system",
            category="base",
            symbols={
                "n": "Number of slip systems.",
                "m": "Number of indices used for reporting Miller (3) or Miller-Bravais indices (4).",
            },
        ),
    )

    lattice_type = Quantity(
        type=MEnum(
            [
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "trigonal",
                "hexagonal",
                "cubic",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_slip_system.html#nxmicrostructure_slip_system-lattice-type-field"
        ],
        description=("Bravais lattice type"),
        a_nexus_field=NeXusField(
            name="lattice_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "trigonal",
                "hexagonal",
                "cubic",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    miller_plane = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_slip_system.html#nxmicrostructure_slip_system-miller-plane-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Array of Miller indices which describe the crystallographic planes."
        ),
        a_nexus_field=NeXusField(
            name="miller_plane",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    miller_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_slip_system.html#nxmicrostructure_slip_system-miller-direction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Array of Miller or Miller-Bravais indices that describe the "
            "crystallographic direction."
        ),
        a_nexus_field=NeXusField(
            name="miller_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    is_specific = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_slip_system.html#nxmicrostructure_slip_system-is-specific-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "For each slip system a marker whether the Miller indices refer to a "
            "specific slip system or to a set of equivalent crystallographic "
            "slip systems."
        ),
        a_nexus_field=NeXusField(
            name="is_specific",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
