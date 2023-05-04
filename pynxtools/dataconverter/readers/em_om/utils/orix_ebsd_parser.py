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
"""Parse H5OINA and create IPF color map default plots using the pyxem/orix library."""

# pylint: disable=no-member,duplicate-code,unsubscriptable-object,comparison-with-callable

# https://orix.readthedocs.io/en/stable/tutorials/inverse_pole_figures.html

# type: ignore

import os

from typing import Dict, Any, List

import matplotlib.pyplot as plt

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

from pynxtools.dataconverter.readers.em_om.utils.image_transform import thumbnail

from pynxtools.dataconverter.readers.em_om.utils.em_nexus_plots import HFIVE_WEB_MAX_SIZE

orix_params = {
    "figure.facecolor": "w",
    "figure.figsize": (8, 8),
    "lines.markersize": 10,
    "font.size": 15,
    "axes.grid": True,
}  # 20, 7),
plt.rcParams.update(orix_params)

# https://orix.readthedocs.io/ for details about the orix lib
# https://www.diffpy.org/diffpy.structure/package.html for details about the diffpy lib


class NxEmOmOrixEbsdParser:
    """Parse *.h5oina EBSD data.

    """

    def __init__(self, file_name, entry_id):
        """Class wrapping pyxem/orix H5OINA parser."""
        # this is one example which should be extended to kikuchipy but this should
        # be done together with Hakon and Knut Marthinsen's team or the pyxem developers
        # the reason why I went for a standalone parser was that kikuchipy v0.7.0 which
        # I had available when implementing this example was that *.h5oina files
        # were forced to have Kikuchi pattern in them. However, in *.h5oina the patterns
        # are optional and this was also the situation for the example file
        # which the EBSD system technology partner Oxford Instrument provided to me
        self.file_names = file_name
        self.entry_id = entry_id
        self.oina_version_identifier = "5.0"
        self.xaxis: List[float] = []
        self.yaxis: List[float] = []
        self.xmap = CrystalMap
        self.oina: Dict[str, Any] = {"n_slices": 1,
                                     "rotation": Rotation,
                                     "scan_point_x": [],
                                     "scan_point_y": [],
                                     "phase_identifier": [],
                                     "band_contrast": [],
                                     "scan_size": [0, 0],
                                     "scan_step": [0., 0.],
                                     "scan_unit": ["n/a", "n/a"],
                                     "phase": [],
                                     "space_group": []}
        # y (aka height), x (aka width) !

    def parse_h5oina(self, slice_id):
        """Parse content from *.h5oina format."""
        # https://github.com/oinanoanalysis/h5oina/blob/master/H5OINAFile.md
        # here implementing version 5.0
        # in this implementation we load all data in main memory, for stream processing
        # when the data are really large one would rather load the data array metadata
        # dtype, size, shape and use lazy loading instead or successive loading
        # file_names is file name
        h5r = h5py.File(self.file_names, "r")
        self.oina_version_identifier = h5r["/Format Version"][0].decode("utf-8")
        self.oina["n_slices"] = h5r["/Index"][0]
        print(f"H5OINA v{self.oina_version_identifier} has {self.oina['n_slices']} slices")
        if self.oina_version_identifier != "5.0" or self.oina["n_slices"] != 1:
            print("This examples supports H5OINA only in version 5.0 with one slice!")
            return

        self.parse_h5oina_ebsd_data(h5r, slice_id)
        self.parse_h5oina_ebsd_header(h5r, slice_id)

        group_names = []
        group_name = f"/{slice_id}/EBSD/Header/Phases"
        if group_name in h5r:
            group_names = sorted(list(h5r[group_name].keys()), key=int)
        for name in group_names:
            self.parse_h5oina_phase(h5r, slice_id, name)

        h5r.close()
        self.generate_xmap()

    def parse_h5oina_ebsd_data(self, h5r, slice_id):
        """Parse EBSD data section for specific slice."""
        group_name = f"/{slice_id}/EBSD/Data"
        # required entries in v5.0
        dset_name = f"{group_name}/Euler"
        if dset_name in h5r:
            self.oina["rotation"] = Rotation.from_euler(euler=h5r[dset_name],
                                                        direction='lab2crystal',
                                                        degrees=False)  # rad in v5.0
        dset_name = f"{group_name}/Phase"
        if dset_name in h5r:
            self.oina["phase_identifier"] = np.asarray(h5r[dset_name], np.int32)

        # optional entries in v5.0
        dset_name = f"{group_name}/X"  # v5.0, top-left-corner µm
        if dset_name in h5r:
            self.oina["scan_point_x"] = np.asarray(h5r[dset_name], np.float32)
        dset_name = f"{group_name}/Y"  # v5.0, top-left-corner µm
        if dset_name in h5r:
            self.oina["scan_point_y"] = np.asarray(h5r[dset_name], np.float32)
        dset_name = f"{group_name}/Band Contrast"
        if dset_name in h5r:  # is not required but should how else to create a ROI image
            self.oina["band_contrast"] = np.asarray(h5r[dset_name], np.uint8)

    def parse_h5oina_ebsd_header(self, h5r, slice_id):
        """Parse EBSD header section for specific slice."""
        group_name = f"/{slice_id}/EBSD/Header"
        dset_name = f"{group_name}/Y Cells"  # v5.0 height of the map
        if dset_name in h5r:
            self.oina["scan_size"][0] = h5r[dset_name][0]
        dset_name = f"{group_name}/X Cells"  # v5.0 width of the map
        if dset_name in h5r:
            self.oina["scan_size"][1] = h5r[dset_name][0]
        dset_name = f"{group_name}/Y Step"  # v5.0, µm
        if dset_name in h5r:
            dst_y = h5r[dset_name]
            self.oina["scan_step"][0] = dst_y[0]
            if "Unit" in dst_y.attrs:
                self.oina["scan_unit"][0] = dst_y.attrs["Unit"]
        dset_name = f"{group_name}/X Step"  # v5.0, µm
        if dset_name in h5r:
            dst_x = h5r[dset_name]
            self.oina["scan_step"][1] = dst_x[0]
            if "Unit" in dst_x.attrs:
                self.oina["scan_unit"][1] = dst_x.attrs["Unit"]
        # ##MK:: check that all data in the self.oina are consistent

    def parse_h5oina_phase(self, h5r, slice_id, name):
        """Parse one phase."""
        print(f"Loading phase {name}...")
        # required in v5.0
        sub_group_name = f"/{slice_id}/EBSD/Header/Phases/{name}"
        dset_name = f"{sub_group_name}/Phase Name"
        if dset_name in h5r:
            phase_name = h5r[dset_name][0].decode("utf-8")
        # "Reference", but even examples from Oxford place no DOIs here
        dset_name = f"{sub_group_name}/Lattice Angles"
        if dset_name in h5r:
            alpha_beta_gamma = np.asarray(h5r[dset_name][:].flatten()) / np.pi * 180.
            # rad2deg
        dset_name = f"{sub_group_name}/Lattice Dimensions"
        if dset_name in h5r:
            a_b_c = np.asarray(h5r[dset_name][:].flatten()) * 0.1
            # angstroem2nm

        # optional in v5.0
        # many inconsistencies and metadata cluttering by design across
        # tools of the community and of technology partners:
        # e.g. MTex uses point group required, Oxford uses space group but
        # optional, neither of them store atom positions and
        # computed intensities because for this there are other files...
        dset_name = f"{sub_group_name}/Space Group"
        if dset_name in h5r:
            space_group = int(h5r[dset_name][0])
            self.oina["space_group"].append(space_group)

        self.oina["phase"].append(
            Structure(title=phase_name,
                      atoms=None,
                      lattice=Lattice(a_b_c[0], a_b_c[1], a_b_c[2],
                                      alpha_beta_gamma[0],
                                      alpha_beta_gamma[1],
                                      alpha_beta_gamma[2])))

    def generate_xmap(self):
        """Generate the orientation map and orix/diffsims data structures."""
        coordinates, _ = create_coordinate_arrays(
            (self.oina["scan_size"][0], self.oina["scan_size"][1]),
            (self.oina["scan_step"][0], self.oina["scan_step"][1]))
        self.xaxis = coordinates["x"]
        self.yaxis = coordinates["y"]
        del coordinates

        # orix expects non-indexed scan points to have phase_id -1
        # while H5OINA v5.0 specifies that such points have phase ID 0
        # H5OINA v5.0 specifies further one subgroup per phase
        # phase_identifier starting at 1, as non-indexed points do not belong to a phase
        self.oina["phase_identifier"] = self.oina["phase_identifier"] - 1
        print(np.unique(self.oina["phase_identifier"]))

        self.xmap = CrystalMap(rotations=self.oina["rotation"],
                               x=self.xaxis, y=self.yaxis,
                               phase_id=self.oina["phase_identifier"],
                               phase_list=PhaseList(space_groups=self.oina["space_group"],
                                                    structures=self.oina["phase"]),
                               prop={"bc": self.oina["band_contrast"]},
                               scan_unit=self.oina["scan_unit"])
        print(self.xmap)

    def parse_roi_default_plot(self, template: dict) -> dict:
        """Parse data for the region-of-interest default plot."""
        print("Parse ROI default plot...")
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/region_of_interest"
        template[f"{trg}/descriptor"] = str("normalized_band_contrast")
        # ##MK:: need a better strategy here because the descriptor
        # band contrast is not a required field in v5.0,
        # thus it should not be hardcoded and assumed that it is present
        # but there is also no other field in v5.0 that could stand in as a descriptor

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/region_of_interest/roi"
        template[f"{trg}/title"] = str("Region-of-interest overview image")
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/region_of_interest/roi/data"
        template[f"{trg}"] = {"compress": np.reshape(
            np.asarray(np.asarray((self.xmap.bc / np.max(self.xmap.bc) * 255.),
                       np.uint32), np.uint8), (self.xmap.shape[0], self.xmap.shape[1]),
            order="C"), "strength": 1}
        # 0 is y while 1 is x !
        template[f"{trg}/@long_name"] = "Signal"
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/region_of_interest/roi/axis_x"
        template[f"{trg}"] = {"compress": np.asarray(
            0.5 * self.oina["scan_step"][1] + self.xaxis[0:self.xmap.shape[1]],
            np.float32), "strength": 1}
        template[f"{trg}/@long_name"] \
            = f"Calibrated coordinate along x-axis ({self.oina['scan_unit'][1]})"
        template[f"{trg}/@units"] = self.oina["scan_unit"][1]

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/region_of_interest/roi/axis_y"
        template[f"{trg}"] = {"compress": np.asarray(
            0.5 * self.oina["scan_step"][0] + self.yaxis[0:self.xmap.size:self.xmap.shape[1]],
            np.float32), "strength": 1}
        template[f"{trg}/@long_name"] \
            = f"Calibrated coordinate along y-axis ({self.oina['scan_unit'][0]})"
        template[f"{trg}/@units"] = self.oina["scan_unit"][0]
        return template

    def parse_phases(self, template: dict) -> dict:
        """Parse data for the crystal structure models aka phases."""
        print("Parse crystal_structure_models aka phases...")
        identifier = 1
        # identifier match because phase is a list asc. sorted by numerical keys
        for phase in self.oina["phase"]:
            trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
                  f"EM_EBSD_CRYSTAL_STRUCTURE_MODEL" \
                  f"[em_ebsd_crystal_structure_model{identifier}]"
            template[f"{trg}/phase_identifier"] = np.uint32(identifier)
            template[f"{trg}/phase_name"] = str(phase.title)
            template[f"{trg}/unit_cell_abc"] = np.asarray(
                [phase.lattice.a, phase.lattice.b, phase.lattice.c],
                np.float32)
            template[f"{trg}/unit_cell_abc/@units"] = "nm"
            template[f"{trg}/unit_cell_alphabetagamma"] = np.asarray(
                [phase.lattice.alpha, phase.lattice.beta, phase.lattice.gamma],
                np.float32)
            template[f"{trg}/unit_cell_alphabetagamma/@units"] = "°"
            identifier += 1
        return template

    def parse_inverse_pole_figures(self, template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings."""
        print("Parse inverse pole figures (IPFs)...")
        print(len(self.oina["phase"]))
        # identifier match because phase is a list asc. sorted by numerical keys
        for identifier in np.arange(0, np.max(self.xmap.phase_id) + 1):
            self.parse_inverse_pole_figure_map(identifier, template)
            self.parse_inverse_pole_figure_color_key(identifier, template)
            identifier += 1

        return template

    def parse_inverse_pole_figure_map(self, identifier, template: dict) -> dict:
        """Parse and create inverse-pole-figure (IPF) mappings on their color models."""
        # +1 because for orix not_indexed -1 and "first" phase has ID 0 !
        phase_id = identifier + 1
        phase_name = self.xmap.phases[identifier].name
        print(f"Generate inverse pole figure (IPF) map for {identifier}, {phase_name}...")

        phase_id_ipf_key = plot.IPFColorKeyTSL(
            self.xmap.phases[identifier].point_group.laue,
            direction=Vector3d.zvector())

        rgb_px_with_phase_id = np.asarray(
            np.asarray(phase_id_ipf_key.orientation2color(
                self.xmap[phase_name].rotations) * 255., np.uint32), np.uint8)

        ipf_rgb_map = np.asarray(
            np.uint8(np.zeros((self.xmap.shape[0] * self.xmap.shape[1], 3)) * 255.0))
        # background is black instead of white (which would be more pleasing)
        # but IPF color maps have a whitepoint which encodes in fact an orientation
        # and because of that we may have a single crystal with an orientation
        # close to the whitepoint which become a fully white seemingly "empty" image
        ipf_rgb_map[self.xmap.phase_id == identifier, :] = rgb_px_with_phase_id
        ipf_rgb_map = np.reshape(ipf_rgb_map,
                                 (self.xmap.shape[0], self.xmap.shape[1], 3),
                                 order="C")  # 0 is y while 1 is x !

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{phase_id}]"
        template[f"{trg}/bitdepth"] = np.uint32(8)
        template[f"{trg}/phase_identifier"] = np.uint32(phase_id)
        template[f"{trg}/phase_name"] = str(phase_name)
        template[f"{trg}/PROGRAM[program1]/program"] = str("orix")
        template[f"{trg}/PROGRAM[program1]/program/@version"] = orix.__version__
        template[f"{trg}/PROGRAM[program2]/program"] = str("diffsims")
        template[f"{trg}/PROGRAM[program2]/program/@version"] = diffsims.__version__
        template[f"{trg}/projection_direction"] = np.asarray([0., 0., 1.], np.float32)
        # should have a reference so that it is directly interpretable

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{phase_id}]/ipf_rgb_map"
        template[f"{trg}/title"] = str("Inverse pole figure color map")
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{phase_id}]/ipf_rgb_map/DATA[data]"
        template[f"{trg}"] = {"compress": ipf_rgb_map, "strength": 1}
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        # dimension scale axes value arrays same for each phase, entire IPF map
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{phase_id}]/ipf_rgb_map/axis_x"
        template[f"{trg}"] = {"compress": np.asarray(
            0.5 * self.oina["scan_step"][1] + self.xaxis[0:self.xmap.shape[1]],
            np.float32), "strength": 1}
        template[f"{trg}/@long_name"] \
            = f"Calibrated coordinate along x-axis ({self.oina['scan_unit'][1]})"
        template[f"{trg}/@units"] = self.oina["scan_unit"][1]

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{phase_id}]/ipf_rgb_map/axis_y"
        template[f"{trg}"] = {"compress": np.asarray(
            0.5 * self.oina["scan_step"][0]
            + self.yaxis[0:self.xmap.size:self.xmap.shape[1]],
            np.float32), "strength": 1}
        template[f"{trg}/@long_name"] \
            = f"Calibrated coordinate along y-axis ({self.oina['scan_unit'][0]})"
        template[f"{trg}/@units"] = self.oina["scan_unit"][0]

        return template

    def parse_inverse_pole_figure_color_key(self, identifier, template: dict) -> dict:
        """Parse color key renderings of inverse-pole-figure (IPF) mappings."""
        # +1 because for orix not_indexed -1 and "first" phase has ID 0 !
        phase_id = identifier + 1
        phase_name = self.xmap.phases[identifier].name
        print(f"Parse inverse pole figure (IPF) color key {identifier}, {phase_name}...")

        phase_id_ipf_key = plot.IPFColorKeyTSL(
            self.xmap.phases[identifier].point_group.laue,
            direction=Vector3d.zvector())

        # render domain-specific IPF color keys using orix
        fig = phase_id_ipf_key.plot(return_figure=True)
        fig.savefig("temporary.png", dpi=300, facecolor='w', edgecolor='w',
                    orientation='landscape', format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1, metadata=None)
        # constraint further to 8bit RGB and no flipping
        # im = np.asarray(imageio.v3.imread(symm_name))
        img = np.asarray(thumbnail(pil.open("temporary.png", "r", ["png"]),
                         size=HFIVE_WEB_MAX_SIZE), np.uint8)
        img = img[:, :, 0:3]  # discard alpha channel
        if os.path.exists("temporary.png"):
            os.remove("temporary.png")
        # ##MK::need to constrain more the writing of the image that it is guaranteed
        # a specific type of image and bitdepth and color model, and avoid implicit
        # image transformations such as flips or rotations

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model"
        template[f"{trg}/title"] = str("Inverse pole figure color key with SST")
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model/DATA[data]"
        template[f"{trg}"] = {"compress": img, "strength": 1}
        template[f"{trg}/@CLASS"] = "IMAGE"
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model/AXISNAME[axis_y]"
        template[f"{trg}"] = {"compress":
                              np.asarray(np.linspace(1,
                                                     np.shape(img)[0],
                                                     num=np.shape(img)[0],
                                                     endpoint=True), np.uint32),
                              "strength": 1}
        template[f"{trg}/@long_name"] = "Pixel along y-axis"
        template[f"{trg}/@units"] = "px"

        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model/AXISNAME[axis_x]"
        template[f"{trg}"] = {"compress":
                              np.asarray(np.linspace(1,
                                                     np.shape(img)[1],
                                                     num=np.shape(img)[1],
                                                     endpoint=True), np.uint32),
                              "strength": 1}
        template[f"{trg}/@long_name"] = "Pixel along x-axis"
        template[f"{trg}/@units"] = "px"

        return template

    def parse(self, template: dict) -> dict:
        """Parse NOMAD OASIS relevant data and metadata from an H5OINA file."""
        print("Parsing EBSD data pyxem/orix-style for an H5OINA example...")
        print(self.file_names)
        print(f"{self.entry_id}")
        self.parse_h5oina(1)
        self.parse_roi_default_plot(template)
        self.parse_phases(template)
        self.parse_inverse_pole_figures(template)
        return template
