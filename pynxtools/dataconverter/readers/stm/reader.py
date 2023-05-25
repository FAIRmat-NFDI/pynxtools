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
from pynxtools.dataconverter.readers.stm.bias_spec_data_parser import BiasSpecData
from pynxtools.dataconverter.readers.stm.stm_helper import *


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


def write_nxdata_from_nx_greoup_dict(template, nx_data_info_dict):
    """
    """
    for key, data_info_dict in nx_data_info_dict.items():
        Bias_axis = 0
        grp_key = f"/ENTRY[Entry]/DATA[{data_info_dict['nx_data_group_name']}]"

        data_field = grp_key + '/data'
        template[data_field] = data_info_dict['action_result'][1]
        data_field_signal = data_field + '/@signal'
        template[data_field_signal] = data_info_dict['action_result'][1]
        data_field_axis = data_field + '/axes'
        template[data_field_axis] = ['Bias']
        data_field_long_name = data_field + '/@long_name'
        template[data_field_long_name] = 'dI/dV'

        grp_signal = grp_key + '/@signal'
        grp_axes = grp_key + '/@axes'
        template[grp_axes] = ['Bias']
        template[grp_signal] = 'data'
        grp_axis = grp_key + '/Bias'
        template[grp_axis] = data_info_dict['action_result'][0]
        long_name = 'Bias (mV)'
        grp_axis_lg_nm = grp_axis + '/@long_name'
        template[grp_axis_lg_nm] = long_name
        # template[grp_axis_lg_nm] = 'dI/dV'
        grp_axis_ind = grp_key + '/@Bias_indices'
        template[grp_axis_ind] = Bias_axis


def process_data_from_file_(flattened_dict):
    """Implement this function later.
        TODO:
        This functions mainly intended for automization of data manipulation
         or data driven analytics.
    """
    # This keys are collected from flatten_dict generated in
    # nested_path_to_slash_separated_path()

    # key_data_to_be_processed = {'0': {'/Bias/value': None,
    #                                   '/Current/value': None}}

    # for fla_key, fla_val in flattened_dict.items():
    #     for pro_key, pro_val in key_data_to_be_processed.items():
    #         for ele_key, ele_val in pro_val.items():
    #             if ele_key in fla_key:
    #                 pro_val[ele_key] = fla_val

    # nx_data_info_dict = {'0': {'nx_data_group_name': '(Normal)',
    #                         'nx_data_group_axes': ['Bias', 'dI/dV'],
    #                         'action': [slice_before_last_element, cal_dx_by_dy],
    #                         'action_variable':
    #                         [[key_data_to_be_processed['0']['/Bias/value']],
    #                         [key_data_to_be_processed['0']['/Current/value'],
    #                             key_data_to_be_processed['0']['/Bias/value']]],
    #                         'action_result': []}}

    # # TODO: add the print optionality for flattend dict option inside bias_spec_data_parser.py
    # later add this option inside README doc
    # with open('./dict_from_dat_file.txt', mode='+w', encoding='utf-8',) as fl:
    #     for key, val in flattened_dict.items():
    #         print('## val', key)
    #         fl.write(f"{key} : ##### {val}\n")
    # 0, 1,
    # print('key_data_to_be_processed', key_data_to_be_processed)
    # for key in key_data_to_be_processed.keys():
    #     key_dict = nx_data_info_dict[key]
    #     for action, action_variable in zip(key_dict['action'], key_dict['action_variable']):
    #         key_dict['action_result'].append(action(*action_variable))
    pass


def construct_nxdata(template, data_dict, data_config_dict, data_group):
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
        """Fill up indivisual data field:
            /Entry[ENTRY]/data/DATA
        """
        has_annot = False
        axes = ["Bias/",
                "Current/",
                "Temperature 1/",
                "LI Demod 1 X/",
                "LI Demod 1 Y/",
                "LI Demod 2 X/",
                "LI Demod 2 Y/"
                ]
        current = None
        volt = None
        # list of paths e.g. "/dat_mat_components/Bias/value"
        for path in anot_val:
            extra_annot, trimed_path = find_extra_annot(path)
            for axis in axes:
                if (axis + 'value') in trimed_path:
                    # removing forward slash
                    axes_name.append[axis[0:-1]]
                    axes_data.append[data_dict[path]]
                if (axis + 'unit') in trimed_path:
                    axes_unit.append(data_dict[path] if path in data_dict else "")
                if (axis + "metadata") in trimed_path:
                    axes_metadata.append(data_dict[path] if path in data_dict else "")
            if 'current/value' in trimed_path:
                current = data_dict[path]
            if 'Bias/value' in trimed_path:
                volt = data_dict[path]

        if not extra_annot:
            extra_annot = 'general'

        data_field = data_group + '/' + extra_annot
        template[data_field] = cal_dx_by_dy(current, volt)
        template[data_field + '/@axes'] = axes_name
        template[data_field + '/@long_name'] = "dI/dV(unit)"
        # TODO: After successfully running the code try out commented statement bellow
        # template[data_field + '@units']

    def fill_out_NXdata_group(signal='auxiliary_signals'):
        """To fill out NXdata which is root for data field and elements.
        """
        data_signal = data_group + '/@' + signal
        template[data_signal] = extra_annot
        data_axes = data_group + '/@' + axes_name
        template[data_axes] = axes_name
        for axis in axes_name:
            # construct AXISNAME_indices
            template[data_group + '/@' + axis + '_indices'] = 0

        for axis, unit in zip(axes_name, axes_unit):
            if unit:
                template[data_group + '/' + axis + '/@longname'] = f"{axis}({unit})"
            else:
                template[data_group + '/' + axis + '/@longname'] = f"{axis}"

        # AXISNAME is not defined yet

    def find_extra_annot(key):
        annot_li = [' [filt]']
        for annot in annot_li:
            if annot in key:
                trimed_annot = annot[annot.index('['):-1]
                return trimed_annot, key.replace(annot, "")
        return "", key

    for anot_key, anot_val in data_config_dict.items():
        # Working with '1' order
        # TODO: Discus
        axes_name = []
        axes_unit = []
        axes_metadata = []
        axes_data = []
        # 'extra_annot' will be considered as a data field /NXdata/DATA
        extra_annot = ""
        # To fill out data field and NXdata class
        if anot_key == '1':
            indivisual_DATA_field()
            fill_out_NXdata_group('signal')
        # To fill out data field as many as we have
        else:
            indivisual_DATA_field()
            fill_out_NXdata_group()


def from_dat_file_into_template(template, dat_file, config_dict):
    """Pass metadata, current and voltage into template from file
    with dat extension.
    """

    b_s_d = BiasSpecData(dat_file)
    flattened_dict = {}
    nested_path_to_slash_separated_path(
        b_s_d.get_data_nested_dict(),
        flattened_dict=flattened_dict)
    for c_key, c_val in config_dict.items():
        for t_key, _ in template.copy.items():
            if c_key == t_key and isinstance(c_val, str):
                template[t_key] = flattened_dict[c_val]
                continue
            if c_key == t_key and isinstance(c_val, dict):
                data_group = "/ENTRY[entry]/data"
                if data_group == t_key:
                    # pass data processing here
                    construct_nxdata(template, flattened_dict, c_val, data_group)
                else:
                    # pass other physical propertise
                    pass


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
        has_sxm_input_file = False
        sxm_file: str = ""
        has_dat_input_file = False
        dat_file: str = ""
        # TODO: remove clean_template and add there template that comes as a function
        # parameter
        filled_template: Union[Dict, None] = None
        template = Template()
        config_dict: Union[Dict, None] = None

        for file in file_paths:
            ext = file.rsplit('.', 1)[-1]

            if ext == 'sxm' and not has_dat_input_file:
                has_sxm_input_file = True
                dat_file = file
            if ext == 'dat' and not has_sxm_input_file:
                sxm_file = file
                filled_template = template
            if ext == 'json':
                with open(file, mode="r", encoding="utf-8") as jf:
                    config_dict = json.load(jf)
        if not has_dat_input_file and not has_sxm_input_file:
            raise ValueError("Not correct file has been found. please render correct input"
                             " file of spm with extension: .dat or .sxm")
        if has_dat_input_file and has_sxm_input_file:
            raise ValueError("Only one file from .dat or .sxm can be read.")
        if has_sxm_input_file and config_dict:
            filled_template = from_sxm_into_template(template, sxm_file, config_dict)
        if has_dat_input_file and config_dict:
            from_dat_file_into_template(template, file, config_dict)



        if filled_template is not None:
            return filled_template
        else:
            raise ValueError("Reader could not read anything! Check for input files and the"
                             " corresponding extention.")


READER = STMReader
