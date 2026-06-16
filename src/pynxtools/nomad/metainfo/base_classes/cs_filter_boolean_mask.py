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
# Run `pynx nomad generate-metainfo --nxdl NXcs_filter_boolean_mask` to regenerate.
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

__all__ = ["CsFilterBooleanMask"]


class CsFilterBooleanMask(Object):
    """
    Base class for packing and unpacking booleans.

    The field mask should be constructed from packing a vector of booleans (a
    bitfield) into unsigned integers with bytesize bitdepth. Padding to an
    integer number of such integers is assumed.

    Thereby, this base class can be used to inform software about necessary
    modulo operations to decode the mask to recover e.g. set membership of
    objects in sets whose membership has been encoded as a vector of booleans.

    This is useful e.g. when processing object sets such as point cloud data.
    If e.g. a spatial filter has been applied to a set of points, we may wish
    to document memory-space efficiently which points were analyzed. An array
    of boolean values is one option to achieve this. A value is true if the
    point is included and false otherwise.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_filter_boolean_mask.html#nxcs_filter_boolean_mask"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_filter_boolean_mask",
            category="base",
            symbols={
                "n_objs": "Number of entries (e.g. number of points or objects).",
                "bitdepth": "Number of bits assumed for the container datatype used.",
                "n_total": "Length of mask considering the eventual need for padding.",
            },
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_filter_boolean_mask.html#nxcs_filter_boolean_mask-depends-on-field"
        ],
        description=(
            "Possibility to refer to which set this mask applies. If depends_on "
            "is not provided, it is assumed that the mask applies to its direct "
            "parent."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_filter_boolean_mask.html#nxcs_filter_boolean_mask-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of objects represented by the mask."),
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_filter_boolean_mask.html#nxcs_filter_boolean_mask-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Number of bits assumed matching on a default datatype. (e.g. 8 bits "
            "for a C-style uint8)."
        ),
        a_nexus_field=NeXusField(
            name="bitdepth",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_filter_boolean_mask.html#nxcs_filter_boolean_mask-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The content of the mask. If padding is used, padding bits have to "
            "be set to 0."
        ),
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
