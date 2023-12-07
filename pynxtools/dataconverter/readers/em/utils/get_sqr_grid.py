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
"""Discretize point cloud in R^d (d=2, 3) with mark data to square/cube voxel grid."""

# pylint: disable=no-member

import numpy as np
from scipy.spatial import KDTree

from pynxtools.dataconverter.readers.em.examples.ebsd_database import SQUARE_GRID
from pynxtools.dataconverter.readers.em.utils.get_scan_points import \
    threed, square_grid, hexagonal_grid


def get_scan_points_with_mark_data_discretized_on_sqr_grid(src_grid: dict,
                                                           max_edge_length: int) -> dict:
    """Inspect grid_type, dimensionality, point locations, and mark src_grida, map then."""
    is_threed = threed(src_grid)
    req_keys = ["grid_type", "tiling", "flight_plan"]
    dims = ["x", "y"]
    if is_threed is True:
        dims.append("z")
    for dim in dims:
        req_keys.append(f"scan_point_{dim}")
        req_keys.append(f"n_{dim}")
        req_keys.append(f"s_{dim}")

    trg_grid = {}
    for key in req_keys:
        if key not in src_grid.keys():
            raise ValueError(f"Unable to find required key {key} in src_grid !")

    # take discretization of the source grid as a guide for the target_grid
    # optimization possible if square grid and matching maximum_extent

    max_extent = None
    if is_threed is False:
        max_extent = np.max((src_grid["n_x"], src_grid["n_y"]))
    else:
        max_extent = np.max((src_grid["n_x"], src_grid["n_y"], src_grid["n_z"]))

    if square_grid(src_grid) is True:
        if max_extent <= max_edge_length:
            return src_grid
        else:
            # too large square grid has to be discretized and capped
            # cap to the maximum extent to comply with h5web technical constraints
            max_extent = max_edge_length
    elif hexagonal_grid(src_grid) is True:
        if max_extent > max_edge_length:
            max_extent = max_edge_length
    else:
        raise ValueError(f"Facing an unsupported grid type !")

    # all non-square grids or too large square grids will be
    # discretized onto a regular grid with square or cubic pixel/voxel
    aabb = []
    for dim in dims:
        aabb.append(np.min(src_grid[f"scan_point_{dim}"] - 0.5 * src_grid[f"s_{dim}"]))
        aabb.append(np.max(src_grid[f"scan_point_{dim}"] + 0.5 * src_grid[f"s_{dim}"]))
    print(f"{aabb}")

    if is_threed is False:
        if aabb[1] - aabb[0] >= aabb[3] - aabb[2]:
            trg_sxy = (aabb[1] - aabb[0]) / max_extent
            trg_nxy = [max_extent, int(np.ceil((aabb[3] - aabb[2]) / trg_sxy))]
        else:
            trg_sxy = (aabb[3] - aabb[2]) / max_extent
            trg_nxy = [int(np.ceil((aabb[1] - aabb[0]) / trg_sxy)), max_extent]
        print(f"H5Web default plot generation, scaling src_nxy "
              f"{[src_grid['n_x'], src_grid['n_y']]}, trg_nxy {trg_nxy}")
        # the above estimate is not exactly correct (may create a slight real space shift)
        # of the EBSD map TODO:: regrid the real world axis-aligned bounding box aabb with
        # a regular tiling of squares or hexagons
        # https://stackoverflow.com/questions/18982650/differences-between-matlab-and-numpy-and-pythons-round-function
        # MTex/Matlab round not exactly the same as numpy round but reasonably close

        # scan point positions were normalized by tech partner subparsers such that they
        # always build on pixel coordinates calibrated for step size not by giving absolute positions
        # in the sample surface frame of reference as this is typically not yet consistently documented
        # because we assume in addition that we always start at the top left corner the zeroth/first
        # coordinate is always 0., 0. !
        trg_xy = np.column_stack((np.tile(np.linspace(0, trg_nxy[0] - 1, num=trg_nxy[0], endpoint=True) * trg_sxy, trg_nxy[1]),
                                  np.repeat(np.linspace(0, trg_nxy[1] - 1, num=trg_nxy[1], endpoint=True) * trg_sxy, trg_nxy[0])))
        # TODO:: if scan_point_{dim} are calibrated this approach
        # here would shift the origin to 0, 0 implicitly which may not be desired
        print(f"trg_xy {trg_xy}, shape {np.shape(trg_xy)}")
        tree = KDTree(np.column_stack((src_grid["scan_point_x"], src_grid["scan_point_y"])))
        d, idx = tree.query(trg_xy, k=1)
        if np.sum(idx == tree.n) > 0:
            raise ValueError(f"kdtree query left some query points without a neighbor!")
        del d
        del tree

        # rebuild src_grid container with only the relevant src_grida selected from src_grid
        for key in src_grid.keys():
            if key == "euler":
                trg_grid[key] = np.empty((np.shape(trg_xy)[0], 3), np.float32)
                trg_grid[key].fill(np.nan)
                trg_grid[key] = src_grid["euler"][idx, :]
                if np.isnan(trg_grid[key]).any() is True:
                    raise ValueError(f"Downsampling of the point cloud left "
                                     f"pixels without mark data {key} !")
                print(f"final np.shape(trg_grid[{key}]) {np.shape(trg_grid[key])}")
            elif key == "phase_id" or key == "bc":
                trg_grid[key] = np.empty((np.shape(trg_xy)[0],), np.int32)
                trg_grid[key].fill(np.int32(-2))
                # pyxem_id is at least -1, bc is typically positive
                trg_grid[key] = src_grid[key][idx]
                if np.sum(trg_grid[key] == -2) > 0:
                    raise ValueError(f"Downsampling of the point cloud left "
                                     f"pixels without mark data {key} !")
                print(f"final np.shape(trg_grid[{key}]) {np.shape(trg_grid[key])}")
            elif key == "ci" or key == "mad":
                trg_grid[key] = np.empty((np.shape(trg_xy)[0],), np.float32)
                trg_grid[key].fill(np.nan)
                trg_grid[key] = src_grid[key][idx]
                print(f"final np.shape(trg_grid[{key}]) {np.shape(trg_grid[key])}")
                if np.isnan(trg_grid[key]).any() is True:
                    raise ValueError(f"Downsampling of the point cloud left "
                                     f"pixels without mark data {key} !")
            elif key not in ["n_x", "n_y", "n_z",
                             "s_x", "s_y", "s_z",
                             "scan_point_x", "scan_point_y", "scan_point_z"]:
                trg_grid[key] = src_grid[key]
            #     print(f"WARNING:: src_grid[{key}] is mapped as is on trg_grid[{key}] !")
            #     print(f"final np.shape(trg_grid[{key}]) {np.shape(trg_grid[key])}")
            else:
                print(f"WARNING:: src_grid[{key}] is not yet mapped on trg_grid[{key}] !")
            trg_grid["n_x"] = trg_nxy[0]
            trg_grid["n_y"] = trg_nxy[1]
            trg_grid["s_x"] = trg_sxy
            trg_grid["s_y"] = trg_sxy
            trg_grid["scan_point_x"] = trg_xy[0]
            trg_grid["scan_point_y"] = trg_xy[1]
            # TODO::need to update scan_point_{dim}
        return trg_grid
    else:
        raise ValueError(f"The 3D discretization is currently not implemented because "
                         f"we do not know of any large enough dataset the test it !")
