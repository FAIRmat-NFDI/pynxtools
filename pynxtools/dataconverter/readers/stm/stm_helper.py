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
import numpy as np


def nested_path_to_slash_separated_path(nested_dict: dict,
                                        flattened_dict: dict,
                                        parent_path=''):
    """Convert nested dict into slash separeted path upto certain level.
    """
    start = '/'

    for key, val in nested_dict.items():
        path = parent_path + start + key
        if isinstance(val, dict):
            nested_path_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def cal_dx_by_dy(x_val: np.ndarray, y_val: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calc conductance or gradiant dx/dy for x-variable and y-variable also return the result.
    """
    dx = x_val[0::2] - x_val[1::2]
    dy = y_val[0::2] - y_val[1::2]

    dx_by_dy = dx / dy

    return dx_by_dy


def cal_X_multi_Y(x_val: np.ndarray, y_val: np.ndarray) -> np.ndarray:
    """Return multiplication of two array
    """
    return x_val * y_val


def slice_before_last_element(np_array):
    """Get all the elements before last element.
    """
    if isinstance(np_array, np.ndarray) and len(np.shape(np_array)) == 1:
        return np_array[:-1]
    else:
        raise ValueError('Please provide a numpy array of 1D.')


def transform(text):
    """
        Transform string to the intended data type, if not then return text.
    e.g '2.5E-2' will be transfor into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'], None]
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32], None
    """
    symbol_list_for_data_seperation = [';']
    transformed = ""
    if text is None:
        return text
    if isinstance(text, list):
        text = list(text)
        try:

            transformed = np.array(text, dtype=np.float64)
            return transformed
        except ValueError:
            pass

    try:
        transformed = int(text)
        return transformed
    except ValueError:
        pass

    try:
        transformed = float(text)
        return transformed
    except ValueError:
        pass

    for sym in symbol_list_for_data_seperation:
        if sym in text:
            parts = text.split(sym)
            modified_parts = []
            for part in parts:
                modified_parts.append(transform(part))
            return modified_parts

    return text
