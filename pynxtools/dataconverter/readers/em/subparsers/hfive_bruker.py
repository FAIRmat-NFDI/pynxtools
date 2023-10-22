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

import os
from typing import Dict, Any, List
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
from orix.quaternion import Rotation
from orix.vector import Vector3d

import matplotlib.pyplot as plt

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

BRUKER_MAP_SPACEGROUP = {"F m#ovl3m": 225}


class HdfFiveBrukerEspritReader(HdfFiveBaseParser):
    """Read Bruker Esprit H5"""
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
        self.supported_version["tech_partner"] = ["Bruker Nano"]
        self.supported_version["schema_name"] = ["H5"]
        self.supported_version["schema_version"] = ["Esprit 2.X"]
        self.supported_version["writer_name"] = []
        self.supported_version["writer_version"] = ["Esprit 2.X"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as supported Bruker H5"""
        self.supported = True  # try to falsify
        with h5py.File(self.file_path, "r") as h5r:
            if "/Manufacturer" in h5r:
                self.version["tech_partner"] \
                    = read_strings_from_dataset(h5r["/Manufacturer"][()])
                if self.version["tech_partner"] not in self.supported_version["tech_partner"]:
                    self.supported = False
            else:
                self.supported = False
            if "/Version" in h5r:
                self.version["schema_version"] \
                    = read_strings_from_dataset(h5r["/Version"][()])
                if self.version["schema_version"] not in self.supported_version["schema_version"]:
                    self.supported = False
            else:
                self.supported = False

        if self.supported is True:
            self.version["schema_name"] = self.supported_version["schema_name"]
            self.version["writer_name"] = self.supported_version["writer_name"]
            self.version["writer_version"] = self.supported_version["writer_version"]

    def parse_and_normalize(self):
        """Read and normalize away Bruker-specific formatting with an equivalent in NXem."""
        with h5py.File(f"{self.file_path}", "r") as h5r:
            cache_id = 0
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
        if f"{grp_name}/NCOLS" in fp:  # TODO::what is y and x depends on coordinate system
            self.tmp[ckey]["n_x"] = fp[f"{grp_name}/NCOLS"][()]
        else:
            raise ValueError(f"Unable to parse {grp_name}/NCOLS !")

        if f"{grp_name}/NROWS" in fp:
            self.tmp[ckey]["n_y"] = fp[f"{grp_name}/NROWS"][()]
        else:
            raise ValueError(f"Unable to parse {grp_name}/NROWS !")

        if f"{grp_name}/SEPixelSizeX" in fp:
            self.tmp[ckey]["s_x"] = fp[f"{grp_name}/SEPixelSizeX"][()]
            self.tmp[ckey]["s_unit"] = "µm"  # TODO::always micron?
        else:
            raise ValueError(f"Unable to parse {grp_name}/SEPixelSizeX !")

        if f"{grp_name}/SEPixelSizeY" in fp:
            self.tmp[ckey]["s_y"] = fp[f"{grp_name}/SEPixelSizeY"][()]
        else:
            raise ValueError(f"Unable to parse {grp_name}/SEPixelSizeY !")
        # TODO::check that all data in the self.oina are consistent

    def parse_and_normalize_group_ebsd_phases(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Header"
        # Phases, contains a subgroup for each phase where the name
        # of each subgroup is the index of the phase starting at 1.
        if f"{grp_name}/Phases" in fp:
            phase_ids = sorted(list(fp[f"{grp_name}/Phases"]), key=int)
            self.tmp[ckey]["phase"] = []
            self.tmp[ckey]["space_group"] = []
            self.tmp[ckey]["phases"] = {}
            for phase_id in phase_ids:
                if phase_id.isdigit() is True:
                    self.tmp[ckey]["phases"][int(phase_id)] = {}
                    sub_grp_name = f"/{grp_name}/Phases/{phase_id}"
                    # Name
                    if f"{sub_grp_name}/Name" in fp:
                        phase_name = read_strings_from_dataset(fp[f"{sub_grp_name}/Name"][()])
                        self.tmp[ckey]["phases"][int(phase_id)]["phase_name"] = phase_name
                    else:
                        raise ValueError(f"Unable to parse {sub_grp_name}/Name !")

                    # Reference not available
                    self.tmp[ckey]["phases"][int(phase_id)]["reference"] = "n/a"

                    # LatticeConstants, a, b, c (angstrom) followed by alpha, beta and gamma angles in degree
                    if f"{sub_grp_name}/LatticeConstants" in fp:
                        values = np.asarray(fp[f"{sub_grp_name}/LatticeConstants"][:].flatten())
                        a_b_c = values[0:3]
                        angles = values[3:6]
                        self.tmp[ckey]["phases"][int(phase_id)]["a_b_c"] \
                            = a_b_c * 0.1
                        self.tmp[ckey]["phases"][int(phase_id)]["alpha_beta_gamma"] \
                            = angles
                    else:
                        raise ValueError(f"Unable to parse {sub_grp_name}/LatticeConstants !")

                    # Space Group, no, H5T_NATIVE_INT32, (1, 1), Space group index.
                    # The attribute Symbol contains the string representation, for example P m -3 m.
                    if f"{sub_grp_name}/SpaceGroup" in fp:
                        spc_grp  = read_strings_from_dataset(fp[f"{sub_grp_name}/SpaceGroup"][()])
                        if spc_grp in BRUKER_MAP_SPACEGROUP.keys():
                            space_group = BRUKER_MAP_SPACEGROUP[spc_grp]
                            self.tmp[ckey]["phases"][int(phase_id)]["space_group"] = space_group
                        else:
                            raise ValueError(f"Unable to decode improperly formatted space group {spc_grp} !")
                    else:
                        raise ValueError(f"Unable to parse {sub_grp_name}/SpaceGroup !")
                    # formatting is a nightmare F m#ovl3m for F m 3bar m...
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
        else:
            raise ValueError(f"Unable to parse {grp_name}/Phases !")

    def parse_and_normalize_group_ebsd_data(self, fp, ckey: str):
        # no official documentation yet from Bruker but seems inspired by H5EBSD
        grp_name = f"{self.prfx}/EBSD/Data"
        print(f"Parsing {grp_name}")
        # Euler, yes, H5T_NATIVE_FLOAT, (size, 3), Orientation of Crystal (CS2) to Sample-Surface (CS1).
        n_pts = 0
        if f"{grp_name}/phi1" in fp and f"{grp_name}/PHI" in fp and f"{grp_name}/phi2" in fp:
            n_pts = (np.shape(fp[f"{grp_name}/phi1"][:])[0],
                     np.shape(fp[f"{grp_name}/PHI"][:])[0],
                     np.shape(fp[f"{grp_name}/phi2"][:])[0])
            if all_equal(n_pts) is True and n_pts[0] > 0:
                self.tmp[ckey]["euler"] = np.zeros((n_pts[0], 3), np.float32)
                column_id = 0
                for angle in ["phi1", "PHI", "phi2"]:
                    self.tmp[ckey]["euler"][:, column_id] \
                        = np.asarray(fp[f"{grp_name}/{angle}"][:], np.float32)
                    column_id += 1
                is_degrees = False
                is_negative = False
                for column_id in [0, 1, 2]:
                    if np.max(np.abs(self.tmp[ckey]["euler"][:, column_id])) > 2. * np.pi:
                        is_degrees = True
                    if np.min(self.tmp[ckey]["euler"][:, column_id]) < 0.:
                        is_negative = True
                if is_degrees is True:
                    self.tmp[ckey]["euler"] = self.tmp[ckey]["euler"] / 180. * np.pi
                if is_negative is True:
                    symmetrize = [2. * np.pi, np.pi, 2. * np.pi]
                    # TODO::symmetry in Euler space really at PHI=180deg?
                    for column_id in [0, 1, 2]:
                        self.tmp[ckey]["euler"][:, column_id] \
                            = self.tmp[ckey]["euler"][:, column_id] + symmetrize[column_id]
                n_pts = n_pts[0]
            # inconsistency f32 in file although specification states float
                #Rotation.from_euler(euler=fp[f"{grp_name}/Euler"],
                 #                                 direction='lab2crystal',
                  #                                degrees=is_degrees)
        else:
            raise ValueError(f"Unable to parse {grp_name}/phi1, ../PHI, ../phi2 !")

        # index of phase, 0 if not indexed
        # # no normalization needed, also in NXem_ebsd the null model notIndexed is phase_identifier 0
        if f"{grp_name}/Phase" in fp:
            if np.shape(fp[f"{grp_name}/Phase"][:])[0] == n_pts:
                self.tmp[ckey]["phase_id"] = np.asarray(fp[f"{grp_name}/Phase"][:], np.int32)
            else:
                raise ValueError(f"{grp_name}/Phase has unexpected shape !")
        else:
            raise ValueError(f"Unable to parse {grp_name}/Phase !")

        # X
        if f"{grp_name}/X SAMPLE" in fp:
            if np.shape(fp[f"{grp_name}/X SAMPLE"][:])[0] == n_pts:
                self.tmp[ckey]["scan_point_x"] \
                    = np.asarray(fp[f"{grp_name}/X SAMPLE"][:], np.float32)
            else:
                raise ValueError(f"{grp_name}/X SAMPLE has unexpected shape !")
        else:
            raise ValueError(f"Unable to parse {grp_name}/X SAMPLE !")

        # Y
        if f"{grp_name}/Y SAMPLE" in fp:
            if np.shape(fp[f"{grp_name}/Y SAMPLE"][:])[0] == n_pts:
                self.tmp[ckey]["scan_point_y"] \
                    = np.asarray(fp[f"{grp_name}/Y SAMPLE"], np.float32)
            else:
                raise ValueError(f"{grp_name}/Y SAMPLE has unexpected shape !")
        else:
            raise ValueError(f"Unable to parse {grp_name}/Y SAMPLE !")

        # Band Contrast is not stored in Bruker but Radon Quality or MAD
        # but this is s.th. different as it is the mean angular deviation between
        # indexed with simulated and measured pattern
        if f"{grp_name}/MAD" in fp:
            if np.shape(fp[f"{grp_name}/MAD"][:])[0] == n_pts:
                self.tmp[ckey]["mad"] = np.asarray(fp[f"{grp_name}/MAD"][:], np.float32)
            else:
                raise ValueError(f"{grp_name}/MAD has unexpected shape !")
        else:
            raise ValueError(f"Unable to parse {grp_name}/MAD !")

