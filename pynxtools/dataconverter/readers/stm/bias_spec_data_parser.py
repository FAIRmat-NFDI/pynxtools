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

# Type aliases
NestedDict = Dict[str, Union[int, 'NestedDict']]




class BiasSpectData():
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
        print('#ssss')
        self.choose_correct_function_to_extract_data()

    def get_data_nested_dict(self, file_name: str) -> NestedDict:
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

        key_seperators = ['>', '/']
        unit_separators = [' (']
        is_matrix_data_found = False
        one_d_numpy_array = np.empty(0)

        # TODO convert it into static mathod
        def retrive_key_recursively(line_to_analse,
                                    dict_to_store):

            line_to_analse = line_to_analse.strip()
            for k_sep in key_seperators:
                if k_sep in line_to_analse:
                    key, rest = line_to_analse.split(k_sep, 1)
                    key = key.strip()
                    if key in dict_to_store:
                        new_dict = dict_to_store[key]
                    else:
                        new_dict: NestedDict = {}
                    dict_to_store[key.strip()] = new_dict
                    retrive_key_recursively(rest, new_dict)
                    return
            for u_sep in unit_separators:
                if u_sep in line_to_analse:
                    unit, rest = line_to_analse.split(')', 1)
                    dict_to_store['unit'] = unit[1:].strip()
                    retrive_key_recursively(rest, dict_to_store)
                    return
            # check the line_to_analyse has reached to the end point
            dict_to_store['value'] = line_to_analse
            return

        def check_matrix_data_block_has_started(line_to_analyse):
            wd_list = line_to_analyse.split()
            int_list = []
            for word in wd_list:
                try:
                    float_n = float(word)
                    int_list.append(float_n)
                except ValueError:
                    return False, []
            return True, int_list

        def dismentle_matrix_into_dict_key_value(column_string, one_d_np_array, dict_to_store):
            column_keys = column_string.split()
            np_2d_array = one_d_np_array.reshape(-1, )
            for ind, key_and_unit in enumerate(column_keys):
                if '(' in key_and_unit:
                    key, unit = key_and_unit.split('(')
                    dict_to_store[key.strip()] = {'unit': unit[0:-1],
                                                  'value': list(np_2d_array[:, ind])}

        # TODO: write here the algorithm for reading each line
        with open(self.raw_file, 'r') as file_obj:
            lines = file_obj.readlines()
            # last two lines for getting matrix data block that comes at the end of the file
            last_line: str
            for ind, line in enumerate(lines):
                if ind == 0:
                    last_line = line
                    continue
                matrix_data, data_list = check_matrix_data_block_has_started(line)
                if matrix_data:
                    is_matrix_data_found = True
                    np.append(one_d_numpy_array, data_list)
                elif not matrix_data and is_matrix_data_found:
                    is_matrix_data_found = False
                    dismentle_matrix_into_dict_key_value(last_line, one_d_numpy_array, self.bias_spect_dict)
                    last_line = line
                else:
                    retrive_key_recursively(last_line, self.bias_spect_dict)
                    last_line = line

                last_line = line
                # check for

    def choose_correct_function_to_extract_data(self) -> None:
        """Choose correct function to extract data that data in organised format.
        """
        if not os.path.isfile(self.raw_file):
            raise ValueError("Provide correct file.")

        ext = self.raw_file.rsplit('.', 1)[-1]
        if ext == 'dat':
            self.extract_and_store_from_dat_file()

