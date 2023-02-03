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

# pylint: disable=E1101

import flatdict as fd

import numpy as np

import yaml

from ase.data import chemical_symbols

from nexusutils.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_ADEF_NAME, NX_APM_ADEF_VERSION, NX_APM_EXEC_NAME, NX_APM_EXEC_VERSION


class NxApmNomadOasisElnSchemaParser:  # pylint: disable=R0903
    """Parse eln_data.yaml dump file content generated from a NOMAD OASIS YAML.

    It is planned that the ELN and NeXus application definition schemes
    will eventually merge into one. In this case and also in general
    making a data artefact to comply with a specific application definition
    demands that required groups/field/attribute need to and optional ones
    may be filled into the NeXus file.
    Therefore, in order to match these constraints of a specific appdef
    like NXapm (here implemented) demands that the required entries are
    in the yaml, if they cannot be filled by vendor files
    (e.g. pos, epos, apt, rng, rrng, ...)
    when the ELN and NeXus appdef schema syntax have been harmonized
    the same keywords will be used. So it is possible that the function
    here just parses specific (eventually nested) keyword, values from
    the ELN yaml file, as in this case anyway all content in a yaml file
    that is not also available in the appdef will be ignored

    given that the syntax for nomadOASIS ELN and NeXus schemes is
    as of 2022/06/28 not yet fully harmonized plus we dont want
    to create an extra blocker in sprint 9, we carry the values hardcoded
    """

    def __init__(self, file_name: str, entry_id: int):
        assert "eln_data" in file_name, \
            "Argument file_name should be eln_data* YAML !"
        assert entry_id > 0, "Argument entry_id has to be > 0 !"
        self.file_name = file_name
        self.entry_id = entry_id
        with open(self.file_name, "r", encoding="utf-8") as stream:
            self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=":")

    def parse_entry(self, template: dict) -> dict:
        """Copy data in entry section."""
        # print("Parsing entry...")
        trg = f"/ENTRY[entry{self.entry_id}]/"
        src = "entry"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        appdef_name = NX_APM_ADEF_NAME
        appdef_version = NX_APM_ADEF_VERSION

        # check for required fields based on the above-mentioned NXem version
        assert self.yml[src + ":attr_version"] == appdef_version, \
            "Facing an ELN schema instance whose NXem version is not supported!"
        template[trg + "@version"] = appdef_version
        assert self.yml[src + ":definition"] == appdef_name, \
            "Facing an ELN schema instance whose appdef name is not NXem!"
        template[trg + "definition"] = appdef_name
        assert "program" in self.yml[src].keys(), \
            "program is a required field but not found in ELN input!"
        template[trg + "program"] \
            = "source: " + self.yml[src + ":program"] + ", parser: " \
            + NX_APM_EXEC_NAME
        assert "program__attr_version" in self.yml[src].keys(), \
            "program__attr_version is a required field but not found in ELN input!"
        template[trg + "program/@version"] \
            = "source: " + self.yml[src + ":program__attr_version"] + ", parser: " \
            + NX_APM_EXEC_VERSION
        required_field_names = [
            "experiment_identifier",
            "run_number",
            "operation_mode"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + " is a required field but not found in ELN input!"
            template[trg + field_name] \
                = self.yml[src + ":" + field_name]
        optional_field_names = [
            "start_time", "end_time",
            "experiment_description", "experiment_documentation"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] \
                    = self.yml[src + ":" + field_name]

        return template

    def parse_user(self, template: dict) -> dict:
        """Copy data in user section."""
        # print("Parsing user...")
        src = "user"
        assert isinstance(self.yml[src], list), \
            "Facing an ELN schema instance with an incorrect operator section!"
        assert len(self.yml[src]) >= 1, \
            "Facing an ELN schema instance with an empty operator section!"
        user_id = 1
        for user_list in self.yml[src]:
            trg = f"/ENTRY[entry{self.entry_id}]/USER[user{user_id}]/"
            assert "name" in user_list.keys(), \
                "name is a required field but not found in ELN input!"
            template[trg + "name"] = user_list["name"]
            optional_field_names = [
                "email", "affiliation", "address", "orcid", "orcid_platform",
                "telephone_number", "role",
                "social_media_name", "social_media_platform"]
            for field_name in optional_field_names:
                if field_name in user_list.keys():
                    template[trg + field_name] \
                        = user_list[field_name]
            user_id += 1

        return template

    def parse_specimen(self, template: dict) -> dict:
        """Copy data in specimen section."""
        # print("Parsing sample...")
        src = "specimen"
        trg = f"/ENTRY[entry{self.entry_id}]/specimen/"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        assert isinstance(self.yml[src + ":atom_types"], list), \
            "Facing an ELN schema instance with an incorrect atom_types info!"
        assert len(self.yml[src + ":atom_types"]) >= 1, \
            "Facing an ELN schema instance with an empty atom_types info!"
        for symbol in self.yml[src + ":atom_types"]:
            assert isinstance(symbol, str), \
                "Facing an atom_types list entry which is not a string!"
            assert (symbol in chemical_symbols) and (symbol != "X"), \
                "Facing an atom_types list entry which is not an element!"
        template[trg + "atom_types"] \
            = ", ".join(list(self.yml[src + ":atom_types"]))

        required_field_names = ["name", "sample_history", "preparation_date"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + " is a required field but not found in ELN input!"
            template[trg + field_name] = self.yml[src + ":" + field_name]

        optional_field_names = ["short_title", "description"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] = self.yml[src + ":" + field_name]
        # optional value fields
        return template

    def parse_instrument_header(self, template: dict) -> dict:
        """Copy data in instrument_header section."""
        # print("Parsing instrument header...")
        src = "atom_probe"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/"
        assert "instrument_name" in self.yml[src].keys(), \
            "instrument_name " + error_msg
        template[trg + "instrument_name"] = self.yml[src + ":instrument_name"]
        if src + ":location" in self.yml.keys():
            template[trg + "location"] = self.yml[src + ":location"]

        fpl_exists = ("flight_path_length:value" in self.yml[src].keys()) \
            and ("flight_path_length:unit" in self.yml[src].keys())
        assert fpl_exists is True, \
            "flight_path_length " + error_msg
        template[trg + "flight_path_length"] \
            = np.float64(self.yml[src + ":" + "flight_path_length:value"])
        template[trg + "flight_path_length/@units"] \
            = self.yml[src + ":" + "flight_path_length:unit"]
        fov_exists = ("field_of_view:value" in self.yml[src].keys()) \
            and ("field_of_view:unit" in self.yml[src].keys())
        if fov_exists is True:
            template[trg + "field_of_view"] \
                = np.float64(self.yml[src + ":" + "field_of_view:value"])
            template[trg + "field_of_view/@units"] \
                = self.yml[src + ":" + "field_of_view:unit"]

        return template

    def parse_fabrication(self, template: dict) -> dict:
        """Copy data in fabrication section."""
        # print("Parsing fabrication...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/FABRICATION[fabrication]/"
        error_msg = " is a required field but not found in ELN input!"
        required_field_names = [
            "fabrication_vendor", "fabrication_model"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name.replace("fabrication_", "")] \
                = self.yml[src + ":" + field_name]

        optional_field_names = [
            "fabrication_identifier", "fabrication_capabilities"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name.replace("fabrication_", "")] \
                    = self.yml[src + ":" + field_name]

        return template

    def parse_analysis_chamber(self, template: dict) -> dict:
        """Copy data in analysis_chamber section."""
        # print("Parsing analysis chamber...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/analysis_chamber/"
        error_msg = " is a required field but not found in ELN input!"
        required_value_fields = ["analysis_chamber_pressure"]
        for field_name in required_value_fields:
            field_exists = (field_name + ":value" in self.yml[src].keys()) \
                and (field_name + ":unit" in self.yml[src].keys())
            assert field_exists is True, \
                field_name + error_msg
            template[trg + field_name.replace("analysis_chamber_", "")] \
                = np.float64(self.yml[src + ":" + field_name + ":value"])
            template[trg + field_name.replace("analysis_chamber_", "") + "/@units"] \
                = self.yml[src + ":" + field_name + ":unit"]

        return template

    def parse_reflectron(self, template: dict) -> dict:
        """Copy data in reflectron section."""
        # print("Parsing reflectron...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/REFLECTRON[reflectron]/"
        error_msg = " is a required field but not found in ELN input!"
        required_field_names = ["reflectron_applied"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name.replace("reflectron_", "")] \
                = self.yml[src + ":" + field_name]

        return template

    def parse_local_electrode(self, template: dict) -> dict:
        """Copy data in local_electrode section."""
        # print("Parsing local electrode...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/local_electrode/"
        error_msg = " is a required field but not found in ELN input!"
        required_field_names = ["local_electrode_name"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name.replace("local_electrode_", "")] \
                = self.yml[src + ":" + field_name]

        return template

    def parse_detector(self, template: dict) -> dict:
        """Copy data in ion_detector section."""
        # print("Parsing detector...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/ion_detector/"
        error_msg = " is a required field but not found in ELN input!"
        required_field_names = [
            "ion_detector_type",
            "ion_detector_name",
            "ion_detector_model",
            "ion_detector_serial_number"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name.replace("ion_detector_", "")] \
                = self.yml[src + ":" + field_name]
        return template

    def parse_stage_lab(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage_lab...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/stage_lab/"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        required_value_fields = ["stage_lab_base_temperature"]
        for field_name in required_value_fields:
            field_exists = (field_name + ":value" in self.yml[src].keys()) \
                and (field_name + ":unit" in self.yml[src].keys())
            assert field_exists is True, \
                field_name + error_msg
            template[trg + field_name.replace("stage_lab_", "")] \
                = np.float64(self.yml[src + ":" + field_name + ":value"])
            template[trg + field_name.replace("stage_lab_", "") + "/@units"] \
                = self.yml[src + ":" + field_name + ":unit"]

        return template

    def parse_specimen_monitoring(self, template: dict) -> dict:
        """Copy data in specimen_monitoring section."""
        # print("Parsing specimen_monitoring...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/specimen_monitoring/"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        any_required_fields = [
            "specimen_monitoring_detection_rate"]
        any_required_value_fields = [
            "specimen_monitoring_initial_radius",
            "specimen_monitoring_shank_angle"]
        # if any field is present all of the section have to be present
        section_exists = False
        if any_required_fields[0] in self.yml[src].keys():
            section_exists = True
        for field_name in any_required_value_fields:
            if field_name in self.yml[src].keys():
                section_exists = True

        if section_exists is True:
            # all required fields have to be there
            assert any_required_fields[0] in self.yml[src].keys(), \
                any_required_fields[0] + error_msg
            template[trg + "detection_rate"] \
                = np.float64(self.yml[src + ":" + any_required_fields[0]])
            template[trg + "detection_rate/@units"] = ""
            for field_name in any_required_value_fields:
                field_exists = (field_name + ":value" in self.yml[src].keys()) \
                    and (field_name + ":unit" in self.yml[src].keys())
                assert field_exists is True, \
                    field_name + error_msg
                template[
                    trg + field_name.replace("specimen_monitoring_", "")] \
                    = np.float64(self.yml[src + ":" + field_name + ":value"])
                template[trg + field_name.replace(
                    "specimen_monitoring_", "") + "/@units"] = self.yml[
                        src + ":" + field_name + ":unit"]

        return template

    def parse_control_software(self, template: dict) -> dict:
        """Copy data in control software section."""
        # print("Parsing control software...")
        src = "atom_probe"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/control_software/"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        assert "control_software_program" in self.yml[src].keys(), \
            "control_software_program " + error_msg
        template[trg + "program"] \
            = self.yml[src + ":control_software_program"]
        assert "control_software_program__attr_version" in self.yml[src].keys(), \
            "control_software_program__attr_version " + error_msg
        template[trg + "program/@version"] \
            = self.yml[src + ":control_software_program__attr_version"]

        return template

    def parse_pulser(self, template: dict) -> dict:
        """Copy data in pulser section."""
        # print("Parsing pulser...")
        src = "atom_probe:pulser"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/pulser/"
        error_msg = " is a required field but not found in ELN input!"
        # decisions depend on pulse_mode
        assert "pulse_mode" in self.yml[src].keys(), \
            "pulse_mode" + error_msg
        pulse_mode = self.yml[src + ":" + "pulse_mode"]
        template[trg + "pulse_mode"] = pulse_mode
        assert "pulse_fraction" in self.yml[src].keys(), \
            "pulse_fraction" + error_msg
        template[trg + "pulse_fraction"] = self.yml[src + ":" + "pulse_fraction"]
        template[trg + "pulse_fraction/@units"] = ""
        field_exists = ("pulse_frequency:value" in self.yml[src].keys()) \
            and ("pulse_frequency:unit" in self.yml[src].keys())
        assert field_exists is True, \
            "pulse_frequency" + error_msg
        template[trg + "pulse_frequency"] \
            = np.float64(self.yml[src + ":pulse_frequency:value"])
        template[trg + "pulse_frequency/@units"] \
            = self.yml[src + ":pulse_frequency:unit"]

        # additionally required data for laser and laser_and_voltage runs
        if pulse_mode != "voltage":
            trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/pulser/laser_gun/"
            assert "laser_gun_name" in self.yml[src].keys(), \
                "laser_gun_name" + error_msg
            template[trg + "name"] = self.yml[src + ":laser_gun_name"]
            required_field_names = [
                "laser_gun_wavelength",
                "laser_gun_pulse_energy"]
            for field_name in required_field_names:
                field_exists = (field_name + ":value" in self.yml[src].keys()) \
                    and (field_name + ":unit" in self.yml[src].keys())
                assert field_exists is True, \
                    field_name + error_msg
                template[trg + field_name.replace("laser_gun_", "")] \
                    = np.float64(self.yml[src + ":" + field_name + ":value"])
                template[trg + field_name.replace("laser_gun_", "") + "/@units"] \
                    = self.yml[src + ":" + field_name + ":unit"]
            optional_field_names = ["laser_gun_power"]
            for field_name in optional_field_names:
                field_exists = (field_name + ":value" in self.yml[src].keys()) \
                    and (field_name + ":unit" in self.yml[src].keys())
                if field_exists is True:
                    template[
                        trg + field_name.replace("laser_gun_", "")] \
                        = np.float64(self.yml[src + ":" + field_name + ":value"])
                    template[
                        trg + field_name.replace("laser_gun_", "") + "/@units"] \
                        = self.yml[src + ":" + field_name + ":unit"]

        return template

    def parse_reconstruction(self, template: dict) -> dict:
        """Copy data in reconstruction section."""
        # print("Parsing reconstruction...")
        src = "reconstruction"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/reconstruction/"
        error_msg = " is a required field but not found in ELN input!"
        assert "program" in self.yml[src].keys(), \
            "program" + error_msg
        template[trg + "program"] = self.yml[src + ":program"]
        assert "program__attr_version" in self.yml[src].keys(), \
            "program__attr_version" + error_msg
        template[trg + "program/@version"] \
            = self.yml[src + ":program__attr_version"]
        required_field_names = [
            "protocol_name",
            "parameter",
            "crystallographic_calibration"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name] = self.yml[src + ":" + field_name]

        return template

    def parse_ranging(self, template: dict) -> dict:
        """Copy data in ranging section."""
        # print("Parsing ranging...")
        src = "ranging"
        trg = f"/ENTRY[entry{self.entry_id}]/atom_probe/ranging/"
        error_msg = " is a required field but not found in ELN input!"
        assert "program" in self.yml[src].keys(), \
            "program" + error_msg
        template[trg + "program"] = self.yml[src + ":program"]
        assert "program__attr_version" in self.yml[src].keys(), \
            "program__attr_version" + error_msg
        template[trg + "program/@version"] \
            = self.yml[src + ":program__attr_version"]
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
