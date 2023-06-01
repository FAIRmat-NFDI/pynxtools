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
"""Parse metadata in generic (like reported by an OASIS ELN) schema."""

# pylint: disable=no-member,duplicate-code

import numpy as np

import flatdict as fd

import yaml

# from ase.data import chemical_symbols

from pynxtools.dataconverter.readers.em_om.utils.versioning \
    import NX_EM_OM_ADEF_NAME, NX_EM_OM_ADEF_VERSION
from pynxtools.dataconverter.readers.em_om.utils.versioning \
    import NX_EM_OM_EXEC_NAME, NX_EM_OM_EXEC_VERSION

from pynxtools.dataconverter.readers.em_om.utils.handed_cartesian \
    import REFERENCE_FRAMES, AXIS_DIRECTIONS, is_cs_well_defined

# example how to check against different types of Euler angle conventions
# from pynxtools.dataconverter.readers.em_om.utils.euler_angle_convention \
#    import which_euler_convention

# example how to check if set of conventions matches to some suggestion in the literature
# from pynxtools.dataconverter.readers.em_om.utils.msmse_convention \
#     import is_consistent_with_msmse_convention


class NxEmOmGenericElnSchemaParser:
    """Parse eln_data.yaml dump file content generated from an (e.g. OASIS) ELN.

    """

    def __init__(self, file_name: str, entry_id: int, pattern_simulation: bool):
        """Fill template with ELN pieces of information."""
        self.pattern_simulation = pattern_simulation
        print(f"Extracting data from ELN file: {file_name}")
        if (file_name.rsplit('/', 1)[-1].startswith("eln_data")
                or file_name.startswith("eln_data")) and entry_id > 0:
            self.entry_id = entry_id
            self.file_name = file_name
            with open(self.file_name, "r", encoding="utf-8") as stream:
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=":")
        else:
            self.entry_id = 1
            self.file_name = ""
            self.yml = {}

        # if "ElectronBackscatterDiffraction" in self.yml:
        #     self.yml = self.yml["ElectronBackscatterDiffraction"]

    def parse(self, template: dict) -> dict:
        """Extract metadata from generic ELN text file to respective NeXus objects."""
        print("Parsing ELN input...")
        print(f"{self.file_name}")
        print(f"{self.entry_id}")
        self.parse_entry_section(template)
        self.parse_user_section(template)
        if self.pattern_simulation is False:
            self.parse_commerical_on_the_fly_section(template)
            self.parse_measurement_section(template)
            self.parse_calibration_section(template)
        self.parse_rotation_convention_section(template)
        self.parse_processing_frame_section(template)
        self.parse_sample_frame_section(template)
        self.parse_detector_frame_section(template)
        self.parse_gnomonic_projection_section(template)
        if self.pattern_simulation is False:
            self.parse_indexing(template)
        return template

    def parse_entry_section(self, template: dict) -> dict:
        """"Parse entry section."""
        print("Parse entry...")
        src = "entry"
        trg = f"/ENTRY[entry{self.entry_id}]/"
        if (self.yml[f"{src}:attr_version"] == NX_EM_OM_ADEF_VERSION) \
                and (self.yml[f"{src}:definition"] == NX_EM_OM_ADEF_NAME):
            template[f"{trg}@version"] = NX_EM_OM_ADEF_VERSION
            template[f"{trg}definition"] = NX_EM_OM_ADEF_NAME
            template[f"{trg}PROGRAM[program1]/program"] = NX_EM_OM_EXEC_NAME
            template[f"{trg}PROGRAM[program1]/program/@version"] = NX_EM_OM_EXEC_VERSION
        if ("program" in self.yml[src].keys()) \
                and ("program__attr_version" in self.yml[src].keys()):
            template[f"{trg}PROGRAM[program2]/program"] \
                = self.yml[f"{src}:program"]
            template[f"{trg}PROGRAM[program2]/program/@version"] \
                = self.yml[f"{src}:program__attr_version"]
        # check that versions NX_EM_OM_* match
        req_field_names = ["definition", "start_time", "end_time",
                           "workflow_description", "workflow_identifier"]
        for field in req_field_names:
            if field in self.yml[src].keys():
                template[f"{trg}{field}"] = self.yml[f"{src}:{field}"]

        return template

    def parse_user_section(self, template: dict) -> dict:
        """Parse user section."""
        print("Parse user...")
        src = "user"
        if not isinstance(self.yml[src], list):
            return template
        user_id = 1
        for user_list in self.yml[src]:
            trg = f"/ENTRY[entry{self.entry_id}]/USER[user{user_id}]/"
            field_names = [
                "name", "email", "affiliation", "address",
                "orcid", "orcid_platform",
                "telephone_number", "role",
                "social_media_name", "social_media_platform"]
            for field_name in field_names:
                if field_name in user_list.keys():
                    template[f"{trg}{field_name}"] = user_list[field_name]
            user_id += 1
        return template

    def parse_commerical_on_the_fly_section(self, template: dict) -> dict:
        """Parse the on-the-fly section."""
        print("Parse commercial on-the-fly")
        src = "commercial_on_the_fly_indexing"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing/on_the_fly_indexing/"
        if ("program" in self.yml[src].keys()) \
                and ("program__attr_version" in self.yml[src].keys()):
            template[f"{trg}PROGRAM[program1]/program"] \
                = self.yml[f"{src}:program"]
            template[f"{trg}PROGRAM[program1]/program/@version"] \
                = self.yml[f"{src}:program__attr_version"]
        if "results_file" in self.yml[src].keys():
            template[f"{trg}origin"] = self.yml[f"{src}:results_file"]
        if "results_file__attr_version" in self.yml[src].keys():
            template[f"{trg}origin/@version"] \
                = self.yml[f"{src}:results_file__attr_version"]
        template[f"{trg}path"] = str("undefined")
        # NEW ISSUE: this is a bug not results_file version in eln but path !!
        return template

    def parse_measurement_section(self, template: dict) -> dict:
        """Parse measurement section establishing link between NXem_ebsd and NXem."""
        print("Parse measurement...")
        src = "measurement"
        field_names = ["origin", "path"]
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/acquisition/"
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]
        if "origin__attr_version" in self.yml[src].keys():
            template[f"{trg}origin/@version"] = self.yml[f"{src}:origin__attr_version"]
        return template

    def parse_calibration_section(self, template: dict) -> dict:
        """Parse calibration section."""
        print("Parse calibration...")
        src = "calibration"
        field_names = ["origin", "path"]
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/calibration/"
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]
        if "origin__attr_version" in self.yml[src].keys():
            template[f"{trg}origin/@version"] = self.yml[f"{src}:origin__attr_version"]
        return template

    def parse_rotation_convention_section(self, template: dict) -> dict:
        """Parse rotation conventions."""
        src = "rotation_conventions"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions/rotation_conventions/"
        terms = [
            "three_dimensional_rotation_handedness",
            "rotation_convention",
            "euler_angle_convention",
            "axis_angle_convention"]
        for term in terms:
            if term in self.yml[src].keys():
                template[f"{trg}{term}"] = self.yml[f"{src}:{term}"].lower()
        # one term named differently in ELN than in NeXus appdef template keyword
        if "sign_convention" in self.yml[src].keys():
            template[f"{trg}orientation_parameterization_sign_convention"] \
                = self.yml[f"{src}:sign_convention"].lower()
        # if desired one could check conventions are consistent with specific ones
        return template

    def parse_processing_frame_section(self, template: dict) -> dict:
        """Parse processing reference frame definitions."""
        axes_names = ["x", "y", "z"]
        src = "processing_reference_frame"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions/processing_reference_frame/"
        if "reference_frame_type" in self.yml[src].keys():
            if self.yml[f"{src}:reference_frame_type"] in REFERENCE_FRAMES:
                template[f"{trg}reference_frame_type"] \
                    = self.yml[f"{src}:reference_frame_type"]
            xyz_directions = ["undefined", "undefined", "undefined"]
            xyz_aliases = ["", "", ""]
            for idx in np.arange(0, 3):
                axis_name = axes_names[idx]
                if f"{axis_name}axis_direction" in self.yml[src].keys():
                    if self.yml[f"{src}:{axis_name}axis_direction"] in AXIS_DIRECTIONS:
                        xyz_directions[idx] = self.yml[f"{src}:{axis_name}axis_direction"]
                if f"{axis_name}axis_alias" in self.yml[src].keys():
                    xyz_aliases[idx] = self.yml[f"{src}:{axis_name}axis_alias"]

            if is_cs_well_defined(self.yml[f"{src}:reference_frame_type"], xyz_directions):
                for idx in np.arange(0, 3):
                    axis_name = axes_names[idx]
                    template[f"{trg}{axis_name}axis_direction"] = xyz_directions[idx]
                    template[f"{trg}{axis_name}axis_alias"] = xyz_aliases[idx]
            if "origin" in self.yml[src].keys():
                template[f"{trg}origin"] = self.yml[f"{src}:origin"]
        return template

    def parse_sample_frame_section(self, template: dict) -> dict:
        """Parse sample reference frame definitions."""
        axes_names = ["x", "y", "z"]
        src = "sample_reference_frame"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions/sample_reference_frame/"
        if "reference_frame_type" in self.yml[src].keys():
            if self.yml[f"{src}:reference_frame_type"] in REFERENCE_FRAMES:
                template[f"{trg}reference_frame_type"] \
                    = self.yml[f"{src}:reference_frame_type"]
            xyz_directions = ["undefined", "undefined", "undefined"]
            for idx in np.arange(0, 3):
                axis_name = axes_names[idx]
                if f"{axis_name}axis_direction" in self.yml[src].keys():
                    if self.yml[f"{src}:{axis_name}axis_direction"] in AXIS_DIRECTIONS:
                        xyz_directions[idx] = self.yml[f"{src}:{axis_name}axis_direction"]
            if is_cs_well_defined(self.yml[f"{src}:reference_frame_type"], xyz_directions):
                for idx in np.arange(0, 3):
                    axis_name = axes_names[idx]
                    template[f"{trg}{axis_name}axis_direction"] = xyz_directions[idx]
            if "origin" in self.yml[src].keys():
                template[f"{trg}origin"] = self.yml[f"{src}:origin"]
        return template

    def parse_detector_frame_section(self, template: dict) -> dict:
        """Parse detector reference frame definitions."""
        axes_names = ["x", "y", "z"]
        src = "detector_reference_frame"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions/detector_reference_frame/"
        if "reference_frame_type" in self.yml[src].keys():
            if self.yml[f"{src}:reference_frame_type"] in REFERENCE_FRAMES:
                template[f"{trg}reference_frame_type"] \
                    = self.yml[f"{src}:reference_frame_type"]
            xyz_directions = ["undefined", "undefined", "undefined"]
            for idx in np.arange(0, 3):
                axis_name = axes_names[idx]
                if f"{axis_name}axis_direction" in self.yml[src].keys():
                    if self.yml[f"{src}:{axis_name}axis_direction"] in AXIS_DIRECTIONS:
                        xyz_directions[idx] = self.yml[f"{src}:{axis_name}axis_direction"]
            if is_cs_well_defined(self.yml[f"{src}:reference_frame_type"], xyz_directions):
                for idx in np.arange(0, 3):
                    axis_name = axes_names[idx]
                    template[f"{trg}{axis_name}axis_direction"] = xyz_directions[idx]
            if "origin" in self.yml[src].keys():
                template[f"{trg}origin"] = self.yml[f"{src}:origin"]
        # ... <-- is the same except for the src name
        return template

    def parse_gnomonic_projection_section(self, template: dict) -> dict:
        """Parse for the gnomonic projection."""
        axes_names = ["x", "y", "z"]
        src = "gnomonic_projection:gnomonic_projection_reference_frame"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions" \
              f"/gnomonic_projection_reference_frame/"
        if "reference_frame_type" in self.yml[src].keys():
            if self.yml[f"{src}:reference_frame_type"] in REFERENCE_FRAMES:
                template[f"{trg}reference_frame_type"] \
                    = self.yml[f"{src}:reference_frame_type"]
            xyz_directions = ["undefined", "undefined", "undefined"]
            for idx in np.arange(0, 3):
                axis_name = axes_names[idx]
                if f"{axis_name}axis_direction" in self.yml[src].keys():
                    if self.yml[f"{src}:{axis_name}axis_direction"] in AXIS_DIRECTIONS:
                        xyz_directions[idx] = self.yml[f"{src}:{axis_name}axis_direction"]
            if is_cs_well_defined(self.yml[f"{src}:reference_frame_type"], xyz_directions):
                for idx in np.arange(0, 3):
                    axis_name = axes_names[idx]
                    template[f"{trg}{axis_name}axis_direction"] = xyz_directions[idx]
            if "origin" in self.yml[src].keys():
                template[f"{trg}origin"] = self.yml[f"{src}:origin"]

        src = "gnomonic_projection:pattern_centre"
        trg = f"/ENTRY[entry{self.entry_id}]/conventions/pattern_centre/"
        axes_names = ["x", "y"]
        field_names = ["axis_boundary_convention", "axis_normalization_direction"]
        for idx in np.arange(0, 2):
            axis_name = axes_names[idx]
            for field_name in field_names:
                if f"{axis_name}{field_name}" in self.yml[src].keys():
                    template[f"{trg}{axis_name}{field_name}"] \
                        = self.yml[f"{src}:{axis_name}{field_name}"]
        return template

    def parse_indexing(self, template: dict) -> dict:
        """Parse indexing section."""
        print("Parse indexing...")
        src = "indexing"
        trg = f"/ENTRY[entry{self.entry_id}]/experiment/indexing"
        if "method" in self.yml[src].keys():
            template[f"{trg}/method"] = self.yml[f"{src}:method"]
        return template
