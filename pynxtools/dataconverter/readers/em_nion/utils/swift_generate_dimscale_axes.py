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

from typing import List, Any

import numpy as np

from pynxtools.dataconverter.readers.em_nion.map_concepts.swift_display_items_to_nx \
    import metadata_constraints, check_existence_of_required_fields  # nexus_concept_dict


def get_list_of_dimension_scale_axes(dct: dict) -> list:  # , concept_key: str
    """Create a list of dimension scale axes value, unit tuples."""
    # use only when we know already onto which concept a display_item will be mapped
    axes: List[Any] = []
    if (check_existence_of_required_fields(dct, metadata_constraints) is False):
        return axes
    #        or concept_key not in nexus_concept_dict.keys():
    # if nexus_concept_dict[concept_key] is None:
    #     return axes
    if len(dct["dimensional_calibrations"]) != len(dct["data_shape"]):
        return axes

    print(dct["dimensional_calibrations"])
    print(dct["data_shape"])

    for idx in np.arange(0, len(dct["dimensional_calibrations"])):
        nvalues = dct["data_shape"][idx]
        axis_dict = dct["dimensional_calibrations"][idx]
        if isinstance(nvalues, int) and isinstance(axis_dict, dict):
            if (nvalues > 0) \
                    and (set(axis_dict.keys()) == set(["offset", "scale", "units"])):
                start = axis_dict["offset"] + 0.5 * axis_dict["scale"]
                stop = axis_dict["offset"] + ((nvalues - 1) + 0.5) * axis_dict["scale"]
                axes.append(
                    {"value": np.asarray(np.linspace(start,
                                                     stop,
                                                     num=nvalues,
                                                     endpoint=True), np.float64),
                     "unit": axis_dict["units"]})
    return axes
