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
# Run `pynx nomad generate-metainfo --nxdl NXmatch_filter` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MatchFilter"]


class MatchFilter(Parameters):
    """
    Base class of a filter to select members of a set based on their
    identifier.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmatch_filter.html#nxmatch_filter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmatch_filter",
            category="base",
            symbols={
                "n_values": "How many different match values does the filter specify."
            },
        ),
    )

    method = Quantity(
        type=MEnum(["whitelist", "blacklist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmatch_filter.html#nxmatch_filter-method-field"
        ],
        description=(
            "Definition of the logic what the filter yields: * Whitelist "
            "specifies which entries with said value to include. Entries with "
            "all other values will be excluded. * Blacklist specifies which "
            "entries with said value to exclude. Entries with all other values "
            "will be included."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["whitelist", "blacklist"],
        ),
    )
    match = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmatch_filter.html#nxmatch_filter-match-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Array of values to filter according to method. If the match e.g. "
            "specifies [1, 5, 6] and method is set to whitelist, only entries "
            "with values matching 1, 5 or 6 will be processed. All other entries "
            "will be excluded."
        ),
        a_nexus_field=NeXusField(
            name="match",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
