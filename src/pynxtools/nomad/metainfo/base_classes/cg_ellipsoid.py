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
# Run `pynx nomad generate-metainfo --nxdl NXcg_ellipsoid` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgEllipsoid"]


class CgEllipsoid(CgPrimitive):
    """
    Computational geometry description of a set of ellipsoids.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_ellipsoid",
            category="base",
            symbols={
                "d": "The dimensionality of the space in which the members are assumed embedded.",
                "c": "The cardinality of the set, i.e. the number of members.",
            },
        ),
    )

    semi_axes_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-semi-axes-value-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Length of the semi-axes (e.g. semi-major and semi-minor "
            "respectively for an ellipse). Use if all ellipsoids in the set have "
            "the same half-axes."
        ),
        a_nexus_field=NeXusField(
            name="semi_axes_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    semi_axes_values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-semi-axes-values-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Length of the semi-axes if ellipsoids have individually different lengths."
        ),
        a_nexus_field=NeXusField(
            name="semi_axes_values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("In the case that all ellipsoids are spheres."),
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_ellipsoid.html#nxcg_ellipsoid-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "In the case that all ellipsoids are spheres whose radii differ. For "
            "a mixture of spheres use semi_axes_values."
        ),
        a_nexus_field=NeXusField(
            name="radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
