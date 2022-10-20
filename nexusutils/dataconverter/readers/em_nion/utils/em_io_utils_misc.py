#!/usr/bin/env python3
"""Generic utilities for the Nion/NionSwift EM parser."""

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

from typing import Tuple, Optional, Dict

import numpy as np

import h5py


def string_array_to_utf8(strings: list) -> np.ndarray:
    """Format a list of strings to a h5py compliant UTF-8 formatted array."""
    # https://manual.nexusformat.org/classes/base_classes/NXdata.html#nxdata
    # https://docs.h5py.org/en/stable/strings.html

    utf8_type = h5py.string_dtype('utf-8', 30)
    return np.array([s.encode("utf-8") for s in strings], utf8_type)


def recursive_query_nested_dict(path: str, dct: dict):
    """Traverse nested Python dict to find value to flattened path.

    The function left-strips the path with walking each layer deeper.
    """
    # prev_key: str,
    assert path not in ['', '/'], 'Path must not be empty or slash/root only!'
    # NEW ISSUE: eventually return None in the above cases
    idx = path.find('/')
    curr_key = path
    if idx != -1:
        curr_key = path[0:idx]
        remaining_path = path[idx + 1::]
        if curr_key[0] == "[" and curr_key[-1] == "]":
            # lst_id = int(curr_key[1:-1])
            # print('-->Traversing into list of dictionaries lst_id: '
            #       + str(lst_id) + ' using prev_key: ' + prev_key)
            return recursive_query_nested_dict(remaining_path, dct[int(curr_key[1:-1])])

        # print('-->Traversing dictionary key: '
        #       + curr_key + ' using prev_key: ' + prev_key)
        return recursive_query_nested_dict(
            remaining_path, dct[curr_key])  # curr_key,
    # print('-->Found leaf, key: '
    #       + curr_key + ' value: ' + str(dct[curr_key]))
    return dct[curr_key]


NIONSWIFT_FILE_TYPES = ['npy', 'json']
ELAB_FILE_TYPES = ['dat']
NION_ERROR_CODES = {-1: 'Invalid input', 0: 'Single Nion/NionSwift dataset'}


def assess_situation_with_input_files(file_paths: Optional[Tuple[str, ...]] = None):
    """Different file formats contain different types of data.

    Identify how many files of specific type Tuple contains to judge if the
    input has at all a chance to populate all required fields of
    the application definition.

    """
    file_paths = ('HAADF_01.json', 'HAADF_01.npy', 'HAADF_01.ELabFTW.dat')
    filetype_dict: Dict[str, list] = {}
    for file_name in file_paths:
        index = file_name.lower().rfind('.')
        if index >= 0:
            suffix = file_name.lower()[index + 1::]
            if suffix in NIONSWIFT_FILE_TYPES + ELAB_FILE_TYPES:
                if suffix in filetype_dict.keys():
                    filetype_dict[suffix].append(file_name)
                else:
                    filetype_dict[suffix] = [file_name]
        # files without endings are ignored

    # identify which use case we face
    filetype_counts = {}
    for suffix, filenames in filetype_dict.items():
        filetype_counts[suffix] = len(filenames)

    # decide what to do based on the use case
    if len(filetype_dict['npy']) == 1 and len(filetype_dict['json']) == 1 \
       and len(filetype_dict['dat']) == 1:
        return (filetype_dict, NION_ERROR_CODES[0])
    # ##MK \ and len(filetype_dict['yml']) == 1:

    return (filetype_dict, NION_ERROR_CODES[-1])
