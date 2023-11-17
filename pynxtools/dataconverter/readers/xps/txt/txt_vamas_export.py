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

import numpy as np

from pynxtools.dataconverter.readers.xps.reader_utils import (
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key
)

class TxtParserVamasExport():
    """
    Class for restructuring .txt data file from
    Scienta TXT export into python dictionary.
    """
    config_file = "config_sle_specs.json"

    def __init__(self):
        self.raw_data: list = []
        self._xps_dict: dict = {}
        self._root_path = '/ENTRY[entry]'

        self.parser = TextParser()


        self.raw_data: list = []
        self._xps_dict: dict = {}

        self._root_path = '/ENTRY[entry]'

    def parse_file(self, filepath, **kwargs):
        """
        Parse the file using the Scienta TXT parser.

        """
        self.raw_data = self.parser.parse_file(filepath, **kwargs)

        file_key = f'{self._root_path}/File'
        self._xps_dict[file_key] = filepath

        self.construct_data()

        return self.data_dict

    @property
    def data_dict(self) -> dict:
        """ Getter property."""
        return self._xps_dict

    ## Need to have a mapping function.

# =============================================================================
#     def construct_data(self):
#         """ Map TXT format to NXmpes-ready dict. """
#         spectra = copy.deepcopy(self.raw_data)
#
#         self._xps_dict["data"]: dict = {}
#
#         key_map = {
#             'file_info': [
#                 'data_file',
#                 'sequence_file'
#             ],
#             'user': [
#                 'user_initials',
#             ],
#             'instrument': [
#                 'instrument_name',
#                 'vendor',
#             ],
#             'source': [],
#             'beam': [
#                 'excitation_energy'
#             ],
#             'analyser': [],
#             'collectioncolumn': [
#                 'lens_mode',
#             ],
#             'energydispersion': [
#                 'acquisition_mode',
#                 'pass_energy',
#             ],
#             'detector': [
#                 'detector_first_x_channel',
#                 'detector_first_y_channel',
#                 'detector_last_x_channel',
#                 'detector_last_y_channel',
#                 'detector_mode',
#                 'dwell_time',
#             ],
#             'manipulator': [],
#             'calibration': [],
#             'sample': [
#                 'sample_name'
#             ],
#             'data': [
#                 'x_units',
#                 'energy_axis',
#                 'energy_type',
#                 'step_size',
#             ],
#             'region': [
#                 'center_energy',
#                 'energy_scale',
#                 'energy_size',
#                 'no_of_scans',
#                 'region_id',
#                 'spectrum_comment',
#                 'start_energy',
#                 'stop_energy',
#                 'time_stamp'
#             ],
#             # 'unused': [
#             #     'energy_unit',
#             #     'number_of_slices',
#             #     'software_version',
#             #     'spectrum_comment',
#             #     'start_date',
#             #     'start_time',
#             #     'time_per_spectrum_channel'
#             # ]
#         }
#
#         for spectrum in spectra:
#             self._update_xps_dict_with_spectrum(spectrum, key_map)
#
#     def _update_xps_dict_with_spectrum(self, spectrum, key_map):
#         """
#         Map one spectrum from raw data to NXmpes-ready dict.
#
#         """
#         # pylint: disable=too-many-locals
#         group_parent = f'{self._root_path}/RegionGroup_{spectrum["spectrum_type"]}'
#         region_parent = f'{group_parent}/regions/RegionData_{spectrum["region_name"]}'
#         file_parent = f'{region_parent}/file_info'
#         instrument_parent = f'{region_parent}/instrument'
#         analyser_parent = f'{instrument_parent}/analyser'
#
#         path_map = {
#             'file_info': f'{file_parent}',
#             'user': f'{region_parent}/user',
#             'instrument': f'{instrument_parent}',
#             'source': f'{instrument_parent}/source',
#             'beam': f'{instrument_parent}/beam',
#             'analyser': f'{analyser_parent}',
#             'collectioncolumn': f'{analyser_parent}/collectioncolumn',
#             'energydispersion': f'{analyser_parent}/energydispersion',
#             'detector': f'{analyser_parent}/detector',
#             'manipulator': f'{instrument_parent}/manipulator',
#             'calibration': f'{instrument_parent}/calibration',
#             'sample': f'{region_parent}/sample',
#             'data': f'{region_parent}/data',
#             'region': f'{region_parent}'
#         }
#
#         for grouping, spectrum_keys in key_map.items():
#             root = path_map[str(grouping)]
#             for spectrum_key in spectrum_keys:
#                 try:
#                     units = re.search(r'\[([A-Za-z0-9_]+)\]', spectrum_key).group(1)
#                     mpes_key = spectrum_key.rsplit(' ', 1)[0]
#                     self._xps_dict[f'{root}/{mpes_key}/@units'] = units
#                     self._xps_dict[f'{root}/{mpes_key}'] = spectrum[spectrum_key]
#                 except AttributeError:
#                     mpes_key = spectrum_key
#                     self._xps_dict[f'{root}/{mpes_key}'] = spectrum[spectrum_key]
#
#         entry = construct_entry_name(region_parent)
#         self._xps_dict["data"][entry] = xr.Dataset()
#
#         scan_key = construct_data_key(spectrum)
#
#         energy = np.array(spectrum["data"]["x"])
#
#         channel_key = f'{scan_key}_chan_0'
#         self._xps_dict["data"][entry][channel_key] = \
#             xr.DataArray(
#                 data=spectrum["data"]['y'],
#                 coords={"energy": energy})
#
#         self._xps_dict["data"][entry][scan_key] = \
#             xr.DataArray(
#                 data=spectrum["data"]['y'],
#                 coords={"energy": energy})
#
#         detector_data_key_child = construct_detector_data_key(spectrum)
#         detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'
#
#         self._xps_dict[detector_data_key] = spectrum["data"]['y']
# =============================================================================


class TextParser:
    """Parser for ASCI files exported from CasaXPS."""

    def __init__(self, **kwargs):
        self.data_dict = []

    def parse_file(self, filepath, **kwargs):
        """Parse the file into a list of dictionaries.

        Parsed data stored in the attribute 'self.data'.
        """
        if "n_headerlines" in kwargs.keys():
            self.n_headerlines = kwargs["n_headerlines"]
        else:
            self.n_headerlines = 4

        self._read_lines(filepath)
        self._parse_header()
        return self._buildDict()

    def _read_lines(self, filepath):
        self.data = []
        self.filepath = filepath
        with open(filepath) as fp:
            for line in fp:
                self.data += [line]

    def _parse_header(self):
        self.header = self.data[: self.n_headerlines]
        self.data = self.data[self.n_headerlines :]

    def _build_dict(self):
        lines = np.array([[float(i) for i in d.split()] for d in self.data])
        x = lines[:, 0]
        y = lines[:, 2]
        x, y = self._checkStepWidth(x, y)
        spect = {"data": {"x": list(x), "y": list(y)}}
        self.data_dict += [spect]
        return self.data_dict

    def _check_step_width(self, x, y):
        """Check to see if a non-uniform step width is used in the spectrum."""
        start = x[0]
        stop = x[-1]
        x1 = np.roll(x, -1)
        diff = np.abs(np.subtract(x, x1))
        step = round(np.min(diff[diff != 0]), 2)
        if step != 0.0 and (stop - start) / step > len(x):
            x, y = self._interpolate(x, y, step)
        return x, y

    def _interpolate(self, x, y, step):
        """Interpolate data points in case a non-uniform step width was used."""
        new_x = []
        new_y = []
        for i in range(len(x) - 1):
            diff = np.abs(np.around(x[i + 1] - x[i], 2))
            if (diff > step) & (diff < 10):
                for j in range(int(np.round(diff / step))):
                    new_x += [x[i] + j * step]
                    k = j / int(diff / step)
                    new_y += [y[i] * (1 - k) + y[i + 1] * k]
            else:
                new_x += [x[i]]
                new_y += [y[i]]

        new_x += [x[-1]]
        new_y += [y[-1]]
        x = new_x
        y = np.array(new_y)
        return x, y
