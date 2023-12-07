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
"""Parse conventions from an ELN schema instance."""

# pylint: disable=no-member

# ,duplicate-code

from pynxtools.dataconverter.readers.em.geometry.handed_cartesian \
    import REFERENCE_FRAMES, AXIS_DIRECTIONS, is_cs_well_defined

from pynxtools.dataconverter.readers.em.concepts.concept_mapper \
    import variadic_path_to_specific_path, apply_modifier

from pynxtools.dataconverter.readers.em.geometry.geometry \
    import NxEmConventions

# example how to check against different types of Euler angle conventions
# from pynxtools.dataconverter.readers.em.geometry.euler_angle_convention \
#    import which_euler_convention

# example how to check if set of conventions matches to some suggestion in the literature
# from pynxtools.dataconverter.readers.em.geometry.msmse_convention \
#     import is_consistent_with_msmse_convention


class NxEmConventionMapper:
    """TODO::

    """

    def __init__(self, file_name: str, entry_id: int = 1):  # , pattern_simulation: bool):
        """Fill template with ELN pieces of information."""
        if entry_id > 0:
            self.entry_id = entry_id
        else:
            self.entry_id = 1
        # self.pattern_simulation = pattern_simulation
        # print(f"Extracting data from ELN file: {file_name}")
        # if (file_name.rsplit('/', 1)[-1].startswith("eln_data")
        #         or file_name.startswith("eln_data")) and entry_id > 0:
        #     self.entry_id = entry_id
        #     self.file_name = file_name
        #     with open(self.file_name, "r", encoding="utf-8") as stream:
        #         self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=":")
        # else:
        #     self.entry_id = 1
        #     self.file_name = ""
        #     self.yml = {}
        # if "ElectronBackscatterDiffraction" in self.yml:
        #     self.yml = self.yml["ElectronBackscatterDiffraction"]

    def parse(self, template: dict) -> dict:
        """Extract metadata from generic ELN text file to respective NeXus objects."""
        print("Parsing conventions...")
        for nx_path, value in NxEmConventions.items():
            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [self.entry_id])
                res = value
                if res is not None:
                    template[trg] = res
        return template
        # self.parse_rotation_convention_section(template)
        # self.parse_processing_frame_section(template)
        # self.parse_sample_frame_section(template)
        # self.parse_detector_frame_section(template)
        # self.parse_gnomonic_projection_section(template)
        # return template
