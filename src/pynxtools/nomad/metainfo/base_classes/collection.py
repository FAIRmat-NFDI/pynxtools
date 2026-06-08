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
# Run `pynx nomad generate-metainfo --nxdl NXcollection` to regenerate.
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
