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

"""A generic reader for loading XPS (X-ray Photoelectron Spectroscopy) data
 file into nxdl (NeXus Definition Language) template.
"""
import os.path

from nexusutils.dataconverter.readers.base.reader import BaseReader
from typing import Tuple

from typing import Any, List
import xarray as xr
import numpy as np
import sys
from nexusutils.dataconverter.readers.xps_specs import XpsDataFileParser
import json

np.set_printoptions(threshold=sys.maxsize)


def find_entry_and_value(xps_data_dict,
                         data_dest, #TODO rewrite the data dest as data_loc
                         dest_type):

    entries_values = dict()

    if dest_type in ["@region_data", "@parameters_data"]:
        for key, val in xps_data_dict.items():
            if data_dest in key:
                components = key.split("/")
                entry = (components[1] + ":" +
                         components[2].split("_", 1)[1] + ":" +
                         components[4].split("_", 1)[1]
                         )
                entries_values = {entry: val}

    if dest_type=="@data":
        for key, val in xps_data_dict.items()():
            if data_dest in key:
                components = key.split("/")
                entry = (components[1] + ":" +
                         components[2].split("_", 1)[1] + ":" +
                         components[4].split("_", 1)[1]
                         )

                if entry not in entries_values.keys():
                    entries_values[entry] = xr.Dataset()

                # data_dest -> cycles/Cycle_
                _, last_part = key.split(data_dest)
                parts = last_part.split("/")
                cycle_num, scan_num = parts[0], parts[-2].split("_")[1]
                da_name = f"cycle{cycle_num}_scan{scan_num}"

                entries_values[entry][da_name] = val

                # TODO add x-coordinate if the the BE can be calculated later

    return entries_values


class XPS_Reader(BaseReader):

    supported_nxdls = ["NXmpes"]


    def read(self,
             template: dict = None,
             file_paths: List[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""

        # TODO: add the config file in example folder or intended folder
        # (if the is not eample folder) and add the path in con_file_path
        con_file_path = f'{os.path.dirname("__file__")}{os.path.sep}cofig_file.json'
        file_paths.append(con_file_path)
        config_dict = {}
        xps_data_dict = {}

        for file in file_paths:
            file_ext = file.rsplit(".", 1)[-1]
            if file_ext == "json":
                with open(file, encoding="utf-8", mode="r") as json_file:
                    config_dict = json.load(json_file)

            elif file_ext in ["yaml", "yml"]:
                #TODO: yet to develop
                pass

            else:
                Xps_paser_object = XpsDataFileParser(file_paths)
                data_dict = Xps_paser_object.get_dict()
                xps_data_dict = {**xps_data_dict, **data_dict}

        for key, value in config_dict.items():

            if "@region_data" in value:
                data_dest = value.split("region_data:")[-1]
                entries_values = find_entry_and_value(xps_data_dict,
                                                      data_dest,
                                                      dest_type=\
                                                      "@region_data")

                for entry, value in entries_values.items():
                    modified_key = key.replace("entry", entry)
                    template[modified_key] = value
                    try:
                        template[f"{modified_key}/@units"] = \
                            config_dict[f"{key}/@units"]

                        del template[f"{key}/@units"]
                    except KeyError:
                        pass

                try:
                    del template[key]
                except KeyError:
                    pass

            elif "@parameters_data" in value:
                data_dest = value.split("parameters_data:")[-1]
                entries_values = find_entry_and_value(xps_data_dict,
                                                      data_dest,
                                                      dest_type=\
                                                      "@parameters_data")

                for entry, value in entries_values.items():
                    modified_key = key.replace("entry", entry)
                    template[modified_key] = value
                    try:
                        template[f"{modified_key}/@units"] = \
                            config_dict[f"{key}/@units"]

                        del template[f"{key}/@units"]
                    except KeyError:
                        pass

                try:
                    del template[key]
                except KeyError:
                    pass

            elif "@invalid_value" in value:
                pass

            elif "@data" in value:
                data_dest = value.split("data:")[-1]
                entries_values = find_entry_and_value(xps_data_dict,
                                                      data_dest,
                                                      dest_type=\
                                                      "@data")

                for entry, value in entries_values.items():
                    modified_key = key.replace("entry", entry)
                    template[modified_key] = value
                    # signal takes the sum of the counts along the scan axis
                    template[f"{modified_key}/@signal"] = \
                        np.sum([value[x_arr] for x_arr in value.data_vars],
                               axis=0)
                    template[f"{modified_key}/@units"] = \
                        config_dict[f"{key}/@units"]
                try:
                    del template[f"{key}"]
                    del template[f"{key}/@signal"]
                    del template[f"{key}/@units"]
                except KeyError:
                    pass

        # if not template.items():
        #     # intended for NXroot
        #     for key, val in data_dict.items():
        #         if key[-1] == "/":
        #             key = key[:-1]
        #         if val not in ["None"]:
        #             template[key] = val
        #
        # elif template.items():
        #     # intended for NXtest
        #     for key, val in data_dict.items():
        #         if key[-1] == "/":
        #             key = key[:-1]
        #
        #         if val not in ["None"]:
        #             template[key] = val

        return template


READER = XPS_Reader