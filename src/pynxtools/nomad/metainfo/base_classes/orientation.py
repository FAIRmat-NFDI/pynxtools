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
# Run `pynx nomad generate-metainfo --nxdl NXorientation` to regenerate.
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

__all__ = ["Orientation"]


class Orientation(Object):
    """
    legacy class - recommend to use :ref:`NXtransformations` now

    Description for a general orientation of a component - used by
    :ref:`NXgeometry`
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXorientation.html#nxorientation"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXorientation",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=(
            "Link to another object if we are using relative positioning, else absent"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXorientation.html#nxorientation-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 6],
        description=(
            "The orientation information is stored as direction cosines. The "
            "direction cosines will be between the local coordinate directions "
            "and the reference directions (to origin or relative NXgeometry). "
            "Calling the local unit vectors (x',y',z') and the reference unit "
            "vectors (x,y,z) the six numbers will be [x' dot x, x' dot y, x' dot "
            "z, y' dot x, y' dot y, y' dot z] where \"dot\" is the scalar dot "
            "product (cosine of the angle between the unit vectors). The unit "
            "vectors in both the local and reference coordinates are "
            "right-handed and orthonormal. The pair of groups NXtranslation and "
            "NXorientation together describe the position of a component."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
