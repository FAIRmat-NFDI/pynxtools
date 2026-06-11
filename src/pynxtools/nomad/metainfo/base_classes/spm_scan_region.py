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
# Run `pynx nomad generate-metainfo --nxdl NXspm_scan_region` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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

__all__ = ["SpmScanRegion"]


class SpmScanRegion(Object):
    """
    The scan region is the area of phase space or sub-phase space where the
    scan is performed. The region could be N-dimensional and is defined by the
    minimum and maximum values of the scan axes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_scan_region",
            category="base",
        ),
    )

    scan_offset_valueN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region-scan-offset-valuen-field"
        ],
        variable=True,
        description=(
            "The offset of center of the scan region from the origin along the "
            "specific scan axis. 'N' denotes the name of the specific scan axis. "
            "(Offset, start and end positions are related)"
        ),
        a_nexus_field=NeXusField(
            name="scan_offset_valueN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    scan_rangeN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region-scan-rangen-field"
        ],
        variable=True,
        description=(
            "The range of the scan is the difference start and end values of the "
            "scan region along the dimension 'N'."
        ),
        a_nexus_field=NeXusField(
            name="scan_rangeN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    scan_angleN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region-scan-anglen-field"
        ],
        variable=True,
        dimensionality="[angle]",
        unit="radian",
        description=(
            "The orientation of the scan region or subspace. Usually, the "
            "scan_offset and scan_range are enough to define the scan region. "
            "This field defines how the spatial space is oriented with respect "
            "to the frame of reference. Rename the field describing the angle "
            "with an axis of the spatial space (e.g. scan_angle_x)."
        ),
        a_nexus_field=NeXusField(
            name="scan_angleN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    scan_startN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region-scan-startn-field"
        ],
        variable=True,
        description=(
            "The start of the scan is the starting point of the scan region "
            "(phase space or sub-phase space) for each independent scan axis. "
            "For N-dimensional, it is a list of N numbers."
        ),
        a_nexus_field=NeXusField(
            name="scan_startN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    scan_endN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_region.html#nxspm_scan_region-scan-endn-field"
        ],
        variable=True,
        description=(
            "The end of the scan is the ending point of the scan region (phase "
            "space or sub-phase space) for each independent scan axis. Note: The "
            "scan_offset and scan_range are equivalent to the scan_start and "
            "scan_end. For N-dimensional, it is a list of N numbers."
        ),
        a_nexus_field=NeXusField(
            name="scan_endN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
