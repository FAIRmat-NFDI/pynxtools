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

"""
Class for reading XPS files from TXT export of Scienta.
"""

from datetime import datetime
import pytz
import numpy as np


class ScientaTxtParser():
    """ Parser for Scienta TXT exports."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.lines: list = []
        self.spectra: list = []
        self.no_of_regions = 0

        keys_map = {
            'Number of Regions': 'no_of_regions',
            'Version': 'software_version',
            'Lens Mode': 'lens_mode',
            'Pass Energy': 'pass_energy',
            'Number of Sweeps': 'no_of_scans',
            'Excitation Energy': 'excitation_energy',
            'Energy Scale': 'energy_scale',
            'Acquisition Mode': 'acquisition_mode',
            'Energy Unit': 'x_units',
            'Center Energy': 'center_energy',
            'Low Energy': 'start_energy',
            'High Energy': 'stop_energy',
            'Energy Step': 'step_size',
            'Step Time': 'dwell_time',
            'Number of Slices': 'number_of_slices',
            'File': 'data_file',
            'Sequence': 'sequence_file',
            'Spectrum Name': 'spectrum_type',
            'Instrument': 'instrument_name',
            'Location': 'vendor',
            'User': 'user_initials',
            'Sample': 'sample_name',
            'Comments': 'spectrum_comment',
            'Date': 'start_date',
            'Time': 'start_time',
            'Time per Spectrum Channel': 'time_per_spectrum_channel',
            'DetectorMode': 'detector_mode',
        }

        self.region_keys_map = {
            'Region Name': 'region_name',
            'name': 'energy_type',
            'size': 'energy_size',
            'scale': 'energy_axis',
        }

        detector_map = {
            'Detector First X-Channel': 'detector_first_x_channel',
            'Detector Last X-Channel': 'detector_last_x_channel',
            'Detector First Y-Channel': 'detector_first_y_channel',
            'Detector Last Y-Channel': 'detector_last_y_channel',
        }

        lens_mode_map = {
            'Transmission': 'fixed analyzer transmission'
        }

        self.key_maps = [
            keys_map,
            self.region_keys_map,
            detector_map,
            lens_mode_map,
        ]

        self.value_map = {
            'no_of_regions': self._change_no_of_regions,
            'x_units': self._change_energy_type,
            'energy_axis': [self._separate_dimension_scale, np.array],
            'energy_scale': self._change_energy_type,
            'acquisition_mode': self._change_scan_mode,
        }

    def parse_file(self, file):
        """
        Parse the file's data and metadata into a flat
        list of dictionaries.


        Parameters
        ----------
        file : str
            Filepath of the TXT file to be read.

        Returns
        -------
        self.spectra
            Flat list of dictionaries containing one spectrum each.

        """
        self._read_lines(file)
        self._parse_header()

        for region_id in range(1, self.no_of_regions + 1):
            self._parse_region(region_id)

        return self.spectra

    def _read_lines(self, filepath):
        """
        Read all lines from the input txt files.


        Parameters
        ----------
        filepath : str
            Filepath of the TXT file to be read.

        Returns
        -------
        None.

        """
        with open(filepath, encoding="utf-8") as file:
            for line in file:
                self.lines += [line]

    def _parse_header(self):
        """
        Parse header with information about the software version
        and the number of spectra in the file.

        Returns
        -------
        None.

        """
        n_headerlines = 4
        header = self.lines[:n_headerlines]
        self.lines = self.lines[n_headerlines:]

        for line in header:
            key, value = self._get_key_value_pair(line)
            if key:
                value = self._re_map_values(key, value)
                setattr(self, key, value)

    def _parse_region(self, region_id):
        """
        Parse data from one region (i.e., one measured spectrum)
        into a dictioanry and append to all spectra.

        Parameters
        ----------
        region_id : int
            Number of the region in the file.

        Returns
        -------
        None.

        """

        region_data = {
            'region_id': region_id,
            'data': {
                'x': [],
                'y': []
            },
        }

        begin_region = False
        begin_info = False
        begin_data = False

        for line in self.lines:
            if line.startswith(f'[Region {region_id}'):
                begin_region = True
            if line.startswith(f'[Info {region_id}'):
                begin_info = True
            if line.startswith(f'[Data {region_id}'):
                begin_data = True
                continue

            if line.startswith("\n"):
                begin_region = False
                begin_info = False
                begin_data = False

            if begin_region:
                # Read region meta data.
                key, value = self._get_key_value_pair(line)
                if 'Dimension' in key:
                    key = self._re_map_keys(key)
                    key = self.region_keys_map[key.rsplit(' ')[-1]]
                    key = key.rsplit(' ')[-1]
                    value = self._re_map_values(key, value)
                    if self._check_valid_value(value):
                        region_data[key] = value

            if begin_info:
                # Read instrument meta data for this region.
                key, value = self._get_key_value_pair(line)
                if self._check_valid_value(value):
                    region_data[key] = value

            if begin_data:
                # Read XY data for this region.
                [energy, intensity] = \
                    [float(s) for s in line.split(' ') if s != '']

                region_data['data']['x'].append(energy)
                region_data['data']['y'].append(intensity)

        region_data['data']['x'] = np.array(region_data['data']['x'])
        region_data['data']['y'] = np.array(region_data['data']['y'])

        # Convert date and time to ISO8601 date time.
        start_date = region_data['start_date']
        start_time = region_data['start_time']
        region_data['time_stamp'] = self._construct_date_time(
            start_date,
            start_time)

        self.spectra.append(region_data)

    def _check_valid_value(self, value):
        """
        Check if a string or an array is empty.

        Parameters
        ----------
        value : obj
            For testing, this can be a str or a np.ndarray.

        Returns
        -------
        bool
            True if the string or np.ndarray is not empty.

        """
        if isinstance(value, str) and value:
            return True
        if isinstance(value, np.ndarray) and value.size != 0:
            return True
        return False

    def _get_key_value_pair(self, line):
        """
        Split the line at the '=' sign and return a
        key-value pair. The values are mapped according
        to the desired format.

        Parameters
        ----------
        line : str
            One line from the input file.

        Returns
        -------
        key : str
            Anything before the '=' sign, mapped to the desired
            key format.
        value : obj
            Anything after the '=' sign, mapped to the desired
            value format and type.

        """
        try:
            [key, value] = line.split('=')
            key = self._re_map_keys(key)
            value = self._re_map_values(key, value)
            return key, value

        except ValueError:
            key, value = '', ''
            return key, value

    def _re_map_keys(self, key):
        """
        Map the keys returned from the file to the preferred keys for
        the parser output.

        """
        maps = {}
        for key_map in self.key_maps:
            maps.update(key_map)

        keys = list(maps.keys())

        if key in keys:
            key = maps[key]

        return key

    def _change_no_of_regions(self, no_of_regions):
        """
        Make no_of_regions an integer.
        Maps e.g. from '0001' string to 1.

        Parameters
        ----------
        no_of_regions : str
            No. of regions in the data file,
            read from the first line.

        Returns
        -------
        int
            Ineger value of the number of regions.

        """
        return int(no_of_regions)

    def _change_energy_type(self, energy):
        """
        Change the strings for energy type to the preferred format.

        """
        if 'Binding' in energy:
            return 'binding energy'
        if 'Kinetic' in energy:
            return 'kinetic energy'
        return None

    def _separate_dimension_scale(self, scale):
        return [float(s) for s in scale.split(' ')]

    def _change_scan_mode(self, acquisition_mode):
        """
        Change the strings for acquisition mode type to
        the allowed values in NXmpes.

        """
        if acquisition_mode == 'Fixed':
            return 'fixed'
        if acquisition_mode == 'Swept':
            return 'sweep'
        return None

    def _construct_date_time(self, date, time):
        """
        Convert the native time format to the datetime string
        in the ISO 8601 format: '%Y-%b-%dT%H:%M:%S.%fZ'.

        """
        date_time = datetime.combine(
            datetime.strptime(date, "%Y-%m-%d"),
            datetime.strptime(time, '%H:%M:%S').time())

        localtz = pytz.timezone('Europe/Berlin')
        date_time = localtz.localize(date_time)

        return date_time.isoformat()

    def _re_map_values(self, input_key, value):
        """
        Map the values returned from the file to the preferred format for
        the parser output.

        """
        try:
            value = value.rstrip('\n')
        except AttributeError:
            pass

        keys = list(self.value_map.keys())

        for k in keys:
            if k in input_key:
                if not isinstance(self.value_map[k], list):
                    map_methods = [self.value_map[k]]
                else:
                    map_methods = self.value_map[k]
                for method in map_methods:
                    value = method(value)
        return value
