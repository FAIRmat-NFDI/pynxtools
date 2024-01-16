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

import os
import numpy as np
# from typing import Dict, Any, List
from PIL import Image as pil
from orix import plot
from orix.quaternion import Rotation
from orix.quaternion.symmetry import get_point_group
from orix.vector import Vector3d

from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset
from pynxtools.dataconverter.readers.em.utils.hfive_web_constants \
    import HFIVE_WEB_MAXIMUM_ROI, HFIVE_WEB_MAXIMUM_RGB
from pynxtools.dataconverter.readers.em.utils.hfive_web_utils \
    import hfive_web_decorate_nxdata
from pynxtools.dataconverter.readers.em.utils.image_processing import thumbnail
from pynxtools.dataconverter.readers.em.utils.get_sqr_grid import \
    get_scan_points_with_mark_data_discretized_on_sqr_grid
from pynxtools.dataconverter.readers.em.utils.get_scan_points import \
    square_grid, hexagonal_grid, threed, get_scan_point_axis_values, get_scan_point_coords

from pynxtools.dataconverter.readers.em.subparsers.hfive_oxford import HdfFiveOxfordReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_bruker import HdfFiveBrukerEspritReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_edax import HdfFiveEdaxOimAnalysisReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_apex import HdfFiveEdaxApexReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_ebsd import HdfFiveCommunityReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_emsoft import HdfFiveEmSoftReader
from pynxtools.dataconverter.readers.em.subparsers.hfive_dreamthreed import HdfFiveDreamThreedReader
from pynxtools.dataconverter.readers.em.concepts.nxs_image_r_set import NxImageRealSpaceSet


PROJECTION_VECTORS = [Vector3d.xvector(), Vector3d.yvector(), Vector3d.zvector()]
PROJECTION_DIRECTIONS = [("X", Vector3d.xvector().data.flatten()),
                         ("Y", Vector3d.yvector().data.flatten()),
                         ("Z", Vector3d.zvector().data.flatten())]


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
        self.id_mgn = {"event": 1,
                       "event_img": 1,
                       "event_spc": 1,
                       "roi": 1,
                       "eds_img": 1}
        self.cache = {"is_filled": False}

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
        self.process_roi_eds_spectra(inp, template)
        self.process_roi_eds_maps(inp, template)

        return template

    def get_named_axis(self, inp: dict, dim_name: str):
        # Return scaled but not offset-calibrated scan point coordinates along dim.
        # TODO::remove!
        if square_grid(inp) is True or hexagonal_grid(inp) is True:
            # TODO::this code does not work for scaled and origin-offset scan point positions!
            # TODO::below formula is only the same for sqr and hex grid if
            # s_{dim_name} already accounts for the fact that typically s_y = sqrt(3)/2 s_x !
            return np.asarray(np.linspace(0,
                                          inp[f"n_{dim_name}"] - 1,
                                          num=inp[f"n_{dim_name}"],
                                          endpoint=True) * inp[f"s_{dim_name}"], np.float32)
        return None

    def process_roi_overview(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd") and inp[ckey] != {}:
                self.process_roi_overview_ebsd_based(
                    inp[ckey], ckey.replace("ebsd", ""), template)
                # break  # only one roi for now
            if ckey.startswith("eds_roi") and inp[ckey] != {}:
                self.process_roi_overview_eds_based(
                    inp[ckey], template)
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

    def process_roi_overview_eds_based(self,
                                       inp,
                                       template: dict) -> dict:
        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"IMAGE_R_SET[image_r_set{self.id_mgn['event_img']}]/DATA[image_twod]"
        template[f"{trg}/@NX_class"] = "NXdata"  # TODO::should be autodecorated
        template[f"{trg}/description"] = inp.tmp["source"]
        template[f"{trg}/title"] = f"Region-of-interest overview image"
        template[f"{trg}/@signal"] = "intensity"
        dims = [("x", 0), ("y", 1)]
        template[f"{trg}/@axes"] = []
        for dim in dims[::-1]:
            template[f"{trg}/@axes"].append(f"axis_{dim[0]}")
        template[f"{trg}/intensity"] \
            = {"compress": inp.tmp["image_twod/intensity"].value, "strength": 1}
        template[f"{trg}/intensity/@long_name"] = f"Signal"
        for dim in dims:
            template[f"{trg}/@AXISNAME_indices[axis_{dim[0]}_indices]"] \
                = np.uint32(dim[1])
            template[f"{trg}/AXISNAME[axis_{dim[0]}]"] \
                = {"compress": inp.tmp[f"image_twod/axis_{dim[0]}"].value, "strength": 1}
            template[f"{trg}/AXISNAME[axis_{dim[0]}]/@long_name"] \
                = inp.tmp[f"image_twod/axis_{dim[0]}@long_name"].value
        self.id_mgn["event_img"] += 1
        self.id_mgn["event"] += 1
        return template

    def process_roi_ebsd_maps(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("ebsd") and inp[ckey] != {}:
                if ckey.replace("ebsd", "").isdigit():
                    roi_id = int(ckey.replace("ebsd", ""))
                    if threed(inp[ckey]) is False:
                        self.onthefly_process_roi_ipfs_phases_twod(inp[ckey], roi_id, template)
                    else:
                        self.onthefly_process_roi_ipfs_phases_threed(inp[ckey], roi_id, template)
        return template

    def onthefly_process_roi_ipfs_phases_twod(self,
                                              inp: dict,
                                              roi_id: int,
                                              template: dict) -> dict:
        dimensionality = inp["dimensionality"]
        print(f"Parse crystal_structure_models aka phases {dimensionality}D version...")
        nxem_phase_id = 0
        prfx = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing"
        # bookkeeping is always reported for the original grid
        # because the eventual discretization for h5web is solely
        # for the purpose of showing users a readily consumable default plot
        # to judge for each possible dataset in the same way if the
        # dataset is worthwhile and potentially valuable for ones on research
        n_pts = inp["n_x"] * inp["n_y"]
        n_pts_indexed = np.sum(inp["phase_id"] != 0)
        print(f"n_pts {n_pts}, n_pts_indexed {n_pts_indexed}")
        template[f"{prfx}/number_of_scan_points"] = np.uint32(n_pts)
        template[f"{prfx}/indexing_rate"] = np.float64(100. * n_pts_indexed / n_pts)
        template[f"{prfx}/indexing_rate/@units"] = f"%"
        grp_name = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]"
        template[f"{grp_name}/number_of_scan_points"] \
            = np.uint32(np.sum(inp["phase_id"] == 0))
        template[f"{grp_name}/phase_identifier"] = np.uint32(nxem_phase_id)
        template[f"{grp_name}/phase_name"] = f"notIndexed"

        print(f"----unique inp phase_id--->{np.unique(inp['phase_id'])}")
        for nxem_phase_id in np.arange(1, np.max(np.unique(inp["phase_id"])) + 1):
            # starting here at ID 1 because the subpasrsers have already normalized the
            # tech partner specific phase_id convention to follow NXem NeXus convention
            print(f"inp[phases].keys(): {inp['phases'].keys()}")
            if nxem_phase_id not in inp["phases"].keys():
                raise ValueError(f"{nxem_phase_id} is not a key in inp['phases'] !")
            trg = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]"
            template[f"{trg}/number_of_scan_points"] \
                = np.uint32(np.sum(inp["phase_id"] == nxem_phase_id))
            template[f"{trg}/phase_identifier"] = np.uint32(nxem_phase_id)
            template[f"{trg}/phase_name"] \
                = f"{inp['phases'][nxem_phase_id]['phase_name']}"
            # internally the following function may discretize a coarser IPF
            # if the input grid inp is too large for h5web to display
            # this remove fine details in the EBSD maps but keep in mind
            # that the purpose of the default plot is to guide the user
            # of the potential usefulness of the dataset when searching in
            # a RDMS like NOMAD OASIS, the purpose is NOT to take the coarse-grained
            # discretization and use this for scientific data analysis!
            self.process_roi_phase_ipfs_twod(inp,
                                             roi_id,
                                             nxem_phase_id,
                                             inp["phases"][nxem_phase_id]["phase_name"],
                                             inp["phases"][nxem_phase_id]["space_group"],
                                             template)
        return template

    def process_roi_phase_ipfs_twod(self,
                                    inp: dict,
                                    roi_id: int,
                                    nxem_phase_id: int,
                                    phase_name: str,
                                    space_group: int,
                                    template: dict) -> dict:
        print(f"Generate 2D IPF maps for {nxem_phase_id}, {phase_name}...")
        trg_grid \
            = get_scan_points_with_mark_data_discretized_on_sqr_grid(inp, HFIVE_WEB_MAXIMUM_RGB)

        rotations = Rotation.from_euler(
            euler=trg_grid["euler"][trg_grid["phase_id"] == nxem_phase_id],
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
                np.zeros((trg_grid["n_y"] * trg_grid["n_x"], 3)) * 255., np.uint32), np.uint8)
            # background is black instead of white (which would be more pleasing)
            # but IPF color maps have a whitepoint which encodes in fact an orientation
            # and because of that we may have a map from a single crystal characterization
            # whose orientation could be close to the whitepoint which becomes a fully white
            # seemingly "empty" image, therefore we use black as empty, i.e. white reports an
            # orientation
            ipf_rgb_map[trg_grid["phase_id"] == nxem_phase_id, :] = rgb_px_with_phase_id
            ipf_rgb_map = np.reshape(ipf_rgb_map, (trg_grid["n_y"], trg_grid["n_x"], 3), order="C")
            # 0 is y, 1 is x, only valid for REGULAR_TILING and FLIGHT_PLAN !

            trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing" \
                  f"/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]" \
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

            scan_unit = trg_grid["s_unit"]  # TODO::this is not necessarily correct
            # could be a scale-invariant synthetic microstructure whose simulation
            # would work on multiple length-scales as atoms are not resolved directly!
            if scan_unit == "um":
                scan_unit = "µm"
            for dim in dims:
                template[f"{mpp}/AXISNAME[axis_{dim}]"] \
                    = {"compress": self.get_named_axis(trg_grid, f"{dim}"), "strength": 1}
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

            dims_idxs = {"x": 1, "y": 0}
            for dim, idx in dims_idxs.items():
                template[f"{lgd}/AXISNAME[axis_{dim}]"] \
                    = {"compress": np.asarray(np.linspace(0,
                                                          np.shape(img)[idx] - 1,
                                                          num=np.shape(img)[idx],
                                                          endpoint=True), np.uint32),
                       "strength": 1}
                template[f"{lgd}/AXISNAME[axis_{dim}]/@long_name"] \
                    = f"Pixel along {dim[0]}-axis"
                template[f"{lgd}/AXISNAME[axis_{dim}]/@units"] = "px"
        return template

    def onthefly_process_roi_ipfs_phases_threed(self,
                                                inp: dict,
                                                roi_id: int,
                                                template: dict) -> dict:
        # this function is almost the same as its twod version we keep it for
        # now an own function until the rediscretization also works for the 3D grid
        dimensionality = inp["dimensionality"]
        print(f"Parse crystal_structure_models aka phases {dimensionality}D version...")
        # see comments in twod version of this function
        nxem_phase_id = 0
        prfx = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing"
        n_pts = inp["n_x"] * inp["n_y"] * inp["n_z"]
        n_pts_indexed = np.sum(inp["phase_id"] != 0)
        print(f"n_pts {n_pts}, n_pts_indexed {n_pts_indexed}")
        template[f"{prfx}/number_of_scan_points"] = np.uint32(n_pts)
        template[f"{prfx}/indexing_rate"] = np.float64(100. * n_pts_indexed / n_pts)
        template[f"{prfx}/indexing_rate/@units"] = f"%"
        grp_name = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]"
        template[f"{grp_name}/number_of_scan_points"] \
            = np.uint32(np.sum(inp["phase_id"] == 0))
        template[f"{grp_name}/phase_identifier"] = np.uint32(nxem_phase_id)
        template[f"{grp_name}/phase_name"] = f"notIndexed"

        print(f"----unique inp phase_id--->{np.unique(inp['phase_id'])}")
        for nxem_phase_id in np.arange(1, np.max(np.unique(inp["phase_id"])) + 1):
            print(f"inp[phases].keys(): {inp['phases'].keys()}")
            if nxem_phase_id not in inp["phases"].keys():
                raise ValueError(f"{nxem_phase_id} is not a key in inp['phases'] !")
            trg = f"{prfx}/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]"
            template[f"{trg}/number_of_scan_points"] \
                = np.uint32(np.sum(inp["phase_id"] == nxem_phase_id))
            template[f"{trg}/phase_identifier"] = np.uint32(nxem_phase_id)
            template[f"{trg}/phase_name"] \
                = f"{inp['phases'][nxem_phase_id]['phase_name']}"

            self.process_roi_phase_ipfs_threed(inp,
                                               roi_id,
                                               nxem_phase_id,
                                               inp["phases"][nxem_phase_id]["phase_name"],
                                               inp["phases"][nxem_phase_id]["space_group"],
                                               template)
        return template

    def process_roi_phase_ipfs_threed(self,
                                      inp: dict,
                                      roi_id: int,
                                      nxem_phase_id: int,
                                      phase_name: str,
                                      space_group: int,
                                      template: dict) -> dict:
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
        print(f"Generate 3D IPF map for {nxem_phase_id}, {phase_name}...")
        rotations = Rotation.from_euler(
            euler=inp["euler"][inp["phase_id"] == nxem_phase_id],
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
            ipf_rgb_map[inp["phase_id"] == nxem_phase_id, :] = rgb_px_with_phase_id
            ipf_rgb_map = np.reshape(
                ipf_rgb_map, (inp["n_z"], inp["n_y"], inp["n_x"], 3), order="C")
            # 0 is z, 1 is y, while 2 is x !

            trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{roi_id}]/ebsd/indexing" \
                  f"/EM_EBSD_CRYSTAL_STRUCTURE_MODEL[phase{nxem_phase_id}]" \
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

            dims_idxs = {"x": 1, "y": 0}
            for dim, idx in dims_idxs.items():
                template[f"{lgd}/AXISNAME[axis_{dim}]"] \
                    = {"compress": np.asarray(np.linspace(0,
                                                          np.shape(img)[idx] - 1,
                                                          num=np.shape(img)[idx],
                                                          endpoint=True), np.uint32),
                       "strength": 1}
                template[f"{lgd}/AXISNAME[axis_{dim}]/@long_name"] \
                    = f"Pixel along {dim}-axis"
                template[f"{lgd}/AXISNAME[axis_{dim}]/@units"] = "px"
        return template

    def process_roi_eds_spectra(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("eds_spc") and inp[ckey] != {}:
                trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
                      f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
                      f"SPECTRUM_SET[spectrum_set{self.id_mgn['event_spc']}]/" \
                      f"DATA[spectrum_zerod]"
                # TODO::check if its a spectrum_zerod !!!
                template[f"{trg}/@NX_class"] = "NXdata"  # TODO::should be autodecorated
                template[f"{trg}/description"] = inp[ckey].tmp["source"]
                template[f"{trg}/title"] = f"Region-of-interest overview image"
                template[f"{trg}/@signal"] = "intensity"
                template[f"{trg}/@axes"] = ["axis_energy"]
                template[f"{trg}/intensity"] \
                    = {"compress": inp[ckey].tmp["spectrum_zerod/intensity"].value,
                       "strength": 1}
                template[f"{trg}/intensity/@long_name"] \
                    = inp[ckey].tmp["spectrum_zerod/intensity@long_name"].value  # f"Signal"
                template[f"{trg}/@AXISNAME_indices[axis_energy_indices]"] = np.uint32(0)
                template[f"{trg}/AXISNAME[axis_energy]"] \
                    = {"compress": inp[ckey].tmp[f"spectrum_zerod/axis_energy"].value,
                       "strength": 1}
                template[f"{trg}/AXISNAME[axis_energy]/@long_name"] \
                    = inp[ckey].tmp[f"spectrum_zerod/axis_energy@long_name"].value
                self.id_mgn["event_spc"] += 1
                self.id_mgn["event"] += 1
        return template

    def process_roi_eds_maps(self, inp: dict, template: dict) -> dict:
        for ckey in inp.keys():
            if ckey.startswith("eds_map") and inp[ckey] != {}:
                trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{self.id_mgn['roi']}]/" \
                      f"eds/indexing"
                template[f"{trg}/source"] = inp[ckey].tmp["source"]
                for img in inp[ckey].tmp["IMAGE_R_SET"]:
                    if not isinstance(img, NxImageRealSpaceSet):
                        continue
                    trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{self.id_mgn['roi']}]/eds/" \
                          f"indexing/IMAGE_R_SET[image_r_set{self.id_mgn['eds_img']}]"
                    template[f"{trg}/source"] = img.tmp["source"]
                    template[f"{trg}/description"] = img.tmp["description"]
                    template[f"{trg}/energy_range"] = img.tmp["energy_range"].value
                    template[f"{trg}/energy_range/@units"] = img.tmp["energy_range"].unit
                    template[f"{trg}/iupac_line_candidates"] = img.tmp["iupac_line_candidates"]
                    template[f"{trg}/@NX_class"] = "NXdata"  # TODO::should be autodecorated
                    template[f"{trg}/@signal"] = "intensity"
                    template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
                    template[f"{trg}/title"] = f"EDS map {img.tmp['description']}"
                    template[f"{trg}/intensity"] \
                        = {"compress": img.tmp["image_twod/intensity"].value,
                           "strength": 1}
                    template[f"{trg}/intensity/@long_name"] = f"Signal"
                    dims = [("x", 0), ("y", 1)]
                    for dim in dims:
                        template[f"{trg}/@AXISNAME_indices[axis_{dim[0]}_indices]"] \
                            = np.uint32(dim[1])
                        template[f"{trg}/AXISNAME[axis_{dim[0]}]"] \
                            = {"compress": img.tmp[f"image_twod/axis_{dim[0]}"].value,
                               "strength": 1}
                        template[f"{trg}/AXISNAME[axis_{dim[0]}]/@long_name"] \
                            = img.tmp[f"image_twod/axis_{dim[0]}@long_name"].value
                    self.id_mgn["eds_img"] += 1
                self.id_mgn["roi"] += 1

        return template
