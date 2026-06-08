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
# Run `pynx nomad generate-metainfo --nxdl NXbending_magnet` to regenerate.
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

__all__ = ["BendingMagnet"]


class BendingMagnet(Component):
    """
    A bending magnet
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXbending_magnet",
            category="base",
        ),
    )

    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("bending magnet spectrum"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=('"Engineering" position of bending magnet'),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the bending magnet and NXoff_geometry to describe its shape instead",
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

    critical_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-critical-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        a_nexus_field=NeXusField(
            name="critical_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    bending_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-bending-radius-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="bending_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    magnetic_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-magnetic-field-field"
        ],
        dimensionality="[current]",
        description=("strength of magnetic field of dipole magnets"),
        a_nexus_field=NeXusField(
            name="magnetic_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    accepted_photon_beam_divergence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-accepted-photon-beam-divergence-field"
        ],
        dimensionality="[length]",
        description=(
            "An array of four numbers giving X+, X-, Y+ and Y- half divergence"
        ),
        a_nexus_field=NeXusField(
            name="accepted_photon_beam_divergence",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    source_distance_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-source-distance-x-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance of source point from particle beam waist in X (horizontal) "
            "direction. Note, it is recommended to use NXtransformations instead "
            "to place component."
        ),
        a_nexus_field=NeXusField(
            name="source_distance_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    source_distance_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-source-distance-y-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance of source point from particle beam waist in Y (vertical) "
            "direction. Note, it is recommended to use NXtransformations instead "
            "to place component."
        ),
        a_nexus_field=NeXusField(
            name="source_distance_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    divergence_x_plus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-divergence-x-plus-field"
        ],
        dimensionality="[angle]",
        description=(
            "Accepted photon beam divergence in X+ (horizontal outboard) "
            "direction. Note that divergence_x_plus+divergence_x_minus is the "
            "total horizontal beam divergence."
        ),
        a_nexus_field=NeXusField(
            name="divergence_x_plus",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    divergence_x_minus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-divergence-x-minus-field"
        ],
        dimensionality="[angle]",
        description=(
            "Accepted photon beam divergence in X- (horizontal inboard) "
            "direction. Note that divergence_x_plus+divergence_x_minus is the "
            "total horizontal beam divergence."
        ),
        a_nexus_field=NeXusField(
            name="divergence_x_minus",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    divergence_y_plus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-divergence-y-plus-field"
        ],
        dimensionality="[angle]",
        description=(
            "Accepted photon beam divergence in Y+ (vertical upward) direction. "
            "Note that divergence_y_plus+divergence_y_minus is the total "
            "vertical beam divergence."
        ),
        a_nexus_field=NeXusField(
            name="divergence_y_plus",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    divergence_y_minus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-divergence-y-minus-field"
        ],
        dimensionality="[angle]",
        description=(
            "Accepted photon beam divergence in Y- (vertical downward) "
            "direction. Note that divergence_y_plus+divergence_y_minus is the "
            "total vertical beam divergence."
        ),
        a_nexus_field=NeXusField(
            name="divergence_y_minus",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbending_magnet.html#nxbending_magnet-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a bending magnet."
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
