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
# Run `pynx nomad generate-metainfo --nxdl NXspm_scan_pattern` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmScanPattern"]


class SpmScanPattern(Object):
    """
    Basic base class to define the pattern of a scan in a given scan region.

    The base class is intended to handle the following scan types or patterns:

    Trajectory: A list of N-dimensional sequential vectors, representing a
    point in phase space, describes the trajectory line for a full scan. Mesh:
    For each dimension, a range and a direction are chosen. When a scan along a
    dimension is done, a single step in the next dimension is taken, and then
    the scan in the previous dimension is repeated. As such we can speak about
    the fastest and the slowest scan axes.

    Snake: Similar to a mesh scan but the current scanning direction reversed
    after each line completed. Spiral: A scan taken along a spiral trajectory.
    Tilt: At each step, a proportional movement is done in all dimensions (an
    special case of Trajectory scan). Linear: A scan where the scanning will be
    performed along a single independent axis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_scan_pattern",
            category="base",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_scan_pattern.SpmScanPatternData",
        repeats=True,
        variable=True,
        description=(
            "The scan data is the data collected during the scan. If the scan "
            "has several channels or derivatives from the channel data, please "
            "duplicate this NXdata group for each."
        ),
    )

    scan_speedN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-scan-speedn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "Define the scan speed in the forward direction along the axis "
            "(except the spiral and trajectory scans), if forward and backward "
            "speeds below are not specified. If the scan goes in the negative "
            "direction, the speed should be negative. Rename the field, "
            "according to the name of the dimension (e.g. scan_speed_x, "
            "scan_speed_voltage). Trajectory scan: N refers to the nth "
            "trajectory line (line between two trajectory points). Spiral scan: "
            "N refers to the nth circle from center."
        ),
        a_nexus_field=NeXusField(
            name="scan_speedN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    forward_speedN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-forward-speedn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "Define the scan speed in the forward directions (except the spiral "
            "and trajectory scans). Rename the field, according to the name of "
            "the dimension. Trajectory scan: N refers to the nth trajectory line "
            "(line between two trajectory points). Spiral scan: N refers to the "
            "nth circle from center."
        ),
        a_nexus_field=NeXusField(
            name="forward_speedN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    backward_speedN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-backward-speedn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "Define the scan speed in the backward directions (except the spiral "
            "and trajectory scans). Rename the field, according to the name of "
            "the dimension. Trajectory scan: N refers to the nth trajectory line "
            "(line between two trajectory points). Spiral scan: N refers to the "
            "nth circle from center."
        ),
        a_nexus_field=NeXusField(
            name="backward_speedN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    channelNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-channelname-field"
        ],
        variable=True,
        description=(
            "Name of the channel that leads the scan data. The ending annotation "
            "'NAME' is to represent the name of the channel and/or dimension. "
            "Rename the field, according to the name of the channel and "
            "dimension (e.g. channel_piezo_scanner_x)."
        ),
        a_nexus_field=NeXusField(
            name="channelNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    scan_pointsN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-scan-pointsn-field"
        ],
        variable=True,
        description=(
            "Define the total number of points in the given axis the scan to be "
            "performed (except the spiral and trajectory scans). Rename the "
            "field, according to the name of the dimension (e.g. scan_points_x, "
            "scan_points_voltage). Trajectory scan: N refers to the nth "
            "trajectory line (line between two trajectory points). Spiral scan: "
            "N refers to the nth circle from center."
        ),
        a_nexus_field=NeXusField(
            name="scan_pointsN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    steppingN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-steppingn-field"
        ],
        variable=True,
        description=(
            "The number of steps the probe jumps over the scan steps or points "
            "in the scanning process. This comes into picture, when not every "
            "point from the scan_points is scanned along an axis (except the "
            "spiral and trajectory scans). Rename the field, according to the "
            "name of the dimension (e.g. stepping_x, stepping_voltage). "
            "Trajectory scan: N refers to the nth trajectory line (line between "
            "two trajectory points). Spiral scan: N refers to the nth circle "
            "from center."
        ),
        a_nexus_field=NeXusField(
            name="steppingN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    step_sizeN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-step-sizen-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The size of each step in the scan on each dimension (except the "
            "spiral and trajectory scans). Rename the field, according to the "
            "name of the dimension (e.g. step_size_x, step_size_voltage). "
            "Trajectory scan: N refers to the nth trajectory line (line between "
            "two trajectory points). Spiral scan: N refers to the nth circle "
            "from center."
        ),
        a_nexus_field=NeXusField(
            name="step_sizeN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    continuousN = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-continuousn-field"
        ],
        variable=True,
        description=(
            "If the scan probe moves continuously over the scan points or steps, "
            "use True. The default value is True. Usually, continuous scanning "
            "is possible in one dimension. On other dimensions, the scan probe "
            "moves in steps. Rename the field, according to the name of the "
            "dimension (e.g. continuous_voltage). Trajectory scan: N refers to "
            "the nth trajectory line (line between two trajectory points). "
            "Spiral scan: N refers to the nth circle from center."
        ),
        a_nexus_field=NeXusField(
            name="continuousN",
            type="NX_BOOLEAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    oscillating = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-oscillating-field"
        ],
        description=(
            "If the scan probe oscillates over the scan point, use True. The "
            "default value is False."
        ),
        a_nexus_field=NeXusField(
            name="oscillating",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    oscillation_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-oscillation-frequency-field"
        ],
        description=("The number of oscillations on each scanning point per second."),
        a_nexus_field=NeXusField(
            name="oscillation_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    number_of_trajectory_points = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-number-of-trajectory-points-field"
        ],
        description=(
            "The number of trajectory points in the entire scan that defines the "
            "path or lines of the trajectory. Each trajectory line is defined by "
            "two subsequent trajectory points."
        ),
        a_nexus_field=NeXusField(
            name="number_of_trajectory_points",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    trajectory_points = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-trajectory-points-field"
        ],
        shape=["*", "*"],
        description=(
            "The trajectory points (nTraj) are the N-dimensional vectors (nD), "
            "each vector refers to a point in N-dimensional phase space."
        ),
        a_nexus_field=NeXusField(
            name="trajectory_points",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    spiral_radiusN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-spiral-radiusn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "Define the radius of the spiral circle of scanning. Rename the "
            "field, according to the circle order, the nearest circle to the "
            "center is 0."
        ),
        a_nexus_field=NeXusField(
            name="spiral_radiusN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class SpmScanPatternData(Data):
    """
    The scan data is the data collected during the scan. If the scan has
    several channels or derivatives from the channel data, please duplicate
    this NXdata group for each.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    DATA = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-data-data-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The data (e.g. current, voltage, temperature) field that can be "
            "plotted against the axes."
        ),
        a_nexus_field=NeXusField(
            name="DATA",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    AXISNAME = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_scan_pattern.html#nxspm_scan_pattern-data-axisname-field"
        ],
        variable=True,
        flexible_unit=True,
        description=("The name of the axis that corresponds to the data field."),
        a_nexus_field=NeXusField(
            name="AXISNAME",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
