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
# Run `pynx nomad generate-metainfo --nxdl NXgeometry` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Geometry"]


class Geometry(Object):
    """
    legacy class - recommend to use :ref:`NXtransformations` now

    It is recommended that instances of :ref:`NXgeometry` be converted to use
    :ref:`NXtransformations`.

    This is the description for a general position of a component. It is
    recommended to name an instance of :ref:`NXgeometry` as "geometry" to aid
    in the use of the definition in simulation codes such as McStas. Also, in
    HDF, linked items must share the same name. However, it might not be
    possible or practical in all situations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXgeometry.html#nxgeometry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXgeometry",
            category="base",
            deprecated="as decided at 2014 NIAC meeting, convert to use :ref:`NXtransformations`",
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.shape.Shape",
        repeats=True,
        variable=True,
        description=("shape/size information of component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    translation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.translation.Translation",
        repeats=True,
        variable=True,
        description=("translation of component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXtranslation",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.orientation.Orientation",
        repeats=True,
        variable=True,
        description=("orientation of component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXgeometry.html#nxgeometry-description-field"
        ],
        description=(
            "Optional description/label. Probably only present if we are an "
            "additional reference point for components rather than the location "
            "of a real component."
        ),
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
    component_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXgeometry.html#nxgeometry-component-index-field"
        ],
        description=(
            "Position of the component along the beam path. The sample is at 0, "
            "components upstream have negative component_index, components "
            "downstream have positive component_index."
        ),
        a_nexus_field=NeXusField(
            name="component_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
