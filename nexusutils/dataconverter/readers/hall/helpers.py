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
from typing import Tuple, Union, Dict, Any
import re
from datetime import datetime
import numpy as np
import pandas as pd
import pytz


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


def is_value_with_unit(expr: str) -> bool:
    """Checks whether an expression is a value with a unit,
    i.e. is of the form value [unit].

    Args:
        expr (str): The expression to check

    Returns:
        bool: Returns true if the expr is a value with unit
    """
    return bool(re.search(r"^.+\s\[.+\]$", expr))


def is_integer(expr: str) -> bool:
    """Checks whether an expression is an integer number,
    i.e. 3, +3 or -3. Also supports numbers in the form of 003.

    Args:
        expr (str): The expression to check

    Returns:
        bool: Returns true if the expr is an integer number
    """
    return bool(re.search(r"^[+-]?\d+$", expr))


def is_number(expr: str) -> bool:
    """Checks whether an expression is a number,
    i.e. is of the form 0.3, 3, 1e-3, 1E5 etc.

    Args:
        expr (str): The expression to check

    Returns:
        bool: Returns true if the expr is a number
    """
    return bool(
        re.search(r"^[+-]?(\d+([.]\d*)?([eE][+-]?\d+)?|[.]\d+([eE][+-]?\d+)?)$", expr)
    )


def is_boolean(expr: str) -> bool:
    """Checks whether an expression is a boolean,
    i.e. is equal to True or False (upper or lower case).

    Args:
        expr (str): The expression to check.

    Returns:
        bool: Returns true if the expr is a boolean
    """
    return bool(re.search(r"True|False|true|false|On|Off|Yes|No", expr))


def to_bool(expr: str) -> bool:
    """Converts boolean representations in strings to python booleans.

    Args:
        expr (str): The string to convert to boolean.

    Returns:
        bool: The boolean value.
    """
    replacements = {
        'On': True,
        'Off': False,
        'Yes': True,
        'No': False,
        'True': True,
        'False': False,
        'true': True,
        'false': False,
    }

    return replacements.get(expr)


def split_str_with_unit(expr: str, lower: bool = True) -> Tuple[str, str]:
    """Splits an expression into a string and a unit.
    The input expression should be of the form value [unit] as
    is checked with is_value_with_unit function.

    Args:
        expr (str): The expression to split
        lower (bool, optional):
            If True the value is converted to lower case. Defaults to True.

    Returns:
        Tuple[str, str]: A tuple of a value unit pair.
    """
    value = re.split(r"\s+\[.+\]", expr)[0]
    unit = re.search(r"(?<=\[).+?(?=\])", expr)[0]

    if lower:
        return value.lower(), unit
    return value, unit


def split_value_with_unit(expr: str) -> Tuple[Union[float, str], str]:
    """Splits an expression into a string or float and a unit.
    The input expression should be of the form value [unit] as
    is checked with is_value_with_unit function.
    The value is automatically converted to a float if it is a number.

    Args:
        expr (str): The expression to split

    Returns:
        Tuple[Union[float, str], str]: A tuple of a value unit pair.
    """
    value, unit = split_str_with_unit(expr, False)

    if is_number(value):
        return float(value), unit

    return value, unit


def clean(unit: str) -> str:
    """Cleans an unit string, e.g. converts `VS` to `volt * seconds`.
    If the unit is not in the conversion dict the input string is
    returned without modification.

    Args:
        unit (str): The dirty unit string.

    Returns:
        str: The cleaned unit string.
    """
    conversions = {
        'VS': "volt * second",
        'Sec': "s",
        '²': "^2",
        '³': "^3",
        'ohm cm': "ohm * cm",
    }

    for old, new in conversions.items():
        unit = unit.replace(old, new)

    return unit


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


def pandas_df_to_template(prefix: str, data: pd.DataFrame) -> Dict[str, Any]:
    """Converts a dataframe to a NXdata entry template.

    Args:
        prefix (str): The path prefix to write the data into. Without a trailing slash.
        df (pd.DataFrame): The dataframe which should be converted.

    Returns:
        Dict[str, Any]: The dict containing the data and metainfo.
    """
    if prefix.endswith('/'):
        prefix = prefix[:-1]

    template: Dict[str, Any] = {}
    template[f'{prefix}/@NX_class'] = 'NXdata'

    def write_data(header: str, attr: str, data: np.ndarray) -> None:
        if header is None:
            print('Warning: Trying to write dataframe without a header. Skipping.')
            return

        if is_value_with_unit(header):
            name, unit = split_str_with_unit(header)
            template[f'{prefix}/{name}/@units'] = clean(unit)
        else:
            name = header.lower()

        if attr == '@auxiliary_signals':
            if f'{prefix}/{attr}' in template:
                template[f'{prefix}/{attr}'].append(name)
            else:
                template[f'{prefix}/{attr}'] = [name]
        else:
            template[f'{prefix}/{attr}'] = name
        template[f'{prefix}/{name}'] = data

    if data.index.name is None:
        data = data.set_index(data.columns[0])

    # Drop last line if it has an errornous zero temperature
    if data.index.values[-1] == 0:
        data = data.iloc[:-1]

    write_data(data.index.name, '@axes', data.index.values)
    write_data(data.columns[0], '@signal', data.iloc[:, 0].values)

    for column in data.columns[1:]:
        write_data(column, '@auxiliary_signals', data[column].values)

    return template


def convert_date(datestr: str, timezone: str = "Europe/Berlin") -> str:
    """Converts a hall date formated string to isoformat string.

    Args:
        datestr (str): The hall date string
        timezone (str): The timezone of the hall date string. Defaults to "Europe/Berlin"

    Returns:
        str: The iso formatted string.
    """

    try:
        return (
            datetime
            .strptime(datestr, r'%m/%d/%y %H%M%S')
            .astimezone(pytz.timezone(timezone))
            .isoformat()
        )
    except ValueError:
        print("Warning: datestring does not conform to date format. Skipping.")
        return datestr
