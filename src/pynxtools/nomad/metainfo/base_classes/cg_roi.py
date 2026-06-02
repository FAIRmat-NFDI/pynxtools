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
# Run `pynx nomad generate-metainfo --nx-class NXcg_roi` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgRoi"]


class CgRoi(Object):
    """
    Base class for a region-of-interest (ROI) bound by geometric primitives.

    So-called region-of-interest(s) (ROIs) are typically used to describe a
    region in space (and time) where an observation is made or for which a
    computer simulation is performed with given boundary conditions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_roi.html#nxcg_roi"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_roi",
            category="base",
        ),
    )

    cg_ellipsoid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_ellipsoid.CgEllipsoid",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_ellipsoid",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_cylinder = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_cylinder.CgCylinder",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_parallelogram = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_parallelogram.CgParallelogram",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_parallelogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_hexahedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_hexahedron.CgHexahedron",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_polyhedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
