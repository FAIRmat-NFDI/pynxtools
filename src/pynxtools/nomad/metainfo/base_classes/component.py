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
# Run `pynx nomad generate-metainfo --nxdl NXcomponent` to regenerate.
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

__all__ = ["Component"]


class Component(Object):
    """
    Base class for components of an instrument - real ones or simulated ones.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcomponent",
            category="base",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        description=(
            "Collection of axis-based translations and rotations to describe the "
            "location and geometry of the component in the instrument. The "
            "dependency chain may however traverse similar groups in other "
            "component groups."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-applied-field"
        ],
        description=("Was the component used?"),
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-name-field"
        ],
        description=("Name of the component."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-description-field"
        ],
        description=(
            "Ideally, use instances of ``identifierNAME`` to point to a resource "
            "that provides further details. If such a resource does not exist or "
            "should not be used, use this free text, although it is not "
            "recommended."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    inputs = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-inputs-field"
        ],
        description=(
            "Instance or list of instances of ``NXcomponent`` (or base classes "
            "extending ``NXcomponent``) or ``NXbeam`` that act as input(s) to "
            "this component. Each input should point to the path of the group "
            "acting as input. An example usage would be to chain components "
            "and/or beams together to describe the beam path in an experiment."
        ),
        a_nexus_field=NeXusField(
            name="inputs",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    outputs = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-outputs-field"
        ],
        description=(
            "Instance or list of instances of ``NXcomponent`` (or base classes "
            "extending ``NXcomponent``) or ``NXbeam`` that act as output(s) of "
            "this component. For more information, see :ref:`inputs "
            "</NXcomponent/inputs-field>`."
        ),
        a_nexus_field=NeXusField(
            name="outputs",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-depends-on-field"
        ],
        description=(
            "Specifies the position of the component by pointing to the last "
            "transformation in the transformation chain that is defined via the "
            "NXtransformations group. NeXus positions components by applying a "
            "set of translations and rotations to apply to the component "
            "starting from 0, 0, 0. The order of these operations is critical "
            "and forms what NeXus calls a dependency chain. The depends_on field "
            "defines the path to the top most operation of the dependency chain "
            'or the string "." if located in the origin. Usually these '
            "operations are stored in a NXtransformations group. But NeXus "
            "allows them to be stored anywhere."
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
