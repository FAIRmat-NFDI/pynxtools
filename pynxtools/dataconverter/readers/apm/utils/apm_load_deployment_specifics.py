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

from pynxtools.dataconverter.readers.apm.map_concepts.apm_oasis_cfg_to_nx_map \
    import APM_OASIS_TO_NEXUS_CFG
from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import apply_modifier, variadic_path_to_specific_path


class NxApmNomadOasisConfigurationParser:  # pylint: disable=too-few-public-methods
    """Parse deployment specific configuration."""

    def __init__(self, file_path: str, entry_id: int, verbose: bool = False):
        print(f"Extracting data from deployment specific configuration file: {file_path}")
        if (file_path.rsplit('/', 1)[-1].endswith(".oasis.specific.yaml")
                or file_path.endswith(".oasis.specific.yml")) and entry_id > 0:
            self.entry_id = entry_id
            self.file_path = file_path
            with open(self.file_path, "r", encoding="utf-8") as stream:
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter="/")
                if verbose == True:
                    for key, val in self.yml.items():
                        print(f"key: {key}, val: {val}")
        else:
            self.entry_id = 1
            self.file_path = ""
            self.yml = {}

    def report(self, template: dict) -> dict:
        """Copy data from configuration applying mapping functors."""
        for tpl in APM_OASIS_TO_NEXUS_CFG:
            identifier = [self.entry_id]
            if isinstance(tpl, tuple) and len(tpl) >= 2:
                if tpl[0] not in ("IGNORE", "UNCLEAR"):
                    trg = variadic_path_to_specific_path(tpl[0], identifier)
                    # print(f"processing tpl {tpl} ... trg {trg}")
                    if len(tpl) == 2:
                        # nxpath, value to use directly
                        template[trg] = tpl[1]
                    if len(tpl) == 3:
                        # nxpath, modifier, value, modifier (function) evaluates value to use
                        if tpl[1] == "load_from":
                            if tpl[2] in self.yml.keys():
                                template[trg] = self.yml[tpl[2]]
                            else:
                                raise ValueError(f"tpl2 {tpl[2]} not in self.yml.keys()!")
                        else:
                            raise ValueError(f"tpl1 {tpl[1]} is not load_from!")
        return template
