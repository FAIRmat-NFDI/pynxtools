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
# Run `pynx nomad generate-metainfo --nxdl NXdetector_module` to regenerate.
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

__all__ = ["DetectorModule"]


class DetectorModule(Object):
    """
    Geometry and logical description of a detector module. When used, child
    group to NXdetector.

    Many detectors consist of multiple smaller modules. Sometimes it is
    important to know the exact position of such modules. This is the purpose
    of this group. It is a child group to NXdetector.

    Note, the pixel size is given as values in the array fast_pixel_direction
    and slow_pixel_direction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdetector_module",
            category="base",
        ),
    )

    data_origin = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-data-origin-field"
        ],
        description=(
            "A dimension-2 or dimension-3 field which gives the indices of the "
            "origin of the hyperslab of data for this module in the main area "
            "detector image in the parent NXdetector module. The data_origin is "
            "0-based. The frame number dimension (np) is omitted. Thus the "
            "data_origin field for a dimension-2 dataset with indices (np, i, j) "
            "will be an array with indices (i, j), and for a dimension-3 dataset "
            "with indices (np, i, j, k) will be an array with indices (i, j, k). "
            "The :ref:`order <Design-ArrayStorageOrder>` of indices (i, j or i, "
            "j, k) is slow to fast."
        ),
        a_nexus_field=NeXusField(
            name="data_origin",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    data_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-data-size-field"
        ],
        description=(
            "Two or three values for the size of the module in pixels in each "
            "direction. Dimensionality and order of indices is the same as for "
            "data_origin."
        ),
        a_nexus_field=NeXusField(
            name="data_size",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    module_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-field"
        ],
        dimensionality="[length]",
        description=(
            "Offset of the module in regards to the origin of the detector in an "
            "arbitrary direction."
        ),
        a_nexus_field=NeXusField(
            name="module_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    module_offset__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="module_offset",
            enumeration=["translation"],
        ),
    )
    module_offset__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-vector-attribute"
        ],
        description=("Three values that define the axis for this transformation"),
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="module_offset",
        ),
    )
    module_offset__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-offset-attribute"
        ],
        description=(
            "A fixed offset applied before the transformation (three vector "
            "components)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="module_offset",
        ),
    )
    module_offset__offset_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-offset-units-attribute"
        ],
        description=("Units of the offset."),
        a_nexus_attribute=NeXusAttribute(
            name="offset_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="module_offset",
        ),
    )
    module_offset__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-module-offset-depends-on-attribute"
        ],
        description=("Points to the path of the next element in the geometry chain."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="module_offset",
        ),
    )
    fast_pixel_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-field"
        ],
        dimensionality="[length]",
        description=(
            "Values along the direction of :ref:`fastest varying "
            "<Design-ArrayStorageOrder>` :index:`pixel direction<dimension; "
            "fastest varying>`. Each value in this array is the size of a pixel "
            "in the units specified. Alternatively, if only one value is given, "
            "all pixels in this direction have the same value. The direction "
            "itself is given through the vector attribute."
        ),
        a_nexus_field=NeXusField(
            name="fast_pixel_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    fast_pixel_direction__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="fast_pixel_direction",
            enumeration=["translation"],
        ),
    )
    fast_pixel_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-vector-attribute"
        ],
        description=("Three values that define the axis for this transformation"),
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="fast_pixel_direction",
        ),
    )
    fast_pixel_direction__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-offset-attribute"
        ],
        description=(
            "A fixed offset applied before the transformation (three vector "
            "components)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="fast_pixel_direction",
        ),
    )
    fast_pixel_direction__offset_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-offset-units-attribute"
        ],
        description=("Units of the offset."),
        a_nexus_attribute=NeXusAttribute(
            name="offset_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="fast_pixel_direction",
        ),
    )
    fast_pixel_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-fast-pixel-direction-depends-on-attribute"
        ],
        description=("Points to the path of the next element in the geometry chain."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="fast_pixel_direction",
        ),
    )
    slow_pixel_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-field"
        ],
        dimensionality="[length]",
        description=(
            "Values along the direction of :ref:`slowest "
            "varying<Design-ArrayStorageOrder>` :index:`pixel "
            "direction<dimension; slowest varying>`. Each value in this array is "
            "the size of a pixel in the units specified. Alternatively, if only "
            "one value is given, all pixels in this direction have the same "
            "value. The direction itself is given through the vector attribute."
        ),
        a_nexus_field=NeXusField(
            name="slow_pixel_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    slow_pixel_direction__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="slow_pixel_direction",
            enumeration=["translation"],
        ),
    )
    slow_pixel_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-vector-attribute"
        ],
        description=("Three values that define the axis for this transformation"),
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="slow_pixel_direction",
        ),
    )
    slow_pixel_direction__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-offset-attribute"
        ],
        description=(
            "A fixed offset applied before the transformation (three vector "
            "components)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="slow_pixel_direction",
        ),
    )
    slow_pixel_direction__offset_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-offset-units-attribute"
        ],
        description=("Units of the offset."),
        a_nexus_attribute=NeXusAttribute(
            name="offset_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="slow_pixel_direction",
        ),
    )
    slow_pixel_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-slow-pixel-direction-depends-on-attribute"
        ],
        description=("Points to the path of the next element in the geometry chain."),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="slow_pixel_direction",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_module.html#nxdetector_module-depends-on-field"
        ],
        description=("Points to the start of the dependency chain for this module."),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
