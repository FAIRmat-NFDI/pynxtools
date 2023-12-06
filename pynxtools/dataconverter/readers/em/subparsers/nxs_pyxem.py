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
from orix.quaternion.symmetry import get_point_group
from orix.vector import Vector3d

import matplotlib.pyplot as plt

from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset
from pynxtools.dataconverter.readers.em.utils.hfive_web_constants \
    import HFIVE_WEB_MAXIMUM_ROI, HFIVE_WEB_MAXIMUM_RGB
from pynxtools.dataconverter.readers.em.utils.hfive_web_utils \
    import hfive_web_decorate_nxdata
from pynxtools.dataconverter.readers.em.utils.image_processing import thumbnail
from pynxtools.dataconverter.readers.em.utils.get_sqr_grid import \
    get_scan_points_with_mark_data_discretized_on_sqr_grid
from pynxtools.dataconverter.readers.em.utils.get_scan_points import \
    get_scan_point_axis_values, get_scan_point_coords

PROJECTION_VECTORS = [Vector3d.xvector(), Vector3d.yvector(), Vector3d.zvector()]
PROJECTION_DIRECTIONS = [("X", Vector3d.xvector().data.flatten()),
                         ("Y", Vector3d.yvector().data.flatten()),
                         ("Z", Vector3d.zvector().data.flatten())]

from pynxtools.dataconverter.readers.em.subparsers.hfive_oxford import HdfFiveOxfordReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_bruker import HdfFiveBrukerEspritReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_edax import HdfFiveEdaxOimAnalysisReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_apex import HdfFiveEdaxApexReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_ebsd import HdfFiveCommunityReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_emsoft import HdfFiveEmSoftReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_dreamthreed import HdfFiveDreamThreedReader


def get_ipfdir_legend(ipf_key):
    """Generate IPF color map key for a specific ipf_key."""
    img = None
    fig = ipf_key.plot(return_figure=True)
    fig.savefig("temporary.png", dpi=300, facecolor='w', edgecolor='w',
                orientation='landscape', format='png', transparent=False,
                bbox_inches='tight', pad_inches=0.1, metadata=None)
    img = np.asarray(thumbnail(pil.open("temporary.png", "r", ["png"]),
                        size=HFIVE_WEB_MAXIMUM_RGB), np.uint8)  # no flipping
    img = img[:, :, 0:3]  # discard alpha channel
    if os.path.exists("temporary.png"):
        os.remove("temporary.png")
    return img


class NxEmNxsPyxemSubParser:
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
        # therefore, in this example we carry over the EBSD map and some metadata
        # to motivate that there is indeed value wrt to interoperability when such data
        # are harmonized upon injection in the RDMS - exactly this is the point
        # we would like to make with this comprehensive example of data harmonization
        # within the field of EBSD as one method in the field of electron diffraction
        # we use NeXus, NOMAD OASIS within the FAIRmat project
        # it is practically beyond our resources to implement a mapping for all cases
        # and corner cases of vendor files
        # ideally concept mapping would be applied to just point to pieces of information
        # in (HDF5) files based on which semantically understood pieces of information
        # are then interpreted and injected into the RDMS
        # currently the fact that the documentation by tech partners is incomplete
        # and the fact that conceptually similar or even the same concepts as instances
        # with their pieces of information are formatted very differently, it is
        # non-trivial to establish this mapping and only because of this we
        # map over using hardcoding of concept names and symbols

        # a collection of different tech-partner-specific subparser follows
        # these subparsers already extract specific information and perform a first
        # step of harmonization. The subparsers specifically store e.g. EBSD maps in a
        # tmp dictionary, which is
        # TODO: scan point positions (irrespective on which grid type (sqr, hex) these
        # were probed, in some cases the grid may have a two large extent along a dim
        # so that a sub-sampling is performed, here only for the purpose of using
        # h5web to show the IPF color maps but deal with the fact that h5web has so far
        # not been designed to deal with images as large as several thousand pixels along
        # either dimension
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
            # self.process_into_template(emsoft.tmp, template)
        elif hfive_parser_type == "dreamthreed":
            dreamthreed = HdfFiveDreamThreedReader(self.file_path)
            dreamthreed.parse_and_normalize()
            self.process_into_template(dreamthreed.tmp, template)
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
        hdf = HdfFiveDreamThreedReader(f"{self.file_path}")
        if hdf.supported is True:
            return "dreamthreed"
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
        """"Return scaled but not offset-calibrated scan point coordinates along dim."""
        # TODO::remove!
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
        # tech partner specific subparsers have just extracted the per scan point information
        # in the sequence they were (which is often how they were scanned)
        # however that can be a square, a hexagonal or some random grid
        # a consuming visualization tool (like h5web) may however not be able to
        # represent the data as point cloud but only visualizes a grid of square pixels
        # therefore in general the scan_point_x and scan_point_y arrays and their associated
        # data arrays such as euler should always be interpolated on a specific grid
        # Here, the square_grid supported by h5web with a specific maximum extent
        # which may represent a downsampled representation of the actual ROI
        # only in the case that indeed the grid is a square grid this interpolation is
        # obsolete but also only when the grid does not exceed the technical limitation
        # of here h5web
        # TODO::implement rediscretization using a kdtree take n_x, n_y, and n_z as guides

        trg_grid \
            = get_scan_points_with_mark_data_discretized_on_sqr_grid(inp,
                                                                     HFIVE_WEB_MAXIMUM_ROI)

        contrast_modes = [(None, "n/a"),
                          ("bc", "normalized_band_contrast"),
                          ("ci", "normalized_confidence_index"),
                          ("mad", "normalized_mean_angular_deviation")]
        contrast_mode = None
        for mode in contrast_modes:
            if mode[0] in trg_grid.keys() and contrast_mode is None:
                contrast_mode = mode
                break
        if contrast_mode is None:
            print(f"{__name__} unable to generate plot for entry{self.entry_id}, roi{roi_id} !")
            return template

        template[f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/@NX_class"] = "NXroi"
        # TODO::writer should decorate automatically!
        template[f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing/@NX_class"] = "NXprocess"
        # TODO::writer should decorate automatically!
        trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing/DATA[roi]"
        template[f"{trg}/title"] = f"Region-of-interest overview image"
        template[f"{trg}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
        template[f"{trg}/@signal"] = "data"
        dims = ["x", "y"]
        if trg_grid["dimensionality"] == 3:
            dims.append("z")
        idx = 0
        for dim in dims:
            template[f"{trg}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(idx)
            idx += 1
        template[f"{trg}/@axes"] = []
        for dim in dims[::-1]:
            template[f"{trg}/@axes"].append(f"axis_{dim}")

        if trg_grid["dimensionality"] == 3:
            template[f"{trg}/data"] = {"compress": np.squeeze(np.asarray(np.asarray((trg_grid[contrast_mode[0]] / np.max(trg_grid[contrast_mode[0]], axis=None) * 255.), np.uint32), np.uint8), axis=3), "strength": 1}
        else:
            template[f"{trg}/data"] = {"compress": np.reshape(np.asarray(np.asarray((trg_grid[contrast_mode[0]] / np.max(trg_grid[contrast_mode[0]]) * 255.), np.uint32), np.uint8), (trg_grid["n_y"], trg_grid["n_x"]), order="C"), "strength": 1}
        template[f"{trg}/descriptor"] = contrast_mode[1]

        # 0 is y while 1 is x for 2d, 0 is z, 1 is y, while 2 is x for 3d
        template[f"{trg}/data/@long_name"] = f"Signal"
        hfive_web_decorate_nxdata(f"{trg}/data", template)

        scan_unit = trg_grid["s_unit"]
        if scan_unit == "um":
            scan_unit = "µm"
        for dim in dims:
            template[f"{trg}/AXISNAME[axis_{dim}]"] \
                = {"compress": self.get_named_axis(trg_grid, dim), "strength": 1}
            template[f"{trg}/AXISNAME[axis_{dim}]/@long_name"] \
                = f"Coordinate along {dim}-axis ({scan_unit})"
            template[f"{trg}/AXISNAME[axis_{dim}]/@units"] = f"{scan_unit}"
        return template

    def process_roi_ebsd_maps(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd") and inp[ckey] != {}:
                if ckey.replace("ebsd", "").isdigit():
                    roi_id = int(ckey.replace("ebsd", ""))
                    if "n_z" not in inp[ckey].keys():
                        self.prepare_roi_ipfs_phases_twod(inp[ckey], roi_id, template)
                        self.process_roi_ipfs_phases_twod(inp[ckey], roi_id, template)
                        # self.onthefly_process_roi_ipfs_phases_two(inp[ckey], roi_id, template)
                    else:
                        self.onthefly_process_roi_ipfs_phases_threed(inp[ckey], roi_id, template)
        return template

    def prepare_roi_ipfs_phases_twod(self, inp: dict, roi_id: int, template: dict) -> dict:
        """Process crystal orientation map from normalized orientation data."""
        # for NeXus to create a default representation of the EBSD map to explore
        # get rid of this xmap at some point it is really not needed in my option
        # one can work with passing the set of EulerAngles to the IPF mapper directly
        # the order of the individual per scan point results arrays anyway are assumed
        # to have the same sequence of scan points and thus the same len along the scan axes
        self.xmap = None
        self.axis_x = None
        self.axis_y = None

        print(f"Unique phase_identifier {np.unique(inp['phase_id'])}")
        min_phase_id = np.min(np.unique(inp["phase_id"]))

        if np.max((inp["n_x"], inp["n_y"])) > HFIVE_WEB_MAXIMUM_RGB:
            # assume center of mass of the scan points
            # TODO::check if mapping correct for hexagonal and square grid
            aabb = [np.min(inp["scan_point_x"]) - 0.5 * inp["s_x"],
                    np.max(inp["scan_point_x"]) + 0.5 * inp["s_x"],
                    np.min(inp["scan_point_y"]) - 0.5 * inp["s_y"],
                    np.max(inp["scan_point_y"]) + 0.5 * inp["s_y"]]
            print(f"{aabb}")
            if aabb[1] - aabb[0] >= aabb[3] - aabb[2]:
                sqr_step_size = (aabb[1] - aabb[0]) / HFIVE_WEB_MAXIMUM_RGB
                nxy = [HFIVE_WEB_MAXIMUM_RGB,
                       int(np.ceil((aabb[3] - aabb[2]) / sqr_step_size))]
            else:
                sqr_step_size = (aabb[3] - aabb[2]) / HFIVE_WEB_MAXIMUM_RGB
                nxy = [int(np.ceil((aabb[1] - aabb[0]) / sqr_step_size)),
                       HFIVE_WEB_MAXIMUM_RGB]
            print(f"H5Web default plot generation, scaling nxy0 {[inp['n_x'], inp['n_y']]}, nxy {nxy}")
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
            xy = np.column_stack(
                (np.tile(np.linspace(0, nxy[0] - 1, num=nxy[0], endpoint=True) * sqr_step_size, nxy[1]),
                np.repeat(np.linspace(0, nxy[1] - 1, num=nxy[1], endpoint=True) * sqr_step_size, nxy[0])))
            print(f"xy {xy}, shape {np.shape(xy)}")
            tree = KDTree(np.column_stack((inp["scan_point_x"], inp["scan_point_y"])))
            d, idx = tree.query(xy, k=1)
            if np.sum(idx == tree.n) > 0:
                raise ValueError(f"kdtree query left some query points without a neighbor!")
            del d
            del tree
            pyxem_euler = np.zeros((np.shape(xy)[0], 3), np.float32)
            pyxem_euler = np.nan
            pyxem_euler = inp["euler"][idx, :]
            if np.isnan(pyxem_euler).any() is True:
                raise ValueError(f"Downsampling of the EBSD map left pixels without euler!")
            phase_new = np.zeros((np.shape(xy)[0],), np.int32) - 2
            phase_new = inp["phase_id"][idx]
            if np.sum(phase_new == -2) > 0:
                raise ValueError(f"Downsampling of the EBSD map left pixels without euler!")
            del xy

            if min_phase_id > 0:
                pyxem_phase_id = phase_new - min_phase_id
            elif min_phase_id == 0:
                pyxem_phase_id = phase_new - 1
            else:
                raise ValueError(f"Unable how to deal with unexpected phase_identifier!")
            del phase_new

            coordinates, _ = create_coordinate_arrays(
                (nxy[1], nxy[0]), (sqr_step_size, sqr_step_size))
            xaxis = coordinates["x"]
            yaxis = coordinates["y"]
            print(f"coordinates" \
                  f"xmi {np.min(xaxis)}, xmx {np.max(xaxis)}, " \
                  f"ymi {np.min(yaxis)}, ymx {np.max(yaxis)}")
            del coordinates
            self.axis_x = np.linspace(0, nxy[0] - 1, num=nxy[0], endpoint=True) * sqr_step_size
            self.axis_y = np.linspace(0, nxy[1] - 1, num=nxy[1], endpoint=True) * sqr_step_size
        else:
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

            pyxem_euler = inp["euler"]
            # TODO::there was one example 093_0060.h5oina
            # where HitRate was 75% but no pixel left unidentified ??
            if min_phase_id > 0:
                pyxem_phase_id = inp["phase_id"] - min_phase_id
            elif min_phase_id == 0:
                pyxem_phase_id = inp["phase_id"] - 1
            else:
                raise ValueError(f"Unable how to deal with unexpected phase_identifier!")

        # inp["phase_id"] - (np.min(inp["phase_id"]) - (-1))
        # for pyxem the non-indexed has to be -1 instead of 0 which is what NeXus uses
        # -1 always because content of inp["phase_id"] is normalized
        # to NeXus NXem_ebsd_crystal_structure concept already!
        print(f"Unique pyxem_phase_id {np.unique(pyxem_phase_id)}")
        self.xmap = CrystalMap(rotations=Rotation.from_euler(euler=pyxem_euler,
                                                             direction='lab2crystal',
                                                             degrees=False),
                               x=xaxis, y=yaxis,
                               phase_id=pyxem_phase_id,
                               phase_list=PhaseList(space_groups=inp["space_group"],
                                                    structures=inp["phase"]),
                               prop={},
                               scan_unit=inp["s_unit"])
        del xaxis
        del yaxis
        # "bc": inp["band_contrast"]}, scan_unit=inp["s_unit"])
        print(self.xmap)
        return template

    def process_roi_ipfs_phases_twod(self, inp: dict, roi_id: int, template: dict) -> dict:
        print("Parse crystal_structure_models aka phases (use xmap)...")
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

            min_phase_id = np.min(np.unique(inp["phase_id"]))
            if min_phase_id > 0:
                pyx_phase_id = inp["phase_id"] - min_phase_id
            elif min_phase_id == 0:
                pyx_phase_id = inp["phase_id"] - 1
            else:
                raise ValueError(f"Unable how to deal with unexpected phase_identifier!")
            del min_phase_id

            template[f"{trg}/number_of_scan_points"] \
                = np.uint32(np.sum(pyx_phase_id == pyxem_phase_id))
            del pyx_phase_id
            # not self.xmap.phase_id because in NeXus the number_of_scan_points is always
            # accounting for the original map size and not the potentially downscaled version
            # of the map as the purpose of the later one is exclusively to show a plot at all
            # because of a technical limitation of H5Web if there would be a tool that
            # could show larger RGB plots we would not need to downscale the EBSD map resolution!
            template[f"{trg}/phase_identifier"] = np.uint32(pyxem_phase_id + 1)
            template[f"{trg}/phase_name"] \
                = f"{inp['phases'][pyxem_phase_id + 1]['phase_name']}"

            self.process_roi_phase_ipfs_twod(roi_id, pyxem_phase_id, template)
        return template

    def onthefly_process_roi_ipfs_phases_twod(self, inp: dict, roi_id: int, template: dict) -> dict:
        # TODO: #####
        return template

    def process_roi_phase_ipfs_twod(self, roi_id: int, pyxem_phase_id: int, template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings for specific phase."""
        phase_name = self.xmap.phases[pyxem_phase_id].name
        print(f"Generate 2D IPF map for {pyxem_phase_id}, {phase_name}...")
        for idx in np.arange(0, len(PROJECTION_VECTORS)):
            ipf_key = plot.IPFColorKeyTSL(
                self.xmap.phases[pyxem_phase_id].point_group.laue,
                direction=PROJECTION_VECTORS[idx])
            img = get_ipfdir_legend(ipf_key)

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
            template[f"{trg}/projection_direction"] \
                = np.asarray(PROJECTION_VECTORS[idx].data.flatten(), np.float32)

            # add the IPF color map
            mpp = f"{trg}/DATA[map]"
            template[f"{mpp}/title"] \
                = f"Inverse pole figure {PROJECTION_DIRECTIONS[idx][0]} {phase_name}"
            template[f"{mpp}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{mpp}/@signal"] = "data"
            dims = ["x", "y"]
            template[f"{mpp}/@axes"] = []
            for dim in dims[::-1]:
                template[f"{mpp}/@axes"].append(f"axis_{dim}")
            enum = 0
            for dim in dims:
                template[f"{mpp}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(enum)
                enum += 1
            template[f"{mpp}/DATA[data]"] = {"compress": ipf_rgb_map, "strength": 1}
            hfive_web_decorate_nxdata(f"{mpp}/DATA[data]", template)

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
                = f"Inverse pole figure {PROJECTION_DIRECTIONS[idx][0]} {phase_name}"
            # template[f"{trg}/title"] = f"Inverse pole figure color key with SST"
            template[f"{lgd}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{lgd}/@signal"] = "data"
            template[f"{lgd}/@axes"] = []
            for dim in dims[::-1]:
                template[f"{lgd}/@axes"].append(f"axis_{dim}")
            enum = 0
            for dim in dims:
                template[f"{lgd}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(enum)
                enum += 1
            template[f"{lgd}/data"] = {"compress": img, "strength": 1}
            hfive_web_decorate_nxdata(f"{lgd}/data", template)

            dims = [("x", 1), ("y", 0)]
            for dim in dims:
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]"] \
                    = {"compress": np.asarray(np.linspace(0,
                                                          np.shape(img)[dim[1]] - 1,
                                                          num=np.shape(img)[dim[1]],
                                                          endpoint=True), np.uint32),
                       "strength": 1}
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]/@long_name"] \
                    = f"Pixel along {dim[0]}-axis"
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]/@units"] = "px"

        # call process_roi_ipf_color_key
        return template

    def onthefly_process_roi_ipfs_phases_threed(self, inp: dict, roi_id: int, template: dict) -> dict:
        print("Parse crystal_structure_models aka phases (no xmap)...")
        phase_id = 0
        prfx = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing"
        n_pts = inp["n_x"] * inp["n_y"] * inp["n_z"]
        n_pts_indexed = np.sum(inp["phase_id"] != 0)
        print(f"n_pts {n_pts}, n_pts_indexed {n_pts_indexed}")
        template[f"{prfx}/number_of_scan_points"] = np.uint32(n_pts)
        template[f"{prfx}/indexing_rate"] = np.float64(100. * n_pts_indexed / n_pts)
        template[f"{prfx}/indexing_rate/@units"] = f"%"
        grp_name = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{phase_id}]"
        template[f"{grp_name}/number_of_scan_points"] \
            = np.uint32(np.sum(inp["phase_id"] == 0))
        template[f"{grp_name}/phase_identifier"] = np.uint32(phase_id)
        template[f"{grp_name}/phase_name"] = f"notIndexed"

        print(f"----unique inp phase_id--->{np.unique(inp['phase_id'])}")
        for phase_id in np.arange(1, np.max(np.unique(inp["phase_id"])) + 1):
            # starting here at ID 1 because TODO::currently the only supported 3D case
            # is from DREAM3D and here phase_ids start at 0 but this marks in DREAM3D jargon
            # the 999 i.e. null-model of the notIndexed phase !
            print(f"inp[phases].keys(): {inp['phases'].keys()}")
            if phase_id not in inp["phases"].keys():
                raise ValueError(f"{phase_id} is not a key in inp['phases'] !")
            # pyxem_phase_id for notIndexed is -1, while for NeXus it is 0 so add + 1 in naming schemes
            trg = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{phase_id}]"

            # TODO::dealing with unexpected phase_identifier should not be an issue
            # with DREAM3D because that software is more restrictive on this
            template[f"{trg}/number_of_scan_points"] \
                = np.uint32(np.sum(inp["phase_id"] == phase_id))
            template[f"{trg}/phase_identifier"] = np.uint32(phase_id)
            template[f"{trg}/phase_name"] \
                = f"{inp['phases'][phase_id]['phase_name']}"

            # mind to pass phase_id - 1 from the perspective of pyxem because
            # in that software the id of the null-model is -1 and not 0 like in NeXus or DREAM3D!
            self.process_roi_phase_ipfs_threed(inp,
                                               roi_id,
                                               phase_id,
                                               inp["phases"][phase_id]["phase_name"],
                                               inp["phases"][phase_id]["space_group"],
                                               template)
        return template

    def process_roi_phase_ipfs_threed(self, inp: dict, roi_id: int, pyxem_phase_id: int, phase_name: str, space_group: int, template: dict) -> dict:
        """Generate inverse pole figures (IPF) for 3D mappings for specific phase."""
        # equivalent to the case in twod, one needs at if required regridding/downsampling
        # code here when any of the ROI's number of pixels along an edge > HFIVE_WEB_MAXIMUM_RGB
        # TODO: I have not seen any dataset yet where is limit is exhausted, the largest
        # dataset is a 3D SEM/FIB study from a UK project this is likely because to
        # get an EBSD map as large one already scans quite long for one section as making
        # a compromise is required and thus such hypothetical large serial-sectioning
        # studies would block the microscope for a very long time
        # however I have seen examples from Hadi Pirgazi with L. Kestens from Leuven
        # where indeed large but thin 3d slabs were characterized
        print(f"Generate 3D IPF map for {pyxem_phase_id}, {phase_name}...")
        rotations = Rotation.from_euler(
            euler=inp["euler"][inp["phase_id"] == pyxem_phase_id],
            direction='lab2crystal', degrees=False)
        print(f"shape rotations -----> {np.shape(rotations)}")

        for idx in np.arange(0, len(PROJECTION_VECTORS)):
            point_group = get_point_group(space_group, proper=False)
            ipf_key = plot.IPFColorKeyTSL(
                point_group.laue, direction=PROJECTION_VECTORS[idx])
            img = get_ipfdir_legend(ipf_key)

            rgb_px_with_phase_id = np.asarray(np.asarray(
                ipf_key.orientation2color(rotations) * 255., np.uint32), np.uint8)
            print(f"shape rgb_px_with_phase_id -----> {np.shape(rgb_px_with_phase_id)}")

            ipf_rgb_map = np.asarray(np.asarray(
                np.zeros((inp["n_z"] * inp["n_y"] * inp["n_x"], 3)) * 255., np.uint32), np.uint8)
            # background is black instead of white (which would be more pleasing)
            # but IPF color maps have a whitepoint which encodes in fact an orientation
            # and because of that we may have a single crystal with an orientation
            # close to the whitepoint which become a fully white seemingly "empty" image
            ipf_rgb_map[inp["phase_id"] == pyxem_phase_id, :] = rgb_px_with_phase_id
            ipf_rgb_map = np.reshape(
                ipf_rgb_map, (inp["n_z"], inp["n_y"], inp["n_x"], 3), order="C")
            # 0 is z, 1 is y, while 2 is x !

            trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing" \
                  f"/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{pyxem_phase_id}]" \
                  f"/MS_IPF[ipf{idx + 1}]"
            template[f"{trg}/projection_direction"] \
                = np.asarray(PROJECTION_VECTORS[idx].data.flatten(), np.float32)

            # add the IPF color map
            mpp = f"{trg}/DATA[map]"
            template[f"{mpp}/title"] \
                = f"Inverse pole figure {PROJECTION_DIRECTIONS[idx][0]} {phase_name}"
            template[f"{mpp}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{mpp}/@signal"] = "data"
            dims = ["x", "y", "z"]
            template[f"{mpp}/@axes"] = []
            for dim in dims[::-1]:
                template[f"{mpp}/@axes"].append(f"axis_{dim}")
            enum = 0
            for dim in dims:
                template[f"{mpp}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(enum)
                enum += 1
            template[f"{mpp}/DATA[data]"] = {"compress": ipf_rgb_map, "strength": 1}
            hfive_web_decorate_nxdata(f"{mpp}/DATA[data]", template)

            scan_unit = inp["s_unit"]  # TODO::this is not necessarily correct
            # could be a scale-invariant synthetic microstructure whose simulation
            # would work on multiple length-scales as atoms are not resolved directly!
            if scan_unit == "um":
                scan_unit = "µm"
            for dim in dims:
                template[f"{mpp}/AXISNAME[axis_{dim}]"] \
                    = {"compress": self.get_named_axis(inp, f"{dim}"), "strength": 1}
                template[f"{mpp}/AXISNAME[axis_{dim}]/@long_name"] \
                    = f"Coordinate along {dim}-axis ({scan_unit})"
                template[f"{mpp}/AXISNAME[axis_{dim}]/@units"] = f"{scan_unit}"

            # add the IPF color map legend/key
            lgd = f"{trg}/DATA[legend]"
            template[f"{lgd}/title"] \
                = f"Inverse pole figure {PROJECTION_DIRECTIONS[idx][0]} {phase_name}"
            # template[f"{trg}/title"] = f"Inverse pole figure color key with SST"
            template[f"{lgd}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{lgd}/@signal"] = "data"
            template[f"{lgd}/@axes"] = []
            dims = ["x", "y"]
            for dim in dims[::-1]:
                template[f"{lgd}/@axes"].append(f"axis_{dim}")
            enum = 0
            for dim in dims:
                template[f"{lgd}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(enum)
                enum += 1
            template[f"{lgd}/data"] = {"compress": img, "strength": 1}
            hfive_web_decorate_nxdata(f"{lgd}/data", template)

            dims = [("x", 1), ("y", 0)]
            for dim in dims:
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]"] \
                    = {"compress": np.asarray(np.linspace(0,
                                                          np.shape(img)[dim[1]] - 1,
                                                          num=np.shape(img)[dim[1]],
                                                          endpoint=True), np.uint32),
                       "strength": 1}
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]/@long_name"] \
                    = f"Pixel along {dim[0]}-axis"
                template[f"{lgd}/AXISNAME[axis_{dim[0]}]/@units"] = "px"
        return template
