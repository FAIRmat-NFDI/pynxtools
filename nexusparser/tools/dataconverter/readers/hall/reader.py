
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
"""Lake Shore Hall file reader implementation for the DataConverter."""
import re
from typing import Any, List, TextIO, Dict
import numpy as np
import pandas as pd

from nexusparser.tools.dataconverter.readers.json_yml.reader import YamlJsonReader
import nexusparser.tools.dataconverter.readers.hall.helpers as helpers
from nexusparser.tools.dataconverter.readers.utils import parse_json, parse_yml

# Replacement dict for section names
SECTION_REPLACEMENTS = {
    "Sample parameters": "entry/sample",
    "Measurements": "entry/measurement",
}

# Replacement dict for measurement indicators
MEASUREMENT_REPLACEMENTS = {
    "IV Curve Measurement": "iv_curve",
    "Variable Field Measurement": "variable_field",
}

# Keys that indicate the start of measurement block
MEASUREMENT_KEYS = ["Contact Sets"]


def split_add_key(fobj: TextIO, dic: dict, prefix: str, expr: str) -> None:
    """Splits a key value pair and adds it to the dictionary.
    It also checks for measurement headers and adds the full tabular data as a
    pandas array to the dictionary.

    Args:
        fobj (TextIO): The file object to read from
        dic (dict): The dict to write the data into
        prefix (str): Key prefix for the dict
        expr (str): The current expr/line to parse
    """
    key, *val = re.split(r"\s*[:|=]\s*", expr)
    jval = "".join(val).strip()

    if key in MEASUREMENT_KEYS:
        data = []
        for line in fobj:
            if not line.strip():
                break
            if helpers.is_key(line):
                split_add_key(
                    None,  # There should be no deeper measurement,
                    # prevent further consumption of lines
                    dic,
                    f"{prefix}/{key}/{jval}",
                    line,
                )
            else:
                data.append(list(map(lambda x: x.strip(), re.split("\t+", line))))

        dkey = helpers.get_unique_dkey(dic, f"{prefix}/{key}/{jval}/data")
        dic[dkey] = pd.DataFrame(np.array(data[1:], dtype=np.float64), columns=data[0])
    else:
        dic[f"{prefix}/{key}"] = jval


def parse_txt(fname: str, encoding: str = "iso-8859-1") -> dict:
    """Reads a template dictonary from a hall measurement file

    Args:
        fname (str): The file name of the masurement file
        encoding (str, optional): The encoding of the ASCII file. Defaults to "iso-8859-1".

    Returns:
        dict: Dict containing the data and metadata of the measurement
    """
    template: Dict[str, Any] = {}
    current_section = "/entry"
    current_measurement = ""
    with open(fname, encoding=encoding) as fobj:
        for line in fobj:
            if helpers.is_section(line):
                sline = line.strip()[1:-1]
                current_section = f"/{SECTION_REPLACEMENTS.get(sline, sline)}"
                current_measurement = ""
            elif helpers.is_measurement(line):
                step, _, *meas = line.partition(":")
                sline = f"{step[6:]}_" + "".join(meas).strip()[:-1]
                current_measurement = f"/{MEASUREMENT_REPLACEMENTS.get(sline, sline)}"
            elif helpers.is_key(line):
                split_add_key(
                    fobj, template, f"{current_section}{current_measurement}", line
                )
            elif helpers.is_meas_header(line):
                data = []
                for mline in fobj:
                    if not mline.strip():
                        break
                    data.append(list(map(lambda x: x.strip(), re.split("\t+", mline))))

                header = list(map(lambda x: x.strip(), re.split("\t+", line)))
                dkey = helpers.get_unique_dkey(
                    template, f"{current_section}{current_measurement}/data"
                )
                template[dkey] = pd.DataFrame(
                    np.array(data, dtype=np.float64), columns=header
                )
            else:
                if line.strip():
                    print(f"Warning: line `{line.strip()}` ignored")

    return template


# pylint: disable=too-few-public-methods
class HallReader(YamlJsonReader):
    """HallReader implementation for the DataConverter
    to convert Hall data to Nexus."""

    supported_nxdls: List[str] = ["NXroot"]
    extensions = {
        ".txt": lambda fname: parse_txt(fname, "iso-8859-1"),
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, {}, {}),
        ".yaml": lambda fname: parse_yml(fname, {}, {}),
    }


READER = HallReader
