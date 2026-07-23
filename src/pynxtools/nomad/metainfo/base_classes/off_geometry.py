# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXoff_geometry (see
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
# Run `pynx nomad generate-metainfo --nxdl NXoff_geometry` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import ArchiveSection
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

__all__ = ["OffGeometry"]


class OffGeometry(Object, ArchiveSection):
    """
    Geometry (shape) description. The format closely matches the Object File
    Format (OFF) which can be output by most CAD software. It can be used to
    describe the shape of any component, including detectors. In the case of
    detectors it can be used to define the shape of a single pixel, or, if the
    pixel shapes are non-uniform, to describe the shape of the whole detector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoff_geometry.html#nxoff_geometry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoff_geometry",
            category="base",
            symbols={
                "i": "number of vertices in the shape",
                "k": "number of faces in the shape",
                "l": "number faces which are detecting surfaces or form the boundary of\n        detecting volumes",
            },
        ),
    )

    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoff_geometry.html#nxoff_geometry-vertices-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        description=(
            "List of x,y,z coordinates for vertices. The origin of the "
            "coordinates is the position of the parent component, for example "
            "the NXdetector which the geometry describes. If the shape describes "
            "a single pixel for a detector with uniform pixel shape then the "
            "origin is the position of each pixel as described by the "
            "``x/y/z_pixel_offset`` datasets in ``NXdetector``."
        ),
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    winding_order = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoff_geometry.html#nxoff_geometry-winding-order-field"
        ],
        shape=["*"],
        description=(
            "List of indices of vertices in the ``vertices`` dataset to form "
            "each face, right-hand rule for face normal."
        ),
        a_nexus_field=NeXusField(
            name="winding_order",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoff_geometry.html#nxoff_geometry-faces-field"
        ],
        shape=["*"],
        description=("The start index in ``winding_order`` for each face."),
        a_nexus_field=NeXusField(
            name="faces",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    detector_faces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoff_geometry.html#nxoff_geometry-detector-faces-field"
        ],
        shape=["*", 2],
        description=(
            'List of pairs of index in the "faces" dataset and detector id. '
            "Face IDs in the first column, and corresponding detector IDs in the "
            "second column. This dataset should only be used only if the "
            "``NXoff_geometry`` group is describing a detector. Note, the face "
            "indices must be in ascending order but need not be consecutive as "
            "not every face in faces need be a detecting surface or boundary of "
            "detecting volume. Can use multiple entries with the same detector "
            "id to define detector volumes."
        ),
        a_nexus_field=NeXusField(
            name="detector_faces",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
