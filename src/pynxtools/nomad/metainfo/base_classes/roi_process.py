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
# Run `pynx nomad generate-metainfo --nxdl NXroi_process` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["RoiProcess"]


class RoiProcess(Process):
    """
    Base class to report on the characterization of an area or volume of
    material.

    This area or volume of material is considered a region-of-interest (ROI).

    This base class should be used when the characterization was achieved by
    processing data from experiment or computer simulations into models of the
    microstructure of the material and the properties of the material or its
    crystal defects within this ROI. Microstructural features is a narrow
    synonym for these crystal defects.

    This base class can also be used to store data and metadata of the
    representation of the ROI, i.e. its discretization and shape.

    Methods from computational geometry are typically used for defining a
    discretization of the area and volume.

    Do not confuse this base class with :ref:`NXregion`. The purpose of the
    :ref:`NXregion` base class is to document data access i.e. I/O pattern on
    arrays. Therefore, concepts from :ref:`NXregion` operate in data space
    rather than in real or simulated real space.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroi_process.html#nxroi_process"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXroi_process",
            category="base",
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
