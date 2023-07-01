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
import json
from typing import Any, Dict
import pandas as pd

from pynxtools.dataconverter.readers.json_yml.reader import YamlJsonReader
from pynxtools.dataconverter.readers.utils import parse_yml


# Dictionary mapping metadata in the asc file to the paths in the NeXus file.
# The entry can either be a function with one list parameter
# which is executed to fill the specific path or an
# integer which is used to get the value at the index of the metadata.
# If the value is a str this string gets inputed at the path.
METADATA_MAP: Dict[str, Any] = {}
# Dictionary to map value during the yaml eln reading
# This is typically a mapping from ELN signifier to NeXus path
CONVERT_DICT: Dict[str, str] = {"Sample": "SAMPLE[sample]", "unit": "@units"}
# Dictionary to map nested values during the yaml eln reading
# This is typically a mapping from nested ELN signifiers to NeXus group
REPLACE_NESTED: Dict[str, str] = {}


def data_to_template(data: pd.DataFrame) -> Dict[str, Any]:
    """Builds the data entry dict from the data in a pandas dataframe

    Args:
        data (pd.DataFrame): The dataframe containing the data.

    Returns:
        Dict[str, Any]: The dict with the data paths inside NeXus.
    """
    template: Dict[str, Any] = {}
    template["/ENTRY[entry]/data/@axes"] = "wavelength"
    template["/ENTRY[entry]/data/type"] = "transmission"
    template["/ENTRY[entry]/data/@signal"] = "transmission"
    template["/ENTRY[entry]/data/wavelength"] = data.index.values
    template["/ENTRY[entry]/instrument/spectrometer/wavelength"] = data.index.values
    template["/ENTRY[entry]/data/wavelength/@units"] = "nm"
    template["/ENTRY[entry]/data/transmission"] = data.values[:, 0]
    template["/ENTRY[entry]/instrument/measured_data"] = data.values

    return template


def parse_measurement_file(file_path: str) -> Dict[str, Any]:
    """TODO: _summary_

    Args:
        file_path (str): File path to the measurement file.

    Returns:
        Dict[str, Any]:
            Dictionary containing the metadata and data from the measurement file.
    """
    template: Dict[str, Any] = {}

    return template


def parse_measurement_set(measurement_set: Dict[str, Any]) -> Dict[str, Any]:
    """TODO: _summary_

    Args:
        measurement_set (Dict[str, Any]): TODO: _description_

    Returns:
        Dict[str, Any]: TODO: _description_
    """
    template: Dict[str, Any] = {}

    return template


def parse_json(file_path: str) -> Dict[str, Any]:
    """Parses a metadata json file into a dictionary.

    Args:
        file_path (str): The file path of the json file.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the json.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    if "measurement_set" in json_data:
        json_data.update(parse_measurement_set(json_data.get("measurement_set")))
        del json_data["measurement_set"]

    return json_data


def add_def_info() -> Dict[str, str]:
    """Creates a template with definition version information"""
    template: Dict[str, Any] = {}
    template["/@default"] = "entry"
    template["/ENTRY[entry]/@default"] = "data"
    template["/ENTRY[entry]/definition"] = "NXellipsometry"
    template["/ENTRY[entry]/definition/@version"] = "v2022.06"
    template["/ENTRY[entry]/definition/@url"] = (
        "https://fairmat-experimental.github.io/nexus-fairmat-proposal/"
        + "50433d9039b3f33299bab338998acb5335cd8951/index.html"
    )

    return template


# pylint: disable=too-few-public-methods
class EllipsometrySentechReader(YamlJsonReader):
    """
    Reads ellipsometry data from sentech spectraray ascii files.
    """

    supported_nxdls = ["NXellipsometry"]
    extensions = {
        ".txt": parse_measurement_file,
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        ".yaml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        "default": lambda _: add_def_info(),
    }


READER = EllipsometrySentechReader
