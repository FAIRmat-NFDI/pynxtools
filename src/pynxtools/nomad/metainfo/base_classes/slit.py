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
# Run `pynx nomad generate-metainfo --nx-class NXslit` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Slit"]


class Slit(Component):
    """
    A simple slit.

    For more complex geometries, :ref:`NXaperture` should be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXslit.html#nxslit"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXslit",
            category="base",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXslit.html#nxslit-depends-on-field"
        ],
        description=(
            "If desired the location of the slit can also be described relative "
            "to an NXbeam, which will allow a simple description of a "
            "non-centred slit. The reference plane of the slit is orthogonal to "
            "the z axis and includes the surface that is the entry surface of "
            "the slit. The reference point of the slit is the centre of the slit "
            "opening in the x and y axis on the reference plane. The reference "
            "point on the z axis is the reference plane. .. image:: "
            "slit/slit.png :width: 40%"
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    x_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXslit.html#nxslit-x-gap-field"
        ],
        dimensionality="[length]",
        description=(
            "Size of the gap opening in the first dimension of the local "
            "coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="x_gap",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXslit.html#nxslit-y-gap-field"
        ],
        dimensionality="[length]",
        description=(
            "Size of the gap opening in the second dimension of the local "
            "coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="y_gap",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
