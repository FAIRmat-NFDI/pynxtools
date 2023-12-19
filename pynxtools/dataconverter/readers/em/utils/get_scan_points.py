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
"""Identify likely scan_point_positions for specific EBSD grid types."""

# pylint: disable=no-member

import numpy as np

from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    HEXAGONAL_GRID, SQUARE_GRID, REGULAR_TILING, FLIGHT_PLAN


def get_scan_point_axis_values(inp: dict, dim_name: str):
    is_threed = False
    if "dimensionality" in inp.keys():
        if inp["dimensionality"] == 3:
            is_threed = True
    req_keys = ["grid_type", f"n_{dim_name}", f"s_{dim_name}"]
    for key in req_keys:
        if key not in inp.keys():
            raise ValueError(f"Unable to find required key {key} in inp !")

    if inp["grid_type"] in [HEXAGONAL_GRID, SQUARE_GRID]:
        return np.asarray(np.linspace(0,
                                      inp[f"n_{dim_name}"] - 1,
                                      num=inp[f"n_{dim_name}"],
                                      endpoint=True) * inp[f"s_{dim_name}"], np.float32)
    else:
        return None


def threed(inp: dict):
    """Identify if 3D triboolean."""
    if "dimensionality" in inp.keys():
        if inp["dimensionality"] == 3:
            return True
        return False
    return None


def square_grid(inp: dict):
    """Identify if square grid with specific assumptions."""
    if inp["grid_type"] == SQUARE_GRID and inp["tiling"] == REGULAR_TILING and inp["flight_plan"] == FLIGHT_PLAN:
        return True
    return False


def hexagonal_grid(inp: dict):
    """Identify if square grid with specific assumptions."""
    if inp["grid_type"] == HEXAGONAL_GRID and inp["tiling"] == REGULAR_TILING and inp["flight_plan"] == FLIGHT_PLAN:
        return True
    return False


def get_scan_point_coords(inp: dict) -> dict:
    """Add scan_point_dim array assuming top-left to bottom-right snake style scanning."""
    is_threed = threed(inp)
    req_keys = ["grid_type", "tiling", "flight_plan"]
    dims = ["x", "y"]
    if is_threed is True:
        dims.append("z")
    for dim in dims:
        req_keys.append(f"n_{dim}")
        req_keys.append(f"s_{dim}")

    for key in req_keys:
        if key not in inp.keys():
            raise ValueError(f"Unable to find required key {key} in inp !")

    if is_threed is False:
        if square_grid(inp) is True:
            for dim in dims:
                if "scan_point_{dim}" in inp.keys():
                    print("WARNING::Overwriting scan_point_{dim} !")
            inp["scan_point_x"] = np.tile(
                np.linspace(0, inp["n_x"] - 1, num=inp["n_x"], endpoint=True) * inp["s_x"], inp["n_y"])
            inp["scan_point_y"] = np.repeat(
                np.linspace(0, inp["n_y"] - 1, num=inp["n_y"], endpoint=True) * inp["s_y"], inp["n_x"])
        elif hexagonal_grid(inp) is True:
            for dim in dims:
                if "scan_point_{dim}" in inp.keys():
                    print("WARNING::Overwriting scan_point_{dim} !")
            # the following code is only the same as for the sqrgrid because
            # typically the tech partners already take into account and export scan step
            # values such that for a hexagonal grid one s_{dim} (typically s_y) is sqrt(3)/2*s_{other_dim} !
            inp["scan_point_x"] = np.tile(
                np.linspace(0, inp["n_x"] - 1, num=inp["n_x"], endpoint=True) * inp["s_x"], inp["n_y"])
            inp["scan_point_y"] = np.repeat(
                np.linspace(0, inp["n_y"] - 1, num=inp["n_y"], endpoint=True) * inp["s_y"], inp["n_x"])
        else:
            print("WARNING::{__name__} facing an unknown scan strategy !")
    else:
        print("WARNING::{__name__} not implemented for 3D case !")
    return inp
