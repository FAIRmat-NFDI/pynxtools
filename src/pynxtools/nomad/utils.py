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

__REPLACEMENT_FOR_NX = ""

# This is a list of NeXus group names that are not allowed because they are defined as quantities in the BaseSection class.
UNALLOWED_GROUP_NAMES = {"name", "datetime", "lab_id", "description"}


def __rename_classes_in_nomad(nx_name: str) -> Optional[str]:
    """Replace subsection names in NOMAD that may cause collisions."""
    if nx_name in UNALLOWED_GROUP_NAMES:
        return nx_name + "__group"
    return nx_name


def __remove_nx_for_nomad(name: str, is_group: bool = False) -> Optional[str]:
    """
    Rename the NXDL name for NOMAD.
    For example: NXdata -> data,
    except NXobject -> NXobject
    """
    if name == "NXobject":
        return name
    if name is not None:
        if name.startswith("NX"):
            name = __REPLACEMENT_FOR_NX + name[2:]
    if is_group:
        name = __rename_classes_in_nomad(name)
    return name
