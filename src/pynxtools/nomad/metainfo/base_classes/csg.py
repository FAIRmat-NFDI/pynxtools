# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcsg (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXcsg` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import ArchiveSection
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

__all__ = ["Csg"]


class Csg(Object, ArchiveSection):
    """
    Constructive Solid Geometry (CSG) base class.

    Offers concepts for combining the definitions of leaf and branching nodes
    of a CSG tree.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcsg.html#nxcsg"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcsg",
            category="base",
        ),
    )

    a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.csg.Csg",
        repeats=False,
        description=(
            "The first operand of constructive solid geometry operation. "
            "Compulsory if 'operation' is UNION, INTERSECTION, DIFFERENCE or "
            "COMPLEMENT."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcsg",
            name="a",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.csg.Csg",
        repeats=False,
        description=(
            "The second operand of constructive solid geometry operation. "
            "Compulsory if 'operation' is UNION, INTERSECTION or DIFFERENCE."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcsg",
            name="b",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    operation = Quantity(
        type=MEnum(
            [
                "UNION",
                "INTERSECTION",
                "DIFFERENCE",
                "COMPLEMENT",
                "IS_QUADRIC",
                "IS_MESH",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcsg.html#nxcsg-operation-field"
        ],
        description=(
            "One of the standard construction solid geometry set operations, or "
            "statement IS_QUADRIC or IS_MESH if the CSG is a pointer to an "
            "instance of a geometry class. Takes values:"
        ),
        a_nexus_field=NeXusField(
            name="operation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "UNION",
                "INTERSECTION",
                "DIFFERENCE",
                "COMPLEMENT",
                "IS_QUADRIC",
                "IS_MESH",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    geometry = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcsg.html#nxcsg-geometry-field"
        ],
        description=(
            "Path to a field that is an instance of one of several possible "
            "geometry classes: Specifically, :ref:`NXquadric` if 'operation' is "
            "IS_QUADRIC, :ref:`NXoff_geometry`, or other primitive based base "
            "classes if 'operation' is IS_MESH. The instance defines the surface "
            "making up the constructive solid geometry component. This field is "
            "compulsory if 'operation' is IS_QUADRIC or IS_MESH."
        ),
        a_nexus_field=NeXusField(
            name="geometry",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
