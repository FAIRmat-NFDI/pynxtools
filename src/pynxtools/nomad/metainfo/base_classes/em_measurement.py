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
# Run `pynx nomad generate-metainfo --nxdl NXem_measurement` to regenerate.
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

__all__ = ["EmMeasurement"]


class EmMeasurement(Object):
    """
    Base class for documenting a measurement with an electron microscope.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_measurement.html#nxem_measurement"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_measurement",
            category="base",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_instrument.EmInstrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name="instrument",
            name_type="specified",
            optionality="optional",
        ),
    )
    eventID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_event_data.EmEventData",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_event_data",
            name="eventID",
            name_type="partial",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
