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
"""Load deployment-specific quantities."""

# pylint: disable=no-member

import flatdict as fd

import yaml

from pynxtools.dataconverter.readers.apm.map_concepts.apm_deployment_specifics_to_nx_map \
    import NxApmDeploymentSpecificInput

from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import apply_modifier, variadic_path_to_specific_path


class NxApmNomadOasisConfigurationParser:  # pylint: disable=too-few-public-methods
    """Parse deployment specific configuration."""

    def __init__(self, file_name: str, entry_id: int):
        print(f"Extracting data from deployment specific configuration file: {file_name}")
        if (file_name.rsplit('/', 1)[-1].endswith(".oasis.specific.yaml")
                or file_name.endswith(".oasis.specific.yml")) and entry_id > 0:
            self.entry_id = entry_id
            self.file_name = file_name
            with open(self.file_name, "r", encoding="utf-8") as stream:
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter="/")
        else:
            self.entry_id = 1
            self.file_name = ""
            self.yml = {}

    def report(self, template: dict) -> dict:
        """Copy data from configuration applying mapping functors."""
        for nx_path, modifier in NxApmDeploymentSpecificInput.items():
            if nx_path not in ("IGNORE", "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [self.entry_id, 1])
                res = apply_modifier(modifier, self.yml)
                if res is not None:
                    template[trg] = res
        return template
