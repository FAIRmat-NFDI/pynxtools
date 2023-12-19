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
"""(Sub-)parser mapping concepts and content from Bruker *.h5 files on NXem."""

import numpy as np
import h5py
from typing import Dict
from diffpy.structure import Lattice, Structure

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import \
    EBSD_MAP_SPACEGROUP, read_strings_from_dataset, all_equal, format_euler_parameterization
from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    ASSUME_PHASE_NAME_TO_SPACE_GROUP, SQUARE_GRID, REGULAR_TILING, FLIGHT_PLAN  # HEXAGONAL_GRID
from pynxtools.dataconverter.readers.em.utils.get_scan_points import \
    get_scan_point_coords


class HdfFiveBrukerEspritReader(HdfFiveBaseParser):
    """Read Bruker Esprit H5"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp: Dict = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        if self.is_hdf is True:
            self.init_support()
            self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["Bruker Nano"]
        self.supported_version["schema_name"] = ["H5"]
        self.supported_version["schema_version"] = ["Esprit 2.X"]
        self.supported_version["writer_name"] = []
        self.supported_version["writer_version"] = ["Esprit 2.X"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as supported Bruker H5"""
        self.supported = 0  # voting-based
        with h5py.File(self.file_path, "r") as h5r:
            req_fields = ["Manufacturer", "Version"]
            for req_field in req_fields:
                if f"/{req_field}" not in h5r:
                    self.supported = False
                    return

            self.version["tech_partner"] = read_strings_from_dataset(h5r["/Manufacturer"][()])
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
        """Read and normalize away Bruker-specific formatting with an equivalent in NXem."""
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

        self.tmp[ckey]["dimensionality"] = 2  # TODO::QUBE can also yield 3D datasets
        if read_strings_from_dataset(fp[f"{grp_name}/Grid Type"][()]) == "isometric":
            self.tmp[ckey]["grid_type"] = SQUARE_GRID
        else:
            raise ValueError(f"Unable to parse {grp_name}/Grid Type !")
        # the next two lines encode the typical assumption that is not reported in tech partner file!
        self.tmp[ckey]["tiling"] = REGULAR_TILING
        self.tmp[ckey]["flight_plan"] = FLIGHT_PLAN

        req_fields = ["NCOLS", "NROWS", "XSTEP", "YSTEP"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        self.tmp[ckey]["n_x"] = fp[f"{grp_name}/NCOLS"][()]
        self.tmp[ckey]["n_y"] = fp[f"{grp_name}/NROWS"][()]
        self.tmp[ckey]["s_x"] = fp[f"{grp_name}/XSTEP"][()]
        self.tmp[ckey]["s_unit"] = "um"  # "µm"  # TODO::always micron?
        self.tmp[ckey]["s_y"] = fp[f"{grp_name}/YSTEP"][()]
        # TODO::check that all data are consistent
        # TODO::what is y and x depends on coordinate system

    def parse_and_normalize_group_ebsd_phases(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Header/Phases"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable parse {grp_name} !")

        # Phases, contains a subgroup for each phase where the name
        # of each subgroup is the index of the phase starting at 1.
        phase_ids = sorted(list(fp[f"{grp_name}"]), key=int)
        self.tmp[ckey]["phase"] = []
        self.tmp[ckey]["space_group"] = []
        self.tmp[ckey]["phases"] = {}
        for phase_id in phase_ids:
            if phase_id.isdigit() is True:
                self.tmp[ckey]["phases"][int(phase_id)] = {}
                sub_grp_name = f"/{grp_name}/{phase_id}"
                req_fields = ["Name", "LatticeConstants", "SpaceGroup"]
                for req_field in req_fields:
                    if f"{sub_grp_name}/{req_field}" not in fp:
                        raise ValueError(f"Unable to parse {sub_grp_name}/{req_field} !")
                # Name
                phase_name = read_strings_from_dataset(fp[f"{sub_grp_name}/Name"][()])
                self.tmp[ckey]["phases"][int(phase_id)]["phase_name"] = phase_name

                # Reference not available
                self.tmp[ckey]["phases"][int(phase_id)]["reference"] = "n/a"

                # LatticeConstants, a, b, c (angstrom) followed by alpha, beta and gamma angles in degree
                values = np.asarray(fp[f"{sub_grp_name}/LatticeConstants"][:].flatten())
                a_b_c = values[0:3]
                angles = values[3:6]
                self.tmp[ckey]["phases"][int(phase_id)]["a_b_c"] = a_b_c * 0.1
                # TODO::all examples indicate reporting in angstroem
                self.tmp[ckey]["phases"][int(phase_id)]["alpha_beta_gamma"] = angles

                # Space Group, no, H5T_NATIVE_INT32, (1, 1), Space group index.
                # The attribute Symbol contains the string representation, for example P m -3 m.
                spc_grp = read_strings_from_dataset(fp[f"{sub_grp_name}/SpaceGroup"][()])
                if spc_grp in EBSD_MAP_SPACEGROUP.keys():
                    space_group = EBSD_MAP_SPACEGROUP[spc_grp]
                    self.tmp[ckey]["phases"][int(phase_id)]["space_group"] = space_group
                elif phase_name in ASSUME_PHASE_NAME_TO_SPACE_GROUP.keys():
                    space_group = ASSUME_PHASE_NAME_TO_SPACE_GROUP[phase_name]
                    self.tmp[ckey]["phases"][int(phase_id)]["space_group"] = space_group
                else:
                    raise ValueError(f"Unable to decode improperly formatted space group {spc_grp} !")
                # formatting is a nightmare F m#ovl3m for F m 3bar m...
                # TODO::in some case instead a group IT (likely International Tables of Crystallography)
                # was there so parse this instead of the above used mapping table
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
                    self.tmp[ckey]["phase"] = [
                        Structure(title=phase_name, atoms=None,
                                  lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                                  angles[0], angles[1], angles[2]))]

    def parse_and_normalize_group_ebsd_data(self, fp, ckey: str):
        # no official documentation yet from Bruker but seems inspired by H5EBSD
        grp_name = f"{self.prfx}/EBSD/Data"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        req_fields = ["phi1", "PHI", "phi2", "Phase", "MAD"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        # Euler
        n_pts_probe = (np.shape(fp[f"{grp_name}/phi1"][:])[0],
                       np.shape(fp[f"{grp_name}/PHI"][:])[0],
                       np.shape(fp[f"{grp_name}/phi2"][:])[0])
        n_pts = None
        if all_equal(n_pts_probe) is True and n_pts_probe[0] == (self.tmp[ckey]["n_x"] * self.tmp[ckey]["n_y"]):
            self.tmp[ckey]["euler"] = np.zeros((n_pts_probe[0], 3), np.float32)
            column_id = 0
            for angle in ["phi1", "PHI", "phi2"]:
                # TODO::available examples support that Bruker reports Euler triplets in degree
                self.tmp[ckey]["euler"][:, column_id] \
                    = np.asarray(fp[f"{grp_name}/{angle}"][:], np.float32) / 180. * np.pi
                column_id += 1
            self.tmp[ckey]["euler"] = format_euler_parameterization(self.tmp[ckey]["euler"])
            n_pts = n_pts_probe[0]

        # index of phase, 0 if not indexed
        # no normalization needed, also in NXem_ebsd the null model notIndexed is phase_identifier 0
        if np.shape(fp[f"{grp_name}/Phase"][:])[0] == n_pts:
            self.tmp[ckey]["phase_id"] = np.asarray(fp[f"{grp_name}/Phase"][:], np.int32)
        else:
            raise ValueError(f"{grp_name}/Phase has unexpected shape !")

        # X and Y
        # there is X SAMPLE and Y SAMPLE but these are not defined somewhere instead
        # here adding x and y assuming that we scan first lines along positive x and then
        # moving downwards along +y
        # TODO::calculation below x/y only valid if self.tmp[ckey]["grid_type"] == SQUARE_GRID
        if self.tmp[ckey]["grid_type"] != SQUARE_GRID:
            print(f"WARNING: Check carefully correct interpretation of scan_point coords!")
        # self.tmp[ckey]["scan_point_x"] \
        #     = np.asarray(np.tile(np.linspace(0.,
        #                                      self.tmp[ckey]["n_x"] - 1.,
        #                                      num=self.tmp[ckey]["n_x"],
        #                                      endpoint=True) * self.tmp[ckey]["s_x"],
        #                                      self.tmp[ckey]["n_y"]), np.float32)
        # self.tmp[ckey]["scan_point_y"] \
        #     = np.asarray(np.repeat(np.linspace(0.,
        #                                        self.tmp[ckey]["n_y"] - 1.,
        #                                        num=self.tmp[ckey]["n_y"],
        #                                        endpoint=True) * self.tmp[ckey]["s_y"],
        #                                        self.tmp[ckey]["n_x"]), np.float32)
        get_scan_point_coords(self.tmp[ckey])

        # Band Contrast is not stored in Bruker but Radon Quality or MAD
        # but this is s.th. different as it is the mean angular deviation between
        # indexed with simulated and measured pattern
        if np.shape(fp[f"{grp_name}/MAD"][:])[0] == n_pts:
            self.tmp[ckey]["mad"] = np.asarray(fp[f"{grp_name}/MAD"][:], np.float32)
        else:
            raise ValueError(f"{grp_name}/MAD has unexpected shape !")
