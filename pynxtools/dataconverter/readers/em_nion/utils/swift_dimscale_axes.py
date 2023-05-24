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
"""Utility for creating list of numpy arrays with dimension scale axes values."""

# pylint: disable=no-member


def identify_dimension_scale_axes(dct: dict, nx_concept_key: str) -> list:
    """Create a list of dimension scale axes value, unit tuples."""
    axes = []
    if (check_existence_of_required_fields(dct, metadata_constraints) is False) \
            or nx_concept_key not in nexus_concept_dict.keys():
        return axes
    if nexus_concept_dict[nx_concept_key] is None:
        return axes
    if len(dct["dimensional_calibrations"]) != len(dct["data_shape"]):
        return axes

    for idx in np.arange(0, len(dct["dimensional_calibrations"])):
        nvalues = dct["data_shape"][idx]
        axis_dict = dct["dimensional_calibrations"][idx]
        if isinstance(nvalues, int) and isinstance(axis_dict, dict):
            if (nvalues > 0) \
                    and (set(axis_dict.keys()) == set(["offset", "scale", "units"])):
                axes.append({"value": np.asarray(
                    np.linspace(axis_dict["offset"],
                                axis_dict["offset"]+nvalues*axis_dict["scale"],
                                num=nvalues,endpoint=True), np.float64),
                             "unit": axis_dict["units"]
                            })
    return axes
