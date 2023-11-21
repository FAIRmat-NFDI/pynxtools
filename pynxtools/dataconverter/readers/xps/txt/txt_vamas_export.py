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

# pylint: disable=too-many-lines

import itertools
import operator
import copy
from abc import ABC, abstractmethod
from scipy.interpolate import interp1d
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.reader_utils import (
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class TxtParserVamasExport:
    """
    Class for restructuring .txt data file from
    Casa TXT export (from Vamas) into python dictionary.
    """

    config_file = "config_sle_txt_vamas_export.json"

    def __init__(self):
        self.raw_data: list = []
        self._xps_dict: dict = {}
        self._root_path = "/ENTRY[entry]"

        self.parser_map = {
            "rows_of_tables": TextParserRows,
            "columns_of_tables": TextParserColumns,
        }

        self.raw_data: list = []
        self._xps_dict: dict = {}

        self._root_path = "/ENTRY[entry]"

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the Scienta TXT parser.

        """
        self.parser = self.parser_map[self._get_file_type(file)]()
        self.raw_data = self.parser.parse_file(file, **kwargs)

        file_key = f"{self._root_path}/File"
        self._xps_dict[file_key] = file

        self.construct_data()

        return self.data_dict

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
        with open(file) as f:
            first_line = f.readline()
            if first_line.startswith("Cycle"):
                return "columns_of_tables"
            return "rows_of_tables"

    @property
    def data_dict(self) -> dict:
        """Getter property."""
        return self._xps_dict

    def construct_data(self):
        """Map TXT format to NXmpes-ready dict."""
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "file_info": [],
            "user": [],
            "instrument": [],
            "source": [],
            "beam": [
                "excitation_energy",
                "excitation_energy/@units",
            ],
            "analyser": [],
            "collectioncolumn": [],
            "energydispersion": [],
            "detector": [
                "dwell_time",
                "dwell_time/@units",
            ],
            "manipulator": [],
            "calibration": [],
            "sample": ["sample_name"],
            "data": [
                "dwell_time",
                "y_units",
            ],
            "region": [
                "region_name",
                "start_energy",
                "stop_energy",
            ],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["spectrum_type"]}'
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

        entry = construct_entry_name(region_parent)
        self._xps_dict["data"][entry] = xr.Dataset()

        scan_key = construct_data_key(spectrum)

        energy = np.array(spectrum["data"]["binding_energy"])

        self._xps_dict["data"][entry][scan_key] = xr.DataArray(
            data=spectrum["data"]["intensity"], coords={"energy": energy}
        )

        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'

        self._xps_dict[detector_data_key] = spectrum["data"]["intensity"]


def safe_arange_with_edges(start, stop, step):
    """
    In order to avoid float point errors in the division by step.

    Parameters
    ----------
    start : float
        Smallest value.
    stop : float
        Biggest value.
    step : float
        Step size between points.

    Returns
    -------
    ndarray
        1D array with values in the interval (start, stop),
        incremented by step.

    """
    return step * np.arange(start / step, (stop + step) / step)


def _resample_array(y, x0, x1):
    """
    Resample an array (y) which has the same initial spacing
    of another array(x0), based on the spacing of a new
    array(x1).

    Parameters
    ----------
    y : array
        Lineshape array.
    x0 : array
        x array with old spacing.
    x1 : array
        x array with new spacing.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    fn = interp1d(x0, y, axis=0, fill_value="extrapolate")
    return fn(x1)


class TextParser(ABC):
    """
    Parser for ASCI files exported from CasaXPS.
    """

    def __init__(self, **kwargs):
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
        if "n_headerlines" in kwargs.keys():
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
        with open(file) as f:
            for line in f:
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

    def _check_uniform_step_width(self, x):
        """
        Check to see if a non-uniform step width is used in the spectrum

        Parameters
        ----------
        x : list
            List of data points.

        Returns
        -------
        bool
            False if list is non-uniformally spaced.

        """
        start = x[0]
        stop = x[-1]
        step = self._get_minimal_step(x)

        if step != 0.0 and np.abs((stop - start) / step) > len(x):
            return False
        return True

    def _get_minimal_step(self, x):
        """
        Return the minimal difference between two consecutive values
        in a list. Used for extracting minimal difference in a
        list with non-uniform spacing.

        Parameters
        ----------
        x : list
            List of data points.

        Returns
        -------
        step : float
            Non-zero, minimal distance between consecutive data
            points in x.

        """
        x1 = np.roll(x, -1)
        diff = np.abs(np.subtract(x, x1))
        step = round(np.min(diff[diff != 0]), 2)

        return step

    def _interpolate(self, x, array_list):
        """
        Interpolate data points in case a non-uniform step width was used.

        Parameters
        ----------
        x : list
            List of non-uniformally spaced data points.
        array_list : list
            List of arrays to be interpolated according to new x axis.

        Returns
        -------
        x, array_list
            Interpolated x axis and list of arrays

        """
        if not isinstance(array_list, list):
            array_list = [array_list]
        start = x[0]
        stop = x[-1]
        step = self._get_minimal_step(x)
        if start > stop:
            new_x = np.flip(safe_arange_with_edges(stop, start, step))
        else:
            new_x = safe_arange_with_edges(start, stop, step)

        output_list = [_resample_array(arr, x, new_x) for arr in array_list]

        return new_x, output_list


class TextParserRows(TextParser):
    """
    Parser for ASCI files exported from CasaXPS using the
    'Rows of Tables' option.
    """

    def __init__(self, **kwargs):
        super(TextParserRows, self).__init__(**kwargs)
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
            spectra += [spec_settings | spec_data]

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
            sample_name = spec_header.split(":")[1]
            region = spec_header.split(":")[2]
            spectrum_type = sample_name + "_" + region
            spectrum_settings = {
                "sample_name": sample_name,
                "region_name": region,
                "spectrum_type": spectrum_type,
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

        lines = [[] for _ in range(max([len(l) for l in data_lines]))]

        for line in data_lines:
            for i, data_point in enumerate(line):
                try:
                    lines[i].append(float(data_point.strip("\n")))
                except ValueError:
                    pass

        data = []

        for x_bin, y in zip(lines[::2], lines[1::2]):
            x_bin, y = np.array(x_bin), np.array(y)

            if self.uniform_energy_steps and not self._check_uniform_step_width(x_bin):
                x_bin, y = self._interpolate(x_bin, y)

            spectrum = {
                "binding_energy": np.array(x_bin),
                "intensity": np.array(y).squeeze(),
            }

            data += [
                {
                    "data": spectrum,
                    "step_size": self._check_uniform_step_width(x_bin),
                    "start_energy": x_bin[0],
                    "stop_energy": x_bin[-1],
                }
            ]

        return data


class TextParserColumns(TextParser):
    """
    Parser for ASCI files exported from CasaXPS using the
    'Columns of Tables' option.
    """

    def __init__(self, **kwargs):
        super(TextParserColumns, self).__init__(**kwargs)
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
        settings : dict
            Dict of measurement settings for one spectrum.

        """
        sample_name = header[0].split(":")[1]
        region = header[0].split(":")[2].split("\n")[0]
        spectrum_type = sample_name + "_" + region
        settings = {
            "sample_name": sample_name,
            "region_name": region,
            "spectrum_type": spectrum_type,
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
        y = lines[:, 1]

        if self.uniform_energy_steps and not self._check_uniform_step_width(x_kin):
            x_kin, (x_bin, y) = self._interpolate(x_kin, [x_bin, y])

        return {
            "kinetic_energy": np.array(x_kin),
            "binding_energy": np.array(x_bin),
            "intensity": np.array(y).squeeze(),
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
                    "step_size": self._check_uniform_step_width(kinetic_energy),
                    "start_energy": kinetic_energy[0],
                    "stop_energy": kinetic_energy[-1],
                }
            )
            spectra += [block_settings | block_data]

        return spectra


if __name__ == "__main__":
    filepaths = [
        r"C:\Users\pielsticker\Downloads\vm_test_rows_r.txt",
        r"C:\Users\pielsticker\Downloads\vm_test_rows_irr.txt",
        r"C:\Users\pielsticker\Downloads\vm_test_cols_r.txt",
        r"C:\Users\pielsticker\Downloads\vm_test_cols_irr.txt",
    ]

    l = []

    for file in filepaths:
        p = TxtParserVamasExport()
        new_dict = p.parse_file(file=file, uniform_energy_steps=True)
        l.append(new_dict)
