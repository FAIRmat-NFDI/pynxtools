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
# Run `pynx nomad generate-metainfo --nx-class NXattenuator` to regenerate.
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

__all__ = ["Attenuator"]


class Attenuator(Component):
    """
    A device that reduces the intensity of a beam by attenuation.

    If uncertain whether to use :ref:`NXfilter` (band-pass filter) or
    :ref:`NXattenuator` (reduces beam intensity), then choose
    :ref:`NXattenuator`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXattenuator",
            category="base",
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=False,
        description=(
            "Shape of this component. Particularly useful to define the origin "
            "for position and orientation in non-standard cases."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name="shape",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance from sample. Note, it is recommended to use "
            "NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-type-field"
        ],
        description=("Type or composition of attenuator, e.g. polythene"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of attenuator along beam direction"),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    scattering_cross_section = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-scattering-cross-section-field"
        ],
        dimensionality="[length] ** 2",
        description=("Scattering cross section (coherent+incoherent)"),
        a_nexus_field=NeXusField(
            name="scattering_cross_section",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CROSS_SECTION",
        ),
    )
    absorption_cross_section = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-absorption-cross-section-field"
        ],
        dimensionality="[length] ** 2",
        description=("Absorption cross section"),
        a_nexus_field=NeXusField(
            name="absorption_cross_section",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CROSS_SECTION",
        ),
    )
    attenuator_transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-attenuator-transmission-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The nominal amount of the beam that gets through (transmitted "
            "intensity)/(incident intensity)"
        ),
        a_nexus_field=NeXusField(
            name="attenuator_transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    status = Quantity(
        type=MEnum(["in", "out", "moving"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-status-field"
        ],
        description=("In or out or moving of the beam"),
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["in", "out", "moving"],
        ),
    )
    status__time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-status-time-attribute"
        ],
        description=("time stamp for this observation"),
        a_nexus_attribute=NeXusAttribute(
            name="time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="status",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXattenuator.html#nxattenuator-depends-on-field"
        ],
        description=(
            "The reference point of the attenuator is its center in the x and y "
            "axis. The reference point on the z axis is the surface of the "
            "attenuator pointing towards the source. In complex (asymmetric) "
            "geometries an NXoff_geometry group can be used to provide an "
            "unambiguous reference. .. image:: attenuator/attenuator.png :width: "
            "40%"
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
