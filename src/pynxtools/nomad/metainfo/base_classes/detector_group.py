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
# Run `pynx nomad generate-metainfo --nxdl NXdetector_group` to regenerate.
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

__all__ = ["DetectorGroup"]


class DetectorGroup(Object):
    """
    Logical grouping of detectors. When used, describes a group of detectors.

    Each detector is represented as an NXdetector with its own detector data
    array. Each detector data array may be further decomposed into array
    sections by use of NXdetector_module groups. Detectors can be grouped
    logically together using NXdetector_group. Groups can be further grouped
    hierarchically in a single NXdetector_group (for example, if there are
    multiple detectors at an endstation or multiple endstations at a facility).
    Alternatively, multiple NXdetector_groups can be provided.

    The groups are defined hierarchically, with names given in the group_names
    field, unique identifying indices given in the field group_index, and the
    level in the hierarchy given in the group_parent field. For example if an
    x-ray detector group, DET, consists of four detectors in a rectangular
    array::

    DTL DTR DLL DLR

    We could have::

    group_names: ["DET", "DTL", "DTR", "DLL", "DLR"] group_index: [1, 2, 3, 4,
    5] group_parent: [-1, 1, 1, 1, 1]
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_group.html#nxdetector_group"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdetector_group",
            category="base",
        ),
    )

    group_names = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_group.html#nxdetector_group-group-names-field"
        ],
        description=(
            "An array of the names of the detectors given in NXdetector groups "
            "or the names of hierarchical groupings of detectors given as names "
            "of NXdetector_group groups or in NXdetector_group group_names and "
            "group_parent fields as having children."
        ),
        a_nexus_field=NeXusField(
            name="group_names",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    group_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_group.html#nxdetector_group-group-index-field"
        ],
        shape=["*"],
        description=(
            "An array of unique identifiers for detectors or groupings of "
            "detectors. Each ID is a unique ID for the corresponding detector or "
            "group named in the field group_names. The IDs are positive integers "
            "starting with 1."
        ),
        a_nexus_field=NeXusField(
            name="group_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    group_parent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_group.html#nxdetector_group-group-parent-field"
        ],
        description=(
            "An array of the hierarchical levels of the parents of detectors or "
            "groupings of detectors. A top-level grouping has parent level -1."
        ),
        a_nexus_field=NeXusField(
            name="group_parent",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    group_type = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_group.html#nxdetector_group-group-type-field"
        ],
        description=("Code number for group type, e.g. bank=1, tube=2 etc."),
        a_nexus_field=NeXusField(
            name="group_type",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
