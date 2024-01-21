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
# pylint: disable=too-many-lines

import re
from copy import deepcopy
import datetime
from abc import ABC, abstractmethod
from itertools import groupby
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.vms.vamas_data_model import VamasHeader, Block

from pynxtools.dataconverter.readers.xps.reader_utils import (
    XPSMapper,
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class VamasMapper(XPSMapper):
    """
    Class for restructuring .txt data file from
    Vamas format into python dictionary.
    """

    config_file = "config_vms.json"

    def __init__(self):
        self.file = None
        self.parsers = [
            VamasParserRegular,
            VamasParserIrregular,
        ]
        self.parser_map = {
            "regular": VamasParserRegular,
            "irregular": VamasParserIrregular,
        }

        super().__init__()

    def _select_parser(self):
        """
        Select parser based on the structure of the Vamas file,
        i.e., whether it is regular or irregular.

        Returns
        -------
        VamasParserVMS
            Vamas parser for reading this file structure.

        """
        vms_type = self._get_vms_type()
        return self.parser_map[vms_type]()

    def _get_vms_type(self):
        """Check if the vamas file is regular or irregular"""
        contents = []
        with open(self.file, "rb") as vms_file:
            for line in vms_file:
                if line.endswith(b"\r\n"):
                    contents += [line.decode("utf-8", errors="ignore").strip()]

        for vms_type in self.parser_map:
            if vms_type.upper() in contents:
                return vms_type
        return ""

    def construct_data(self):
        """Map VMS format to NXmpes-ready dict."""
        # pylint: disable=duplicate-code
        spectra = deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "user": [],
            "instrument": [],
            "source": [
                "source_label",
                "source_analyzer_angle",
            ],
            "beam": ["excitation_energy"],
            "analyser": [
                "analyzer_take_off_azimuth",
                "analyzer_take_off_polar",
                "analysis_width_x",
                "analysis_width_y",
                "target_bias",
                "work_function",
            ],
            "collectioncolumn": [],
            "energydispersion": [
                "scan_mode",
                "pass_energy",
            ],
            "detector": [
                "signal_mode",
                "dwell_time",
            ],
            "manipulator": [],
            "sample": [],
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
            ],
            "region": [
                "analysis_method",
                "spectrum_type",
                "comments",
                "spectrum_id",
                "time_stamp",
                "scans",
            ],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """Map one spectrum from raw data to NXmpes-ready dict."""
        # pylint: disable=too-many-locals,duplicate-code
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

        # Create keys for writing to data and detector
        entry = construct_entry_name(region_parent)
        scan_key = construct_data_key(spectrum)
        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'

        energy = np.array(spectrum["data"]["x"])
        intensity = np.array(spectrum["data"]["y"])

        if entry not in self._xps_dict["data"]:
            self._xps_dict["data"][entry] = xr.Dataset()

        # Write averaged cycle data to 'data'.
        all_scan_data = [
            np.array(value)
            for key, value in self._xps_dict["data"][entry].items()
            if scan_key.split("_")[0] in key
        ]

        # Write averaged cycle data to 'data'.
        averaged_scans = np.mean(all_scan_data, axis=0)
        if averaged_scans.size == 1:
            # on first scan in cycle
            averaged_scans = intensity

        try:
            self._xps_dict["data"][entry][scan_key.split("_")[0]] = xr.DataArray(
                data=averaged_scans,
                coords={"energy": energy},
            )
        except ValueError:
            pass

        # Write scan data to 'data'.
        self._xps_dict["data"][entry][scan_key] = xr.DataArray(
            data=intensity, coords={"energy": energy}
        )

        # Write raw intensities to 'detector'.
        self._xps_dict[detector_data_key] = intensity


class VamasParser(ABC):
    """A parser for reading vamas files."""

    def __init__(self):
        """Construct the vamas parser.

        Class attributes are a VamasHeader, which stores the vamas header
        attributes, blocks, which store the individual Block objects. Each
        block represents one spectrum, then there are several kinds of
        vamas attribute keys, which are used, depending on how the
        vamas file is formatted.
        """
        self.data = []

        self.header = VamasHeader()
        self.blocks = []

        self.attrs = {
            "common_header": [
                "format_id",
                "institute_id",
                "instrumentModel_id",
                "operator_id",
                "experiment_id",
                "no_comment_lines",
            ],
            "exp_var": ["exp_var_label", "exp_var_unit"],
            "norm_header": [
                "scan_mode",
                "nr_regions",
                "nr_exp_var",
                "unknown_3",
                "unknown_4",
                "unknown_5",
                "unknown_6",
                "no_blocks",
            ],
            "map_header": [
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
            ],
            "norm_block": [
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
            ],
            "map_block": [
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
            ],
        }

    def parse_file(self, file):
        """Parse the vamas file into a list of dictionaries.

        Parameters
        ----------
        file: str
           The location and name of the vamas file to be parsed.
        """
        self._read_lines(file)
        self._parse_header()
        self._parse_blocks()
        return self.build_list()

    def _read_lines(self, file):
        with open(file, "rb") as vms_file:
            for line in vms_file:
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
        for attr in self.attrs["common_header"]:
            setattr(self.header, attr, self.data.pop(0).strip())
        no_comment_lines = int(self.header.no_comment_lines)
        comments = ""
        for _ in range(no_comment_lines):
            comments += self.data.pop(0)
        self.header.comment_lines = comments
        self.header.exp_mode = self.data.pop(0).strip()
        if self.header.exp_mode == "NORM":
            for attr in self.attrs["norm_header"]:
                setattr(self.header, attr, self.data.pop(0).strip())
                if attr == "nr_exp_var":
                    self._add_exp_var()

        elif self.header.exp_mode == "MAP":
            for attr in self.attrs["map_header"]:
                setattr(self.header, attr, self.data.pop(0).strip())
                if attr == "nr_exp_var":
                    self._add_exp_var()

    def _add_exp_var(self):
        for _ in range(int(self.header.nr_exp_var)):
            for attr in self.attrs["exp_var"]:
                setattr(self.header, attr, self.data.pop(0).strip())

    def _parse_blocks(self):
        for _ in range(int(self.header.no_blocks)):
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
        return Block()

    @abstractmethod
    def _parse_map_block(self):
        """
        Use this method when the MAP keyword is present.

        This method has to be implemented in the inherited parsers.

        """
        return Block()

    def _get_scan_numbers_for_spectra(self, spectra):
        """
        For a flat list of spectra, groupby group name and spectrum
        type and iteratively give them scan numbers.

        Parameters
        ----------
        spectra : list
            List of dicts with each dict containing data and metadata
            for one spectrum.

        Returns
        -------
        flattened_spectra : list
            Same list of dicts, but each spectrum gets a scan number.

        """
        grouped_spectra = [
            list(y)
            for x, y in groupby(
                sorted(spectra, key=lambda x: (x["group_name"], x["spectrum_type"])),
                lambda x: (x["group_name"], x["spectrum_type"]),
            )
        ]

        for group in grouped_spectra:
            for i, spectrum in enumerate(group):
                spectrum["scan_no"] = i

        flattened_spectra = [
            spectrum for group in grouped_spectra for spectrum in group
        ]

        return flattened_spectra

    def build_list(self):
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

        for spectrum_id, block in enumerate(self.blocks):
            group_name = block.sample_id
            # This set of conditions detects if the group name has changed.
            # If it has, then it increments the group_idx.
            if group_name != temp_group_name:
                temp_group_name = group_name
                group_id += 1

            spectrum_type = str(block.species_label + block.transition_label)

            settings = {
                "region": block.block_id,
                "sample_name": block.sample_id,
                "comments": block.comment_lines,
                "analysis_method": block.technique,
                "source_label": block.source_label,
                "excitation_energy": block.source_energy,
                "source_analyzer_angle": block.source_analyzer_angle,
                "scan_mode": block.analyzer_mode,
                "pass_energy": block.resolution,
                "magnification": block.magnification,
                "work_function": block.work_function,
                "target_bias": block.target_bias,
                "analysis_width_x": block.analyzer_width_x,
                "analysis_width_y": block.analyzer_width_y,
                "analyzer_take_off_polar": block.analyzer_take_off_polar_angle,
                "analyzer_take_off_azimuth": block.analyzer_azimuth,
                "element": block.species_label,
                "transition": block.transition_label,
                "particle_charge": block.particle_charge,
                "x_label": block.abscissa_label,
                "x_units": block.abscissa_units,
                "start_energy": block.abscissa_start,
                "step_size": block.abscissa_step,
                "y_labels_1": block.variable_label_1,
                "y_units_1": block.variable_units_1,
                "y_labels_2": block.variable_label_2,
                "y_units_2": block.variable_units_2,
                "signal_mode": block.signal_mode,
                "dwell_time": block.dwell_time,
                "time_correction": block.time_correction,
                "sample_normal_polarangle_tilt": block.sample_angle_tilt,
                "sample_tilt_azimuth": block.sample_tilt_azimuth,
                "sample_rotation_angle": block.sample_rotation,
                "n_values": int(block.num_ord_values / block.no_variables),
            }

            # Convert the native time format to the datetime string
            # in the ISO 8601 format
            tzinfo = datetime.timezone(
                datetime.timedelta(hours=block.no_hrs_in_advance_of_gmt)
            )
            date_time = datetime.datetime(
                block.year,
                block.month,
                block.day,
                block.hour,
                block.minute,
                block.second,
                tzinfo=tzinfo,
            )

            data = {"x": block.x}
            for var in range(int(block.no_variables)):
                if var == 0:
                    key = "y"
                else:
                    key = "y" + str(var)
                data[key] = getattr(block, key)

            spec_dict = {
                "time_stamp": date_time,
                "group_name": group_name,
                "group_id": group_id,
                "spectrum_type": spectrum_type,
                "spectrum_id": spectrum_id,
                "scans": block.no_scans,
                "data": data,
            }
            spec_dict.update(settings)
            spectra += [spec_dict]

        spectra = self._get_scan_numbers_for_spectra(spectra)

        return spectra


class VamasParserRegular(VamasParser):
    """Parser for .vms files of type REGULAR"""

    def _parse_norm_block(self):
        """
        Use this method when the NORM keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        # pylint: disable=too-many-statements
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
        for _ in range(block.no_comment_lines):
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        for _ in range(int(self.header.nr_exp_var)):
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
        for var in range(block.no_variables):
            name = "variable_label_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for param in range(block.no_additional_params):
            name = "param_label_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for var in range(block.no_variables):
            name = "min_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(var + 1)
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
        # pylint: disable=too-many-statements
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
        for _ in range(block.no_comment_lines):
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
        for var in range(block.no_variables):
            name = "variable_label_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for param in range(block.no_additional_params):
            name = "param_label_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for var in range(block.no_variables):
            name = "min_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)

        return block

    def _add_data_values(self, block):
        """Add data values to a Vamas data block."""
        data_dict = {}
        start = float(block.abscissa_start)
        step = float(block.abscissa_step)
        num = int(block.num_ord_values / block.no_variables)
        energy = [round(start + i * step, 2) for i in range(num)]

        if block.abscissa_label == "binding energy":
            energy.reverse()

        setattr(block, "x", energy)

        for var in range(block.no_variables):
            if var == 0:
                name = "y"
            else:
                name = "y" + str(var)
            data_dict[name] = []

        data_array = list(np.array(self.data[: block.num_ord_values], dtype=float))

        self.data = self.data[block.num_ord_values :]

        for var in range(block.no_variables):
            max_var = block.no_variables
            if var == 0:
                name = "y"
            else:
                name = "y" + str(var)
            data_array_slice = data_array[var::max_var]
            data_dict[name] = data_array_slice
            setattr(block, name, data_dict[name])


# THIS DOESN'T WORK SO FAR!!
class VamasParserIrregular(VamasParser):
    """Parser for .vms files of type IRREGULAR"""

    def _parse_norm_block(self):
        """
        Use this method when the NORM keyword is present.

        Returns
        -------
        block : vamas.Block object.
            A block represents one spectrum with its metadata.

        """
        # pylint: disable=too-many-statements
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
        for _ in range(block.no_comment_lines):
            block.comment_lines += self.data.pop(0)
        block.technique = self.data.pop(0).strip()
        for _ in range(int(self.header.nr_exp_var)):
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
        for var in range(block.no_variables):
            name = "variable_label_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for param in range(block.no_additional_params):
            name = "param_label_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for var in range(block.no_variables):
            name = "min_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(var + 1)
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
        # pylint: disable=too-many-statements
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
        for _ in range(block.no_comment_lines):
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
        for var in range(block.no_variables):
            name = "variable_label_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
            name = "variable_units_" + str(var + 1)
            setattr(block, name, self.data.pop(0).strip())
        block.signal_mode = self.data.pop(0).strip()
        block.dwell_time = float(self.data.pop(0).strip())
        block.no_scans = int(self.data.pop(0).strip())
        block.time_correction = self.data.pop(0).strip()
        block.sample_angle_tilt = float(self.data.pop(0).strip())
        block.sample_tilt_azimuth = float(self.data.pop(0).strip())
        block.sample_rotation = float(self.data.pop(0).strip())
        block.no_additional_params = int(self.data.pop(0).strip())
        for param in range(block.no_additional_params):
            name = "param_label_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_unit_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
            name = "param_value_" + str(param + 1)
            setattr(block, name, self.data.pop(0))
        block.num_ord_values = int(self.data.pop(0).strip())
        for var in range(block.no_variables):
            name = "min_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))
            name = "max_ord_value_" + str(var + 1)
            setattr(block, name, float(self.data.pop(0).strip()))

        self._add_data_values(block)

        return block

    def _add_data_values(self, block):
        """Add data values to a Vamas data block."""
        data_dict = {}
        start = float(block.abscissa_start)
        step = float(block.abscissa_step)
        num = int(block.num_ord_values / block.no_variables)
        energy = [round(start + i * step, 2) for i in range(num)]

        if block.abscissa_label == "binding energy":
            energy.reverse()

        setattr(block, "x", energy)

        for var in range(block.no_variables):
            if var == 0:
                name = "y"
            else:
                name = "y" + str(var)
            data_dict[name] = []

        data_array = list(np.array(self.data[: block.num_ord_values], dtype=float))

        self.data = self.data[block.num_ord_values :]

        for var in range(block.no_variables):
            max_var = block.no_variables
            if var == 0:
                name = "y"
            else:
                name = "y" + str(var)
            data_array_slice = data_array[var::max_var]
            data_dict[name] = data_array_slice
            setattr(block, name, data_dict[name])
