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

"""
Extract atom types - now in dataconverter/helper.py
"""

import xml.etree.ElementTree as EmtT
from typing import Tuple, List, Any, Union
import copy
import xarray as xr
import numpy as np
from ase.data import chemical_symbols


def extract_atom_types(formula: str) -> list:
    """Extract atom types form chemical formula."""

    def check_for_valid_atom_types(atom: str):
        """Check for whether atom exists in periodic table. """
        if atom not in chemical_symbols:
            raise ValueError(f"The element {atom} is not found in periodictable, "
                             f"check for correct element name")

    atom_types: set = set()
    element: str = ""
    # tested with "(C38H54S4)n(NaO2)5(CH4)NH3"
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

    return list(atom_types)
