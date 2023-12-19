"""
Classes for reading XPS files from TXT export of CasaXPS.
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
# pylint: disable=too-many-lines,too-few-public-methods

import itertools
import operator
import copy
from abc import ABC, abstractmethod
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.reader_utils import (
    XPSMapper,
    check_uniform_step_width,
    get_minimal_step,
    interpolate_arrays,
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class TxtMapperVamasExport(XPSMapper):
    """
    Class for restructuring .txt data file from
    Casa TXT export (from Vamas) into python dictionary.
    """

    config_file = "config_txt_vamas_export.json"

    def __init__(self):
        self.parser_map = {
            "rows_of_tables": TextParserRows,
            "columns_of_tables": TextParserColumns,
        }
        super().__init__()

    def _get_file_type(self, file):
        """
        Check which export option was used in CasaXPS.

        Parameters
        ----------
        file : str
            XPS data filepath.

        Returns
        -------
        str
            Either columns_of_tables or rows_of_tables.

        """
        with open(file, encoding="utf-8") as txt_file:
            first_line = txt_file.readline()
            if first_line.startswith("Cycle"):
                return "columns_of_tables"
            return "rows_of_tables"

    def _select_parser(self):
        """
        Select parser based on the structure of the text file

        Returns
        -------
        TextParser
            TextParser for CasaXPS export from Vamas files.

        """
        return self.parser_map[self._get_file_type(self.file)]()

    def construct_data(self):
        """Map TXT format to NXmpes-ready dict."""
        # pylint: disable=duplicate-code
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "file_info": [],
            "user": [],
            "instrument": [],
            "source": [],
            "beam": [
                "excitation_energy",
                "excitation_energy/units",
            ],
            "analyser": [],
            "collectioncolumn": [],
            "energydispersion": [],
            "detector": [
                "dwell_time",
                "dwell_time/units",
            ],
            "manipulator": [],
            "calibration": [],
            "sample": [],
            "data": [
                "dwell_time",
                "x_units" "y_units",
                "start_energy",
                "stop_energy",
                "step_size",
            ],
            "region": ["region_name"],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals,duplicate-code
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["group_name"]}'
        region_parent = f'{group_parent}/regions/RegionData_{spectrum["spectrum_type"]}'
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

        # Create keys for writing to data and detector
        entry = construct_entry_name(region_parent)
        scan_key = construct_data_key(spectrum)
        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'

        energy = np.array(spectrum["data"]["binding_energy"])
        intensity = np.array(spectrum["data"]["intensity"])

        # If multiple spectra exist to entry, only create a new
        # xr.Dataset if the entry occurs for the first time.
        if entry not in self._xps_dict["data"]:
            self._xps_dict["data"][entry] = xr.Dataset()

        # Write averaged cycle data to 'data'.
        all_scan_data = [
            value
            for key, value in self._xps_dict["data"][entry].items()
            if scan_key.split("_")[0] in key
        ]
        averaged_scans = np.mean(all_scan_data, axis=0)
        if averaged_scans.size == 1:
            # on first scan in cycle
            averaged_scans = intensity

        self._xps_dict["data"][entry][scan_key.split("_")[0]] = xr.DataArray(
            data=averaged_scans,
            coords={"energy": energy},
        )

        self._xps_dict["data"][entry][scan_key] = xr.DataArray(
            data=intensity, coords={"energy": energy}
        )

        self._xps_dict[detector_data_key] = intensity


class TextParser(ABC):  # pylint: disable=too-few-public-methods
    """
    Parser for ASCI files exported from CasaXPS.
    """

    def __init__(self):
        self.lines = []
        self.data_dict = []
        self.n_headerlines = 7
        self.uniform_energy_steps = True

    def parse_file(self, file, uniform_energy_steps=True, **kwargs):
        """
        Parse the file into a list of dictionaries.

        Parsed data stored in the attribute 'self.data'.

        Parameters
        ----------
        file : str
            XPS data filepath.
        uniform_energy_steps : bool, optional
            If true, the spectra are interpolate to have uniform
            energy steps. The default is True.
        **kwargs : dict
            n_headerlines: number of header_lines in each data block.

        Returns
        -------
        dict
            DESCRIPTION.

        """
        if "n_headerlines" in kwargs:
            self.n_headerlines = kwargs["n_headerlines"]

        self.uniform_energy_steps = uniform_energy_steps

        self._read_lines(file)
        blocks = self._parse_blocks()
        return self._build_list_of_dicts(blocks)

    def _read_lines(self, file):
        """
        Read in all lines from the file as a list of strings.

        Parameters
        ----------
        file : str
            XPS data filepath.

        Returns
        -------
        None.

        """
        with open(file, encoding="utf-8") as txt_file:
            for line in txt_file:
                self.lines += [line]

    @abstractmethod
    def _parse_blocks(self):
        """
        Extract spectrum blocks from full data string.

        This method has to be implemented in the inherited parsers.

        Returns
        -------
        blocks : list
            List of strings, with each string containing one spectrum's
            data and metadata.

        """
        blocks = []

        return blocks

    @abstractmethod
    def _build_list_of_dicts(self, blocks):
        """
        Build list of dictionaries, with each dict containing data
        and metadata of one spectrum (block).

        This method has to be implemented in the inherited parsers.

        Parameters
        ----------
        blocks : list
            List of data blocks containing one spectrum each.

        Returns
        -------
        spectra : list
            List of dicts with spectrum data and metadata.

        """
        spectra = []

        return spectra

    def _separate_header_and_data(self, block):
        """
        Separate header (with metadata) from data for one measurement
        block

        Returns
        -------
        None.

        """
        header = block[: self.n_headerlines]
        data = block[self.n_headerlines :]

        return header, data


class TextParserRows(TextParser):
    """
    Parser for ASCI files exported from CasaXPS using the
    'Rows of Tables' option.
    """

    def __init__(self):
        super().__init__()
        self.n_headerlines = 7

    def _parse_blocks(self):
        """
        With the 'Rows of Tables' option, there is only one block
        with common metadata.

        """
        return self.lines

    def _build_list_of_dicts(self, blocks):
        """
        Build list of dictionaries, with each dict containing data
        and metadata of one spectrum.

        Parameters
        ----------
        blocks : list
            List of data blocks containing one spectrum each.

        Returns
        -------
        spectra : list
            List of dicts with spectrum data and metadata.

        """
        spectra = []

        header, data_lines = self._separate_header_and_data(blocks)
        settings = self._parse_header(header)
        data = self._parse_data(data_lines)
        for spec_settings, spec_data in zip(settings, data):
            spectra += [{**spec_settings, **spec_data}]

        return spectra

    def _parse_header(self, header):
        """
        Parse header into metadata dictionary.

        Parameters
        ----------
        header : str
            Header data for one spectrum as a String.

        Returns
        -------
        settings : list
            List of dicts with measurement settings for
            one spectrum each.

        """
        settings = []
        for spec_header in header[-1].split("\t")[1::3]:
            group_name = spec_header.split(":")[1]
            region = spec_header.split(":")[2]
            spectrum_settings = {
                "group_name": group_name,
                "spectrum_type": region,
                "x_units": "binding",
                "y_units": spec_header.split(":")[3],
            }
            settings += [spectrum_settings]

        return settings

    def _parse_data(self, data_lines):
        """
        Extract energy and intensity data.

        Parameters
        ----------
        data_lines : list
            List of lines with measurement data.

        Returns
        -------
        list
            List of dicts containing the binding energy
            and the intensity axes of one spectrum each.

        """
        data_lines = [x.split("\t") for x in data_lines]
        for line in data_lines:
            del line[2::3]
            del line[-1]

        lines = [[] for _ in range(max(len(line) for line in data_lines))]

        for line in data_lines:
            for i, data_point in enumerate(line):
                try:
                    lines[i].append(float(data_point.strip("\n")))
                except ValueError:
                    pass

        data = []

        for x_bin, intensity in zip(lines[::2], lines[1::2]):
            x_bin, intensity = np.array(x_bin), np.array(intensity)

            if self.uniform_energy_steps and not check_uniform_step_width(x_bin):
                x_bin, intensity = interpolate_arrays(x_bin, intensity)

            spectrum = {
                "data": {
                    "binding_energy": np.array(x_bin),
                    "intensity": np.array(intensity).squeeze(),
                },
                "start_energy": x_bin[0],
                "stop_energy": x_bin[-1],
                "x_units": "binding",
                "y_units": "CPS",
            }

            if check_uniform_step_width(x_bin):
                spectrum["step_size"] = get_minimal_step(x_bin)

            data += [spectrum]

        return data


class TextParserColumns(TextParser):
    """
    Parser for ASCI files exported from CasaXPS using the
    'Columns of Tables' option.
    """

    def __init__(self):
        super().__init__()
        self.n_headerlines = 8

    def _parse_blocks(self):
        """
        Extract spectrum blocks from full data string.

        Returns
        -------
        blocks : list
            List of strings, with each string containing one spectrum's
            data and metadata.

        """
        blocks = [
            list(g) for _, g in itertools.groupby(self.lines, lambda i: "Cycle " in i)
        ]
        blocks = [operator.add(*blocks[i : i + 2]) for i in range(0, len(blocks), 2)]

        return blocks

    def _parse_block_header(self, header):
        """
        Parse spectrum block header into metadata dictionary.

        Parameters
        ----------
        header : str
            Header data for one spectrum as a String.

        Returns
        -------
        settings : dictf
            Dict of measurement settings for one spectrum.

        """
        group_name = header[0].split(":")[1]
        region = header[0].split(":")[2].split("\n")[0]
        settings = {
            "group_name": group_name,
            "spectrum_type": region,
            "excitation_energy": header[1].split("\t")[2],
            "excitation_energy/@units": header[1].split("\t")[1].split(" ")[-1],
            "dwell_time": float(header[1].split("\t")[4].strip()),
            "dwell_time/@units": header[1].split("\t")[3].split(" ")[-1],
        }

        return settings

    def _parse_block_data(self, block_data):
        """
        Extract energy and intensity data from one data block.

        Parameters
        ----------
        block_data : list
            List of lines with measurement data.

        Returns
        -------
        dict
            Dict containing the kinetic/binding energy
            and the intensity axes.

        """
        lines = np.array([[float(i) for i in d.split()] for d in block_data])

        x_kin = lines[:, 0]
        x_bin = lines[:, 2]
        intensity = lines[:, 1]

        if self.uniform_energy_steps and not check_uniform_step_width(x_kin):
            x_kin, (x_bin, intensity) = interpolate_arrays(x_kin, [x_bin, intensity])

        return {
            "kinetic_energy": np.array(x_kin),
            "binding_energy": np.array(x_bin),
            "intensity": np.array(intensity).squeeze(),
        }

    def _build_list_of_dicts(self, blocks):
        """
        Build list of dictionaries, with each dict containing data
        and metadata of one spectrum (block).


        Parameters
        ----------
        blocks : list
            List of data blocks containing one spectrum each.

        Returns
        -------
        spectra : list
            List of dicts with spectrum data and metadata.

        """
        spectra = []
        for block in blocks:
            header, block_data_lines = self._separate_header_and_data(block)
            block_settings = self._parse_block_header(header)
            block_data = {"data": self._parse_block_data(block_data_lines)}
            kinetic_energy = block_data["data"]["kinetic_energy"]
            block_settings.update(
                {
                    "start_energy": kinetic_energy[0],
                    "stop_energy": kinetic_energy[-1],
                }
            )
            if check_uniform_step_width(kinetic_energy):
                block_settings["step_size"] = get_minimal_step(kinetic_energy)

            spectra += [{**block_settings, **block_data}]

        return spectra
