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
    """
    Helper function to get entry name from data converter style entry:
    ENTRY[entry] -> entry
    """
    regex = re.compile(r'(?<=\[)(.*?)(?=\])')
    results = regex.search(entry)
    return entry if results is None else results.group(1)


def convert_data_dict_path_to_hdf5_path(path) -> str:
    """
    Helper function to convert data converter style path to HDF5 style path:
    /ENTRY[entry]/sample -> /entry/sample
    """
    hdf5path = ''
    for entry in path.split('/')[1:]:
        hdf5path += '/' + get_name_from_data_dict_entry(entry)
    return hdf5path


def is_value_valid_element_of_enum(value, elem) -> Tuple[bool, list]:
    """Checks whether a value has to be specific from the NXDL enumeration.
    Returns the list of enums"""
    if elem is not None:
        has_enums, enums = nexus.get_enums(elem)
        if has_enums and (isinstance(value, list) or value not in enums[0:-1] or value == ""):
            return False, enums
    return True, []


NUMPY_FLOAT_TYPES = (np.half, np.float16, np.single, np.double, np.longdouble)
NUMPY_INT_TYPES = (np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint)

NEXUS_TO_PYTHON_DATA_TYPES = {
    "ISO8601": (str),
    "NX_BINARY": (bytes, bytearray, np.byte, np.ubyte),
    "NX_BOOLEAN": (bool),
    "NX_CHAR": (str),
    "NX_DATE_TIME": (str),
    "NX_FLOAT": (float, np.ndarray) + NUMPY_FLOAT_TYPES,
    "NX_INT": (int, np.ndarray) + NUMPY_INT_TYPES,
    "NX_NUMBER": (int, float, np.ndarray) + NUMPY_INT_TYPES + NUMPY_FLOAT_TYPES,
    "NX_POSINT": (int, np.ndarray),  # value > 0 is checked in is_valid_data_type()
    "NXDL_TYPE_UNAVAILABLE": (str)  # Defaults to a string if a type is not provided.
}


def check_all_children_for_callable(objects: list, check: Callable, *args) -> bool:
    """Checks whether all objects in list are validated by given callable."""
    for obj in objects:
        if not check(obj, *args):
            return False

    return True


def is_valid_data_type(value, nxdl_type, path):
    """Checks whether a given value is valid according to what is defined in the NXDL."""
    accepted_types = NEXUS_TO_PYTHON_DATA_TYPES[nxdl_type]
    if not ((isinstance(value, list)
             and check_all_children_for_callable(value, isinstance, accepted_types))
            or isinstance(value, accepted_types)):
        raise Exception(f"The value at {path} should be of Python type: {accepted_types}"
                        f", as defined in the NXDL as {nxdl_type}.")

    is_greater_than = lambda x: x.flat[0] if isinstance(x, np.ndarray) else x > 0

    if (nxdl_type == "NX_POSINT"
            and ((not isinstance(value, list)
                  and (value.flat[0] < 0 if isinstance(value, np.ndarray) else value < 0))
                 or (isinstance(value, list)
                     and not check_all_children_for_callable(value,
                                                             is_greater_than)))):
        raise Exception(f"The value at {path} should be a positive int.")

    if nxdl_type in ("ISO8601", "NX_DATE_TIME"):
        iso8601 = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):"
                             r"(\d{2}(?:\.\d*)?)((-(\d{2}):(\d{2})|Z)?)$")
        results = iso8601.search(value)
        if results is None:
            raise Exception(f"The date at {path} should be an ISO8601 formatted str object.")


def path_in_data_dict(nxdl_path: str, data: dict) -> Tuple[bool, str]:
    """Checks if there is an accepted variation of path in the dictionary & returns the dict path"""
    for key in data.keys():
        if nxdl_path == convert_data_converter_dict_to_nxdl_path(key):
            return True, key
    return False, ""


def validate_data_dict(template: dict, data: dict, nxdl_root: ET.Element):
    """Checks whether all the required paths from the template are returned in data dict"""
    if nxdl_root is None:
        raise Exception("The NXDL file hasn't been loaded.")

    for path in template:
        nxdl_path = convert_data_converter_dict_to_nxdl_path(path)
        is_path_in_data_dict, renamed_path = path_in_data_dict(nxdl_path, data)

        entry_name = get_name_from_data_dict_entry(path[path.rindex('/') + 1:])
        if entry_name[0] == "@":
            if entry_name == "@units":
                is_valid_data_type(data[renamed_path], "NX_CHAR", renamed_path)
            continue

        elem = nexus.get_node_at_nxdl_path(nxdl_path=nxdl_path, elem=nxdl_root)

        if nexus.get_required_string(elem) == "<<REQUIRED>>" and \
           not is_path_in_data_dict or\
           data[renamed_path] is None:
            raise Exception(f"The data entry, {renamed_path}, is required and hasn't been "
                            "supplied by the reader.")
        nxdl_type = elem.attrib["type"] if "type" in elem.attrib.keys() else "NXDL_TYPE_UNAVAILABLE"

        is_valid_data_type(data[renamed_path], nxdl_type, renamed_path)
        is_valid_enum, enums = is_value_valid_element_of_enum(data[renamed_path], elem)
        if not is_valid_enum:
            raise Exception(f"The value at {renamed_path} should be"
                            f" one of the following strings: {enums}")

    return True


def remove_namespace_from_tag(tag):
    """Helper function to remove the namespace from an XML tag."""
    return tag.split("}")[-1]


def get_first_group(root):
    """Helper function to get the actual first group element from the NXDL"""
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root
