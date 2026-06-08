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
# Run `pynx nomad generate-metainfo --nxdl NXsqom` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Sqom"]


class Sqom(Entry):
    """
    This is the application definition for S(Q,OM) processed data.

    As this kind of data is in general not on a rectangular grid after data
    reduction, it is stored as Q,E positions plus their intensity, table like.
    It is the task of a possible visualisation program to regrid this data in a
    sensible way.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsqom",
            category="application",
            symbols={"nP": "Number of points"},
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sqom.SqomInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sqom.SqomSample",
        repeats=True,
        variable=True,
    )
    reduction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sqom.SqomReduction",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sqom.SqomData",
        repeats=True,
        variable=True,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsqom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsqom"],
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


class SqomInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-instrument-name-field"
        ],
        description=("Name of the instrument from which this data was reduced."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SqomSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SqomReduction(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-reduction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="reduction",
            name_type="specified",
            optionality="required",
        ),
    )

    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-reduction-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-reduction-version-field"
        ],
        a_nexus_field=NeXusField(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SqomData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-data-field"
        ],
        shape=["*"],
        description=("This is the intensity for each point in QE"),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    qx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-qx-field"
        ],
        dimensionality="1 / [length]",
        shape=["*"],
        description=("Positions for the first dimension of Q"),
        a_nexus_field=NeXusField(
            name="qx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVENUMBER",
        ),
    )
    qy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-qy-field"
        ],
        dimensionality="1 / [length]",
        shape=["*"],
        description=("Positions for the the second dimension of Q"),
        a_nexus_field=NeXusField(
            name="qy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVENUMBER",
        ),
    )
    qz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-qz-field"
        ],
        dimensionality="1 / [length]",
        shape=["*"],
        description=("Positions for the the third dimension of Q"),
        a_nexus_field=NeXusField(
            name="qz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVENUMBER",
        ),
    )
    en = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXsqom.html#nxsqom-entry-data-en-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Values for the energy transfer for each point"),
        a_nexus_field=NeXusField(
            name="en",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
