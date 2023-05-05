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
"""Parse three-dimensional EBSD data from a DREAM3D file."""

# pylint: disable=no-member,too-many-instance-attributes

# type: ignore

# from typing import Dict, Any, List, Tuple

import yaml

import numpy as np

import h5py

# import imageio.v3 as iio
from PIL import Image as pil

# from pynxtools.dataconverter.readers.em_om.utils.dream3d_filter_class \
#     import DreamThreedFilter

from pynxtools.dataconverter.readers.em_om.utils.image_transform import thumbnail

from pynxtools.dataconverter.readers.em_om.utils.em_nexus_plots import HFIVE_WEB_MAX_SIZE


class NxEmOmDreamThreedEbsdParser:
    """Parse DREAM3D EBSD data.

    """

    def __init__(self, file_name, entry_id):
        """Class wrapping dream3d parser."""
        # this is one example which should be extended to interpretation of more
        # DREAM3D filter, currently though all these filter and the DREAM.3D software
        # experiences major refactoring associated with the introduction of DREAM3DNX
        self.file_name = file_name
        self.entry_id = entry_id
        self.pipeline = {}
        # the dictionary nest in DREAM.3D SIMPL pipeline notation
        self.stack_meta = {}
        self.stack = []
        self.roi = []
        self.xyz = {}
        self.phase_id = []
        self.phases = {}

    def parse_pipeline(self):
        """Parse and understand pipeline json description of the dream3d file."""
        h5r = h5py.File(self.file_name, "r")
        dsnm = "Pipeline/Pipeline"
        if dsnm in h5r:
            self.pipeline = yaml.safe_load(h5r[dsnm][()].decode("utf-8"))
        h5r.close()

        print(self.pipeline)
        # add all logical understanding of the pipeline steps
        # ##MK::should be extended

    def parse_roi_geometry(self):
        """Parse the geometry of the 3D dataset ##MK::assuming that it exists."""
        # NEW ISSUE: this is an example how to parse 3D reconstructed EBSD data
        # from the older version of DREAM.3D (not for DREAM.3D NX) maps on NXem_ebsd

        h5r = h5py.File(self.file_name, "r")

        grpnm = "/DataContainers/Small IN100/_SIMPL_GEOMETRY"
        # NEW ISSUE: interpret from filter!
        has_required_metadata = True
        has_correct_shape = True
        req_field_names = [("dims", "DIMENSIONS"),
                           ("origin", "ORIGIN"),
                           ("spacing", "SPACING")]
        for field_tuple in req_field_names:
            if f"{grpnm}/{field_tuple[1]}" in h5r:
                self.stack_meta[field_tuple[0]] = h5r[f"{grpnm}/{field_tuple[1]}"][...]
                if np.shape(self.stack_meta[field_tuple[0]]) != (3,):
                    has_correct_shape = False
            else:
                has_required_metadata = False

        if (has_required_metadata is True) and (has_correct_shape is True):
            grpnm = "/DataContainers/Small IN100/EBSD Scan Data"

            dsnm = f"{grpnm}/Phases"
            self.phase_id = np.asarray(h5r.get(dsnm)[...], np.uint32)
            # DREAM.3D stores int32_t but only >= 0 ##?, we can silently promote to uint32

            dsnm = f"{grpnm}/Image Quality"
            self.roi = np.asarray(h5r.get(dsnm)[...], np.float32)

            dsnm = f"{grpnm}/IPFColor"
            self.stack = np.asarray(h5r.get(dsnm)[...], np.uint8)  # RGB triplet
            # if len(np.shape(self.stack)) == 4:
            #     for i in np.arange(0, 3):
            #         if np.shape(self.stack)[i] >= 1:
            # if np.shape(self.stack)[3] == 3:
            print(np.shape(self.roi))
            print(np.shape(self.phase_id))
            print(np.shape(self.stack))

            # NEW ISSUE: more consistence checks that sizes and shapes match

        h5r.close()

    def parse_roi_dimension_scale_axes(self):
        """Create correctly calibrated dimension scale axes center-of-mass arrays."""
        axes_names = [(0, "x"), (1, "y"), (2, "z")]
        self.xyz = {}
        for axisname in axes_names:
            i = axisname[0]
            # self.xyz[axisname[1]] = np.asarray(np.linspace(self.stack_meta["origin"][i],
            #     self.stack_meta["origin"][i] + self.stack_meta["dims"][i] \
            #     * self.stack_meta["spacing"][i], num=self.stack_meta["dims"][i],
            #     endpoint=True), np.float32)  # DREAM.3D uses single precision
            self.xyz[axisname[1]] = np.asarray(
                np.linspace(self.stack_meta["origin"][i],
                            self.stack_meta["origin"][i] + self.stack_meta["dims"][i]
                            * self.stack_meta["spacing"][i], num=self.stack_meta["dims"][i],
                            endpoint=True),
                np.float32)  # DREAM.3D uses single precision

        # endpoint true? voxel center or its min or max bound?

    def parse_roi_default_plot(self, template: dict) -> dict:
        """Create default plot for the region-of-interest."""
        trg = f"/ENTRY[entry{self.entry_id}]/correlation/region_of_interest/roi"
        template[f"{trg}/title"] = str("Region-of-interest overview image")
        template[f"{trg}/@signal"] = "data"
        # template[f"{trg}/@axes"] = ["axis_x", "axis_y", "axis_z"]
        template[f"{trg}/@axes"] = ["axis_z", "axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        template[f"{trg}/@AXISNAME_indices[axis_z_indices]"] = np.uint32(2)

        trg = f"/ENTRY[entry{self.entry_id}]/correlation/region_of_interest/roi/data"
        template[f"{trg}"] = {"compress": self.roi[:, :, :, 0], "strength": 1}

        template[f"{trg}/@long_name"] = "Signal"
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = [("axis_x", "x"), ("axis_y", "y"), ("axis_z", "z")]
        for axisname in axes_names:
            trg = f"/ENTRY[entry{self.entry_id}]/correlation/region_of_interest" \
                  f"/roi/AXISNAME[{axisname[0]}]"
            template[f"{trg}"] = {"compress": self.xyz[axisname[1]], "strength": 1}
            template[f"{trg}/@long_name"] \
                = f"Calibrated position along {axisname[1]}-axis (µm)"
            template[f"{trg}/@units"] = "µm"  # parse from filter!

        return template

    def parse_phases(self, template: dict) -> dict:
        """Parse data for the crystal structure models aka phases."""
        h5r = h5py.File(self.file_name, "r")
        grpnm = "/DataContainers/Small IN100/Phase Data"  # NEW ISSUE: interpret from filter!
        dsnm = f"{grpnm}/CrystalStructures"
        phase_ids = h5r[dsnm][...].flatten()
        print(phase_ids)
        dsnm = f"{grpnm}/MaterialName"
        phase_names = []
        for phase_name in h5r[dsnm][...]:
            phase_names.append(phase_name.decode("utf-8"))
        print(phase_names)
        dsnm = f"{grpnm}/LatticeConstants"
        unit_cells = h5r[dsnm][...]
        identifier = 0
        if np.shape(phase_ids)[0] == np.shape(phase_names)[0]:
            if np.shape(phase_ids)[0] == np.shape(unit_cells)[0]:
                if np.shape(unit_cells)[1] == 6:
                    # NEW ISSUE: assume first one is invalid
                    identifier = 1

        if identifier == 1:  # NEW ISSUE: extend for arbitrary number of phases
            self.phases[identifier] = {}
            self.phases[identifier]["name"] = phase_names[identifier]

            trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
                  f"/EM_EBSD_CRYSTAL_STRUCTURE_MODEL" \
                  f"[em_ebsd_crystal_structure_model{identifier}]"
            template[f"{trg}/phase_identifier"] = np.uint32(identifier)
            template[f"{trg}/phase_name"] = str(phase_names[identifier])
            template[f"{trg}/unit_cell_abc"] = np.asarray(
                [unit_cells[identifier, 0] * 0.1,
                 unit_cells[identifier, 1] * 0.1,
                 unit_cells[identifier, 2] * 0.1], np.float32)
            # ##? DREAM.3D reports in angstroem but no units attribute in dream3d file!
            template[f"{trg}/unit_cell_abc/@units"] = "nm"
            template[f"{trg}/unit_cell_alphabetagamma"] = np.asarray(
                [unit_cells[identifier, 3],
                 unit_cells[identifier, 4],
                 unit_cells[identifier, 5]], np.float32)
            # ##? DREAM.3D reports in degree
            template[f"{trg}/unit_cell_alphabetagamma/@units"] = "°"

        return template

    def parse_inverse_pole_figures(self, template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings."""
        print("Parse inverse pole figures (IPFs)...")
        # identifier match because phase is a list asc. sorted by numerical keys
        # "first phase_id" in DREAM.3D and em_om is 1
        for identifier in np.arange(1, np.max(self.phase_id) + 1):
            self.parse_inverse_pole_figure_map(identifier, template)
            self.parse_inverse_pole_figure_color_key(identifier, template)
            identifier += 1

        return template

    def parse_inverse_pole_figure_map(self, identifier, template: dict) -> dict:
        """Create default plot for the IPF-Z orientation mapping."""
        phase_id = identifier
        phase_name = self.phases[identifier]["name"]
        print(f"Generate inverse pole figure (IPF) map for {identifier}, {phase_name}...")

        trg = f"/ENTRY[entry{self.entry_id}]/correlation/PROCESS[ipf_map{phase_id}]"
        template[f"{trg}/bitdepth"] = np.uint32(8)
        template[f"{trg}/phase_identifier"] = np.uint32(phase_id)
        template[f"{trg}/phase_name"] = str(phase_name)
        template[f"{trg}/PROGRAM[program1]/program"] = str("dream3d")
        template[f"{trg}/PROGRAM[program1]/program/@version"] = "v6.5.163"
        template[f"{trg}/projection_direction"] = np.asarray([0., 0., 1.], np.float32)

        trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_map"
        template[f"{trg}/title"] = str("DREAM.3D ROI inverse-pole-figure colored")
        template[f"{trg}/@signal"] = "data"
        # template[f"{trg}/@axes"] = ["axis_x", "axis_y", "axis_z"]
        template[f"{trg}/@axes"] = ["axis_z", "axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        template[f"{trg}/@AXISNAME_indices[axis_z_indices]"] = np.uint32(2)
        # check again order x, y, z ??

        trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_map/data"
        # NEW ISSUE: needs one more check if precise currently
        ipf_map = np.asarray(np.zeros(np.shape(self.stack), np.uint8))  # 4d array
        # msk = self.phase_id == phase_id
        indices = np.shape(self.stack)
        for i in np.arange(0, indices[0]):
            for j in np.arange(0, indices[1]):
                for k in np.arange(0, indices[2]):
                    if self.phase_id[i, j, k, 0] == phase_id:
                        ipf_map[i, j, k, 0:3] = self.stack[i, j, k, 0:3]
        # likely this can be done with much fancy numpy nd indexing and more pythonic
        # instead of this loop nest but this is right at least...
        # needs a multi-dimensional masking of all values [x, y, z] check order...
        # where self.phase_id[x, y, z] != phase_id set ipf_map[x, y, z, 0:3]
        template[f"{trg}"] = {"compress": ipf_map, "strength": 1}

        template[f"{trg}/@long_name"] = "Signal"
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = [("axis_x", "x"), ("axis_y", "y"), ("axis_z", "z")]
        for axisname in axes_names:
            trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
                  f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_map/AXISNAME[{axisname[0]}]"
            template[f"{trg}"] = {"compress": self.xyz[axisname[1]], "strength": 1}
            template[f"{trg}/@long_name"] \
                = f"Calibrated position along {axisname[1]}-axis (µm)"
            template[f"{trg}/@units"] = "µm"  # parse from filter!

        return template

    def parse_inverse_pole_figure_color_key(self, identifier, template: dict) -> dict:
        """Parse color key renderings of inverse-pole-figure (IPF) mappings."""
        # in DREAM.3D not_indexed phase is 0 and "first" phase has ID 1
        # this is coincidently the convention which also this nomad-parser-nexus
        # em_om reader uses
        phase_id = identifier
        phase_name = self.phases[identifier]["name"]
        print(f"Parse inverse pole figure (IPF) color key {identifier}, {phase_name}...")

        # the key problem is that the DREAM.3D pipeline does not store the point group
        # so we need to have a heuristic approach which selects the correct IPF
        # color maps from the available default color mappings
        # https://github.com/BlueQuartzSoftware/DREAM3D/tree/v6_5_163/Source/Plugins/
        # OrientationAnalysis/Data/OrientationAnalysis/IPF_Legend
        # DREAM.3D stores a library of prerendered color keys as image files
        color_key_path = (__file__).replace(
            "dream3d_ebsd_parser.py", "dream3d_v65163_color_keys")
        color_key_file_name = f"{color_key_path}/Cubic_High.png"
        # NEW ISSUE:must not be Cubic_High.png only, this holds only for this example!

        # constraint further to 8bit RGB and no flipping
        # im = np.asarray(imageio.v3.imread(symm_name))
        img = np.asarray(thumbnail(pil.open(color_key_file_name, "r", ["png"]),
                         size=HFIVE_WEB_MAX_SIZE), np.uint8)
        img = img[:, :, 0:3]  # discard potential alpha channel
        # ##MK::need to constrain more the writing of the image that it is guaranteed
        # a specific type of image and bitdepth and color model, and avoid implicit
        # image transformations such as flips or rotations

        trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model"
        template[f"{trg}/title"] = str("Inverse pole figure color key with SST")
        template[f"{trg}/@signal"] = "data"
        template[f"{trg}/@axes"] = ["axis_y", "axis_x"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)
        trg = f"/ENTRY[entry{self.entry_id}]/correlation" \
              f"/PROCESS[ipf_map{phase_id}]/ipf_rgb_color_model/DATA[data]"
        template[f"{trg}"] = {"compress": img, "strength": 1}
        template[f"{trg}/@CLASS"] = "IMAGE"
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = [("axis_y", 0, "y-axis"), ("axis_x", 1, "x-axis")]
        for axis in axes_names:
            trg = f"/ENTRY[entry{self.entry_id}]/correlation/PROCESS[ipf_map{phase_id}]" \
                  f"/ipf_rgb_color_model/AXISNAME[{axis[0]}]"
            template[f"{trg}"] = {"compress": np.asarray(
                np.linspace(1, np.shape(img)[axis[1]], num=np.shape(img)[axis[1]],
                            endpoint=True), np.uint32), "strength": 1}
            template[f"{trg}/@long_name"] = f"Pixel along {axis[2]}"
            template[f"{trg}/@units"] = "px"

        return template

    def parse(self, template: dict) -> dict:
        """Parse NOMAD OASIS relevant data and metadata from a DREAM.3D file."""
        print("Parsing EBSD data from DREAM.3D...")
        print(self.file_name)
        print(f"{self.entry_id}")
        self.parse_pipeline()
        self.parse_roi_geometry()
        self.parse_roi_dimension_scale_axes()
        self.parse_roi_default_plot(template)
        self.parse_phases(template)
        self.parse_inverse_pole_figures(template)
        return template
