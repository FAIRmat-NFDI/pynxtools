# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXmatch_filter (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXmatch_filter` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    match = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmatch_filter.html#nxmatch_filter-match-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
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
