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
"""MyDataReader implementation for the DataConverter to convert mydata to Nexus."""

import os
import collections
from typing import Tuple, Any, Dict
import json
import yaml
import pandas as pd

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader


#: Dictionary mapping the line numbers in the asc file to the paths in the NeXus file.
METADATA_MAP: Dict[str, Any] = {}


def parse_asc(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Parses a Perkin Ellmer asc file into metadata and data dictionary.

    Args:
        file_path (str): File path to the asc file.

    Returns:
        Dict[str, Any]: Dictionary containing the metadata and data from the asc file.
    """
    template: Dict[str, Any] = {}
    data_start_ind = "#DATA"

    with open(file_path, encoding=encoding) as fobj:
        keys = []
        for line in fobj:
            if line.strip() == data_start_ind:
                break
            keys.append(line.strip())

        for key, val in METADATA_MAP.items():
            template[key] = keys[val]

        template["/ENTRY[entry]/data"] = pd.read_csv(
            fobj, delim_whitespace=True, header=None, index_col=0
        )

    return template


def parse_json(file_path: str) -> Dict[str, Any]:
    """Parses a metadata json file into a dictionary.

    Args:
        file_path (str): The file path of the json file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the json.
    """
    with open(file_path, "r") as file:
        return json.load(file)


CONVERT_DICT: Dict[str, str] = {}
REPLACE_NESTED: Dict[str, str] = {}


def flatten_and_replace(dic, parent_key="/ENTRY[entry]", sep="/"):
    """Flatten a nested dictionary, and replace the keys with the appropriate
    paths in the nxs file.
    Args:
        d (dict): dictionary to flatten
        parent_key (str): parent key of the dictionary
        sep (str): separator for the keys
    Returns:
        dict: flattened dictionary
    """
    items = []
    for key, val in dic.items():
        new_key = parent_key + sep + CONVERT_DICT.get(key, key)
        if isinstance(val, collections.Mapping):
            items.extend(flatten_and_replace(val, new_key, sep=sep).items())
        else:
            for old, new in REPLACE_NESTED.items():
                new_key = new_key.replace(old, new)

            if new_key.endswith("/value"):
                items.append((new_key[:-6], val))
            else:
                items.append((new_key, val))
    return dict(items)


def parse_yml(file_path: str) -> Dict[str, Any]:
    """Parses a metadata yaml file into a dictionary.

    Args:
        file_path (str): The file path of the yml file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the yml.
    """
    with open(file_path) as file:
        return flatten_and_replace(yaml.safe_load(file))


class TransmissionReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to Nexus."""

    supported_nxdls = ["NXtransmission"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        _: Tuple[Any] = None,
    ) -> dict:
        """_summary_

        Args:
            template (dict, optional): _description_. Defaults to None.
            file_paths (Tuple[str], optional): _description_. Defaults to None.
            objects (Tuple[Any], optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """

        extensions = {
            ".asc": lambda fpath: parse_asc(fpath),
            ".json": parse_json,
            ".yml": parse_yml,
            ".yaml": parse_yml,
        }

        if template is None:
            template = {}

        sorted_paths = sorted(file_paths, key=lambda f: os.path.splitext(f)[1])
        for file_path in sorted_paths:
            extension = os.path.splitext(file_path)[1]
            if extension not in extensions.keys():
                print(
                    f"WARNING: "
                    f"File {file_path} has an unsupported extension, ignoring file."
                )
                continue
            if not os.path.exists(file_path):
                print(f"WARNING: File {file_path} does not exist, ignoring entry.")
                continue

            template.update(extensions.get(extension, lambda _: {})(file_path))

        return template


READER = TransmissionReader
