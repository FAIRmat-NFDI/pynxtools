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
"""Helper functions for reading sections from Lake Shore files"""
import re


def is_section(expr: str) -> bool:
    """Checks whether an expression follows the form of a section
    i.e. is of the form [section]

    Args:
        expr (str): The current expression to check

    Returns:
        bool: Returns true if the expr is of the form of a section
    """
    return bool(re.search(r"^\[.+\]$", expr))


def is_measurement(expr):
    """Checks whether an expression follows the form of a measurement indicator
    i.e. is of the form <measurement>

    Args:
        expr (str): The current expression to check

    Returns:
        bool: Returns true if the expr is of the form of a measurement indicator
    """
    return bool(re.search(r"^\<.+\>$", expr))


def is_key(expr: str) -> bool:
    """Checks whether an expression follows the form of a key value pair
    i.e. is of the form key: value or key = value

    Args:
        expr (str): The current expression to check

    Returns:
        bool: Returns true if the expr is of the form of a key value pair
    """
    return bool(re.search(r"^.+\s*[:|=]\s*.+$", expr))


def is_meas_header(expr: str) -> bool:
    """Checks whether an expression follows the form of a measurement header,
    i.e. starts with: Word [Unit]

    Args:
        expr (str): The current expression to check

    Returns:
        bool: Returns true if the expr is of the form of a measurement header
    """
    return bool(re.search(r"^[^\]]+\[[^\]]+\]", expr))


def get_unique_dkey(dic: dict, dkey: str) -> str:
    """Checks whether a data key is already contained in a dictionary
    and returns a unique key if it is not.

    Args:
        dic (dict): The dictionary to check for keys
        dkey (str): The data key which shall be written.

    Returns:
        str: A unique data key. If a key already exists it is appended with a number
    """
    suffix = 0
    while f"{dkey}{suffix}" in dic:
        suffix += 1

    return f"{dkey}{suffix}"
