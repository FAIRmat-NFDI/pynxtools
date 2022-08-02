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

import errno
import os
from typing import Tuple, Any, Dict
import json
import yaml

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader


def parse_asc(file_path: str) -> Dict[str, Any]:
    pass


def parse_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)


def parse_yml(file_path: str) -> Dict[str, Any]:
    with open(file_path) as file:
        return yaml.safe_load(file)


def load_files_into_template(file_paths: Tuple[str]) -> Dict[str, Any]:
    """_summary_

    Args:
        file_paths (Tuple[str]): _description_

    Raises:
        ValueError: _description_
        FileNotFoundError: _description_

    Returns:
        list: _description_
    """
    extensions = {
        ".asc": parse_asc,
        ".json": parse_json,
        ".yml": parse_yml,
        ".yaml": parse_yml,
    }

    # Approach:
    # 1. Split files by extensions, if not splitable throw a warning and ignore file
    # 2. Check if file exists, if not throw a warning and ignore file
    # 3. Sort files by extension (to account for reproducible updating of reduntant values)
    # 4. Loop through files list

    data: Dict[str, Any] = {}
    for file_path in file_paths:
        try:
            file_extension = file_path[file_path.rindex(".") :]
        except ValueError as err:
            raise ValueError(
                f"The file path {file_path} muste have an extension."
            ) from err

        if file_extension not in extensions.keys():
            print(
                f"WARNING\n"
                f"The reader only supports files of type {extensions.keys()},"
                f"but {file_path} does not match."
            )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                file_path,
            )

        data.update(extensions.get(file_extension, lambda _: {})(file_path))

    return data


class TransmissionReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to Nexus."""

    supported_nxdls = ["NXtransmission"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ) -> dict:
        """_summary_

        Args:
            template (dict, optional): _description_. Defaults to None.
            file_paths (Tuple[str], optional): _description_. Defaults to None.
            objects (Tuple[Any], optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """

        if not file_paths:
            raise Exception("No input files were given to the transmission reader.")

        return template


READER = TransmissionReader
