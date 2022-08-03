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
"""Perkin Ellmer transmission file reader implementation for the DataConverter."""

import os
from typing import Tuple, Any, Dict, Callable
import json
import yaml
import pandas as pd

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
import nexusparser.tools.dataconverter.readers.transmission.metadata_parsers as mpars
from nexusparser.tools.dataconverter.readers.utils import flatten_and_replace


#: Dictionary mapping metadata in the asc file to the paths in the NeXus file.
METADATA_MAP: Dict[str, Callable[[list], Any]] = {
    "/ENTRY[entry]/start_time": mpars.read_start_date,
    "/ENTRY[entry]/instrument/sample_attenuator/attenuator_transmission":
        mpars.read_sample_attenuator,
    "/ENTRY[entry]/instrument/ref_attenuator/attenuator_transmission":
        mpars.read_ref_attenuator
}
# Dictionary to map value during the yaml eln reading
# This is typically a mapping from ELN signifier to NeXus path
CONVERT_DICT: Dict[str, str] = {}
# Dictionary to map nested values during the yaml eln reading
# This is typically a mapping from nested ELN signifiers to NeXus group
REPLACE_NESTED: Dict[str, str] = {}


def parse_asc(file_path: str) -> Dict[str, Any]:
    """Parses a Perkin Ellmer asc file into metadata and data dictionary.

    Args:
        file_path (str): File path to the asc file.

    Returns:
        Dict[str, Any]: Dictionary containing the metadata and data from the asc file.
    """
    template: Dict[str, Any] = {}
    data_start_ind = "#DATA"

    with open(file_path, encoding="utf-8") as fobj:
        keys = []
        for line in fobj:
            if line.strip() == data_start_ind:
                break
            keys.append(line.strip())

        for path, parser in METADATA_MAP.items():
            template[path] = parser(keys)

        data = pd.read_csv(
            fobj, delim_whitespace=True, header=None, index_col=0
        )

    template["/ENTRY[entry]/data/@signal"] = "data"
    template["/ENTRY[entry]/data/@axes"] = "wavelength"
    template["/ENTRY[entry]/data/type"] = "transmission"
    template["/ENTRY[entry]/data/@signal"] = "transmission"
    template["/ENTRY[entry]/data/wavelength"] = data.index.values
    template["/ENTRY[entry]/data/wavelength/@units"] = "nm"
    template["/ENTRY[entry]/data/transmission"] = data.values[:, 0]

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


def parse_yml(file_path: str) -> Dict[str, Any]:
    """Parses a metadata yaml file into a dictionary.

    Args:
        file_path (str): The file path of the yml file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the yml.
    """
    with open(file_path) as file:
        return flatten_and_replace(yaml.safe_load(file), CONVERT_DICT, REPLACE_NESTED)


# pylint: disable=too-few-public-methods
class TransmissionReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to Nexus."""

    supported_nxdls = ["NXtransmission"]

    def read(
            self,
            template: dict = None,
            file_paths: Tuple[str] = None,
            _: Tuple[Any] = None,
    ) -> dict:
        """Reader class to read transmission data from Perkin Ellmer measurement files"""
        extensions = {
            ".asc": parse_asc,
            ".json": parse_json,
            ".yml": parse_yml,
            ".yaml": parse_yml,
        }

        template["/@default"] = "entry"
        template["/ENTRY[entry]/@default"] = "data"
        template["/ENTRY[entry]/definition"] = "NXtransmission"
        template["/ENTRY[entry]/definition/@version"] = "v2022.06"
        template["/ENTRY[entry]/definition/@url"] = \
            "https://fairmat-experimental.github.io/nexus-fairmat-proposal/" + \
            "50433d9039b3f33299bab338998acb5335cd8951/index.html"

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
