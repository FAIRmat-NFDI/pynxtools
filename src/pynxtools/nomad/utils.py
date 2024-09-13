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

__REPLACEMENT_FOR_NX = "BS"


def __rename_nx_to_nomad(name: str) -> Optional[str]:
    """
    Rename the NXDL name to NOMAD.
    For example: NXdata -> BSdata,
    except NXobject -> NXobject
    """
    if name == "NXobject":
        return name
    if name is not None:
        if name.startswith("NX"):
            return name.replace("NX", __REPLACEMENT_FOR_NX)
    return name
