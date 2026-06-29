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
# Run `pynx nomad generate-metainfo --nxdl NXcg_unit_normal` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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

__all__ = ["CgUnitNormal"]


class CgUnitNormal(Object):
    """
    Computational geometry description of a set of (oriented) unit normal
    vectors.

    Store normal vector information as properties of primitives. Use only only
    as a child of an instance of :ref:`NXcg_primitive` so that this instance
    acts as the parent to define a context.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_unit_normal",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 2.",
                "c": "The cardinality of the set, i.e. the number of unit normals.",
            },
        ),
    )

    normals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal-normals-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Direction of each normal - a unit normal."),
        a_nexus_field=NeXusField(
            name="normals",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    orientation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_unit_normal.html#nxcg_unit_normal-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "An indicator which details the orientation of each normal vector in "
            "relation to its primitive, assuming the object is viewed from a "
            "position outside the object. * 0 - undefined * 1 - outer unit "
            "normal vector * 2 - inner unit normal vector"
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
