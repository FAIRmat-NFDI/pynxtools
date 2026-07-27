# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcylindrical_geometry (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcylindrical_geometry` to regenerate.
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
