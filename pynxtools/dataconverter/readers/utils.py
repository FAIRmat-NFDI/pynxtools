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
from dataclasses import dataclass, replace
from typing import List, Any, Dict, Optional
from collections.abc import Mapping
import json
import yaml


@dataclass
class FlattenSettings():
    """Settings for flattening operations.

    Args:
        dic (dict): Dictionary to flatten
        convert_dict (dict): Dictionary for renaming keys in the flattend dict.
        replace_nested (dict): Dictionary for renaming nested keys.
        parent_key (str, optional):
            Parent key of the dictionary. Defaults to "/ENTRY[entry]".
        sep (str, optional): Separator for the keys. Defaults to "/".
    """
    dic: Mapping
    convert_dict: dict
    replace_nested: dict
    parent_key: str = "/ENTRY[entry]"
    sep: str = "/"
    is_in_section: bool = False
    ignore_keys: Optional[list] = None


def is_section(val: Any) -> bool:
    """Checks whether a value is a section.

    Args:
        val (Any): A list or value.

    Returns:
        bool: True if val is a section.
    """
    return isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict)


def is_value_unit_pair(val: Any) -> bool:
    """Checks whether the value contains a dict of a value unit pair.

    Args:
        val (Any): The value to be checked.

    Returns:
        bool: True if val contains a value unit pair dict.
    """
    if not isinstance(val, dict):
        return False

    if len(val) == 2 and "value" in val and "unit" in val:
        return True
    return False


def uniquify_keys(ldic: list) -> List[Any]:
    """Uniquifys keys in a list of tuple lists containing key value pairs.

    Args:
        ldic (list): List of lists of length two, containing key value pairs.

    Returns:
        List[Any]: Uniquified list, where duplicate keys are appended with 1, 2, etc.
    """
    dic: dict = {}
    for key, val in ldic:
        suffix = 0
        sstr = "" if suffix == 0 else str(suffix)
        while f"{key}{sstr}" in dic:
            sstr = "" if suffix == 0 else str(suffix)
            suffix += 1

        if is_value_unit_pair(val):
            dic[f"{key}{sstr}"] = val["value"]
            dic[f"{key}{sstr}/@units"] = val["unit"]
            continue
        dic[f"{key}{sstr}"] = val

    return list(map(list, dic.items()))


def parse_section(key: str, val: Any, settings: FlattenSettings) -> List[Any]:
    """Parse a section, i.e. an entry containing a list of entries.

    Args:
        key (str): The key which is currently being checked.
        val (Any): The value at the current key.
        settings (FlattenSettings): The flattening settings.

    Returns:
        List[Any]: A list of list tuples containing key, value pairs.
    """
    if not is_section(val):
        return [(key, val)]

    groups: List[Any] = []
    for group in val:
        groups.extend(
            flatten_and_replace(
                replace(settings, dic=group, parent_key=key, is_in_section=True)
            ).items()
        )

    return uniquify_keys(groups)


def flatten_and_replace(settings: FlattenSettings) -> dict:
    """Flatten a nested dictionary, and replace the keys with the appropriate
    paths in the nxs file.

    Args:
        settings (FlattenSettings): Settings dataclass for flattening the data.

    Returns:
        dict: Flattened dictionary
    """
    items: List[Any] = []
    for key, val in settings.dic.items():
        if settings.ignore_keys and key in settings.ignore_keys:
            continue
        new_key = settings.parent_key + settings.sep + settings.convert_dict.get(key, key)
        if isinstance(val, Mapping):
            items.extend(
                flatten_and_replace(replace(settings, dic=val, parent_key=new_key))
                .items()
                if not (settings.is_in_section and is_value_unit_pair(val))
                else [[new_key, val]]
            )
            continue

        for old, new in settings.replace_nested.items():
            new_key = new_key.replace(old, new)

        if new_key.endswith("/value"):
            items.append((new_key[:-6], val))
        else:
            items.extend(parse_section(new_key, val, settings))

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

    convert_dict["unit"] = "@units"

    with open(file_path, encoding='utf-8') as file:
        return flatten_and_replace(
            FlattenSettings(
                dic=yaml.safe_load(file),
                convert_dict=convert_dict,
                replace_nested=replace_nested
            )
        )


def parse_json(file_path: str) -> Dict[str, Any]:
    """Parses a metadata json file into a dictionary.

    Args:
        file_path (str): The file path of the json file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the json.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
