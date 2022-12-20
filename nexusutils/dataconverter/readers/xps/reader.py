"""A generic reader for loading XPS (X-ray Photoelectron Spectroscopy) data
 file into mpes nxdl (NeXus Definition Language) template.
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
import os
from pathlib import Path
from typing import Any, Dict, Set
from typing import Tuple
import sys
import json
import copy

import xarray as xr
import yaml
import numpy as np

from nexusutils.dataconverter.readers.base.reader import BaseReader
from nexusutils.dataconverter.readers.xps.reader_utils import XpsDataFileParser
from nexusutils.dataconverter.readers.utils import flatten_and_replace, FlattenSettings

np.set_printoptions(threshold=sys.maxsize)

CONVERT_DICT = {
    'Instrument': 'INSTRUMENT[instrument]',
    'Analyser': 'ELECTRONANALYSER[electronanalyser]',
    'Beam': 'BEAM[beam]',
    'unit': '@units',
    'Sample': 'SAMPLE[sample]',
    'User': 'USER[user]',
    'Data': 'DATA[data]',
    'Source': 'SOURCE[source]',
    'Collectioncolumn': 'COLLECTIONCOLUMN[collectioncolumn]',
    'Energydispersion': 'ENERGYDISPERSION[cnergydispersion]'
}

REPLACE_NESTED: Dict[str, str] = {}


# This function must be same as that in reader_utils.py
def construct_entry_name(key):
        """TODO: add Docstring"""
        components = key.split("/")
        try:
            # entry: vendor__sample__name_of_scan_rerion
            entry_name = (f'{components[2]}'
                          f'__'
                          f'{components[3].split("_", 1)[1]}'
                          f'__'
                          f'{components[5].split("_", 1)[1]}'
                          )
        except IndexError:
            entry_name = ""
        return entry_name


def find_entry_and_value(xps_data_dict,
                         key_part,
                         dt_typ):
    """Construct the entry name and pick up the corresponding data for
        that for that entry.
    """

    entries_values = {}
    if dt_typ in ["@region_data",
                  "@parameters_data",
                  "@analyzer_info",
                  "@source_info"]:

        for key, val in xps_data_dict.items():
            if key_part in key:
                entry = construct_entry_name(key)
                entries_values[entry] = val

    elif dt_typ == "@data":
        # entries_values = entry:{cycle0_scan0_chan0:xr.data}
        entries_values = xps_data_dict["data"]

    return entries_values


def fill_data_class(key,
                            value,
                            config_dict,
                            xps_data_dict,
                            template,
                            entry_set):

    key_part = value.split("data:")[-1]
    dt_typ = "@data"
    entries_values = find_entry_and_value(xps_data_dict,
                                          key_part, dt_typ)

    survey_count_ = 0
    count = 0

    for entry, xr_data in entries_values.items():
        entry_set.add(entry)
        modified_key = key.replace("entry", entry)
        root = key[0]
        modifid_entry = key[0:13]
        modifid_entry = modifid_entry.replace("entry", entry)
        template[f"{modifid_entry}/@default"] = "data"

        # Set first Survey as default for .nxs file
        if "Survey" in entry and survey_count_ == 0:
            survey_count_ = survey_count_ + 1
            template[f"{root}@default"] = entry

        # If no Survey set any scan for default
        if survey_count_ == 0 and count == 0:
            count = count + 1
            template[f"{root}@default"] = entry

        binding_energy_coord = None
        for data_var in xr_data.data_vars:
            scan = data_var
            key_indv_scn_dt = modified_key.replace("[data]/data",
                                                   f"[data]/{scan}")
            key_indv_scn_dt_unit = modified_key.replace("[data]/data",
                                                        f"[data]/{scan}/@units")

            cord_nm = list(xr_data[data_var].coords)[0]
            binding_energy_coord = np.array(xr_data[data_var][cord_nm])
            template[key_indv_scn_dt] = \
                np.array(xr_data[data_var].data)
            template[key_indv_scn_dt_unit] = \
                config_dict[f"{key}/@units"]

        key_data = modified_key.replace("[data]/data", "[data]/data")
        key_data_unit = f"{key_data}/@units"

        key_signal = modified_key.replace("[data]/data",
                                        "[data]/@signal")
        BE_nm = "BE"
        key_BE = modified_key.replace("[data]/data", f"[data]/{BE_nm}")
        key_BE_unit = f"{key_BE}/@units"
        key_BE_axes = modified_key.replace("[data]/data", "[data]/@axes")
        key_BE_ind = modified_key.replace("[data]/data",
                                          f"[data]/@{BE_nm}_indices")

        key_nxclass = modified_key.replace("[data]/data",
                                           "[data]/@NX_class")

        template[key_signal] = "data"
        template[key_data] = np.mean([xr_data[x_arr].data
                                     for x_arr in xr_data.data_vars
                                     if "_chan" not in x_arr],
                                     axis=0)

        template[f"{key_data}_errors"] = \
            np.std([xr_data[x_arr].data
                    for x_arr in xr_data.data_vars
                    if "_chan" not in x_arr], axis=0)
        template[key_data_unit] = config_dict[f"{key}/@units"]
        template[key_BE_unit] = "eV"
        template[key_BE] = binding_energy_coord
        template[key_BE_axes] = BE_nm
        template[key_BE_ind] = 0
        template[key_nxclass] = "NXdata"


def fill_template_with_xps_data(config_dict,
                                xps_data_dict,
                                template,
                                searching_keys,
                                entry_set):
    """Collect the xps data from xps_data_dict
        and store them into template. We use searching_keys
        for separating the data from xps_data_dict.
    """

    for key, value in config_dict.items():
        print("## Before : ", entry_set)
        if "@data" in value:
            fill_data_class(key, value, config_dict,
                                    xps_data_dict, template, entry_set)
            print("#### After : ", entry_set)
        else:
            for search_key in searching_keys:
                if search_key in value:
                    key_part = value.split(f"{search_key}:")[-1]
                    entries_values = find_entry_and_value(xps_data_dict,
                                                          key_part,
                                                          dt_typ=search_key)
                    for entry, ent_value in entries_values.items():
                        entry_set.add(entry)
                        modified_key = key.replace("[entry]", f"[{entry}]")

                        template[modified_key] = ent_value
                        try:
                            template[f"{modified_key}/@units"] = \
                                config_dict[f"{key}/@units"]
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


# pylint: disable=too-few-public-methods
class XPSReader(BaseReader):
    """ Reader for XPS.
    """

    supported_nxdls = ["NXmpes"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Reads data from given file and returns
        a filled template dictionary"""

        reader_dir = Path(__file__).parent
        config_file = reader_dir.joinpath("config_file.json")

        xps_data_dict: Dict[str, Any] = {}
        eln_data_dict: Dict[str, Any] = {}
        entry_set: Set[str] = set()
        searching_keys = ["@analyzer_info",
                          "@region_data",
                          "@parameters_data",
                          "@source_info"]

        for file in file_paths:
            file_ext = os.path.splitext(file)[1]

            if file_ext in [".yaml", ".yml"]:
                with open(file, mode="r", encoding="utf-8") as eln:
                    eln_data_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(eln),
                            CONVERT_DICT,
                            REPLACE_NESTED
                        )
                    )

            elif file_ext == ".xml":
                data_dict = XpsDataFileParser([file]).get_dict()
                xps_data_dict = {**xps_data_dict, **data_dict}

        with open(config_file, encoding="utf-8", mode="r") as cfile:
            config_dict = json.load(cfile)

        fill_template_with_xps_data(config_dict,
                                    xps_data_dict,
                                    template,
                                    searching_keys,
                                    entry_set)

        # Fill slot or field data from eln yaml file
        if eln_data_dict:
            for eln_key, eln_val in eln_data_dict.items():
                if eln_val == 'None':
                    pass
                elif eln_val:
                    tail_part_eln_key = eln_key.split("[entry]")[-1]
                    for tem_key, _ in template.items():
                        if tail_part_eln_key in tem_key:
                            template[tem_key] = eln_val

        str_entry = "/ENTRY[entry]"
        for key, _ in template.items():
            if str_entry in key:
                del template[key]

        return template


READER = XPSReader
