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
"""Utility functions when working with parsing HDF5."""

import numpy as np
import os, glob, re, sys
import h5py
import yaml
import json


def read_strings_from_dataset(obj):
    # print(f"type {type(obj)}, np.shape {np.shape(obj)}, obj {obj}")
    # if hasattr(obj, "dtype"):
    #     print(obj.dtype)
    if isinstance(obj, np.ndarray):
        retval = []
        for entry in obj:
            if isinstance(entry, bytes):
                retval.append(entry.decode("utf-8"))
            elif isinstance(entry, str):
                retval.append(entry)
            else:
                continue
                # raise ValueError("Neither bytes nor str inside np.ndarray!")
        # specific implementation rule that all lists with a single string
        # will be returned in paraprobe as a scalar string
        if len(retval) > 1:
            return retval
        elif len(retval) == 1:
            return retval[0]
        else:
            return None
    elif isinstance(obj, bytes):
        return obj.decode("utf8")
    elif isinstance(obj, str):
        return obj
    else:
        return None
        # raise ValueError("Neither np.ndarray, nor bytes, nor str !")
