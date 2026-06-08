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
# Run `pynx nomad generate-metainfo --nxdl NXcxi_ptycho` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CxiPtycho"]


class CxiPtycho(Entry):
    """
    Application definition for a ptychography experiment, compatible with CXI
    from version 1.6.

    This is compatible with CXI from version 1.6 if this application definition
    is put at the top "entry" level. Above this a "cxi_version" field should be
    defined. The CXI format is name based, rather than class based, and so it
    is important to pay attention to the naming convention to be CXI
    compatible. There are duplications due to the format merger. These should
    be achieved by linking, with hdf5 Virtual Dataset being used to restructure
    any data that needs to be remapped. To be fully CXI compatible, all units
    (including energy) must be in SI units.

    An example here is that CXI expects the data to always to have shape
    (npts_x*npts_y, frame_size_x, frame_size_y). For nexus this is only true
    for arbitrary scan paths with raster format scans taking shape (npts_x,
    npts_y, frame_size_x, frame_size_y).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcxi_ptycho.html#nxcxi_ptycho"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcxi_ptycho",
            category="application",
            symbols={
                "npts_x": "The number of points in the x direction",
                "npts_y": "Number of points in the y direction.",
                "frame_size_x": "Number of detector pixels in x",
                "frame_size_y": "Number of detector pixels in y",
            },
        ),
    )

    instrument_1 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument_1",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcxi_ptycho.html#nxcxi_ptycho-entry-1-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcxi_ptycho.html#nxcxi_ptycho-entry-1-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcxi_ptycho.html#nxcxi_ptycho-entry-1-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXcxi_ptycho"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcxi_ptycho.html#nxcxi_ptycho-entry-1-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXcxi_ptycho"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
