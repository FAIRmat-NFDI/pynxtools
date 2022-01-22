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
"""Test cases for the helper functions used by the DataConverter."""

import xml.etree.ElementTree as ET
import os
import pytest
import numpy as np

import nexusparser.tools.dataconverter.helpers as helpers


def alter_dict(data_dict: dict, key: str, value: object):
    """Helper function to alter a single entry in dict for parametrize."""
    if data_dict is not None:
        internal_dict = dict(data_dict)
        internal_dict[key] = value
        return internal_dict

    return None


@pytest.fixture(name="nxdl_root")
def fixture_nxdl_root():
    """pytest fixtrue to load the same NXDL file for all tests."""
    nxdl_file = os.path.join("tests", "data", "tools", "dataconverter", "NXtest.nxdl.xml")
    yield ET.parse(nxdl_file).getroot()


@pytest.fixture(name="template")
def fixture_template():
    """pytest fixture to use the same template in all tests"""
    yield {
        "/ENTRY[entry]/NXODD_name/bool_value": None,
        "/ENTRY[entry]/NXODD_name/char_value": None,
        "/ENTRY[entry]/NXODD_name/float_value": None,
        "/ENTRY[entry]/NXODD_name/float_value/@units": None,
        "/ENTRY[entry]/NXODD_name/int_value": None,
        "/ENTRY[entry]/NXODD_name/int_value/@units": None,
        "/ENTRY[entry]/NXODD_name/posint_value": None,
        "/ENTRY[entry]/NXODD_name/posint_value/@units": None,
        "/ENTRY[entry]/NXODD_name/type": None,
        "/ENTRY[entry]/definition": None,
        "/ENTRY[entry]/definition/@version": None,
        "/ENTRY[entry]/program_name": None
    }


VALID_DATA_DICT = {
    "/ENTRY[my_entry]/NXODD_name/float_value": 2.0,
    "/ENTRY[my_entry]/NXODD_name/float_value/@units": "nm",
    "/ENTRY[my_entry]/NXODD_name/bool_value": True,
    "/ENTRY[my_entry]/NXODD_name/int_value": 2,
    "/ENTRY[my_entry]/NXODD_name/int_value/@units": "eV",
    "/ENTRY[my_entry]/NXODD_name/posint_value": np.array([1, 2, 3], dtype=np.int8),
    "/ENTRY[my_entry]/NXODD_name/posint_value/@units": "kg",
    "/ENTRY[my_entry]/NXODD_name/char_value": "just chars",
    "/ENTRY[my_entry]/definition": "NXtest",
    "/ENTRY[my_entry]/definition/@version": "2.4.6",
    "/ENTRY[my_entry]/program_name": "Testing program",
    "/ENTRY[my_entry]/NXODD_name/type": "2nd type"
}


@pytest.mark.parametrize("data_dict,error_message", [
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/int_value", "1"),
        ("The value at /ENTRY[my_entry]/NXODD_name/in"
         "t_value should be of Python type: (<class 'int'>, <cla"
         "ss 'numpy.ndarray'>, <class 'numpy.signedinteger'>),"
         " as defined in the NXDL as NX_INT."),
        id="string-instead-of-int"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/bool_value", "True"),
        ("The value at /ENTRY[my_entry]/NXODD_name/bool_value sh"
         "ould be of Python type: (<class 'bool'>, <class 'numpy.ndarray'>, <class '"
         "numpy.bool_'>), as defined in the NXDL as NX_BOOLEAN."),
        id="string-instead-of-bool"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/posint_value", -1),
        ("The value at /ENTRY[my_entry]/NXODD_name/posint_value "
         "should be a positive int."),
        id="negative-posint"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/char_value", 3),
        ("The value at /ENTRY[my_entry]/NXODD_name/char_value should be of Python type:"
         " (<class 'str'>, <class 'numpy.ndarray'>, <class 'numpy.chararray'>),"
         " as defined in the NXDL as NX_CHAR."),
        id="int-instead-of-chars"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/float_value", None),
        (""),
        id="empty-optional-field"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/bool_value", None),
        ("The data entry, /ENTRY[my_entry]/NXODD_name/bool_value, is required and "
         "hasn't been supplied by the reader."),
        id="empty-required-field"),
    pytest.param(
        {
            "/ENTRY[my_entry]/NXODD_name/float_value": [2.0],
            "/ENTRY[my_entry]/NXODD_name/float_value/@units": "nm",
            "/ENTRY[my_entry]/NXODD_name/bool_value": [True],
            "/ENTRY[my_entry]/NXODD_name/int_value": [np.zeros(3), np.zeros(5)],
            "/ENTRY[my_entry]/NXODD_name/int_value/@units": "eV",
            "/ENTRY[my_entry]/NXODD_name/posint_value": [1, 2, 3],
            "/ENTRY[my_entry]/NXODD_name/posint_value/@units": "kg",
            "/ENTRY[my_entry]/NXODD_name/char_value": ["just chars"],
            "/ENTRY[my_entry]/definition": "NXtest",
            "/ENTRY[my_entry]/definition/@version": ["2.4.6"],
            "/ENTRY[my_entry]/program_name": ["Testing program"],
            "/ENTRY[my_entry]/NXODD_name/type": "2nd type"
        }, "",
        id="lists"),
    pytest.param(
        alter_dict(VALID_DATA_DICT, "/ENTRY[my_entry]/NXODD_name/type", "Wrong option"),
        ("The value at /ENTRY[my_entry]/NXODD_name/type should be one of the following"
         " strings: [1st type,2nd type,3rd type,4th type]"),
        id="wrong-enum-choice"),
    pytest.param(
        VALID_DATA_DICT,
        "",
        id="valid-data-dict"),
])
def test_validate_data_dict(data_dict, error_message, template, nxdl_root, request):
    """Unit test for the data validation routine"""
    if request.node.callspec.id in ("valid-data-dict", "lists", "empty-optional-field"):
        helpers.validate_data_dict(template, data_dict, nxdl_root)
    else:
        with pytest.raises(Exception) as execinfo:
            helpers.validate_data_dict(template, data_dict, nxdl_root)

        assert (error_message) == str(execinfo.value)


@pytest.mark.parametrize("nxdl_path,expected", [
    pytest.param(
        "/ENTRY/definition/@version",
        (True, "/ENTRY[entry]/definition/@version"),
        id="path-exists-in-dict"),
    pytest.param(
        "/RANDOM/does/not/@exist",
        (False, ""),
        id="path-does-not-exist-in-dict")
])
def test_path_in_data_dict(nxdl_path, expected, template):
    """Unit test for helper function to check if an NXDL path exists in the reader dictionary."""
    assert helpers.path_in_data_dict(nxdl_path, template) == expected
