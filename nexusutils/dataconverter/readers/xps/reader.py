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
                components = key.split("/")
                entry = (f'{components[2]}'
                         f'__'
                         f'{components[3].split("_", 1)[1]}'
                         f'__'
                         f'{components[5].split("_", 1)[1]}'
                         )
                entries_values[entry] = val

    elif dt_typ == "@data":

        # var needs to construct BE axis
        attr_dict = {"mcd_num": 0,
                     "curves_per_scan": 0,
                     "values_per_curve": 0,
                     "mcd_head": 0,
                     "mcd_tail": 0,
                     "excitation_energy": 0,
                     "kinetic_energy": 0,
                     "effective_workfunction": 0,
                     "scan_delta": 0,
                     "pass_energy": 0,
                     "mcd_shifts": [],
                     "mcd_poss": [],
                     "mcd_gains": []}

        for key, val in xps_data_dict.items():
            components = key.split("/")
            try:
                entry = (f'{components[2]}'
                         f'__'
                         f'{components[3].split("_", 1)[1]}'
                         f'__'
                         f'{components[5].split("_", 1)[1]}'
                         )
            except IndexError:
                continue

            if entry not in entries_values:
                entries_values[entry] = {}
                entries_values[entry]["data"] = {}
                entries_values[entry]["attrb"] = copy.deepcopy(attr_dict)

            if "region/curves_per_scan" in key:
                entries_values[entry]["attrb"]["curves_per_scan"] = val
            elif "region/values_per_curve" in key:
                entries_values[entry]["attrb"]["values_per_curve"] = val

            elif "region/excitation_energy" in key:
                entries_values[entry]["attrb"]["excitation_energy"] = val

            elif "region/scan_mode/name" in key:
                entries_values[entry]["attrb"]["scan_mode"] = val

            elif "region/kinetic_energy" in key:
                if "region/kinetic_energy_base" not in key:
                    entries_values[entry]["attrb"]["kinetic_energy"] = val
                else:
                    continue

            elif "region/effective_workfunction" in key:
                entries_values[entry]["attrb"]["effective_workfunction"] = val

            elif "region/scan_delta" in key:
                entries_values[entry]["attrb"]["scan_delta"] = val

            elif "region/pass_energy" in key:
                entries_values[entry]["attrb"]["pass_energy"] = val

            elif "mcd_head" in key:
                entries_values[entry]["attrb"]["mcd_head"] = val

            elif "mcd_tail" in key:
                entries_values[entry]["attrb"]["mcd_tail"] = val

            elif "shift" in key:
                entries_values[entry]["attrb"]["mcd_shifts"].append(val)
                entries_values[entry]["attrb"]["mcd_num"] += 1

            elif "gain" in key:
                entries_values[entry]["attrb"]["mcd_gains"].append(val)

            elif "position" in key:
                entries_values[entry]["attrb"]["mcd_poss"].append(val)

            if key_part in key:

                # key_part -> cycles/Cycle_
                _, last_part = key.split(key_part)
                if "/time" in last_part:
                    continue
                parts = last_part.split("/")
                cycle_num, scan_num = parts[0], parts[-2].split("_")[1]
                da_name = f"cycle{cycle_num}_scan{scan_num}_"

                # data_array = (name, data, dimension,
                counts = val
                entries_values[entry]["data"][da_name] = counts

        def construct_be_and_counts():
            """Construct the Binding Energy and separate the counts for
               different detectors and finally sum up all the counts for
               to find total electron counts.
            """
            ents_vals_items = copy.deepcopy(tuple(entries_values.items()))
            for entry_key, entry_val in ents_vals_items:

                data = copy.deepcopy(entry_val["data"])
                entries_values[entry_key]["data"] = None
                attrb = entry_val["attrb"]

                mcd_num = int(attrb["mcd_num"])
                curves_per_scan = attrb["curves_per_scan"]
                values_per_curve = attrb["values_per_curve"]
                values_per_scan = curves_per_scan * values_per_curve
                mcd_head = int(attrb["mcd_head"])
                mcd_tail = int(attrb["mcd_tail"])
                values_per_scan = int(values_per_scan)
                excitation_energy = attrb["excitation_energy"]
                scan_mode = attrb["scan_mode"]
                kinetic_energy = attrb["kinetic_energy"]
                scan_delta = attrb["scan_delta"]
                pass_energy = attrb["pass_energy"]

                binding_energy_upper = excitation_energy - kinetic_energy

                mcd_energy_shifts = attrb["mcd_shifts"]
                mcd_energy_offsets = []
                offset_ids = []
                # consider offset values for detector with respect to
                # position at +16 which is usually large
                # and positive value

                for mcd_shift in mcd_energy_shifts:
                    mcd_energy_offset = (mcd_energy_shifts[-1] - mcd_shift) * pass_energy
                    mcd_energy_offsets.append(mcd_energy_offset)
                    offset_id = round(mcd_energy_offset / scan_delta)
                    offset_ids.append(int(offset_id - 1 if offset_id > 0 else offset_id))

                # Skiping entry without count data
                if not mcd_energy_offsets:
                    del entries_values[entry_key]
                    continue
                mcd_energy_offsets = np.array(mcd_energy_offsets)
                # Putting energy of the last detector as a highest energy
                starting_eng_pnts = binding_energy_upper - mcd_energy_offsets
                ending_eng_pnts = \
                    (starting_eng_pnts - values_per_scan * scan_delta)

                channeltron_eng_axes = np.zeros((mcd_num, values_per_scan))
                for ind in np.arange(len(channeltron_eng_axes)):
                    channeltron_eng_axes[ind, :] = \
                        np.linspace(starting_eng_pnts[ind],
                                    ending_eng_pnts[ind],
                                    values_per_scan)

                channeltron_eng_axes = np.round_(channeltron_eng_axes,
                                                 decimals=8)
                # construct ultimate or incorporated energy axis from
                # lower to higher energy
                scans = list(data.keys())
                # Check whether array is empty or not
                if not scans:
                    del entries_values[entry_key]
                    continue
                if not data[scans[0]].any():
                    del entries_values[entry_key]
                    continue
                # Sorting in descending order
                binding_energy = channeltron_eng_axes[-1, :]

                entries_values[entry_key]["data"] = xr.Dataset()

                for scan_nm in scans:
                    channel_counts = np.zeros((mcd_num + 1,
                                               values_per_scan))
                    # values for scan_nm corresponds to the data for each
                    # "scan" in individual CountsSeq
                    scan_counts = data[scan_nm]

                    if scan_mode == "FixedAnalyzerTransmission":
                        for row in np.arange(mcd_num):

                            count_on_row = scan_counts[row::mcd_num]
                            # Reverse counts from lower BE to higher
                            # BE as in BE_eng_axis
                            count_on_row = \
                                count_on_row[mcd_head:-mcd_tail]

                            channel_counts[row + 1, :] = count_on_row
                            channel_counts[0, :] += count_on_row

                            entries_values[entry_key]["data"][f"{scan_nm}chan{row}"] = \
                                xr.DataArray(data=channel_counts[row + 1, :],
                                             coords={"BE": binding_energy})

                            if row == (mcd_num - 1):
                                data_var = f"{scan_nm[:-1]}"

                                entries_values[entry_key]["data"][data_var] = \
                                    xr.DataArray(data=channel_counts[0, :],
                                                 coords={"BE": binding_energy})
                    else:
                        for row in np.arange(mcd_num):

                            start_id = offset_ids[row]
                            count_on_row = scan_counts[start_id::mcd_num]
                            count_on_row = count_on_row[0:values_per_scan]
                            channel_counts[row + 1, :] = count_on_row

                            # shifting and adding all the curves over the left curve.
                            channel_counts[0, :] += count_on_row

                            entries_values[entry_key]["data"][f"{scan_nm}chan{row}"] = \
                                xr.DataArray(data=channel_counts[row + 1, :],
                                             coords={"BE": binding_energy})

                            if row == (mcd_num - 1):
                                data_var = f"{scan_nm[:-1]}"

                                entries_values[entry_key]["data"][data_var] = \
                                    xr.DataArray(data=channel_counts[0, :],
                                                 coords={"BE": binding_energy})

        construct_be_and_counts()

    return entries_values


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

        if "@data" in value:

            key_part = value.split("data:")[-1]
            dt_typ = "@data"
            entries_values = find_entry_and_value(xps_data_dict,
                                                  key_part, dt_typ)

            survey_count_ = 0
            count = 0

            for entry, ent_value in entries_values.items():
                entry_set.add(entry)
                modified_key = key.replace("entry", entry)
                modified_root = key[0]
                modifid_entry = key[0:13]
                modifid_entry = modifid_entry.replace("entry", entry)
                template[f"{modifid_entry}/@default"] = "data"
                if "Survey" in entry and survey_count_ == 0:
                    survey_count_ = survey_count_ + 1
                    template[f"{modified_root}/@default"] = entry
                if survey_count_ == 0 and count == 0:
                    count = count + 1
                    template[f"{modified_root}/@default"] = entry
                # Filling out the scan data separately
                data = ent_value["data"]
                # attr = ent_value["attrb"]
                binding_energy_coord = None
                scan_num = 0
                for data_var in data.data_vars:
                    scan_num = scan_num + 1
                    scan = data_var
                    key_indv_scn_dta = modified_key.replace("[data]/data",
                                                            f"[data]/{scan}")
                    key_indv_scn_dta_unit = \
                        modified_key.replace("[data]/data",
                                             f"[data]/{scan}/@units")

                    binding_energy_coord = list(data[data_var].coords)[0]
                    binding_energy_coord = np.array(data[data_var][binding_energy_coord])
                    template[key_indv_scn_dta] = \
                        ent_value["data"][data_var].data
                    template[key_indv_scn_dta_unit] = \
                        config_dict[f"{key}/@units"]

                # signal takes the sum of the counts along the scan axis
                key_signal = modified_key.replace("[data]/data",
                                                  "[data]/@signal")
                key_data = modified_key.replace("[data]/data",
                                                "[data]/data")
                key_data_unit = modified_key.replace("[data]/data",
                                                     "[data]/data/@units")
                key_binding_energy = modified_key.replace("[data]/data", "[data]/BE")
                key_binding_energy_unit = modified_key.replace("[data]/data",
                                                               "[data]/BE/@units")
                key_binding_energy_axes = modified_key.replace("[data]/data",
                                                               "[data]/@axes")
                key_binding_energy_ind = modified_key.replace("[data]/data",
                                                              "[data]/@BE_indices")
                key_nxclass = modified_key.replace("[data]/data",
                                                   "[data]/@NX_class")

                template[key_signal] = "data"
                template[key_data] = np.mean([data[x_arr].data
                                             for x_arr in data.data_vars
                                              if "_chan" not in x_arr],
                                             axis=0)
                template[f"{key_data}_errors"] = \
                    np.std([data[x_arr].data
                            for x_arr in data.data_vars
                            if "_chan" not in x_arr], axis=0)
                template[key_data_unit] = config_dict[f"{key}/@units"]
                template[key_binding_energy_unit] = "eV"
                template[key_binding_energy] = binding_energy_coord
                template[key_binding_energy_axes] = "BE"
                template[key_binding_energy_ind] = 0
                template[key_nxclass] = "NXdata"

            try:
                del template[key]
            except KeyError:
                pass

            try:
                key_signal = key.replace("/data", "/@signal")
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
