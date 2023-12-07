"""
Data model for Vamas ISO standard.
"""
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
# pylint: disable=too-many-instance-attributes

from dataclasses import dataclass


@dataclass
class VamasHeader:
    """An object to store the Vamas header information."""

    format_id: str = (
        "VAMAS Surface Chemical Analysis Standard Data Transfer Format 1988 May 4"
    )
    institute_id: str = "Not Specified"
    instrument_model_id: str = "Not Specified"
    operator_id: str = "Not Specified"
    experiment_id: str = "Not Specified"
    no_comment_lines: str = "2"
    comment_lines: str = "Casa Info Follows CasaXPS Version 2.3.22PR1.0\n0"
    exp_mode: str = "NORM"
    scan_mode: str = "REGULAR"
    nr_regions: str = "0"
    nr_exp_var: str = "1"
    exp_var_label: str = "Exp Variable"
    exp_var_unit: str = "d"
    unknown_3: str = "0"
    unknown_4: str = "0"
    unknown_5: str = "0"
    unknown_6: str = "0"
    no_blocks: str = "1"


@dataclass
class Block:
    """An object to store a block of spectrum data and meta-data."""

    block_id: str = ""
    sample_id: str = ""
    year: str = ""
    month: str = ""
    day: str = ""
    hour: str = ""
    minute: str = ""
    second: str = ""
    no_hrs_in_advance_of_gmt: str = "0"
    no_comment_lines: str = ""
    # This list should contain one element per for each
    # line in the comment block
    comment_lines: str = ""
    technique: str = ""
    exp_var_value: str = ""
    source_label: str = ""
    source_energy: str = ""
    unknown_1: str = "0"
    unknown_2: str = "0"
    unknown_3: str = "0"
    source_analyzer_angle: str = ""
    unknown_4: str = "180"
    analyzer_mode: str = ""
    resolution: str = ""
    magnification: str = "1"
    work_function: str = ""
    target_bias: str = "0"
    # analyser slit length divided by the magnification
    # of the analyser transfer lens
    analyzer_width_x: str = "0"
    analyzer_width_y: str = "0"
    # degrees from upward z-direction,
    # defined by the sample stage
    analyzer_take_off_polar_angle: str = "0"
    analyzer_azimuth: str = "0"
    species_label: str = ""
    transition_label: str = ""
    particle_charge: str = "-1"
    abscissa_label: str = "kinetic energy"
    abscissa_units: str = "eV"
    abscissa_start: str = ""
    abscissa_step: str = ""
    no_variables: str = "2"
    variable_label_1: str = "counts"
    variable_units_1: str = "d"
    variable_label_2: str = "Transmission"
    variable_units_2: str = "d"
    signal_mode: str = "pulse counting"
    dwell_time: str = ""
    no_scans: str = ""
    time_correction: str = "0"
    # degrees from upward z-direction,
    # defined by the sample stage
    sample_angle_tilt: str = "0"
    # degrees clockwise from the y-direction towards the
    # operator, defined by the sample stage
    sample_tilt_azimuth: str = "0"
    sample_rotation: str = "0"
    no_additional_params: str = "2"
    param_label_1: str = "ESCAPE DEPTH TYPE"
    param_unit_1: str = "d"
    param_value_1: str = "0"
    param_label_2: str = "MFP Exponent"
    param_unit_2: str = "d"
    param_value_2: str = "0"
    num_ord_values: str = ""
    min_ord_value_1: str = ""
    max_ord_value_1: str = ""
    min_ord_value_2: str = ""
    max_ord_value_2: str = ""
    data_string: str = ""
