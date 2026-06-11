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
# Run `pynx nomad generate-metainfo --nxdl NXspm_bias_spectroscopy` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.circuit import Circuit
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.spm_scan_control import SpmScanControl
from pynxtools.nomad.metainfo.base_classes.spm_scan_pattern import SpmScanPattern
from pynxtools.nomad.metainfo.base_classes.spm_scan_region import SpmScanRegion

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmBiasSpectroscopy"]


class SpmBiasSpectroscopy(Object):
    """
    A base class for bias spectroscopy to describe the change in the physical
    properties of the sample with respect to the sweep voltage applied on a
    sample of STM/AFM/... experiments.

    In these experiments an electric potential is applied between the
    (conductive) sample and the probe (tip), and the physical properties (e.g.
    tunnelling current) are measured as the function of this potential. The
    potential is varied in so-called voltage sweeps and the corresponding
    properties are recorded accordingly.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_bias_spectroscopy",
            category="base",
        ),
    )

    spm_positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_positioner.SpmPositioner",
        repeats=True,
        variable=True,
        description=(
            "Information about the positioner PID (proportional, integral, "
            "differential feedback system), offset values, setpoint values and "
            "so on, while running bias voltage-tunneling current measurement. "
            "These components position the probe relative to the sample, thus "
            "help obtaining maps of the data across the sample surface."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_positioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    circuit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_bias_spectroscopy.SpmBiasSpectroscopyCircuit",
        repeats=True,
        variable=True,
    )
    spm_scan_control = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_bias_spectroscopy.SpmBiasSpectroscopySpmScanControl",
        repeats=True,
        variable=True,
        description=(
            "The bias sweep scan which is is performed in the scanning probe "
            "microscopy experiments."
        ),
    )

    measurement_type = Quantity(
        type=MEnum(["constant_spacing", "variadic_spacing"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-measurement-type-field"
        ],
        description=(
            "The measurement type defines how current is measured under the "
            "different input variables like bias voltage (constant_spacing) or "
            "height (variadic_spacing) is applied during the measurement."
        ),
        a_nexus_field=NeXusField(
            name="measurement_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["constant_spacing", "variadic_spacing"],
        ),
    )
    identifier_environment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-identifier-environment-field"
        ],
        description=(
            "Unique identifier for the environment defined by the user or lab. "
            "When multiple scans are performed in a single environment "
            "conditions or settings, the entire scan environment can be "
            "differentiated by this identifier. For example, scan on a sample of "
            "TiSe2 with layered of evaporated pyrene and annealed at 300K "
            "temperature for 5 min process."
        ),
        a_nexus_field=NeXusField(
            name="identifier_environment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class SpmBiasSpectroscopyCircuit(Circuit):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-circuit-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcircuit",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    animation_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-circuit-animation-time-field"
        ],
        dimensionality="[time]",
        description=("The time or period a bias sweep to be displayed."),
        a_nexus_field=NeXusField(
            name="animation_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    measurement_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-circuit-measurement-time-field"
        ],
        dimensionality="[time]",
        description=(
            "The time or period taken by the circuit to measure a full bias "
            "sweep (duration of the voltage-current measurement measurement)."
        ),
        a_nexus_field=NeXusField(
            name="measurement_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmBiasSpectroscopySpmScanControl(SpmScanControl):
    """
    The bias sweep scan which is is performed in the scanning probe microscopy
    experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_control",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    spatial_location = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.coordinate_system.CoordinateSystem",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="spatial_location",
            name_type="specified",
            optionality="optional",
        ),
    )
    scan_region = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_bias_spectroscopy.SpmBiasSpectroscopySpmScanControlScanRegion",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="optional",
        ),
    )
    linear_sweep = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_bias_spectroscopy.SpmBiasSpectroscopySpmScanControlLinearSweep",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="linear_sweep",
            name_type="specified",
            optionality="optional",
        ),
    )

    scan_type = Quantity(
        type=MEnum(["linear"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-type-field"
        ],
        description=(
            "This combines not only how the voltages are changed, but how the "
            "voltage values are correlated to a position across the sample "
            "surface, measuring sweeps are each spatial coordinate or mapping "
            "the response at constant voltage, etc. For STS experiment, the scan "
            "type is usually a single-point scan (trajectory scan)."
        ),
        a_nexus_field=NeXusField(
            name="scan_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["linear"],
        ),
    )
    number_of_sweeps = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-number-of-sweeps-field"
        ],
        description=(
            "The number of sweeps (a full scan from starting bias to end bias) "
            "taken during the bias spectroscopy."
        ),
        a_nexus_field=NeXusField(
            name="number_of_sweeps",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    first_settling_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-first-settling-time-field"
        ],
        dimensionality="[time]",
        description=(
            "The initial time taken to settle the bias voltage at the desired "
            "value. On each sweep usually, the system takes time to settle to "
            "the bias voltage at the next value."
        ),
        a_nexus_field=NeXusField(
            name="first_settling_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    end_settling_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-end-settling-time-field"
        ],
        dimensionality="[time]",
        description=(
            "The time (at the last sweep) to settle for the last value of the sweep."
        ),
        a_nexus_field=NeXusField(
            name="end_settling_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    settling_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-settling-time-field"
        ],
        dimensionality="[time]",
        description=(
            "The time taken to settle the bias voltage at the desired value. On "
            "each sweep usually, the system takes time to settle the bias "
            "voltage at the next value."
        ),
        a_nexus_field=NeXusField(
            name="settling_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    max_slew_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-max-slew-rate-field"
        ],
        description=(
            "The rate at which the amplifier responds to the voltage change (to "
            "reach at the desired value). It defines if the tip movement and "
            "voltage sweep are synchronized."
        ),
        a_nexus_field=NeXusField(
            name="max_slew_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    final_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-final-z-field"
        ],
        dimensionality="[length]",
        description=("The z position after the sweeps are done."),
        a_nexus_field=NeXusField(
            name="final_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    total_spectroscopy_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-total-spectroscopy-time-field"
        ],
        dimensionality="[time]",
        description=("The total time needed for the entire voltage sweep."),
        a_nexus_field=NeXusField(
            name="total_spectroscopy_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmBiasSpectroscopySpmScanControlScanRegion(SpmScanRegion):
    """
    The scan region is the area of phase space or sub-phase space where the
    scan is performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-region-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_region",
            name="scan_region",
            name_type="specified",
            optionality="optional",
        ),
    )

    scan_offset_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-region-scan-offset-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The starting voltage of the bias sweep. The range of voltages for "
            "the sweep can be defined with scan voltage offset and scan voltage "
            "range (difference between minimum and maximum voltage values in a "
            "sweep)"
        ),
        a_nexus_field=NeXusField(
            name="scan_offset_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    scan_range_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-region-scan-range-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The range of voltages for the sweep can be defined with scan "
            "voltage offset and scan voltage range (difference between minimum "
            "and maximum voltage values in a sweep)"
        ),
        a_nexus_field=NeXusField(
            name="scan_range_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    scan_start_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-region-scan-start-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("The start of the bias scan voltage."),
        a_nexus_field=NeXusField(
            name="scan_start_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    scan_end_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-scan-region-scan-end-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("The end value of the bias scan voltage."),
        a_nexus_field=NeXusField(
            name="scan_end_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmBiasSpectroscopySpmScanControlLinearSweep(SpmScanPattern):
    """
    In the linear sweep, the bias voltage is changed linearly from the start
    value to the end value.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_scan_pattern",
            name="linear_sweep",
            name_type="specified",
            optionality="optional",
        ),
    )

    backward_sweep = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-backward-sweep-field"
        ],
        description=(
            "If the bias voltage sweep is also performed in the opposite direction."
        ),
        a_nexus_field=NeXusField(
            name="backward_sweep",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    scan_points_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-scan-points-bias-field"
        ],
        description=("The number of voltage points per sweep."),
        a_nexus_field=NeXusField(
            name="scan_points_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    step_size_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-step-size-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The step size between the two consecutive bias voltage values "
            "during the sweep."
        ),
        a_nexus_field=NeXusField(
            name="step_size_bias",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    scan_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-scan-time-field"
        ],
        dimensionality="[time]",
        description=("The time taken by the scanner to scan the entire area."),
        a_nexus_field=NeXusField(
            name="scan_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    reset_bias = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_bias_spectroscopy.html#nxspm_bias_spectroscopy-bias-sweep-linear-sweep-reset-bias-field"
        ],
        description=(
            "The reset_bias defines whether the bias voltage should be reset to "
            "the starting value after the sweep is completed."
        ),
        a_nexus_field=NeXusField(
            name="reset_bias",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
