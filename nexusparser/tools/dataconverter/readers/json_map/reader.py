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
"""An example reader implementation for the DataConverter."""
import re
from typing import Tuple, Any
import numpy as np
import json
import pickle
import xarray

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader


def parse_slice(slice_string):
    slices = slice_string.split(",")
    for index, item in enumerate(slices):
        values = item.split(":")
        if len(values)<3:
            values.append("")
        slices[index] = slice(*tuple([int(x) if x != "" else None for x in values]))
        # :,3:4,:
        # (slice(None, None, None), slice(3, 4, None), slice(None, None, None))
    return np.index_exp[tuple(slices)]

class JsonMapReader(BaseReader):
    """A reader that takes a mapping json file and a data file/object to return a template."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXtest", "*"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """
        Reads data from given file and returns a filled template dictionary.

        Only the data object is expected to be passed as the first object.
        Alteratively, a data object represented with a file.json or file.xarray.pickle
        can also be used.
        The mapping is only accepted as file.mapping.json to the inputs.
        """
        data: dict = {}
        mapping: dict = {}

        if objects:
            data = objects[0]

        for file_path in file_paths:
            file_extension = file_path[file_path.rindex("."):]
            if file_extension == ".json":
                with open(file_path, "r") as input_file:
                    if ".mapping" in file_path:
                        mapping = json.loads(input_file.read())
                    else:
                        data = json.loads(input_file.read())
            elif file_extension == ".pickle":
                with open(file_path, "rb") as input_file:  # type: ignore[assignment]
                    data = pickle.load(input_file)  # type: ignore[arg-type]

        # TODO: Restructure the array received from Johannes.
        # restructured = [[data["data"][0][3], data["data"][0][4]], [data["data"][1][3], data["data"][1][4]], [data["data"][2][3], data["data"][2][4]], [data["data"][3][3], data["data"][3][4]]]

        # Convert shape slice strings to slice objects
        for key in mapping:
            if isinstance(mapping[key], dict):
                if "shape" in mapping[key]:
                    mapping[key]["shape"] = parse_slice(mapping[key]["shape"])

        def get_val_nested_keystring_from_dict(keystring, data):
            if isinstance(keystring, list) or isinstance(keystring, dict):
                return keystring

            # print(keystring, data)
            # if "/" not in keystring and isinstance(data, dict):
            #     return data[keystring]["value"]

            current_key = keystring.split("/")[0]
            if isinstance(data[current_key], dict):
                return get_val_nested_keystring_from_dict(keystring[keystring.find("/") + 1:],
                                                          data[current_key])
            if isinstance(data[current_key], xarray.DataArray):
                return data[current_key].values
            if isinstance(data[current_key], xarray.core.dataset.Dataset):
                raise Exception(f"Xarray datasets are not supported. "
                                f"You can only use xarray dataarrays.")

            return data[current_key]

        # template["/default_plot"] = mapping["/default_plot"]

        # if we have links dict, then we process them differently

        # print(get_val_nested_keystring_from_dict(mapping["/ENTRY[entry]/INSTRUMENT[instrument]/IVcurrent_source/model"], data))

        for req in ("required", "optional", "recommended"):
            for path in template[req]:
                try:
                    template[path] = get_val_nested_keystring_from_dict(mapping[path], data)
                    # TODO:
                    # !!!!! I CANT FIND THE PATH BELOW HERE !!!! IT GETS SAVED WRONG IN THE NEXUS FILE

                    del mapping[path]
                except KeyError:
                    if req != "required":
                        pass
                    else:
                        raise Exception(f"Required map for, {path},"
                                        f"doesn't exist in JSON map file.")

        print(data["metadata_start"]["device_config"]["keysight_e5270b"]["keysight_e5270b_idn"].values)
        print(template)
        for path, value in mapping.items():
            template[path] = value


        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = JsonMapReader
