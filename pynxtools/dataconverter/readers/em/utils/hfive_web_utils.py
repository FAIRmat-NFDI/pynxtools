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
"""Utilities relevant when working with H5Web."""

import numpy as np


def hfive_web_decorate_nxdata(path: str, inp: dict) -> dict:
    if f"{path}" in inp.keys():
        inp[f"{path}/@CLASS"] = f"IMAGE"  # required by H5Web to plot RGB maps
        inp[f"{path}/@IMAGE_VERSION"] = f"1.2"
        inp[f"{path}/@SUBCLASS_VERSION"] = np.int64(15)
        inp[f"{path}/@long_name"] = f"Signal"
    return inp
