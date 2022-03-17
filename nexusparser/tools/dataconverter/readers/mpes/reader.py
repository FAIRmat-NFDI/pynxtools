#
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

"""MPES reader implementation for the DataConverter."""

from typing import Tuple
import json
import h5py
import xarray as xr
from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

DEFAULT_UNITS = {
    'X': 'step',
    'Y': 'step',
    't': 'step',
    'tofVoltage': 'V',
    'extractorVoltage': 'V',
    'extractorCurrent': 'A',
    'cryoTemperature': 'K',
    'sampleTemperature': 'K',
    'dldTimeBinSize': 'ns',
    'delay': 'ps',
    'timeStamp': 's',
    'E': 'eV',
    'kx': '1/A',
    'ky': '1/A'}


def res_to_xarray(res, bin_names, bin_axes, metadata=None):
    """ creates a BinnedArray (xarray subclass) out of the given np.array
    Parameters:
        res: np.array
            nd array of binned data
        bin_names (list): list of names of the binned axes
        bin_axes (list): list of np.arrays with the values of the axes
    Returns:
        ba: BinnedArray (xarray)
            an xarray-like container with binned data, axis, and all available metadata
    """
    dims = bin_names
    coords = {}
    for name, vals in zip(bin_names, bin_axes):
        coords[name] = vals

    xres = xr.DataArray(res, dims=dims, coords=coords)

    for name in bin_names:
        try:
            xres[name].attrs['unit'] = DEFAULT_UNITS[name]
        except KeyError:
            pass

    xres.attrs['units'] = 'counts'
    xres.attrs['long_name'] = 'photoelectron counts'

    if metadata is not None:
        xres.attrs['metadata'] = metadata

    return xres


def h5_to_xarray(faddr, mode='r'):
    """ Rear xarray data from formatted hdf5 file
    Args:
        faddr (str): complete file name (including path)
        mode (str): hdf5 read/write mode
    Returns:
        xarray (xarray.DataArray): output xarra data
    """
    with h5py.File(faddr, mode) as h5_file:
        # Reading data array
        try:
            data = h5_file['binned']['BinnedData']
        except KeyError:
            print("Wrong Data Format, data not found")
            raise

        # Reading the axes
        axes = []
        bin_names = []

        try:
            for axis in h5_file['axes']:
                axes.append(h5_file['axes'][axis])
                bin_names.append(h5_file['axes'][axis].attrs['name'])
        except KeyError:
            print("Wrong Data Format, axes not found")
            raise

        # load metadata
        if 'metadata' in h5_file:
            def recursive_parse_metadata(node):
                if isinstance(node, h5py.Group):
                    dictionary = {}
                    for key, value in node.items():
                        dictionary[key] = recursive_parse_metadata(value)

                else:
                    dictionary = node[...]
                    try:
                        dictionary = dictionary.item()
                        if isinstance(dictionary, (bytes, bytearray)):
                            dictionary = dictionary.decode()
                    except ValueError:
                        pass

                return dictionary

            metadata = recursive_parse_metadata(h5_file['metadata'])

        xarray = res_to_xarray(data, bin_names, axes, metadata)
        return xarray


def iterate_dictionary(dic, key_string):
    """Recursively iterate in dictionary and give back its values

"""
    keys = key_string.split('/', 1)
    if keys[0] in dic:
        if len(keys) == 1:
            return dic[keys[0]]
        if not len(keys) == 1:
            return iterate_dictionary(dic[keys[0]], keys[1])
    else:
        raise KeyError
    return None


def handle_h5_and_json_file(file_paths):
    """Handle h5 or json input files.

"""
    for file_path in file_paths:
        file_extension = file_path[file_path.rindex("."):]
        if file_extension == '.h5':
            x_array_loaded = h5_to_xarray(file_path)
        elif file_extension == '.json':
            with open(file_path, 'r') as file:
                config_file_dict = json.load(file)
    return x_array_loaded, config_file_dict


class MPESReader(BaseReader):
    """MPES-specific reader class

"""
    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXmpes"]

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""

        if not file_paths:
            raise Exception("No input files were given to MPES Reader.")

        x_array_loaded, config_file_dict = handle_h5_and_json_file(file_paths)

        for key, value in config_file_dict.items():

            if isinstance(value, str) and ':' in value:
                precursor = value.split(':')[0]
                value = value[value.index(':') + 1:]

                # Filling in the data and axes along with units from xarray
                if precursor == '@data':
                    try:
                        template[key] = eval("x_array_loaded." + value)  # pylint:disable=eval-used

                        if key.split('/')[-1] == '@axes':
                            template[key] = list(template[key])

                    except NameError:
                        print(f"Incorrect naming syntax or the xarray"
                              f"doesn't contain entry corresponding to the path {key}")
                    except KeyError:
                        print(f"The xarray doesn't contain entry corresponding to the path {key}")

                # Filling in the metadata from xarray
                elif precursor == '@attrs':

                    try:  # Tries to fill the metadata
                        template[key] = iterate_dictionary(x_array_loaded.attrs, value)

                    except KeyError:
                        print(f"The xarray doesn't contain entry corresponding to the path {key}")

            else:
                # Fills in the fixed metadata
                template[key] = value

        return template


READER = MPESReader
