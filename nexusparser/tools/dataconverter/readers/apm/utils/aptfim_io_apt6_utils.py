#!/usr/bin/env python3
"""AMETEK APT(6) data exchange file reader used by atom probe microscopists."""

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

# pylint: disable=E1101


import numpy as np


def np_uint16_to_string(uint16_array: np.ndarray) -> str:
    """Create string from array of uint16 numbers (UTF-16)."""
    str_parsed = ''
    for value in uint16_array:
        if value != 0:  # '\x00'
            str_parsed += chr(value)
    return np.str(str_parsed)


def string_to_typed_nparray(string: str, length: int,
                            dtype: np.dtype = np.uint8) -> np.ndarray:
    """Create fixed length np.uint16 numpy array from string."""
    assert dtype is not None, 'dtype must not be None!'
    assert len(string) <= length, 'Input string is longer than \
                                  number of array elements !'
    nparray = np.zeros(length, dtype)
    for value in np.arange(0, len(string)):
        nparray[value] = ord(string[value])
    return nparray
