# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXgeometry (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXgeometry` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
            component=ELNComponentEnum.RichTextEditQuantity,
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
