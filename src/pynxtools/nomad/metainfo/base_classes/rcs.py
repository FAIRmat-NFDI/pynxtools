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
# Run `pynx nomad generate-metainfo --nxdl NXrcs` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Rcs"]


class Rcs(Object):
    """
    A base class for the Real Time Control System (RCS).

    A real time control system (RCS) is a reference architecture model used to
    design highly task intensive software systems and computing control
    systems.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXrcs",
            category="base",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.rcs.RcsFabrication",
        repeats=False,
        description=("The fabrication information."),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-name-field"
        ],
        description=("The name of the real-time control system."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-description-field"
        ],
        description=("The description of the real-time control system."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-type-field"
        ],
        description=("The type of the real-time control system."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "The frequency of the real-time controller system which indicated "
            "the number of close-loop process (gathering data, process data and "
            "update system) control cycles per unit time."
        ),
        a_nexus_field=NeXusField(
            name="frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    measurement_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-measurement-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "The time of data measuring in a data lifecycle or process cycle."
        ),
        a_nexus_field=NeXusField(
            name="measurement_time",
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
    acquisition_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-acquisition-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Data acquisition time in single data lifecycle or process cycle of "
            "the real-time control system."
        ),
        a_nexus_field=NeXusField(
            name="acquisition_time",
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
    animation_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-animation-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "The time of data animation of single in a data lifecycle or process cycle."
        ),
        a_nexus_field=NeXusField(
            name="animation_time",
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
    indication_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-indication-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("The time of data indication of the end of process."),
        a_nexus_field=NeXusField(
            name="indication_time",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class RcsFabrication(Fabrication):
    """
    The fabrication information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    model = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXrcs.html#nxrcs-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
