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
# Run `pynx nomad generate-metainfo --nxdl NXspm_scan_control` to regenerate.
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

__all__ = ["SpmScanControl"]


class SpmScanControl(Object):
    """
    A scan is performed inside an N-dimensional phase space, where each
    dimension can correspond not only to real space coordinates (x,y) but also
    to any other parameter. This class contains detailed information about
    controlling the scan in such a phase space (or its subspace).

    scan_types: Trajectory: A list of N-dimensional sequential vectors
    describes the trajectory line for a full scan. Mesh: For each dimension a
    range and a direction are chosen. When a scan along a dimension is done, a
    single step in the next dimension is taken, and then the scan in the
    previous dimension is repeated. As such we can speak about the fastest and
    the slowest scan axes. Snake: Similar to a mesh scan but with the scanning
    direction reversed after each line. Spiral: A scan taken along a spiral
    trajectory. Linear: A scan where the scanning will be performed along a
    single independent axis. Tilt: At each step, a proportional movement is
    done in all dimensions (an special case of Trajectory scan).

    Scan_control_types: Stepping: At each step, a movement to the next point is
    performed; correction (for example backlash) or active regulation (feedback
    loop) may or may not be applied. After the movement is done, the
    measurement is performed without the movement. Continuous: The scanning of
    each line in an N-dimensional phase space is done without stopping;
    measurements are done simultaneously with the movement. Oscillating:
    Scanning over a scan point continuously and then moving to start scanning
    at the next position.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_scan_control",
            category="base",
        ),
    )

    scan_region = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_region.SpmScanRegion",
        repeats=False,
        description=(
            "The scan region is the area of phase space or sub-phase space where "
            "the scan is performed. The region could be N-dimensional and is "
            "defined by the minimum and maximum values of the scan axes."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="optional",
        ),
    )
    meshSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPattern",
        repeats=True,
        variable=True,
        description=(
            "For each dimension a range and a direction are chosen. When a scan "
            "along a dimension is done, a single step in the next dimension is "
            "taken, and then the scan in the previous dimension is repeated. As "
            "such we can speak about the fastest and the slowest scan axes."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="meshSCAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    spiralSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPattern",
        repeats=True,
        variable=True,
        description=("To define the spiral or circular scan, use this group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="spiralSCAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    snakeSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPattern",
        repeats=True,
        variable=True,
        description=("To define the snake scan, use this group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="snakeSCAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    trajSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPattern",
        repeats=True,
        variable=True,
        description=("To define the trajectory scan, use this group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="trajSCAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    linearSCAN = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPattern",
        repeats=True,
        variable=True,
        description=("To define the linear scan, use this group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="linearSCAN",
            name_type="partial",
            optionality="optional",
        ),
    )

    scan_time_start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-scan-time-start-field"
        ],
        dimensionality="[time]",
        description=("The start time of the scan."),
        a_nexus_field=NeXusField(
            name="scan_time_start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    scan_time_end = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-scan-time-end-field"
        ],
        dimensionality="[time]",
        description=("The end time of the scan."),
        a_nexus_field=NeXusField(
            name="scan_time_end",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    independent_scan_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-independent-scan-axes-field"
        ],
        description=(
            "An array of scan axes which are controlled independently of each "
            "other. (e.g. X, Y, Z, or other physical dimensions) The array "
            "elements are in the order of axes of the scan from the fastest to "
            "the slowest."
        ),
        a_nexus_field=NeXusField(
            name="independent_scan_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    scan_resolutionN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-scan-resolutionn-field"
        ],
        variable=True,
        description=(
            "Define the scan resolution along each dimension as the number of "
            "steps per unit of the dimension parameters. Rename the field "
            "according to the name of the independent dimension (e.g. "
            "scan_resolution_x, scan_resolution_voltage)."
        ),
        a_nexus_field=NeXusField(
            name="scan_resolutionN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    accuracyN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-accuracyn-field"
        ],
        variable=True,
        dimensionality="[length]",
        description=("Define the accuracy of the scan probe."),
        a_nexus_field=NeXusField(
            name="accuracyN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    scan_type = Quantity(
        type=MEnum(["trajectory", "mesh", "snake", "spiral", "linear", "tilt"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-scan-type-field"
        ],
        description=("This group specifies how the trajectory of the scan is defined."),
        a_nexus_field=NeXusField(
            name="scan_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["trajectory", "mesh", "snake", "spiral", "linear", "tilt"],
        ),
    )
    scan_control_type = Quantity(
        type=MEnum(["stepping", "continuous", "oscillating"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_control.html#nxspm_scan_control-scan-control-type-field"
        ],
        description=("This string describes how the scan was performed."),
        a_nexus_field=NeXusField(
            name="scan_control_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["stepping", "continuous", "oscillating"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
