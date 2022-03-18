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

from typing import Tuple, Callable
import re
import xml.etree.ElementTree as ET

import numpy as np

from nexusparser.tools import nexus


def generate_template_from_nxdl(root, template, path=None, nxdl_root=None):
    """Helper function to generate a template dictionary for given NXDL"""
    if nxdl_root is None:
        nxdl_root = root
        root = get_first_group(root)
    if path is None:
        path = ""

    tag = remove_namespace_from_tag(root.tag)

    if tag == "doc":
        return

    suffix = ""
    if "name" in root.attrib:
        suffix = root.attrib['name']
    elif "type" in root.attrib:
        nexus_class = convert_nexus_to_caps(root.attrib['type'])
        hdf5name = f"[{convert_nexus_to_suggested_name(root.attrib['type'])}]"
        suffix = f"{nexus_class}{hdf5name}"

    if tag == "attribute":
        suffix = f"@{suffix}"

    path = path + "/" + suffix

    # Only add fields or attributes to the dictionary
    if tag in ("field", "attribute"):
        optionality = get_required_string(root)
        if optionality == "required":
            optional_parent = check_for_optional_parent(path, nxdl_root)
            optionality = "required" if optional_parent == "<<NOT_FOUND>>" else "optional"
            if optional_parent != "<<NOT_FOUND>>":
                template.optional_parents.append(optional_parent)
        template[optionality][path] = None

        # Only add units if it is a field and the the units are defined but not set to NX_UNITLESS
        if tag == "field" \
           and ("units" in root.attrib.keys() and root.attrib["units"] != "NX_UNITLESS"):
            template[optionality][f"{path}/@units"] = None

    for child in root:
        generate_template_from_nxdl(child, template, path, nxdl_root)


def get_required_string(elem):
    """Helper function to return nicely formatted names for optionality."""
    return nexus.get_required_string(elem)[2:-2].lower()


def convert_nexus_to_caps(nexus_name):
    """Helper function to convert a Nexus class from <NxClass> to <CLASS>."""
    return nexus_name[2:].upper()


def convert_nexus_to_suggested_name(nexus_name):
    """Helper function to suggest a name for a group from its Nexus class."""
    return nexus_name[2:]


def convert_data_converter_entry_to_nxdl_path_entry(entry) -> str:
    """
    Helper function to convert data converter style entry to NXDL style entry:
    ENTRY[entry] -> ENTRY
    """
    regex = re.compile(r'(.*?)(?=\[)')
    results = regex.search(entry)
    return entry if results is None else results.group(1)


def convert_data_converter_dict_to_nxdl_path(path) -> str:
    """
    Helper function to convert data converter style path to NXDL style path:
    /ENTRY[entry]/sample -> /ENTRY/sample
    """
    nxdl_path = ''
    for entry in path.split('/')[1:]:
        nxdl_path += '/' + convert_data_converter_entry_to_nxdl_path_entry(entry)
    return nxdl_path


def get_name_from_data_dict_entry(entry) -> str:
    """Helper function to get entry name from data converter style entry

    ENTRY[entry] -> entry
    """
    regex = re.compile(r'(?<=\[)(.*?)(?=\])')
    results = regex.search(entry)
    return entry if results is None else results.group(1)


def convert_data_dict_path_to_hdf5_path(path) -> str:
    """Helper function to convert data converter style path to HDF5 style path

    /ENTRY[entry]/sample -> /entry/sample
    """
    hdf5path = ''
    for entry in path.split('/')[1:]:
        hdf5path += '/' + get_name_from_data_dict_entry(entry)
    return hdf5path


def is_value_valid_element_of_enum(value, elem) -> Tuple[bool, list]:
    """Checks whether a value has to be specific from the NXDL enumeration and returns options."""
    if elem is not None:
        has_enums, enums = nexus.get_enums(elem)
        if has_enums and (isinstance(value, list)
                          or value not in enums[1:-1].split(",") or value == ""):
            return False, enums
    return True, []


NUMPY_FLOAT_TYPES = (np.half, np.float16, np.single, np.double, np.longdouble)
NUMPY_INT_TYPES = (np.short, np.intc, np.int_)
NUMPY_UINT_TYPES = (np.ushort, np.uintc, np.uint)

NEXUS_TO_PYTHON_DATA_TYPES = {
    "ISO8601": (str),
    "NX_BINARY": (bytes, bytearray, np.byte, np.ubyte, np.ndarray),
    "NX_BOOLEAN": (bool, np.ndarray, np.bool_),
    "NX_CHAR": (str, np.ndarray, np.chararray),
    "NX_DATE_TIME": (str),
    "NX_FLOAT": (float, np.ndarray, np.floating),
    "NX_INT": (int, np.ndarray, np.signedinteger),
    "NX_UINT": (np.ndarray, np.unsignedinteger),
    "NX_NUMBER": (int, float, np.ndarray, np.signedinteger, np.unsignedinteger, np.floating, dict),
    "NX_POSINT": (int, np.ndarray, np.signedinteger),  # > 0 is checked in is_valid_data_field()
    "NXDL_TYPE_UNAVAILABLE": (str)  # Defaults to a string if a type is not provided.
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
    is_greater_than = lambda x: x.flat[0] > 0 if isinstance(x, np.ndarray) else x > 0

    if isinstance(value, list):
        return check_all_children_for_callable(value, is_greater_than)

    return value.flat[0] > 0 if isinstance(value, np.ndarray) else value > 0


def is_valid_data_field(value, nxdl_type, path):
    """Checks whether a given value is valid according to what is defined in the NXDL."""
    accepted_types = NEXUS_TO_PYTHON_DATA_TYPES[nxdl_type]

    if not is_valid_data_type(value, accepted_types):
        raise Exception(f"The value at {path} should be of Python type: {accepted_types}"
                        f", as defined in the NXDL as {nxdl_type}.")

    if nxdl_type == "NX_POSINT" and not is_positive_int(value):
        raise Exception(f"The value at {path} should be a positive int.")

    if nxdl_type in ("ISO8601", "NX_DATE_TIME"):
        iso8601 = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:"
                             r"\.\d*)?)(((?!-00:00)(\+|-)(\d{2}):(\d{2})|Z){1})$")
        results = iso8601.search(value)
        if results is None:
            raise Exception(f"The date at {path} should be a timezone aware ISO8601 "
                            f"formatted str. For example, 2022-01-22T12:14:12.05018Z"
                            f" or 2022-01-22T12:14:12.05018+00:00.")


def path_in_data_dict(nxdl_path: str, data: dict) -> Tuple[bool, str]:
    """Checks if there is an accepted variation of path in the dictionary & returns the path."""
    for key in data.keys():
        if nxdl_path == convert_data_converter_dict_to_nxdl_path(key):
            return True, key
    return False, ""


def check_for_optional_parent(path: str, nxdl_root: ET.Element) -> str:
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
    if nxdl_key[nxdl_key.rindex("/") + 1:] == "@units":
        return False
    if nxdl_key[nxdl_key.rindex("/") + 1] == "@":
        nxdl_key = nxdl_key[0:nxdl_key.rindex("/") + 1] + nxdl_key[nxdl_key.rindex("/") + 2:]
    node = nexus.get_node_at_nxdl_path(nxdl_key, elem=nxdl_root)
    return nexus.get_required_string(node) == "<<REQUIRED>>"


def all_required_children_are_set(optional_parent_path, data, nxdl_root):
    """Walks over optional parent's children and makes sure all required ones are set"""
    optional_parent_path = convert_data_converter_dict_to_nxdl_path(optional_parent_path)
    for key in data:
        nxdl_key = convert_data_converter_dict_to_nxdl_path(key)
        if optional_parent_path in nxdl_key \
           and is_node_required(nxdl_key, nxdl_root) \
           and data[key] is None:
            return False

    return True


def check_optionality_based_on_parent_group(
        path,
        nxdl_path,
        nxdl_root,
        data,
        template):
    """Checks whether field is part of an optional parent and then confirms its optionality"""
    for optional_parent in template["optional_parents"]:
        optional_parent_nxdl = convert_data_converter_dict_to_nxdl_path(optional_parent)
        if optional_parent_nxdl in nxdl_path \
           and not all_required_children_are_set(optional_parent, data, nxdl_root):
            raise Exception(f"The data entry, {path}, has an optional parent, "
                            f"{optional_parent}, with required children set. Either"
                            f" provide no children for {optional_parent} or provide"
                            f" all required ones.")


def ensure_all_required_fields_exist(template, data):
    """Checks whether all the required fields are in the returned data object."""
    for path in template["required"]:
        entry_name = get_name_from_data_dict_entry(path[path.rindex('/') + 1:])
        if entry_name == "@units":
            continue
        nxdl_path = convert_data_converter_dict_to_nxdl_path(path)
        is_path_in_data_dict, renamed_path = path_in_data_dict(nxdl_path, data)
        if not is_path_in_data_dict or data[renamed_path] is None:
            raise Exception(f"The data entry corresponding to {path} is required and"
                            f" hasn't been supplied by the reader.")


def validate_data_entry(path, template, data, nxdl_root, undocumented=False):
    """Checks whether a given entry in the data dict adheres to the schema definition."""
    elem = None
    if data[path] is not None:
        entry_name = get_name_from_data_dict_entry(path[path.rindex('/') + 1:])
        nxdl_path = convert_data_converter_dict_to_nxdl_path(path)

        if entry_name == "@units":
            return
        if entry_name[0] == "@":
            if nxdl_path.find("@") >= 0: # Only strip @ from path if it is contained.
                index_of_at = nxdl_path.rindex("@")
                nxdl_path = nxdl_path[0:index_of_at] + nxdl_path[index_of_at + 1:]

        try:
            elem = nexus.get_node_at_nxdl_path(nxdl_path=nxdl_path, elem=nxdl_root)
        except nexus.NxdlAttributeError as error:
            # print(error)
            print(f'Attributes were not found for element {path}.')

        # Only check for validation in the NXDL if we did find the entry
        # otherwise we just pass it along
        if elem is not None \
           and remove_namespace_from_tag(elem.tag) in ("field", "attribute"):
            if undocumented:
                data[get_required_string(elem)][path] = data["undocumented"][path]
                del data["undocumented"][path]
                units_path = f"{path}/@units"
                if units_path in data["undocumented"]:
                    data[get_required_string(elem)][units_path] = data["undocumented"][units_path]
                    del data["undocumented"][units_path]

            check_optionality_based_on_parent_group(path, nxdl_path, nxdl_root, data, template)

            attrib = elem.attrib
            nxdl_type = attrib["type"] if "type" in attrib.keys() else "NXDL_TYPE_UNAVAILABLE"
            is_valid_data_field(data[path], nxdl_type, path)
            is_valid_enum, enums = is_value_valid_element_of_enum(data[path], elem)
            if not is_valid_enum:
                raise Exception(f"The value at {path} should be"
                                f" one of the following strings: {enums}")


def validate_data_dict(template, data, nxdl_root: ET.Element):
    """Checks whether all the required paths from the template are returned in data dict."""
    assert nxdl_root is not None, "The NXDL file hasn't been loaded."

    # Make sure all required fields exist.
    ensure_all_required_fields_exist(template, data)

    for path in data.get_documented().keys():
        validate_data_entry(path, template, data, nxdl_root)

    for path in list(data["undocumented"]):
        validate_data_entry(path, template, data, nxdl_root, True)

    return True


def remove_namespace_from_tag(tag):
    """Helper function to remove the namespace from an XML tag."""
    return tag.split("}")[-1]


def get_first_group(root):
    """Helper function to get the actual first group element from the NXDL."""
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root
