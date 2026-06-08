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
# Run `pynx nomad generate-metainfo --nxdl NXdistortion` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Distortion"]


class Distortion(Process):
    """
    Subclass of NXprocess to describe post-processing distortion correction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdistortion",
            category="base",
            symbols={
                "nsym": "Number of symmetry points used for distortion correction",
                "ndx": "Number of points of the matrix distortion field (x direction)",
                "ndy": "Number of points of the matrix distortion field (y direction)",
            },
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-applied-field"
        ],
        description=("Has the distortion correction been applied?"),
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    symmetry = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-symmetry-field"
        ],
        dimensionality="dimensionless",
        description=(
            "For `symmetry-guided distortion correction`_, where a pattern of "
            "features is mapped to the regular geometric structure expected from "
            "the symmetry. Here we record the number of elementary symmetry "
            "operations. .. _symmetry-guided distortion correction: "
            "https://www.sciencedirect.com/science/article/abs/pii/S0304399118303474?via%3Dihub"
        ),
        a_nexus_field=NeXusField(
            name="symmetry",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    original_centre = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-original-centre-field"
        ],
        dimensionality="dimensionless",
        shape=[2],
        description=(
            "For symmetry-guided distortion correction. Here we record the "
            "coordinates of the symmetry centre point."
        ),
        a_nexus_field=NeXusField(
            name="original_centre",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    original_points = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-original-points-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 2],
        description=(
            "For symmetry-guided distortion correction. Here we record the "
            "coordinates of the relevant symmetry points."
        ),
        a_nexus_field=NeXusField(
            name="original_points",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    cdeform_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-cdeform-field-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Column deformation field for general non-rigid distortion "
            "corrections. 2D matrix holding the column information of the "
            "mapping of each original coordinate."
        ),
        a_nexus_field=NeXusField(
            name="cdeform_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    rdeform_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-rdeform-field-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Row deformation field for general non-rigid distortion corrections. "
            "2D matrix holding the row information of the mapping of each "
            "original coordinate."
        ),
        a_nexus_field=NeXusField(
            name="rdeform_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdistortion.html#nxdistortion-description-field"
        ],
        description=("Description of the procedures employed."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
