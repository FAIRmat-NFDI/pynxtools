# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXsubsampling_filter (see
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
# Run `pynx nomad generate-metainfo --nxdl NXsubsampling_filter` to regenerate.
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

__all__ = ["SubsamplingFilter"]


class SubsamplingFilter(Parameters):
    r"""
    Base class of a filter to sample members in a set based on their indices.

    The filter defines three parameters: The minimum, the increment, and the
    maximum index of values to include of a sequence :math:`[i_0, i_0 + 1, i_0
    + 2, \ldots, i_0 + \mathcal{N}] with i_0 \in \mathcal{Z}` of indices. The
    increment controls which n-th index (value) to take.

    Take as an example a dataset with 100 indices (aka entries). Assume that
    the indices start at zero, i.e., index_offset is 0. Assume further that
    min, increment, max are set to 0, 1, and 99, respectively. In this case the
    filter will yield all indices. Setting min, increment, max to 0, 2, and 99,
    respectively will yield each second index value. Setting min, increment,
    max to 90, 3, and 99 respectively will yield each third index value
    beginning from index values 90 up to 99.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsubsampling_filter",
            category="base",
        ),
    )

    min = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter-min-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Minimum index."),
        a_nexus_field=NeXusField(
            name="min",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    increment = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter-increment-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Increment."),
        a_nexus_field=NeXusField(
            name="increment",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter-max-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Maximum index."),
        a_nexus_field=NeXusField(
            name="max",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
