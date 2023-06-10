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
"""Utility for analyzing swift data/metadata of display_items to identify NeXus concepts."""

# pylint: disable=no-member

import flatdict as fd


metadata_constraints = {"type": str,
                        "uuid": str,
                        "created": str,
                        "data_shape": list,
                        "data_dtype": str,
                        "is_sequence": bool,
                        "dimensional_calibrations": list,
                        "data_modified": str,
                        "timezone": str,
                        "timezone_offset": str,
                        "metadata/hardware_source/hardware_source_id": str,
                        "version": int,
                        "modified": str}

nexus_concept_dict = {"ITULL": "NxImageSetRealSpace",
                      "IFLL": "NxImageSetRealSpace",
                      "IFL": None,
                      "ITUL": None,
                      "STUUE": "NxSpectrumSetEelsOmegaQ",
                      "STULLE": "NxSpectrumSetEels",
                      "STULLUE": "NxSpectrumSetOmegaQ",
                      "SFLLUE": "NxSpectrumSetOmegaQ",
                      "SFLLE": "NxSpectrumSetEels",
                      "SFUE": "NxSpectrumSetEelsOmegaQ",
                      "RFAA": "NxImageAngSpace",
                      "RTUAA": "NxImageAngSpace"}


def check_existence_of_required_fields(dct: dict, constraint_dct: dict) -> bool:
    """Checks if given dictionary has fields with values which match constraints."""
    flat_dct = fd.FlatDict(dct, delimiter='/')
    for keyword, dtyp in constraint_dct.items():
        if keyword not in flat_dct.keys():
            print(f"-->{keyword} not keyword")
            return False
        if not isinstance(flat_dct[keyword], dtyp):
            print(f"-->{keyword} not instance")
            return False
    return True


def identify_nexus_concept_key(dct: dict) -> str:
    """Identifies best candidate to map data/metadata on a NeXus concept."""
    # ##MK::imporve that we work ideally always with the flattened dictionary
    nexus_concept_key = "UNKNOWN"
    if check_existence_of_required_fields(dct, metadata_constraints) is False:
        return nexus_concept_key
    lst_unit_catg = []
    for axis_dict in dct["dimensional_calibrations"]:  # inspect axes in sequence
        if isinstance(axis_dict, dict):
            if set(axis_dict.keys()) == set(["offset", "scale", "units"]):
                unit_arg = axis_dict["units"].lower()
                if unit_arg == "":
                    lst_unit_catg.append("U")
                elif unit_arg in ["nm"]:  # replace by pint to pick up on any length
                    lst_unit_catg.append("L")
                elif unit_arg in ["ev"]:  # replace by pint to pick up on any enery
                    lst_unit_catg.append("E")
                elif unit_arg in ["rad"]:  # replace by pint to pick up on angle unit
                    lst_unit_catg.append("A")
                else:
                    return nexus_concept_key
        set_unit_catg = set(lst_unit_catg)

        if "A" in set_unit_catg:
            nexus_concept_key \
                = f"R{str(dct['is_sequence']).upper()[0:1]}{''.join(lst_unit_catg)}"
        elif "E" in set_unit_catg:
            nexus_concept_key \
                = f"S{str(dct['is_sequence']).upper()[0:1]}{''.join(lst_unit_catg)}"
        elif "E" not in set_unit_catg:
            nexus_concept_key \
                = f"I{str(dct['is_sequence']).upper()[0:1]}{''.join(lst_unit_catg)}"
        else:
            return nexus_concept_key
    return nexus_concept_key
