"""
Class for reading XPS files from raw VMS data.
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

import re
import copy
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.vms.vamas_data_model import VamasHeader, Block

from pynxtools.dataconverter.readers.xps.reader_utils import (
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class VamasParser:
    def __init__(self):
        self.parsers = [
            VamasParserRegular,
            VamasParserIrregular,
        ]

        self.parser_map = {
            "regular": VamasParserRegular,
            "irregular": VamasParserIrregular,
        }

        self.raw_data: list = []
        self._xps_dict: dict = {}

        self._root_path = "/ENTRY[entry]"

    @property
    def data_dict(self) -> dict:
        """Getter property."""
        return self._xps_dict

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the parser that fits the Prodigy SLE version.
        Returns flat list of dictionaries containing one spectrum each.

        """
        self.file = file
        vms_type = self._get_vms_type()
        parser = self.parser_map[vms_type]()
        self.raw_data = parser.parse_file(file, **kwargs)

        file_key = f"{self._root_path}/Files"
        self._xps_dict[file_key] = file

        self.construct_data()

        return self.data_dict

    def _get_vms_type(self):
        """
        Check if the vamas file is regular or irregular

        Returns
        -------
        vms_type : str
            'regular' or 'irregular'

        """
        contents = []
        with open(self.file, "rb") as f:
            for line in f:
                if line.endswith(b"\r\n"):
                    contents += [line.decode("utf-8", errors="ignore").strip()]

        for vms_type in self.parser_map.keys():
            if vms_type.upper() in contents:
                return vms_type

    def construct_data(self):
        """Map VMS format to NXmpes-ready dict."""
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "user": [],
            "instrument": [
                "work_function",
                "target_bias",
                "analyzer_take_off_azimuth",
                "analyzer_take_off_polar",
                "analysis_width_x",
                "analysis_width_y",
            ],
            "source": [
                "source_label",
                "source_analyzer_angle",
            ],
            "beam": ["excitation_energy"],
            "analyser": [],
            "collectioncolumn": [],
            "energydispersion": [
                "scan_mode",
                "pass_energy",
            ],
            "detector": ["signal_mode"],
            "manipulator": [],
            "sample": ["target_bias"],
            "calibration": [],
            "data": [
                "x_label",
                "x_units",
                "y_labels_1",
                "y_units_1",
                "y_labels_2",
                "y_units_2",
                "n_values",
                "start_energy",
                "step_size",
                "dwell_time",
            ],
            "region": [
                "analysis_method",
                "spectrum_type",
                "dwell_time",
                "comments",
                "spectrum_id",
                "time_stamp",
                "scans",
            ],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["group_name"]}'
        region_parent = f'{group_parent}/regions/RegionData_{spectrum["spectrum_type"]}'
        instrument_parent = f"{region_parent}/instrument"
        analyser_parent = f"{instrument_parent}/analyser"

        path_map = {
            "user": f"{region_parent}/user",
            "instrument": f"{instrument_parent}",
            "source": f"{instrument_parent}/source",
            "beam": f"{instrument_parent}/beam",
            "analyser": f"{analyser_parent}",
            "collectioncolumn": f"{analyser_parent}/collectioncolumn",
            "energydispersion": f"{analyser_parent}/energydispersion",
            "detector": f"{analyser_parent}/detector",
            "manipulator": f"{instrument_parent}/manipulator",
            "calibration": f"{instrument_parent}/calibration",
            "sample": f"{region_parent}/sample",
            "data": f"{region_parent}/data",
            "region": f"{region_parent}",
        }

        for grouping, spectrum_keys in key_map.items():
            root = path_map[str(grouping)]
            for spectrum_key in spectrum_keys:
                try:
                    units = re.search(r"\[([A-Za-z0-9_]+)\]", spectrum_key).group(1)
                    mpes_key = spectrum_key.rsplit(" ", 1)[0]
                    self._xps_dict[f"{root}/{mpes_key}/@units"] = units
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]
                except AttributeError:
                    mpes_key = spectrum_key
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]

        entry = construct_entry_name(region_parent)
        self._xps_dict["data"][entry] = xr.Dataset()

        scan_key = construct_data_key(spectrum)

        energy = np.array(spectrum["data"]["x"])

        channels = [key for key in spectrum["data"] if "cps_ch_" in key]

        for channel in channels:
            ch_no = channel.rsplit("_")[-1]
            channel_key = f"{scan_key}_chan_{ch_no}"
            cps = np.array(spectrum["data"][channel])

            self._xps_dict["data"][entry][channel_key] = xr.DataArray(
                data=cps, coords={"energy": energy}
            )

        self._xps_dict["data"][entry][scan_key] = xr.DataArray(
            data=spectrum["data"]["cps_calib"], coords={"energy": energy}
        )

        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'

        self._xps_dict[detector_data_key] = spectrum["data"]["cps_calib"]


class VamasParserVMS(ABC):
    """A parser for reading vamas files."""

    def __init__(self):
        """Construct the vamas parser.

        Class attributes are a VamasHeader, which stores the vamas header
        attributes, blocks, which store the individual Block objects. Each
        block represents one spectrum, then there are several kinds of
        vamas attribute keys, which are used, depending on how the
        vamas file is formatted.
        """
        self.header = VamasHeader()
        self.blocks = []
        self.common_header_attr = [
            "format_id",
            "institute_id",
            "instrumentModel_id",
            "operator_id",
            "experiment_id",
            "no_comment_lines",
        ]

        self.exp_var_attributes = ["exp_var_label", "exp_var_unit"]

        self.norm_header_attr = [
            "scan_mode",
            "nr_regions",
            "nr_exp_var",
            "unknown_3",
            "unknown_4",
            "unknown_5",
            "unknown_6",
            "no_blocks",
        ]

        self.map_header_attr = [
            "scan_mode",
            "nr_regions",
            "nr_positions",
            "nr_x_coords",
            "nr_y_coords",
            "nr_exp_var",
            "unknown_3",
            "unknown_4",
            "unknown_5",
            "unknown_6",
            "no_blocks",
        ]

        self.norm_block_attr = [
            "block_id",
            "sample_id",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "no_hrs_in_advance_of_gmt",
            "no_comment_lines",
            "comment_lines",
            "technique",
            "exp_var_value",
            "source_label",
            "source_energy",
            "unknown_1",
            "unknown_2",
            "unknown_3",
            "source_analyzer_angle",
            "unknown_4",
            "analyzer_mode",
            "resolution",
            "magnification",
            "work_function",
            "target_bias",
            "analyzer_width_x",
            "analyzer_width_y",
            "analyzer_take_off_polar_angle",
            "analyzer_azimuth",
            "species_label",
            "transition_label",
            "particle_charge",
            "abscissa_label",
            "abscissa_units",
            "abscissa_start",
            "abscissa_step",
            "no_variables",
            "variable_label1",
            "variable_units1",
            "variable_label2",
            "variable_units2",
            "signal_mode",
            "dwell_time",
            "no_scans",
            "time_correction",
            "sample_angle_tilt",
            "sample_tilt_azimuth",
            "sample_rotation",
            "no_additional_params",
            "param_label_1",
            "param_unit_1",
            "param_value_1",
            "param_label_2",
            "param_unit_2",
            "param_value_2",
            "num_ord_values",
            "min_ord_value_1",
            "max_ord_value_1",
            "min_ord_value_2",
            "max_ord_value_2",
            "data_string",
        ]

        self.map_block_attr = [
            "block_id",
            "sample_id",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "no_hrs_in_advance_of_gmt",
            "no_comment_lines",
            "comment_lines",
            "technique",
            "x_coord",
            "y_coord",
            "exp_var_value",
            "source_label",
            "source_energy",
            "unknown_1",
            "unknown_2",
            "unknown_3",
            "fov_x",
            "fov_y",
            "source_analyzer_angle",
            "unknown_4",
            "analyzer_mode",
            "resolution",
            "magnification",
            "work_function",
            "target_bias",
            "analyzer_width_x",
            "analyzer_width_y",
            "analyzer_take_off_polar_angle",
            "analyzer_azimuth",
            "species_label",
            "transition_label",
            "particle_charge",
            "abscissa_label",
            "abscissa_units",
            "abscissa_start",
            "abscissa_step",
            "no_variables",
            "variable_label_1",
            "variable_units_1",
            "variable_label_2",
            "variable_units_2",
            "signal_mode",
            "dwell_time",
            "no_scans",
            "time_correction",
            "sample_angle_tilt",
            "sample_tilt_azimuth",
            "sample_rotation",
            "no_additional_params",
            "param_label_1",
            "param_unit_1",
            "param_value_1",
            "param_label_2",
            "param_unit_2",
            "param_value_2",
            "num_ord_values",
            "min_ord_value_1",
            "max_ord_value_1",
            "min_ord_value_2",
            "max_ord_value_2",
            "data_string",
        ]

    def parse_file(self, filepath, **kwargs):
        """Parse the vamas file into a list of dictionaries.

        This method should be called inside the Converter object.
        Parameters
        ----------
        filepath: STRING
        The location and name of the vamas file to be parsed.
        """
        self._read_lines(filepath)
        self._parse_header()
        self._parse_blocks()
        return self._build_list()

    def _read_lines(self, filepath):
        self.data = []
        self.filepath = filepath

        with open(filepath, "rb") as fp:
            for line in fp:
                if line.endswith(b"\r\n"):
                    self.data += [line.decode("utf-8", errors="ignore").strip()]

    def _parse_header(self):
        """Parse the vama header into a VamasHeader object.

        The common_header_attr are the header attributes that are common
        to both types of Vamas format (NORM and MAP).
        Returns
        -------
        None.
        """
        for attr in self.common_header_attr:
            setattr(self.header, attr, self.data.pop(0).strip())
        n = int(self.header.no_comment_lines)
        comments = ""
        for l in range(n):
            comments += self.data.pop(0)
        self.header.comment_lines = comments
        self.header.exp_mode = self.data.pop(0).strip()
        if self.header.exp_mode == "NORM":
            for attr in self.norm_header_attr:
                setattr(self.header, attr, self.data.pop(0).strip())
                if attr == "nr_exp_var":
                    self._add_exp_var()

        elif self.header.exp_mode == "MAP":
            for attr in self.map_header_attr:
                setattr(self.header, attr, self.data.pop(0).strip())
                if attr == "nr_exp_var":
                    self._add_exp_var()

    def _add_exp_var(self):
        for v in range(int(self.header.nr_exp_var)):
            for attr in self.exp_var_attributes:
                setattr(self.header, attr, self.data.pop(0).strip())

    def _parse_blocks(self):
        for b in range(int(self.header.no_blocks)):
            self._parse_one_block()

    def _parse_one_block(self):
        if self.header.exp_mode == "NORM":
            self.blocks += [self._parse_norm_block()]
        elif self.header.exp_mode == "MAP":
            self.blocks += [self._parse_map_block()]

    @abstractmethod
    def _parse_norm_block(self):
        """
        Use this method when the NORM keyword is present.

        This method has to be implemented in the inherited parsers.

        """
        block = Block()

        return Block

    @abstractmethod
    def _parse_map_block(self):
        """
        Use this method when the MAP keyword is present.

        This method has to be implemented in the inherited parsers.

        """
        block = Block()

        return Block

    def _build_list(self):
        """
        Construct a list of dictionaries from the Vamas objects

        Returns
        -------
        List
            Each list element is a dictionary with the data and
            metadata of one spectrum.

        """
        group_id = -1
        temp_group_name = ""
        spectra = []

        for idx, b in enumerate(self.blocks):
            group_name = b.sampleID
            """ This set of conditions detects if the group name has changed.
            If it has, then it increments the group_idx.
            """
            if group_name != temp_group_name:
                temp_group_name = group_name
                group_id += 1

            spectrum_type = str(b.species_label + b.transition_label)
            spectrum_id = idx

            settings = {
                "region": b.block_id,
                "sample_name": b.sample_id,
                "comments": b.comment_lines,  ## need to be split,
                "analysis_method": b.technique,
                "source_label": b.source_label,  # Al
                "excitation_energy": b.source_energy,
                "source_analyzer_angle": b.source_analyzer_angle,
                "scan_mode": b.analyzer_mode,
                "pass_energy": b.resolution,
                "magnification": b.magnification,
                "work_function": b.work_function,
                "target_bias": b.target_bias,
                "analysis_width_x": b.analyzer_width_x,  # analyser slit length divided by the magnification of the analyser transfer lens
                "analysis_width_y": b.analyzer_width_y,
                "analyzer_take_off_polar": b.analyzer_take_off_polar_angle,  # degrees from upward z-direction, defined by the sample stage
                "analyzer_take_off_azimuth": b.analyzer_azimuth,
                "element": b.species_label,  # Fe
                "transition": b.transition_label,  # 2p
                "particle_charge": b.particle_charge,  # -1
                "x_label": b.abscissa_label,
                "x_units": b.abscissa_units,
                "start_energy": b.abscissa_start,
                "step_size": b.abscissa_step,
                "y_labels_1": b.variable_label_1,
                "y_units_1": b.variable_units_1,
                "y_labels_2": b.variable_label_2,
                "y_units_2": b.variable_units_2,
                "signal_mode": b.signal_mode,  # pulse counting
                "dwell_time": b.dwell_time,
                "time_correction": b.time_correction,
                "sample_normal_polarangle_tilt": b.sample_angle_tilt,  # degrees from upward z-direction, defined by the sample stag
                "sample_tilt_azimuth": b.sample_tilt_azimuth,  # degrees clockwise from the y-direction towards the operator, defined by the sample stage
                "sample_rotation_angle": b.sample_rotation,
                "n_values": int(b.num_ord_values / b.no_variables),
            }

            date = (
                str(b.year)
                + "-"
                + str(b.month)
                + "-"
                + str(b.day)
                + " "
                + str(b.hour)
                + ":"
                + str(b.minute)
                + ":"
                + str(b.second)
            )

            # Convert the native time format to the datetime string
            # in the ISO 8601 format: '%Y-%b-%dT%H:%M:%S.%fZ'.
            date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date_time += timedelta(hours=b.no_hrs_in_advance_of_gmt)

            data = {"x": b.x}
            for n in range(int(b.no_variables)):
                if n == 0:
                    key = "y"
                else:
                    key = "y" + str(n)
                data[key] = getattr(b, key)

            spec_dict = {
                "time_stamp": date_time,
                "group_name": group_name,
                "group_id": group_id,
                "spectrum_type": spectrum_type,
                "spectrum_id": spectrum_id,
                "scans": b.no_scans,
                "data": data,
            }
            spec_dict.update(settings)
            spectra += [spec_dict]

        self.data_list = spectra
        return self.data_list


class VamasParserRegular(VamasParserVMS):
    def _parse_norm_block(self):
        """
        Use this method when the NORM keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        block = Block()

        block.block_id = self.data.pop(0).strip()
        block.sample_id = self.data.pop(0).strip()
        block.year = int(self.data.pop(0).strip())
        block.month = int(self.data.pop(0).strip())
        block.day = int(self.data.pop(0).strip())
        block.hour = int(self.data.pop(0).strip())
        block.minute = int(self.data.pop(0).strip())
        block.second = int(self.data.pop(0).strip().split(".")[0])
        block.no_hrs_in_advance_of_gmt = int(self.data.pop(0).strip())
        block.no_comment_lines = int(self.data.pop(0).strip())
        for n in range(block.no_comment_lines):
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        for v in range(int(self.header.nr_exp_var)):
            block.exp_var_value = self.data.pop(0).strip()
        block.source_label = self.data.pop(0).strip()
        block.source_energy = float(self.data.pop(0).strip())
        block.unknown_1 = self.data.pop(0).strip()
        block.unknown_2 = self.data.pop(0).strip()
        block.unknown_3 = self.data.pop(0).strip()
        block.source_analyzer_angle = self.data.pop(0).strip()
        block.unknown_4 = self.data.pop(0).strip()
        block.analyzer_mode = self.data.pop(0).strip()
        block.resolution = float(self.data.pop(0).strip())
        block.magnification = self.data.pop(0).strip()
        block.work_function = float(self.data.pop(0).strip())
        block.target_bias = float(self.data.pop(0).strip())
        block.analyzer_width_x = self.data.pop(0).strip()
        block.analyzer_width_y = self.data.pop(0).strip()
        block.analyzer_take_off_polar_angle = self.data.pop(0).strip()
        block.analyzer_azimuth = self.data.pop(0).strip()
        block.species_label = self.data.pop(0).strip()
        block.transition_label = self.data.pop(0).strip()
        block.particle_charge = self.data.pop(0).strip()
        block.abscissa_label = self.data.pop(0).strip()
        block.abscissa_units = self.data.pop(0).strip()
        block.abscissa_start = float(self.data.pop(0).strip())
        block.abscissa_step = float(self.data.pop(0).strip())
        block.no_variables = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "variable_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for p in range(block.no_additional_params):
            name = "param_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "min_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)
        return block

    def _parse_map_block(self):
        """
        Use this method when the MAP keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        block = Block()
        block.block_id = self.data.pop(0).strip()
        block.sample_id = self.data.pop(0).strip()
        block.year = int(self.data.pop(0).strip())
        block.month = int(self.data.pop(0).strip())
        block.day = int(self.data.pop(0).strip())
        block.hour = int(self.data.pop(0).strip())
        block.minute = int(self.data.pop(0).strip())
        block.second = int(self.data.pop(0).strip())
        block.no_hrs_in_advance_of_gmt = int(self.data.pop(0).strip())
        block.no_comment_lines = int(self.data.pop(0).strip())
        for n in range(block.no_comment_lines):
            self.data.pop(0)
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        block.x_coord = self.data.pop(0).strip()
        block.y_coord = self.data.pop(0).strip()
        block.exp_var_value = self.data.pop(0).strip()
        block.source_label = self.data.pop(0).strip()
        block.source_energy = float(self.data.pop(0).strip())
        block.unknown_1 = self.data.pop(0).strip()
        block.unknown_2 = self.data.pop(0).strip()
        block.unknown_3 = self.data.pop(0).strip()
        block.fov_x = self.data.pop(0).strip()
        block.fov_y = self.data.pop(0).strip()
        block.source_analyzer_angle = self.data.pop(0).strip()
        block.unknown_4 = self.data.pop(0).strip()
        block.analyzer_mode = self.data.pop(0).strip()
        block.resolution = float(self.data.pop(0).strip())
        block.magnification = self.data.pop(0).strip()
        block.work_function = float(self.data.pop(0).strip())
        block.target_bias = float(self.data.pop(0).strip())
        block.analyzer_width_x = self.data.pop(0).strip()
        block.analyzer_width_y = self.data.pop(0).strip()
        block.analyzer_take_off_polar_angle = self.data.pop(0).strip()
        block.analyzer_azimuth = self.data.pop(0).strip()
        block.species_label = self.data.pop(0).strip()
        block.transition_label = self.data.pop(0).strip()
        block.particle_charge = self.data.pop(0).strip()
        block.abscissa_label = self.data.pop(0).strip()
        block.abscissa_units = self.data.pop(0).strip()
        block.abscissa_start = float(self.data.pop(0).strip())
        block.abscissa_step = float(self.data.pop(0).strip())
        block.no_variables = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "variable_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for p in range(block.no_additional_params):
            name = "param_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "min_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)

        return block

    def _add_data_values(self, block):
        data_dict = {}
        start = float(block.abscissa_start)
        step = float(block.abscissa_step)
        num = int(block.num_ord_values / block.no_variables)
        x = [round(start + i * step, 2) for i in range(num)]

        if block.abscissa_label == "binding energy":
            x.reverse()

        setattr(block, "x", x)

        for v in range(block.no_variables):
            if v == 0:
                name = "y"
            else:
                name = "y" + str(v)
            data_dict[name] = []

        d = list(np.array(self.data[: block.num_ord_values], dtype=float))

        self.data = self.data[block.num_ord_values :]

        """for r in range(int(block.numOrdValues / block.noVariables)):
            for v in range(block.noVariables):
                name = 'y' + str(v)
                data_dict[name] += [float(self.data.pop(0).strip())]"""

        for v in range(block.no_variables):
            n = block.no_variables
            if v == 0:
                name = "y"
            else:
                name = "y" + str(v)
            dd = d[v::n]
            data_dict[name] = dd
            setattr(block, name, data_dict[name])


### THIS DOESN'T WORK SO FAR!!
class VamasParserIrregular(VamasParserVMS):
    def _parse_norm_block(self):
        """
        Use this method when the NORM keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        block = Block()

        block.block_id = self.data.pop(0).strip()
        block.sample_id = self.data.pop(0).strip()
        block.year = int(self.data.pop(0).strip())
        block.month = int(self.data.pop(0).strip())
        block.day = int(self.data.pop(0).strip())
        block.hour = int(self.data.pop(0).strip())
        block.minute = int(self.data.pop(0).strip())
        block.second = int(self.data.pop(0).strip().split(".")[0])
        block.no_hrs_in_advance_of_gmt = int(self.data.pop(0).strip())
        block.no_comment_lines = int(self.data.pop(0).strip())
        for n in range(block.no_comment_lines):
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        for v in range(int(self.header.nr_exp_var)):
            block.exp_var_value = self.data.pop(0).strip()
        block.source_label = self.data.pop(0).strip()
        block.source_energy = float(self.data.pop(0).strip())
        block.unknown_1 = self.data.pop(0).strip()
        block.unknown_2 = self.data.pop(0).strip()
        block.unknown_3 = self.data.pop(0).strip()
        block.source_analyzer_angle = self.data.pop(0).strip()
        block.unknown_4 = self.data.pop(0).strip()
        block.analyzer_mode = self.data.pop(0).strip()
        block.resolution = float(self.data.pop(0).strip())
        block.magnification = self.data.pop(0).strip()
        block.work_function = float(self.data.pop(0).strip())
        block.target_bias = float(self.data.pop(0).strip())
        block.analyzer_width_x = self.data.pop(0).strip()
        block.analyzer_width_y = self.data.pop(0).strip()
        block.analyzer_take_off_polar_angle = self.data.pop(0).strip()
        block.analyzer_azimuth = self.data.pop(0).strip()
        block.species_label = self.data.pop(0).strip()
        block.transition_label = self.data.pop(0).strip()
        block.particle_charge = self.data.pop(0).strip()
        block.abscissa_label = self.data.pop(0).strip()
        block.abscissa_units = self.data.pop(0).strip()
        block.abscissa_start = float(self.data.pop(0).strip())
        block.abscissa_step = float(self.data.pop(0).strip())
        block.no_variables = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "variable_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for p in range(block.no_additional_params):
            name = "param_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "min_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)
        return block

    def _parse_map_block(self):
        """
        Use this method when the MAP keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        block = Block()
        block.block_id = self.data.pop(0).strip()
        block.sample_id = self.data.pop(0).strip()
        block.year = int(self.data.pop(0).strip())
        block.month = int(self.data.pop(0).strip())
        block.day = int(self.data.pop(0).strip())
        block.hour = int(self.data.pop(0).strip())
        block.minute = int(self.data.pop(0).strip())
        block.second = int(self.data.pop(0).strip())
        block.no_hrs_in_advance_of_gmt = int(self.data.pop(0).strip())
        block.no_comment_lines = int(self.data.pop(0).strip())
        for n in range(block.no_comment_lines):
            self.data.pop(0)
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        block.x_coord = self.data.pop(0).strip()
        block.y_coord = self.data.pop(0).strip()
        block.exp_var_value = self.data.pop(0).strip()
        block.source_label = self.data.pop(0).strip()
        block.source_energy = float(self.data.pop(0).strip())
        block.unknown_1 = self.data.pop(0).strip()
        block.unknown_2 = self.data.pop(0).strip()
        block.unknown_3 = self.data.pop(0).strip()
        block.fov_x = self.data.pop(0).strip()
        block.fov_y = self.data.pop(0).strip()
        block.source_analyzer_angle = self.data.pop(0).strip()
        block.unknown_4 = self.data.pop(0).strip()
        block.analyzer_mode = self.data.pop(0).strip()
        block.resolution = float(self.data.pop(0).strip())
        block.magnification = self.data.pop(0).strip()
        block.work_function = float(self.data.pop(0).strip())
        block.target_bias = float(self.data.pop(0).strip())
        block.analyzer_width_x = self.data.pop(0).strip()
        block.analyzer_width_y = self.data.pop(0).strip()
        block.analyzer_take_off_polar_angle = self.data.pop(0).strip()
        block.analyzer_azimuth = self.data.pop(0).strip()
        block.species_label = self.data.pop(0).strip()
        block.transition_label = self.data.pop(0).strip()
        block.particle_charge = self.data.pop(0).strip()
        block.abscissa_label = self.data.pop(0).strip()
        block.abscissa_units = self.data.pop(0).strip()
        block.abscissa_start = float(self.data.pop(0).strip())
        block.abscissa_step = float(self.data.pop(0).strip())
        block.no_variables = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "variable_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(p + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for p in range(block.no_additional_params):
            name = "param_label_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(p + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for p in range(block.no_variables):
            name = "min_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(p + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)

        return block

    def _add_data_values(self, block):
        data_dict = {}
        start = float(block.abscissa_start)
        step = float(block.abscissa_step)
        num = int(block.num_ord_values / block.no_variables)
        x = [round(start + i * step, 2) for i in range(num)]

        if block.abscissa_label == "binding energy":
            x.reverse()

        setattr(block, "x", x)

        for v in range(block.no_variables):
            if v == 0:
                name = "y"
            else:
                name = "y" + str(v)
            data_dict[name] = []

        d = list(np.array(self.data[: block.num_ord_values], dtype=float))

        self.data = self.data[block.num_ord_values :]

        """for r in range(int(block.numOrdValues / block.noVariables)):
            for v in range(block.noVariables):
                name = 'y' + str(v)
                data_dict[name] += [float(self.data.pop(0).strip())]"""

        for v in range(block.no_variables):
            n = block.no_variables
            if v == 0:
                name = "y"
            else:
                name = "y" + str(v)
            dd = d[v::n]
            data_dict[name] = dd
            setattr(block, name, data_dict[name])


if __name__ == "__main__":
    filepath = r"C:\Users\pielsticker\Lukas\MPI-CEC\Projects\deepxps\xpsdeeplearning\data\references\Fe_references.vms"
    # filepath = r"C:\Users\pielsticker\Downloads\CasaXP1_irregular.vms"
    v = VamasParser()
    V = v.parse_file(filepath)
    data_dict = v.data_dict
    # h = v.header
    # n = h.no_blocks
    # b = v.blocks[0]
    # header = h.__dict__
