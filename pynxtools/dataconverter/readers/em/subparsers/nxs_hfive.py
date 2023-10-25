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
from pynxtools.dataconverter.readers.em.utils.image_processing import thumbnail

from pynxtools.dataconverter.readers.em.subparsers.hfive_oxford import HdfFiveOxfordReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_bruker import HdfFiveBrukerEspritReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_edax import HdfFiveEdaxOimAnalysisReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_apex import HdfFiveEdaxApexReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_ebsd import HdfFiveCommunityReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_emsoft import HdfFiveEmSoftReader


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
            emsoft = HdfFiveEmSoftReader(self.file_path)
            emsoft.parse_and_normalize()
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
        hdf = HdfFiveEmSoftReader(f"{self.file_path}")
        if hdf.supported is True:
            return "emsoft"
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

    def get_named_axis(self, inp: dict, dim_name: str):
        return np.asarray(np.linspace(0,
                                      inp[f"n_{dim_name}"] - 1,
                                      num=inp[f"n_{dim_name}"],
                                      endpoint=True) * inp[f"s_{dim_name}"], np.float32)

    def process_roi_overview(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd") and inp[ckey] != {}:
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
        # prfx = f"/roi{roi_id}"
        trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing/DATA[roi]"
        template[f"{trg}/title"] = f"Region-of-interest overview image"
        template[f"{trg}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        contrast_modes = [(None, "n/a"),
                          ("bc", "normalized_band_contrast"),
                          ("ci", "normalized_confidence_index"),
                          ("mad", "normalized_mean_angular_deviation")]
        success = False
        for contrast_mode in contrast_modes:
            if contrast_mode[0] in inp.keys() and success is False:
                template[f"{trg}/data"] = {"compress": np.reshape(np.asarray(np.asarray((inp[contrast_mode[0]] / np.max(inp[contrast_mode[0]]) * 255.), np.uint32), np.uint8), (inp["n_y"], inp["n_x"]), order="C"), "strength": 1}
                template[f"{trg}/descriptor"] = contrast_mode[1]
                success = True
        if success is False:
            raise ValueError(f"{__name__} unable to generate plot for {trg} !")
        # 0 is y while 1 is x !
        template[f"{trg}/data/@long_name"] = f"Signal"
        template[f"{trg}/data/@CLASS"] = "IMAGE"  # required H5Web, RGB map
        template[f"{trg}/data/@IMAGE_VERSION"] = f"1.2"
        template[f"{trg}/data/@SUBCLASS_VERSION"] = np.int64(15)

        scan_unit = inp["s_unit"]
        if scan_unit == "um":
            scan_unit = "µm"
        template[f"{trg}/AXISNAME[axis_x]"] \
            = {"compress": self.get_named_axis(inp, "x"), "strength": 1}
        template[f"{trg}/AXISNAME[axis_x]/@long_name"] \
            = f"Coordinate along x-axis ({scan_unit})"
        template[f"{trg}/AXISNAME[axis_x]/@units"] = f"{scan_unit}"
        template[f"{trg}/AXISNAME[axis_y]"] \
            = {"compress": self.get_named_axis(inp, "y"), "strength": 1}
        template[f"{trg}/AXISNAME[axis_y]/@long_name"] \
            = f"Coordinate along y-axis ({scan_unit})"
        template[f"{trg}/AXISNAME[axis_y]/@units"] =  f"{scan_unit}"
        return template

    def process_roi_ebsd_maps(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd") and inp[ckey] != {}:
                if ckey.replace("ebsd", "").isdigit():
                    roi_id = int(ckey.replace("ebsd", ""))
                    self.process_roi_xmap(inp[ckey], roi_id, template)
                    self.process_roi_phases(inp[ckey], roi_id, template)
        return template

    def process_roi_xmap(self, inp: dict, roi_id: int, template: dict) -> dict:
        """Process crystal orientation map from normalized orientation data."""
        # for NeXus to create a default representation of the EBSD map to explore
        self.xmap = None
        self.axis_x = None
        self.axis_y = None
        if np.max((inp["n_x"], inp["n_y"])) < HFIVE_WEB_MAXIMUM_RGB:
            # can use the map discretization as is
            coordinates, _ = create_coordinate_arrays(
                (inp["n_y"], inp["n_x"]), (inp["s_y"], inp["s_x"]))
            xaxis = coordinates["x"]
            yaxis = coordinates["y"]
            print(f"xmi {np.min(xaxis)}, xmx {np.max(xaxis)}, " \
                  f"ymi {np.min(yaxis)}, ymx {np.max(yaxis)}")
            del coordinates
            self.axis_x = self.get_named_axis(inp, "x")
            self.axis_y = self.get_named_axis(inp, "y")
        else:
            raise ValueError(f"Downsampling for too large EBSD maps is currently not supported !")
            # need to regrid to downsample too large maps
            # TODO::implement 1NN-based downsampling approach
            #       build grid
            #       tree-based 1NN
            #       proceed as usual

        # TODO::there was one example 093_0060.h5oina
        # where HitRate was 75% but no pixel left unidentified ??
        print(f"Unique phase_identifier {np.unique(inp['phase_id'])}")
        min_phase_id = np.min(np.unique(inp["phase_id"]))
        if min_phase_id > 0:
            pyxem_phase_identifier = inp["phase_id"] - min_phase_id
        elif min_phase_id == 0:
            pyxem_phase_identifier = inp["phase_id"] - 1
        else:
            raise ValueError(f"Unable how to deal with unexpected phase_identifier!")
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
                               prop={},
                               scan_unit=inp["s_unit"])
        del xaxis
        del yaxis
        # "bc": inp["band_contrast"]}, scan_unit=inp["s_unit"])
        print(self.xmap)
        return template

    def process_roi_phases(self, inp: dict, roi_id: int, template: dict) -> dict:
        print("Parse crystal_structure_models aka phases...")
        phase_id = 0
        prfx = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing"
        n_pts = inp["n_x"] * inp["n_y"]
        n_pts_indexed = np.sum(inp["phase_id"] != 0)
        print(f"n_pts {n_pts}, n_pts_indexed {n_pts_indexed}")
        template[f"{prfx}/number_of_scan_points"] = np.uint32(n_pts)
        template[f"{prfx}/indexing_rate"] = np.float64(100. * n_pts_indexed / n_pts)
        template[f"{prfx}/indexing_rate/@units"] = f"%"
        grp_name = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{phase_id}]"
        template[f"{grp_name}/number_of_scan_points"] = np.uint32(0)
        template[f"{grp_name}/phase_identifier"] = np.uint32(phase_id)
        template[f"{grp_name}/phase_name"] = f"notIndexed"

        for pyxem_phase_id in np.arange(0, np.max(self.xmap.phase_id) + 1):
            # this loop is implicitly ignored as when xmap is None
            print(f"inp[phases].keys(): {inp['phases'].keys()}")
            if (pyxem_phase_id + 1) not in inp["phases"].keys():
                raise ValueError(f"{pyxem_phase_id + 1} is not a key in inp['phases'] !")
            # phase_id of pyxem notIndexed is -1 while for NeXus
            # it is 0 so add + 1 in naming schemes
            trg = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{pyxem_phase_id + 1}]"
            template[f"{trg}/number_of_scan_points"] \
                = np.uint32(np.sum(self.xmap.phase_id == pyxem_phase_id))
            template[f"{trg}/phase_identifier"] = np.uint32(pyxem_phase_id + 1)
            template[f"{trg}/phase_name"] \
                = f"{inp['phases'][pyxem_phase_id + 1]['phase_name']}"

            self.process_roi_phase_inverse_pole_figures(roi_id, pyxem_phase_id, template)
        return template

    def process_roi_phase_inverse_pole_figures(self,
                                               roi_id: int,
                                               pyxem_phase_id: int,
                                               template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings."""
        # call process_roi_ipf_map
        phase_name = self.xmap.phases[pyxem_phase_id].name
        print(f"Generate IPF map for {pyxem_phase_id}, {phase_name}...")

        projection_directions = [("X", [1., 0., 0.]),
                                 ("Y", [0., 1., 0.]),
                                 ("Z", [0., 0., 1.])]
        projection_vectors = [Vector3d.xvector(), Vector3d.yvector(), Vector3d.zvector()]
        for idx in [0, 1, 2]:
            ipf_key = plot.IPFColorKeyTSL(
                self.xmap.phases[pyxem_phase_id].point_group.laue,
                direction=projection_vectors[idx])

            fig = ipf_key.plot(return_figure=True)
            fig.savefig("temporary.png", dpi=300, facecolor='w', edgecolor='w',
                        orientation='landscape', format='png', transparent=False,
                        bbox_inches='tight', pad_inches=0.1, metadata=None)
            img = np.asarray(thumbnail(pil.open("temporary.png", "r", ["png"]),
                             size=HFIVE_WEB_MAXIMUM_RGB), np.uint8)  # no flipping
            img = img[:, :, 0:3]  # discard alpha channel
            if os.path.exists("temporary.png"):
                os.remove("temporary.png")

            rgb_px_with_phase_id = np.asarray(
                np.asarray(ipf_key.orientation2color(
                    self.xmap[phase_name].rotations) * 255., np.uint32), np.uint8)

            print(f"idx {idx}, phase_name {phase_name}, shape {self.xmap.shape}")
            ipf_rgb_map = np.asarray(
                np.uint8(np.zeros((self.xmap.shape[0] * self.xmap.shape[1], 3)) * 255.))
            # background is black instead of white (which would be more pleasing)
            # but IPF color maps have a whitepoint which encodes in fact an orientation
            # and because of that we may have a single crystal with an orientation
            # close to the whitepoint which become a fully white seemingly "empty" image
            ipf_rgb_map[self.xmap.phase_id == pyxem_phase_id, :] = rgb_px_with_phase_id
            ipf_rgb_map = np.reshape(
                ipf_rgb_map, (self.xmap.shape[0], self.xmap.shape[1], 3), order="C")
            # 0 is y while 1 is x !

            trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing" \
                  f"/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{pyxem_phase_id + 1}]" \
                  f"/MS_IPF[ipf{idx + 1}]"
            template[f"{trg}/projection_direction"] = np.asarray([0., 0., 1.], np.float32)

            # add the IPF color map
            mpp = f"{trg}/DATA[map]"
            template[f"{mpp}/title"] \
                = f"Inverse pole figure {projection_directions[idx][0]} {phase_name}"
            template[f"{mpp}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{mpp}/@signal"] = "data"
            template[f"{mpp}/@axes"] = ["axis_y", "axis_x"]
            template[f"{mpp}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
            template[f"{mpp}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
            template[f"{mpp}/DATA[data]"] = {"compress": ipf_rgb_map, "strength": 1}
            template[f"{mpp}/DATA[data]/@CLASS"] = "IMAGE"  # required, H5Web, RGB
            template[f"{mpp}/DATA[data]/@IMAGE_VERSION"] = "1.2"
            template[f"{mpp}/DATA[data]/@SUBCLASS_VERSION"] = np.int64(15)

            scan_unit = self.xmap.scan_unit
            if scan_unit == "um":
                scan_unit = "µm"
            template[f"{mpp}/AXISNAME[axis_x]"] = {"compress": self.axis_x, "strength": 1}
            template[f"{mpp}/AXISNAME[axis_x]/@long_name"] \
                = f"Coordinate along x-axis ({scan_unit})"
            template[f"{mpp}/AXISNAME[axis_x]/@units"] = f"{scan_unit}"
            template[f"{mpp}/AXISNAME[axis_y]"] = {"compress": self.axis_y, "strength": 1}
            template[f"{mpp}/AXISNAME[axis_y]/@long_name"] \
                = f"Coordinate along y-axis ({scan_unit})"
            template[f"{mpp}/AXISNAME[axis_y]/@units"] = f"{scan_unit}"

            # add the IPF color map legend/key
            lgd = f"{trg}/DATA[legend]"
            template[f"{lgd}/title"] \
                = f"Inverse pole figure {projection_directions[idx][0]} {phase_name}"
            # template[f"{trg}/title"] = f"Inverse pole figure color key with SST"
            template[f"{lgd}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{lgd}/@signal"] = "data"
            template[f"{lgd}/@axes"] = ["axis_y", "axis_x"]
            template[f"{lgd}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
            template[f"{lgd}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
            template[f"{lgd}/data"] = {"compress": img, "strength": 1}
            template[f"{lgd}/data/@CLASS"] = f"IMAGE"  # required by H5Web to plot RGB maps
            template[f"{lgd}/data/@IMAGE_VERSION"] = f"1.2"
            template[f"{lgd}/data/@SUBCLASS_VERSION"] = np.int64(15)

            template[f"{lgd}/AXISNAME[axis_x]"] \
                = {"compress": np.asarray(np.linspace(0,
                                                      np.shape(img)[1] - 1,
                                                      num=np.shape(img)[1],
                                                      endpoint=True), np.uint32),
                   "strength": 1}
            template[f"{lgd}/AXISNAME[axis_x]/@long_name"] = "Pixel along x-axis"
            template[f"{lgd}/AXISNAME[axis_x]/@units"] = "px"
            template[f"{lgd}/AXISNAME[axis_y]"] \
                = {"compress": np.asarray(np.linspace(0,
                                                      np.shape(img)[0] - 1,
                                                      num=np.shape(img)[0],
                                                      endpoint=True), np.uint32),
                   "strength": 1}
            template[f"{lgd}/AXISNAME[axis_y]/@long_name"] = "Pixel along y-axis"
            template[f"{lgd}/AXISNAME[axis_y]/@units"] = "px"

        # call process_roi_ipf_color_key
        return template
