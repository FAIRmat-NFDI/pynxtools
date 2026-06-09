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
# Run `pynx nomad generate-metainfo --nxdl NXenvironment` to regenerate.
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

__all__ = ["Environment"]


class Environment(Object):
    """
    Parameters for controlling external conditions
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXenvironment",
            category="base",
        ),
    )

    position = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        description=(
            "The position and orientation of the apparatus. Note, it is "
            "recommended to use NXtransformations instead."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="position",
            name_type="specified",
            optionality="optional",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        description=(
            "This is the group recommended for holding the chain of translation "
            "and rotation operations necessary to position the component within "
            "the instrument. The dependency chain may however traverse similar "
            "groups in other component groups."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=("Additional information, LabView logs, digital photographs, etc"),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        description=(
            "Any actuator used to control the environment. This can be linked to "
            "an actuator defined in an NXinstrument instance."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        description=(
            "Any sensor used to monitor the environment. This can be linked to a "
            "sensor defined in an NXinstrument instance."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-name-field"
        ],
        description=("Apparatus identification code/model number; e.g. OC100 011"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-short-name-field"
        ],
        description=(
            "Alternative short name, perhaps for dashboard display like a "
            "present Seblock name"
        ),
        a_nexus_field=NeXusField(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-type-field"
        ],
        description=(
            "Type of apparatus. This could be the SE codes in scheduling "
            "database; e.g. OC/100"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-description-field"
        ],
        description=(
            "Description of the apparatus; e.g. 100mm bore orange cryostat with "
            "Roots pump"
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-program-field"
        ],
        description=("Program controlling the apparatus; e.g. LabView VI name"),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-value-field"
        ],
        description=(
            "This is to be used if there is no actuator/sensor that "
            "controls/measures the environment parameters, but the user would "
            "still like to give a value for it. An example would be a room "
            "temperature experiment where the temperature is not actively "
            "measured, but rather estimated. Note that this method for recording "
            "the environment parameters is not advised, but using NXsensor and "
            "NXactuator is strongly recommended instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenvironment.html#nxenvironment-depends-on-field"
        ],
        description=(
            "NeXus positions components by applying a set of translations and "
            "rotations to apply to the component starting from 0, 0, 0. The "
            "order of these operations is critical and forms what NeXus calls a "
            "dependency chain. The depends_on field defines the path to the top "
            'most operation of the dependency chain or the string "." if '
            "located in the origin. Usually these operations are stored in a "
            "NXtransformations group. But NeXus allows them to be stored "
            "anywhere."
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
