
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
from pathlib import Path
import re
from typing import Any, List, TextIO, Dict, Optional
import logging
import numpy as np
import pandas as pd

from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader
from nexusutils.dataconverter.readers.hall import helpers
from nexusutils.dataconverter.readers.utils import parse_json, parse_yml

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

# Dict for converting values for specific keys
CONVERSION_FUNCTIONS = {
    "Start Time": helpers.convert_date,
    "Time Completed": helpers.convert_date,
    "Skipped at": helpers.convert_date
}

# Keys that indicate the start of measurement block
MEASUREMENT_KEYS = ["Contact Sets"]

reader_dir = Path(__file__).parent
config_file = reader_dir.joinpath("enum_map.json")
ENUM_FIELDS = parse_json(str(config_file))

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


def split_add_key(fobj: Optional[TextIO], dic: dict, prefix: str, expr: str) -> None:
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

    def parse_enum() -> bool:
        sprefix = prefix.strip("/")
        if 'Keithley' not in sprefix:
            w_trailing_num = re.search(r"(.*) \d+$", sprefix)
            if w_trailing_num:
                sprefix = w_trailing_num.group(1)

        if (
            sprefix in ENUM_FIELDS
            and key in ENUM_FIELDS[sprefix]
            and helpers.is_integer(jval)
        ):
            if jval not in ENUM_FIELDS[sprefix][key]:
                logger.warning("Option `%s` not in `%s, %s`", jval, sprefix, key)
            dic[f"{prefix}/{key}"] = ENUM_FIELDS[sprefix][key].get(jval, "UNKNOWN")
            return True

        return False

    def parse_field():
        if helpers.is_value_with_unit(jval):
            value, unit = helpers.split_value_with_unit(jval)
            dic[f"{prefix}/{key}"] = value
            dic[f"{prefix}/{key}/@units"] = helpers.clean(unit)
            return

        if parse_enum():
            return

        if helpers.is_integer(jval):
            dic[f"{prefix}/{key}"] = int(jval)
            return

        if helpers.is_number(jval):
            dic[f"{prefix}/{key}"] = float(jval)
            return

        if helpers.is_boolean(jval):
            dic[f"{prefix}/{key}"] = helpers.to_bool(jval)
            return

        dic[f"{prefix}/{key}"] = CONVERSION_FUNCTIONS.get(key, lambda v: v)(jval)

    def parse_data():
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
                continue
            data.append(list(map(lambda x: x.strip(), re.split("\t+", line))))

        dkey = helpers.get_unique_dkey(dic, f"{prefix}/{key}/{jval}/data")
        dic[dkey] = pd.DataFrame(np.array(data[1:], dtype=np.float64), columns=data[0])

    if fobj is not None and key in MEASUREMENT_KEYS:
        parse_data()
    else:
        parse_field()


def parse_txt(fname: str, encoding: str = "iso-8859-1") -> dict:
    """Reads a template dictonary from a hall measurement file

    Args:
        fname (str): The file name of the masurement file
        encoding (str, optional): The encoding of the ASCII file. Defaults to "iso-8859-1".

    Returns:
        dict: Dict containing the data and metadata of the measurement
    """
    def parse_measurement(line: str, current_section: str, current_measurement: str):
        data = []
        for mline in fobj:
            if not mline.strip():
                break
            data.append(list(map(lambda x: x.strip(), re.split("\t+", mline))))

        header = list(map(lambda x: x.strip(), re.split("\t+", line)))
        dkey = helpers.get_unique_dkey(
            template, f"{current_section}{current_measurement}/data"
        )
        template.update(helpers.pandas_df_to_template(
            dkey,
            pd.DataFrame(
                np.array(data, dtype=np.float64), columns=header
            )
        ))

        return current_section, current_measurement

    def parse(line: str, current_section: str, current_measurement: str):
        if helpers.is_section(line):
            sline = line.strip()[1:-1]
            current_section = f"/{SECTION_REPLACEMENTS.get(sline, sline)}"
            current_measurement = ""
            return current_section, current_measurement

        if helpers.is_measurement(line):
            step, _, *meas = line.partition(":")
            sline = f"{step[6:]}_" + "".join(meas).strip()[:-1]
            current_measurement = f"/{MEASUREMENT_REPLACEMENTS.get(sline, sline)}"
            return current_section, current_measurement

        if helpers.is_key(line):
            split_add_key(
                fobj, template, f"{current_section}{current_measurement}", line
            )
            return current_section, current_measurement

        if helpers.is_meas_header(line):
            return parse_measurement(line, current_section, current_measurement)

        if line.strip():
            logger.warning("Line `%s` ignored", line.strip())

        return current_section, current_measurement

    template: Dict[str, Any] = {}
    current_section = "/entry"
    current_measurement = ""
    with open(fname, encoding=encoding) as fobj:
        for line in fobj:
            current_section, current_measurement = parse(
                line, current_section, current_measurement
            )

    return template


# pylint: disable=too-few-public-methods
class HallReader(YamlJsonReader):
    """HallReader implementation for the DataConverter
    to convert Hall data to Nexus."""

    supported_nxdls: List[str] = ["NXroot"]
    extensions = {
        ".txt": lambda fname: parse_txt(fname, "iso-8859-1"),
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, None, None),
        ".yaml": lambda fname: parse_yml(fname, None, None),
    }


READER = HallReader
