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
"""For given energy range find possible X-ray emission lines in this region."""

import xraydb

from ase.data import chemical_symbols


def get_all_xraylines() -> dict:
    xray_lines = {}
    for symbol in chemical_symbols[1:]:
        for name, line in xraydb.xray_lines(symbol).items():
            xray_lines[f"{symbol}-{name}"] = line.energy
    return xray_lines


def get_xrayline_candidates(e_min, e_max) -> list:
    # one could try to resolve the line from the alias of
    # the actual entry but this is not rigorous!
    cand = []
    for key, val in get_all_xraylines().items():
        if val < e_min:
            continue
        if val > e_max:
            continue
        cand.append(key)
    return cand
