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
# Run `pynx nomad generate-metainfo --nxdl NXoff_geometry` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OffGeometry"]


class OffGeometry(Object):
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
