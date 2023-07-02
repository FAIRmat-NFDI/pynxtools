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
import numpy as np
import pandas as pd

from pynxtools.dataconverter.readers.json_yml.reader import YamlJsonReader
from pynxtools.dataconverter.readers.utils import parse_yml
from pynxtools.dataconverter.readers.ellips.reader import CONVERT_DICT, REPLACE_NESTED


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


def _get_columns_as_number(dataframe: pd.DataFrame) -> list:
    return list(
        map(
            lambda aoi: round(float(aoi.replace(".", "").replace(",", ".")), 2),
            dataframe.columns,
        )
    )


def read_measurement_file_to_pandas_df(file_path: str) -> pd.DataFrame:
    """TODO: _summary_

    Args:
        file_path (str): File path to the measurement file.

    Returns:
        Dict[str, Any]:
            Dictionary containing the metadata and data from the measurement file.
    """
    frame = pd.read_csv(file_path, decimal=",", sep=r"\s+", index_col=0)

    nrows, ncols = frame.shape
    data = {
        "psi": frame.iloc[:, ::2].to_numpy().ravel("F"),
        "delta": frame.iloc[:, 1::2].to_numpy().ravel("F"),
        "aoi": np.asarray(_get_columns_as_number(frame.iloc[:, ::2])).repeat(nrows),
    }
    return pd.DataFrame(
        data,
        index=np.tile(np.asarray(frame.index), ncols // 2),
        columns=["aoi", "psi", "delta"],
    )


def parse_measurement_set(measurement_set: Dict[str, Any]) -> Dict[str, Any]:
    """TODO: _summary_

    Args:
        measurement_set (Dict[str, Any]): TODO: _description_

    Returns:
        Dict[str, Any]: TODO: _description_
    """

    for key in ("axis_name", "values", "files"):
        if key not in measurement_set:
            raise ValueError(f"No {key} found in measurement set.")

    for lis in ("values", "files"):
        if not isinstance(lis, list):
            raise ValueError(
                f"{lis} in measurement set must be a list. But is {type(lis)}"
            )

    if len(measurement_set["values"]) != len(measurement_set["files"]):
        raise ValueError("Values and files list must have the same length.")
    template: Dict[str, Any] = {}

    frames = []
    for value, file in zip(measurement_set["values"], measurement_set["files"]):
        frame = read_measurement_file_to_pandas_df(file)
        frame[measurement_set["axis_name"]] = value
        frames.append(frame)

    full_frame = pd.concat(frames)

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


def appdef_defaults() -> Dict[str, str]:
    """Creates a template with definition version information"""
    template: Dict[str, Any] = {}
    template["/@default"] = "entry"
    template["/ENTRY[entry]/@default"] = "data"
    template["/ENTRY[entry]/definition"] = "NXellipsometry"
    template["/ENTRY[entry]/definition/@version"] = "v2022.07"
    template["/ENTRY[entry]/definition/@url"] = (
        "https://fairmat-nfdi.github.io/nexus-fairmat-proposal/"
        "9636feecb79bb32b828b1a9804269573256d7696/classes/"
        "contributed_definitions/NXellipsometry.html#nxellipsometry"
    )

    return template


# pylint: disable=too-few-public-methods
class EllipsometrySentechReader(YamlJsonReader):
    """
    Reads ellipsometry data from sentech spectraray ascii files.
    """

    supported_nxdls = ["NXellipsometry"]
    extensions = {
        # ".csv": parse_measurement_file,
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        ".yaml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        "default": lambda _: appdef_defaults(),
    }


READER = EllipsometrySentechReader
