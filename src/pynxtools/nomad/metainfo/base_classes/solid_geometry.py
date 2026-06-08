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
# Run `pynx nomad generate-metainfo --nxdl NXsolid_geometry` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SolidGeometry"]


class SolidGeometry(Object):
    """
    The head node for constructively defined geometry.

    * `S. Ghebi <https://doi.org/10.1007/978-1-84800-115-2>`_ * `L. H. Laidlaw
    <https://doi.org/10.1145/15886.15904>`_

    for an introduction into the topic of modeling shapes with constructive
    solid geometry (CSG).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolid_geometry.html#nxsolid_geometry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsolid_geometry",
            category="base",
        ),
    )

    quadric = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.quadric.Quadric",
        repeats=True,
        variable=True,
        description=(
            "Instances of :ref:`NXquadric` making up elements of the geometry."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXquadric",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=(
            "Instances of :ref:`NXoff_geometry` making up elements of the geometry."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    csg = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.csg.Csg",
        repeats=True,
        variable=True,
        description=(
            "The geometries defined, made up of e.g. instances of "
            ":ref:`NXquadric`, :ref:`NXoff_geometry`, or instances of other base "
            "classes that define geometries."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcsg",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
