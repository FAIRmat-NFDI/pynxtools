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
"""Utilities for working with TFS/FEI-specific concepts."""

# pylint: disable=no-member

from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs_cfg import \
    TfsToNexusConceptMapping


def get_nexus_value(modifier, metadata: dict):
    """Interpret a functional mapping using data from dct via calling modifiers."""
    if isinstance(modifier, dict):
        # different commands are available
        if set(["fun", "terms"]) == set(modifier.keys()):
            if modifier["fun"] == "load_from":
                if modifier["terms"] in metadata.keys():
                    return metadata[modifier['terms']]
                else:
                    raise ValueError(f"Unable to interpret modififier load_from for argument {modifier['terms']}")
            if modifier["fun"] == "tfs_to_nexus":
                # print(metadata[modifier['terms']])
                if f"{modifier['terms']}/{metadata[modifier['terms']]}" in TfsToNexusConceptMapping.keys():
                    return TfsToNexusConceptMapping[f"{modifier['terms']}/{metadata[modifier['terms']]}"]
                else:
                    raise ValueError(f"Unable to interpret modifier tfs_to_nexus for argument {modifier['terms']}/{metadata[modifier['terms']]}")
        else:
            print(f"WARNING::Modifier {modifier} is currently not implemented !")
            # elif set(["link"]) == set(modifier.keys()), with the jsonmap reader Sherjeel conceptualized "link"
            return None
    elif isinstance(modifier, str):
        return modifier  # metadata[modifier]
    else:
        return None
