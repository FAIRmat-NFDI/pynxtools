# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcollection (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcollection` to regenerate.
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

__all__ = ["Collection"]


class Collection(Object):
    """
    An unvalidated set of terms, such as the description of a beam line.

    Use :ref:`NXcollection` to gather together any set of terms. The original
    suggestion is to use this as a container class for the description of a
    beamline.

    For NeXus validation, :ref:`NXcollection` will always generate a warning
    since it is always an optional group. Anything (groups, fields, or
    attributes) placed in an :ref:`NXcollection` group will not be validated.

    .. admonition:: NXcollection content is not validated.

    :ref:`NXcollection` is and will always be for unvalidated content.

    Any and all content within a :ref:`NXcollection` group specified by an
    application definition cannot be validated.

    It is suggested to use a :ref:`NXparameters` group for similar content
    which should be validated.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollection.html#nxcollection"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcollection",
            category="base",
            ignore_extra_groups=True,
            ignore_extra_fields=True,
            ignore_extra_attributes=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
