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
"""Wrapping multiple parsers for vendor files with NOMAD OASIS/ELN/YAML metadata."""

# pylint: disable=no-member,duplicate-code,too-many-nested-blocks

import flatdict as fd
import yaml

from ase.data import chemical_symbols
from pynxtools.dataconverter.readers.apm.map_concepts.apm_example_eln_to_nx_map \
    import APM_EXAMPLE_OTHER_TO_NEXUS, APM_EXAMPLE_USER_TO_NEXUS
from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import variadic_path_to_specific_path
from pynxtools.dataconverter.readers.apm.utils.apm_parse_composition_table \
    import parse_composition_table
from pynxtools.dataconverter.readers.shared.shared_utils \
    import get_sha256_of_file_content


class NxApmNomadOasisElnSchemaParser:  # pylint: disable=too-few-public-methods
    """Parse eln_data.yaml dump file content generated from a NOMAD OASIS YAML.

    This parser implements a design where an instance of a specific NOMAD
    custom schema ELN template is used to fill pieces of information which
    are typically not contained in files from technology partners
    (e.g. pos, epos, apt, rng, rrng, ...). Until now, this custom schema and
    the NXapm application definition do not use a fully harmonized vocabulary.
    Therefore, the here hardcoded implementation is needed which maps specifically
    named pieces of information from the custom schema instance on named fields
    in an instance of NXapm

    The functionalities in this ELN YAML parser do not check if the
    instantiated template yields an instance which is compliant with NXapm.
    Instead, this task is handled by the generic part of the dataconverter
    during the verification of the template dictionary.
    """

    def __init__(self, file_path: str, entry_id: int, verbose: bool = False):
        print(f"Extracting data from ELN file: {file_path}")
        if (file_path.rsplit('/', 1)[-1].startswith("eln_data")
                or file_path.startswith("eln_data")) and entry_id > 0:
            self.entry_id = entry_id
            self.file_path = file_path
            with open(self.file_path, "r", encoding="utf-8") as stream:
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter="/")
                if verbose is True:
                    for key, val in self.yml.items():
                        print(f"key: {key}, value: {val}")
        else:
            self.entry_id = 1
            self.file_path = ""
            self.yml = {}

    def parse_sample_composition(self, template: dict) -> dict:
        """Interpret human-readable ELN input to generate consistent composition table."""
        src = "sample/composition"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                dct = parse_composition_table(self.yml[src])

                prfx = f"/ENTRY[entry{self.entry_id}]/sample/" \
                       f"CHEMICAL_COMPOSITION[chemical_composition]"
                unit = "at.-%"  # the assumed default unit
                if "normalization" in dct:
                    if dct["normalization"] in ["%", "at%", "at-%", "at.-%", "ppm", "ppb"]:
                        unit = "at.-%"
                        template[f"{prfx}/normalization"] = "atom_percent"
                    elif dct["normalization"] in ["wt%", "wt-%", "wt.-%"]:
                        unit = "wt.-%"
                        template[f"{prfx}/normalization"] = "weight_percent"
                    else:
                        return template
                ion_id = 1
                for symbol in chemical_symbols[1::]:
                    # ase convention, chemical_symbols[0] == "X"
                    # to use ordinal number for indexing
                    if symbol in dct:
                        if isinstance(dct[symbol], tuple) and len(dct[symbol]) == 2:
                            trg = f"{prfx}/ION[ion{ion_id}]"
                            template[f"{trg}/name"] = symbol
                            template[f"{trg}/composition"] = dct[symbol][0]
                            template[f"{trg}/composition/@units"] = unit
                            if dct[symbol][1] is not None:
                                template[f"{trg}/composition_error"] = dct[symbol][1]
                                template[f"{trg}/composition_error/@units"] = unit
                            ion_id += 1
        return template

    def parse_user(self, template: dict) -> dict:
        """Copy data from user section into template."""
        src = "user"
        if src in self.yml:
            if isinstance(self.yml[src], list):
                if all(isinstance(entry, dict) for entry in self.yml[src]) is True:
                    user_id = 1
                    # custom schema delivers a list of dictionaries...
                    for user_dict in self.yml[src]:
                        if user_dict == {}:
                            continue
                        identifier = [self.entry_id, user_id]
                        for key in user_dict:
                            for tpl in APM_EXAMPLE_USER_TO_NEXUS:
                                if isinstance(tpl, tuple) and (len(tpl) == 3):
                                    if (tpl[1] == "load_from") and (key == tpl[2]):
                                        trg = variadic_path_to_specific_path(
                                            tpl[0], identifier)
                                        # res = apply_modifier(modifier, user_dict)
                                        # res is not None
                                        template[trg] = user_dict[tpl[2]]
                        user_id += 1
        return template

    def parse_pulser_source(self, template: dict) -> dict:
        """Copy data into the (laser)/source section of the pulser."""
        # additional laser-specific details only relevant when the laser was used
        if "atom_probe/pulser/pulse_mode" in self.yml.keys():
            if self.yml["atom_probe/pulser/pulse_mode"] == "voltage":
                return template

        src = "atom_probe/pulser/laser_source"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                if all(isinstance(entry, dict) for entry in self.yml[src]) is True:
                    laser_id = 1
                    # custom schema delivers a list of dictionaries...
                    for ldct in self.yml[src]:
                        trg_sta = f"/ENTRY[entry{self.entry_id}]/measurement/" \
                                  f"instrument/pulser/SOURCE[source{laser_id}]"
                        if "name" in ldct:
                            template[f"{trg_sta}/name"] = ldct["name"]
                        quantities = ["wavelength"]
                        for qnt in quantities:
                            if ("value" in ldct[qnt]) and ("unit" in ldct[qnt]):
                                template[f"{trg_sta}/{qnt}"] = ldct[qnt]["value"]
                                template[f"{trg_sta}/{qnt}/@units"] = ldct[qnt]["unit"]

                        trg_dyn = f"/ENTRY[entry{self.entry_id}]/measurement/" \
                                  f"event_data_apm_set/EVENT_DATA_APM[event_data_apm]/" \
                                  f"instrument/pulser/SOURCE[source{laser_id}]"
                        quantities = ["power", "pulse_energy"]
                        for qnt in quantities:
                            if isinstance(ldct[qnt], dict):
                                if ("value" in ldct[qnt]) and ("unit" in ldct[qnt]):
                                    template[f"{trg_dyn}/{qnt}"] = ldct[qnt]["value"]
                                    template[f"{trg_dyn}/{qnt}/@units"] = ldct[qnt]["unit"]
                        laser_id += 1
                    return template
        print("WARNING: pulse_mode != voltage but no laser details specified!")
        return template

    def parse_other(self, template: dict) -> dict:
        """Copy data from custom schema into template."""
        identifier = [self.entry_id]
        for tpl in APM_EXAMPLE_OTHER_TO_NEXUS:
            if isinstance(tpl, tuple) and len(tpl) >= 2:
                if tpl[1] not in ("ignore"):
                    trg = variadic_path_to_specific_path(tpl[0], identifier)
                    # print(f"processing tpl {tpl} ... trg {trg}")
                    if len(tpl) == 2:
                        template[trg] = tpl[1]
                    if len(tpl) == 3:
                        # nxpath, modifier, value, modifier (function) evaluates value to use
                        if tpl[1] == "load_from":
                            if tpl[2] in self.yml.keys():
                                template[trg] = self.yml[tpl[2]]
                            else:
                                raise ValueError(f"tpl2 {tpl[2]} not in self.yml.keys()!")
                        elif tpl[1] == "sha256":
                            if tpl[2] in self.yml.keys():
                                with open(self.yml[tpl[2]], "rb") as fp:
                                    template[trg] = get_sha256_of_file_content(fp)
                            else:
                                raise ValueError(f"tpl2 {tpl[2]} not in self.yml.keys()!")
                        else:
                            raise ValueError(f"tpl1 {tpl[1]} is an modifier (function)!")
        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_sample_composition(template)
        self.parse_user(template)
        self.parse_pulser_source(template)
        self.parse_other(template)
        return template
