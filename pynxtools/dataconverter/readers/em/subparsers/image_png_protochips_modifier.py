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
"""Utilities for working with Protochips-specific concepts."""

# pylint: disable=no-member

import re
from numpy import pi


def specific_to_variadic(token):
    # "MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[0].DataValues.AuxiliaryDataValue.[20].HeatingPower"
    # to "MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HeatingPower"
    if isinstance(token, str) and token != "":
        concept = token.strip()
        idxs = re.finditer(r".\[[0-9]+\].", concept)
        if (sum(1 for _ in idxs) > 0):
            variadic = concept
            for idx in re.finditer(r".\[[0-9]+\].", concept):
                variadic = variadic.replace(concept[idx.start(0):idx.end(0)], ".[*].")
            return variadic
        else:
            return concept
    return None


def get_nexus_value(modifier, qnt_name, metadata: dict):
    """Interpret a functional mapping and modifier on qnt_name loaded from metadata."""
    if modifier == "load_from":
        if isinstance(qnt_name, str):
            for qnt in metadata.keys():
                if qnt_name == specific_to_variadic(qnt):
                    return metadata[qnt]
    elif modifier == "load_from_concatenate":
        if isinstance(qnt_name, list):
            retval = []
            for entry in qnt_name:
                for qnt in metadata.keys():
                    if entry == specific_to_variadic(qnt):
                        retval.append(metadata[qnt])
                        break  # breaking only out of the inner loop
            if retval != []:
                return retval
        return None
    else:
        return None
