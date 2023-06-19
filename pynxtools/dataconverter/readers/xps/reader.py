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
from typing import Any, Dict, Set, List
from typing import Tuple
import sys
import json

import yaml
import numpy as np

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.xps.reader_utils import XpsDataFileParser
from pynxtools.dataconverter.readers.utils import flatten_and_replace, FlattenSettings
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.helpers import extract_atom_types

np.set_printoptions(threshold=sys.maxsize)

XPS_TOCKEN = "@xps_tocken:"
XPS_DATA_TOCKEN = "@data:"
XPS_DETECTOR_TOCKEN = "@detector_data:"
ELN_TOCKEN = "@eln"
# Track entries for using for eln data
ENTRY_SET: Set[str] = set()
DETECTOR_SET: Set[str] = set()
POSSIBLE_ENTRY_PATH: Dict = {}


CONVERT_DICT = {
    'unit': '@units',
    'version': '@version',
    'User': 'USER[user]',
    'Instrument': 'INSTRUMENT[instrument]',
    'Source': 'SOURCE[source]',
    'Beam': 'BEAM[beam]',
    'Analyser': 'ELECTRONANALYSER[electronanalyser]',
    'Collectioncolumn': 'COLLECTIONCOLUMN[collectioncolumn]',
    'Energydispersion': 'ENERGYDISPERSION[energydispersion]',
    'Detector': 'DETECTOR[detector]',
    'Manipulator': 'MANIPULATOR[manipulator]',
    'Sample': 'SAMPLE[sample]',
    'Data': 'DATA[data]',
}

REPLACE_NESTED: Dict[str, str] = {}


def construct_entry_name(key):
    """Construct entry name from vendor, sample_name and region name"""

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
    if dt_typ == XPS_TOCKEN:

        for key, val in xps_data_dict.items():
            if key_part in key:
                entry = construct_entry_name(key)
                entries_values[entry] = val

    elif dt_typ in (XPS_DATA_TOCKEN, XPS_DETECTOR_TOCKEN):
        # entries_values = entry:{cycle0_scan0_chan0:xr.data}
        entries_values = xps_data_dict["data"]

    return entries_values


# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def fill_data_group(key,
                    entries_values,
                    config_dict,
                    template,
                    entry_set):
    """Fill out fileds and attributes for NXdata"""

    survey_count_ = 0
    count = 0

    for entry, xr_data in entries_values.items():
        entry_set.add(entry)
        modified_key = key.replace("entry", entry)
        modified_key = modified_key.replace("[data]/data", "[data]")
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
        chan_count = "_chan"
        for data_var in xr_data.data_vars:
            scan = data_var
            # Collecting only accumulated counts
            # indivisual channeltron counts goes to detector data section
            if chan_count not in scan:
                key_indv_scn_dt = f"{modified_key}/{scan}"

                key_indv_scn_dt_unit = f"{key_indv_scn_dt}/@units"

                coord_nm = list(xr_data[data_var].coords)[0]
                binding_energy_coord = np.array(xr_data[data_var][coord_nm])
                template[key_indv_scn_dt] = xr_data[data_var].data
                template[key_indv_scn_dt_unit] = config_dict[f"{key}/@units"]

        key_data = f"{modified_key}/data"
        key_data_unit = f"{key_data}/@units"

        key_signal = f"{modified_key}/@signal"

        be_nm = "BE"
        be_index = 0
        key_be = f"{modified_key}/{be_nm}"
        key_be_unit = f"{key_be}/@units"
        key_be_axes = f"{modified_key}/@axes"
        key_be_ind = f"{modified_key}/@{be_nm}_indices"

        # setting up AXISNAME
        axisname = "AXISNAME[axisname]"
        long_name = "Binding Energy"
        key_ax_mn = f"{modified_key}/{axisname}"
        key_ax_ln_nm = f"{modified_key}/{axisname}/@long_name"

        key_nxclass = f"{modified_key}/@NX_class"

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
        template[key_be_unit] = "eV"
        template[key_be] = binding_energy_coord
        template[key_be_axes] = be_nm
        template[key_be_ind] = be_index
        template[key_nxclass] = "NXdata"
        template[key_ax_ln_nm] = long_name
        template[key_ax_mn] = be_index


def fill_detector_group(key,
                        entries_values,
                        config_dict,
                        template,
                        entry_set):
    """Fill out fileds and attributes for NXdetector/NXdata"""

    for entry, xr_data in entries_values.items():
        entry_set.add(entry)

        chan_count = "_chan"

        # Iteration over scan
        for data_var in xr_data.data_vars:

            if chan_count in data_var:
                detector_num = data_var.split("_chan")[-1]
                detector_nm = f"detector{detector_num}"
                DETECTOR_SET.add(detector_nm)
                scan_num = data_var.split("_scan")[-1].split("_chan")[0]
                scan_nm = f"scan_{scan_num}"
                modified_key = key.replace("entry", entry)
                modified_key = modified_key.replace("[detector]", f"[{detector_nm}]")
                modified_key = modified_key.replace("[data]", f"[{scan_nm}]")
                modified_key_unit = modified_key + "/@units"

                template[modified_key] = xr_data[data_var].data
                key_indv_chan_sginal = modified_key.replace("/raw", "/@signal")
                template[key_indv_chan_sginal] = "raw"
                template[modified_key_unit] = config_dict[f"{key}/@units"]


def fill_template_with_xps_data(config_dict,
                                xps_data_dict,
                                template,
                                entry_set):
    """Collect the xps data from xps_data_dict
        and store them into template. We use searching_keys
        for separating the data from xps_data_dict.
    """
    for key, value in config_dict.items():
        if XPS_DATA_TOCKEN in value:
            key_part = value.split(XPS_DATA_TOCKEN)[-1]
            entries_values = find_entry_and_value(xps_data_dict,
                                                  key_part,
                                                  dt_typ=XPS_DATA_TOCKEN)

            fill_data_group(key, entries_values, config_dict, template, entry_set)

        if XPS_DETECTOR_TOCKEN in value:
            key_part = value.split(XPS_DATA_TOCKEN)[-1]
            entries_values = find_entry_and_value(xps_data_dict,
                                                  key_part,
                                                  dt_typ=XPS_DETECTOR_TOCKEN)

            fill_detector_group(key, entries_values, config_dict, template, entry_set)

        if XPS_TOCKEN in value:
            tocken = value.split(XPS_TOCKEN)[-1]
            entries_values = find_entry_and_value(xps_data_dict,
                                                  tocken,
                                                  dt_typ=XPS_TOCKEN)
            for entry, ent_value in entries_values.items():
                entry_set.add(entry)
                modified_key = key.replace("[entry]", f"[{entry}]")
                template[modified_key] = ent_value
                try:
                    template[f"{modified_key}/@units"] = config_dict[f"{key}/@units"]
                except KeyError:
                    pass


# pylint: disable=too-many-branches
def fill_template_with_eln_data(eln_data_dict,
                                config_dict,
                                template,
                                entry_set):
    """Fill the template from provided eln data"""

    def fill_atom_types(key):
        atom_types: List = []
        field_value = eln_data_dict[key]

        if "chemical_formula" in key:
            atom_types = list(extract_atom_types(field_value))

        if field_value is None:
            return

        for entry in entry_set:
            modified_key = key.replace("[entry]", f"[{entry}]")
            template[modified_key] = field_value
            if atom_types:
                modified_key = modified_key.replace('chemical_formula', 'atom_types')
                template[modified_key] = ', '.join(atom_types)

    def fill_from_value(key):
        field_value = eln_data_dict[key]
        if not field_value:
            return
        # Do for all entry name
        for entry in entry_set:
            modified_key = key.replace("[entry]", f"[{entry}]")
            # Do for all detector
            if "[detector]" in key:
                for detector in DETECTOR_SET:
                    detr_key = modified_key.replace("[detector]", f"[{detector}]")
                    template[detr_key] = field_value
            else:
                template[modified_key] = field_value

    for key, val in config_dict.items():
        if ELN_TOCKEN in val:
            fill_atom_types(key)
        elif key in list(eln_data_dict.keys()):
            fill_from_value(key)


def concatenate_values(value1, value2):
    """
    Concatenate two values of same type to be stored
    in xps_data_dict. Dicts are merged and every other object is
    appended to a list.

    """
    if (isinstance(value1, dict) and isinstance(value2, dict)):
        concatenated = {**value1, **value2}
    else:
        if not isinstance(value1, list):
            value1 = [value1]
        if not isinstance(value2, list):
            value2 = [value2]
        concatenated = value1 + value2

    return concatenated


# pylint: disable=too-few-public-methods
class XPSReader(BaseReader):
    """ Reader for XPS.
    """

    supported_nxdls = [
        "NXmpes",
        # "NXmpes_xps"
    ]

    __config_files: Dict = {
        "xml": "config_file_xml.json",
        "sle": "config_file_xml.json",
        "txt": "config_file_scienta_txt.json",
    }

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None,
             **kwargs) -> dict:
        """Reads data from given file and returns
        a filled template dictionary"""

        reader_dir = Path(__file__).parent

        xps_data_dict: Dict[str, Any] = {}
        eln_data_dict: Dict[str, Any] = {}

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
            elif file_ext in [".sle", ".xml", ".txt"]:
                data_dict = XpsDataFileParser([file]).get_dict(**kwargs)

                # If there are multiple input data files, make sure
                # that existing keys are not overwritten.
                existing = [
                    (key, xps_data_dict[key], data_dict[key]) for
                    key in set(xps_data_dict).intersection(data_dict)
                ]

                xps_data_dict = {**xps_data_dict, **data_dict}
                for (key, value1, value2) in existing:
                    xps_data_dict[key] = concatenate_values(
                        value1, value2)

                config_file = reader_dir.joinpath(
                    XPSReader.__config_files[file_ext.rsplit('.')[1]]
                )

            # This code is not very robust.
            elif file_ext == ".json":
                if "config_file" in file:
                    config_file = Path(file)

        with open(config_file, encoding="utf-8", mode="r") as cfile:
            config_dict = json.load(cfile)

        fill_template_with_xps_data(config_dict,
                                    xps_data_dict,
                                    template,
                                    ENTRY_SET)
        if eln_data_dict:
            fill_template_with_eln_data(eln_data_dict,
                                        config_dict,
                                        template,
                                        ENTRY_SET)
        else:
            raise ValueError("Eln file must be submited with some required fields and attributes.")

        final_template = Template()
        for key, val in template.items():
            if ("/ENTRY[entry]" not in key) and (val is not None):
                final_template[key] = val

        return final_template


READER = XPSReader
