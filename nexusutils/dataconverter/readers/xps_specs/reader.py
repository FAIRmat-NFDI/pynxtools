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

#np.set_printoptions(threshold=sys.maxsize)


def find_entry_and_value(xps_data_dict,
                         data_dest,#TODO rewrite the data dest as data_loc
                         dest_type):

    entries_values = dict()
    if dest_type in ["@region_data",
                     "@parameters_data",
                     "@analyzer_info",
                     "@source_info"]:

        for key, val in xps_data_dict.items():
            if data_dest in key:
                components = key.split("/")
                entry = (components[2] + "__" +
                         components[3].split("_", 1)[1] + "__" +
                         components[5].split("_", 1)[1]
                         )
                entries_values = {entry: val}

    elif dest_type == "@data":
        for key, val in xps_data_dict.items():
            if data_dest in key:
                components = key.split("/")
                entry = (components[2] + "__" +
                         components[3].split("_", 1)[1] + ":" +
                         components[5].split("_", 1)[1]
                         )

                if entry not in entries_values.keys():
                    entries_values[entry] = xr.Dataset()

                # data_dest -> cycles/Cycle_
                _, last_part = key.split(data_dest)
                if "/time" in last_part:
                    continue
                parts = last_part.split("/")
                cycle_num, scan_num = parts[0], parts[-2].split("_")[1]
                da_name = f"cycle{cycle_num}_scan{scan_num}"

                # data_array = (name, data, dimension,
                entries_values[entry][da_name] = ("counts", val)

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
        con_file_path = f'{os.path.dirname(__file__)}{os.path.sep}config_file.json'
        if isinstance(file_paths, list):
            file_paths.append(con_file_path)
        elif isinstance(file_paths, tuple):
            file_paths = (*file_paths, con_file_path)
        else:
            file_paths = [file_paths]
            file_paths.append(con_file_path)

        config_dict = {}
        xps_data_dict = {}
        entry_set = set()
        searching_keys = ["@analyzer_info",
                          "@region_data",
                          "@parameters_data",
                          "@source_info"]

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

            if "@data" in value:
                data_dest = value.split("data:")[-1]
                entries_values = find_entry_and_value(xps_data_dict,
                                                      data_dest,
                                                      dest_type= \
                                                      "@data")

                counts_length = 0
                for entry, ent_value in entries_values.items():
                    entry_set.add(entry)
                    modified_key = key.replace("entry", entry)
                    modified_key_ = modified_key

                    # filling out the scan data separately
                    BE_x_axis = "BE"
                    data_y_axis = "data"
                    axes = [BE_x_axis, data_y_axis]
                    for data_var in ent_value.data_vars:
                        modified_key_scan = modified_key_.replace(
                            "/data",
                            f"/{data_var}")

                        counts_arr = np.array(ent_value[data_var])
                        template[modified_key_scan] = counts_arr

                        counts_length = np.shape(counts_arr)[-1]

                        template[f"{modified_key_scan}/@units"] = \
                            config_dict[f"{key}/@units"]

                    # signal takes the sum of the counts along the scan axis
                    key_signal = modified_key_.replace("/data", "/@signal")
                    key_axes = modified_key_.replace("/data", "/@axes")
                    key_BE_x_axis = modified_key_.replace("/data",
                                                          f"/{BE_x_axis}")
                    template[key_signal] = "data"
                    template[modified_key] = \
                        np.sum([ent_value[x_arr] for x_arr in ent_value.data_vars],
                               axis=0)
                    template[key_axes] = axes
                    template[key_BE_x_axis] = np.arange(counts_length)

                    template[f"{modified_key}/@units"] = \
                        config_dict[f"{key}/@units"]

                try:
                    del template[key]
                except KeyError:
                    pass

                try:
                    key_signal = key
                    key_signal = key_signal.replace("/data", "/@signal")
                    del template[key_signal]
                except KeyError:
                    pass

                try:
                    del template[f"{key}/@units"]
                except KeyError:
                    pass

            else:
                for search_key in searching_keys:
                    if search_key in value:
                        data_dest = value.split(f"{search_key}:")[-1]
                        entries_values = find_entry_and_value(xps_data_dict,
                                                              data_dest,
                                                              dest_type= \
                                                              search_key)
                        for entry, ent_value in entries_values.items():
                            entry_set.add(entry)
                            modified_key = key.replace("[entry]", f"[{entry}]")

                            template[modified_key] = ent_value
                            try:
                                template[f"{modified_key}/@units"] = \
                                    config_dict[f"{key}/@units"]
                            except KeyError:
                                pass

                        try:
                            del template[key]
                        except KeyError:
                            pass
                        try:
                            del template[f"{key}/@units"]
                        except KeyError:
                            pass

        # Fill template by pre-defined value
        for key, value in config_dict.items():

            if "example_value" in value:
                field_value = value.split("example_value:")[-1]
                for entry in entry_set:
                    modified_key = key.replace("[entry]", f"[{entry}]")

                    try:
                        field_value_ = float(field_value)
                    except ValueError:
                        if isinstance(field_value, list):
                            field_value_ = np.array(field_value)
                        else:
                            field_value_ = field_value

                    template[modified_key] = field_value_

                try:
                    del template[key]
                except KeyError:
                    pass

            elif "entry_name" in value:
                for entry in entry_set:
                    modified_key = key.replace("[entry]",
                                               f"[{entry}]")
                    template[modified_key] = entry
                template[key] = value
                try:
                    del template[key]

                except KeyError:
                    pass
        return template


READER = XPS_Reader