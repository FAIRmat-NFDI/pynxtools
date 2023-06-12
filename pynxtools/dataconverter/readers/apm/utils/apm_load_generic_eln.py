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

from pynxtools.dataconverter.readers.apm.map_concepts.apm_eln_to_nx_map \
    import NxApmElnInput, NxUserFromListOfDict

from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import variadic_path_to_specific_path, apply_modifier

from pynxtools.dataconverter.readers.apm.utils.apm_parse_composition_table \
    import parse_composition_table


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

    def parse_user_section(self, template: dict) -> dict:
        """Copy data from user section into template."""
        src = "user"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                if all(isinstance(entry, dict) for entry in self.yml[src]) is True:
                    user_id = 1
                    # custom schema delivers a list of dictionaries...
                    for user_dict in self.yml[src]:
                        # ... for each of them inspect for fields mappable on NeXus
                        identifier = [self.entry_id, user_id]
                        # identifier to get instance NeXus path from variadic NeXus path
                        # try to find all quantities on the left-hand side of the mapping
                        # table and check if we can find these
                        for nx_path, modifier in NxUserFromListOfDict.items():
                            if nx_path not in ("IGNORE", "UNCLEAR"):
                                trg = variadic_path_to_specific_path(nx_path, identifier)
                                res = apply_modifier(modifier, user_dict)
                                if res is not None:
                                    template[trg] = res
                        user_id += 1
        return template

    def parse_laser_pulser_details(self, template: dict) -> dict:
        """Copy data in pulser section."""
        # additional laser-specific details only relevant when the laser was used
        src = "atom_probe/pulser/pulse_mode"
        if src in self.yml.keys():
            if self.yml[src] == "voltage":
                return template
        else:
            return template
        src = "atom_probe/pulser/laser_source"
        if src in self.yml.keys():
            if isinstance(self.yml[src], list):
                if all(isinstance(entry, dict) for entry in self.yml[src]) is True:
                    laser_id = 1
                    # custom schema delivers a list of dictionaries...
                    trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/pulser" \
                          f"/SOURCE[source{laser_id}]"
                    for laser_dict in self.yml[src]:
                        if "name" in laser_dict.keys():
                            template[f"{trg}/name"] = laser_dict["name"]
                        quantities = ["power", "pulse_energy", "wavelength"]
                        for quant in quantities:
                            if isinstance(laser_dict[quant], dict):
                                if ("value" in laser_dict[quant].keys()) \
                                        and ("unit" in laser_dict[quant].keys()):
                                    template[f"{trg}/{quant}"] \
                                        = laser_dict[quant]["value"]
                                    template[f"{trg}/{quant}/@units"] \
                                        = laser_dict[quant]["unit"]
                        laser_id += 1
        return template

    def parse_other_sections(self, template: dict) -> dict:
        """Copy data from custom schema into template."""
        for nx_path, modifier in NxApmElnInput.items():
            if nx_path not in ("IGNORE", "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [self.entry_id, 1])
                res = apply_modifier(modifier, self.yml)
                if res is not None:
                    template[trg] = res
        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_sample_composition(template)
        self.parse_user_section(template)
        self.parse_laser_pulser_details(template)
        self.parse_other_sections(template)
        return template
