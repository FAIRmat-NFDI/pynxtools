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
"""Low-level utility helpers for NeXus/HDF5 data handling.

Contains:
- HDF5 string/bytes decoding (``decode_if_string``)
- NXDL XML helpers (``get_nxdl_root_and_path``, ``get_all_parents_for``,
  ``get_appdef_root``, ``is_appdef``, ``is_variadic``,
  ``remove_namespace_from_tag``)
- NeXus-to-Python type mapping (``NEXUS_TO_PYTHON_DATA_TYPES``)

This module only depends on ``numpy``, ``lxml``, and
``pynxtools.definitions``; it must NOT import from ``pynxtools.nexus.nexus_tree``
or ``pynxtools.dataconverter`` to remain free of circular imports.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import lxml.etree as ET
import numpy as np

from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    decode_or_not,
    find_definition_file,
    get_nexus_definitions_path,
)

# ---------------------------------------------------------------------------
# NeXus primitive type aliases
# ---------------------------------------------------------------------------

nx_char = (str, np.character)
nx_int = (int, np.integer)
nx_float = (float, np.floating)
nx_number = nx_int + nx_float
nx_bool = (bool, np.bool_)

NEXUS_TO_PYTHON_DATA_TYPES: dict[str, tuple] = {
    "ISO8601": (str,),
    "NX_BINARY": (bytes, bytearray, np.bytes_),
    "NX_BOOLEAN": nx_bool,
    "NX_CHAR": nx_char,
    "NX_DATE_TIME": (str,),
    "NX_FLOAT": nx_float,
    "NX_INT": nx_int,
    "NX_UINT": (np.unsignedinteger,),
    "NX_NUMBER": nx_number,
    "NX_POSINT": nx_int,
    "NX_COMPLEX": (complex, np.complexfloating),
    "NX_CHAR_OR_NUMBER": nx_char + nx_number + nx_bool,
    "NXDL_TYPE_UNAVAILABLE": (nx_char,),
}

# ---------------------------------------------------------------------------
# NXDL XML utilities
# ---------------------------------------------------------------------------

_NXDL_DATA_DIR = Path(__file__).parent.parent / "data"

_NXDL_SPECIAL_NAMES = {
    "NXsimple": str(_NXDL_DATA_DIR / "NXsimple.nxdl.xml"),
    "NXtest": str(_NXDL_DATA_DIR / "NXtest.nxdl.xml"),
    "NXtest_extended": str(_NXDL_DATA_DIR / "NXtest_extended.nxdl.xml"),
}


def remove_namespace_from_tag(tag: str) -> str:
    """Strip the XML namespace from an element tag."""
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", maxsplit=1)[-1]


def get_nxdl_root_and_path(nxdl: str) -> tuple[ET._Element, str]:
    """Return (xml_root, file_path) for the given NXDL definition name.

    Args:
        nxdl: NXDL definition name, e.g. ``"NXarpes"`` or ``"NXdata"``.

    Raises:
        FileNotFoundError: If no NXDL file with that name can be found.
    """
    if nxdl in _NXDL_SPECIAL_NAMES:
        nxdl_f_path = _NXDL_SPECIAL_NAMES[nxdl]
    else:
        nxdl_f_path = find_definition_file(nxdl)
        if nxdl_f_path is None:
            raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")
    return ET.parse(nxdl_f_path).getroot(), nxdl_f_path


def get_appdef_root(xml_elem: ET._Element) -> ET._Element:
    """Return the root element of the lxml tree that contains *xml_elem*."""
    return xml_elem.getroottree().getroot()


def is_appdef(xml_elem: ET._Element) -> bool:
    """Return True if *xml_elem* belongs to an application definition."""
    return get_appdef_root(xml_elem).attrib.get("category") == "application"


def is_variadic(name: str, name_type: str) -> bool:
    """Return True if *name* is a variadic (template) concept name.

    A name is variadic when ``name_type`` is not ``"specified"``, or when
    *name* itself is ``None``/empty.
    """
    if name:
        return name_type != "specified"
    return True


def get_all_parents_for(xml_elem: ET._Element) -> list[ET._Element]:
    """Follow the ``extends`` chain from *xml_elem*'s definition root.

    Returns the list of parent XML roots, outermost first.
    """
    root = get_appdef_root(xml_elem)
    inheritance_chain: list[ET._Element] = []
    extends = root.get("extends")
    while extends is not None:
        parent_xml_root, _ = get_nxdl_root_and_path(extends)
        extends = parent_xml_root.get("extends")
        inheritance_chain.append(parent_xml_root)
    return inheritance_chain


def decode_if_string(
    elem: Any, encoding: str = "utf-8", decode: bool = True
) -> Any | None:
    """
    Decodes a numpy ndarray or list of byte objects or byte strings to strings.
    If `decode` is False, returns the input value unchanged. Non-byte/str types
    are returned without modification.

    Args:
        elem: A numpy ndarray, list, bytes, or any other object.
        encoding: The encoding scheme to use. Default is "utf-8".
        decode: A boolean flag indicating whether to perform decoding.

    Returns:
        A decoded string, a numpy array of decoded strings, a list of decoded strings,
        or the input value if not decodable.
        Returns None if the input is empty or invalid.

    Raises:
        ValueError: If decoding fails on bytes or numpy array elements.
    """
    if not decode:
        return elem

    if isinstance(elem, np.ndarray):
        if elem.size == 0:
            return elem  # Return the empty array unchanged

        # This only checks for null-terminated strings,
        # may need to be updated in the future: https://api.h5py.org/h5t.html
        if elem.dtype.kind == "S":  # Check if it's a bytes array (fixed-length strings)
            decoded_array = np.vectorize(
                lambda x: (
                    x.decode(encoding).rstrip("\x00") if isinstance(x, bytes) else x
                )
            )(elem)
            return decoded_array.astype(str)  # Ensure the dtype is str

        # Handle mixed-type arrays
        if elem.dtype == object:
            decoded_array = np.vectorize(
                lambda x: x.decode(encoding) if isinstance(x, bytes) else x
            )(elem)
            return decoded_array.astype(str)  # Ensure all elements are strings

    return decode_or_not(elem, encoding, decode)
