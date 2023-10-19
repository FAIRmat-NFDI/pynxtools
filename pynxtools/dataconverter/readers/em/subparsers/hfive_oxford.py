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

from pynxtools.dataconverter.readers.em.subparsers.hfive import \
    HdfFiveGenericReader, read_strings_from_dataset
from pynxtools.dataconverter.readers.em.subparsers.pyxem_processor import PyxemProcessor


class HdfFiveOinaReader(HdfFiveGenericReader):
    """Read h5oina"""
    def __init__(self, file_name: str = ""):
        super().__init__(file_name)
        # this specialized reader implements reading capabilities for the following formats
        self.supported_version = {}
        self.version = {}
        self.supported_version["tech_partner"] = ["Oxford Instruments"]
        self.supported_version["schema_name"] = ["H5OINA"]
        self.supported_version["schema_version"] = ["2.0", "3.0", "4.0", "5.0"]
        self.supported_version["writer_name"] = ["AZTec"]
        self.supported_version["writer_version"] \
            = ["4.4.7495.1", "5.0.7643.1", "5.1.7829.1", "6.0.8014.1", "6.0.8196.1"]
        self.supported = True
        # check if instance matches all constraints to qualify as that supported h5oina
        h5r = h5py.File(self.file_name, "r")
        if "/Manufacturer" in h5r:
            self.version["tech_partner"] \
                = super().read_strings_from_dataset(h5r["/Manufacturer"][()])
            if self.version["tech_partner"] not in self.supported_version["tech_partner"]:
                # print(f"{self.version['tech_partner']} is not {self.version['tech_partner']} !")
                self.supported = False
        else:
            self.supported = False
        # only because we know (thanks to Philippe Pinard who wrote the H5OINA writer) that different
        # writer versions should implement the different HDF version correctly we can lift the
        # constraint on the writer_version for which we had examples available
        if "/Software Version" in h5r:
            self.version["writer_version"] \
                = super().read_strings_from_dataset(h5r["/Software Version"][()])
            if self.version["writer_version"] not in self.supported_version["writer_version"]:
                # print(f"{self.version['writer_version']} is not any of {self.supported_version['writer_version']} !")
                self.supported = False
        else:
            self.supported = False
        if "/Format Version" in h5r:
            self.version["schema_version"] \
                = super().read_strings_from_dataset(h5r["/Format Version"][()])
            if self.version["schema_version"] not in self.supported_version["schema_version"]:
                # print(f"{self.version['schema_version']} is not any of {self.supported_version['schema_version']} !")
                self.supported = False
        else:
            self.supported = False
        h5r.close()

        if self.supported is True:
            # print(f"Reading {self.file_name} is supported")
            self.version["schema_name"] = self.supported_version["schema_name"]
            self.version["writer_name"] = self.supported_version["writer_name"]
            # print(f"{self.version['schema_name']}, {self.supported_version['schema_version']}, {self.supported_version['writer_name']}, {self.supported_version['writer_version']}")
        # else:
            # print(f"Reading {self.file_name} is not supported!")

    def parse(self, template: dict, entry_id=1) -> dict:
        """Parse NeXus-relevant (meta)data from an H5OINA file."""
        print(f"Parsing with sub-parser {__class__.__name__}, " \
              f"file: {self.file_name}, entry_id: {entry_id}")
        # find how many slices there are
        with h5py.File(f"{self.file_name}", "r") as h5r:
            entries = sorted(list(h5r["/"]), key=int)
            for entry in entries:
                if entry.isdigit() is True: # non-negative integer
                    if entry == "1":
                        self.slice = {}
                        self.parse_and_normalize_slice(h5r, int(entry))
                        # at this point all Oxford jargon is ironed out and the
                        # call is the same irrespective of the tech partner
                        # that was used to take the orientation maps
                        pyx = PyxemProcessor(entry_id)
                        pyx.process_roi_overview(template)
                        pyx.process_roi_xmap(template)
                        pyx.process_roi_phases(template)
                        pyx.process_roi_inverse_pole_figures(template)
        return template

    def parse_and_normalize_slice(fp, slice_id: int):
        """Read and normalize away Oxford-specific formatting of data in specific slice."""
        self.parse_and_normalize_slice_ebsd_data(fp, slice_id)
        self.parse_and_normalize_slice_ebsd_header(fp, slice_id)

    def parse_and_normalize_slice_ebsd_data(fp, slice_id: int):
        # https://github.com/oinanoanalysis/h5oina/blob/master/H5OINAFile.md
        group_name = f"/{slice_id}/EBSD/Data"
        self.slice["slice_id"] = slice_id
        print(f"Parsing {group_name}, {self.slice['slice_id']}")
        # Euler, yes, H5T_NATIVE_FLOAT, (size, 3), Orientation of Crystal (CS2) to Sample-Surface (CS1).
        if f"{group_name}/Euler" in fp:
            is_degrees = False
            if read_strings_from_dataset(fp[f"{group_name}/Euler"].attrs["Unit"]) == "rad":
                is_degrees = False
            self.slice["rotation"] = Rotation.from_euler(euler=fp[f"{group_name}/Euler"],
                                                         direction='lab2crystal',
                                                         degrees=is_degrees)
        else:
            raise ValueError(f"Unable to parse Euler !")

        # Phase, yes, H5T_NATIVE_INT32, (size, 1), Index of phase, 0 if not indexed
        # no normalization needed, also in NXem_ebsd the null model notIndexed is phase_identifier 0
        if f"{group_name}/Phase" in fp:
            self.slice["phase_id"] = np.asarray(fp[f"{group_name}/Phase"], np.int32)
        else:
            raise ValueError(f"Unable to parse Phase !")

        # X, no, H5T_NATIVE_FLOAT, (size, 1), X position of each pixel in micrometers (origin: top left corner)
        if f"{group_name}/X" in fp:
            self.slice["scan_point_x"] = np.asarray(fp[f"{group_name}/X"], np.float32)
        else:
            raise ValueError(f"Unable to parse pixel position X !")

        # Y, no, H5T_NATIVE_FLOAT, (size, 1), Y position of each pixel in micrometers (origin: top left corner)
        if f"{group_name}/Y" in fp:
            self.slice["scan_point_y"] = np.asarray(fp[f"{group_name}/Y"], np.float32)
            # TODO::inconsistent float vs f32
        else:
            raise ValueError(f"Unable to parse pixel position Y !")

        # Band Contrast, no, H5T_NATIVE_INT32, (size, 1)
        if f"{group_name}/Band Contrast" in fp:
            self.slice["band_contrast"] = np.asarray(fp[f"{group_name}/Band Contrast"], np.uint8)
            # TODO::inconsistent int32 vs uint8
        else:
            raise ValueError(f"Unable to band contrast !")

        # TODO::processed patterns

    def parse_and_normalize_slice_ebsd_header(fp, slice_id: int):
        """Parse EBSD header section for specific slice."""
        group_name = f"/{slice_id}/EBSD/Header"
        # Phases, yes, Contains a subgroup for each phase where the name of each subgroup is the index of the phase starting at 1.
        if f"{group_name}/Phases" in fp:
            phase_ids = sorted(list(fp[f"{group_name}/Phases"]), key=int)
            self.slice["phase"] = []
            self.slice["space_group"] = []
            self.slice["phases"] = {}
            for phase_id in phase_ids:
                if phase_id.isdigit() is True:
                    self.slice["phases"][int(phase_id)] = {}
                    sub_group_name = f"/{slice_id}/EBSD/Header/Phases"
                    # Phase Name, yes, H5T_STRING, (1, 1)
                    if f"{sub_group_name}/Phase Name" in fp:
                        phase_name = read_strings_from_dataset(fp[f"{sub_group_name}/Phase Name"][()])
                        self.slice["phases"][int(phase_id)]["phase_name"] = phase_name
                    else:
                        raise ValueError("Unable to parse Phase Name !")

                    # Reference, yes, H5T_STRING, (1, 1), Changed in version 2.0 to mandatory
                    if f"{sub_group_name}/Reference" in fp:
                        self.slice["phases"][int(phase_id)]["reference"] \
                            = read_strings_from_dataset(fp[f"{sub_group_name}/Reference"][()])
                    else:
                        raise ValueError("Unable to parse Reference !")

                    # Lattice Angles, yes, H5T_NATIVE_FLOAT, (1, 3), Three columns for the alpha, beta and gamma angles in radians
                    if f"{sub_group_name}/Lattice Angles" in fp:
                        is_degrees = False
                        if read_strings_from_dataset(fp[f"{sub_group_name}/Lattice Angles"].attrs["Unit"]) == "rad":
                            is_degrees = False
                        angles = np.asarray(fp[f"{sub_group_name}/Lattice Angles"][:].flatten()) / np.pi * 180.
                        self.slice["phases"][int(phase_id)]["alpha_beta_gamma"] \
                            = angles
                    else:
                        raise ValueError("Unable to parse Lattice Angles !")

                    # Lattice Dimensions, yes, H5T_NATIVE_FLOAT, (1, 3), Three columns for a, b and c dimensions in Angstroms
                    if f"{sub_group_name}/Lattice Dimensions" in fp:
                        is_nanometer = False
                        if read_strings_from_dataset(fp[f"{sub_group_name}/Lattice Dimensions"].attrs["Unit"]) == "angstrom":
                            is_nanometer = False
                        a_b_c = np.asarray(fp[f"{sub_group_name}/Lattice Dimensions"][:].flatten()) * 0.1
                        self.slice["phases"][int(phase_id)]["a_b_c"] = a_b_c
                    else:
                        raise ValueError("Unable to parse Lattice Dimensions !")

                    # Space Group, no, H5T_NATIVE_INT32, (1, 1), Space group index.
                    # The attribute Symbol contains the string representation, for example P m -3 m.
                    if f"{sub_group_name}/Space Group" in fp:
                        space_group = int(fp[f"{sub_group_name}/Space Group"][0])
                        self.slice["phases"][int(phase_id)]["space_group"] = space_group
                    else:
                        raise ValueError("Unable to parse Space Group !")
                    if len(self.slice["space_group"]) > 0:
                        self.slice["space_group"].append(space_group)
                    else:
                        self.slice["space_group"] = [space_group]

                    if len(self.slice["phase"]) > 0:
                        Structure(title=phase_name, atoms=None,
                                  lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                  angles[0], angles[1], angles[2]))
                    else:
                        self.slice["phase"] \
                            = [Structure(title=phase_name, atoms=None,
                                         lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                         angles[0], angles[1], angles[2]))]
        else:
            raise ValueError("Unable to parse Phases !")

        # X Cells, yes, H5T_NATIVE_INT32, (1, 1), Map: Width in pixels, Line scan: Length in pixels.
        if f"{group_name}/X Cell" in fp:
            self.slice["n_x"] = fp[f"{group_name}/X Cells"][0]
        else:
            raise ValueError("Unable to parse X Cells !")
        # Y Cells, yes, H5T_NATIVE_INT32, (1, 1), Map: Height in pixels. Line scan: Always set to 1.
        if f"{group_name}/Y Cell" in fp:
            self.slice["n_x"] = fp[f"{group_name}/Y Cells"][0]
        else:
            raise ValueError("Unable to parse Y Cells !")
        # X Step, yes, H5T_NATIVE_FLOAT, (1, 1), Map: Step size along x-axis in micrometers. Line scan: step size along the line scan in micrometers.
        if f"{group_name}/X Step" in fp:
            if read_strings_from_dataset(fp[f"{group_name}/X Step"].attrs["Unit"]) == "um":
                self.slice["s_x"] = fp[f"{group_name}/X Step"][0]
                self.slice["s_unit"] = "µm"
            else:
                raise ValueError("Unexpected X Step Unit attribute !")
        else:
            raise ValueError("Unable to parse X Step !")
        # Y Step, yes, H5T_NATIVE_FLOAT, (1, 1), Map: Step size along y-axis in micrometers. Line scan: Always set to 0.
        if f"{group_name}/Y Step" in fp:
            if read_strings_from_dataset(fp[f"{group_name}/Y Step"].attrs["Unit"]) == "um":
                self.slice["s_y"] = fp[f"{group_name}/Y Step"][0]
            else:
                raise ValueError("Unexpected Y Step Unit attribute !")
        else:
            raise ValueError("Unable to parse Y Step !")
        # TODO::check that all data in the self.oina are consistent

        for key, val in self.slice.items():
            print(f"{key}, type: {type(val)}, shape: {np.shape(val)}")
