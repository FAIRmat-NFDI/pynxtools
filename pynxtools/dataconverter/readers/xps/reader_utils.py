"""
Helper functions for populating NXmpes template
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
from abc import ABC, abstractmethod
from scipy.interpolate import interp1d
import numpy as np


class XPSMapper(ABC):
    """Abstract base class from mapping from a parser to NXmpes template"""

    def __init__(self):
        self.file = None
        self.raw_data: list = []
        self._xps_dict: dict = {}
        self._root_path = "/ENTRY[entry]"

        self.parser = None

    @abstractmethod
    def _select_parser(self):
        """
        Select the correct parser for the file extension and format.

        Should be implemented by the inheriting mapper.

        Returns
        -------
        Parser

        """

    @property
    def data_dict(self) -> dict:
        """Getter property."""
        return self._xps_dict

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the Scienta TXT parser.

        """
        self.file = file
        self.parser = self._select_parser()
        self.raw_data = self.parser.parse_file(file, **kwargs)

        file_key = f"{self._root_path}/File"
        self._xps_dict[file_key] = file

        self.construct_data()

        return self.data_dict

    @abstractmethod
    def construct_data(self):
        """
        Map from individual parser format to NXmpes-ready dict.

        Should be implemented by the inheriting mapper.

        """


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


def check_uniform_step_width(lst):
    """
    Check to see if a non-uniform step width is used in an lst

    Parameters
    ----------
    lst : list
        List of data points.

    Returns
    -------
    bool
        False if list is non-uniformally spaced.

    """
    start = lst[0]
    stop = lst[-1]
    step = get_minimal_step(lst)

    if step != 0.0 and np.abs((stop - start) / step) > len(lst):
        return False
    return True


def get_minimal_step(lst):
    """
    Return the minimal difference between two consecutive values
    in a list. Used for extracting minimal difference in a
    list with non-uniform spacing.

    Parameters
    ----------
    lst : list
        List of data points.

    Returns
    -------
    step : float
        Non-zero, minimal distance between consecutive data
        points in lst.

    """
    lst1 = np.roll(lst, -1)
    diff = np.abs(np.subtract(lst, lst1))
    step = round(np.min(diff[diff != 0]), 2)

    return step


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
    list
        Interpolated y array.

    """
    # pylint: disable=invalid-name
    interp_fn = interp1d(x0, y, axis=0, fill_value="extrapolate")
    return interp_fn(x1)


def interpolate_arrays(x, array_list):
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
    # pylint: disable=invalid-name
    if not isinstance(array_list, list):
        array_list = [array_list]
    start = x[0]
    stop = x[-1]
    step = get_minimal_step(x)
    if start > stop:
        # pylint: disable=arguments-out-of-order
        new_x = np.flip(safe_arange_with_edges(stop, start, step))
    else:
        new_x = safe_arange_with_edges(start, stop, step)

    output_list = [_resample_array(arr, x, new_x) for arr in array_list]

    return new_x, output_list


def construct_data_key(spectrum):
    """
    Construct a key for the 'data' field of the xps_dict.
    Output example: cycle0_scan0.

    """
    if "loop_no" in spectrum:
        cycle_key = f'cycle{spectrum["loop_no"]}'
    else:
        cycle_key = "cycle0"

    if "scan_no" in spectrum:
        scan_key = f'scan{spectrum["scan_no"]}'
    else:
        scan_key = "scan0"

    return f"{cycle_key}_{scan_key}"


def construct_detector_data_key(spectrum):
    """
    Construct a key for the detector data fields of the xps_dict.
    Output example: 'cycles/Cycle_0/scans/Scan_0'

    """
    if "loop_no" in spectrum:
        cycle_key = f'cycles/Cycle_{spectrum["loop_no"]}'
    else:
        cycle_key = "cycles/Cycle_0"

    if "scan_no" in spectrum:
        scan_key = f'scans/Scan_{spectrum["scan_no"]}'
    else:
        scan_key = "scans/Scan_0"

    key = f"{cycle_key}/{scan_key}"

    if "channel_no" in spectrum:
        key += f'/channels/Channel_{spectrum["channel_no"]}'

    return key


def construct_entry_name(key):
    """Construction entry name."""
    key_parts = key.split("/")
    try:
        # entry example : sample__name_of_scan_region
        entry_name = (
            f'{key_parts[2].split("_", 1)[1]}' f"__" f'{key_parts[4].split("_", 1)[1]}'
        )
    except IndexError:
        entry_name = ""
    return entry_name
