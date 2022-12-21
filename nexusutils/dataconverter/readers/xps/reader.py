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
from nexusutils.dataconverter.template import Template

np.set_printoptions(threshold=sys.maxsize)

xps_tocken = "@xps_tocken:"
xps_data_tocken = "@data:"
eln_tocken = "@eln"

CONVERT_DICT = {
    'Instrument': 'INSTRUMENT[instrument]',
    'Analyser': 'ELECTRONANALYSER[electronanalyser]',
    'Beam': 'BEAM[beam]',
    'unit': '@units',
    'version': '@version',
    'Sample': 'SAMPLE[sample]',
    'User': 'USER[user]',
    'Data': 'DATA[data]',
    'Source': 'SOURCE[source]',
    'Collectioncolumn': 'COLLECTIONCOLUMN[collectioncolumn]',
    'Energydispersion': 'ENERGYDISPERSION[energydispersion]'
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
    if dt_typ == xps_tocken:

        for key, val in xps_data_dict.items():
            if key_part in key:
                entry = construct_entry_name(key)
                entries_values[entry] = val

    elif dt_typ == xps_data_tocken:
        # entries_values = entry:{cycle0_scan0_chan0:xr.data}
        entries_values = xps_data_dict["data"]

    return entries_values


def fill_data_class(key,
                    entries_values,
                    config_dict,
                    template,
                    entry_set):

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
                                entry_set):
    """Collect the xps data from xps_data_dict
        and store them into template. We use searching_keys
        for separating the data from xps_data_dict.
    """

    for key, value in config_dict.items():

        if xps_data_tocken in value:
            key_part = value.split(xps_data_tocken)[-1]
            entries_values = find_entry_and_value(xps_data_dict,
                                                  key_part,
                                                  dt_typ=xps_data_tocken)

            fill_data_class(key, entries_values, config_dict,
                            template, entry_set)

        if xps_tocken in value:
            tocken = value.split(xps_tocken)[-1]
            entries_values = find_entry_and_value(xps_data_dict,
                                                  tocken,
                                                  dt_typ=xps_tocken)
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
def fill_template_with_eln_data(eln_data_dict,
                                config_dict,
                                template,
                                entry_set):

    for key, val in config_dict.items():

        if eln_tocken in val:
            field_value = eln_data_dict[key]
            if field_value is None:
                continue
            for entry in entry_set:
                modified_key = key.replace("[entry]", f"[{entry}]")

                try:
                    field_value = float(field_value)
                except ValueError:
                    if isinstance(field_value, list):
                        field_value = np.array(field_value)
                template[modified_key] = field_value

        elif key in list(eln_data_dict.keys()):
            field_value = eln_data_dict[key]
            if field_value is not None:
                for entry in entry_set:
                    modified_key = key.replace("[entry]", f"[{entry}]")
                    template[modified_key] = field_value


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
                                    entry_set)
        if eln_data_dict:
            fill_template_with_eln_data(eln_data_dict,
                                        config_dict,
                                        template,
                                        entry_set)
        # TODO: add here warnings instead of error
        else:
            raise ValueError("Eln file must be submit with some required filed and attribute.")

        final_template = Template()
        str_entry = "/ENTRY[entry]"
        for key, val in template.items():
            if (str_entry in key) and (val is not None):
                final_template[key] = val

        return final_template


READER = XPSReader
