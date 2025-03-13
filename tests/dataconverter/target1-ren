<<<<<<< HEAD
from pynxtools.dataconverter.template import Template


def remove_optional_parent(data_dict: Template):
    """Completely removes the optional group from the test Template."""
    internal_dict = Template(data_dict)
    del internal_dict["/ENTRY[my_entry]/optional_parent/required_child"]
    del internal_dict["/ENTRY[my_entry]/optional_parent/optional_child"]
    del internal_dict[
        "/ENTRY[my_entry]/optional_parent/req_group_in_opt_group/DATA[data]"
    ]

    return internal_dict


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
            ) or isinstance(data_dict[optionality][path], list):
                listified_template[optionality][path] = data_dict[optionality][path]
            else:
                listified_template[optionality][path] = [data_dict[optionality][path]]
    return listified_template


TEMPLATE = Template()
TEMPLATE["optional"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]"
] = 2
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
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value"] = 2
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units"] = (
    "eV"
)
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
TEMPLATE["required"][
    "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/anamethatRENAMES[anamethatichangetothis]"
] = 2  # pylint: disable=E1126
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
TEMPLATE["required"]["/ENTRY[my_entry]/OPTIONAL_group[my_group]/required_field"] = 1  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/definition"] = "NXtest"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/definition/@version"] = "2.4.6"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/program_name"] = "Testing program"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type"] = "2nd type"  # pylint: disable=E1126
TEMPLATE["required"]["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array"] = [0, 1, 2]
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
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]",
                "not_a_num",
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]"
                " should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in "
                "the NXDL as NX_INT."
            ),
            id="variadic-field-str-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                "not_a_num",
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/in"
                "t_value should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in "
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
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value should be one of the following Python types: (<class 'bool'>, <class 'numpy.bool_'>), as defined in the NXDL as NX_BOOLEAN."
            ),
            id="string-instead-of-bool",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                ["1", "2", "3"],
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value should"
                " be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT."
            ),
            id="list-of-int-str-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                np.array([2.0, 3.0, 4.0], dtype=np.float32),
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value should be"
                " one of the following Python types: (<class 'int'>, <class 'numpy.integer'>), as defined in the NXDL as NX_INT."
            ),
            id="array-of-float-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                [2, 3, 4],
            ),
            (""),
            id="list-of-int-instead-of-int",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                np.array([2, 3, 4], dtype=np.int32),
            ),
            (""),
            id="array-of-int32-instead-of-int",
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
            id="int-instead-of-date",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                0,
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value should be one of the following Python types: (<class 'float'>, <class 'numpy.floating'>), as defined in the NXDL as NX_FLOAT."
            ),
            id="int-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value",
                "0",
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value should be one of the following Python types: (<class 'int'>, <class 'numpy.integer'>, <class 'float'>, <class 'numpy.floating'>), as defined in the NXDL as NX_NUMBER."
            ),
            id="str-instead-of-number",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array([0.0, 2]),
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value should be one"
                " of the following Python types: (<class 'str'>, <class 'numpy.character'>), as"
                " defined in the NXDL as NX_CHAR."
            ),
            id="wrong-type-ndarray-instead-of-char",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["x", "2"]),
            ),
            (""),
            id="valid-ndarray-instead-of-char",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value",
                {"link": "/a-link"},
            ),
            (""),
            id="link-dict-instead-of-int",
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
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                [-1, 2],
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value "
                "should be a positive int, but is [-1, 2]."
            ),
            id="negative-posint-list",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                np.array([-1, 2], dtype=np.int8),
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value should"
                " be a positive int, but is [-1  2]."
            ),
            id="negative-posint-array",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                [1, 2],
            ),
            (""),
            id="positive-posint-list",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value",
                np.array([1, 2], dtype=np.int8),
            ),
            (""),
            id="positive-posint-array",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value", 3
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value should be one of the following Python types:"
                " (<class 'str'>, <class 'numpy.character'>),"
                " as defined in the NXDL as NX_CHAR."
            ),
            id="int-instead-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["1", "2", "3"], dtype=np.str_),
            ),
            (""),
            id="array-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                np.array(["1", "2", "3"], dtype=np.bytes_),
            ),
            (""),
            id="array-of-bytes-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value",
                ["list", "of", "chars"],
            ),
            "",
            id="list-of-string-instead-of-chars",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value", None
            ),
            "",
            id="empty-optional-field",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.array([2.0, 3.0, 4.0], dtype=np.float32),
            ),
            "",
            id="array-of-float-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                np.array(["2.0", "3.0"], dtype=np.str_),
            ),
            "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value should be "
            "one of the following Python types: (<class 'float'>, <class 'numpy.floating'>), as defined in the NXDL "
            "as NX_FLOAT.",
            id="array-of-str-instead-of-float",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value",
                [2],  # pylint: disable=E1126
            ),
            "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value should be "
            "one of the following Python types: (<class 'float'>, <class 'numpy.floating'>), as defined in the NXDL "
            "as NX_FLOAT.",
            id="list-of-int-instead-of-float",
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
                "be one of the following"
                ": ['1st type', '2nd type', '3rd type', '4th type']"
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
        pytest.param(
            alter_dict(
                TEMPLATE,
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array",
                ["0", 1, 2],
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array should be one of the following: [[0, 1, 2], [2, 3, 4]]"
            ),
            id="wrong-type-array-in-attribute",
        ),
        pytest.param(
            alter_dict(
                TEMPLATE, "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array", [1, 2]
            ),
            (
                "The value at /ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array should be one of the following: [[0, 1, 2], [2, 3, 4]]"
            ),
            id="wrong-value-array-in-attribute",
        ),
    ],
)
def test_validate_data_dict(caplog, data_dict, error_message, request):
    """Unit test for the data validation routine."""

    def format_error_message(msg: str) -> str:
        return msg[msg.rfind("G: ") + 3 :].rstrip("\n")

    if request.node.callspec.id in (
        "valid-data-dict",
        "lists",
        "empty-optional-field",
        "UTC-with-+00:00",
        "UTC-with-Z",
        "no-child-provided-optional-parent",
        "link-dict-instead-of-int",
        "opt-group-completely-removed",
        "required-field-provided-in-variadic-optional-group",
        "valid-ndarray-instead-of-char",
        "list-of-int-instead-of-int",
        "list-of-string-instead-of-chars",
        "array-of-int32-instead-of-int",
        "List-of-int-instead-of-int",
        "positive-posint-list",
        "positive-posint-array",
        "array-of-chars",
        "array-of-bytes-chars",
        "array-of-float-instead-of-float",
        "numpy-chararray",
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
        assert any(
            error_message == format_error_message(rec.message) for rec in captured_logs
        )
    else:
        with caplog.at_level(logging.WARNING):
            assert not validate_dict_against("NXtest", data_dict)[0]
        assert any(
            error_message == format_error_message(rec.message) for rec in caplog.records
        )
=======
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
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]": 2,
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value_no_attr": 2.0,
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
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/type/@array": [0, 1, 2],
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value": "2022-01-22T12:14:12.05018+00:00",
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value/@units": "",
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/anamethatRENAMES[anamethatichangetothis]": 2,
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
        "/ENTRY[my_entry]/NXODD_name[nxodd_two_name]/type/@array": [0, 1, 2],
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
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value_no_attr",
                get_data_dict(),
            ),
            id="removed-optional-value",
        ),
    ],
)
def test_valid_data_dict(caplog, data_dict):
    with caplog.at_level(logging.WARNING):
        assert validate_dict_against("NXtest", data_dict)[0]
    assert caplog.text == ""


@pytest.mark.parametrize(
    "data_dict, error_message_1, error_message_2",
    [
        pytest.param(
            remove_from_dict(
                "/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value", get_data_dict()
            ),
            "The attribute /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units will not be written.",
            "There were attributes set for the field /ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value, but the field does not exist.",
            id="removed-optional-value-with-attribute-remaining",
        ),
    ],
)
def test_data_dict_attr_with_no_field(
    caplog, data_dict, error_message_1, error_message_2
):
    with caplog.at_level(logging.WARNING):
        assert not validate_dict_against("NXtest", data_dict)[0]
    assert error_message_1 in caplog.text
    assert error_message_2 in caplog.text


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
        assert not validate_dict_against("NXtest", data_dict)[0]

    assert error_message in caplog.text
>>>>>>> 9023d8d9 (rename original targets)
