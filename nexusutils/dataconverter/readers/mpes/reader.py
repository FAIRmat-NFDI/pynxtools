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
import errno
import json
import os
from functools import reduce
from typing import Any
from typing import Tuple

import h5py
import xarray as xr
import yaml

from nexusutils.dataconverter.readers.base.reader import BaseReader
from nexusutils.dataconverter.readers.utils import flatten_and_replace, FlattenSettings

DEFAULT_UNITS = {
    "X": "step",
    "Y": "step",
    "t": "step",
    "tofVoltage": "V",
    "extractorVoltage": "V",
    "extractorCurrent": "A",
    "cryoTemperature": "K",
    "sampleTemperature": "K",
    "dldTimeBinSize": "ns",
    "delay": "ps",
    "timeStamp": "s",
    "energy": "eV",
    "kx": "1/A",
    "ky": "1/A",
}


def res_to_xarray(res, bin_names, bin_axes, metadata=None):
    """creates a BinnedArray (xarray subclass) out of the given np.array
    Parameters:
        res: np.array
            nd array of binned data
        bin_names (list): list of names of the binned axes
        bin_axes (list): list of np.arrays with the values of the axes
    Returns:
        ba: BinnedArray (xarray)
            an xarray-like container with binned data, axis, and all
            available metadata
    """
    dims = bin_names
    coords = {}
    for name, vals in zip(bin_names, bin_axes):
        coords[name] = vals

    xres = xr.DataArray(res, dims=dims, coords=coords)

    for name in bin_names:
        try:
            xres[name].attrs["unit"] = DEFAULT_UNITS[name]
        except KeyError:
            pass

    xres.attrs["units"] = "counts"
    xres.attrs["long_name"] = "photoelectron counts"

    if metadata is not None:
        xres.attrs["metadata"] = metadata

    return xres


def h5_to_xarray(faddr, mode="r"):
    """Rear xarray data from formatted hdf5 file
    Args:
        faddr (str): complete file name (including path)
        mode (str): hdf5 read/write mode
    Returns:
        xarray (xarray.DataArray): output xarra data
    """
    with h5py.File(faddr, mode) as h5_file:
        # Reading data array
        try:
            data = h5_file["binned"]["BinnedData"]
        except KeyError:
            print("Wrong Data Format, data not found")
            raise

        # Reading the axes
        axes = []
        bin_names = []

        try:
            for axis in h5_file["axes"]:
                axes.append(h5_file["axes"][axis])
                bin_names.append(h5_file["axes"][axis].attrs["name"])
        except KeyError:
            print("Wrong Data Format, axes not found")
            raise

        # load metadata
        if "metadata" in h5_file:

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

            metadata = recursive_parse_metadata(h5_file["metadata"])
        # Segment to change Vset to V in lens voltages
        if "file" in metadata.keys():
            for k in list(metadata['file']):
                if "VSet" in k:
                    key = k[:-3]
                    metadata['file'][key] = metadata['file'][k]
                    del metadata['file'][k]

        xarray = res_to_xarray(data, bin_names, axes, metadata)
        return xarray


def iterate_dictionary(dic, key_string):
    """Recursively iterate in dictionary and give back its values"""
    keys = key_string.split("/", 1)
    if keys[0] in dic:
        if len(keys) == 1:
            return dic[keys[0]]
        if not len(keys) == 1:
            return iterate_dictionary(dic[keys[0]], keys[1])
    else:
        raise KeyError
    return None


CONVERT_DICT = {
    'Instrument': 'INSTRUMENT[instrument]',
    'Analyzer': 'ELECTRONANALYSER[electronanalyser]',
    'Manipulator': 'MANIPULATOR[manipulator]',
    'Beam': 'BEAM[beam]',
    'unit': '@units',
    'Sample': 'SAMPLE[sample]',
    'Source': 'SOURCE[source]',
    'User': 'USER[user]'
}

REPLACE_NESTED = {
    'SOURCE[source]/Probe': 'SOURCE[source]',
    'SOURCE[source]/Pump': 'SOURCE[source_pump]',
    'BEAM[beam]/Probe': 'BEAM[beam]',
    'BEAM[beam]/Pump': 'BEAM[beam_pump]',
    'sample_history': 'sample_history/description'
}


def handle_h5_and_json_file(file_paths, objects):
    """Handle h5 or json input files."""
    x_array_loaded = xr.DataArray()
    config_file_dict = {}
    eln_data_dict = {}

    for file_path in file_paths:
        try:
            file_extension = file_path[file_path.rindex("."):]
        except ValueError as exc:
            raise ValueError(
                f"The file path {file_path} must have an extension.",
            ) from exc

        extentions = [".h5", ".json", ".yaml", ".yml"]
        if file_extension not in extentions:
            print(
                f"WARNING \n"
                f"The reader only supports files of type {extentions}, "
                f"but {file_path} does not match.",
            )

        if not os.path.exists(file_path):
            file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "tests",
                "data",
                "dataconverter",
                "readers",
                "mpes",
                file_path,
            )
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                file_path,
            )

        if file_extension == ".h5":
            x_array_loaded = h5_to_xarray(file_path)
        elif file_extension == ".json":
            with open(file_path, encoding="utf-8") as file:
                config_file_dict = json.load(file)
        elif file_extension in [".yaml", ".yml"]:
            with open(file_path, encoding="utf-8") as feln:
                eln_data_dict = flatten_and_replace(
                    FlattenSettings(
                        dic=yaml.safe_load(feln),
                        convert_dict=CONVERT_DICT,
                        replace_nested=REPLACE_NESTED
                    )
                )

    if objects is not None:
        # For the case of a single object
        assert isinstance(
            objects,
            xr.core.dataarray.DataArray,
        ), "The given object must be an xarray"
        x_array_loaded = objects

    return x_array_loaded, config_file_dict, eln_data_dict


def rgetattr(obj, attr):
    """Get attributes recursively"""
    def _getattr(obj, attr):
        return getattr(obj, attr)

    if "index" in attr:
        axis = attr.split(".")[0]
        return str(obj.dims.index(f"{axis}"))

    return reduce(_getattr, [obj] + attr.split("."))


class MPESReader(BaseReader):
    """MPES-specific reader class"""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXmpes"]

    def read(
            self,
            template: dict = None,
            file_paths: Tuple[str] = None,
            objects: Tuple[Any] = None,
    ) -> dict:
        """Reads data from given file or alternatively an xarray object
        and returns a filled template dictionary"""

        if not file_paths:
            raise Exception("No input files were given to MPES Reader.")

        (
            x_array_loaded,
            config_file_dict,
            eln_data_dict,
        ) = handle_h5_and_json_file(file_paths, objects)

        for key, value in config_file_dict.items():

            if isinstance(value, str) and ":" in value:
                precursor = value.split(":")[0]
                value = value[value.index(":") + 1:]

                # Filling in the data and axes along with units from xarray
                if precursor == "@data":
                    try:
                        template[key] = rgetattr(
                            obj=x_array_loaded,
                            attr=value,
                        )
                        if key.split("/")[-1] == "@axes":
                            template[key] = list(template[key])

                    except ValueError:
                        print(
                            f"Incorrect axis name corresponding to "
                            f"the path {key}",
                        )

                    except AttributeError:
                        print(
                            f"Incorrect naming syntax or the xarray doesn't "
                            f"contain entry corresponding to the path {key}",
                        )

                # Filling in the metadata from xarray
                elif precursor == "@attrs":
                    if key not in eln_data_dict:
                        try:  # Tries to fill the metadata
                            template[key] = iterate_dictionary(
                                x_array_loaded.attrs,
                                value,
                            )

                        except KeyError:
                            print(
                                f"[info]: Path {key} not found. "
                                f"Skipping the entry.",
                            )

            else:
                # Fills in the fixed metadata
                template[key] = value

        # Filling in ELN metadata and overwriting the common paths by
        # giving preference to the ELN metadata
        for key, value in eln_data_dict.items():
            template[key] = value

        return template


READER = MPESReader
