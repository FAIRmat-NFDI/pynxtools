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
# Run `pynx nomad generate-metainfo --nx-class NXbeam_stop` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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

__all__ = ["BeamStop"]


class BeamStop(Component):
    """
    A device that blocks the beam completely, usually to protect a detector.

    Beamstops and their positions are important for SANS and SAXS experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXbeam_stop",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("engineering shape, orientation and position of the beam stop."),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the beamstop and NXoff_geometry to describe its shape instead",
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
    cylindrical_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cylindrical_geometry.CylindricalGeometry",
        repeats=True,
        variable=True,
        description=(
            "This group is an alternative to NXoff_geometry for describing the "
            "shape of the beam stop."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcylindrical_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    description_quantity = Quantity(
        type=MEnum(["circular", "rectangular"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-description-field"
        ],
        description=("description of beamstop"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["circular", "rectangular"],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-size-field"
        ],
        dimensionality="[length]",
        description=(
            "Size of beamstop. If this is not sufficient to describe the beam "
            "stop use NXoff_geometry instead."
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-x-field"
        ],
        dimensionality="[length]",
        description=(
            "x position of the beamstop in relation to the detector. Note, it is "
            "recommended to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-y-field"
        ],
        dimensionality="[length]",
        description=(
            "y position of the beamstop in relation to the detector. Note, it is "
            "recommended to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    distance_to_detector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-distance-to-detector-field"
        ],
        dimensionality="[length]",
        description=(
            "distance of the beamstop to the detector. Note, it is recommended "
            "to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance_to_detector",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    status = Quantity(
        type=MEnum(["in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-status-field"
        ],
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["in", "out"],
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_stop.html#nxbeam_stop-depends-on-field"
        ],
        description=(
            "The reference point of the beam stop is its center in the x and y "
            "axis. The reference point on the z axis is the surface of the beam "
            "stop pointing towards the source. .. image:: "
            "beam_stop/beam_stop.png :width: 40%"
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
