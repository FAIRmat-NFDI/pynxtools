#!/usr/bin/env python3
"""
    To collect data from Bias Spectroscopy output file that is mainly a file with dat extension.
"""
# -*- coding: utf-8 -*-
#
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


from typing import Dict, Union, TextIO
import os
import numpy as np
from pynxtools.dataconverter.readers.stm.stm_helper import (nested_path_to_slash_separated_path,
                                                            transform, cal_dx_by_dy)


# Type aliases
NestedDict = Dict[str, Union[int, str, 'NestedDict']]


class BiasSpecData():
    """This class mainly collect and store data fo Bias spectroscopy that is SPM experiment.
       The class splits the data and store in into nested python dictionary as follows.
       E.g.
        bais_data = {data_field_name:{value: value_for_data_field_of_any_data_typeS,
                                      unit: unit name,
                                      date: ---,
                                      time: ---}
                    }

    """
    def __init__(self, file_name: str) -> None:
        """Innitialize object level variables.
        """
        # TODO: If get some information about nachines or vendors which makes the data file
        # distinguished collecte them.
        self.bias_spect_dict: NestedDict = {}
        self.raw_file: str = file_name
        # self.file_obj: TextIO = None
        self.choose_correct_function_to_extract_data()

    def get_data_nested_dict(self) -> NestedDict:
        """Retrun nested dict as bellow
        bais_data = {data_field_name:{value: value_for_data_field_of_any_data_typeS,
                                      unit: unit name,
                                      date: ---,
                                      time: ---}
                    }
        """
        return self.bias_spect_dict

    def extract_and_store_from_dat_file(self) -> None:
        """Extract data from data file and store them into object level nested dictionary.
        """

        key_seperators = ['>', '\t']
        unit_separators = [' (']
        is_matrix_data_found = False
        one_d_numpy_array = np.empty(0)

        def check_and_write_unit(dct, key_or_line, value=None):
            for sep_unit in unit_separators:
                if sep_unit in key_or_line:
                    key, unit = key_or_line.split(sep_unit, 1)
                    unit = unit.split(')')[0]
                    if key_or_line in dct:
                        del dct[key_or_line]
                    if isinstance(value, dict):
                        value['unit'] = unit
                    else:
                        value: NestedDict = {}
                        value['unit'] = unit
                    dct[key] = value
                    break

        def check_metadata_and_unit(key_and_unit):
            metadata = ''
            key, unit = key_and_unit.split('(')
            unit, rest = unit.split(')', 1)
            # Some units have extra info e.g. Current (A) [filt]
            if '[' in rest:
                metadata = rest.split('[')[-1].split(']')[0]
            return key, unit, metadata

        # TODO convert it into static mathod
        def retrive_key_recursively(line_to_analyse: str,
                                    dict_to_store: NestedDict) -> None:

            line_to_analyse = line_to_analyse.strip()
            for k_sep in key_seperators:
                if k_sep in line_to_analyse:
                    key, rest = line_to_analyse.split(k_sep, 1)
                    key = key.strip()
                    if key in dict_to_store:
                        new_dict = dict_to_store[key]
                    else:
                        new_dict: NestedDict = {}
                    dict_to_store[key] = new_dict
                    # check if key contains any unit inside bracket '()'
                    check_and_write_unit(dict_to_store, key, new_dict)
                    retrive_key_recursively(rest, new_dict)
                    return

            for sep_unit in unit_separators:
                if sep_unit in line_to_analyse:
                    check_and_write_unit(dict_to_store, line_to_analyse)
                    return

            dict_to_store['value'] = line_to_analyse.strip()
            return

        def check_matrix_data_block_has_started(line_to_analyse):
            wd_list = line_to_analyse.split()
            int_list = []
            if not wd_list:
                return False, []
            for word in wd_list:
                try:
                    float_n = float(word)
                    int_list.append(float_n)
                except ValueError:
                    return False, []
            return True, int_list

        def dismentle_matrix_into_dict_key_value_list(column_string,
                                                      one_d_np_array,
                                                      dict_to_store):
            column_keys = column_string.split('\t')
            np_2d_array = one_d_np_array.reshape(-1, len(column_keys))
            dat_mat_comp = 'dat_mat_components'
            dict_to_store[dat_mat_comp] = {}
            for ind, key_and_unit in enumerate(column_keys):
                if '(' in key_and_unit:
                    key, unit, data_stage = check_metadata_and_unit(key_and_unit)
                    # data_stage could be 'filt' or something like this
                    if data_stage:
                        dict_to_store[dat_mat_comp][f"{key.strip()} [{data_stage}]"] = \
                                                            {'unit': unit,
                                                             'value': np_2d_array[:, ind],
                                                             'metadata': data_stage}
                    else:
                        dict_to_store[dat_mat_comp][key.strip()] = {'unit': unit,
                                                      'value': np_2d_array[:, ind]}
                else:
                    dict_to_store[dat_mat_comp][key.strip()] = {'value': list(np_2d_array[:, ind])}

        # TODO: write here the algorithm for reading each line
        with open(self.raw_file, mode='r', encoding='utf-8') as file_obj:
            lines = file_obj.readlines()
            # last two lines for getting matrix data block that comes at the end of the file
            last_line: str
            for ind, line in enumerate(lines):
                if ind == 0:
                    last_line = line
                    continue
                is_mat_data, data_list = check_matrix_data_block_has_started(line)
                if is_mat_data:
                    is_matrix_data_found = True
                    one_d_numpy_array = np.append(one_d_numpy_array, data_list)
                    is_mat_data = False
                # Map matrix data if file has at least two empty lines or starts
                # other data or metadata except matrix data
                elif (not is_mat_data) and is_matrix_data_found:
                    is_matrix_data_found = False
                    dismentle_matrix_into_dict_key_value_list(last_line, one_d_numpy_array, self.bias_spect_dict)
                    last_line = line
                else:
                    retrive_key_recursively(last_line, self.bias_spect_dict)
                    last_line = line

            if (not is_mat_data) and is_matrix_data_found:
                is_matrix_data_found = False
                dismentle_matrix_into_dict_key_value_list(last_line, one_d_numpy_array, self.bias_spect_dict)

    def choose_correct_function_to_extract_data(self) -> None:
        """Choose correct function to extract data that data in organised format.
        """
        if not os.path.isfile(self.raw_file):
            raise ValueError("Provide correct file.")

        ext = self.raw_file.rsplit('.', 1)[-1]
        if ext == 'dat':
            self.extract_and_store_from_dat_file()


def collect_default_value(template, search_key):
    default_dict = {"/ENTRY[entry]/definition": "NXiv_sweep2",
                    "/ENTRY[entry]/experiment_description": "An stm experiment."}
    template[search_key] = default_dict[search_key]


def construct_nxdata_for_dat(template, data_dict, data_config_dict, data_group):
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
        # NOTE : Try to replace this hard axes name
        # TODO: Try to include re module to check similar pattern for data fields
        # These are possible axes and nxdata fields
        axes = ["Bias/",]
        data_fields = ["Current/",
                    # "Temperature 1/",
                       "LI Demod 1 X/",
                       "LI Demod 2 X/",
                       "LI Demod 1 Y/",
                       "LI Demod 2 Y/"]

        global extra_annot
        # Bellow we are collecting: axes, and data field info.
        # list of paths e.g. "/dat_mat_components/Bias/value" comes from
        # dict value of /ENTRY[entry]/DATA[data] in config file.
        for path in dt_val:
            # Extra annot could be 'filt'
            extra_annot, trimed_path = find_extra_annot(path)
            for axis in axes:
                if (axis + 'value') in trimed_path:
                    # removing forward slash
                    axes_name.append(axis[0:-1])
                    axes_data.append(data_dict[path])
                if (axis + 'unit') in trimed_path:
                    axes_unit.append(data_dict[path] if path in data_dict else "")
                if (axis + "metadata") in trimed_path:
                    axes_metadata.append(data_dict[path] if path in data_dict else "")
            for possible_field in data_fields:
                if possible_field + 'value' in trimed_path and path in data_dict:
                    data_field_dt.append(data_dict[path])
                    data_field_nm.append(possible_field[0:-1])
                    data_field_unit.append(get_unit(path, data_dict))

        # Note: this value must come from ELN
        # Note try to create link for axes
        flip_number = -1
        global temp_data_grp
        for dt_fd, dat_, unit in zip(data_field_nm, data_field_dt, data_field_unit):
            if extra_annot:
                temp_data_grp = data_group.replace("DATA[data", f"DATA[{dt_fd}({extra_annot})")
            else:
                temp_data_grp = data_group.replace("DATA[data", f"DATA[{dt_fd}")
            template[temp_data_grp + '/@signal'] = dt_fd
            template[temp_data_grp + '/@axes'] = axes_name
            # template[temp_data_grp + '/title'] =
            data_field = temp_data_grp + '/' + dt_fd
            if "LI Demod" in dt_fd:
                template[data_field] = dat_ * flip_number
            else:
                template[data_field] = dat_  # cal_dx_by_dy(current, volt)

            for axis, data_, a_unit in zip(axes_name, axes_data, axes_unit):
                template[temp_data_grp + '/' + axis] = data_
                template[f"{temp_data_grp}/{axis}/@long_name"] = f"{axis}({a_unit})"
                template[f"{temp_data_grp}/@{axis}_indices"] = 0
            if unit:
                template[data_field + '/@long_name'] = f"{dt_fd} ({unit})"
            else:
                template[data_field + '/@long_name'] = dt_fd

    def get_unit(value_key, data_dict):
        # value_key: /dat_mat_components/LI Demod 1 X/value
        # unit_key: /dat_mat_components/LI Demod 1 X/unit
        unit_key = value_key.replace('/value', '/unit')
        if unit_key in data_dict:
            return data_dict[unit_key]
        else:
            return ""

    def find_extra_annot(key):
        """Find out extra annotation that comes with data e.g. filt in
        /dat_mat_components/Current [filt]/value
        """
        annot_li = [' [filt]']
        for annot in annot_li:
            if annot in key:
                trimed_annot = annot[annot.index('[') + 1:-1]
                return trimed_annot, key.replace(annot, "")
        return "", key

    for dt_key, dt_val in data_config_dict.items():
        # The axes and data list will be field globaly and used inside other local functions
        axes_name = []
        axes_unit = []
        axes_metadata = []
        axes_data = []
        data_field_nm = []
        data_field_dt = []
        data_field_unit = []
        # There are several scan data gourp in the given file.
        if dt_key == '0':
            continue
        if dt_key == '1':
            indivisual_DATA_field()
        # To fill out data field as many as we have
        else:
            indivisual_DATA_field()


def from_dat_file_into_template(template, dat_file, config_dict):
    """Pass metadata, current and voltage into template from file
    with dat extension.
    """

    b_s_d = BiasSpecData(dat_file)
    flattened_dict = {}
    nested_path_to_slash_separated_path(
        b_s_d.get_data_nested_dict(),
        flattened_dict=flattened_dict)
    # TODO: remove this block that has been wrtteing to dev purpose
    temp_file = 'dat_data.txt'
    with open(temp_file, encoding='utf-8', mode='w') as dat_f:
        for key, val in flattened_dict.items():
            dat_f.write(f"{key} : {val}\n")

    # TODO: remove upto here
    template_keys = template.keys()
    for c_key, c_val in config_dict.items():
        for t_key in template_keys:
            # debug
            if c_val in ["None", ""]:
                continue
            if "@reader" in c_val and c_key == t_key:
                collect_default_value(template, c_key)
                break
            if c_key == t_key and isinstance(c_val, str):
                template[t_key] = transform(flattened_dict[c_val])
                break
            if c_key == t_key and isinstance(c_val, dict):
                data_group = "/ENTRY[entry]/DATA[data]"
                if data_group == t_key:
                    # pass exp. data section to NXdata group
                    construct_nxdata_for_dat(template, flattened_dict, c_val, data_group)
                else:
                    # pass other physical quantity that has muliple dimensions or type for
                    # same physical quantity e.g. in drift_N N will be replaced X, Y and Z
                    work_out_overwriteable_field(template, flattened_dict, c_val, t_key)
                break


def work_out_overwriteable_field(template, data_dict, data_config_dict, nexus_path):
    """
    Overwrite a field for multiple dimention of the same type of physical quantity.

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
    field_path : NeXus field path

    Returns:
    --------
    None
    """
    # TODO: Try here to use regrex module
    # Find the overwriteable part
    overwrite_part = ""
    # Two possibilities are considered: tilt_N/@units and tilt_N
    if '/@units' in nexus_path:
        field_to_replace = nexus_path.rsplit('/')[1]
    else:
        field_to_replace = nexus_path.rsplit('/', 1)[1]
    for char in field_to_replace:
        if char.isupper():
            overwrite_part = overwrite_part + char
    if overwrite_part == "":
        raise ValueError("No overwriteable part has been found.")
    for ch_to_subs, value_dict in data_config_dict.items():
        modified_field = field_to_replace.replace(overwrite_part, ch_to_subs)
        new_temp_key = nexus_path.replace(field_to_replace, modified_field)
        value = "value"
        unit = "unit"
        if value in value_dict:
            path_to_dt = value_dict[value]
            template[new_temp_key] = transform(data_dict[path_to_dt]
                                               if path_to_dt in data_dict else None)
        if unit in value_dict:
            path_to_dt = value_dict[unit]
            template[new_temp_key + "/@unit"] = transform(data_dict[path_to_dt]
                                                          if path_to_dt in data_dict
                                                          else None)


def process_data_from_file_(flattened_dict):
    """Implement this function later.
        TODO:
        This functions mainly intended for automization of data manipulation
         or data driven analytics. Try it out later.
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

