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
# Run `pynx nomad generate-metainfo --nxdl NXcg_polyline` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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

__all__ = ["CgPolyline"]


class CgPolyline(CgPrimitive):
    """
    Computational geometry description of a set of polylines.

    Each polyline is built from a sequence of vertices (points with
    identifiers). Each polyline must have a start and an end point. The
    sequence describes the traversal along the polyline when walking from the
    first to the last vertex.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_polyline",
            category="base",
            symbols={
                "d": "The dimensionality, which has to be at least 1.",
                "c": "The cardinality of the set, i.e. the number of polylines.",
                "n_v": "The number of vertices, supporting the polylines.",
                "n_total": "The total number of vertices traversed when visiting every polyline.",
            },
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-depends-on-field"
        ],
        description=(
            "Reference to an instance of :ref:`NXcg_point` which defines the "
            "location of the vertices that are referred to in this NXcg_polyline "
            "instance."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    number_of_unique_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-number-of-unique-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The total number of vertices that have different positions."),
        a_nexus_field=NeXusField(
            name="number_of_unique_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    number_of_total_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-number-of-total-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The total number of vertices, irrespective of their eventual uniqueness."
        ),
        a_nexus_field=NeXusField(
            name="number_of_total_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    number_of_vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-number-of-vertices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The total number of vertices of each polyline, irrespectively "
            "whether vertices are shared by vertices or not."
        ),
        a_nexus_field=NeXusField(
            name="number_of_vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-vertices-field"
        ],
        shape=["*", "*"],
        description=(
            "Positions of the vertices which support the members of the polyline "
            "set. Users are encouraged to reduce the vertices to unique "
            "positions and vertices as this often supports with storing geometry "
            "data more efficiently. It is also possible though to store the "
            "vertex positions naively in which case vertices_are_unique is "
            "likely False. Naively, here means that one stores each vertex of a "
            "triangle mesh even though many vertices are shared between "
            "triangles and thus storing multiple copies of their positions is "
            "redundant."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    vertices_are_unique = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-vertices-are-unique-field"
        ],
        description=(
            "If true indicates that the vertices are all placed at different "
            "positions and have different identifiers, i.e. no points overlap or "
            "are counted several times."
        ),
        a_nexus_field=NeXusField(
            name="vertices_are_unique",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    polylines = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_polyline.html#nxcg_polyline-polylines-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Sequence of identifier for vertices how they build each polyline. A "
            "trivial example is a set with two polylines with three vertices "
            "each. If the polylines meet at a vertex (assume for example that "
            "the second vertex is shared and marking the junction between the "
            "two polylines), it is possible that there are only five unique "
            "positions. This suggests to store five unique vertices. A "
            "non-trivial example is a set with several polylines. Assume that "
            "each has a different number of vertices. The array stores the "
            "identifier of the vertices in the sequence how the polylines are "
            "visited: The first entry is the identifier of the first vertex of "
            "the first polyline, followed by the second vertex of the first "
            "polyline, until the last vertex of the first polyline. Thereafter, "
            "the first vertex of the second polyline, and so on and so forth. "
            "Using the (cumulated) counts in number_of_vertices (:math:`n^v_i`), "
            "the vertices of the N-th polyline can be accessed on the array "
            "index interval :math:`[\\sum_{i=0}^{i=N-1} n^v_i, \\sum_{i=0}^{i=N} "
            "n^v_i]`."
        ),
        a_nexus_field=NeXusField(
            name="polylines",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
