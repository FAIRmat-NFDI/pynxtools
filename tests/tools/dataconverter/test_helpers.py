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
from nexusparser.tools.dataconverter.template import Template


def alter_dict(data_dict: Template, key: str, value: object):
    """Helper function to alter a single entry in dict for parametrize."""
    if data_dict is not None:
        internal_dict = Template(data_dict)
        internal_dict[key] = value
        return internal_dict

    return None


def listify_template(data_dict: Template):
    """Helper function to turn most values in the Template into lists"""
    listified_template = Template()
    for optionality in ("optional", "recommended", "required", "undocumented"):
        for path in data_dict[optionality]:
            if path[path.rindex("/") + 1:] in ("@units", "type", "definition", "date_value"):
                listified_template[optionality][path] = data_dict[optionality][path]
            else:
                listified_template[optionality][path] = [data_dict[optionality][path]]
    return listified_template


@pytest.fixture(name="nxdl_root")
def fixture_nxdl_root():
    """pytest fixture to load the same NXDL file for all tests."""
    nxdl_file = os.path.join("tests", "data", "tools", "dataconverter", "NXtest.nxdl.xml")
    yield ET.parse(nxdl_file).getroot()


@pytest.fixture(name="template")
def fixture_template():
    """pytest fixture to use the same template in all tests"""
    nxdl_root = ET.parse("tests/data/tools/dataconverter/NXtest.nxdl.xml").getroot()
    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)
    yield template


@pytest.mark.usefixtures("template")
@pytest.fixture(name="filled_test_data")
def fixture_filled_test_data(template):
    """pytest fixture to setup a filled in template."""
    template.clear()
    template["optional"]["/ENTRY[my_entry]/NXODD_name/float_value"] = 2.0
    template["optional"]["/ENTRY[my_entry]/NXODD_name/float_value/@units"] = "nm"
    template["optional"]["/ENTRY[my_entry]/optional_parent/required_child"] = 1
    template["optional"]["/ENTRY[my_entry]/optional_parent/optional_child"] = 1
    template["required"]["/ENTRY[my_entry]/NXODD_name/bool_value"] = True
    template["required"]["/ENTRY[my_entry]/NXODD_name/int_value"] = 2
    template["required"]["/ENTRY[my_entry]/NXODD_name/int_value/@units"] = "eV"
    template["required"]["/ENTRY[my_entry]/NXODD_name/posint_value"] = np.array([1, 2, 3],
                                                                                dtype=np.int8)
    template["required"]["/ENTRY[my_entry]/NXODD_name/posint_value/@units"] = "kg"
    template["required"]["/ENTRY[my_entry]/NXODD_name/char_value"] = "just chars"
    template["required"]["/ENTRY[my_entry]/definition"] = "NXtest"
    template["required"]["/ENTRY[my_entry]/definition/@version"] = "2.4.6"
    template["required"]["/ENTRY[my_entry]/program_name"] = "Testing program"
    template["required"]["/ENTRY[my_entry]/NXODD_name/type"] = "2nd type"
    template["required"]["/ENTRY[my_entry]/NXODD_name/date_value"] = ("2022-01-22T12"
                                                                      ":14:12.05018+00:00")
    template["undocumented"]["/ENTRY[my_entry]/does/not/exist"] = "random"
    yield template


TEMPLATE = Template()
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name/float_value"] = 2.0
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name/float_value/@units"] = "nm"
TEMPLATE["optional"]["/ENTRY[my_entry]/optional_parent/required_child"] = 1
TEMPLATE["optional"]["/ENTRY[my_entry]/optional_parent/optional_child"] = 1
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/bool_value"] = True
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/int_value"] = 2
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/int_value/@units"] = "eV"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/posint_value"] = np.array([1, 2, 3],
                                                                            dtype=np.int8)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/posint_value/@units"] = "kg"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/char_value"] = "just chars"
TEMPLATE["required"]["/ENTRY[my_entry]/definition"] = "NXtest"
TEMPLATE["required"]["/ENTRY[my_entry]/definition/@version"] = "2.4.6"
TEMPLATE["required"]["/ENTRY[my_entry]/program_name"] = "Testing program"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/type"] = "2nd type"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name/date_value"] = "2022-01-22T12:14:12.05018+00:00"
TEMPLATE["optional_parents"].append("/ENTRY[entry]/optional_parent")


@pytest.mark.parametrize("data_dict,error_message", [
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/int_value", "1"),
        ("The value at /ENTRY[my_entry]/NXODD_name/in"
         "t_value should be of Python type: (<class 'int'>, <cla"
         "ss 'numpy.ndarray'>, <class 'numpy.signedinteger'>),"
         " as defined in the NXDL as NX_INT."),
        id="string-instead-of-int"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/bool_value", "True"),
        ("The value at /ENTRY[my_entry]/NXODD_name/bool_value sh"
         "ould be of Python type: (<class 'bool'>, <class 'numpy.ndarray'>, <class '"
         "numpy.bool_'>), as defined in the NXDL as NX_BOOLEAN."),
        id="string-instead-of-bool"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/posint_value", -1),
        ("The value at /ENTRY[my_entry]/NXODD_name/posint_value "
         "should be a positive int."),
        id="negative-posint"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/char_value", 3),
        ("The value at /ENTRY[my_entry]/NXODD_name/char_value should be of Python type:"
         " (<class 'str'>, <class 'numpy.ndarray'>, <class 'numpy.chararray'>),"
         " as defined in the NXDL as NX_CHAR."),
        id="int-instead-of-chars"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/float_value", None),
        "",
        id="empty-optional-field"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/bool_value", None),
        ("The data entry corresponding to /ENTRY[entry]/NXODD_name/bool_value is"
         " required and hasn't been supplied by the reader."),
        id="empty-required-field"),
    pytest.param(
        alter_dict(TEMPLATE,
                   "/ENTRY[my_entry]/NXODD_name/date_value",
                   "2022-01-22T12:14:12.05018+00:00"),
        "",
        id="UTC-with-+00:00"),
    pytest.param(
        alter_dict(TEMPLATE,
                   "/ENTRY[my_entry]/NXODD_name/date_value",
                   "2022-01-22T12:14:12.05018Z"),
        "",
        id="UTC-with-Z"),
    pytest.param(
        alter_dict(TEMPLATE,
                   "/ENTRY[my_entry]/NXODD_name/date_value",
                   "2022-01-22T12:14:12.05018-00:00"),
        "The date at /ENTRY[my_entry]/NXODD_name/date_value should be a timezone aware"
        " ISO8601 formatted str. For example, 2022-01-22T12:14:12.05018Z or 2022-01-22"
        "T12:14:12.05018+00:00.",
        id="UTC-with--00:00"),
    pytest.param(
        listify_template(TEMPLATE),
        "",
        id="lists"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/NXODD_name/type", "Wrong option"),
        ("The value at /ENTRY[my_entry]/NXODD_name/type should be one of the following"
         " strings: [1st type,2nd type,3rd type,4th type]"),
        id="wrong-enum-choice"),
    pytest.param(
        alter_dict(TEMPLATE, "/ENTRY[my_entry]/optional_parent/required_child", None),
        ("The data entry, /ENTRY[my_entry]/optional_parent/optional_child, has an "
         "optional parent, /ENTRY[entry]/optional_parent, with required children set"
         ". Either provide no children for /ENTRY[entry]/optional_parent or provide "
         "all required ones."),
        id="atleast-one-required-child-not-provided-optional-parent"),
    pytest.param(
        alter_dict(alter_dict(TEMPLATE,
                              "/ENTRY[my_entry]/optional_parent/required_child",
                              None),
                   "/ENTRY[my_entry]/optional_parent/optional_child",
                   None),
        (""),
        id="no-child-provided-optional-parent"),
    pytest.param(
        TEMPLATE,
        "",
        id="valid-data-dict"),
])
def test_validate_data_dict(data_dict, error_message, template, nxdl_root, request):
    """Unit test for the data validation routine"""
    if request.node.callspec.id in ("valid-data-dict",
                                    "lists",
                                    "empty-optional-field",
                                    "UTC-with-+00:00",
                                    "UTC-with-Z",
                                    "no-child-provided-optional-parent"):
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
