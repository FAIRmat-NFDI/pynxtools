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
"""(Sub-)parser mapping concepts and content from EDAX/AMETEK *.oh5/*.h5 (OIM Analysis) files on NXem."""

import numpy as np
import h5py
from typing import Dict
from diffpy.structure import Lattice, Structure

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import EULER_SPACE_SYMMETRY, \
    read_strings_from_dataset, read_first_scalar, format_euler_parameterization
from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    ASSUME_PHASE_NAME_TO_SPACE_GROUP, HEXAGONAL_GRID, SQUARE_GRID, REGULAR_TILING, FLIGHT_PLAN


class HdfFiveEdaxOimAnalysisReader(HdfFiveBaseParser):
    """Read EDAX (O)H5"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        if self.is_hdf is True:
            self.init_support()
            self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["EDAX"]
        self.supported_version["schema_name"] = ["H5"]
        self.supported_version["schema_version"] \
            = ["OIM Analysis 8.6.0050 x64 [18 Oct 2021]", "OIM Analysis 8.5.1002 x64 [07-17-20]"]
        self.supported_version["writer_name"] = ["OIM Analysis"]
        self.supported_version["writer_version"] \
            = ["OIM Analysis 8.6.0050 x64 [18 Oct 2021]", "OIM Analysis 8.5.1002 x64 [07-17-20]"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as old EDAX"""
        self.supported = 0  # voting-based
        with h5py.File(self.file_path, "r") as h5r:
            req_fields = ["Manufacturer", "Version"]
            for req_field in req_fields:
                if f"/{req_field}" not in h5r:
                    self.supported = False
                    return

            self.version["tech_partner"] = read_strings_from_dataset(h5r["/Manufacturer"][()])
            # for 8.6.0050 but for 8.5.1002 it is a matrix, this is because how strings end up in HDF5 allowed for so much flexibility!
            if self.version["tech_partner"] in self.supported_version["tech_partner"]:
                self.supported += 1
            self.version["schema_version"] = read_strings_from_dataset(h5r["/Version"][()])
            if self.version["schema_version"] in self.supported_version["schema_version"]:
                self.supported += 1

            if self.supported == 2:
                self.version["schema_name"] = self.supported_version["schema_name"]
                self.version["writer_name"] = self.supported_version["writer_name"]
                self.version["writer_version"] = self.supported_version["writer_version"]
                self.supported = True
            else:
                self.supported = False

    def parse_and_normalize(self):
        """Read and normalize away EDAX-specific formatting with an equivalent in NXem."""
        with h5py.File(f"{self.file_path}", "r") as h5r:
            cache_id = 1
            grp_names = list(h5r["/"])
            for grp_name in grp_names:
                if grp_name not in ["Version", "Manufacturer"]:
                    self.prfx = f"/{grp_name}"
                    ckey = self.init_named_cache(f"ebsd{cache_id}")
                    self.parse_and_normalize_group_ebsd_header(h5r, ckey)
                    self.parse_and_normalize_group_ebsd_phases(h5r, ckey)
                    self.parse_and_normalize_group_ebsd_data(h5r, ckey)
                    # add more information to pass to hfive parser
                    cache_id += 1

    def parse_and_normalize_group_ebsd_header(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Header"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        n_pts = 0
        req_fields = ["Grid Type", "Step X", "Step Y", "nColumns", "nRows"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        self.tmp[ckey]["dimensionality"] = 2
        grid_type = read_strings_from_dataset(fp[f"{grp_name}/Grid Type"][()])
        if grid_type == "HexGrid":
            self.tmp[ckey]["grid_type"] = HEXAGONAL_GRID
        elif grid_type == "SqrGrid":
            self.tmp[ckey]["grid_type"] = SQUARE_GRID
        else:
            raise ValueError(f"Unable to parse {grp_name}/Grid Type !")
        # the next two lines encode the typical assumption that is not reported in tech partner file!
        self.tmp[ckey]["tiling"] = REGULAR_TILING
        self.tmp[ckey]["flight_plan"] = FLIGHT_PLAN

        self.tmp[ckey]["s_x"] = read_first_scalar(fp[f"{grp_name}/Step X"])
        self.tmp[ckey]["s_unit"] = "um"  # "µm"  # TODO::always micron?
        self.tmp[ckey]["n_x"] = read_first_scalar(fp[f"{grp_name}/nColumns"])
        self.tmp[ckey]["s_y"] = read_first_scalar(fp[f"{grp_name}/Step Y"])
        self.tmp[ckey]["n_y"] = read_first_scalar(fp[f"{grp_name}/nRows"])
        # TODO::different version store the same concept with the same path name with different shape
        # the read_first_scalar is not an optimal solution, in the future all reads from
        # HDF5 should check for the shape instead
        # TODO::check that all data are consistent

    def parse_and_normalize_group_ebsd_phases(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Header/Phase"
        # Phases, contains a subgroup for each phase where the name
        # of each subgroup is the index of the phase starting at 1.
        if f"{grp_name}" in fp:
            phase_ids = sorted(list(fp[f"{grp_name}"]), key=int)
            self.tmp[ckey]["phase"] = []
            self.tmp[ckey]["space_group"] = []
            self.tmp[ckey]["phases"] = {}
            for phase_id in phase_ids:
                if phase_id.isdigit() is True:
                    self.tmp[ckey]["phases"][int(phase_id)] = {}
                    sub_grp_name = f"{grp_name}/{phase_id}"
                    # Name
                    if f"{sub_grp_name}/MaterialName" in fp:
                        phase_name = read_strings_from_dataset(fp[f"{sub_grp_name}/MaterialName"][0])
                        self.tmp[ckey]["phases"][int(phase_id)]["phase_name"] = phase_name
                    else:
                        raise ValueError(f"Unable to parse {sub_grp_name}/MaterialName !")

                    # Reference not available only Info but this can be empty
                    self.tmp[ckey]["phases"][int(phase_id)]["reference"] = "n/a"

                    req_fields = ["a", "b", "c", "alpha", "beta", "gamma"]
                    for req_field in req_fields:
                        if f"{sub_grp_name}/Lattice Constant {req_field}" not in fp:
                            raise ValueError(f"Unable to parse ../Lattice Constant {req_field} !")
                    a_b_c = [fp[f"{sub_grp_name}/Lattice Constant a"][()],
                             fp[f"{sub_grp_name}/Lattice Constant b"][()],
                             fp[f"{sub_grp_name}/Lattice Constant c"][()]]
                    angles = [fp[f"{sub_grp_name}/Lattice Constant alpha"][()],
                              fp[f"{sub_grp_name}/Lattice Constant beta"][()],
                              fp[f"{sub_grp_name}/Lattice Constant gamma"][()]]
                    # TODO::available examples support reporting in angstroem and degree
                    self.tmp[ckey]["phases"][int(phase_id)]["a_b_c"] \
                        = np.asarray(a_b_c, np.float32) * 0.1
                    self.tmp[ckey]["phases"][int(phase_id)]["alpha_beta_gamma"] \
                        = np.asarray(angles, np.float32)

                    # Space Group not stored, only laue group, point group and symmetry
                    # https://doi.org/10.1107/S1600576718012724 is a relevant read here
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
                            Structure(title=phase_name,
                                      atoms=None,
                                      lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                                      angles[0], angles[1], angles[2])))
                    else:
                        self.tmp[ckey]["phase"] \
                            = [Structure(title=phase_name,
                                         atoms=None,
                                         lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                                         angles[0], angles[1], angles[2]))]
        else:
            raise ValueError(f"Unable to parse {grp_name} !")

    def parse_and_normalize_group_ebsd_data(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Data"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        req_fields = ["CI", "Phase", "Phi1", "Phi", "Phi2", "X Position", "Y Position"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        n_pts = self.tmp[ckey]["n_x"] * self.tmp[ckey]["n_y"]
        self.tmp[ckey]["euler"] = np.zeros((n_pts, 3), np.float32)
        # TODO::available examples support that rumour that in EDAX file sometimes values
        # of Euler angle triplets are larger than mathematically possible
        # unfortunately there is no confirmation from EDAX what is the reported unit and
        # normalization for each software version, TODO::here rad is assumed but then values
        # as large as 12.... should not be possible
        # TODO::there has to be a mechanism which treats these dirty scan points!
        self.tmp[ckey]["euler"][:, 0] = np.asarray(fp[f"{grp_name}/Phi1"][:], np.float32)
        self.tmp[ckey]["euler"][:, 1] = np.asarray(fp[f"{grp_name}/Phi"][:], np.float32)
        self.tmp[ckey]["euler"][:, 2] = np.asarray(fp[f"{grp_name}/Phi2"][:], np.float32)
        # TODO::seems to be the situation in the example but there is no documentation
        self.tmp[ckey]["euler"] = format_euler_parameterization(self.tmp[ckey]["euler"])

        # given no official EDAX OimAnalysis spec we cannot define for sure if
        # phase_id == 0 means just all was indexed with the first/zeroth phase or nothing
        # was indexed, here we assume it means all indexed with first phase
        # and we assume EDAX uses -1 for notIndexed, this assumption is also
        # substantiated by the situation in the hfive_apex parser
        if np.all(fp[f"{grp_name}/Phase"][:] == 0):
            self.tmp[ckey]["phase_id"] = np.zeros(n_pts, np.int32) + 1
        else:
            self.tmp[ckey]["phase_id"] = np.asarray(fp[f"{grp_name}/Phase"][:], np.int32)
        # TODO::mark scan points as dirty
        # the line below shows an example how this could be achieved
        # is_dirty = np.zeros((n_pts,), bool)
        # for column_id in [0, 1, 2]:
        #    is_dirty = is_dirty & np.abs(self.tmp[ckey]["euler"][:, column_id]) > EULER_SPACE_SYMMETRY
        # print(f"Found {np.sum(is_dirty)} scan points which are marked now as dirty!")
        # self.tmp[ckey]["phase_id"][is_dirty] = 0

        # promoting int8 to int32 no problem
        self.tmp[ckey]["ci"] = np.asarray(fp[f"{grp_name}/CI"][:], np.float32)
        # normalize pixel coordinates to physical positions even though the origin can still dangle somewhere
        # expected is order on x is first all possible x values while y == 0
        # followed by as many copies of this linear sequence for each y increment
        # tricky situation is that for one version pixel coordinates while in another case
        # calibrated e.g. micron coordinates are reported that is in the first case px needs
        # multiplication with step size in the other one must not multiple with step size
        # as the step size has already been accounted for by the tech partner when writing!
        if self.version["schema_version"] in ["OIM Analysis 8.5.1002 x64 [07-17-20]"]:
            print(f"{self.version['schema_version']}, tech partner accounted for calibration")
            if self.tmp[ckey]["grid_type"] != SQUARE_GRID:
                print(f"WARNING: Check carefully correct interpretation of scan_point coords!")
            self.tmp[ckey]["scan_point_x"] \
                = np.asarray(fp[f"{grp_name}/X Position"][:], np.float32)
            self.tmp[ckey]["scan_point_y"] \
                = np.asarray(fp[f"{grp_name}/Y Position"][:], np.float32)
        else:
            print(f"{self.version['schema_version']}, parser has to do the calibration")
            if self.tmp[ckey]["grid_type"] != SQUARE_GRID:
                print(f"WARNING: Check carefully correct interpretation of scan_point coords!")
            self.tmp[ckey]["scan_point_x"] = np.asarray(
                fp[f"{grp_name}/X Position"][:] * self.tmp[ckey]["s_x"], np.float32)
            self.tmp[ckey]["scan_point_y"] = np.asarray(
                fp[f"{grp_name}/Y Position"][:] * self.tmp[ckey]["s_y"], np.float32)
        # despite differences in reported calibrations the scan_point_{dim} arrays are
        # already provided by the tech partner as tile and repeat coordinates
