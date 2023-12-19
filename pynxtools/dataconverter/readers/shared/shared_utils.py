#!/usr/bin/env python3
"""Functionalities shared across different parsers."""

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

# pylint: disable=E1101, R0801

# import git
import hashlib


def get_repo_last_commit() -> str:
    """Identify the last commit to the repository."""
    # repo = git.Repo(search_parent_directories=True)
    # sha = str(repo.head.object.hexsha)
    # if sha != "":
    #    return sha
    # currently update-north-markus branch on nomad-FAIR does not pick up
    # git even though git in the base image and gitpython in pynxtools deps
    return "unknown git commit id or unable to parse git reverse head"


def get_sha256_of_file_content(file_hdl) -> str:
    """Compute a hashvalue of given file, here SHA256."""
    file_hdl.seek(0)
    # Read and update hash string value in blocks of 4K
    sha256_hash = hashlib.sha256()
    for byte_block in iter(lambda: file_hdl.read(4096), b""):
        sha256_hash.update(byte_block)
    return str(sha256_hash.hexdigest())


class NxObject:  # pylint: disable=R0903
    """An object in a graph e.g. a field or group in NeXus."""

    def __init__(self,
                 name: str = None,
                 unit: str = None,
                 dtype=str,
                 value=None,
                 **kwargs):
        if name is not None:
            assert name != "", "Argument name needs to be a non-empty string !"
        if unit is not None:
            assert unit != "", "Argument unit needs to be a non-empty string !"
        assert dtype is not None, "Argument dtype must not be None !"
        if dtype is not None:
            assert isinstance(dtype, type), \
                "Argument dtype needs a valid, ideally numpy, datatype !"
        # ##MK::if value is not None:
        self.is_a = "NXobject"
        self.is_attr = False  # if True indicates object is attribute
        self.doc = ""  # docstring
        self.name = name  # name of the field
        self.unit = unit  # not unit category but actual unit
        # use special values "unitless" for NX_UNITLESS (e.g. 1) and
        # "dimensionless" for NX_DIMENSIONLESS (e.g. 1m / 1m)
        self.dtype = dtype  # use np.dtype if possible
        if value is None or dtype is str:
            self.unit = "unitless"
        if value is not None:
            self.value = value
        else:
            self.value = None
        # value should be a numpy scalar, tensor, or string if possible
        if "is_attr" in kwargs:
            assert isinstance(kwargs["is_attr"], bool), \
                "Kwarg is_attr needs to be a boolean !"
            self.is_attr = kwargs["is_attr"]

    def print(self):
        """Report values."""
        print("name: ")
        print(str(self.name))
        print("unit:")
        print(str(self.unit))
        print("dtype: ")
        print(self.dtype)

# test = NxObject(name="test", unit="baud", dtype=np.uint32, value=32000)
# test.print()
