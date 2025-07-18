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

from typing import Optional

import numpy as np

try:
    from nomad.metainfo.data_type import (
        Bytes,
        Datetime,
        m_bool,
        m_complex128,
        m_float64,
        m_int,
        m_int64,
        m_str,
    )
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

REPLACEMENT_FOR_NX = ""

# This is a list of NeXus group names that are not allowed because they are defined as quantities in the BaseSection class.
UNALLOWED_GROUP_NAMES = {"name", "datetime", "lab_id", "description"}

NX_TYPES = {  # Primitive Types,  'ISO8601' is the only type not defined here
    "NX_COMPLEX": m_complex128,
    "NX_FLOAT": m_float64,
    "NX_CHAR": m_str,
    "NX_BOOLEAN": m_bool,
    "NX_INT": m_int64,
    "NX_UINT": m_int64,
    "NX_NUMBER": m_float64,
    "NX_POSINT": m_int64,
    "NX_BINARY": Bytes,
    "NX_DATE_TIME": Datetime,
    "NX_CHAR_OR_NUMBER": m_float64,  # TODO: fix this mapping
}

FIELD_STATISTICS: dict[str, list] = {
    "suffix": ["__mean", "__std", "__min", "__max", "__size", "__ndim"],
    "function": [np.mean, np.std, np.min, np.max, np.size, np.ndim],
    "type": [np.float64, np.float64, None, None, np.int32, np.int32],
    "mask": [True, True, True, True, False, False],
}


def _rename_classes_in_nomad(nx_name: str) -> str:
    """
    Modify group names that conflict with NOMAD due to being defined as quantities
    in the BaseSection class by appending '__group' to those names.

    Some quantities names names are reserved in the BaseSection class (or even higher up in metainfo),
    and thus require renaming to avoid collisions.

    Args:
        nx_name (str): The original group name.

    Returns:
        Optional[str]: The modified group name with '__group' appended if it's in
        UNALLOWED_GROUP_NAMES, or the original name if no change is needed.
    """
    return nx_name + "__group" if nx_name in UNALLOWED_GROUP_NAMES else nx_name


def _rename_nx_for_nomad(
    name: str,
    is_group: bool = False,
    is_field: bool = False,
    is_attribute: bool = False,
) -> Optional[str]:
    """
    Rename NXDL names for compatibility with NOMAD, applying specific rules
    based on the type of the NeXus concept. (group, field, or attribute).

    - NXobject is unchanged.
    - NX-prefixed names (e.g., NXdata) are renamed by replacing 'NX' with a custom string.
    - Group names are passed to _rename_classes_in_nomad(), and the result is capitalized.
    - Fields and attributes have '__field' or '__attribute' appended, respectively.

    Args:
        name (str): The NXDL name.
        is_group (bool): Whether the name represents a group.
        is_field (bool): Whether the name represents a field.
        is_attribute (bool): Whether the name represents an attribute.

    Returns:
        Optional[str]: The renamed NXDL name, with group names capitalized,
        or None if input is invalid.
    """
    if name and name.startswith("NX"):
        name = REPLACEMENT_FOR_NX + name[2:]
        name = name[0].upper() + name[1:]

    if name[0] in "0123456789":
        name = f"_{name}"

    if is_group:
        name = _rename_classes_in_nomad(name)
    elif is_field:
        name += "__field"
    elif is_attribute:
        pass
    return name


def get_quantity_base_name(quantity_name):
    return (
        quantity_name[:-7]
        if quantity_name.endswith("__field") and quantity_name[-8] != "_"
        else quantity_name
    )
