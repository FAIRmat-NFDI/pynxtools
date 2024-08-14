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
from typing import Optional

from click.testing import CliRunner
import numpy as np
import pytest

from pynxtools.dataconverter.helpers import get_nxdl_root_and_path
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against
from pynxtools.dataconverter.verify import verify
from pynxtools.dataconverter.writer import Writer

from .test_helpers import alter_dict  # pylint: disable=unused-import


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


def compress_paths_in_dict(data_dict: Template, paths=list[str]):
    """For each path, compress the value in data_dict using a strength of 3."""
    types = {
        "int": np.int64,
        "float": np.float32,
    }
    if data_dict is not None:
        internal_dict = Template(data_dict)
        for path in paths:
            if (value := internal_dict.get(path)) is not None:
                if np_type := types.get(type(value).__name__):
                    value = np_type(value)
                internal_dict[path] = {"compress": value, "strength": 3}
        return internal_dict

    return None


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
                "@signal",
            ) or isinstance(data_dict[optionality][path], list):
                listified_template[optionality][path] = data_dict[optionality][path]
            else:
                listified_template[optionality][path] = [data_dict[optionality][path]]
    return listified_template


TEMPLATE = Template()
TEMPLATE["required"]["/ENTRY[my_entry]/definition"] = "NXtest"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/definition/@version"] = "2.4.6"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/program_name"] = "Testing program"  # pylint: disable=E1126

TEMPLATE["required"]["/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field"] = 1
TEMPLATE["optional"]["/ENTRY[my_entry]/OPTIONAL_group[my_group]/optional_field"] = 1

TEMPLATE["required"][
    "/ENTRY[my_entry]/specified_group_with_no_name_type/specified_field_with_no_name_type"
] = 1.0
TEMPLATE["required"][
    "/ENTRY[my_entry]/specified_group_with_no_name_type/specified_field_with_no_name_type/@units"
] = "eV"
TEMPLATE["required"][
    "/ENTRY[my_entry]/specified_group_with_no_name_type/specified_field_with_no_name_type/@specified_attr_in_field_with_no_name_type"
] = "data"
TEMPLATE["required"][
    "/ENTRY[my_entry]/specified_group_with_no_name_type/@specified_attr_with_no_name_type"
] = "attr"

TEMPLATE["required"]["/ENTRY[my_entry]/specified_group/specified_field"] = 1.0
TEMPLATE["required"]["/ENTRY[my_entry]/specified_group/specified_field/@units"] = "cm"
TEMPLATE["required"][
    "/ENTRY[my_entry]/specified_group/specified_field/@specified_attr_in_field"
] = "attr"
TEMPLATE["required"]["/ENTRY[my_entry]/specified_group/@specified_attr"] = "attr"


TEMPLATE["optional"][
    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]"
] = 1.0
TEMPLATE["optional"][
    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@units"
] = "pixel"
TEMPLATE["required"][
    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@any_attrATTR_in_field[@any_attrATTR_in_field]"
] = "attr"
TEMPLATE["required"][
    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/@any_attrATTR[@any_attrATTR]"
] = "attr"

TEMPLATE["optional"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]"
] = 2
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value"] = 2.0  # pylint: disable=E1126
TEMPLATE["optional"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units"] = (
    "eV"  # pylint: disable=E1126
)
TEMPLATE["optional"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/DATA[float_value_no_attr]"
] = (2.0,)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value"] = 2
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units"] = (
    "eV"
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value"] = True  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value/@units"] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value"] = 2  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value/@units"] = "nm"  # pylint: disable=E1126

TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value"] = np.array(
    [1, 2, 3],  # pylint: disable=E1126
    dtype=np.int8,
)  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value/@units"] = (
    "mm"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value"] = (
    "just chars"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value/@units"] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/@group_attribute"] = (
    "data"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"] = (
    "2022-01-22T12:14:12.05018+00:00"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value/@units"] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type"] = "2nd type"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array"] = [0, 1, 2]
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/@signal"] = "data"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/DATA[data]"] = 1  # pylint: disable=E1126

TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value"] = True  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value/@units"
] = ""
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/anamethatRENAMES[anamethatichangetothis]"
] = 2  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value"] = 2  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/int_value/@units"] = (
    "m"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value"] = (
    np.array(
        [1, 2, 3],  # pylint: disable=E1126
        dtype=np.int8,
    )
)  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/posint_value/@units"
] = "cm"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value"] = (
    "just chars"  # pylint: disable=E1126
)
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/char_value/@units"
] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/type"] = "2nd type"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/type/@array"] = [
    0,
    1,
    2,
]
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value"] = (
    "2022-01-22T12:14:12.05018+00:00"  # pylint: disable=E1126
)
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/date_value/@units"
] = ""
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/@group_attribute"] = (
    "data"  # pylint: disable=E1126
)
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/@signal"] = "data"
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/DATA[data]"] = 1  # pylint: disable=E1126

TEMPLATE["optional"]["/ENTRY[my_entry]/required_group/description"] = (
    "An example description"
)
TEMPLATE["optional"]["/ENTRY[my_entry]/required_group2/description"] = (
    "An example description"
)

TEMPLATE["required"]["/ENTRY[my_entry]/optional_parent/required_child"] = 1  # pylint: disable=E1126
TEMPLATE["optional"]["/ENTRY[my_entry]/optional_parent/optional_child"] = 1  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]"
] = 1
TEMPLATE["lone_groups"] = [
    "/ENTRY[entry]/required_group",
    "/ENTRY[entry]/required_group2",
    "/ENTRY[entry]/optional_parent/req_group_in_opt_group",
]
TEMPLATE["optional"]["/@default"] = "Some NXroot attribute"
# keys not registered in appdef
TEMPLATE["required"]["/ENTRY[my_entry]/duration"] = 1  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/duration/@units"] = "s"  # pylint: disable=E1126
TEMPLATE["required"][
    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type"
] = "Ion Source"  # pylint: disable=E1126


# pylint: disable=too-many-arguments
@pytest.mark.parametrize(
    "data_dict,error_messages",
    [
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NOTE[required_group2]/description",
                "an additional description",
            ),
            [
                "The key '/ENTRY[my_entry]/NOTE[required_group2]/description' uses the valid concept name 'NOTE', "
                "but there is another valid key /ENTRY[my_entry]/required_group2/description that uses the non-variadic "
                "name of the node.'",
                "The key /ENTRY[my_entry]/NOTE[required_group2]/description will not be written.",
            ],
            id="same-concept-with-and-without-concept-name",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        alter_dict(
                            alter_dict(
                                TEMPLATE,
                                "/ENTRY[my_entry]/SAMPLE[some_name]/name",
                                "A sample name",
                            ),
                            "/ENTRY[my_entry]/SAMPLE[some_name]/description",
                            "A sample description",
                        ),
                        "/ENTRY[my_entry]/USER[some_name]/name",
                        "A user name",
                    ),
                    "/ENTRY[my_entry]/MONITOR[some_name]/name",
                    "A monitor name",
                ),
                "/ENTRY[my_entry]/MONITOR[some_name]/description",
                "A monitor description",
            ),
            [
                "Instance name 'some_name' used for multiple different concepts: MONITOR, SAMPLE, USER. "
                "The following keys are affected: /ENTRY[my_entry]/MONITOR[some_name]/description, "
                "/ENTRY[my_entry]/MONITOR[some_name]/name, /ENTRY[my_entry]/SAMPLE[some_name]/description, "
                "/ENTRY[my_entry]/SAMPLE[some_name]/name, /ENTRY[my_entry]/USER[some_name]/name.",
                "The key /ENTRY[my_entry]/MONITOR[some_name]/description will not be written.",
                "The key /ENTRY[my_entry]/MONITOR[some_name]/name will not be written.",
                "The key /ENTRY[my_entry]/SAMPLE[some_name]/description will not be written.",
                "The key /ENTRY[my_entry]/SAMPLE[some_name]/name will not be written.",
                "The key /ENTRY[my_entry]/USER[some_name]/name will not be written.",
            ],
            id="variadic-groups-of-the-same-name",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/INSTRUMENT[instrument]/APERTURE[another_name]/name",
                        "An aperture within an instrument",
                    ),
                    "/ENTRY[my_entry]/INSTRUMENT[instrument]/DETECTOR[another_name]/name",
                    "A detector within an instrument",
                ),
                "/ENTRY[my_entry]/INSTRUMENT[instrument]/SOURCE[my_source]/APERTURE[another_name]/name",
                "An aperture within a source inside an instrument",
            ),
            [
                "Instance name 'another_name' used for multiple different concepts: APERTURE, DETECTOR. "
                "The following keys are affected: /ENTRY[my_entry]/INSTRUMENT[instrument]/APERTURE[another_name]/name, "
                "/ENTRY[my_entry]/INSTRUMENT[instrument]/DETECTOR[another_name]/name.",
                "The key /ENTRY[my_entry]/INSTRUMENT[instrument]/APERTURE[another_name]/name will not be written.",
                "The key /ENTRY[my_entry]/INSTRUMENT[instrument]/DETECTOR[another_name]/name will not be written.",
            ],
            id="variadic-groups-of-the-same-name-but-at-different-levels",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        alter_dict(
                            alter_dict(
                                alter_dict(
                                    TEMPLATE,
                                    "/ENTRY[my_entry]/USER[user]/name",
                                    "A user name",
                                ),
                                "/ENTRY[my_entry]/USER[user]/role",
                                "A user role",
                            ),
                            "/ENTRY[my_entry]/USER[user]/affiliation",
                            "A user affiliation",
                        ),
                        "/ENTRY[my_entry]/ILLEGAL[user]/name",
                        "An illegal user name",
                    ),
                    "/ENTRY[my_entry]/ILLEGAL[user]/role",
                    "An illegal user role",
                ),
                "/ENTRY[my_entry]/ILLEGAL[user]/affiliation",
                "An illegal user affiliation",
            ),
            [
                "Instance name 'user' used for multiple different concepts: ILLEGAL, USER. "
                "The following keys are affected: /ENTRY[my_entry]/ILLEGAL[user]/affiliation, /ENTRY[my_entry]/ILLEGAL[user]/name, "
                "/ENTRY[my_entry]/ILLEGAL[user]/role, /ENTRY[my_entry]/USER[user]/affiliation, /ENTRY[my_entry]/USER[user]/name, "
                "/ENTRY[my_entry]/USER[user]/role.",
                "The key /ENTRY[my_entry]/ILLEGAL[user]/affiliation will not be written.",
                "The key /ENTRY[my_entry]/ILLEGAL[user]/name will not be written.",
                "The key /ENTRY[my_entry]/ILLEGAL[user]/role will not be written.",
            ],
            id="variadic-groups-of-the-same-name-illegal-concept-multiple-fields",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/USER[user]/name",
                        "A user name",
                    ),
                    "/ENTRY[my_entry]/USERS[user]/name",
                    "An invalid group of the same name",
                ),
                "/ENTRY[my_entry]/SAMPLE[user]/name",
                "A sample group called user with a name",
            ),
            [
                "Instance name 'user' used for multiple different concepts: SAMPLE, USER, USERS. "
                "The following keys are affected: /ENTRY[my_entry]/SAMPLE[user]/name, "
                "/ENTRY[my_entry]/USERS[user]/name, /ENTRY[my_entry]/USER[user]/name.",
                "The key /ENTRY[my_entry]/USERS[user]/name will not be written.",
                "The key /ENTRY[my_entry]/SAMPLE[user]/name will not be written.",
                "The key /ENTRY[my_entry]/USER[user]/name will not be written.",
            ],
            id="variadic-groups-of-the-same-name-mix-of-valid-and-illegal-concepts",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        remove_from_dict(
                            remove_from_dict(
                                remove_from_dict(
                                    remove_from_dict(
                                        TEMPLATE,
                                        "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]",
                                        "optional",
                                    ),
                                    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@units",
                                    "optional",
                                ),
                                "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@any_attrATTR_in_field[@any_attrATTR_in_field]",
                                "required",
                            ),
                            "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/@any_attrATTR[@any_attrATTR]",
                            "required",
                        ),
                        "/ENTRY[my_entry]/any_groupGROUP[some_group_name]/any_fieldFIELD[some_field_name]",
                        1.0,
                    ),
                    "/ENTRY[my_entry]/any_groupGROUP[some_group_name]/any_fieldFIELD[some_field_name]/@any_attrATTR_in_field[@some_attr_name]",
                    "new attr",
                ),
                "/ENTRY[my_entry]/any_groupGROUP[some_group_name]/@any_attrATTR[@some_attr_name]",
                "new attr",
            ),
            [],
            id="name-type-any",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]",
                "not_a_num",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]"
                " should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in "
                "the NXDL as NX_INT."
            ],
            id="variadic-field-str-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                "not_a_num",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/in"
                "t_value should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in "
                "the NXDL as NX_INT."
            ],
            id="string-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                "NOT_TRUE_OR_FALSE",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value should be one of the following Python types: (<class 'bool'>, <class 'numpy.bool_'>), as defined in the NXDL as NX_BOOLEAN."
            ],
            id="string-instead-of-bool",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                ["1", "2", "3"],
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value should"
                " be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT."
            ],
            id="list-of-int-str-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                np.array([2.0, 3.0, 4.0], dtype=np.float32),
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value should be"
                " one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT."
            ],
            id="array-of-float-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                [2, 3, 4],
            ),
            [],
            id="list-of-int-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                np.array([2, 3, 4], dtype=np.int32),
            ),
            [],
            id="array-of-int32-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018-00:00",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"
                " = 2022-01-22T12:14:12.05018-00:00 should be a timezone aware"
                " ISO8601 formatted str. For example, 2022-01-22T12:14:12.05018Z or 2022-01-22"
                "T12:14:12.05018+00:00."
            ],
            id="int-instead-of-date",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                0,
            ),
            [],
            id="int-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.complex128(0),
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value should be one of the following Python types: (<class 'float'>, <class 'numpy.floating'>), as defined in the NXDL as NX_FLOAT."
            ],
            id="complex-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value",
                "0",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>, <class 'float'>, <class 'numpy.floating'>), as defined in the NXDL as NX_NUMBER."
            ],
            id="str-instead-of-number",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array([0.0, 2]),
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value should be one"
                " of the following Python types: (<class 'str'>, <class 'numpy.character'>), as"
                " defined in the NXDL as NX_CHAR."
            ],
            id="wrong-type-ndarray-instead-of-char",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["x", "2"]),
            ),
            [],
            id="valid-ndarray-instead-of-char",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                {"link": "/a-link"},
            ),
            [
                "Broken link at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value to /a-link.",
                "The key /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value will not be written.",
                "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value is required and hasn't been supplied by the reader.",
            ],
            id="link-dict-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value", -1
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value "
                "should be a positive int, but is -1."
            ],
            id="negative-posint",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                [-1, 2],
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value "
                "should be a positive int, but is [-1, 2]."
            ],
            id="negative-posint-list",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                np.array([-1, 2], dtype=np.int8),
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value should"
                " be a positive int, but is [-1  2]."
            ],
            id="negative-posint-array",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                [1, 2],
            ),
            [],
            id="positive-posint-list",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                np.array([1, 2], dtype=np.int8),
            ),
            [],
            id="positive-posint-array",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value", 3
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value should be one of the following Python types:"
                " (<class 'str'>, <class 'numpy.character'>),"
                " as defined in the NXDL as NX_CHAR."
            ],
            id="int-instead-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["1", "2", "3"], dtype=np.str_),
            ),
            [],
            id="array-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["1", "2", "3"], dtype=np.bytes_),
            ),
            [],
            id="array-of-bytes-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                ["list", "of", "chars"],
            ),
            [],
            id="list-of-string-instead-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value", None
            ),
            [],
            id="empty-optional-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.array([2.0, 3.0, 4.0], dtype=np.float32),
            ),
            [],
            id="array-of-float-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.array(["2.0", "3.0"], dtype=np.str_),
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value should be "
                "one of the following Python types: (<class 'float'>, <class 'numpy.floating'>), as defined in the NXDL "
                "as NX_FLOAT."
            ],
            id="array-of-str-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                [2],  # pylint: disable=E1126
            ),
            [],
            id="list-of-int-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.array([2]),  # pylint: disable=E1126
            ),
            [],
            id="array-of-int-instead-of-float",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                "required",
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value "
                "is required and hasn't been supplied by the reader.",
                "There were attributes set for the field /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value, but the field does not exist.",
            ],
            id="empty-required-field",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value",
                "required",
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/"
                "NXODD_name[nxodd_two_name]/bool_value is"
                " required and hasn't been supplied by the reader.",
                "There were attributes set for the field /ENTRY[my_entry]/NXODD_name[nxodd_two_name]/bool_value, but the field does not exist.",
            ],
            id="empty-required-field",
        ),
        pytest.param(
            remove_from_dict(
                remove_from_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]",
                    "optional",
                ),
                "/ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@units",
                "optional",
            ),
            [
                "There were attributes set for the field /ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD], "
                "but the field does not exist.",
                "The attribute /ENTRY[my_entry]/any_groupGROUP[any_groupGROUP]/any_fieldFIELD[any_fieldFIELD]/@any_attrATTR_in_field[@any_attrATTR_in_field] "
                "will not be written.",
            ],
            id="removed-optional-value-with-attribute-remaining",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                "optional",
            ),
            [
                "Unit /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units in dataset without its field /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value.",
                "The attribute /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units will not be written.",
            ],
            id="removed-optional-value-with-unit-remaining",
        ),
        pytest.param(
            remove_from_dict(
                remove_from_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                    "required",
                ),
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value/@units",
                "required",
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value is required and hasn't been supplied by the reader."
            ],
            id="missing-required-value",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/@group_attribute",
                "required",
            ),
            [
                'Missing attribute: "/ENTRY[my_entry]/NXODD_name[nxodd_name]/@group_attribute"'
            ],
            id="missing-required-group-attribute",
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
            ["The required group, /ENTRY[my_entry]/NXODD_name, hasn't been supplied."],
            id="all-required-fields-set-to-none",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018+00:00",
            ),
            [],
            id="UTC-with-+00:00",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018Z",
            ),
            [],
            id="UTC-with-Z",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                "2022-01-22T12:14:12.05018-00:00",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"
                " = 2022-01-22T12:14:12.05018-00:00 should be a timezone aware"
                " ISO8601 formatted str. For example, 2022-01-22T12:14:12.05018Z or 2022-01-22"
                "T12:14:12.05018+00:00."
            ],
            id="UTC-with--00:00",
        ),
        pytest.param(listify_template(TEMPLATE), "", id="lists"),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type", "Wrong option"
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type should "
                "be one of the following"
                ": ['1st type', '2nd type', '3rd type', '4th type']."
            ],
            id="wrong-enum-choice",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type2",
                "a very different type",
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type2 does not match with the "
                "enumerated items from the open enumeration: ['1st type open', '2nd type open']."
            ],
            id="open-enum-with-new-item",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE, "/ENTRY[my_entry]/optional_parent/required_child", "required"
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/optional_parent/"
                "required_child is required and hasn't been supplied by the reader."
            ],
            id="atleast-one-required-child-not-provided-optional-parent",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field",
                "required",
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/"
                "OPTIONAL_group[my_group]/required_field "
                "is required and hasn't been supplied by the reader."
            ],
            id="required-field-not-provided-in-variadic-optional-group",
        ),
        pytest.param(
            set_to_none_in_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/optional_field",
                "required",
            ),
            [],
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
            [],
            id="no-child-provided-optional-parent",
        ),
        pytest.param(
            alter_dict(
                remove_from_dict(
                    remove_from_dict(
                        remove_from_dict(
                            remove_from_dict(
                                TEMPLATE,
                                "/ENTRY[my_entry]/specified_group/specified_field",
                                "required",
                            ),
                            "/ENTRY[my_entry]/specified_group/specified_field/@units",
                            "required",
                        ),
                        "/ENTRY[my_entry]/specified_group/specified_field/@specified_attr_in_field",
                        "required",
                    ),
                    "/ENTRY[my_entry]/specified_group/@specified_attr",
                    "required",
                ),
                "/ENTRY[my_entry]/SAMPLE[specified_group]/specified_field",
                1.0,
            ),
            [
                "The required group, /ENTRY[my_entry]/specified_group, hasn't been supplied.",
                "Given group name 'SAMPLE' conflicts with the non-variadic name 'specified_group (req)', "
                "which should be of type NXdata.",
                "Field /ENTRY[my_entry]/SAMPLE[specified_group]/specified_field written without documentation.",
            ],
            id="illegal-concept-name-for-nonvariadic-group",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    remove_from_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/optional_parent/required_child",
                        "required",
                    ),
                    "/ENTRY[my_entry]/optional_parent/AXISNAME[required_child]",
                    1,
                ),
                "/ENTRY[my_entry]/optional_parent/AXISNAME[optional_child]",
                1,
            ),
            [],
            id="concept-name-given-for-nonvariadic-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/optional_parent/@AXISNAME_indices[@required_child_indices]",
                0,
            ),
            [],
            id="concept-name-given-for-optional-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/identified_calibration/identifier_1/some_field",
                "123",
            ),
            [
                "Expected a field at /ENTRY[my_entry]/identified_calibration/identifier_1 but found a group.",
                "The type ('group') of the given concept 'identifier_1' conflicts with another "
                "existing concept of the same name, which is of type 'field'.",
                "The field /ENTRY[my_entry]/identified_calibration/identifier_1/some_field will not be written.",
            ],
            id="group-instead-of-named-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/identified_calibration",
                "123",
            ),
            [
                "The type ('field') of the given concept 'identified_calibration' conflicts with another "
                "existing concept of the same name, which is of type 'group'.",
                "The field /ENTRY[my_entry]/identified_calibration will not be written.",
            ],
            id="field-instead-of-named-group",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/identified_calibration",
                    {"link": "/my_entry/some_group"},
                ),
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                {"link": "/my_entry/specified_group/some_field"},
            ),
            [
                "Broken link at /ENTRY[my_entry]/identified_calibration to /my_entry/some_group.",
                "The key /ENTRY[my_entry]/identified_calibration will not be written.",
                "Broken link at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value to /my_entry/specified_group/some_field.",
                "The key /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value will not be written.",
            ],
            id="appdef-broken-links",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    remove_from_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/required_group/description",
                        "optional",
                    ),
                    "/ENTRY[my_entry]/required_group",
                    {"link": "/my_entry/required_group2"},
                ),
                "/ENTRY[my_entry]/OPTIONAL_group[some_group]/required_field",
                {"link": "/my_entry/specified_group/specified_field"},
            ),
            [],
            id="appdef-links-with-matching-nexus-types",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/USER[my_user]",
                    {"link": "/my_entry/my_group/required_field"},
                ),
                "/ENTRY[my_entry]/OPTIONAL_group[some_group]/required_field",
                {"link": "/my_entry/specified_group"},
            ),
            [
                "Expected a field at /ENTRY[my_entry]/OPTIONAL_group[some_group]/required_field but found a group.",
                "Expected a group at /ENTRY[my_entry]/USER[my_user] but found a field or attribute.",
                "Field /ENTRY[my_entry]/USER[my_user] written without documentation.",
            ],
            id="appdef-links-with-wrong-nexus-types",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/SAMPLE[my_sample]",
                    {"link": "/my_entry/some_group"},
                ),
                "/ENTRY[my_entry]/SAMPLE[my_sample2]/name",
                {"link": "/my_entry/specified_group/some_field223"},
            ),
            [
                "Broken link at /ENTRY[my_entry]/SAMPLE[my_sample] to /my_entry/some_group.",
                "The key /ENTRY[my_entry]/SAMPLE[my_sample] will not be written.",
                "Broken link at /ENTRY[my_entry]/SAMPLE[my_sample2]/name to /my_entry/specified_group/some_field223.",
                "The key /ENTRY[my_entry]/SAMPLE[my_sample2]/name will not be written.",
            ],
            id="baseclass-broken-links",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/SAMPLE[my_sample]",
                    {"link": "/my_entry/my_group"},
                ),
                "/ENTRY[my_entry]/SAMPLE[my_sample]/name",
                {"link": "/my_entry/nxodd_name/char_value"},
            ),
            [],
            id="baseclass-links-with-matching-nexus-types",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/SAMPLE[my_sample]",
                    {"link": "/my_entry/my_group/required_field"},
                ),
                "/ENTRY[my_entry]/SAMPLE[my_sample]/name",
                {"link": "/my_entry/my_group"},
            ),
            [
                "Expected a group at /ENTRY[my_entry]/SAMPLE[my_sample] but found a field or attribute.",
                "Field /ENTRY[my_entry]/SAMPLE[my_sample] written without documentation.",
                "Expected a field at /ENTRY[my_entry]/SAMPLE[my_sample]/name but found a group.",
            ],
            id="baseclass-links-with-wrong-nexus-types",
        ),
        pytest.param(
            alter_dict(
                remove_from_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/optional_parent/optional_child",
                    "optional",
                ),
                "/ENTRY[my_entry]/optional_parent/AXISNAME[optional_child]",
                "test value",
            ),
            [
                "The value at /ENTRY[my_entry]/optional_parent/AXISNAME[optional_child] should be "
                "one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as "
                "defined in the NXDL as NX_INT."
            ],
            id="concept-name-given-for-nonvariadic-field-wrong-type",
        ),
        pytest.param(TEMPLATE, "", id="valid-data-dict"),
        pytest.param(
            remove_from_dict(TEMPLATE, "/ENTRY[my_entry]/required_group/description"),
            [
                "The required group, /ENTRY[my_entry]/required_group, hasn't been supplied."
            ],
            id="missing-empty-yet-required-group",
        ),
        pytest.param(
            remove_from_dict(TEMPLATE, "/ENTRY[my_entry]/required_group2/description"),
            [
                "The required group, /ENTRY[my_entry]/required_group2, hasn't been supplied."
            ],
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
            [
                "The required group, /ENTRY[my_entry]/required_group, hasn't been supplied."
            ],
            id="allow-required-and-empty-group",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]",
                "required",
            ),
            [
                "The required group, /ENTRY[my_entry]/"
                "optional_parent/req_group_in_opt_group, "
                "hasn't been supplied."
            ],
            id="req-group-in-opt-parent-removed",
        ),
        pytest.param((TEMPLATE), (""), id="opt-group-completely-removed"),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array",
                ["0", 1, 2],
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT.",
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array should be one of the following: [[0, 1, 2], [2, 3, 4]].",
            ],
            id="wrong-type-array-in-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array", [1, 2]
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array should be one of the following: [[0, 1, 2], [2, 3, 4]]."
            ],
            id="wrong-value-array-in-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units",
                "m",
            ),
            [
                "The unit 'm' at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units does not match with the unit category NX_ENERGY of 'float_value'."
            ],
            id="appdef-invalid-units",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/duration",
                    2,
                ),
                "/ENTRY[my_entry]/duration/@units",
                "kg",
            ),
            [
                "The unit 'kg' at /ENTRY[my_entry]/duration/@units does not match with the unit category NX_TIME of 'duration'."
            ],
            id="baseclass-invalid-units",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/MONOCHROMATOR[monochromator]/energy_dispersion",
                    0.5,
                ),
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/MONOCHROMATOR[monochromator]/energy_dispersion/@units",
                "J/mm",
            ),
            [],
            id="baseclass-valid-unit-example",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/SAMPLE[sample1]]/changer_position",
                        1,
                    ),
                    "/ENTRY[my_entry]/SAMPLE[sample1]]/changer_position/@units",
                    "mm",
                ),
                "/ENTRY[my_entry]/SAMPLE[sample2]]/changer_position",
                1,
            ),
            [
                "The unit 'mm' at /ENTRY[my_entry]/SAMPLE[sample1]]/changer_position/@units does not match with the unit category NX_UNITLESS of 'changer_position'."
            ],
            id="baseclass-unitless-field",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        alter_dict(
                            alter_dict(
                                alter_dict(
                                    alter_dict(
                                        alter_dict(
                                            TEMPLATE,
                                            "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation]",
                                            1.0,
                                        ),
                                        "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation]/@transformation_type",
                                        "translation",
                                    ),
                                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation]/@units",
                                    "m",
                                ),
                                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_translation]",
                                1.0,
                            ),
                            "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_translation]/@transformation_type",
                            "rotation",
                        ),
                        "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_translation]/@units",
                        "m",
                    ),
                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation_no_units]",
                    1.0,
                ),
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation_no_units]/@transformation_type",
                "translation",
            ),
            [
                "The unit 'm' at /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_translation]/@units "
                "does not match with the unit category NX_TRANSFORMATION of 'AXISNAME'. Based on the 'transformation_type' of the field "
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_translation], "
                "it should match with 'NX_ANGLE'.",
                "Field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[translation_no_units] requires a unit "
                "in the unit category NX_TRANSFORMATION.",
            ],
            id="nxtransformations-translation-units",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        alter_dict(
                            alter_dict(
                                alter_dict(
                                    alter_dict(
                                        alter_dict(
                                            TEMPLATE,
                                            "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation]",
                                            1.0,
                                        ),
                                        "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation]/@transformation_type",
                                        "rotation",
                                    ),
                                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation]/@units",
                                    "degree",
                                ),
                                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_rotation]",
                                1.0,
                            ),
                            "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_rotation]/@transformation_type",
                            "translation",
                        ),
                        "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_rotation]/@units",
                        "degree",
                    ),
                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation_no_units]",
                    1.0,
                ),
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation_no_units]/@transformation_type",
                "rotation",
            ),
            [
                "The unit 'degree' at /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_rotation]/@units "
                "does not match with the unit category NX_TRANSFORMATION of 'AXISNAME'. Based on the 'transformation_type' of the field "
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[wrong_rotation], "
                "it should match with 'NX_LENGTH'.",
                "Field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[rotation_no_units] requires a unit "
                "in the unit category NX_TRANSFORMATION.",
            ],
            id="nxtransformations-rotation-units",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[direction]",
                        1.0,
                    ),
                    "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[direction_with_unit]",
                    1.0,
                ),
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[direction_with_unit]/@units",
                "m",
            ),
            [
                "The unit 'm' at /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[direction_with_unit]/@units "
                "does not match with the unit category NX_TRANSFORMATION of 'AXISNAME'. Based on the 'transformation_type' of the field "
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[source]/TRANSFORMATIONS[transformations]/AXISNAME[direction_with_unit], "
                "it should match with 'NX_UNITLESS'.",
            ],
            id="nxtransformations-direction-units",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units",
                "required",
            ),
            [
                "Field /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value requires a unit in the unit category NX_ENERGY."
            ],
            id="missing-unit",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value",
                "required",
            ),
            [
                "Unit /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units in dataset without its field /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value.",
                "The attribute /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units will not be written.",
            ],
            id="unit-missing-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/required_group/illegal_name",
                1,
            ),
            [
                "Field /ENTRY[my_entry]/required_group/illegal_name written without documentation."
            ],
            id="add-undocumented-field",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/required_group/author",
                    "author",
                ),
                "/ENTRY[my_entry]/required_group/author/@illegal",
                "illegal_attribute",
            ),
            [
                "Attribute /ENTRY[my_entry]/required_group/author/@illegal written without documentation."
            ],
            id="add-undocumented-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEAM[my_beam]/@default",
                "unknown",
            ),
            [],
            id="group-with-only-attributes",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEAM[my_beam]/@illegal",
                "unknown",
            ),
            [
                "Attribute /ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEAM[my_beam]/@illegal written without documentation."
            ],
            id="group-with-illegal-attributes",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/optional_parent/required_child/@units",
                "s",
            ),
            [
                "The unit, /ENTRY[my_entry]/optional_parent/required_child/@units = s, is being written but has no documentation."
            ],
            id="field-with-illegal-unit",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/ILLEGAL[my_source2]/type",
                1,
            ),
            [
                "Field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/ILLEGAL[my_source2]/type written without documentation."
            ],
            id="bad-namefitting",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/data/test",
                1,
            ),
            ["Field /ENTRY[my_entry]/data/test written without documentation."],
            id="namefitting-of-illegal-named-group",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/USE[user]/name",
                "Some name",
            ),
            ["Field /ENTRY[my_entry]/USE[user]/name written without documentation."],
            id="namefitting-of-group-with-typo",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/USE[user]/test",
                "Some name",
            ),
            ["Field /ENTRY[my_entry]/USE[user]/test written without documentation."],
            id="namefitting-of-group-with-typo-and-new-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/duration",
                np.array([2.0, 3.0, 4.0], dtype=np.float32),
            ),
            [
                "The value at /ENTRY[my_entry]/duration should be"
                " one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT."
            ],
            id="baseclass-wrong-dtype",
        ),
        pytest.param(
            remove_from_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/duration/@units",
                "required",
            ),
            [
                "Field /ENTRY[my_entry]/duration requires a unit in the unit category NX_TIME."
            ],
            id="baseclass-missing-unit",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEA[my_beam]/@illegal",
                "unknown",
            ),
            [
                "There were attributes set for the group or field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEA[my_beam], but the group or field does not exist.",
                "The attribute /ENTRY[my_entry]/INSTRUMENT[my_instrument]/BEA[my_beam]/@illegal will not be written.",
            ],
            id="baseclass-attribute-missing-group",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/collection_time/@illegal",
                "s",
            ),
            [
                "There were attributes set for the field /ENTRY[my_entry]/collection_time, but the field does not exist.",
                "The attribute /ENTRY[my_entry]/collection_time/@illegal will not be written.",
            ],
            id="baseclass-attribute-missing-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/target_material",
                "Cu",
            ),
            [
                "The value at /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/target_material "
                "should be one of the following: ['Ta', 'W', 'depleted_U', 'enriched_U', 'Hg', 'Pb', 'C']."
            ],
            id="baseclass-wrong-enum",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type",
                "Wrong source type",
            ),
            [
                "The value at /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type does not match with the enumerated "
                "items from the open enumeration: ['Spallation Neutron Source', 'Pulsed Reactor Neutron Source', 'Reactor Neutron Source', "
                "'Synchrotron X-ray Source', 'Pulsed Muon Source', 'Rotating Anode X-ray', 'Fixed Tube X-ray', 'UV Laser', 'Free-Electron Laser', "
                "'Optical Laser', 'Ion Source', 'UV Plasma Source', 'Metal Jet X-ray', 'Laser', 'Dye Laser', 'Broadband Tunable Light Source', "
                "'Halogen Lamp', 'LED', 'Mercury Cadmium Telluride Lamp', 'Deuterium Lamp', 'Xenon Lamp', 'Globar']."
            ],
            id="baseclass-open-enum-with-new-item",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal_name",
                1,
            ),
            [
                "Field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal_name written without documentation."
            ],
            id="baseclass-add-undocumented-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type/@illegal",
                "illegal_attribute",
            ),
            [
                "Attribute /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type/@illegal written without documentation."
            ],
            id="baseclass-add-undocumented-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal/@units",
                "illegal_attribute",
            ),
            [
                "Unit /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal/@units "
                "in dataset without its field /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal.",
                "The attribute /ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/illegal/@units will not be written.",
            ],
            id="baseclass-add-unit-of-missing-undocumented-field",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/required_group/author",
                    "author",
                ),
                "/ENTRY[my_entry]/required_group/author/@units",
                "s",
            ),
            [
                "The unit, /ENTRY[my_entry]/required_group/author/@units = s, is being written but has no documentation."
            ],
            id="baseclass-field-with-illegal-unit",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/identified_calibration/identifier_1",
                "123",
            ),
            [],
            id="specified-identifier-without-type",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/identified_calibration/identifier_1",
                    "123",
                ),
                "/ENTRY[my_entry]/identified_calibration/identifier_1/@type",
                "ORCID",
            ),
            [],
            id="specified-identifier-with-type",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/identifierNAME[identifier_id]",
                    "123",
                ),
                "/ENTRY[my_entry]/identifierNAME[identifier_id]/@type",
                "ORCID",
            ),
            [],
            id="name-fitted-identifier-with-type",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/identifierNAME[identifier_id]",
                    "123",
                ),
                "/ENTRY[my_entry]/identifierNAME[identifier_id]/@type",
                "ORCID",
            ),
            [],
            id="name-fitted-identifier-with-type",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/CALIBRATION[identified_calibration]/identifier_1",
                "123",
            ),
            [],
            id="group-with-correct-concept",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/CALIBRATION[identified_calibration]/identifier_1",
                    "123",
                ),
                "/ENTRY[my_entry]/identified_calibration/identifier_2",
                "456",
            ),
            [
                "The data entry corresponding to /ENTRY[my_entry]/identified_calibration/identifier_1 is required "
                "and hasn't been supplied by the reader."
            ],
            id="group-with-correct-concept-and-non-concept-sibling",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/COLLECTION[collection]/some_field",
                        0.5,
                    ),
                    "/ENTRY[my_entry]/COLLECTION[collection]/DATA[data]/some_field",
                    0.5,
                ),
                "/ENTRY[my_entry]/COLLECTION[collection]/DATA[data]/some_field/@units",
                "mm",
            ),
            [],
            id="variadic-nxcollection",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        TEMPLATE,
                        "/ENTRY[my_entry]/named_collection/some_field",
                        0.5,
                    ),
                    "/ENTRY[my_entry]/named_collection/DATA[data]/some_field",
                    0.5,
                ),
                "/ENTRY[my_entry]/named_collection/DATA[data]/some_field/@units",
                "mm",
            ),
            [],
            id="nonvariadic-nxcollection",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field_set",
                    1,
                ),
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/some_field_set",
                1,
            ),
            [
                "Reserved suffix '_set' was used in /ENTRY[my_entry]/OPTIONAL_group[my_group]/some_field_set, "
                "but there is no associated field some_field."
            ],
            id="reserved-suffix-from-appdef",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/OPTIONAL_group[my_group]/FIELDNAME_weights[required_field_weights]",
                    0.1,
                ),
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/FIELDNAME_weights[some_random_field_weights]",
                0.1,
            ),
            [
                "Reserved suffix '_weights' was used in /ENTRY[my_entry]/OPTIONAL_group[my_group]/FIELDNAME_weights[some_random_field_weights], but there is no associated field some_random_field.",
            ],
            id="reserved-suffix-from-baseclass",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    alter_dict(
                        alter_dict(
                            TEMPLATE,
                            "/ENTRY[my_entry]/OPTIONAL_group[my_group]/@BLUESKY_attr",
                            "some text",
                        ),
                        "/ENTRY[my_entry]/OPTIONAL_group[my_group]/@DECTRIS_attr",
                        "some text",
                    ),
                    "/ENTRY[my_entry]/OPTIONAL_group[my_group]/DECTRIS_field",
                    "some text",
                ),
                "/ENTRY[my_entry]/OPTIONAL_group[my_group]/@NX_attr",
                "some text",
            ),
            [
                "Reserved prefix @BLUESKY_ was used in key /ENTRY[my_entry]/OPTIONAL_group[my_group]/@BLUESKY_attr, but is not valid here.",
                "Attribute /ENTRY[my_entry]/OPTIONAL_group[my_group]/@BLUESKY_attr written without documentation.",
                "Reserved prefix @DECTRIS_ was used in key /ENTRY[my_entry]/OPTIONAL_group[my_group]/@DECTRIS_attr, but is not valid here. "
                "It is only valid in the context of NXmx.",
                "Attribute /ENTRY[my_entry]/OPTIONAL_group[my_group]/@DECTRIS_attr written without documentation.",
                "Reserved prefix DECTRIS_ was used in key /ENTRY[my_entry]/OPTIONAL_group[my_group]/DECTRIS_field, but is not valid here. "
                "It is only valid in the context of NXmx.",
                "Field /ENTRY[my_entry]/OPTIONAL_group[my_group]/DECTRIS_field written without documentation.",
                "Attribute /ENTRY[my_entry]/OPTIONAL_group[my_group]/@NX_attr written without documentation.",
            ],
            id="reserved-prefix",
        ),
        pytest.param(
            compress_paths_in_dict(
                TEMPLATE,
                [
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value"
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value",
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type",
                ],
            ),
            [],
            id="appdef-compressed",
        ),
        pytest.param(
            alter_dict(
                alter_dict(
                    TEMPLATE,
                    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                    {"compress": np.int64(2.0), "strength": 1},
                ),
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                {"compress": np.float32(2.0), "strength": 1},
            ),
            [
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value "
                "should be one of the following Python types: "
                "(<class 'int'>, <class 'numpy.integer'>), as defined in the "
                "NXDL as NX_INT."
            ],
            id="appdef-compressed-wrong-type",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                {"compress": np.int64(2), "strength": 11},
            ),
            [
                "Compression strength for /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value = "
                "{'compress': 2, 'strength': 11} should be between 0 and 9.",
            ],
            id="appdef-compressed-invalid-strength",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                {"compress": np.float32(2.0), "strength": 0},
            ),
            [
                "Compression strength for /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value "
                "is 0. The value '2.0' will be written uncompressed.",
            ],
            id="appdef-compressed-strength-0",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/SAMPLE[sample1]]/changer_position",
                {"compress": np.int64(2), "strength": 1},
            ),
            [],
            id="baseclass-compressed",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/SAMPLE[sample1]]/changer_position",
                {"compress": np.float32(2.0), "strength": 3},
            ),
            [
                "The value at /ENTRY[my_entry]/SAMPLE[sample1]]/changer_position "
                "should be one of the following Python types: "
                "(<class 'int'>, <class 'numpy.integer'>), as defined in the "
                "NXDL as NX_INT."
            ],
            id="baseclass-compressed-wrong-type",
        ),
    ],
)
def test_validate_data_dict(caplog, data_dict, error_messages, request):
    """Unit test for the data validation routine."""

    def format_error_message(msg: str) -> str:
        for prefix in ("ERROR:", "WARNING:"):
            if msg.startswith(prefix):
                return msg[len(prefix) :].lstrip()
        return msg

    if not error_messages:
        with caplog.at_level(logging.WARNING):
            assert validate_dict_against("NXtest", data_dict)
        assert caplog.text == ""
    else:
        if request.node.callspec.id in (
            "field-with-illegal-unit",
            "baseclass-field-with-illegal-unit",
            "open-enum-with-new-item",
            "baseclass-open-enum-with-new-item",
            "appdef-compressed-strength-0",
        ):
            with caplog.at_level(logging.INFO):
                assert validate_dict_against("NXtest", data_dict)
                assert error_messages[0] in caplog.text
        else:
            with caplog.at_level(logging.WARNING):
                assert not validate_dict_against("NXtest", data_dict)
            assert len(caplog.records) == len(error_messages)
            for expected_message, rec in zip(error_messages, caplog.records):
                assert expected_message == format_error_message(rec.message)
    assert error_message in caplog.text


data_dict_list = [
    (
        {
            "/ENTRY[entry]/definition": "NXhdf5_validator_2",
            "/ENTRY[entry]/version": "no version",
            "/ENTRY[entry]/experiment_result/hdf5_validator_2_intensity": np.array(
                [[11, 12, 13], [21, 22, 23]]
            ),
            "/ENTRY[entry]/hdf5_validator_1_program_name": "hdf5_file_validator",
            "/ENTRY[entry]/hdf5_validator_1_required/required_field": "Required_field_from nxdl-1",
            "/ENTRY[entry]/hdf5_validator_2_users_req/required_field": "Required_field_from_nxdl-2",
        },
        {
            "error_messages": [
                "WARNING: Field version written without documentation.",
                'WARNING: Missing attribute: "/ENTRY/experiment_result/@long_name"',
                'WARNING: Missing attribute: "/ENTRY/experiment_result/@AXISNAME_indices"',
                'WARNING: Missing attribute: "/ENTRY/experiment_result/@axes"',
                'WARNING: Missing attribute: "/ENTRY/experiment_result/@auxiliary_signals"',
                "WARNING: Missing field: /ENTRY/experiment_result/DATA",
                'WARNING: Missing attribute: "/ENTRY/experiment_result/DATA/@units"',
                "WARNING: Missing field: /ENTRY/experiment_result/AXISNAME",
                'WARNING: Missing attribute: "/ENTRY/experiment_result/AXISNAME/@units"',
                'WARNING: Missing attribute: "/ENTRY/experiment_result/@signal"',
                'WARNING: Missing attribute: "/ENTRY/definition/@version"',
                "is NOT a valid file according to the `NXhdf5_validator_2` application definition.",
            ]
        },
    ),
    ({}, {}),
]


@pytest.mark.parametrize("data_dict, error_massages", data_dict_list)
def test_nexus_file_validate(data_dict, error_massages, tmp_path, caplog):
    if not data_dict and not error_massages:
        return

    caplog_level = "INFO"
    template = Template()

    for key, val in data_dict.items():
        template[key] = val

    nxdl_name = "NXhdf5_validator_2"
    _, nxdl_path = get_nxdl_root_and_path(nxdl=nxdl_name)
    hdf_file_path = tmp_path / "hdf5_validator_test.nxs"
    Writer(data=template, nxdl_f_path=nxdl_path, output_path=hdf_file_path).write()
    with caplog.at_level(caplog_level):
        _ = CliRunner().invoke(verify, [str(hdf_file_path)])
    error_massages = error_massages["error_messages"]
    for record in caplog.records:
        try:
            assert (
                record.msg in error_massages
            ), f"Error message not found: {record.msg}"
        except AssertionError:
            # Only for detecting entry or missing application definition massage
            assert (
                error_massages[-1] in record.msg
            ), f"Error message not found: {record.msg}"

    os.remove(hdf_file_path)
