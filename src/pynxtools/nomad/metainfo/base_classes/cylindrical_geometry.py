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
# Run `pynx nomad generate-metainfo --nxdl NXcylindrical_geometry` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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

__all__ = ["CylindricalGeometry"]


class CylindricalGeometry(Object):
    """
    Geometry description for cylindrical shapes. This class can be used in
    place of ``NXoff_geometry`` when an exact representation for cylinders is
    preferred. For example, for Helium-tube, neutron detectors. It can be used
    to describe the shape of any component, including detectors. In the case of
    detectors it can be used to define the shape of a single pixel, or, if the
    pixel shapes are non-uniform, to describe the shape of the whole detector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcylindrical_geometry.html#nxcylindrical_geometry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcylindrical_geometry",
            category="base",
            symbols={
                "i": "number of vertices required to define all cylinders in the shape",
                "j": "number of cylinders in the shape",
                "k": "number cylinders which are detectors",
            },
        ),
    )

    vertices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcylindrical_geometry.html#nxcylindrical_geometry-vertices-field"
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
    cylinders = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcylindrical_geometry.html#nxcylindrical_geometry-cylinders-field"
        ],
        shape=["*", 3],
        description=(
            "List of indices of vertices in the ``vertices`` dataset to form "
            "each cylinder. Each cylinder is described by three vertices A, B, "
            "C. First vertex A lies on the cylinder axis and circular face, "
            "second point B on edge of the same face as A, and third point C at "
            "the other face and on axis."
        ),
        a_nexus_field=NeXusField(
            name="cylinders",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    detector_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcylindrical_geometry.html#nxcylindrical_geometry-detector-number-field"
        ],
        shape=["*"],
        description=("Maps cylinders in ``cylinder``, by index, with a detector id."),
        a_nexus_field=NeXusField(
            name="detector_number",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
