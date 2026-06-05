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
# Run `pynx nomad generate-metainfo --nx-class NXsubsampling_filter` to regenerate.
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

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
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
        description=("Minimum index."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="min",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    increment = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter-increment-field"
        ],
        dimensionality="dimensionless",
        description=("Increment."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="increment",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    max = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsubsampling_filter.html#nxsubsampling_filter-max-field"
        ],
        dimensionality="dimensionless",
        description=("Maximum index."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="max",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
