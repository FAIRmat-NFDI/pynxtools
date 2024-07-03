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
"""Helper functions commonly used by the convert routine."""

import json
import logging
import os
import re
from datetime import datetime, timezone
from enum import Enum
from functools import lru_cache
from typing import Any, Callable, List, Optional, Tuple, Union

import h5py
import lxml.etree as ET
import numpy as np
from ase.data import chemical_symbols

from pynxtools import get_nexus_version, get_nexus_version_hash
from pynxtools.nexus import nexus

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ValidationProblem(Enum):
    UnitWithoutDocumentation = 1
    InvalidEnum = 2
    MissingRequiredGroup = 3
    MissingRequiredField = 4
    MissingRequiredAttribute = 5
    InvalidType = 6
    InvalidDatetime = 7
    IsNotPosInt = 8
    ExpectedGroup = 9
    MissingDocumentation = 10
    MissingUnit = 11
    ChoiceValidationError = 12
    UnitWithoutField = 13
    AttributeForNonExistingField = 14
    BrokenLink = 15
    FailedNamefitting = 16
    NXdataMissingSignalData = 17
    NXdataMissingAxisData = 18
    NXdataAxisMismatch = 19


class Collector:
    """A class to collect data and return it in a dictionary format."""

    def __init__(self):
        self.data = set()
        self.logging = True

    def _log(self, path: str, log_type: ValidationProblem, value: Optional[Any], *args):
        if value is None:
            value = "<unknown>"

        if log_type == ValidationProblem.UnitWithoutDocumentation:
            logger.warning(
                f"The unit, {path} = {value}, "
                "is being written but has no documentation"
            )
        elif log_type == ValidationProblem.InvalidEnum:
            logger.warning(
                f"The value at {path} should be on of the "
                f"following strings: {value}"
            )
        elif log_type == ValidationProblem.MissingRequiredGroup:
            logger.warning(f"The required group, {path}, hasn't been supplied.")
        elif log_type == ValidationProblem.MissingRequiredField:
            logger.warning(
                f"The data entry corresponding to {path} is required "
                "and hasn't been supplied by the reader.",
            )
        elif log_type == ValidationProblem.InvalidType:
            logger.warning(
                f"The value at {path} should be one of: {value}"
                f", as defined in the NXDL as {args[0] if args else '<unknown>'}."
            )
        elif log_type == ValidationProblem.InvalidDatetime:
            logger.warning(
                f"The value at {path} = {value} should be a timezone aware ISO8601 "
                "formatted str. For example, 2022-01-22T12:14:12.05018Z"
                " or 2022-01-22T12:14:12.05018+00:00."
            )
        elif log_type == ValidationProblem.IsNotPosInt:
            logger.warning(
                f"The value at {path} should be a positive int, but is {value}."
            )
        elif log_type == ValidationProblem.ExpectedGroup:
            logger.warning(
                f"Expected a group at {path} but found a field or attribute."
            )
        elif log_type == ValidationProblem.MissingDocumentation:
            logger.warning(f"Field {path} written without documentation.")
        elif log_type == ValidationProblem.MissingUnit:
            logger.warning(
                f"Field {path} requires a unit in the unit category {value}."
            )
        elif log_type == ValidationProblem.MissingRequiredAttribute:
            logger.warning(f'Missing attribute: "{path}"')
        elif log_type == ValidationProblem.UnitWithoutField:
            logger.warning(f"Unit {path} in dataset without its field {value}")
        elif log_type == ValidationProblem.AttributeForNonExistingField:
            logger.warning(
                f"There were attributes set for the field {path}, "
                "but the field does not exist."
            )
        elif log_type == ValidationProblem.BrokenLink:
            logger.warning(f"Broken link at {path} to {value}")
        elif log_type == ValidationProblem.FailedNamefitting:
            logger.warning(f"Found no namefit of {path} in {value}.")
        elif log_type == ValidationProblem.NXdataMissingSignalData:
            logger.warning(f"Missing data for signal in {path}.")
        elif log_type == ValidationProblem.NXdataMissingAxisData:
            logger.warning(f"Missing data for @axes in {path}.")
        elif log_type == ValidationProblem.NXdataAxisMismatch:
            logger.warning(
                f"Length of axis {path} does not match to {value} in dimension {args[0]}"
            )

    def collect_and_log(
        self,
        path: str,
        log_type: ValidationProblem,
        value: Optional[Any],
        *args,
        **kwargs,
    ):
        """Inserts a path into the data dictionary and logs the action."""
        if log_type == ValidationProblem.MissingUnit and value in (
            "NX_UNITLESS",
            "NX_DIMENSIONLESS",
            "NX_ANY",
        ):
            return
        if self.logging:
            self._log(path, log_type, value, *args, **kwargs)
        self.data.add(path)

    def has_validation_problems(self):
        """Returns True if there were any validation problems."""
        return len(self.data) > 0

    def get(self):
        """Returns the set of problematic paths."""
        return self.data

    def clear(self):
        """Clears the collected data."""
        self.data = set()


collector = Collector()


def is_a_lone_group(xml_element) -> bool:
    """Checks whether a given group XML element has no field or attributes mentioned"""
    if xml_element.get("type") == "NXentry":
        return False
    for child in xml_element.findall(".//"):
        if remove_namespace_from_tag(child.tag) in ("field", "attribute"):
            return False
    return True


def get_nxdl_name_from_elem(xml_element) -> str:
    """Extracts the name or uses the type to remove the NX bit and use as name."""
    name_to_add = ""
    if "name" in xml_element.attrib:
        name_to_add = xml_element.attrib["name"]
    elif "type" in xml_element.attrib:
        name_to_add = (
            f"{convert_nexus_to_caps(xml_element.attrib['type'])}"
            f"[{convert_nexus_to_suggested_name(xml_element.attrib['type'])}]"
        )
    return name_to_add


def get_nxdl_name_for(xml_elem: ET._Element) -> Optional[str]:
    """
    Get the name of the element from the NXDL element.
    For an entity having a name this is just the name.
    For groups it is the uppercase type without NX, e.g. "ENTRY" for "NXentry".

    Args:
        xml_elem (ET._Element): The xml element to get the name for.

    Returns:
        Optional[str]:
            The name of the element.
            None if the xml element has no name or type attribute.
    """
    """"""
    if "name" in xml_elem.attrib:
        return xml_elem.attrib["name"]
    if "type" in xml_elem.attrib:
        return convert_nexus_to_caps(xml_elem.attrib["type"])
    return None


def get_appdef_root(xml_elem: ET._Element) -> ET._Element:
    """
    Get the root element of the tree of xml_elem

    Args:
        xml_elem (ET._Element): The element for which to get the root element.

    Returns:
        ET._Element: The root element of the tree.
    """
    return xml_elem.getroottree().getroot()


def is_appdef(xml_elem: ET._Element) -> bool:
    """
    Check whether the xml element is part of an application definition.

    Args:
        xml_elem (ET._Element): The xml_elem whose tree to check.

    Returns:
        bool: True if the xml_elem is part of an application definition.
    """
    return get_appdef_root(xml_elem).attrib.get("category") == "application"


def get_all_parents_for(xml_elem: ET._Element) -> List[ET._Element]:
    """
    Get all parents from the nxdl (via extends keyword)

    Args:
        xml_elem (ET._Element): The element to get the parents for.

    Returns:
        List[ET._Element]: The list of parents xml nodes.
    """
    root = get_appdef_root(xml_elem)
    inheritance_chain = []
    extends = root.get("extends")
    while extends is not None and extends != "NXobject":
        parent_xml_root, _ = get_nxdl_root_and_path(extends)
        extends = parent_xml_root.get("extends")
        inheritance_chain.append(parent_xml_root)

    return inheritance_chain


def get_nxdl_root_and_path(nxdl: str):
    """Get xml root element and file path from nxdl name e.g. NXapm.

    Parameters
    ----------
    nxdl: str
        Name of nxdl file e.g. NXapm from NXapm.nxdl.xml.

    Returns
    -------
    ET.root
        Root element of nxdl file.
    str
        Path of nxdl file.

    Raises
    ------
    FileNotFoundError
        Error if no file with the given nxdl name is found.
    """

    # Reading in the NXDL and generating a template
    definitions_path = nexus.get_nexus_definitions_path()
    data_path = os.path.join(
        f"{os.path.abspath(os.path.dirname(__file__))}/../",
        "data",
    )
    special_names = {
        "NXtest": os.path.join(data_path, "NXtest.nxdl.xml"),
        "NXtest_extended": os.path.join(data_path, "NXtest_extended.nxdl.xml"),
    }

    if nxdl in special_names:
        nxdl_f_path = special_names[nxdl]
    else:
        nxdl_f_path = os.path.join(
            definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml"
        )
        if not os.path.exists(nxdl_f_path):
            nxdl_f_path = os.path.join(
                definitions_path, "applications", f"{nxdl}.nxdl.xml"
            )
        if not os.path.exists(nxdl_f_path):
            nxdl_f_path = os.path.join(
                definitions_path, "base_classes", f"{nxdl}.nxdl.xml"
            )
        if not os.path.exists(nxdl_f_path):
            raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

    return ET.parse(nxdl_f_path).getroot(), nxdl_f_path


def get_all_defined_required_children_for_elem(xml_element):
    """Gets all possible inherited required children for a given NXDL element"""
    list_of_children_to_add = set()
    for child in xml_element:
        tag = remove_namespace_from_tag(child.tag)
        if tag not in ("group", "field", "attribute"):
            continue
        child.set("nxdlbase_class", xml_element.get("nxdlbase_class"))
        if child.attrib and get_required_string(child) == "required":
            tag = remove_namespace_from_tag(child.tag)

            name_to_add = get_nxdl_name_from_elem(child)

            if tag in ("field", "attribute"):
                name_to_add = f"@{name_to_add}" if tag == "attribute" else name_to_add
                list_of_children_to_add.add(name_to_add)
                if tag == "field" and (
                    "units" in child.attrib.keys()
                    and child.attrib["units"] != "NX_UNITLESS"
                ):
                    list_of_children_to_add.add(f"{name_to_add}/@units")
            elif tag == "group":
                nxdlpath = (
                    f'{xml_element.get("nxdlpath")}/{get_nxdl_name_from_elem(child)}'
                )
                nxdlbase = xml_element.get("nxdlbase")
                nx_name = nxdlbase[nxdlbase.rfind("/") + 1 : nxdlbase.rfind(".nxdl")]
                if nxdlpath not in visited_paths:
                    visited_paths.append(nxdlpath)
                    children = get_all_defined_required_children(nxdlpath, nx_name)
                    further_children = set()
                    for further_child in children:
                        further_children.add(f"{name_to_add}/{further_child}")
                    list_of_children_to_add.update(further_children)
    return list_of_children_to_add


visited_paths: List[str] = []


def get_all_defined_required_children(nxdl_path, nxdl_name):
    """Helper function to find all possible inherited required children for an NXDL path"""
    if nxdl_name == "NXtest":
        return []

    elist = nexus.get_inherited_nodes(nxdl_path, nx_name=nxdl_name)[2]
    list_of_children_to_add = set()
    for elem in elist:
        list_of_children_to_add.update(get_all_defined_required_children_for_elem(elem))

    return list_of_children_to_add


def add_inherited_children(list_of_children_to_add, path, nxdl_root, template):
    """Takes a list of child names and appends them to template for a given path."""
    for child in list_of_children_to_add:
        child_path = f"{path}/{child}"
        if child_path not in template.keys():
            optional_parent = check_for_optional_parent(child_path, nxdl_root)
            optionality = (
                "required" if optional_parent == "<<NOT_FOUND>>" else "optional"
            )
            template[optionality][f"{path}/{child}"] = None
    return template


def generate_template_from_nxdl(
    root, template, path="", nxdl_root=None, nxdl_name=None
):
    """Helper function to generate a template dictionary for given NXDL"""
    if nxdl_root is None:
        nxdl_name = root.attrib["name"]
        nxdl_root = root
        root = get_first_group(root)

    tag = remove_namespace_from_tag(root.tag)

    if tag == "doc":
        return

    suffix = ""
    if "name" in root.attrib and not contains_uppercase(root.attrib["name"]):
        suffix = root.attrib["name"]
    elif "type" in root.attrib:
        nexus_class = convert_nexus_to_caps(root.attrib["type"])
        name = root.attrib.get("name")
        hdf_name = root.attrib.get("type")[2:]  # .removeprefix("NX") (python > 3.8)
        suffix = (
            f"{name}[{name.lower()}]"
            if name is not None
            else f"{nexus_class}[{hdf_name}]"
        )

    path = path + "/" + (f"@{suffix}" if tag == "attribute" else suffix)

    # Only add fields or attributes to the dictionary
    if tag in ("field", "attribute"):
        optionality = get_required_string(root)
        if optionality == "required":
            optional_parent = check_for_optional_parent(path, nxdl_root)
            optionality = (
                "required" if optional_parent == "<<NOT_FOUND>>" else "optional"
            )
            if optional_parent != "<<NOT_FOUND>>":
                template.optional_parents.append(optional_parent)
        template[optionality][path] = None

        # Only add units if it is a field and the the units are defined but not set to NX_UNITLESS
        if tag == "field" and (
            "units" in root.attrib.keys() and root.attrib["units"] != "NX_UNITLESS"
        ):
            template[optionality][f"{path}/@units"] = None

        nxdl_path = convert_data_converter_dict_to_nxdl_path(path)
        list_of_children_to_add = get_all_defined_required_children(
            nxdl_path, nxdl_name
        )
        add_inherited_children(list_of_children_to_add, path, nxdl_root, template)

    elif tag == "group" and is_a_lone_group(root):
        template[get_required_string(root)][path] = None
        template["lone_groups"].append(path)
        path_nxdl = convert_data_converter_dict_to_nxdl_path(path)
        list_of_children_to_add = get_all_defined_required_children(
            path_nxdl, nxdl_name
        )
        add_inherited_children(list_of_children_to_add, path, nxdl_root, template)
    # Handling link: link has a target attibute that store absolute path of concept to be
    # linked. Writer reads link from template in the format {'link': <ABSOLUTE PATH>}
    # {'link': ':/<ABSOLUTE PATH TO EXTERNAL FILE>'}
    elif tag == "link":
        # NOTE:  The code below can be implemented later once, NeXus brings optionality in
        # link. Otherwise link will be considered optional by default.

        # optionality = get_required_string(root)
        # optional_parent = check_for_optional_parent(path, nxdl_root)
        # optionality = "required" if optional_parent == "<<NOT_FOUND>>" else "optional"
        # if optionality == "optional":
        #     template.optional_parents.append(optional_parent)
        optionality = "optional"
        template[optionality][path] = {"link": root.attrib["target"]}

    for child in root:
        generate_template_from_nxdl(child, template, path, nxdl_root, nxdl_name)


def get_required_string(elem):
    """Helper function to return nicely formatted names for optionality."""
    return nexus.get_required_string(elem)[2:-2].lower()


def convert_nexus_to_caps(nexus_name):
    """Helper function to convert a NeXus class from <NxClass> to <CLASS>."""
    return nexus_name[2:].upper()


def contains_uppercase(field_name: Optional[str]) -> bool:
    """Helper function to check if a field name contains uppercase characters."""
    if field_name is None:
        return False
    return any(char.isupper() for char in field_name)


def convert_nexus_to_suggested_name(nexus_name):
    """Helper function to suggest a name for a group from its NeXus class."""
    if contains_uppercase(nexus_name):
        return nexus_name
    return nexus_name[2:]


def convert_data_converter_entry_to_nxdl_path_entry(entry) -> Union[str, None]:
    """
    Helper function to convert data converter style entry to NXDL style entry:
    ENTRY[entry] -> ENTRY
    """
    regex = re.compile(r"(.*?)(?=\[)")
    results = regex.search(entry)
    return entry if results is None else results.group(1)


def convert_nxdl_path_entry_to_data_converter_entry(entry) -> str:
    """
    Helper function to convert NXDL style entry to data converter style entry:
    ENTRY -> ENTRY[entry]
    """
    return f"{entry}[{entry.lower()}]"


def convert_nxdl_path_dict_to_data_converter_dict(path) -> str:
    """
    Helper function to convert NXDL style path to data converter style path:
    /ENTRY/entry -> /ENTRY[entry]/entry
    """
    data_converter_path = ""
    for entry in path.split("/")[1:]:
        if not contains_uppercase(entry):
            data_converter_path += f"/{entry}"
            continue
        data_converter_path += "/" + convert_nxdl_path_entry_to_data_converter_entry(
            entry
        )
    return data_converter_path


def convert_data_converter_dict_to_nxdl_path(path) -> str:
    """
    Helper function to convert data converter style path to NXDL style path:
    /ENTRY[entry]/sample -> /ENTRY/sample
    """
    nxdl_path = ""
    for entry in path.split("/")[1:]:
        nxdl_path += "/" + convert_data_converter_entry_to_nxdl_path_entry(entry)
    return nxdl_path


def get_name_from_data_dict_entry(entry: str) -> str:
    """Helper function to get entry name from data converter style entry

    ENTRY[entry] -> entry
    """

    @lru_cache(maxsize=None)
    def get_regex():
        return re.compile(r"(?<=\[)(.*?)(?=\])")

    results = get_regex().search(entry)
    if results is None:
        return entry
    if entry[0] == "@":
        return "@" + results.group(1)
    return results.group(1)


def convert_data_dict_path_to_hdf5_path(path) -> str:
    """Helper function to convert data converter style path to HDF5 style path

    /ENTRY[entry]/sample -> /entry/sample
    """
    hdf5path = ""
    for entry in path.split("/")[1:]:
        hdf5path += "/" + get_name_from_data_dict_entry(entry)
    return hdf5path


def is_value_valid_element_of_enum(value, elist) -> Tuple[bool, list]:
    """Checks whether a value has to be specific from the NXDL enumeration and returns options."""
    for elem in elist:
        enums = nexus.get_enums(elem)
        if enums is not None:
            return value in enums, enums
    return True, []


NUMPY_FLOAT_TYPES = (np.half, np.float16, np.single, np.double, np.longdouble)
NUMPY_INT_TYPES = (np.short, np.intc, np.int_)
NUMPY_UINT_TYPES = (np.ushort, np.uintc, np.uint)

NEXUS_TO_PYTHON_DATA_TYPES = {
    "ISO8601": (str,),
    "NX_BINARY": (bytes, bytearray, np.byte, np.ubyte, np.ndarray),
    "NX_BOOLEAN": (bool, np.ndarray, np.bool_),
    "NX_CHAR": (str, np.ndarray, np.chararray),
    "NX_DATE_TIME": (str,),
    "NX_FLOAT": (float, np.ndarray, np.floating),
    "NX_INT": (int, np.ndarray, np.signedinteger),
    "NX_UINT": (np.ndarray, np.unsignedinteger),
    "NX_NUMBER": (
        int,
        float,
        np.ndarray,
        np.signedinteger,
        np.unsignedinteger,
        np.floating,
        dict,
    ),
    "NX_POSINT": (
        int,
        np.ndarray,
        np.signedinteger,
    ),  # > 0 is checked in is_valid_data_field()
    "NX_COMPLEX": (complex, np.ndarray, np.cdouble, np.csingle),
    "NXDL_TYPE_UNAVAILABLE": (str,),  # Defaults to a string if a type is not provided.
}


def check_all_children_for_callable(objects: list, check: Callable, *args) -> bool:
    """Checks whether all objects in list are validated by given callable."""
    for obj in objects:
        if not check(obj, *args):
            return False

    return True


def is_valid_data_type(value, accepted_types):
    """Checks whether the given value or its children are of an accepted type."""
    if not isinstance(value, list):
        return isinstance(value, accepted_types)

    return check_all_children_for_callable(value, isinstance, accepted_types)


def is_positive_int(value):
    """Checks whether the given value or its children are positive."""

    def is_greater_than(num):
        return num.flat[0] > 0 if isinstance(num, np.ndarray) else num > 0

    if isinstance(value, list):
        return check_all_children_for_callable(value, is_greater_than)

    return value.flat[0] > 0 if isinstance(value, np.ndarray) else value > 0


def convert_str_to_bool_safe(value):
    """Only returns True or False if someone mistakenly adds quotation marks but mean a bool.

    For everything else it returns None.
    """
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return None


def is_valid_data_field(value, nxdl_type, path) -> bool:
    """Checks whether a given value is valid according to what is defined in the NXDL.

    This function will also try to convert typical types, for example int to float,
    and return the successful conversion.

    If it fails to convert, it raises an Exception.

    As a default it just returns the value again.
    """
    accepted_types = NEXUS_TO_PYTHON_DATA_TYPES[nxdl_type]

    if not isinstance(value, dict) and not is_valid_data_type(value, accepted_types):
        try:
            if accepted_types[0] is bool and isinstance(value, str):
                value = convert_str_to_bool_safe(value)
                if value is None:
                    raise ValueError
            return accepted_types[0](value)
        except ValueError:
            collector.collect_and_log(
                path, ValidationProblem.InvalidType, accepted_types, nxdl_type
            )

    if nxdl_type == "NX_POSINT" and not is_positive_int(value):
        collector.collect_and_log(path, ValidationProblem.IsNotPosInt, value)

    if nxdl_type in ("ISO8601", "NX_DATE_TIME"):
        iso8601 = re.compile(
            r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:"
            r"\.\d*)?)(((?!-00:00)(\+|-)(\d{2}):(\d{2})|Z){1})$"
        )
        results = iso8601.search(value)
        if results is None:
            collector.collect_and_log(path, ValidationProblem.InvalidDatetime, value)

    return True


@lru_cache(maxsize=None)
def path_in_data_dict(nxdl_path: str, data_keys: Tuple[str, ...]) -> List[str]:
    """Checks if there is an accepted variation of path in the dictionary & returns the path."""
    found_keys = []
    for key in data_keys:
        if nxdl_path == convert_data_converter_dict_to_nxdl_path(key):
            found_keys.append(key)
    return found_keys


def check_for_optional_parent(path: str, nxdl_root: ET._Element) -> str:
    """Finds a parent in the branch that is optional and returns it's path or s<<NOT_FOUND>>."""
    parent_path = path.rsplit("/", 1)[0]

    if parent_path == "":
        return "<<NOT_FOUND>>"

    parent_nxdl_path = convert_data_converter_dict_to_nxdl_path(parent_path)
    elem = nexus.get_node_at_nxdl_path(nxdl_path=parent_nxdl_path, elem=nxdl_root)

    if nexus.get_required_string(elem) in ("<<OPTIONAL>>", "<<RECOMMENDED>>"):
        return parent_path

    return check_for_optional_parent(parent_path, nxdl_root)


def is_node_required(nxdl_key, nxdl_root):
    """Checks whether a node at given nxdl path is required"""
    if nxdl_key[nxdl_key.rindex("/") + 1 :] == "@units":
        return False
    if nxdl_key[nxdl_key.rindex("/") + 1] == "@":
        nxdl_key = (
            nxdl_key[0 : nxdl_key.rindex("/") + 1]
            + nxdl_key[nxdl_key.rindex("/") + 2 :]
        )
    node = nexus.get_node_at_nxdl_path(nxdl_key, elem=nxdl_root, exc=False)
    return nexus.get_required_string(node) == "<<REQUIRED>>"


def all_required_children_are_set(optional_parent_path, data, nxdl_root):
    """Walks over optional parent's children and makes sure all required ones are set"""
    for key in data:
        if key in data["lone_groups"]:
            continue
        nxdl_key = convert_data_converter_dict_to_nxdl_path(key)
        name = nxdl_key[nxdl_key.rfind("/") + 1 :]
        renamed_path = f"{optional_parent_path}/{name}"
        if (
            nxdl_key[: nxdl_key.rfind("/")]
            == convert_data_converter_dict_to_nxdl_path(optional_parent_path)
            and is_node_required(nxdl_key, nxdl_root)
            and (renamed_path not in data or data[renamed_path] is None)
        ):
            return False

    return True


def is_nxdl_path_a_child(nxdl_path: str, parent: str):
    """Takes an NXDL path for an element and an NXDL parent and confirms it is a child."""
    while nxdl_path.rfind("/") != -1:
        nxdl_path = nxdl_path[0 : nxdl_path.rfind("/")]
        if parent == nxdl_path:
            return True
    return False


def is_group_part_of_path(path_to_group: str, path_of_entry: str) -> bool:
    """Returns true if a group is contained in a path"""

    tokens_group = path_to_group.split("/")
    tokens_entry = convert_data_converter_dict_to_nxdl_path(path_of_entry).split("/")

    if len(tokens_entry) < len(tokens_group):
        return False

    for tog, toe in zip(tokens_group, tokens_entry):
        if tog != toe:
            return False

    return True


def does_group_exist(path_to_group, data):
    """Returns True if the group or any children are set"""
    path_to_group = convert_data_converter_dict_to_nxdl_path(path_to_group)
    for path in data:
        if is_group_part_of_path(path_to_group, path) and data[path] is not None:
            return True
    return False


def get_concept_basepath(path: str) -> str:
    """Get the concept path from the path"""
    path_list = path.split("/")
    concept_path = []
    for p in path_list:
        if re.search(r"[A-Z]", p):
            concept_path.append(p)
    return "/" + "/".join(concept_path)


def remove_namespace_from_tag(tag):
    """Helper function to remove the namespace from an XML tag."""

    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def get_first_group(root):
    """Helper function to get the actual first group element from the NXDL."""
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root


def check_for_valid_atom_types(atoms: Union[str, list]):
    """Check for whether atom exists in periodic table."""

    if isinstance(atoms, list):
        for elm in atoms:
            if elm not in chemical_symbols:
                raise ValueError(
                    f"The element {elm} is not found in periodictable, "
                    f"check for correct element name"
                )
    elif isinstance(atoms, str):
        if atoms not in chemical_symbols:
            raise ValueError(
                f"The element {atoms} is not found in periodictable, "
                f"check for correct element name"
            )


def convert_to_hill(atoms_typ):
    """Convert list of atom into to hill."""
    if not isinstance(atoms_typ, list) and isinstance(atoms_typ, set):
        atoms_typ = list(atoms_typ)
    atoms_typ = sorted(atoms_typ)
    atom_list = []
    if "C" in atoms_typ:
        atom_list.append("C")
    if "H" in atoms_typ:
        atom_list.append("H")
    if atom_list:
        for char in atom_list:
            atoms_typ.remove(char)
    return atom_list + list(atoms_typ)


def add_default_root_attributes(data, filename):
    """
    Takes a dict/Template and adds NXroot fields/attributes that are inherently available
    """

    def update_and_warn(key: str, value: str):
        if key in data and data[key] != value:
            logger.warning(
                f"The NXroot entry '{key}' (value: {data[key]}) should not be changed by "
                f"the reader. This is overwritten by the actually used value '{value}'"
            )
        data[key] = value

    update_and_warn("/@NX_class", "NXroot")
    update_and_warn("/@file_name", filename)
    update_and_warn("/@file_time", str(datetime.now(timezone.utc).astimezone()))
    update_and_warn("/@file_update_time", data["/@file_time"])
    update_and_warn(
        "/@NeXus_repository",
        "https://github.com/FAIRmat-NFDI/nexus_definitions/"
        f"blob/{get_nexus_version_hash()}",
    )
    update_and_warn("/@NeXus_version", get_nexus_version())
    update_and_warn("/@HDF5_version", ".".join(map(str, h5py.h5.get_libversion())))
    update_and_warn("/@h5py_version", h5py.__version__)


def write_nexus_def_to_entry(data, entry_name: str, nxdl_def: str):
    """
    Writes the used nexus definition and version to /ENTRY/definition
    """

    def update_and_warn(key: str, value: str, overwrite=False):
        if key in data and data[key] is not None and data[key] != value:
            report = (
                f"This is overwritten by the actually used value '{value}'"
                if overwrite
                else f"The provided version '{value}' is kept. We assume you know what you are doing."
            )
            logger.log(
                logging.WARNING if overwrite else logging.INFO,
                f"The entry '{key}' (value: {data[key]}) should not be changed by "
                f"the reader. {report}",
            )
        if overwrite or data.get(key) is None:
            data[key] = value

    update_and_warn(f"/ENTRY[{entry_name}]/definition", nxdl_def, overwrite=True)
    update_and_warn(
        f"/ENTRY[{entry_name}]/definition/@version",
        get_nexus_version(),
        overwrite=False,
    )
    update_and_warn(
        f"/ENTRY[{entry_name}]/definition/@URL",
        "https://github.com/FAIRmat-NFDI/nexus_definitions/"
        f"blob/{get_nexus_version_hash()}",
        overwrite=False,
    )


def extract_atom_types(formula, mode="hill"):
    """Extract atom types form chemical formula."""
    atom_types: set = set()
    element: str = ""

    for char in formula:
        if char.isalpha():
            if char.isupper() and element == "":
                element = char
            elif char.isupper() and element != "" and element.isupper():
                check_for_valid_atom_types(element)
                atom_types.add(element)
                element = char
            elif char.islower() and element.isupper():
                element = element + char
                check_for_valid_atom_types(element)
                atom_types.add(element)
                element = ""

        else:
            if element.isupper():
                check_for_valid_atom_types(element)
                atom_types.add(element)
            element = ""
    if element.isupper():
        atom_types.add(element)

    atom_types = list(atom_types)
    atom_types = sorted(atom_types)

    if mode == "hill":
        return convert_to_hill(atom_types)

    return atom_types


# pylint: disable=too-many-branches
def transform_to_intended_dt(str_value: Any) -> Optional[Any]:
    """Transform string to the intended data type, if not then return str_value.

    E.g '2.5E-2' will be transfor into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'],
                 '23 34 444 5000', None
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32],
                 np.array([23 34 444 5000]), None
    NOTE: add another arg in this func for giving 'hint' what kind of data like
        numpy array or list
    Parameters
    ----------
    str_value : str
        Data from other format that comes as string e.g. string of list.

    Returns
    -------
    Union[str, int, float, np.ndarray]
        Converted data type
    """

    symbol_list_for_data_seperation = [";", " "]
    transformed: Any = None

    if isinstance(str_value, list):
        try:
            transformed = np.array(str_value, dtype=np.float64)
            return transformed
        except ValueError:
            pass

    elif isinstance(str_value, np.ndarray):
        return str_value
    elif isinstance(str_value, str):
        try:
            transformed = int(str_value)
        except ValueError:
            try:
                transformed = float(str_value)
            except ValueError:
                if "[" in str_value and "]" in str_value:
                    transformed = json.loads(str_value)
        if transformed is not None:
            return transformed
        for sym in symbol_list_for_data_seperation:
            if sym in str_value:
                parts = str_value.split(sym)
                modified_parts: List = []
                for part in parts:
                    part = transform_to_intended_dt(part)
                    if isinstance(part, (int, float)):
                        modified_parts.append(part)
                    else:
                        return str_value
                return transform_to_intended_dt(modified_parts)

    return str_value


def nested_dict_to_slash_separated_path(
    nested_dict: dict, flattened_dict: dict, parent_path=""
):
    """Convert nested dict into slash separeted path upto certain level."""
    sep = "/"

    for key, val in nested_dict.items():
        path = parent_path + sep + key
        if isinstance(val, dict):
            nested_dict_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val
