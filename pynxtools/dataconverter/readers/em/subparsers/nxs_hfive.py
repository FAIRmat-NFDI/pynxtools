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
"""HDF5 base parser to inherit from for tech-partner-specific HDF5 subparsers."""

# the base parser implements the processing of standardized orientation maps via
# the pyxem software package from the electron microscopy community
# specifically so-called NeXus default plots are generated to add RDMS-relevant
# information to the NeXus file which supports scientists with judging the potential
# value of the dataset in the context of them using research data management systems (RDMS)
# in effect this parser is the partner of the MTex parser for all those file formats
# which are HDF5 based and which (at the time of working on this example Q3/Q4 2023)
# where not supported my MTex
# with offering this parser we also would like to embrace and acknowledge the efforts
# of other electron microscopists (like the pyxem team, hyperspy etc.) and their work
# towards software tools which are complementary to the MTex texture toolbox
# one could have also implemented the HDF5 parsing inside MTex but we leave this as a
# task for the community and instead focus here on showing a more diverse example
# towards more interoperability between the different tools in the community

import os, glob, re, sys
from typing import Dict, Any, List
import numpy as np
import h5py
import yaml, json
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

from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset
from pynxtools.dataconverter.readers.em.utils.hfive_web_constants import HFIVE_WEB_MAXIMUM_RGB

from pynxtools.dataconverter.readers.em.subparsers.hfive_oxford import HdfFiveOxfordReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_bruker import HdfFiveBrukerEspritReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_edax import HdfFiveEdaxOimAnalysisReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_apex import HdfFiveEdaxApexReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_ebsd import HdfFiveCommunityReader
# from pynxtools.dataconverter.readers.em.subparsers.hfive_emsoft import HdfFiveEmSoftReader


class NxEmNxsHfiveSubParser:
    """Map content from different type of *.h5 files on an instance of NXem."""

    def __init__(self, entry_id: int = 1, input_file_name: str = ""):
        """Overwrite constructor of the generic reader."""
        if entry_id > 0:
            self.entry_id = entry_id
        else:
            self.entry_id = 1
        self.file_path = input_file_name
        self.cache = {"is_filled": False}
        self.xmap = None

    def parse(self, template: dict) -> dict:
        hfive_parser_type = self.identify_hfive_type()
        if hfive_parser_type is None:
            print(f"{self.file_path} does not match any of the supported HDF5 formats")
            return template
        print(f"Parsing via {hfive_parser_type}...")

        # ##MK::current implementation pulls all entries into the template
        # before writing them out, this might not fit into main memory
        # copying over all data and content within tech partner files into NeXus makes
        # not much sense as the data exists and we would like to motivate that
        # tech partners and community members write NeXus content directly
        # therefore currently in this example we carry over the EBSD map and some
        # metadata to motivate that there is indeed value wrt to interoperability
        # when such data are harmonized exactly this is the point we would like to
        # make with this example for NeXus and NOMAD OASIS within the FAIRmat project
        # it is practically beyond our resources to implement a mapping for all cases
        # and corner cases of the vendor files
        # ideally concept mapping would be applied to just point to pieces of information
        # in the HDF5 file that is written by the tech partners however because of the
        # fact that currently these pieces of information are formatted very differently
        # it is non-trivial to establish this mapping and only because of this we
        # map over manually
        if hfive_parser_type == "oxford":
            oina = HdfFiveOxfordReader(self.file_path)
            oina.parse_and_normalize()
            self.process_into_template(oina.tmp, template)
        elif hfive_parser_type == "bruker":
            bruker = HdfFiveBrukerEspritReader(self.file_path)
            bruker.parse_and_normalize()
            self.process_into_template(bruker.tmp, template)
        elif hfive_parser_type == "apex":
            apex = HdfFiveEdaxApexReader(self.file_path)
            apex.parse_and_normalize()
            self.process_into_template(apex.tmp, template)
        elif hfive_parser_type == "edax":
            edax = HdfFiveEdaxOimAnalysisReader(self.file_path)
            edax.parse_and_normalize()
            self.process_into_template(edax.tmp, template)
        elif hfive_parser_type == "hebsd":
            ebsd = HdfFiveCommunityReader(self.file_path)
            ebsd.parse_and_normalize()
            self.process_into_template(ebsd.tmp, template)
        elif hfive_parser_type == "emsoft":
            return template
        else:  # none or something unsupported
            return template
        return template

    def identify_hfive_type(self):
        """Identify if HDF5 file matches a known format for which a subparser exists."""
        # tech partner formats used for measurement
        hdf = HdfFiveOxfordReader(f"{self.file_path}")
        if hdf.supported is True:
            return "oxford"
        hdf = HdfFiveEdaxOimAnalysisReader(f"{self.file_path}")
        if hdf.supported is True:
            return "edax"
        hdf = HdfFiveEdaxApexReader(f"{self.file_path}")
        if hdf.supported is True:
            return "apex"
        hdf = HdfFiveBrukerEspritReader(f"{self.file_path}")
        if hdf.supported is True:
            return "bruker"
        hdf = HdfFiveCommunityReader(f"{self.file_path}")
        if hdf.supported is True:
            return "hebsd"
        # computer simulation tools
        # hdf = HdfFiveEmSoftReader(f"{self.file_path}")
        # if hdf.supported is True:
        #     return "emsoft"
        return None

    def process_into_template(self, inp: dict, template: dict) -> dict:
        debugging = False
        if debugging is True:
            for key, val in inp.items():
                if isinstance(val, dict):
                    for ckey, cval in val.items():
                        print(f"{ckey}, {cval}")
                else:
                    print(f"{key}, {val}")

        self.process_roi_overview(inp, template)
        self.process_roi_ebsd_maps(inp, template)
        return template

    def process_roi_overview(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd"):
                self.process_roi_overview_ebsd_based(
                    inp[ckey], ckey.replace("ebsd", ""), template)
                break  # only one roi for now
        return template

    def process_roi_overview_ebsd_based(self,
                                        inp: dict,
                                        roi_id: str,
                                        template: dict) -> dict:
        print("Parse ROI default plot...")
        # prfx = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/region_of_interest/roi{roi_id}"
        prfx = f"/roi{roi_id}"
        trg = f"{prfx}"
        template[f"{trg}/title"] = str("Region-of-interest overview image")
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        trg = f"{prfx}/data"
        contrast_modes = [(None, "n/a"),
                          ("bc", "normalized_band_contrast"),
                          ("ci", "normalized_confidence_index"),
                          ("mad", "normalized_mean_angular_deviation")]
        success = False
        for contrast_mode in contrast_modes:
            if contrast_mode[0] in inp.keys() and success is False:
                template[f"{trg}"] = {"compress": np.reshape(np.asarray(np.asarray((inp[contrast_mode[0]] / np.max(inp[contrast_mode[0]]) * 255.), np.uint32), np.uint8), (inp["n_y"], inp["n_x"]), order="C"), "strength": 1}
                template[f"{prfx}/descriptor"] = contrast_mode[1]
                success = True
        if success is False:
            raise ValueError(f"{__name__} unable to generate plot for {prfx} !")
        # 0 is y while 1 is x !
        template[f"{trg}/@long_name"] = "Signal"
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        trg = f"{prfx}/axis_x"
        template[f"{trg}"] = {"compress": np.asarray(inp["scan_point_x"], np.float32), "strength": 1}
        template[f"{trg}/@long_name"] = f"Coordinate along x-axis ({inp['s_unit']})"
        template[f"{trg}/@units"] = f"{inp['s_unit']}"
        trg = f"{prfx}/axis_y"
        template[f"{trg}"] = {"compress": np.asarray(inp["scan_point_y"], np.float32), "strength": 1}
        template[f"{trg}/@long_name"] = f"Coordinate along y-axis ({inp['s_unit']})"
        template[f"{trg}/@units"] =  f"{inp['s_unit']}"
        return template

    def process_roi_ebsd_maps(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd"):
                roi_identifier = ckey.replace("ebsd", "")
                self.process_roi_xmap(
                    inp[ckey], roi_identifier, template)
                # self.process_roi_phases(
                #     inp[ckey], roi_identifier, template)
                # self.process_roi_inverse_pole_figures(
                #     inp[ckey], roi_identifier, template)
                break  # only one roi for now
        return template

    def process_roi_xmap(self, inp: dict, roi_id: str, template: dict) -> dict:
        """Process crystal orientation map from normalized orientation data."""
        # for NeXus to create a default representation of the EBSD map to explore
        if np.max((inp["n_x"], inp["n_y"])) < HFIVE_WEB_MAXIMUM_RGB:
            # can use the map discretization as is
            coordinates, _ = create_coordinate_arrays(
                (inp["n_x"], inp["n_y"]), (inp["s_x"], inp["s_y"]))
            xaxis = coordinates["x"]
            yaxis = coordinates["y"]
            del coordinates
        else:
            raise ValueError(f"Downsampling for too large EBSD maps is currently not supported !")
            # need to regrid to downsample too large maps
            # TODO::implement 1NN-based downsampling approach
            #       build grid
            #       tree-based 1NN
            #       proceed as usual

        pyxem_phase_identifier = inp["phase_id"] - 1
        # inp["phase_id"] - (np.min(inp["phase_id"]) - (-1))
        # for pyxem the non-indexed has to be -1 instead of 0 which is what NeXus uses
        # -1 always because content of inp["phase_id"] is normalized
        # to NeXus NXem_ebsd_crystal_structure concept already!
        print(f"Unique pyxem_phase_identifier {np.unique(pyxem_phase_identifier)}")

        self.xmap = CrystalMap(rotations=Rotation.from_euler(euler=inp["euler"],
                                                             direction='lab2crystal',
                                                             degrees=False),
                               x=xaxis, y=yaxis,
                               phase_id=pyxem_phase_identifier,
                               phase_list=PhaseList(space_groups=inp["space_group"],
                                                    structures=inp["phase"]),
                               prop={})
        # "bc": inp["band_contrast"]}, scan_unit=inp["s_unit"])
        print(self.xmap)
        return template

    def process_roi_phases(self, template: dict) -> dict:
        return template

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
