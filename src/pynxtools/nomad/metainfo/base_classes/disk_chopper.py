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
# Run `pynx nomad generate-metainfo --nxdl NXdisk_chopper` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["DiskChopper"]


class DiskChopper(Component):
    """
    A device blocking the beam in a temporal periodic pattern.

    A disk which blocks the beam but has one or more slits to periodically let
    neutrons through as the disk rotates. Often used in pairs, one
    NXdisk_chopper should be defined for each disk.

    The rotation of the disk is commonly monitored by recording a timestamp for
    each full rotation of disk, by having a sensor in the stationary disk
    housing sensing when it is aligned with a feature (such as a magnet) on the
    disk. We refer to this below as the "top-dead-center signal".

    Angles and positive rotation speeds are measured in an anticlockwise
    direction when facing away from the source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdisk_chopper",
            category="base",
            symbols={"n": "Number of slits in the disk"},
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the chopper and NXoff_geometry to describe its shape instead",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    type = Quantity(
        type=MEnum(["Chopper type single", "contra_rotating_pair", "synchro_pair"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-type-field"
        ],
        description=(
            "Type of the disk-chopper: only one from the enumerated list (match "
            "text exactly)"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Chopper type single", "contra_rotating_pair", "synchro_pair"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    rotation_speed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-rotation-speed-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "Chopper rotation speed. Positive for anticlockwise rotation when "
            "facing away from the source, negative otherwise."
        ),
        a_nexus_field=NeXusField(
            name="rotation_speed",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    slits = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-slits-field"
        ],
        description=("Number of slits"),
        a_nexus_field=NeXusField(
            name="slits",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    slit_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-slit-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Angular opening"),
        a_nexus_field=NeXusField(
            name="slit_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    pair_separation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-pair-separation-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Disk spacing in direction of beam"),
        a_nexus_field=NeXusField(
            name="pair_separation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    slit_edges = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-slit-edges-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Angle of each edge of every slit from the position of the "
            "top-dead-center timestamp sensor, anticlockwise when facing away "
            "from the source. The first edge must be the opening edge of a slit, "
            "thus the last edge may have an angle greater than 360 degrees."
        ),
        a_nexus_field=NeXusField(
            name="slit_edges",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    top_dead_center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-top-dead-center-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Timestamps of the top-dead-center signal. The times are relative to "
            'the "start" attribute and in the units specified in the "units" '
            "attribute. Please note that absolute timestamps under unix are "
            "relative to ``1970-01-01T00:00:00.0Z``."
        ),
        a_nexus_field=NeXusField(
            name="top_dead_center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    top_dead_center__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-top-dead-center-start-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="top_dead_center",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    beam_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-beam-position-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angular separation of the center of the beam and the "
            "top-dead-center timestamp sensor, anticlockwise when facing away "
            "from the source."
        ),
        a_nexus_field=NeXusField(
            name="beam_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Radius of the disk"),
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    slit_height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-slit-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Total slit height"),
        a_nexus_field=NeXusField(
            name="slit_height",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-phase-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Chopper phase angle"),
        a_nexus_field=NeXusField(
            name="phase",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-delay-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time difference between timing system t0 and chopper driving clock signal"
        ),
        a_nexus_field=NeXusField(
            name="delay",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    ratio = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-ratio-field"
        ],
        description=(
            "Pulse reduction factor of this chopper in relation to other "
            "choppers/fastest pulse in the instrument"
        ),
        a_nexus_field=NeXusField(
            name="ratio",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Effective distance to the origin. Note, it is recommended to use "
            "NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-wavelength-range-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[2],
        description=("Low and high values of wavelength range transmitted"),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdisk_chopper.html#nxdisk_chopper-depends-on-field"
        ],
        description=(
            "The reference plane of the disk chopper includes the surface of the "
            "spinning disk which faces the source. The reference point in the x "
            "and y axis is the point on this surface which is the centre of the "
            "axle which the disk is spinning around. The reference plane is "
            "orthogonal to the z axis and its position is the reference point on "
            "that axis. Note: This reference point in almost all practical cases "
            "is not where the beam passes though. .. image:: "
            "disk_chopper/disk_chopper.png :width: 40%"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
