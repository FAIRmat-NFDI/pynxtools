"""
    A parse stm file in nexus generated definition template.
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


from typing import Any, Dict
import numpy as np
import nanonispy as nap
import re

from pynxtools.dataconverter.readers.stm.bias_spec_file_parser import work_out_overwriteable_field
from pynxtools.dataconverter.readers.stm.stm_helper import *


def is_separator_char_exist(key, sep_char_li):
    """
    Check string or key whether the separator char provided in
    'Separator Char List' exist or not.
    """
    bool_k = [x in sep_char_li for x in key]
    return np.any(bool_k)


def get_nested_dict_from_concatenated_key(data_dict, dict_to_map_path=None,
                                          sep_chars=None):
    """
    Create nested dict. If key are concateneted with '_', '>' split the key and
    construct nested dict. For example, {'x1': {'x2': {'x3': {'x4': {'x5': 3}}}}
    from 'x1_x2_x3_x4>x5:3'
    """
    if dict_to_map_path is not None:
        spreaded_dict = dict_to_map_path
    else:
        spreaded_dict: Dict[str, Any] = {}
    if sep_chars is None:
        sep_chars = ['_', '>']
    for d_key, d_val in data_dict.items():
        if is_separator_char_exist(d_key, sep_chars):
            # Find out which separator char exist there
            for k_c in d_key:
                if k_c in sep_chars:
                    sep_char = k_c
                    break
            l_key, r_key = d_key.split(sep_char, 1)
            if not is_separator_char_exist(r_key, sep_chars):
                if l_key not in spreaded_dict:
                    spreaded_dict[l_key]: Dict[str, Any] = {}
                spreaded_dict[l_key][r_key] = d_val
            else:
                if l_key in spreaded_dict:
                    spreaded_dict[l_key] = get_nested_dict_from_concatenated_key(
                        {r_key: d_val}, dict_to_map_path=spreaded_dict[l_key])
                else:
                    spreaded_dict[l_key]: Dict[str, Any] = {}
                    spreaded_dict[l_key] = get_nested_dict_from_concatenated_key(
                        {r_key: d_val}, dict_to_map_path=spreaded_dict[l_key])
        else:
            spreaded_dict[d_key] = d_val

    return spreaded_dict


def convert_key_to_unit_and_entity(key, val, start_bracket='', end_bracket=''):
    """
    Split key into 'key' and 'key/@units' if key is designed as somthing like this 'key(A)'.
    """
    if start_bracket and end_bracket:
        if start_bracket in key and end_bracket in key:
            tmp_l_part, tmp_r_part = key.rsplit(start_bracket)
            unit = tmp_r_part.rsplit(end_bracket)[0]
            raw_key = tmp_l_part.strip()

            return [(raw_key, val), (f"{raw_key}/@unit", unit)]
    return


def sxm_raw_metadata_and_signal(file_name):
    """
    Retun metadata plain dict and signal
    Convert header part (that contains metadata) of a file with 'sxm' extension into
    plain dict.
    """
    scan_file = nap.read.Scan(file_name)
    header_end_byte = scan_file.start_byte()
    h_part = scan_file.read_raw_header(header_end_byte)
    while True:
        # Ignore all starting chars of string h_part except Alphabat
        if not re.match("[a-zA-Z]", h_part):
            h_part = h_part[1:]
        else:
            break

    h_comp_iter = iter(re.split('\n:|:\n', h_part))
    return dict(zip(h_comp_iter, h_comp_iter)), scan_file.signals


# TODO: REname this function
def get_SPM_metadata_dict_and_signal(file_name):
    """
    Get meradata and signal from spm file.
    """
    # TODO: clean comments
    metadata_dict, signal = sxm_raw_metadata_and_signal(file_name)
    nesteded_matadata_dict = get_nested_dict_from_concatenated_key(metadata_dict)

    # Convert nested (dict) path to signal into slash_separated path to signal
    temp_flattened_dict_sig = {}
    nested_path_to_slash_separated_path(signal,
                                        temp_flattened_dict_sig)
    temp_flattened_dict = {}
    nested_path_to_slash_separated_path(nesteded_matadata_dict,
                                        temp_flattened_dict)
    # path_items = dict_to_path(nested_dict=nesteded_matadata_dict)
    flattened_dict = {}
    for key, val in temp_flattened_dict.items():
        # list of tuples of (data path, data) and (unit path/unit and unit value)
        tuple_li = convert_key_to_unit_and_entity(key, val,
                                                  start_bracket='(',
                                                  end_bracket=')')
        if tuple_li:
            for tup in tuple_li:
                flattened_dict[tup[0]] = tup[1]
        else:
            flattened_dict[key] = val

    flattened_dict.update(temp_flattened_dict_sig)

    return flattened_dict


def construct_nxdata_for_sxm(template, data_dict, data_config_dict, data_group):
    """
    Construct NXdata that includes all the groups, field and attributes. All the elements
    will be stored in template.

    Parameters:
    -----------
    template : dict[str, Any]
        Capturing data elements. One to one dictionary for capturing data array, data axes
        and so on from data_dict to be ploted.
    data_dict : dict[str, Union[array, str]]
        Data stored from dat file. Path (str) to data elements which mainly come from
        dat file. Data from this dict will go to template
    data_config_dict : dict[str, list]
        This dictionary is numerical data order to list (list of path to data elements in
        input file). Each order indicates a group of data set.
    data_group : NeXus path for NXdata

    Return:
    -------
    None

    Raise:
    ------
    None
    """

    def indivisual_DATA_field():
        """Fill up template's indivisual data field and the descendant attribute.
            e.g. /Entry[ENTRY]/data/DATA,
              /Entry[ENTRY]/data/DATA/@axes and so on
        """
        global nxdata_grp, data_field

        # list of paths e.g. "/LI_Demod_2_X/forward" comes from
        # dict value of /ENTRY[entry]/DATA[data] in config file.
        for path in dt_val:
            grp_name, data_field = find_nxdata_group_and_name(path)
            signals.append(data_field)
            nxdata_grp = data_group.replace("DATA[data", f"DATA[{grp_name}")
            temp_data_field = nxdata_grp + '/' + data_field
            template[temp_data_field] = data_dict[path]

    def fill_out_NXdata_group(signal='auxiliary_signals'):
        """To fill out NXdata which is root for all data fields and attributes for NXdata.
           This function fills template with first level of descendent fields and attributes
           of NXdata but not the fields and attributes under child of NXdata.
        """
        for ind, signal in enumerate(signals):
            if ind == 0:
                template[nxdata_grp + '/@' + 'signal'] = data_field
            else:
                template[nxdata_grp + '/@' + 'auxiliary_signal'] = data_field

    def find_nxdata_group_and_name(key):
        """Find data group name from a data path in file.
        E.g. 'Z', 'LI_Demod_2_X' from /Z/forward and /LI_Demod_2_X/forward
        """
        tmp_key = key.split('/', 1)[1]
        grp_name, data_field_name = tmp_key.split('/', 1)

        return grp_name, data_field_name

    for _, dt_val in data_config_dict.items():
        signals = []
        indivisual_DATA_field()
        fill_out_NXdata_group('signal')

 #   template['/ENTRY[entry]/@default'] = {'link':'/ENTRY[entry]/DATA[Z]/forward'}


def collect_default_value(template, search_key):
    default_dict = {"/ENTRY[entry]/definition": "NXiv_sweep2",
                    "/ENTRY[entry]/experiment_description": "An stm experiment."}
    template[search_key] = default_dict[search_key]


def from_sxm_file_into_template(template, file_name, config_dict):
    """
    Pass metadata and signals into template. This should be last steps for writting
    metadata and data into nexus template.
    """

    data_dict = get_SPM_metadata_dict_and_signal(file_name)
    temp_keys = template.keys()

    for temp_key in temp_keys:
        for c_key, c_val in config_dict.items():
            if c_val in ['None', ""]:
                continue
            if temp_key == c_key and isinstance(c_val, str):
                if '@reader' in c_val:
                    collect_default_value(template, temp_key)
                else:
                    template[temp_key] = transform(data_dict[c_val])
                break
            if temp_key == c_key and isinstance(c_val, dict):
                data_group = "/ENTRY[entry]/DATA[data]"
                if temp_key == data_group:
                    construct_nxdata_for_sxm(template, data_dict,
                                             c_val, data_group)
                else:

                    work_out_overwriteable_field(template,
                                                 data_dict,
                                                 c_val,
                                                 temp_key)
                break

    return template