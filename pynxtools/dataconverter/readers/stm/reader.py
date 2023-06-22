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
from typing import Any, Dict, List, Tuple
from typing import Tuple
import numpy as np
import nanonispy as nap
import re

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template


def is_separator_char_exist(key, sep_char_li):
    """
    Check string or key whether the separator char provided in
    'Separator Char List' exist or not.
    """
    bool_k = [x in sep_char_li for x in key]
    return np.any(bool_k)


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

            return [(raw_key, val), (f"{raw_key}/@units", unit)]
    return


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
    print(file_name)

    scan_file = nap.read.Scan(file_name)
    header_end_byte = scan_file.start_byte()

    h_part = scan_file.read_raw_header(header_end_byte)
    while True:
        if not re.match("[a-zA-Z]", h_part):
            h_part = h_part[1:]
        else:
            break
    h_comp_iter = iter(re.split('\n:|:\n', h_part))

    return dict(zip(h_comp_iter, h_comp_iter)), scan_file.signals


def get_SPM_metadata_dict_and_signal(file_name):
    """
    Get meradata and signal from spm file.
    """
    metadata_dict, signal = sxm_raw_metadata_and_signal(file_name)
    nesteded_matadata_dict = get_nested_dict_from_nested_key_dict(metadata_dict)
    path_items = dict_to_path(nested_dict=nesteded_matadata_dict)
    entity_unit_items: List[Tuple[Any, Any]] = []
    for path, val in path_items:
        phy_qunt_unit_list = convert_key_to_unit_and_entity(path, val,
                                                            start_bracket='(',
                                                            end_bracket=')')
        if phy_qunt_unit_list is not None:
            entity_unit_items.extend(phy_qunt_unit_list)
        else:
            entity_unit_items.append((path, val))

    return entity_unit_items, signal


def pass_metadata_and_signal_into_template(template, file_name):
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


class STMReader(BaseReader):
    """ Reader for XPS.
    """
    # NXroot is a general purpose definition one can review data with this definition
    supported_nxdls = ["NXroot"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None):
        """
            General read menthod to prepare the template.
        """

        file_dir = os.path.abspath(os.path.dirname(__file__))
        SPM_file = os.path.join(
            file_dir,
            'SPM_data_folder/TiSe2_2303a_annealing_300C_5min_evaporate_Pyrene_1_0070.sxm')

        clean_template = Template()
        filled_template = pass_metadata_and_signal_into_template(clean_template, SPM_file)
        return filled_template


READER = STMReader
