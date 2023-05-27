"""
    A short description on STM reader.
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
from typing import Any, Dict, List, Tuple, Union
from typing import Tuple
import numpy as np
import nanonispy as nap
import re
import json

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.stm.bias_spec_data_parser import from_dat_file_into_template
from pynxtools.dataconverter.readers.stm.stm_helper import *


def is_separator_char_exist(key, sep_char_li):
    """
    Check string or key whether the separator char provided in
    'Separator Char List' exist or not.
    """
    bool_k = [x in sep_char_li for x in key]
    return np.any(bool_k)


# TODO: get_nested_dict_from_concatenated_key()
# TODO: Add sep_chars in function parameter list
def get_nested_dict_from_nested_key_dict(data_dict, dict_to_map_path=None):
    """
    Create nested dict. If key are concateneted with '_', '>' split the key and
    construct nested dict. For example, {'x1': {'x2': {'x3': {'x4': {'x5': 3}}}}
    from 'x1_x2_x3_x4>x5:3'
    """
    if dict_to_map_path is not None:
        spreaded_dict = dict_to_map_path
    else:
        spreaded_dict: Dict[str, Any] = {}
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
                    spreaded_dict[l_key] = get_nested_dict_from_nested_key_dict(
                        {r_key: d_val}, dict_to_map_path=spreaded_dict[l_key])
                else:
                    spreaded_dict[l_key]: Dict[str, Any] = {}
                    spreaded_dict[l_key] = get_nested_dict_from_nested_key_dict(
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


# TODO: try to replace dict_to_path by nested_dict_to_slash_spepare_path
def dict_to_path(nested_dict, full_path='', sep='/'):
    items = []
    for key, val in nested_dict.items():
        new_path = full_path + sep + key if full_path else f'/{key}'
        if isinstance(val, dict):
            items.extend(dict_to_path(val, new_path, sep=sep))
        else:
            if isinstance(val, dict) and isinstance(new_path, dict):
                items.append((new_path.strip(), val.strip()))
            else:
                items.append((new_path, val))

    return items


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
    nesteded_matadata_dict = get_nested_dict_from_nested_key_dict(metadata_dict)
    # print('#### nested_metadata : ', nesteded_matadata_dict)

    # Convert nested (dict) path to signal into slash_separated path to signal
    temp_flattened_dict_sig = {}
    slash_sep_path_to_signal = nested_path_to_slash_separated_path(signal,
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
    # entity_unit_items: List[Tuple[Any, Any]] = []
    # # print(' path items : ', path_items)
    # for path, val in path_items:
    #     phy_qunt_unit_list = convert_key_to_unit_and_entity(path, val,
    #                                                         start_bracket='(',
    #                                                         end_bracket=')')
    #     if phy_qunt_unit_list is not None:
    #         entity_unit_items.extend(phy_qunt_unit_list)
    #     else:
    #         entity_unit_items.append((path, val))
    # print('### : ', entity_unit_items)
    # return entity_unit_items, signal
    # print('### flattened_dict : ', flattened_dict)

    flattened_dict.update(temp_flattened_dict_sig)
    with open('sxm_data.txt', mode='w', encoding='utf-8') as tmp_f:
        for key, val in flattened_dict.items():
            tmp_f.write(f"{key} ## : ##, {val}\n")
    return flattened_dict


def from_sxm_into_template(template, file_name, config_dict):
    """
    Pass metadata and signals into template. This should be last steps for writting
    metadata and data into nexus template.
    """

    dict_path, signal = get_SPM_metadata_dict_and_signal(file_name)
    for key, val in dict_path:
        key = '/ENTRY[Entry]' + key
        template[key] = val
    template.update(signal_obj_to_template_dict(signal))
    return template


def signal_obj_to_template_dict(signal):
    """
    Write signal data in NXdata class.
    """
    template_dict = {}

    def construct_nexus_data_path(nx_data_field, np_data, prefix,
                                  axes=None, signal=False):

        key = prefix + '/' + nx_data_field
        tmp_dict = {key: np_data}
        if signal:
            key = prefix + '/@signal'
            tmp_dict[key] = nx_data_field[1:]
        if axes:
            key = prefix + '/' + nx_data_field + '/@axes'
            tmp_dict[key] = axes
            for i, axis in enumerate(axes):
                key = prefix + '/' + nx_data_field + f'/@{axis}_indices'
                tmp_dict[key] = i

        return tmp_dict
    path_to_val_items = dict_to_path(signal, full_path='', sep='\u00A0')
    # using unicode \u00A0 for non-space brack character
    for nx_full_path, val in path_to_val_items:
        if 'Z\u00A0forward' in nx_full_path:
            nxdata_signal = True
        else:
            nxdata_signal = False

        template_dict.update(construct_nexus_data_path(
            nx_full_path,
            val, '/ENTRY[Entry]/DATA[DATA]',
            ['slow\u00A0scan\u00A0direction\u00A0in\u00A0pixel',
             'fast\u00A0scan\u00A0direction\u00A0in\u00A0pixel'],
            signal=nxdata_signal))

    return template_dict

# TODO: remove this fucntion. This was written to parse dat file
# def write_nxdata_from_nx_greoup_dict(template, nx_data_info_dict):
#     """
#     """
#     for key, data_info_dict in nx_data_info_dict.items():
#         Bias_axis = 0
#         grp_key = f"/ENTRY[Entry]/DATA[{data_info_dict['nx_data_group_name']}]"

#         data_field = grp_key + '/data'
#         template[data_field] = data_info_dict['action_result'][1]
#         data_field_signal = data_field + '/@signal'
#         template[data_field_signal] = data_info_dict['action_result'][1]
#         data_field_axis = data_field + '/axes'
#         template[data_field_axis] = ['Bias']
#         data_field_long_name = data_field + '/@long_name'
#         template[data_field_long_name] = 'dI/dV'

#         grp_signal = grp_key + '/@signal'
#         grp_axes = grp_key + '/@axes'
#         template[grp_axes] = ['Bias']
#         template[grp_signal] = 'data'
#         grp_axis = grp_key + '/Bias'
#         template[grp_axis] = data_info_dict['action_result'][0]
#         long_name = 'Bias (mV)'
#         grp_axis_lg_nm = grp_axis + '/@long_name'
#         template[grp_axis_lg_nm] = long_name
#         # template[grp_axis_lg_nm] = 'dI/dV'
#         grp_axis_ind = grp_key + '/@Bias_indices'
#         template[grp_axis_ind] = Bias_axis


class STMReader(BaseReader):
    """ Reader for XPS.
    """
    # NXroot is a general purpose definition one can review data with this definition
    supported_nxdls = ["NXiv_sweep2"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None):
        """
            General read menthod to prepare the template.
        """

        has_sxm_input_file = False
        sxm_file: str = ""
        has_dat_input_file = False
        dat_file: str = ""
        filled_template: Union[Dict, None] = Template()
        config_dict: Union[Dict, None] = None

        for file in file_paths:
            ext = file.rsplit('.', 1)[-1]

            if ext == 'sxm':
                has_sxm_input_file = True
                sxm_file = file
            if ext == 'dat':
                has_dat_input_file = True
                dat_file = file
            if ext == 'json':
                with open(file, mode="r", encoding="utf-8") as jf:
                    config_dict = json.load(jf)
        if not has_dat_input_file and not has_sxm_input_file:
            raise ValueError("Not correct file has been found. please render correct input"
                             " file of spm with extension: .dat or .sxm")
        if has_dat_input_file and has_sxm_input_file:
            raise ValueError("Only one file from .dat or .sxm can be read.")
        if has_sxm_input_file and config_dict:
            from_sxm_into_template(template, sxm_file, config_dict)
        elif has_dat_input_file and config_dict:
            from_dat_file_into_template(template, dat_file, config_dict)
        else:
            raise ValueError("Not correct input file has been provided.")

        for key, val in template.items():

            if val is None:
                del template[key]
            else:
                filled_template[key] = val

        if not filled_template:
            return filled_template
        else:
            raise ValueError("Reader could not read anything! Check for input files and the"
                             " corresponding extention.")


READER = STMReader
