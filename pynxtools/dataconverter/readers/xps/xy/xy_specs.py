"""
Parser for reading XPS (X-ray Photoelectron Spectroscopy) data from
Specs Lab Prodigy XY exports, to be passed to mpes nxdl
(NeXus Definition Language) template.
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

# pylint: disable=too-many-lines,too-many-instance-attributes

import re
import itertools
from collections import OrderedDict
import copy
from datetime import datetime
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.reader_utils import (
    XPSMapper,
    check_uniform_step_width,
    get_minimal_step,
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class XyMapperSpecs(XPSMapper):
    """
    Class for restructuring .xy data file from
    Specs vendor into python dictionary.
    """

    config_file = "config_specs_xy.json"

    def __init__(self):
        super().__init__()
        self.write_channels_to_data = True

    def _select_parser(self):
        return XyProdigyParser()

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the Specs XY parser.

        Parameters
        ----------
        file : str
            Filepath of the XY file.
        **kwargs : dict
            write_channels_to_data: bool
                If True, the spectra of each individual channel is
                written to the entry/data field in the MPES template.

        Returns
        -------
        dict
            Flattened dictionary to be passed to MPES template.

        """
        if "write_channels_to_data" in kwargs:
            self.write_channels_to_data = kwargs["write_channels_to_data"]

        return super().parse_file(file, **kwargs)

    def construct_data(self):
        """Map XY format to NXmpes-ready dict."""
        # pylint: disable=duplicate-code
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "user": [],
            "instrument": [
                "work_function",
            ],
            "source": [
                "source_label",
            ],
            "beam": ["excitation_energy"],
            "analyser": ["analyser_name"],
            "collectioncolumn": ["lens_mode"],
            "energydispersion": [
                "scan_mode",
                "pass_energy",
            ],
            "detector": [
                "detector_voltage",
            ],
            "manipulator": [],
            "sample": ["target_bias"],
            "calibration": [],
            "data": [
                "x_units",
                "y_units",
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
                "spectrum_id",
                "cycle_no",
            ],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals,duplicate-code
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["group_name"]}'
        region_parent = f'{group_parent}/regions/RegionData_{spectrum["region_name"]}'
        file_parent = f"{region_parent}/file_info"
        instrument_parent = f"{region_parent}/instrument"
        analyser_parent = f"{instrument_parent}/analyser"

        path_map = {
            "file_info": f"{file_parent}",
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
                    mpes_key = spectrum_key
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]
                except KeyError:
                    pass

        if self.parser.export_settings["Transmission Function"]:
            path = f"{path_map['collectioncolumn']}/transmission_function"
            self._xps_dict[path] = spectrum["data"]["transmission_function"]
            self._xps_dict[f"{path}/units"] = spectrum["tf_units"]

        # Create keys for writing to data and detector
        entry = construct_entry_name(region_parent)
        scan_key = construct_data_key(spectrum)
        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'

        x_units = spectrum["x_units"]
        energy = np.array(spectrum["data"]["x"])
        intensity = np.array(spectrum["data"]["y"])

        if entry not in self._xps_dict["data"]:
            self._xps_dict["data"][entry] = xr.Dataset()

        # Write raw data to detector.
        self._xps_dict[detector_data_key] = intensity

        if not self.parser.export_settings["Separate Channel Data"]:
            averaged_channels = intensity
        else:
            all_channel_data = [
                value
                for key, value in self._xps_dict.items()
                if detector_data_key.split("Channel_")[0] in key
            ]
            averaged_channels = np.mean(all_channel_data, axis=0)

        if not self.parser.export_settings["Separate Scan Data"]:
            averaged_scans = intensity
        else:
            all_scan_data = [
                value
                for key, value in self._xps_dict.items()
                if detector_data_key.split("Scan_")[0] in key
            ]
            averaged_scans = np.mean(all_scan_data, axis=0)

        # Write to data in order: scan, cycle, channel

        # Write averaged cycle data to 'data'.
        self._xps_dict["data"][entry][scan_key.split("_")[0]] = xr.DataArray(
            data=averaged_scans,
            coords={x_units: energy},
        )
        if self.parser.export_settings["Separate Scan Data"]:
            # Write average cycle data to 'data'.
            self._xps_dict["data"][entry][scan_key] = xr.DataArray(
                data=averaged_channels,
                coords={x_units: energy},
            )

        if (
            self.parser.export_settings["Separate Channel Data"]
            and self.write_channels_to_data
        ):
            # Write channel data to 'data'.
            channel_no = spectrum["channel_no"]
            self._xps_dict["data"][entry][
                f"{scan_key}_chan{channel_no}"
            ] = xr.DataArray(data=intensity, coords={x_units: energy})


class XyProdigyParser:  # pylint: disable=too-few-public-methods
    """
    A parser for reading in ASCII-encoded .xy data from Specs Prodigy.

    Tested with SpecsLab Prodigy v 4.64.1-r88350.
    """

    def __init__(self):
        """
        Construct the parser.

        """
        self.lines = []
        self.prefix = "#"
        self.n_headerlines = 14
        self.export_settings = {}

        self.settings_map = {
            "Acquisition Date": "time_stamp",
            "Analysis Method": "analysis_method",
            "Analyzer": "analyser_name",
            "Analyzer Lens": "lens_mode",
            "Analyzer Slit": "entrance_slit",
            "Bias Voltage": "bias_voltage",
            "Binding Energy": "start_energy",
            "Scan Mode": "scan_mode",
            "Values/Curve": "n_values",
            "Eff. Workfunction": "work_function",
            "Excitation Energy": "excitation_energy",
            "Kinetic Energy": "kinetic_energy",
            "Dwell Time": "dwell_time",
            "Detector Voltage": "detector_voltage",
            "Comment": "comments",
            "Curves/Scan": "curves_per_scan",
            "Pass Energy": "pass_energy",
            "Source": "source_label",
            "Spectrum ID": "spectrum_id",
        }

    def parse_file(self, file, **kwargs):
        """
        Parse the .xy file into a list of dictionaries.

        Parsed data is stored in the attribute 'self.data'.
        Each dictionary in the data list is a grouping of related
        attributes. The dictionaries are later re-structured into a
        nested dictionary that more closely resembles the domain logic.

        Parameters
        ----------
        file : str
            XPS data filepath.

        **kwargs : dict
            commentprefix : str
                Prefix for comments in xy file. The default is "#".
            n_headerlines: int
                number of header_lines in each data block.

        Returns
        -------
        list
            Flat list of dictionaries containing one spectrum each.

        """
        if "commentprefix" in kwargs:
            self.prefix = kwargs["commentprefix"]
        if "n_headerlines" in kwargs:
            self.n_headerlines = kwargs["n_headerlines"]

        self.lines = self._read_lines(file)
        header, data = self._separate_header()
        self.export_settings = self._parse_export_settings(header)

        # Recursively read XPS data from flar 'lines' list.
        groups = self._handle_groups(data)

        return self._flatten_dict(groups)

    def _read_lines(self, file):
        """
        Read all lines from the input XY files.

        Parameters
        ----------
        file : str
            Filepath of the XY file to be read.

        Returns
        -------
        lines : list
            All lines in the XY file.

        """
        with open(file, encoding="utf-8") as xy_file:
            lines = xy_file.readlines()

        return lines

    def _separate_header(self):
        """
        Split of common export header.

        Returns
        -------
        header : list
            List of export settings.
        groups : list
            List of list containing data strings.

        """
        header = self.lines[: self.n_headerlines]
        groups = self.lines[self.n_headerlines :]

        return header, groups

    def _parse_export_settings(self, header):
        """
        Parse the top-level Prodigy export settings into a dict.

        Parameters
        ----------
        header : list
            List of header strings.

        Returns
        -------
        export_settings : dict
            Dictionary of export settings.

        """
        bool_map = {
            "yes": True,
            "no": False,
        }

        export_settings = {}
        for line in header:
            line = line.strip(self.prefix).strip()
            if len(line) == 0:
                pass
            else:
                setting = line.split(":", 1)[1].strip()
                setting = bool_map.get(setting)
                export_settings[line.split(":", 1)[0].strip()] = setting

        return export_settings

    def _handle_groups(self, data):
        """
        Separate the data list into a dictionary, with each
        element containing the data list of one group.

        Parameters
        ----------
        data : list
            Full data list (list of strings).

        Returns
        -------
        groups : dict
            Dict with data organized by group
            Entries are as group_name: group_data.

        """
        grouped_list = [
            list(g)
            for _, g in itertools.groupby(
                data, lambda line: "Group:" in line.strip(self.prefix).strip()
            )
        ][1:]

        groups = OrderedDict()

        for name_header, group_data in zip(grouped_list[::2], grouped_list[1::2]):
            name = self._strip_param(name_header[0], "Group:")
            group_settings = {"group_name": name}
            groups[name] = {
                "group_settings": self._replace_keys(group_settings, self.settings_map),
            }
            groups[name].update(self._handle_regions(group_data))

        return groups

    def _handle_regions(self, group_data):
        """
        Separate the data list of an individual group into a
        dictionary, with each element containing the data list
        of one region.

        Parameters
        ----------
        group_data : list
            Group data list (list of strings).

        Returns
        -------
        regions : dict
            Dict with data organized by group
            Entries are as region_name: region_data.

        """
        grouped_list = [
            list(g)
            for _, g in itertools.groupby(
                group_data, lambda line: "Region:" in line.strip(self.prefix).strip()
            )
        ][1:]

        regions = OrderedDict()

        for name_header, region_data in zip(grouped_list[::2], grouped_list[1::2]):
            region_settings = {}
            name = self._strip_param(name_header[0], "Region:")
            region_settings["region_name"] = name

            for i, setting in enumerate(region_data):
                if not setting.startswith(self.prefix):
                    region_data = region_data[i:]
                    break
                setting_name = setting.split(self.prefix)[-1].strip().split(":")[0]
                val = setting.split(self.prefix)[-1].strip().split(":")[1].strip()
                region_settings[setting_name] = val

            regions[name] = {
                "region_settings": self._replace_keys(
                    region_settings, self.settings_map
                ),
            }
            regions[name].update(self._handle_cycles(region_data))

        return regions

    def _handle_cycles(self, region_data):
        """
        Separate the data list of an individual region into a
        dictionary, with each element containing the data list
        of one cycle.

        Parameters
        ----------
        region_data : list
            Region data list (list of strings).

        Returns
        -------
        cycles : dict
            Dict with data organized by cycle
            Entries are as cycle_name: cycle_data.

        """
        cycle_pattern = re.compile(rf"{self.prefix} Cycle: \d\n", re.IGNORECASE)

        cycles = OrderedDict()
        cycle_line_nrs = {}

        for i, line in enumerate(region_data):
            if cycle_pattern.match(line):
                cycle_line_nrs[
                    "cycle_" + str(int(self._strip_param(line, "Cycle:")))
                ] = i
            if i == len(region_data) - 1:
                cycle_line_nrs["end"] = i + 1

        for i, (line_no_a, line_no_b) in enumerate(
            zip(list(cycle_line_nrs.values()), list(cycle_line_nrs.values())[1:])
        ):
            name = f"cycle_{i}"
            cycle_settings = {"loop_no": i}
            cycle_data = region_data[line_no_a:line_no_b]

            cycles[name] = {
                "cycle_settings": self._replace_keys(cycle_settings, self.settings_map),
            }
            cycles[name].update(self._handle_individual_cycles(cycle_data))

        return cycles

    def _handle_individual_cycles(self, cycle_data):
        """
        Separate the data list of an individual cycle into a
        dictionary, with each element containing the data list
        of one scan.

        Parameters
        cycle_data : list
            Cycle data list (list of strings).

        Returns
        -------
        scan : dict
            Dict with data organized by cycle
            Entries are as scan_name: scan_data.

        """
        spec_pattern = rf"{self.prefix} Cycle: \d, Curve: \d"
        if self.export_settings["Separate Scan Data"]:
            spec_pattern += r", Scan: \d"
        if self.export_settings["Separate Channel Data"]:
            spec_pattern += r", Channel: \d"
        spec_pattern = re.compile(spec_pattern, re.IGNORECASE)

        scans = OrderedDict()
        scan_line_nrs = {}

        for i, line in enumerate(cycle_data):
            if spec_pattern.match(line):
                name_dict = dict(
                    (a.strip(), int(b.strip()))
                    for a, b in (
                        element.split(": ")
                        for element in line.strip(self.prefix).strip().split(", ")
                    )
                )
                name = "".join(
                    [
                        f"{key.lower()}_{val}_"
                        for key, val in name_dict.items()
                        if key != "Curve"
                    ]
                ).rstrip("_")
                scan_line_nrs[name] = i
            if i == len(cycle_data) - 1:
                scan_line_nrs["end"] = i + 1

        for i, ((name, line_no_a), line_no_b) in enumerate(
            zip(list(scan_line_nrs.items()), list(scan_line_nrs.values())[1:])
        ):
            scan_data = cycle_data[line_no_a:line_no_b]
            scan = self._handle_individual_scan(scan_data)
            scan["scan_settings"].update(self._extend_scan_settings(name))
            scans[name] = scan

        return scans

    def _handle_individual_scan(self, scan_data):
        """
        Separate the data list of an individual scan into a
        dictionary, with each element containing the data and
        metadata of one spectrum.

        Parameters
        scan_data : list
            Scan data list (list of strings).

        Returns
        -------
        scan : dict
            Dict with scan data and metadata
            Entries are as
            scan_name: {
                "data": scan_data,
                "scan_settings": scan_settings
                }

        """
        energy = []
        intensity = []
        transmission_function = []
        scan_settings = {}

        for line in scan_data:
            if line.startswith(self.prefix) and line.strip(self.prefix).strip("\n"):
                key, val = [
                    item.strip()
                    for item in line.strip(self.prefix).strip("\n").split(":", 1)
                ]
                if key == "Acquisition Date":
                    scan_settings[key] = self._parse_datetime(val)

                if key == "ColumnLabels":
                    if not self.export_settings["Transmission Function"]:
                        x_units, y_units = val.split(" ")
                        scan_settings["x_units"] = x_units
                        scan_settings["y_units"] = self._reformat_y_units(y_units)

                    else:
                        x_units, y_units, tf_units = val.split(" ")
                        scan_settings["x_units"] = x_units
                        scan_settings["y_units"] = self._reformat_y_units(y_units)
                        scan_settings["tf_units"] = tf_units

            if not line.startswith(self.prefix) and line.strip("\n"):
                data = line.strip("\n").split(" ")
                data = [d for d in data if d]
                energy.append(float(data[0]))
                intensity.append(float(data[1]))
                if self.export_settings["Transmission Function"]:
                    transmission_function.append(float(data[2]))

        if check_uniform_step_width(energy):
            scan_settings["step_size"] = get_minimal_step(energy)

        scan = {
            "data": {
                "x": np.array(energy),
                "y": np.array(intensity),
            },
            "scan_settings": self._replace_keys(scan_settings, self.settings_map),
        }

        if self.export_settings["Transmission Function"]:
            scan["data"]["transmission_function"] = np.array(transmission_function)

        return scan

    def _extend_scan_settings(self, scan_name):
        """
        Split the scan name and extract the scan metadata.

        Example:
            scan_name == scan_0_channel_0
            -> settings = {'scan_no': 0, 'channel_no': 0}

        Parameters
        ----------
        scan_name : str
            String with the name of the scan, in the format
            scan_0_channel_0.

            Channel number is optional.

        Returns
        -------
        settings : dict
            Dict with scan settings.

        """
        settings = {}

        split_name = scan_name.split("_")

        for param, val in zip(split_name[::2], split_name[1::2]):
            if param != "cycle":
                settings[f"{param}_no"] = int(val)

        return settings

    def _strip_param(self, line, key):
        """
        Split the scan name and extract the scan metadata.

        Example:
            if self.prefix = "#"
            line = Cycle: # Cycle: 5, key = "Cycle:\n"
            -> return 5

        Parameters
        ----------
        line : str
            String containing the string self.prefix + " " + key"
        key : str
            Keyword to strip from line.

        Returns
        -------
        str
            Stripped line without prefix and key.

        """
        if key in line:
            return line.strip().split(self.prefix + " " + key)[-1].strip()
        return line

    def _flatten_dict(self, data_dict):
        """
        Flatten a raw data dict into a list, with each element
        being a dictionary with data and metadata for one spectrum.

        Parameters
        ----------
        data_dict : dict
            Nested dictionary containing group, regions, cycles,
            and scans.

        Returns
        -------
        spectra : list
            Flattened list of spectra dicts.

        """
        spectra = []

        for group in data_dict.values():
            group_settings = group["group_settings"]
            for region in list(group.values())[1:]:
                region_settings = region["region_settings"]
                for cycle in list(region.values())[1:]:
                    cycle_settings = cycle["cycle_settings"]
                    for scan in list(cycle.values())[1:]:
                        scan_settings = scan["scan_settings"]
                        spectrum = {}
                        for settings in [
                            group_settings,
                            region_settings,
                            cycle_settings,
                            scan_settings,
                        ]:
                            spectrum.update(settings)
                        spectrum["data"] = scan["data"]
                        spectra.append(spectrum)

        return spectra

    def _parse_datetime(self, date):
        """
        Parse datetime into a datetime.datetime object.

        Parameters
        ----------
        date : str
            String representation of the date in the format
            "%m/%d/%y %H:%M:%S".

        Returns
        -------
        date_object : datetime.datetime
            Datetime in datetime.datetime format.

        """
        if date.find("UTC"):
            date = date[: date.find("UTC")].strip()
        else:
            date = date.strip()

        date_object = datetime.strptime(date, "%m/%d/%y %H:%M:%S")

        return date_object

    def _replace_keys(self, dictionary, key_map):
        """
        Replaced keys in dictionar if there is a replacement in
        key_map.

        Parameters
        ----------
        dictionary : dict
            Input non-nested dictionary.
        key_map : dict
            Dictionary with mapping for different keys.

        Returns
        -------
        dictionary : dict
            Updated dictionary with new keys.

        """
        for key in key_map.keys():
            if key in dictionary.keys():
                dictionary[key_map[key]] = dictionary[key]
                dictionary.pop(key, None)
        return dictionary

    def _reformat_y_units(self, y_units):
        """
        Map y_units to shortened values.

        Parameters
        ----------
        y_units : str
            String value for intensity units.

        Returns
        -------
        str
            Shortened intensity units.

        """
        unit_map = {"counts/s": "CPS", "counts": "Counts"}

        return unit_map[y_units]
