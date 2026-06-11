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
# Run `pynx nomad generate-metainfo --nxdl NXxlaue` to regenerate.
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
from pynxtools.nomad.metainfo.applications.xrot import Xrot
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xlaue"]


class Xlaue(Xrot):
    """
    raw data from a single crystal laue camera, extends :ref:`NXxrot`

    This is the application definition for raw data from a single crystal laue
    camera. It extends :ref:`NXxrot`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxlaue",
            category="application",
            symbols={"nE": "Number of energies"},
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xlaue.XlaueInstrument",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXxlaue"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxlaue"],
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
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


class XlaueInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xlaue.XlaueInstrumentSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XlaueInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-instrument-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xlaue.XlaueInstrumentSourceDistribution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="distribution",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XlaueInstrumentSourceDistribution(Data):
    """
    This is the wavelength distribution of the beam
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-instrument-source-distribution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="distribution",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-instrument-source-distribution-data-field"
        ],
        shape=["*"],
        description=('expect ``signal=1 axes="energy"``'),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxlaue.html#nxxlaue-entry-instrument-source-distribution-wavelength-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
