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

# pylint: disable=no-member

import flatdict as fd

import numpy as np

import yaml

from ase.data import chemical_symbols

from pynxtools.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_ADEF_NAME, NX_APM_ADEF_VERSION, NX_APM_EXEC_NAME, NX_APM_EXEC_VERSION


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
                self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=":")
        else:
            self.entry_id = 1
            self.file_name = ""
            self.yml = {}

    def parse_entry(self, template: dict) -> dict:
        """Copy data in entry section."""
        # print("Parsing entry...")
        trg = f"/ENTRY[entry{self.entry_id}]/"
        src = "entry"
        if isinstance(self.yml[src], fd.FlatDict):
            if (self.yml[f"{src}:attr_version"] == NX_APM_ADEF_VERSION) \
                    and (self.yml[f"{src}:definition"] == NX_APM_ADEF_NAME):
                template[f"{trg}@version"] = NX_APM_ADEF_VERSION
                template[f"{trg}definition"] = NX_APM_ADEF_NAME
                template[f"{trg}PROGRAM[program1]/program"] = NX_APM_EXEC_NAME
                template[f"{trg}PROGRAM[program1]/program/@version"] = NX_APM_EXEC_VERSION
            if ("program" in self.yml[src].keys()) \
                    and ("program__attr_version" in self.yml[src].keys()):
                template[f"{trg}PROGRAM[program2]/program"] \
                    = self.yml[f"{src}:program"]
                template[f"{trg}PROGRAM[program2]/program/@version"] \
                    = self.yml[f"{src}:program__attr_version"]

        required_field_names = ["experiment_identifier", "run_number",
                                "operation_mode"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        optional_field_names = ["start_time", "end_time",
                                "experiment_description", "experiment_documentation"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_user(self, template: dict) -> dict:
        """Copy data in user section."""
        # print("Parsing user...")
        src = "user"
        if "user" in self.yml.keys():
            if len(self.yml[src]) >= 1:
                user_id = 1
                for user_list in self.yml[src]:
                    trg = f"/ENTRY[entry{self.entry_id}]/USER[user{user_id}]/"

                    required_field_names = ["name"]
                    for field_name in required_field_names:
                        if field_name in user_list.keys():
                            template[f"{trg}{field_name}"] = user_list[field_name]

                    optional_field_names = ["email", "affiliation", "address",
                                            "orcid", "orcid_platform",
                                            "telephone_number", "role",
                                            "social_media_name", "social_media_platform"]
                    for field_name in optional_field_names:
                        if field_name in user_list.keys():
                            template[f"{trg}{field_name}"] = user_list[field_name]
                    user_id += 1

        return template

    def parse_specimen(self, template: dict) -> dict:
        """Copy data in specimen section."""
        # print("Parsing sample...")
        src = "specimen"
        trg = f"/ENTRY[entry{self.entry_id}]/specimen/"
        if isinstance(self.yml[src], fd.FlatDict):
            if (isinstance(self.yml[f"{src}:atom_types"], list)) \
                    and (len(self.yml[src + ":atom_types"]) >= 1):
                atom_types_are_valid = True
                for symbol in self.yml[f"{src}:atom_types"]:
                    valid = isinstance(symbol, str) \
                        and (symbol in chemical_symbols) and (symbol != "X")
                    if valid is False:
                        atom_types_are_valid = False
                        break
                if atom_types_are_valid is True:
                    template[f"{trg}atom_types"] \
                        = ", ".join(list(self.yml[f"{src}:atom_types"]))

        required_field_names = ["name", "sample_history", "preparation_date"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        optional_field_names = ["short_title", "description"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_instrument_header(self, template: dict) -> dict:
        """Copy data in instrument_header section."""
        # print("Parsing instrument header...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/"
        if isinstance(self.yml[src], fd.FlatDict):
            required_field_names = ["instrument_name", "status"]
            for field_name in required_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]
            optional_field_names = ["location"]
            for field_name in optional_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

            float_field_names = ["flight_path_length", "field_of_view"]
            for field_name in float_field_names:
                if (f"{field_name}:value" in self.yml[src].keys()) \
                        and (f"{field_name}:unit" in self.yml[src].keys()):
                    template[f"{trg}{field_name}"] \
                        = np.float64(self.yml[f"{src}:{field_name}:value"])
                    template[f"{trg}{field_name}/@units"] \
                        = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_fabrication(self, template: dict) -> dict:
        """Copy data in fabrication section."""
        # print("Parsing fabrication...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/FABRICATION[fabrication]/"
        required_field_names = ["fabrication_vendor", "fabrication_model"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                suffix = field_name.replace("fabrication_", "")
                template[f"{trg}{suffix}"] = self.yml[f"{src}:{field_name}"]

        optional_field_names = ["fabrication_identifier", "fabrication_capabilities"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                suffix = field_name.replace("fabrication_", "")
                template[f"{trg}{suffix}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_analysis_chamber(self, template: dict) -> dict:
        """Copy data in analysis_chamber section."""
        # print("Parsing analysis chamber...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/analysis_chamber/"
        float_field_names = ["analysis_chamber_pressure"]
        for field_name in float_field_names:
            if (f"{field_name}:value" in self.yml[src].keys()) \
                    and (f"{field_name}:unit" in self.yml[src].keys()):
                suffix = field_name.replace("analysis_chamber_", "")
                template[f"{trg}{suffix}"] \
                    = np.float64(self.yml[f"{src}:{field_name}:value"])
                template[f"{trg}{suffix}/@units"] = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_reflectron(self, template: dict) -> dict:
        """Copy data in reflectron section."""
        # print("Parsing reflectron...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/REFLECTRON[reflectron]/"
        required_field_names = ["reflectron_applied"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                suffix = field_name.replace("reflectron_", "")
                template[f"{trg}{suffix}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_local_electrode(self, template: dict) -> dict:
        """Copy data in local_electrode section."""
        # print("Parsing local electrode...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/local_electrode/"
        required_field_names = ["local_electrode_name"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                suffix = field_name.replace("local_electrode_", "")
            template[f"{trg}{suffix}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_detector(self, template: dict) -> dict:
        """Copy data in ion_detector section."""
        # print("Parsing detector...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/ion_detector/"
        required_field_names = ["ion_detector_type", "ion_detector_name",
                                "ion_detector_model", "ion_detector_serial_number"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                suffix = field_name.replace("ion_detector_", "")
                template[f"{trg}{suffix}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_stage_lab(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage_lab...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/stage_lab/"
        if isinstance(self.yml[src], fd.FlatDict):
            required_value_fields = ["stage_lab_base_temperature"]
            for field_name in required_value_fields:
                if (f"{field_name}:value" in self.yml[src].keys()) \
                        and (f"{field_name}:unit" in self.yml[src].keys()):
                    suffix = field_name.replace("stage_lab_", "")
                    template[f"{trg}{suffix}"] \
                        = np.float64(self.yml[f"{src}:{field_name}:value"])
                    template[f"{trg}{suffix}/@units"] \
                        = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_specimen_monitoring(self, template: dict) -> dict:
        """Copy data in specimen_monitoring section."""
        # print("Parsing specimen_monitoring...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/specimen_monitoring/"
        if isinstance(self.yml[src], fd.FlatDict):
            required_field_names = ["specimen_monitoring_detection_rate"]
            for field_name in required_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}detection_rate"] \
                        = np.float64(self.yml[f"{src}:{field_name}"])
                float_field_names = ["specimen_monitoring_initial_radius",
                                     "specimen_monitoring_shank_angle"]
                for float_field_name in float_field_names:
                    if (f"{float_field_name}:value" in self.yml[src].keys()) \
                            and (f"{float_field_name}:unit" in self.yml[src].keys()):
                        suffix = float_field_name.replace("specimen_monitoring_", "")
                        template[f"{trg}{suffix}"] \
                            = np.float64(self.yml[f"{src}:{float_field_name}:value"])
                        template[f"{trg}{suffix}/@units"] \
                            = self.yml[f"{src}:{float_field_name}:unit"]

        return template

    def parse_control_software(self, template: dict) -> dict:
        """Copy data in control software section."""
        # print("Parsing control software...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/control_software/"
        if isinstance(self.yml[src], fd.FlatDict):
            prefix = "control_software"
            if (f"{prefix}_program" in self.yml[src].keys()) \
                    and (f"{prefix}_program__attr_version" in self.yml[src].keys()):
                template[f"{trg}PROGRAM[program1]/program"] \
                    = self.yml[f"{src}:{prefix}_program"]
                template[f"{trg}PROGRAM[program1]/program/@version"] \
                    = self.yml[f"{src}:{prefix}_program__attr_version"]

        return template

    def parse_pulser(self, template: dict) -> dict:
        """Copy data in pulser section."""
        # print("Parsing pulser...")
        src = "atom_probe:pulser"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/pulser/"
        if isinstance(self.yml[src], fd.FlatDict):
            if "pulse_mode" in self.yml[src].keys():
                pulse_mode = self.yml[f"{src}:pulse_mode"]
                template[f"{trg}pulse_mode"] = pulse_mode
            else:  # can not parse selectively as pulse_mode was not documented
                return template

            if "pulse_fraction" in self.yml[src].keys():
                template[f"{trg}pulse_fraction"] \
                    = np.float64(self.yml[f"{src}:pulse_fraction"])

            float_field_names = ["pulse_frequency"]
            for field_name in float_field_names:
                if (f"{field_name}:value" in self.yml[src].keys()) \
                        and (f"{field_name}:unit" in self.yml[src].keys()):
                    template[f"{trg}{field_name}"] \
                        = np.float64(self.yml[f"{src}:{field_name}:value"])
                    template[f"{trg}{field_name}/@units"] \
                        = self.yml[f"{src}:{field_name}:unit"]
            # additionally required data for laser and laser_and_voltage runs
            if pulse_mode != "voltage":
                trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/" \
                      f"pulser/SOURCE[laser_source1]/"
                if "laser_source_name" in self.yml[src].keys():
                    template[f"{trg}name"] = self.yml[f"{src}:laser_source_name"]

                float_field_names = ["laser_source_wavelength",
                                     "laser_source_power",
                                     "laser_source_pulse_energy"]
                for field_name in float_field_names:
                    if (f"{field_name}:value" in self.yml[src].keys()) \
                            and (f"{field_name}:unit" in self.yml[src].keys()):
                        suffix = field_name.replace("laser_source_", "")
                        template[f"{trg}{suffix}"] \
                            = np.float64(self.yml[f"{src}:{field_name}:value"])
                        template[f"{trg}{suffix}/@units"] \
                            = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_reconstruction(self, template: dict) -> dict:
        """Copy data in reconstruction section."""
        # print("Parsing reconstruction...")
        src = "reconstruction"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/reconstruction/"
        if ("program" in self.yml[src].keys()) \
                and ("program__attr_version" in self.yml[src].keys()):
            template[f"{trg}PROGRAM[program1]/program"] \
                = self.yml[f"{src}:program"]
            template[f"{trg}PROGRAM[program1]/program/@version"] \
                = self.yml[f"{src}:program__attr_version"]

        required_field_names = ["protocol_name", "parameter",
                                "crystallographic_calibration"]
        for field_name in required_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_ranging(self, template: dict) -> dict:
        """Copy data in ranging section."""
        # print("Parsing ranging...")
        src = "ranging"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/ranging/"
        if ("program" in self.yml[src].keys()) \
                and ("program__attr_version" in self.yml[src].keys()):
            template[f"{trg}PROGRAM[program1]/program"] = self.yml[f"{src}:program"]
            template[f"{trg}PROGRAM[program1]/program/@version"] \
                = self.yml[f"{src}:program__attr_version"]

        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_entry(template)
        self.parse_user(template)
        self.parse_specimen(template)
        self.parse_instrument_header(template)
        self.parse_fabrication(template)
        self.parse_analysis_chamber(template)
        self.parse_reflectron(template)
        self.parse_local_electrode(template)
        self.parse_detector(template)
        self.parse_stage_lab(template)
        self.parse_specimen_monitoring(template)
        self.parse_control_software(template)
        self.parse_pulser(template)
        self.parse_reconstruction(template)
        self.parse_ranging(template)
        return template
