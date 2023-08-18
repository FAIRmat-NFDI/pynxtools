"""
    Some generic function and class for on STM reader.
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

from typing import Tuple
import json
import numpy as np
from pynxtools.dataconverter.helpers import convert_data_dict_path_to_hdf5_path


# Here are some data or data type or unit or data to skip:
UNIT_TO_SKIP = ['on/off', 'off', 'on', 'off/on']


def fill_template_from_eln_data(eln_data_dict, template):
    """Fill out the template from dict that generated from eln yaml file.
    Parameters:
    -----------
    eln_data_dict : dict[str, Any]
        Python dictionary from eln file.
    template : dict[str, Any]
    Return:
    -------
    None
    """

    for e_key, e_val in eln_data_dict.items():
        template[e_key] = to_intended_t(e_val)


def work_out_overwriteable_field(template, data_dict,
                                 sub_config_dict, nexus_path,
                                 dict_orig_key_to_mod_key):
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
    field_path : NeXus field full path

    Returns:
    --------
    None
    """
    # Find the overwriteable part
    overwrite_part = ""
    field_to_replace = ""
    # Two possibilities are considered: tilt_N/@units and tilt_N
    if '/@units' in nexus_path:
        field_to_replace = nexus_path.rsplit('/', 2)[-2]
    else:
        field_to_replace = nexus_path.rsplit('/', 1)[-1]
    for char in field_to_replace:
        if char.isupper():
            overwrite_part = overwrite_part + char

    if not overwrite_part and not field_to_replace and isinstance(sub_config_dict, dict):
        raise ValueError(f"No overwriteable part has been found but data structure "
                         f": {sub_config_dict} intended to overeritten.")
    # sub_config_dict contains key that repalce the overwritable (upper case part)
    # part from nexus path
    for ch_to_replace, data_path in sub_config_dict.items():
        modified_field = field_to_replace.replace(overwrite_part, ch_to_replace)
        # Considering renamed field
        new_temp_key = nexus_path.replace(field_to_replace, f"{field_to_replace}[{modified_field}]")
        value = "value"
        unit = "unit"
        dict_orig_key_to_mod_key[nexus_path] = new_temp_key
        if value in data_path:
            path_to_data = data_path[value]
            template[new_temp_key] = to_intended_t(data_dict[path_to_data]
                                                   if path_to_data in data_dict else None)
        if unit in data_path:
            path_to_data = data_path[unit]
            template[new_temp_key + "/@units"] = to_intended_t(data_dict[path_to_data]
                                                               if path_to_data in data_dict
                                                               else None)


def nested_path_to_slash_separated_path(nested_dict: dict,
                                        flattened_dict: dict,
                                        parent_path=''):
    """Convert nested dict into slash separeted path upto certain level."""
    start = '/'

    for key, val in nested_dict.items():
        path = parent_path + start + key
        if isinstance(val, dict):
            nested_path_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def link_implementation(template, link_modified_dict):
    """Rewrite the link compatible with hdf5 full path.
    for e.g. convert /ENTRY[entry]/INSTRUMENT[instrument]/name to
    /entry/instrument/name and rewrite in template.

    Parameters
    ----------
    template : Template (dict)
        To write out the hdf file
    link_modified_dict : dict
        The key corresponds to nxdl def path e.g. /ENTRY[entry]/INSTRUMENT[instrument]/NAME
        and the value is the modified link path e.g.
        /ENTRY[entry]/INSTRUMENT[special_instrument]/given_name where the
        value is according to the implementaion of the NeXus def.
    """
    for _, val in template.items():
        if isinstance(val, dict) and 'link' in val:
            orig_link_path = val['link']
            # Check whether any concept has been rewriten stored in key value
            if orig_link_path in link_modified_dict:
                # modified concepts come in a list together.
                modif_link_hdf_path = convert_data_dict_path_to_hdf5_path(
                    link_modified_dict[orig_link_path])
                val['link'] = modif_link_hdf_path
            else:
                val['link'] = convert_data_dict_path_to_hdf5_path(orig_link_path)


def cal_dx_by_dy(x_val: np.ndarray, y_val: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calc conductance or gradiant dx/dy for x-variable and y-variable also return the result."""
    dx_ = x_val[0::2] - x_val[1::2]
    dy_ = y_val[0::2] - y_val[1::2]

    dx_by_dy = dx_ / dy_

    return dx_by_dy


def cal_x_multi_x(x_val: np.ndarray, y_val: np.ndarray) -> np.ndarray:
    """Return multiplication of two array
    """
    return x_val * y_val


def slice_before_last_element(np_array):
    """Get all the elements before last element.
    """
    if not isinstance(np_array, np.ndarray) and not len(np.shape(np_array)) == 1:
        raise ValueError('Please provide a numpy array of 1D.')
    return np_array[:-1]


# pylint: disable=too-many-return-statements
def to_intended_t(str_value):
    """
        Transform string to the intended data type, if not then return str_value.
    e.g '2.5E-2' will be transfor into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'], None
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32], None

    Parameters
    ----------
    str_value : _type_
        _description_

    Returns
    -------
    Union[str, int, float, np.ndarray]
        Converted data type
    """
    symbol_list_for_data_seperation = [';']
    transformed = ""
    if str_value is None:
        return str_value

    if isinstance(str_value, list):
        str_value = list(str_value)
        try:
            transformed = np.array(str_value, dtype=np.float64)
            return transformed
        except ValueError:
            pass

    if isinstance(str_value, np.ndarray):
        return str_value
    if isinstance(str_value, str):
        try:
            transformed = int(str_value)
            return transformed
        except ValueError:
            try:
                transformed = float(str_value)
                return transformed
            except ValueError:
                if '[' in str_value and ']' in str_value:
                    transformed = json.loads(str_value)
                    return transformed

        for sym in symbol_list_for_data_seperation:
            if sym in str_value:
                parts = str_value.split(sym)
                modified_parts = []
                for part in parts:
                    modified_parts.append(to_intended_t(part))
                return modified_parts

    return str_value
