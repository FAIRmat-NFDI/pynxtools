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
"""Parse data from custom schema YAML file onto NeXus concept instances in NXem."""

# pylint: disable=no-member

import numpy as np

import flatdict as fd

import yaml

from ase.data import chemical_symbols

from pynxtools.dataconverter.readers.em_nion.utils.em_nion_versioning \
    import NX_EM_NION_ADEF_NAME, NX_EM_NION_ADEF_VERSION

from pynxtools.dataconverter.readers.em_nion.utils.em_nion_versioning \
    import NX_EM_NION_EXEC_NAME, NX_EM_NION_EXEC_VERSION

from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import apply_modifier, variadic_path_to_specific_path

from pynxtools.dataconverter.readers.em_nion.map_concepts.swift_eln_to_nx_map \
    import NxEmElnInput, NxUserFromListOfDict, NxDetectorListOfDict, NxSample


class NxEmNionElnSchemaParser:
    """Parse eln_data.yaml dump file content generated from a NOMAD OASIS YAML.

    The functionalities in this ELN YAML parser do not check if the
    instantiated template yields an instance which is compliant NXapm.
    Instead, this task is handled by the generic part of the dataconverter
    during the verification of the template dictionary.
    """

    def __init__(self, file_name: str, entry_id: int):
        print(f"Extracting data from ELN file: {file_name}")
        if (file_name.rsplit('/', 1)[-1].startswith("eln_data")
                or file_name.startswith("eln_data")) and entry_id > 0:
            self.entry_id = entry_id
            self.file_name = file_name
            with open(self.file_name, "r", encoding="utf-8") as stream:
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter="/")
        else:
            self.entry_id = 1
            self.file_name = ""
            self.yml = {}

    def parse_user_section(self, template: dict) -> dict:
        """Copy data from user section into template."""
        src = "user"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                if (all(isinstance(entry, dict) for entry in self.yml[src]) is True):
                    user_id = 1
                    # custom schema delivers a list of dictionaries...
                    for user_dict in self.yml[src]:
                        # ... for each of them inspect for fields mappable on NeXus
                        identifier = [self.entry_id, user_id]
                        # identifier to get instance NeXus path from variadic NeXus path
                        # try to find all quantities on the left-hand side of the mapping
                        # table and check if we can find these
                        for nx_path, modifier in NxUserFromListOfDict.items():
                            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                                trg = variadic_path_to_specific_path(nx_path, identifier)
                                res = apply_modifier(modifier, user_dict)
                                if res is not None:
                                    template[trg] = res
                        user_id += 1
        return template

    def parse_sample_section(self, template: dict) -> dict:
        """Copy data from sample section into template."""
        src = "sample/atom_types"
        trg = f"/ENTRY[entry{self.entry_id}]/{src}"
        if "sample/atom_types" in self.yml.keys():
            if (isinstance(self.yml[src], list)) and (len(self.yml[src]) >= 1):
                atom_types_are_valid = True
                for symbol in self.yml[src]:
                    valid = isinstance(symbol, str) \
                        and (symbol in chemical_symbols) and (symbol != "X")
                    if valid is False:
                        atom_types_are_valid = False
                        break
                if atom_types_are_valid is True:
                    template[trg] = ", ".join(list(self.yml[src]))

        for nx_path, modifier in NxSample.items():
            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [self.entry_id])
                res = apply_modifier(modifier, self.yml)
                if res is not None:
                    template[trg] = res

        return template

    def parse_detector_section(self, template: dict) -> dict:
        """Copy data from detector section into template."""
        src = "em_lab/detector"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                if (all(isinstance(entry, dict) for entry in self.yml[src]) is True):
                    detector_id = 1
                    # custom schema delivers a list of dictionaries...
                    for detector_dict in self.yml[src]:
                        # ... for each of them inspect for fields mappable on NeXus
                        identifier = [self.entry_id, detector_id]
                        # identifier to get instance NeXus path from variadic NeXus path
                        # try to find all quantities on the left-hand side of the mapping
                        # table and check if we can find these
                        for nx_path, modifier in NxDetectorListOfDict.items():
                            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                                trg = variadic_path_to_specific_path(nx_path, identifier)
                                res = apply_modifier(modifier, detector_dict)
                                if res is not None:
                                    template[trg] = res
                        detector_id += 1

        return template

    def parse_other_sections(self, template: dict) -> dict:
        """Copy data from custom schema (excluding user, sample) into template."""
        for nx_path, modifier in NxEmElnInput.items():
            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [self.entry_id, 1])
                res = apply_modifier(modifier, self.yml)
                if res is not None:
                    template[trg] = res
        return template

    def parse(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_user_section(template)
        self.parse_detector_section(template)
        self.parse_sample_section(template)
        self.parse_other_sections(template)

        debugging = False
        if debugging is True:
            for keyword, value in template.items():
                print(f"{keyword}, {value}")
        return template
