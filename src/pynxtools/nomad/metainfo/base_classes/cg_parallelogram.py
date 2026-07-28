# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcg_parallelogram (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXcg_parallelogram` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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

__all__ = ["CgParallelogram"]


class CgParallelogram(CgPrimitive):
    """
    Computational geometry description of a set of parallelograms.

    This class can also be used to describe rectangles or squares, irrespective
    whether these are axis-aligned or not. The class represents different
    access and description levels to embrace applied scientists and
    computational geometry experts with their different views:

    * The simplest case is the communication of dimensions aka the size of a
    region of interest in the 2D plane. In this case, communicating the
    alignment with axes is maybe not as relevant as it is to report the area of
    the ROI. * In other cases the extent of the parallelogram is relevant
    though. * Finally, in CAD models it should be possible to specify the
    polygons which the parallelograms represent with exact numerical details.

    Parallelograms are important geometrical primitives as their usage for
    describing many scanning experiments shows where typically
    parallelogram-shaped ROIs are scanned across the surface of a sample.

    The term parallelogram will be used throughout this base class thus
    including the important special cases rectangle, square, 2D box,
    axis-aligned bounding box (AABB), or optimal bounding box (OBB) as
    analogous 2D variants to their 3D counterparts. See :ref:`NXcg_hexahedron`
    for the generalization in 3D.

    An axis-aligned bounding box is a common data object in computational
    science and simulation codes to represent a rectangle whose edges are
    aligned with the axes of a coordinate system. As a part of binary trees
    AABBs are important data objects for executing time- as well as
    space-efficient queries of geometric primitives in techniques like
    kd-trees.

    An optimal bounding box is a common data object which provides the best,
    i.e. most tightly fitting box about an arbitrary object. In general such
    boxes are rotated. Other than in 3D dimensions, the rotation caliper method
    offers a rigorous approach to compute an optimal bounding box to a point
    set in 2D.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_parallelogram.html#nxcg_parallelogram"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_parallelogram",
            category="base",
            symbols={
                "c": "The cardinality of the set, i.e. the number of parallelograms."
            },
        ),
    )

    parallelograms = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=False,
        description=("Combined storage of all parallelograms."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="parallelograms",
            name_type="specified",
            optionality="optional",
        ),
    )
    parallelogramID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure.CgFaceListDataStructure",
        repeats=True,
        variable=True,
        description=("Individual storage of each parallelogram."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="parallelogramID",
            name_type="partial",
            optionality="optional",
        ),
    )

    is_rectangle = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_parallelogram.html#nxcg_parallelogram-is-rectangle-field"
        ],
        shape=["*"],
        description=("To specify which parallelogram is a rectangle."),
        a_nexus_field=NeXusField(
            name="is_rectangle",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    is_axis_aligned = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_parallelogram.html#nxcg_parallelogram-is-axis-aligned-field"
        ],
        shape=["*"],
        description=(
            "Only to be used if is_rectangle is present. In this case, this "
            "field describes whether parallelograms are rectangles whose primary "
            "edges are parallel to the axes of the coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="is_axis_aligned",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
