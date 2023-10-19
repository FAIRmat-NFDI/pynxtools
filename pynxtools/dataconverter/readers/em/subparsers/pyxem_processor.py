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
"""Process standardized orientation map using pyxem from normalized orientation data."""

import os
from typing import Dict, Any, List

import numpy as np
import h5py

# import imageio.v3 as iio
from PIL import Image as pil

import diffsims
import orix
from diffpy.structure import Lattice, Structure
from orix import plot
from orix.crystal_map import create_coordinate_arrays, CrystalMap, PhaseList
from orix.quaternion import Rotation
from orix.vector import Vector3d

import matplotlib.pyplot as plt

from pynxtools.dataconverter.readers.em.utils.hfive_web_constants \
    import HFIVE_WEB_MAXIMUM_RGB


class PyxemProcessor:
    def __init__(self, entry_id: int):
        self.entry_id = entry_id
        self.xmap = None
        pass

    def process_roi_overview(inp: dict, template: dict) -> dict:
        pass

    def process_roi_xmap(inp: dict) -> dict:
        """Process standardized IPF orientation map using pyxem from normalized orientation data."""
        # for NeXus would like to create a default
        if np.max(inp["n_x"], inp["n_y"]) < HFIVE_WEB_MAXIMUM_RGB:
            # can use the map discretization as is
            coordinates, _ = create_coordinate_arrays(
                (inp["n_x"], inp["n_y"]), (inp["s_x"], inp["s_y"]))
            xaxis = coordinates["x"]
            yaxis = coordinates["y"]
            del coordinates
        # else:
            # need to regrid to downsample too large maps
            # TODO::implement 1NN-based downsampling approach
            #       build grid
            #       tree-based 1NN
            #       proceed as usual

        pyxem_phase_identifier = inp["phase_identifier"] \
            - (np.min(inp["phase_identifier"]) - (-1))  # pyxem, non-indexed has to be -1
        print(np.unique(pyxem_phase_identifier))

        self.xmap = CrystalMap(rotations=inp["rotation"],
                               x=self.xaxis, y=self.yaxis,
                               phase_id=pyxem_phase_identifier,
                               phase_list=PhaseList(space_groups=inp["space_group"],
                                                    structures=inp["phase"]),
                               prop={"bc": inp["band_contrast"]},
                               scan_unit=inp["s_unit"])
        print(self.xmap)

    def process_roi_phases(self, template: dict) -> dict:
        pass

    def process_roi_inverse_pole_figures(self, template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings."""
        # call process_roi_ipf_map
        # call process_roi_ipf_color_key
        return template

    def process_roi_ipf_map(self, identifier, template: dict) -> dict:
        """Parse and create inverse-pole-figure (IPF) mappings on their color models."""
        # +1 because for orix not_indexed -1 and "first" phase has ID 0 !
        return template

    def process_roi_ipf_color_key(self, identifier, template: dict) -> dict:
        """Parse color key renderings of inverse-pole-figure (IPF) mappings."""
        # +1 because for orix not_indexed -1 and "first" phase has ID 0 !
        return template
