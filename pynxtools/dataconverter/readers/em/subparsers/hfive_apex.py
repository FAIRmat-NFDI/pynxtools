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
"""(Sub-)parser mapping concepts and content from EDAX/AMETEK *.edaxh5 (APEX) files on NXem."""

import numpy as np
import h5py
from itertools import groupby
# import imageio.v3 as iio
from PIL import Image as pil

import diffsims
import orix
from diffpy.structure import Lattice, Structure
from orix import plot
from orix.crystal_map import create_coordinate_arrays, CrystalMap, PhaseList
from orix.quaternion import Rotation, Orientation
from orix.vector import Vector3d

import matplotlib.pyplot as plt

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import \
    read_strings_from_dataset
from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    ASSUME_PHASE_NAME_TO_SPACE_GROUP, HEXAGONAL_GRID, SQUARE_GRID, REGULAR_TILING, FLIGHT_PLAN
from pynxtools.dataconverter.readers.em.utils.get_scan_points import \
    get_scan_point_coords


class HdfFiveEdaxApexReader(HdfFiveBaseParser):
    """Read APEX edaxh5"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp = {}
        self.supported_version = {}
        self.version = {}
        self.init_support()
        self.supported = False
        self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["EDAX, LLC"]
        self.supported_version["schema_name"] = ["EDAXH5"]
        self.supported_version["schema_version"] = ["2.5.1001.0001"]
        self.supported_version["writer_name"] = ["APEX"]
        self.supported_version["writer_version"] = ["2.5.1001.0001"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as supported H5OINA"""
        self.supported = 0  # voting-based
        with h5py.File(self.file_path, "r") as h5r:
            # parse Company and PRODUCT_VERSION attribute values from the first group below / but these are not scalar but single value lists
            # so much about interoperability
            # but hehe for the APEX example from Sebastian and Sabine there is again no Company but PRODUCT_VERSION, 2 files, 2 "formats"
            grp_names = list(h5r["/"])
            if len(grp_names) == 1:
                if read_strings_from_dataset(h5r[grp_names[0]].attrs["Company"][0]) in self.supported_version["tech_partner"]:
                    self.supported += 1
                if read_strings_from_dataset(h5r[grp_names[0]].attrs["PRODUCT_VERSION"][0]) in self.supported_version["schema_version"]:
                    self.supported += 1
            if self.supported == 2:
                self.version = self.supported_version.copy()
                self.supported = True
            else:
                self.supported = False

    def parse_and_normalize(self):
        """Read and normalize away EDAX/APEX-specific formatting with an equivalent in NXem."""
        with h5py.File(f"{self.file_path}", "r") as h5r:
            cache_id = 1
            grp_nms = list(h5r["/"])
            for grp_nm in grp_nms:
                sub_grp_nms = list(h5r[grp_nm])
                for sub_grp_nm in sub_grp_nms:
                    sub_sub_grp_nms = list(h5r[f"/{grp_nm}/{sub_grp_nm}"])
                    for sub_sub_grp_nm in sub_sub_grp_nms:
                        if sub_sub_grp_nm.startswith("Area"):
                            area_grp_nms = list(h5r[f"/{grp_nm}/{sub_grp_nm}/{sub_sub_grp_nm}"])
                            for area_grp_nm in area_grp_nms:
                                if area_grp_nm.startswith("OIM Map"):
                                    self.prfx = f"/{grp_nm}/{sub_grp_nm}/{sub_sub_grp_nm}/{area_grp_nm}"
                                    print(f"Parsing {self.prfx}")
                                    ckey = self.init_named_cache(f"ebsd{cache_id}")
                                    self.parse_and_normalize_group_ebsd_header(h5r, ckey)
                                    self.parse_and_normalize_group_ebsd_phases(h5r, ckey)
                                    self.parse_and_normalize_group_ebsd_data(h5r, ckey)
                                    cache_id += 1

    def parse_and_normalize_group_ebsd_header(self, fp, ckey: str):
        # no official documentation yet from EDAX/APEX, deeply nested, chunking, virtual ds
        if f"{self.prfx}/EBSD/ANG/DATA/DATA" not in fp:
            raise ValueError(f"Unable to parse {self.prfx}/EBSD/ANG/DATA/DATA !")

        # for a regular tiling of R^2 with perfect hexagons
        n_pts = 0
        # their vertical center of mass distance is smaller than the horizontal
        # center of mass distance (x cols, y rows)
        req_fields = ["Grid Type",
                      "Step X", "Step Y",
                      "Number Of Rows", "Number Of Columns"]
        for req_field in req_fields:
            if f"{self.prfx}/Sample/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {self.prfx}/Sample/{req_field} !")

        self.tmp[ckey]["dimensionality"] = 2
        grid_type = read_strings_from_dataset(fp[f"{self.prfx}/Sample/Grid Type"][()])
        if grid_type == "HexGrid":
            self.tmp[ckey]["grid_type"] = HEXAGONAL_GRID
        elif grid_type == "SqrGrid":
            self.tmp[ckey]["grid_type"] = SQUARE_GRID
        else:
            raise ValueError(f"Unable to parse {self.prfx}/Sample/Grid Type !")
        # the next two lines encode the typical assumption that is not reported in tech partner file!
        self.tmp[ckey]["tiling"] = REGULAR_TILING
        self.tmp[ckey]["flight_plan"] = FLIGHT_PLAN
        self.tmp[ckey]["s_x"] = fp[f"{self.prfx}/Sample/Step X"][0]
        self.tmp[ckey]["s_unit"] = "um"  # "µm"  # TODO::always micron?
        self.tmp[ckey]["n_x"] = fp[f"{self.prfx}/Sample/Number Of Columns"][0]
        self.tmp[ckey]["s_y"] = fp[f"{self.prfx}/Sample/Step Y"][0]
        self.tmp[ckey]["n_y"] = fp[f"{self.prfx}/Sample/Number Of Rows"][0]
        # TODO::check that all data are consistent

    def parse_and_normalize_group_ebsd_phases(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/ANG/HEADER/Phase"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        # Phases, contains a subgroup for each phase where the name
        # of each subgroup is the index of the phase starting at 1.
        phase_ids = sorted(list(fp[f"{grp_name}"]), key=int)
        self.tmp[ckey]["phase"] = []
        self.tmp[ckey]["space_group"] = []
        self.tmp[ckey]["phases"] = {}
        for phase_id in phase_ids:
            if phase_id.isdigit() is True:
                self.tmp[ckey]["phases"][int(phase_id)] = {}
                sub_grp_name = f"{grp_name}/{phase_id}"
                # Name
                if f"{sub_grp_name}/Material Name" in fp:
                    phase_name = read_strings_from_dataset(fp[f"{sub_grp_name}/Material Name"][0])
                    self.tmp[ckey]["phases"][int(phase_id)]["phase_name"] = phase_name
                else:
                    raise ValueError(f"Unable to parse {sub_grp_name}/Material Name !")

                # Reference not available only Info but this can be empty
                self.tmp[ckey]["phases"][int(phase_id)]["reference"] = "n/a"

                req_fields = ["A", "B", "C", "Alpha", "Beta", "Gamma"]
                for req_field in req_fields:
                    if f"{sub_grp_name}/Lattice Constant {req_field}" not in fp:
                        raise ValueError(f"Unable to parse ../Lattice Constant {req_field} !")
                a_b_c = [fp[f"{sub_grp_name}/Lattice Constant A"][0],
                            fp[f"{sub_grp_name}/Lattice Constant B"][0],
                            fp[f"{sub_grp_name}/Lattice Constant C"][0]]
                angles = [fp[f"{sub_grp_name}/Lattice Constant Alpha"][0],
                            fp[f"{sub_grp_name}/Lattice Constant Beta"][0],
                            fp[f"{sub_grp_name}/Lattice Constant Gamma"][0]]
                # TODO::available examples support reporting in angstroem and degree
                self.tmp[ckey]["phases"][int(phase_id)]["a_b_c"] \
                    = np.asarray(a_b_c, np.float32) * 0.1
                self.tmp[ckey]["phases"][int(phase_id)]["alpha_beta_gamma"] \
                    = np.asarray(angles, np.float32)

                # Space Group not stored, only laue group, point group and symmetry
                # problematic because mapping is not bijective!
                # if you know the space group we know laue and point group and symmetry
                # but the opposite direction leaves room for ambiguities
                space_group = None
                if phase_name in ASSUME_PHASE_NAME_TO_SPACE_GROUP.keys():
                    space_group = ASSUME_PHASE_NAME_TO_SPACE_GROUP[phase_name]
                self.tmp[ckey]["phases"][int(phase_id)]["space_group"] = space_group

                if len(self.tmp[ckey]["space_group"]) > 0:
                    self.tmp[ckey]["space_group"].append(space_group)
                else:
                    self.tmp[ckey]["space_group"] = [space_group]

                if len(self.tmp[ckey]["phase"]) > 0:
                    self.tmp[ckey]["phase"].append(
                        Structure(title=phase_name, atoms=None,
                                    lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                    angles[0], angles[1], angles[2])))
                else:
                    self.tmp[ckey]["phase"] \
                        = [Structure(title=phase_name, atoms=None,
                                        lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                        angles[0], angles[1], angles[2]))]

    def parse_and_normalize_group_ebsd_data(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/ANG/DATA/DATA"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        n_pts = self.tmp[ckey]["n_x"] * self.tmp[ckey]["n_y"]
        if np.shape(fp[f"{grp_name}"]) != (n_pts,) and n_pts > 0:
            raise ValueError(f"Unexpected shape of {grp_name} !")

        dat = fp[f"{grp_name}"]
        self.tmp[ckey]["euler"] = np.zeros((n_pts, 3), np.float32)
        self.tmp[ckey]["ci"] = np.zeros((n_pts,), np.float32)
        self.tmp[ckey]["phase_id"] = np.zeros((n_pts,), np.int32)

        for i in np.arange(0, n_pts):
            # check shape of internal virtual chunked number array
            oris = Orientation.from_matrix([np.reshape(dat[i][0], (3, 3))])
            self.tmp[ckey]["euler"][i, :] = oris.to_euler(degrees=False)
            self.tmp[ckey]["ci"][i] = dat[i][2]
            self.tmp[ckey]["phase_id"][i] = dat[i][3] + 1  # APEX seems to define
            # notIndexed as -1 and the first valid phase id 0
        if np.isnan(self.tmp[ckey]["euler"]).any():
            raise ValueError(f"Conversion of om2eu unexpectedly resulted in NaN !")
        # TODO::convert orientation matrix to Euler angles via om_eu but what are conventions !
        # orix based transformation ends up in positive half space and with degrees=False
        # as radiants but the from_matrix command above might miss one rotation

        # compute explicit hexagon grid cells center of mass pixel positions
        # TODO::currently assuming s_x and s_y are already the correct center of mass
        # distances for hexagonal or square tiling of R^2
        # self.tmp[ckey]["grid_type"] in ["HexGrid", "SqrGrid"]:
        # if just SQUARE_GRID there is no point to explicitly compute the scan_point
        # coordinates here (for every subparser) especially not when the respective
        # quantity from the tech partner is just a pixel index i.e. zeroth, first px ...
        # however, ideally the tech partners would use the scan_point fields to report
        # calibrated absolute scan point positions in the local reference frame of the
        # sample surface in which case these could indeed not just scaled positions
        # having the correct x and y spacing but eventually even the absolute coordinate
        # where the scan was performed on the sample surface whereby one could conclude
        # more precisely where the scanned area was located, in practice though this precision
        # is usually not needed because scientists assume that the ROI is representative for
        # the material which they typically never scan (time, interest, costs, instrument
        # availability) completely!
        if self.tmp[ckey]["grid_type"] != SQUARE_GRID:
            print(f"WARNING: {self.tmp[ckey]['grid_type']}: check carefully the " \
                  f"correct interpretation of scan_point coords!")
        # the case of EDAX APEX shows the key problem with implicit assumptions
        # edaxh5 file not necessarily store the scan_point_{dim} positions
        # therefore the following code is deprecated as the axes coordinates anyway
        # have to be recomputed based on whether results are rediscretized on a coarser
        # grid or not !
        # mind also that the code below anyway would give only the NeXus dim axis but
        # not the array of pairs of x, y coordinates for each scan point
        # TODO::also keep in mind that the order in which the scan points are stored
        # i.e. which index on self.tmp[ckey]["euler"] belongs to which scan point
        # depends not only on the scan grid but also the flight plan i.e. how the grid
        # gets visited
        # only because of the fact that in most cases people seem to accept that
        # scanning snake like first a line along +x and then +y meandering over the
        # scan area from the top left corner to the bottom right corner is JUST an
        # assumption for a random or dynamically adaptive scan strategy the scan positions
        # have to be reported anyway, TODO::tech partners should be convinced to export
        # scaled and calibrated scan positions as they are not necessarily redundant information
        # that can be stripped to improve performance of their commercial product, I mean
        # we talk typically <5k pattern per second demanding to store 5k * 2 * 8B, indeed
        # this is the non-harmonized content one is facing in the field of EBSD despite
        # almost two decades of commercialization of the technique now
        get_scan_point_coords(self.tmp[ckey])
