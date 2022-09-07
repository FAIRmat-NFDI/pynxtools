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
"""Utility functions for the NeXus reader classes."""
from typing import List, Any, Dict, Optional
from collections.abc import Mapping
import json
import yaml


def flatten_and_replace(
        dic: Mapping,
        convert_dict: dict,
        replace_nested: dict,
        parent_key: str = "/ENTRY[entry]",
        sep: str = "/"
) -> dict:
    """Flatten a nested dictionary, and replace the keys with the appropriate
    paths in the nxs file.

    Args:
        dic (dict): Dictionary to flatten
        convert_dict (dict): Dictionary for renaming keys in the flattend dict.
        replace_nested (dict): Dictionary for renaming nested keys.
        parent_key (str, optional):
            Parent key of the dictionary. Defaults to "/ENTRY[entry]".
        sep (str, optional): Separator for the keys. Defaults to "/".

    Returns:
        dict: Flattened dictionary
    """
    items: List[Any] = []
    for key, val in dic.items():
        new_key = parent_key + sep + convert_dict.get(key, key)
        if isinstance(val, Mapping):
            items.extend(
                flatten_and_replace(val, convert_dict, replace_nested, new_key, sep=sep)
                .items()
            )
        else:
            for old, new in replace_nested.items():
                new_key = new_key.replace(old, new)

            if new_key.endswith("/value"):
                items.append((new_key[:-6], val))
            else:
                items.append((new_key, val))
    return dict(items)


def parse_yml(
        file_path: str,
        convert_dict: Optional[dict] = None,
        replace_nested: Optional[dict] = None
) -> Dict[str, Any]:
    """Parses a metadata yaml file into a dictionary.

    Args:
        file_path (str): The file path of the yml file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the yml.
    """
    if convert_dict is None:
        convert_dict = {}

    if replace_nested is None:
        replace_nested = {}

    with open(file_path) as file:
        return flatten_and_replace(yaml.safe_load(file), convert_dict, replace_nested)


def parse_json(file_path: str) -> Dict[str, Any]:
    """Parses a metadata json file into a dictionary.

    Args:
        file_path (str): The file path of the json file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the json.
    """
    with open(file_path, "r") as file:
        return json.load(file)
