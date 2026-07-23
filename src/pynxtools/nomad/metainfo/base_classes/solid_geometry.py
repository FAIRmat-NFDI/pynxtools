# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXsolid_geometry (see
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
# Run `pynx nomad generate-metainfo --nxdl NXsolid_geometry` to regenerate.
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

__all__ = ["SolidGeometry"]


class SolidGeometry(Object, ArchiveSection):
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
