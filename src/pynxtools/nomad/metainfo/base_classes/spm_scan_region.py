# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXspm_scan_region (see
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
# Run `pynx nomad generate-metainfo --nxdl NXspm_scan_region` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
        flexible_unit=True,
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
        flexible_unit=True,
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
        flexible_unit=True,
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
        flexible_unit=True,
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
