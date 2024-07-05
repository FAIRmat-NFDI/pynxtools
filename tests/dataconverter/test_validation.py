#
# Copyright The pynxtools Authors.
#
# This file is part of pynxtools.
# See https://github.com/FAIRmat-NFDI/pynxtools for further info.
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
import logging
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pytest
from pynxtools.dataconverter.validation import validate_dict_against


def get_data_dict():
    return {
        "/ENTRY[my_entry]/optional_parent/required_child": 1,
        "/ENTRY[my_entry]/optional_parent/optional_child": 1,
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value": 2.0,
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units": "nm",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value": True,
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value": 2,
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value/@units": "eV",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value": np.array(
            [1, 2, 3], dtype=np.int8
        ),
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value/@units": "kg",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value": "just chars",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type": "2nd type",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value": "2022-01-22T12:14:12.05018+00:00",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value": True,
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value": 2,
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value/@units": "eV",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value": np.array(
            [1, 2, 3], dtype=np.int8
        ),
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value/@units": "kg",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value": "just chars",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/type": "2nd type",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value": "2022-01-22T12:14:12.05018+00:00",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value/@units": "",
        "/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field": 1,
        "/ENTRY[my_entry]/definition": "NXtest",
        "/ENTRY[my_entry]/definition/@version": "2.4.6",
        "/ENTRY[my_entry]/program_name": "Testing program",
        "/ENTRY[my_entry]/OPTIONAL_group[my_group]/optional_field": 1,
        "/ENTRY[my_entry]/required_group/description": "An example description",
        "/ENTRY[my_entry]/required_group2/description": "An example description",
        "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/data": 1,
        "/@default": "Some NXroot attribute",
    }


def remove_from_dict(keys: Union[Union[List[str], Tuple[str, ...]], str], data_dict):
    if isinstance(keys, (list, tuple)):
        for key in keys:
            data_dict.pop(key, None)
    else:
        data_dict.pop(keys)

    return data_dict


def alter_dict(new_values: Dict[str, Any], data_dict: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in new_values.items():
        data_dict[key] = value
    return data_dict


@pytest.mark.parametrize(
    "data_dict",
    [
        pytest.param(get_data_dict(), id="valid-unaltered-data-dict"),
        pytest.param(
            remove_from_dict(
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value", get_data_dict()
            ),
            id="removed-optional-value",
        ),
    ],
)
def test_valid_data_dict(caplog, data_dict):
    with caplog.at_level(logging.WARNING):
        validate_dict_against("NXtest", data_dict)
    assert caplog.text == ""


@pytest.mark.parametrize(
    "data_dict, error_message",
    [
        pytest.param(
            remove_from_dict(
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value", get_data_dict()
            ),
            "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value is required and hasn't been supplied by the reader.",
            id="missing-required-value",
        )
    ],
)
def test_validation_shows_warning(caplog, data_dict, error_message):
    with caplog.at_level(logging.WARNING):
        assert not validate_dict_against("NXtest", data_dict)

    assert error_message in caplog.text
