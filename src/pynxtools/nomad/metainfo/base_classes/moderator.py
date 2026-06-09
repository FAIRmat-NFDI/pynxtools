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
# Run `pynx nomad generate-metainfo --nxdl NXmoderator` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Moderator"]


class Moderator(Component):
    """
    A neutron moderator
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmoderator",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=('"Engineering" position of moderator'),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the moderator and NXoff_geometry to describe its shape instead",
        ),
    )
    temperature_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("log file of moderator temperature"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="temperature_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    pulse_shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("moderator pulse shape"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_shape",
            name_type="specified",
            optionality="optional",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the moderator"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Effective distance as seen by measuring radiation. Note, it is "
            "recommended to use NXtransformations instead."
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
        type=MEnum(
            [
                "H20",
                "D20",
                "Liquid H2",
                "Liquid CH4",
                "Liquid D2",
                "Solid D2",
                "C",
                "Solid CH4",
                "Solid H2",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "H20",
                "D20",
                "Liquid H2",
                "Liquid CH4",
                "Liquid D2",
                "Solid D2",
                "C",
                "Solid CH4",
                "Solid H2",
            ],
        ),
    )
    poison_depth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-poison-depth-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="poison_depth",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coupled = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-coupled-field"
        ],
        description=("whether the moderator is coupled"),
        a_nexus_field=NeXusField(
            name="coupled",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    coupling_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-coupling-material-field"
        ],
        description=("The material used for coupling. Usually Cd."),
        a_nexus_field=NeXusField(
            name="coupling_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    poison_material = Quantity(
        type=MEnum(["Gd", "Cd"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-poison-material-field"
        ],
        a_nexus_field=NeXusField(
            name="poison_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Gd", "Cd"],
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-temperature-field"
        ],
        dimensionality="[temperature]",
        description=("average/nominal moderator temperature"),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmoderator.html#nxmoderator-depends-on-field"
        ],
        description=(
            "The reference point of the moderator is its center in the x and y "
            "axis. The reference point on the z axis is the surface of the "
            "moderator pointing towards the source (the negative part of the z "
            "axis). .. image:: moderator/moderator.png :width: 40%"
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
