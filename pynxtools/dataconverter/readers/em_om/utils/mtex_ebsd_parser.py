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
"""Parse intermediate HDF5 files from MTex @EBSD classes and FAIRmat mtex2nexus script."""

# pylint: disable=no-member

import numpy as np

import h5py


class NxEmOmMtexEbsdParser:
    """Parse *.mtex EBSD data.

    """

    def __init__(self, file_name: str, entry_id: int):
        """Class wrapping reading HDF5 files formatted according NXem_ebsd from MTex."""
        self.file_name = file_name
        self.entry_id = entry_id

    def parse_roi_default_plot(self, template: dict) -> dict:
        """Parse data for the region-of-interest default plot."""
        print("Parse ROI default plot...")
        h5r = h5py.File(self.file_name, "r")
        # by construction from MTex entry always named entry1

        src = "/entry1/indexing/region_of_interest"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/region_of_interest"
        template[f"{trg}/descriptor"] = str(h5r[f"{src}/descriptor"][()].decode("utf-8"))

        src = "/entry1/indexing/region_of_interest/roi"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/region_of_interest/roi"
        if src not in h5r.keys():
            # must not happen, grp is required
            # print(f"WARNING {src} not found !")
            return template
        grp = h5r[src]
        # MTex HDF5 file uses formatting from matching that of NXem_ebsd
        template[f"{trg}/title"] = str("Region-of-interest overview image")
        template[f"{trg}/@signal"] = grp.attrs["signal"]
        template[f"{trg}/@axes"] = grp.attrs["axes"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = grp.attrs["axis_x_indices"]
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = grp.attrs["axis_y_indices"]

        src = "/entry1/indexing/region_of_interest/roi/data"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/region_of_interest/roi/data"
        if src not in h5r.keys():
            # must not happen, dst is required
            print(f"{src} not found !")
            return template
        dst = h5r[src]
        template[f"{trg}"] = {"compress": dst[:, :], "strength": 1}
        template[f"{trg}/@long_name"] = dst.attrs["long_name"]
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = ["axis_x", "axis_y"]
        for axis_name in axes_names:
            src = f"/entry1/indexing/region_of_interest/roi/{axis_name}"
            trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
                  f"region_of_interest/roi/{axis_name}"
            if src not in h5r.keys():
                # must not happen, dst is required
                # print(f"{src} not found !")
                return template
            dst = h5r[src]
            template[f"{trg}"] = {"compress": dst[:], "strength": 1}
            template[f"{trg}/@long_name"] = dst.attrs["long_name"]
            template[f"{trg}/@units"] = dst.attrs["units"]

        h5r.close()
        return template

    def parse_phases(self, template: dict) -> dict:
        """Parse data for the crystal structure models aka phases."""
        print("Parse crystal_structure_models aka phases...")
        h5r = h5py.File(self.file_name, "r")

        src = "/entry1/indexing"
        # mtex2nexus MTex/Matlab scripts writes controlled terms phaseID
        group_names = [entry for entry in h5r[src].keys() if entry.startswith('phase')]
        if len(group_names) == 0:
            return template
        # group_names end up sorted in ascending order
        identifier = 1
        for group_name in group_names:
            if f"phase{identifier}" != group_name:
                # must not happen, verifier will complain
                return template
            src = f"/entry1/indexing/{group_name}"
            trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
                  f"EM_EBSD_CRYSTAL_STRUCTURE_MODEL" \
                  f"[em_ebsd_crystal_structure_model{identifier}]"
            template[f"{trg}/phase_identifier"] = h5r[f"{src}/phase_identifier"][0]
            template[f"{trg}/phase_name"] \
                = str(h5r[f"{src}/phase_name"][()].decode("utf-8"))
            template[f"{trg}/point_group"] \
                = str(h5r[f"{src}/point_group"][()].decode("utf-8"))
            dst = h5r[f"{src}/unit_cell_abc"]
            template[f"{trg}/unit_cell_abc"] = dst[:]
            template[f"{trg}/unit_cell_abc/@units"] = dst.attrs["units"]
            dst = h5r[f"{src}/unit_cell_alphabetagamma"]
            template[f"{trg}/unit_cell_alphabetagamma"] = dst[:]
            template[f"{trg}/unit_cell_alphabetagamma/@units"] = dst.attrs["units"]
            identifier += 1
        h5r.close()
        return template

    def parse_inverse_pole_figures(self, template: dict) -> dict:
        """Parse inverse pole figures (IPF) mappings."""
        print("Parse inverse pole figures (IPFs)...")
        h5r = h5py.File(self.file_name, "r")

        src = "/entry1/indexing"
        # mtex2nexus MTex/Matlab scripts writes controlled terms phaseID
        group_names = [entry for entry in h5r[src].keys() if entry.startswith('ipf_map')]
        if len(group_names) == 0:
            return template
        # group_names end up sorted in ascending order
        identifier = 1
        for group_name in group_names:
            if f"ipf_map{identifier}" != group_name:
                # must not happen, verifier will complain that we use incorrect names
                # print(f"WARNING: {group_name} not found !")
                return template

            self.parse_inverse_pole_figure_map(h5r, identifier, template)
            self.parse_inverse_pole_figure_color_key(h5r, identifier, template)

            identifier += 1

        h5r.close()
        return template

    def parse_inverse_pole_figure_map(self, h5r, identifier, template: dict) -> dict:
        """Parse inverse-pole-figure (IPF) mappings on their color models."""
        group_name = f"ipf_map{identifier}"
        print(f"Parse inverse pole figure (IPF) map for {group_name}...")
        src = f"/entry1/indexing/{group_name}"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{identifier}]"
        if src not in h5r.keys():
            # print(f"WARNING: {group_name} not found !")
            return template
        template[f"{trg}/bitdepth"] = np.uint32(8)  # h5r[f"{src}/bitdepth"][0]
        template[f"{trg}/phase_identifier"] = np.uint32(h5r[f"{src}/phase_identifier"][0])
        template[f"{trg}/phase_name"] = str(h5r[f"{src}/phase_name"][()].decode("utf-8"))
        dst = h5r[f"{src}/program"]
        template[f"{trg}/PROGRAM[program1]/program"] = str(dst[()].decode("utf-8"))
        template[f"{trg}/PROGRAM[program1]/program/@version"] = dst.attrs["version"]
        template[f"{trg}/projection_direction"] = np.asarray([0., 0., 1.], np.float32)
        # there should be a depends on etc

        src = f"/entry1/indexing/{group_name}/ipf_rgb_map"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{identifier}]/ipf_rgb_map"
        if src not in h5r.keys():
            # must not happen, grp is required
            # print(f"WARNING: {group_name} not found, ipf_rgb_map !")
            return template
        grp = h5r[src]
        # MTex HDF5 file uses formatting from matching that of NXem_ebsd
        template[f"{trg}/title"] = str("Inverse pole figure color map")
        template[f"{trg}/@signal"] = grp.attrs["signal"]
        template[f"{trg}/@axes"] = grp.attrs["axes"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = grp.attrs["axis_x_indices"]
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = grp.attrs["axis_y_indices"]

        src = f"/entry1/indexing/{group_name}/ipf_rgb_map/data"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/" \
              f"PROCESS[ipf_map{identifier}]/ipf_rgb_map/DATA[data]"
        if src not in h5r.keys():
            # must not happen, dst is required
            # print(f"WARNING: {group_name} not found, ipf_rgb_map, data !")
            return template
        dst = h5r[src]
        template[f"{trg}"] = {"compress": dst[:, :], "strength": 1}
        template[f"{trg}/@long_name"] = dst.attrs["long_name"]
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = ["axis_x", "axis_y"]
        for axis_name in axes_names:
            src = f"/entry1/indexing/{group_name}/ipf_rgb_map/{axis_name}"
            trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
                  f"/PROCESS[ipf_map{identifier}]/ipf_rgb_map/AXISNAME[{axis_name}]"
            if src not in h5r.keys():
                # must not happen, dst is required
                # print(f"WARNING: {group_name} not found, ipf_rgb_map, {axis_name} !")
                return template
            dst = h5r[src]
            template[f"{trg}"] = {"compress": dst[:], "strength": 1}
            template[f"{trg}/@long_name"] = dst.attrs["long_name"]
            template[f"{trg}/@units"] = dst.attrs["units"]

        return template

    def parse_inverse_pole_figure_color_key(self, h5r, identifier, template: dict) -> dict:
        """Parse color key renderings of inverse-pole-figure (IPF) mappings."""
        group_name = f"ipf_map{identifier}"
        print(f"Parse inverse pole figure (IPF) color key {group_name}...")
        src = f"/entry1/indexing/{group_name}/ipf_rgb_color_model"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{identifier}]/ipf_rgb_color_model"
        if src not in h5r.keys():
            # must not happen, grp is required
            # print(f"WARNING: {group_name} not found, ipf_rgb_color_model")
            return template
        grp = h5r[src]
        template[f"{trg}/title"] = str("Inverse pole figure color key with SST")
        template[f"{trg}/@signal"] = grp.attrs["signal"]
        template[f"{trg}/@axes"] = grp.attrs["axes"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = grp.attrs["axis_x_indices"]
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = grp.attrs["axis_y_indices"]

        src = f"/entry1/indexing/{group_name}/ipf_rgb_color_model/data"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
              f"/PROCESS[ipf_map{identifier}]/ipf_rgb_color_model/DATA[data]"
        if src not in h5r.keys():
            # must not happen, dst is required
            # print(f"WARNING: {group_name} not found, ipf_rgb_color_model, data")
            return template
        dst = h5r[src]
        template[f"{trg}"] = {"compress": dst[:, :], "strength": 1}
        template[f"{trg}/@long_name"] = dst.attrs["long_name"]
        template[f"{trg}/@CLASS"] = "IMAGE"
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = ["axis_x", "axis_y"]
        for axis_name in axes_names:
            src = f"/entry1/indexing/{group_name}/ipf_rgb_color_model/{axis_name}"
            trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing" \
                  f"/PROCESS[ipf_map{identifier}]/ipf_rgb_color_model" \
                  f"/AXISNAME[{axis_name}]"
            if src not in h5r.keys():
                # must not happen, dst is required
                # print(f"WARNING: {group_name} not found,
                # ipf_rgb_color_model, {axis_name}")
                return template
            dst = h5r[src]
            template[f"{trg}"] = {"compress": dst[:], "strength": 1}
            template[f"{trg}/@long_name"] = dst.attrs["long_name"]
            template[f"{trg}/@units"] = str("px")

        return template

    def parse(self, template: dict) -> dict:
        """Parse metadata and numerical data."""
        print("Parsing MTex EBSD data...")
        print(f"{self.file_name}")
        print(f"{self.entry_id}")
        # extract data from intermediate HDF5 file and transfer these to the template
        self.parse_roi_default_plot(template)
        self.parse_phases(template)
        self.parse_inverse_pole_figures(template)
        return template
