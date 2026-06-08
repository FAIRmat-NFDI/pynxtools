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
# Run `pynx nomad generate-metainfo --nxdl NXdispersion_repeated_parameter` to regenerate.
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

__all__ = ["DispersionRepeatedParameter"]


class DispersionRepeatedParameter(Object):
    """
    A repeated parameter for a dispersion function
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_repeated_parameter.html#nxdispersion_repeated_parameter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdispersion_repeated_parameter",
            category="base",
            symbols={"n_repetitions": "The number of parameter repetitions"},
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_repeated_parameter.html#nxdispersion_repeated_parameter-name-field"
        ],
        description=("The name of the parameter"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_repeated_parameter.html#nxdispersion_repeated_parameter-description-field"
        ],
        description=("A description of what this parameter represents"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    parameter_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_repeated_parameter.html#nxdispersion_repeated_parameter-parameter-units-field"
        ],
        shape=["*"],
        description=(
            "A unit array associating a unit with each parameter. The first "
            "element should be equal to values/@unit. The values should be SI "
            "interpretable standard units with common prefixes (e.g. micro, nano "
            "etc.) or their short-hand notation (e.g. nm, mm, kHz etc.)."
        ),
        a_nexus_field=NeXusField(
            name="parameter_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_repeated_parameter.html#nxdispersion_repeated_parameter-values-field"
        ],
        shape=["*"],
        description=("The value of the parameter"),
        a_nexus_field=NeXusField(
            name="values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
