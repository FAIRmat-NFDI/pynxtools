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
"""(Sub-)parser mapping concepts and content from Oxford Instruments *.h5oina files on NXem."""

import numpy as np
import h5py
from typing import Dict
from diffpy.structure import Lattice, Structure

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import \
    read_strings_from_dataset, format_euler_parameterization
from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    SQUARE_GRID, REGULAR_TILING, FLIGHT_PLAN  # HEXAGONAL_GRID


class HdfFiveOxfordReader(HdfFiveBaseParser):
    """Overwrite constructor of hfive_base reader"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        # this specialized reader implements reading capabilities for the following formats
        self.prfx = None  # path handling
        self.tmp = {}  # local cache in which normalized data are stored
        # that are once fully populated passed to the base class process_roi* functions
        # which perform plotting and data processing functionalities
        # this design effectively avoids that different specialized hfive readers need to
        # duplicate the code of the base hfive parser for generating NeXus default plots
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        if self.is_hdf is True:
            self.init_support()
            self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["Oxford Instruments"]
        self.supported_version["schema_name"] = ["H5OINA"]
        self.supported_version["schema_version"] = ["2.0", "3.0", "4.0", "5.0"]
        self.supported_version["writer_name"] = ["AZTec"]
        self.supported_version["writer_version"] \
            = ["4.4.7495.1", "5.0.7643.1", "5.1.7829.1", "6.0.8014.1", "6.0.8196.1"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as supported H5OINA"""
        self.supported = 0  # voting-based
        with h5py.File(self.file_path, "r") as h5r:
            req_fields = ["Manufacturer", "Software Version", "Format Version"]
            for req_field in req_fields:
                if f"/{req_field}" not in h5r:
                    self.supported = False
                    return

            self.version["tech_partner"] = read_strings_from_dataset(h5r["/Manufacturer"][()])
            if self.version["tech_partner"] in self.supported_version["tech_partner"]:
                # print(f"{self.version['tech_partner']} is not {self.version['tech_partner']} !")
                self.supported += 1
            # only because we know (thanks to Philippe Pinard who wrote the H5OINA writer) that different
            # writer versions should implement the different HDF version correctly we can lift the
            # constraint on the writer_version for which we had examples available
            self.version["writer_version"] = read_strings_from_dataset(h5r["/Software Version"][()])
            if self.version["writer_version"] in self.supported_version["writer_version"]:
                self.supported += 1
            self.version["schema_version"] = read_strings_from_dataset(h5r["/Format Version"][()])
            if self.version["schema_version"] in self.supported_version["schema_version"]:
                self.supported += 1

            if self.supported == 3:
                self.version["schema_name"] = self.supported_version["schema_name"]
                self.version["writer_name"] = self.supported_version["writer_name"]
                self.supported = True
            else:
                self.supported = False

    def parse_and_normalize(self):
        """Read and normalize away Oxford-specific formatting with an equivalent in NXem."""
        with h5py.File(f"{self.file_path}", "r") as h5r:
            cache_id = 1
            slice_ids = sorted(list(h5r["/"]))
            for slice_id in slice_ids:
                if slice_id.isdigit() is True and slice_id == "1" and f"/{slice_id}/EBSD" in h5r:
                    # non-negative int, parse for now only the 1. slice
                    self.prfx = f"/{slice_id}"
                    ckey = self.init_named_cache(f"ebsd{cache_id}")  # name of the cache to use
                    self.parse_and_normalize_slice_ebsd_header(h5r, ckey)
                    self.parse_and_normalize_slice_ebsd_phases(h5r, ckey)
                    self.parse_and_normalize_slice_ebsd_data(h5r, ckey)
                    # add more information to pass to hfive parser
                    cache_id += 1

    def parse_and_normalize_slice_ebsd_header(self, fp, ckey: str):
        grp_name = f"{self.prfx}/EBSD/Header"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        # TODO::check if Oxford always uses SquareGrid like assumed here
        self.tmp[ckey]["dimensionality"] = 2
        self.tmp[ckey]["grid_type"] = SQUARE_GRID
        # the next two lines encode the typical assumption that is not reported in tech partner file!
        self.tmp[ckey]["tiling"] = REGULAR_TILING
        self.tmp[ckey]["flight_plan"] = FLIGHT_PLAN

        req_fields = ["X Cells", "Y Cells", "X Step", "Y Step"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        # X Cells, yes, H5T_NATIVE_INT32, (1, 1), Map: Width in pixels, Line scan: Length in pixels.
        self.tmp[ckey]["n_x"] = fp[f"{grp_name}/X Cells"][0]
        # Y Cells, yes, H5T_NATIVE_INT32, (1, 1), Map: Height in pixels. Line scan: Always set to 1.
        self.tmp[ckey]["n_y"] = fp[f"{grp_name}/Y Cells"][0]
        # X Step, yes, H5T_NATIVE_FLOAT, (1, 1), Map: Step size along x-axis in micrometers. Line scan: step size along the line scan in micrometers.
        if read_strings_from_dataset(fp[f"{grp_name}/X Step"].attrs["Unit"]) == "um":
            self.tmp[ckey]["s_x"] = fp[f"{grp_name}/X Step"][0]
            self.tmp[ckey]["s_unit"] = "um"  # "µm"
        else:
            raise ValueError(f"Unexpected X Step Unit attribute !")
        # Y Step, yes, H5T_NATIVE_FLOAT, (1, 1), Map: Step size along y-axis in micrometers. Line scan: Always set to 0.
        if read_strings_from_dataset(fp[f"{grp_name}/Y Step"].attrs["Unit"]) == "um":
            self.tmp[ckey]["s_y"] = fp[f"{grp_name}/Y Step"][0]
        else:
            raise ValueError(f"Unexpected Y Step Unit attribute !")
        # TODO::check that all data in the self.oina are consistent

    def parse_and_normalize_slice_ebsd_phases(self, fp, ckey: str):
        """Parse EBSD header section for specific slice."""
        grp_name = f"{self.prfx}/EBSD/Header/Phases"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        # Phases, yes, Contains a subgroup for each phase where the name
        # of each subgroup is the index of the phase starting at 1.
        phase_ids = sorted(list(fp[f"{grp_name}"]), key=int)
        self.tmp[ckey]["phase"] = []
        self.tmp[ckey]["space_group"] = []
        self.tmp[ckey]["phases"] = {}
        for phase_id in phase_ids:
            if phase_id.isdigit() is True:
                self.tmp[ckey]["phases"][int(phase_id)] = {}
                sub_grp_name = f"/{grp_name}/{phase_id}"

                req_fields = ["Phase Name", "Reference", "Lattice Angles",
                              "Lattice Dimensions", "Space Group"]
                for req_field in req_fields:
                    if f"{sub_grp_name}/{req_field}" not in fp:
                        raise ValueError(f"Unable to parse {sub_grp_name}/{req_field} !")

                # Phase Name, yes, H5T_STRING, (1, 1)
                phase_name = read_strings_from_dataset(fp[f"{sub_grp_name}/Phase Name"][()])
                self.tmp[ckey]["phases"][int(phase_id)]["phase_name"] = phase_name

                # Reference, yes, H5T_STRING, (1, 1), Changed in version 2.0 to mandatory
                self.tmp[ckey]["phases"][int(phase_id)]["reference"] \
                    = read_strings_from_dataset(fp[f"{sub_grp_name}/Reference"][()])

                # Lattice Angles, yes, H5T_NATIVE_FLOAT, (1, 3), Three columns for the alpha, beta and gamma angles in radians
                if read_strings_from_dataset(fp[f"{sub_grp_name}/Lattice Angles"].attrs["Unit"]) == "rad":
                    angles = np.asarray(fp[f"{sub_grp_name}/Lattice Angles"][:].flatten())
                else:
                    raise ValueError(f"Unexpected case that Lattice Angles are not reported in rad !")
                self.tmp[ckey]["phases"][int(phase_id)]["alpha_beta_gamma"] = angles

                # Lattice Dimensions, yes, H5T_NATIVE_FLOAT, (1, 3), Three columns for a, b and c dimensions in Angstroms
                if read_strings_from_dataset(fp[f"{sub_grp_name}/Lattice Dimensions"].attrs["Unit"]) == "angstrom":
                    a_b_c = np.asarray(fp[f"{sub_grp_name}/Lattice Dimensions"][:].flatten()) * 0.1
                else:
                    raise ValueError(f"Unexpected case that Lattice Dimensions are not reported in angstroem !")
                self.tmp[ckey]["phases"][int(phase_id)]["a_b_c"] = a_b_c

                # Space Group, no, H5T_NATIVE_INT32, (1, 1), Space group index.
                # The attribute Symbol contains the string representation, for example P m -3 m.
                space_group = int(fp[f"{sub_grp_name}/Space Group"][0])
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

    def parse_and_normalize_slice_ebsd_data(self, fp, ckey: str):
        # https://github.com/oinanoanalysis/h5oina/blob/master/H5OINAFile.md
        grp_name = f"{self.prfx}/EBSD/Data"
        if f"{grp_name}" not in fp:
            raise ValueError(f"Unable to parse {grp_name} !")

        req_fields = ["Euler", "Phase", "X", "Y", "Band Contrast"]
        for req_field in req_fields:
            if f"{grp_name}/{req_field}" not in fp:
                raise ValueError(f"Unable to parse {grp_name}/{req_field} !")

        # Euler, yes, H5T_NATIVE_FLOAT, (size, 3), Orientation of Crystal (CS2) to Sample-Surface (CS1).
        if read_strings_from_dataset(fp[f"{grp_name}/Euler"].attrs["Unit"]) == "rad":
            self.tmp[ckey]["euler"] = np.asarray(fp[f"{grp_name}/Euler"], np.float32)
        else:
            raise ValueError(f"Unexpected case that Euler angle are not reported in rad !")
        self.tmp[ckey]["euler"] = format_euler_parameterization(self.tmp[ckey]["euler"])

        # Phase, yes, H5T_NATIVE_INT32, (size, 1), Index of phase, 0 if not indexed
        # no normalization needed, also in NXem the null model notIndexed is phase_identifier 0
        self.tmp[ckey]["phase_id"] = np.asarray(fp[f"{grp_name}/Phase"], np.int32)

        # normalize pixel coordinates to physical positions even though the origin can still dangle somewhere
        # expected is order on x is first all possible x values while y == 0
        # followed by as many copies of this linear sequence for each y increment
        # no action needed Oxford reports already the pixel coordinate multiplied by step
        if self.tmp[ckey]["grid_type"] != SQUARE_GRID:
            print(f"WARNING: Check carefully correct interpretation of scan_point coords!")
        # X, no, H5T_NATIVE_FLOAT, (size, 1), X position of each pixel in micrometers (origin: top left corner)
        # for Oxford instrument this is already the required tile and repeated array of shape (size,1)
        self.tmp[ckey]["scan_point_x"] = np.asarray(fp[f"{grp_name}/X"], np.float32)
        # inconsistency f32 in file although specification states float

        # Y, no, H5T_NATIVE_FLOAT, (size, 1), Y position of each pixel in micrometers (origin: top left corner)
        self.tmp[ckey]["scan_point_y"] = np.asarray(fp[f"{grp_name}/Y"], np.float32)
        # inconsistency f32 in file although specification states float

        # Band Contrast, no, H5T_NATIVE_INT32, (size, 1)
        self.tmp[ckey]["bc"] = np.asarray(fp[f"{grp_name}/Band Contrast"], np.int32)
        # inconsistency uint8 in file although specification states should be int32
        # promoting uint8 to int32 no problem
