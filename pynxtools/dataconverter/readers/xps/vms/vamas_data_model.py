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
from dataclasses import dataclass

@dataclass
class VamasHeader:
    """An object to store the Vamas header information."""

    def __init__(self):
        """Construct vamas header object."""
        self.formatID = (
            "VAMAS Surface Chemical Analysis Standard Data Transfer Format 1988 May 4"
        )
        self.institute_id = "Not Specified"
        self.instriumentModel_id = "Not Specified"
        self.operator_id = "Not Specified"
        self.experiment_id = "Not Specified"
        self.no_comment_lines = "2"
        self.comment_lines = "Casa Info Follows CasaXPS Version 2.3.22PR1.0\n0"
        self.exp_mode = "NORM"
        self.scan_mode = "REGULAR"
        self.nr_regions = "0"
        self.nr_exp_var = "1"
        self.exp_var_label = "Exp Variable"
        self.exp_var_unit = "d"
        self.unknown_3 = "0"
        self.unknown_4 = "0"
        self.unknown_5 = "0"
        self.unknown_6 = "0"
        self.no_blocks = "1"

@dataclass
class Block:
    """An object to store a block of spectrum data and meta-data."""

    def __init__(self):
        """Construct a Block object.

        The values provided here are default values.
        The order in which the attributes are defined here is important for
        the VamasWriter. Changing the order can result in a Vamas file that
        is un-readable.
        """
        self.blockID = ""
        self.sampleID = ""
        self.year = ""
        self.month = ""
        self.day = ""
        self.hour = ""
        self.minute = ""
        self.second = ""
        self.no_hrs_in_advance_of_gmt = "0"
        self.no_comment_lines = ""
        self.comment_lines = ""  # This list should contain one element per for each line in the comment block
        self.technique = ""
        self.exp_var_value = ""
        self.source_label = ""
        self.source_energy = ""
        self.unknown_1 = "0"
        self.unknown_2 = "0"
        self.unknown_3 = "0"
        self.source_analyzer_angle = ""
        self.unknown_4 = "180"
        self.analyzer_mode = ""
        self.resolution = ""
        self.magnification = "1"
        self.work_function = ""
        self.target_bias = "0"
        self.analyzer_width_x = "0"
        self.analyzer_width_y = "0"
        self.analyzer_take_off_polar_angle = "0"
        self.analyzer_azimuth = "0"
        self.species_label = ""
        self.transition_label = ""
        self.particle_charge = "-1"
        self.abscissa_label = "kinetic energy"
        self.abscissa_units = "eV"
        self.abscissa_start = ""
        self.abscissa_step = ""
        self.no_variables = "2"
        self.variable_label_1 = "counts"
        self.variable_units_1 = "d"
        self.variable_label_2 = "Transmission"
        self.variable_units_2 = "d"
        self.signal_mode = "pulse counting"
        self.dwell_time = ""
        self.no_scans = ""
        self.timeCorrection = "0"
        self.sample_angle_tilt = "0"
        self.sample_tilt_azimuth = "0"
        self.sample_rotation = "0"
        self.no_additional_params = "2"
        self.param_label_1 = "ESCAPE DEPTH TYPE"
        self.param_unit_1 = "d"
        self.param_value_1 = "0"
        self.param_label_2 = "MFP Exponent"
        self.param_unit_2 = "d"
        self.param_value_2 = "0"
        self.num_ord_values = ""
        self.min_ord_value_1 = ""
        self.max_ord_value_1 = ""
        self.min_ord_value_2 = ""
        self.max_ord_value_2 = ""
        self.data_string = ""