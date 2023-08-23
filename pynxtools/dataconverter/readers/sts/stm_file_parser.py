"""
    A parser for files from stm experiment into a simple dict.
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
from typing import Any, Dict
import logging
import re
import numpy as np
import nanonispy as nap

from pynxtools.dataconverter.readers.sts.helper import (nested_path_to_slash_separated_path,
                                                        to_intended_t, fill_template_from_eln_data,
                                                        work_out_overwriteable_field,
                                                        link_seperation_from_hard_code,
                                                        UNIT_TO_SKIP)


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def has_separator_char(key, sep_char_li):
    """
    Check string or key whether the separator char provided in
    'Separator Char List' exist or not.
    """
    bool_k = [x in sep_char_li for x in key]
    return np.any(bool_k)


# pylint: disable=invalid-name
class STM_Nanonis():
    """Specific class for stm reader from nanonis company.

    """

    def __init__(self, file_name):
        """Construct
        """

        self.file_name = file_name

    def get_nested_dict_from_concatenated_key(self, data_dict, dict_to_map_path=None,
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
            if has_separator_char(d_key, sep_chars):
                # Find out which separator char exist there
                for k_c in d_key:
                    if k_c in sep_chars:
                        sep_char = k_c
                        break
                l_key, r_key = d_key.split(sep_char, 1)
                if not has_separator_char(r_key, sep_chars):
                    if l_key not in spreaded_dict:
                        spreaded_dict[l_key]: Dict[str, Any] = {}
                    spreaded_dict[l_key][r_key] = d_val
                else:
                    if l_key in spreaded_dict:
                        spreaded_dict[l_key] = self.get_nested_dict_from_concatenated_key(
                            {r_key: d_val}, dict_to_map_path=spreaded_dict[l_key])
                    else:
                        spreaded_dict[l_key]: Dict[str, Any] = {}
                        spreaded_dict[l_key] = self.get_nested_dict_from_concatenated_key(
                            {r_key: d_val}, dict_to_map_path=spreaded_dict[l_key])
            else:
                spreaded_dict[d_key] = d_val

        return spreaded_dict

    def convert_key_to_unit_and_entity(self, key, val, start_bracket='', end_bracket=''):
        """
        Split key into 'key' and 'key/@units' if key is designed as somthing like this 'key(A)'.
        """
        if start_bracket and end_bracket:
            if start_bracket in key and end_bracket in key:
                tmp_l_part, tmp_r_part = key.rsplit(start_bracket)
                unit = tmp_r_part.rsplit(end_bracket)[0]
                full_key = tmp_l_part.strip()
                if unit in UNIT_TO_SKIP:
                    unit = ''
                return [(full_key, val), (f"{full_key}/@unit", unit)]

            # In case if value contain name and unit e.g. /.../demodulated_signal: 'current(A)'
            if start_bracket in val and end_bracket in val:
                unit_parts = val.rsplit(start_bracket)
                # Assume that val does not have any key but decriptive text,
                # e.g. Current (A);Bias (V);
                if len(unit_parts) > 2:
                    return [(key, val)]
                tmp_l_part, tmp_r_part = unit_parts
                unit = tmp_r_part.rsplit(end_bracket)[0]
                val = tmp_l_part.strip()
                if unit in UNIT_TO_SKIP:
                    unit = ''
                return [(key, val), (f"{key}/@unit", unit)]

        return []

    def get_sxm_raw_metadata_and_signal(self, file_name):
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

    def get_SPM_metadata_dict_and_signal(self):
        """
        Get meradata and signal from spm file.
        """
        metadata_dict, signal = self.get_sxm_raw_metadata_and_signal(self.file_name)
        nesteded_matadata_dict = self.get_nested_dict_from_concatenated_key(metadata_dict)
        # Convert nested (dict) path to signal into slash_separated path to signal
        temp_flattened_dict_sig = {}
        nested_path_to_slash_separated_path(signal,
                                            temp_flattened_dict_sig)
        temp_flattened_dict = {}
        nested_path_to_slash_separated_path(nesteded_matadata_dict,
                                            temp_flattened_dict)
        flattened_dict = {}
        for key, val in temp_flattened_dict.items():
            # list of tuples of (data path, data) and (unit path/unit and unit value)
            tuple_li = self.convert_key_to_unit_and_entity(key, val,
                                                           start_bracket='(',
                                                           end_bracket=')')
            if tuple_li:
                for tup in tuple_li:
                    flattened_dict[tup[0]] = tup[1]
            else:
                flattened_dict[key] = val

        flattened_dict.update(temp_flattened_dict_sig)
        return flattened_dict

    # pylint: disable=too-many-arguments
    def construct_nxdata_for_sxm(self,
                                 template,
                                 data_dict,
                                 sub_config_dict,
                                 coor_info,
                                 data_group):
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
        coor_info: Tuple[list]
            Tuple (for X and Y coordinate respectively) of list  and each list starting and
            end point of x-axis.

        data_group : NeXus path for NXdata

        Return:
        -------
        None

        Raise:
        ------
        None
        """
        # pylint: disable=global-variable-undefined
        def indivisual_DATA_field():
            """Fill up template's indivisual data field and the descendant attribute.
                e.g. /Entry[ENTRY]/data/DATA,
                /Entry[ENTRY]/data/DATA/@axes and so on
            """
            # To define a variable on global namespace
            global nxdata_grp, field_name
            # list of paths e.g. "/LI_Demod_2_X/forward" comes provided file .sxm.
            for path in dt_path_list:
                if path in data_dict:
                    grp_name, field_name = find_nxdata_group_and_name(path)
                    grp_name = '_'.join(grp_name.lower().split(' '))
                    signals.append(field_name)
                    nxdata_grp = data_group.replace("DATA[data", f"DATA[{grp_name}")
                    temp_data_field = nxdata_grp + '/' + field_name
                    scan_dt_arr = to_intended_t(data_dict[path])
                    x_cor_len, y_cor_len = scan_dt_arr.shape
                    # collect for only one data field e.g. forward or backward, as all the data
                    # fields must have the same length of co-ordinate
                    if not axes_data:
                        # coor_info[i] has start, end and unit
                        axes_data.append(np.linspace(*coor_info[0][0:2], x_cor_len))
                        axes_data.append(np.linspace(*coor_info[1][0:2], y_cor_len))
                    axes_units.append(coor_info[0][2])
                    template[temp_data_field] = scan_dt_arr
                else:
                    # to clean up nxdata_grp and field_name from previous loop
                    nxdata_grp = ''
                    field_name = ''

        def fill_out_NXdata_group():
            """To fill out NXdata which is root for all data fields and attributes for NXdata.
            This function fills template with first level of descendent fields and attributes
            of NXdata but not the fields and attributes under child of NXdata.
            """
            if nxdata_grp:
                auxiliary_signals_attr = f"{nxdata_grp}/@auxiliary_signals"
                axes = f"{nxdata_grp}/@axes"
                signal_attr = f"{nxdata_grp}/@signal"
                template[auxiliary_signals_attr] = []
                template[axes] = axes_name
                for ind, data_field_nm in enumerate(signals):

                    if ind == 0:
                        template[signal_attr] = data_field_nm
                    else:
                        template[auxiliary_signals_attr].append(data_field_nm)
                for axis, axis_data in zip(axes_name, axes_data):
                    template[f"{nxdata_grp}/{axis}"] = axis_data

        def find_nxdata_group_and_name(key):
            """Find data group name from a data path in file.
            E.g. 'Z', 'LI_Demod_2_X' from /Z/forward and /LI_Demod_2_X/forward
            Note: Create a function in stm_helper.py to unit scale such as nm, micrometer
            """
            tmp_key = key.split('/', 1)[1]
            grp_name, data_field_name = tmp_key.split('/', 1)
            grp_name = grp_name.upper()
            return grp_name, data_field_name

        for _, dt_path_list in sub_config_dict.items():
            signals = []
            axes_name = ['x', 'y']
            axes_units = []
            axes_data = []
            # The following functions can be thought as unpacked function body here.
            if not dt_path_list:
                continue
            indivisual_DATA_field()
            fill_out_NXdata_group()

    # pylint: disable=too-many-locals
    def get_dimension_info(self, config_dict, data_dict):
        """
        Extract dimension info from scanfield.

            ../ENVIRONMENT[environment]/scan_control/positioner/scanfield"
            The scanfield has four parts starting point of (x, y) co-ordinate
            length on (x, y)-dimenstion and one last unknown values.
        """
        scanfield: str = ''
        for key, val in config_dict.items():
            if ("/ENTRY[entry]/INSTRUMENT[instrument]/ENVIRONMENT[environment]/"
                    "scan_control/positioner/scanfield") == key:
                if val in data_dict:
                    scanfield = data_dict[val]
                else:
                    raise ValueError("Scanfield data missing: /ENTRY[entry]/INSTRUMENT[instrument]"
                                     "/ENVIRONMENT[environment]/scan_control/positioner/scanfield")
        conf_unit_key = 'unit_of_x_y_coordinate'
        try:
            unit_info = data_dict[config_dict[conf_unit_key]]
        except KeyError as exc:
            raise KeyError(f'No info found about coordinate unit. check config file by'
                           f'key {conf_unit_key}') from exc
        for sep in [";"]:
            if sep in scanfield:
                # parts are X_cor, Y_cor, X_len, Y_len and one unkown value
                scanfield_parts = scanfield.split(sep)

                x_start = to_intended_t(scanfield_parts[0])
                x_len = to_intended_t(scanfield_parts[2])
                x_cor = [x_start, x_start + x_len, unit_info]
                y_start = to_intended_t(scanfield_parts[1])
                y_len = to_intended_t(scanfield_parts[3])
                y_cor = [y_start, y_start + y_len, unit_info]
                return (x_cor, y_cor)
        return ()

    # pylint: disable=too-many-branches
    def from_sxm_file_into_template(self, template, config_dict, eln_data_dict):
        """
        Pass metadata and signals into template. This should be last steps for writting
        metadata and data into nexus template.
        """

        nxdl_key_to_modified_key: dict = {}
        data_dict = self.get_SPM_metadata_dict_and_signal()

        fill_template_from_eln_data(eln_data_dict, template)
        # Fill out template from config file
        temp_keys = template.keys()
        for c_key, c_val in config_dict.items():
            if c_val in ['None', ""] or c_key[0] != '/':
                continue
            if c_key in temp_keys:
                if isinstance(c_val, str):
                    if c_val in data_dict:
                        template[c_key] = to_intended_t(data_dict[c_val])
                # Handling multiple possible raw data according to user's defined name.
                if isinstance(c_val, list):
                    for search_key in c_val:
                        if search_key in data_dict:
                            template[c_key] = to_intended_t(data_dict[search_key])
                if isinstance(c_val, dict):
                    data_group = "/ENTRY[entry]/DATA[data]"
                    if c_key == data_group:
                        coor_info = self.get_dimension_info(config_dict, data_dict)
                        self.construct_nxdata_for_sxm(template,
                                                      data_dict,
                                                      c_val,
                                                      coor_info,
                                                      data_group)
                    else:
                        work_out_overwriteable_field(template,
                                                     data_dict,
                                                     c_val,
                                                     c_key,
                                                     nxdl_key_to_modified_key)
            else:
                if isinstance(c_val, dict):
                    work_out_overwriteable_field(template,
                                                 data_dict,
                                                 c_val,
                                                 c_key,
                                                 nxdl_key_to_modified_key)
                else:
                    template[c_key] = to_intended_t(data_dict[c_val]) if c_val in data_dict \
                        else None
        # The following function can be used later it link come true in application def.
        # link_implementation(template, nxdl_key_to_modified_key)
        link_seperation_from_hard_code(template, nxdl_key_to_modified_key)


def get_stm_raw_file_info(raw_file):
    """Parse the raw_file into a organised dictionary. It helps users as well as developers
    to understand how the reader works and modify the config file."""

    raw_file = os.path.basename(raw_file)
    raw_name = raw_file.rsplit('.')[0]
    data_dict = STM_Nanonis(raw_file).get_SPM_metadata_dict_and_signal()
    temp_file = f"{raw_name}.txt"
    with open(temp_file, mode='w', encoding='utf-8') as txt_f:
        for key, val in data_dict.items():
            txt_f.write(f"{key} : {val}\n")
    logging.info(' %s has been created to investigate raw data structure.', temp_file)
