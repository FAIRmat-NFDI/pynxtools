import logging
from typing import Any, Dict, List, Mapping, Tuple, Union

import numpy as np
import pytest

from pynxtools.dataconverter.validation import validate_dict_against


def get_data_dict():
    return {
        "/my_entry/optional_parent/required_child": 1,
        "/my_entry/optional_parent/optional_child": 1,
        "/my_entry/nxodd_name/float_value": 2.0,
        "/my_entry/nxodd_name/float_value/@units": "nm",
        "/my_entry/nxodd_name/bool_value": True,
        "/my_entry/nxodd_name/bool_value/@units": "",
        "/my_entry/nxodd_name/int_value": 2,
        "/my_entry/nxodd_name/int_value/@units": "eV",
        "/my_entry/nxodd_name/posint_value": np.array([1, 2, 3], dtype=np.int8),
        "/my_entry/nxodd_name/posint_value/@units": "kg",
        "/my_entry/nxodd_name/char_value": "just chars",
        "/my_entry/nxodd_name/char_value/@units": "",
        "/my_entry/nxodd_name/type": "2nd type",
        "/my_entry/nxodd_name/date_value": "2022-01-22T12:14:12.05018+00:00",
        "/my_entry/nxodd_name/date_value/@units": "",
        "/my_entry/nxodd_two_name/bool_value": True,
        "/my_entry/nxodd_two_name/bool_value/@units": "",
        "/my_entry/nxodd_two_name/int_value": 2,
        "/my_entry/nxodd_two_name/int_value/@units": "eV",
        "/my_entry/nxodd_two_name/posint_value": np.array([1, 2, 3], dtype=np.int8),
        "/my_entry/nxodd_two_name/posint_value/@units": "kg",
        "/my_entry/nxodd_two_name/char_value": "just chars",
        "/my_entry/nxodd_two_name/char_value/@units": "",
        "/my_entry/nxodd_two_name/type": "2nd type",
        "/my_entry/nxodd_two_name/date_value": "2022-01-22T12:14:12.05018+00:00",
        "/my_entry/nxodd_two_name/date_value/@units": "",
        "/my_entry/my_group/required_field": 1,
        "/my_entry/definition": "NXtest",
        "/my_entry/definition/@version": "2.4.6",
        "/my_entry/program_name": "Testing program",
        "/my_entry/my_group/optional_field": 1,
        "/my_entry/required_group/description": "An example description",
        "/my_entry/required_group2/description": "An example description",
        "/my_entry/optional_parent/req_group_in_opt_group/data": 1,
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
            remove_from_dict("/my_entry/nxodd_name/float_value", get_data_dict()),
            id="removed-optional-value",
        ),
    ],
)
def test_valid_data_dict(caplog, data_dict):
    with caplog.at_level(logging.WARNING):
        validate_dict_against("NXtest", data_dict, ignore_undocumented=True)
    assert caplog.text == ""


@pytest.mark.parametrize(
    "data_dict, error_message",
    [
        pytest.param(
            remove_from_dict("/my_entry/nxodd_name/bool_value", get_data_dict()),
            "The data entry corresponding to /my_entry/nxodd_name/bool_value is required and hasn't been supplied by the reader.",
            id="missing-required-value",
        )
    ],
)
def test_validation_shows_warning(caplog, data_dict, error_message):
    with caplog.at_level(logging.WARNING):
        validate_dict_against("NXtest", data_dict, ignore_undocumented=True)

    assert error_message in caplog.text