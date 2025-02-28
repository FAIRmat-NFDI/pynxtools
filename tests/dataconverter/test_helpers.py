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

import logging
import os
import shutil
import xml.etree.ElementTree as ET
from typing import Optional

import numpy as np
import pytest
from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against


def remove_optional_parent(data_dict: Template):
    """Completely removes the optional group from the test Template."""
    internal_dict = Template(data_dict)
    del internal_dict["/ENTRY[my_entry]/optional_parent/required_child"]
    del internal_dict["/ENTRY[my_entry]/optional_parent/optional_child"]
    del internal_dict[
        "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]"
    ]

    return internal_dict


def alter_dict(data_dict: Template, key: str, value: object):
    """Helper function to alter a single entry in dict for parametrize."""
    if data_dict is not None:
        internal_dict = Template(data_dict)
        internal_dict[key] = value
        return internal_dict

    return None


def set_to_none_in_dict(data_dict: Optional[Template], key: str, optionality: str):
    """Helper function to forcefully set path to 'None'"""
    if data_dict is None:
        return None

    internal_dict = Template(data_dict)
    internal_dict[optionality][key] = None
    return internal_dict


def set_whole_group_to_none(
    data_dict: Optional[Template], key: str, optionality: str
) -> Optional[Template]:
    """Set a whole path to None in the dict"""
    if data_dict is None:
        return None

    internal_dict = Template(data_dict)
    for path in data_dict[optionality]:
        if path.startswith(key):
            internal_dict[optionality][path] = None
    return internal_dict


def remove_from_dict(data_dict: Template, key: str, optionality: str = "optional"):
    """Helper function to remove a key from dict"""
    if data_dict is not None and key in data_dict[optionality]:
        internal_dict = Template(data_dict)
        del internal_dict[optionality][key]
        return internal_dict

    return None


def listify_template(data_dict: Template):
    """Helper function to turn most values in the Template into lists"""
    listified_template = Template()
    for optionality in ("optional", "recommended", "required", "undocumented"):
        for path in data_dict[optionality]:
            if path[path.rindex("/") + 1 :] in (
                "@units",
                "type",
                "definition",
                "date_value",
            ):
                listified_template[optionality][path] = data_dict[optionality][path]
            else:
                listified_template[optionality][path] = [data_dict[optionality][path]]
    return listified_template


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("2.4E-23", 2.4e-23),
        ("28", 28),
        ("45.98", 45.98),
        ("test", "test"),
        (["59", "3.00005", "498E-36"], np.array([59.0, 3.00005, 4.98e-34])),
        ("23 34 444 5000", np.array([23.0, 34.0, 444.0, 5000.0])),
        ("xrd experiment", "xrd experiment"),
        (None, None),
    ],
)
def test_transform_to_intended_dt(input_data, expected_output):
    """Transform to possible numerical method."""
    result = helpers.transform_to_intended_dt(input_data)

    # Use pytest.approx for comparing floating-point numbers
    if isinstance(expected_output, np.ndarray):
        np.testing.assert_allclose(result, expected_output, rtol=1e-3)
    elif isinstance(expected_output, float):
        assert result == pytest.approx(expected_output, rel=1e-5)
    else:
        assert result == expected_output


@pytest.fixture(name="template")
def fixture_template():
    """pytest fixture to use the same template in all tests"""
    nxdl_root = ET.parse("src/pynxtools/data/NXtest.nxdl.xml").getroot()

    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)
    return template


@pytest.mark.usefixtures("template")
@pytest.fixture(name="filled_test_data")
def fixture_filled_test_data(template, tmp_path):
    """pytest fixture to setup a filled in template."""

    # Copy original measurement file to tmp dir,
    # because h5py.ExternalLink is modifying it while
    # linking the nxs file.
    shutil.copy(
        os.path.join(
            os.getcwd(), "src", "pynxtools", "data", "xarray_saved_small_calibration.h5"
        ),
        tmp_path,
    )

    template.clear()
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value"] = 2.0
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units"] = "nm"
    template["/ENTRY[my_entry]/optional_parent/required_child"] = 1
    template["/ENTRY[my_entry]/optional_parent/optional_child"] = 1
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value"] = True
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value"] = 2
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value/@units"] = "eV"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value"] = np.array(
        [1, 2, 3], dtype=np.int8
    )
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value/@units"] = "kg"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value"] = "just chars"
    template["/ENTRY[my_entry]/definition"] = "NXtest"
    template["/ENTRY[my_entry]/definition/@version"] = "2.4.6"
    template["/ENTRY[my_entry]/program_name"] = "Testing program"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type"] = "2nd type"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"] = (
        "2022-01-22T12:14:12.05018+00:00"
    )
    template["/ENTRY[my_entry]/required_group/description"] = "An example description"
    template["/ENTRY[my_entry]/required_group2/description"] = "An example description"
    template["/ENTRY[my_entry]/does/not/exist"] = "random"
    template["/ENTRY[my_entry]/links/ext_link"] = {
        "link": f"{tmp_path}/xarray_saved_small_calibration.h5:/axes/ax3"
    }
    return template


TEMPLATE = Template()
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value"] = 2.0  # pylint: disable=E1126
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units"] = (
    "nm"  # pylint: disable=E1126
)
TEMPLATE["optional"]["/ENTRY[my_entry]/optional_parent/required_child"] = 1  # pylint: disable=E1126
TEMPLATE["optional"]["/ENTRY[my_entry]/optional_parent/optional_child"] = 1  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value"] = True  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value/@units"] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value"] = 2  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value/@units"] = "eV"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value"] = np.array(
    [1, 2, 3],  # pylint: disable=E1126
    dtype=np.int8,
)  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value/@units"] = (
    "kg"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value"] = (
    "just chars"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value/@units"] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value"] = True  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value/@units"
] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value"] = 2  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value/@units"] = (
    "eV"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value"] = (
    np.array(
        [1, 2, 3],  # pylint: disable=E1126
        dtype=np.int8,
    )
)  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value/@units"
] = "kg"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value"] = (
    "just chars"  # pylint: disable=E1126
)
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value/@units"
] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/type"] = "2nd type"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value"] = (
    "2022-01-22T12:14:12.05018+00:00"  # pylint: disable=E1126
)
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value/@units"
] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field"] = 1  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/definition"] = "NXtest"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/definition/@version"] = "2.4.6"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/program_name"] = "Testing program"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type"] = "2nd type"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"] = (
    "2022-01-22T12:14:12.05018+00:00"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value/@units"] = ""
TEMPLATE["optional"]["/ENTRY[my_entry]/OPTIONAL_group[my_group]/optional_field"] = 1
TEMPLATE["optional"]["/ENTRY[my_entry]/required_group/description"] = (
    "An example description"
)
TEMPLATE["optional"]["/ENTRY[my_entry]/required_group2/description"] = (
    "An example description"
)
TEMPLATE["required"][
    "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]"
] = 1
TEMPLATE["lone_groups"] = [
    "/ENTRY[entry]/required_group",
    "/ENTRY[entry]/required_group2",
    "/ENTRY[entry]/optional_parent/req_group_in_opt_group",
]
TEMPLATE["optional"]["/@default"] = "Some NXroot attribute"

# "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/in"
# "t_value should be one of: (<class 'int'>, <cla"
# "ss 'numpy.ndarray'>, <class 'numpy.signedinteger'>),"
# " as defined in the NXDL as NX_INT."


# pylint: disable=too-many-arguments
@pytest.mark.parametrize(
    "data_dict,error_message",
    [
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                "not_a_num",
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/in"
                "t_value should be one of: (<class 'int'>, <class 'numpy"
                ".ndarray'>, <class 'numpy.int32'>, <class 'numpy.int64'>,"
                " <class 'numpy.int64'>, <class 'numpy.int8'>, <class 'numpy"
                ".int16'>, <class 'numpy.int32'>, <class 'numpy.int64'>, "
                "<class 'numpy.uint8'>, <class 'numpy.uint16'>, <class 'numpy"
                ".uint32'>, <class 'numpy.uint64'>, <class 'numpy.unsignedi"
                "nteger'>, <class 'numpy.signedinteger'>), as defined in "
                "the NXDL as NX_INT."
            ),
            id="string-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                "NOT_TRUE_OR_FALSE",
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value sh"
                "ould be one of: (<class 'bool'>, <class 'numpy.ndarray'>, <class '"
                "numpy.bool"
            ),
            id="string-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                {"link": "/a-link"},
            ),
            (""),
            id="link-dict-instead-of-bool",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value", -1
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value "
                "should be a positive int, but is -1."
            ),
            id="negative-posint",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value", 3
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value should be of Python type:"
                " (<class 'str'>, <class 'numpy.ndarray'>, <class 'numpy.chararray'>),"
                " as defined in the NXDL as NX_CHAR."
            ),
            id="int-instead-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value", None
            ),
            "",
            id="empty-optional-field",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                "required",
            ),
            (
                "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]"
                "/bool_value is"
                " required and hasn't been supplied by the reader."
            ),
            id="empty-required-field",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value",
                "required",
            ),
            (
                "The data entry corresponding to /ENTRY[my_entry]/"
                "NXODD_name[nxodd_two_name]/bool_value is"
                " required and hasn't been supplied by the reader."
            ),
            id="empty-required-field",
        ),
        pytest.param(
            remove_from_dict(
                remove_from_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value",
                    "required",
                ),
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                "required",
            ),
            (
                "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]"
                "/bool_value is"
                " required and hasn't been supplied by the reader."
            ),
            id="empty-required-field",
        ),
        pytest.param(
            set_whole_group_to_none(
                set_whole_group_to_none(
                    TEMPLATE,
                    "/ENTRY[my_entry]/NXODD_name",
                    "required",
                ),
                "/ENTRY[my_entry]/NXODD_name",
                "optional",
            ),
            ("The required group, /ENTRY[my_entry]/NXODD_name, hasn't been supplied."),
            id="all-required-fields-set-to-none",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018+00:00",
            ),
            "",
            id="UTC-with-+00:00",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018Z",
            ),
            "",
            id="UTC-with-Z",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018-00:00",
            ),
            "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"
            " = 2022-01-22T12:14:12.05018-00:00 should be a timezone aware"
            " ISO8601 formatted str. For example, 2022-01-22T12:14:12.05018Z or 2022-01-22"
            "T12:14:12.05018+00:00.",
            id="UTC-with--00:00",
        ),
        pytest.param(listify_template(TEMPLATE), "", id="lists"),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type", "Wrong option"
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type should "
                "be on of the following"
                " strings: ['1st type', '2nd type', '3rd type', '4th type']"
            ),
            id="wrong-enum-choice",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE, "/ENTRY[my_entry]/optional_parent/required_child", "optional"
            ),
            (
                "The data entry corresponding to /ENTRY[my_entry]/optional_parent/"
                "required_child is required and hasn't been supplied by the reader."
            ),
            id="atleast-one-required-child-not-provided-optional-parent",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field",
                "required",
            ),
            (
                "The data entry corresponding to /ENTRY[my_entry]/"
                "OPTIONAL_group[my_group]/required_field "
                "is required and hasn't been supplied by the reader."
            ),
            id="required-field-not-provided-in-variadic-optional-group",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/optional_field",
                "required",
            ),
            (""),
            id="required-field-provided-in-variadic-optional-group",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE, "/ENTRY[my_entry]/optional_parent/required_child", None
                ),
                "/ENTRY[my_entry]/optional_parent/optional_child",
                None,
            ),
            (""),
            id="no-child-provided-optional-parent",
        ),
        pytest.param(TEMPLATE, "", id="valid-data-dict"),
        pytest.param(
            remove_from_dict(TEMPLATE, "/ENTRY[my_entry]/required_group/description"),
            "The required group, /ENTRY[my_entry]/required_group, hasn't been supplied.",
            id="missing-empty-yet-required-group",
        ),
        pytest.param(
            remove_from_dict(TEMPLATE, "/ENTRY[my_entry]/required_group2/description"),
            "The required group, /ENTRY[my_entry]/required_group2, hasn't been supplied.",
            id="missing-empty-yet-required-group2",
        ),
        pytest.param(
            alter_dict(
                remove_from_dict(
                    TEMPLATE, "/ENTRY[my_entry]/required_group/description"
                ),
                "/ENTRY[entry]/required_group",
                None,
            ),
            "The required group, /ENTRY[my_entry]/required_group, hasn't been supplied.",
            id="allow-required-and-empty-group",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]",
                "required",
            ),
            (
                "The required group, /ENTRY[my_entry]/"
                "optional_parent/req_group_in_opt_group, "
                "hasn't been supplied."
            ),
            id="req-group-in-opt-parent-removed",
        ),
        pytest.param(
            remove_optional_parent(TEMPLATE), (""), id="opt-group-completely-removed"
        ),
    ],
)
def test_validate_data_dict(caplog, data_dict, error_message, request):
    """Unit test for the data validation routine."""
    if request.node.callspec.id in (
        "valid-data-dict",
        "lists",
        "empty-optional-field",
        "UTC-with-+00:00",
        "UTC-with-Z",
        "no-child-provided-optional-parent",
        "int-instead-of-chars",
        "link-dict-instead-of-bool",
        "opt-group-completely-removed",
        "required-field-provided-in-variadic-optional-group",
    ):
        with caplog.at_level(logging.WARNING):
            assert validate_dict_against("NXtest", data_dict)[0]
        assert caplog.text == ""
    # Missing required fields caught by logger with warning
    elif request.node.callspec.id in (
        "empty-required-field",
        "allow-required-and-empty-group",
        "req-group-in-opt-parent-removed",
        "missing-empty-yet-required-group",
        "missing-empty-yet-required-group2",
    ):
        assert "" == caplog.text
        captured_logs = caplog.records
        assert not validate_dict_against("NXtest", data_dict)[0]
        assert any(error_message in rec.message for rec in captured_logs)
    else:
        with caplog.at_level(logging.WARNING):
            assert not validate_dict_against("NXtest", data_dict)[0]

        assert error_message in caplog.text


@pytest.mark.parametrize(
    "nxdl_path,expected",
    [
        pytest.param(
            "/ENTRY/definition/@version",
            ["/ENTRY[entry]/definition/@version"],
            id="path-exists-in-dict",
        ),
        pytest.param("/RANDOM/does/not/@exist", [], id="path-does-not-exist-in-dict"),
    ],
)
def test_path_in_data_dict(nxdl_path, expected, template):
    """Unit test for helper function to check if an NXDL path exists in the reader dictionary."""
    assert helpers.path_in_data_dict(nxdl_path, tuple(template.keys())) == expected


def test_atom_type_extractor_and_hill_conversion():
    """
    Test atom type extractor and conversion to hill
    """

    test_chemical_formula = "(C38H54S4)n(NaO2)5(CH4)NH3B"
    expected_atom_types = ["C", "H", "B", "N", "Na", "O", "S"]

    atom_list = helpers.extract_atom_types(test_chemical_formula)

    assert expected_atom_types == atom_list


def test_writing_of_root_attributes(caplog):
    """
    Tests if all root attributes are populated
    """
    template = Template()
    filename = "my_nexus_file.nxs"
    with caplog.at_level(logging.WARNING):
        helpers.add_default_root_attributes(template, filename)
        helpers.write_nexus_def_to_entry(template, "entry", "NXtest")
        helpers.write_nexus_def_to_entry(template, "entry1", "NXtest")

    assert "" == caplog.text

    keys_added = template.keys()
    assert "/@NX_class" in keys_added
    assert template["/@NX_class"] == "NXroot"
    assert "/@file_name" in keys_added
    assert template["/@file_name"] == filename
    assert "/@file_time" in keys_added
    assert "/@file_update_time" in keys_added
    assert "/@NeXus_repository" in keys_added
    assert "/@NeXus_version" in keys_added
    assert "/@HDF5_version" in keys_added
    assert "/@h5py_version" in keys_added
    assert "/ENTRY[entry]/definition" in keys_added
    assert "/ENTRY[entry]/definition/@version" in keys_added
    assert "/ENTRY[entry1]/definition" in keys_added
    assert "/ENTRY[entry1]/definition/@version" in keys_added


def test_warning_on_root_attribute_overwrite(caplog):
    """
    A warning is emitted when a root attribute is overwritten
    by pynxtools.
    """
    template = Template()
    template["/@NX_class"] = "NXwrong"
    filname = "my_nexus_file.nxs"
    with caplog.at_level(logging.WARNING):
        helpers.add_default_root_attributes(template, filname)
    error_text = (
        "The NXroot entry '/@NX_class' (value: NXwrong) should not be changed by the reader. "
        "This is overwritten by the actually used value 'NXroot'"
    )
    assert error_text in caplog.text

    assert "/@NX_class" in template.keys()
    assert template["/@NX_class"] == "NXroot"


def test_warning_on_definition_changed_by_reader(caplog):
    template = Template()
    template["/ENTRY[entry]/definition"] = "NXwrong"
    with caplog.at_level(logging.WARNING):
        helpers.write_nexus_def_to_entry(template, "entry", "NXtest")

    error_text = (
        "The entry '/ENTRY[entry]/definition' (value: NXtest) should not be changed by the reader. "
        "This is overwritten by the actually used value 'NXwrong'"
    )
    assert error_text in caplog.text

    assert "/ENTRY[entry]/definition" in template.keys()
    assert template["/ENTRY[entry]/definition"] == "NXtest"
