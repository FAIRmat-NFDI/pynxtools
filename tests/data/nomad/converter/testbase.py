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
# Run `pynx nomad generate-metainfo --nxdl NXtestBase` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Testbase"]


class Testbase(Object):
    """
    Minimal base class used as a controlled fixture in converter unit tests.
    Not part of the NeXus standard definitions. Covers: NX_CHAR, NX_FLOAT with
    units, NX_INT, NX_BOOLEAN, closed enumeration, group reference, and
    group-level attribute — the key structural features exercised by the
    NXDL-to-metainfo converter.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtestBase",
            category="base",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Primary data group (tests group → SubSection mapping)."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="optional",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-label-field"
        ],
        description=("A text label field (tests NX_CHAR → str mapping)."),
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("An energy value (tests NX_FLOAT + unit → np.float64 mapping)."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    count = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-count-field"
        ],
        dimensionality="dimensionless",
        description=("An integer count (tests NX_INT → np.int64 mapping)."),
        a_nexus_field=NeXusField(
            name="count",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    flag = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-flag-field"
        ],
        dimensionality="dimensionless",
        description=("A boolean flag (tests NX_BOOLEAN → bool mapping)."),
        a_nexus_field=NeXusField(
            name="flag",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mode = Quantity(
        type=MEnum(["fast", "slow", "medium"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-mode-field"
        ],
        description=("Operating mode (tests closed enumeration → MEnum mapping)."),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["fast", "slow", "medium"],
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes//home/rubel/NOMAD-FAIRmat/nomad-distro-dev-RM/packages/pynxtools/src/pynxtools/data/NXtestBase.html#nxtestbase-version-attribute"
        ],
        description=(
            "Schema version string (tests group-level attribute → Quantity mapping)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
