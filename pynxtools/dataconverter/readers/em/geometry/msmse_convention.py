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
"""Conventions used in the EBSD communnity

suggested by D. Rowenhorst et al. in DOI: 10.1088/0965-0393/23/8/083501.
"""

# pylint: disable=no-member,duplicate-code

msmse_convention = {
    "three_dimensional_rotation_handedness": "counter_clockwise",
    "rotation_convention": "passive",
    "euler_angle_convention": "zxz",
    "axis_angle_convention": "rotation_angle_on_interval_zero_to_pi"
}
# the sign convention is mentioned in the paper but left as a parameter
# "sign_convention": "p_minus_one"


def is_consistent_with_msmse_convention(dct):
    """Checks if a set of conventions is consistent with that paper (see above)."""
    # triple boolean, yes, no, unclear
    req_fields = [
        "three_dimensional_rotation_handedness",
        "rotation_convention",
        "euler_angle_convention",
        "axis_angle_convention"]
    for field_name in req_fields:
        if (field_name not in dct) or (field_name not in msmse_convention):
            return "unclear"
    # okay, so either matching or not
    for field_name in req_fields:
        if dct[field_name] == msmse_convention[field_name]:
            continue
        return "inconsistent"
    return "consistent"
