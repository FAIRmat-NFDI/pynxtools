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
                                        flattened_dict: dict=None,
                                        parent_path='') -> dict:
    """Convert nested dict into slash separeted path upto certain level.
    """
    start = '/'

    for key, val in nested_dict.items():
        path = parent_path + start + key
        if isinstance(val, dict):
            nested_path_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def cal_dx_by_dy(x_val: np.ndarray, y_val:np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calc conductance dx/dy for x-variable and y-variable also return.
    """
    dI = x_val[0::2] - y_val[1::2]
    dV = x_val[0::2] - y_val[1::2]

    dI_by_dV = dI / dV

    return dI_by_dV, x_val[1:]


def cal_X_multi_Y(x_val: np.ndarray, y_val: np.ndarray) -> np.ndarray:
    """Return multiplication of two array
    """
    return x_val * y_val
