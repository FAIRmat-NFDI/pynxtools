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
"""Parse metadata in specific custom NOMAD OASIS ELN schema to an NXem NXS."""

# pylint: disable=E1101, R0801

import numpy as np

import flatdict as fd

import yaml

from ase.data import chemical_symbols

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_versioning \
    import NX_EM_ADEF_NAME, NX_EM_ADEF_VERSION, NX_EM_EXEC_NAME, NX_EM_EXEC_VERSION


class NxEmNomadOasisElnSchemaParser:
    """Parse eln_data.yaml dump file content generated from a NOMAD OASIS YAML.

    It is planned that the ELN and NeXus application definition schemes
    will eventually merge into one. In this case and also in general
    making a data artifact to comply with a specific application definition
    demands that required groups/field/attribute need to and optional ones
    may be filled into the NeXus file
    therefore, in order to match these constraints of a specific appdef
    like NXem (here implemented) demands that the required entries are
    in the yaml, if they cannot be filled by vendor files
    (e.g. emd, bcf, ...)
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
        with open(file_name, "r", encoding="utf-8") as stream:
            self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=":")
        self.entry_id = entry_id

    def parse_entry_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        # print("Parsing entry...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/"
        src = "entry"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        appdef_name = NX_EM_ADEF_NAME
        appdef_version = NX_EM_ADEF_VERSION

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
            + NX_EM_EXEC_NAME
        assert "program__attr_version" in self.yml[src].keys(), \
            "program__attr_version is a required field but not found in ELN input!"
        template[trg + "program/@version"] \
            = "source: " + self.yml[src + ":program__attr_version"] + ", parser: " \
            + NX_EM_EXEC_VERSION
        assert "experiment_identifier" in self.yml[src].keys(), \
            "experiment_identifier is a required field but not found in ELN input!"
        template[trg + "experiment_identifier"] \
            = self.yml[src + ":experiment_identifier"]
        field_names = [
            "start_time", "end_time",
            "experiment_description", "experiment_documentation"]
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] = self.yml[src + ":" + field_name]
        return template

    def parse_user_section(self, template: dict) -> dict:
        """Copy data in user section."""
        # check if required fields exists and are valid
        # print("Parsing user...")
        src = "user"
        assert isinstance(self.yml[src], list), \
            "Facing an ELN schema instance with an incorrect operator section!"
        assert len(self.yml[src]) >= 1, \
            "Facing an ELN schema instance with an empty operator section!"
        user_id = 1
        for user_list in self.yml[src]:
            assert "name" in user_list.keys(), \
                "name is a required field but not found in ELN input!"
            trg = f"/ENTRY[entry{self.entry_id}]/USER[user{user_id}]/"
            template[trg + "name"] = user_list["name"]
            field_names = [
                "email", "affiliation", "address", "orcid", "orcid_platform",
                "telephone_number", "role",
                "social_media_name", "social_media_platform"]
            for field_name in field_names:
                if field_name in user_list.keys():
                    template[trg + field_name] = user_list[field_name]
            user_id += 1

        return template

    def parse_sample_section(self, template: dict) -> dict:
        """Copy data in sample section."""
        # check if required fields exists and are valid
        # print("Parsing sample...")
        src = "sample"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/sample/"
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
        thickness_exists = ("thickness:value" in self.yml[src].keys()) \
            and ("thickness:unit" in self.yml[src].keys())
        assert thickness_exists is True, \
            "Required field thickness is available in the ELN data!"
        template[trg + "thickness"] \
            = np.float64(self.yml[src + ":thickness:value"])
        template[trg + "thickness/@units"] = self.yml[src + ":thickness:unit"]
        required_field_names = [
            "method", "name", "sample_history", "preparation_date"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + " is a required field but not found in ELN input!"
            template[trg + field_name] = self.yml[src + ":" + field_name]

        optional_field_names = ["short_title", "description"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] = self.yml[src + ":" + field_name]
        # optional value fields
        density_exists = ("density:value" in self.yml[src].keys()) \
            and ("density:unit" in self.yml[src].keys())
        if density_exists is True:
            template[trg + "density"] = np.float64(self.yml["sample:density:value"])
            template[trg + "density/@units"] = self.yml["sample:density:unit"]
        return template

    def parse_coordinate_system_section(self, template: dict) -> dict:
        """Define the coordinate systems to be used."""
        # ##MK::the COORDINATE_SYSTEM_SET section depends often on conventions
        # which are neither explicitly documented in instances of
        # files from vendor software nor via ELNs, take for instance the example
        # of SEM/EBSD TSL, the specific coordinate system conventions used
        # are defined in the famous "coin selector GUI window from TSL e.g."
        # but these values are not stored in vendor files.
        # Oxford nowadays stores coordinate systems implicitly as the
        # standard defines the coordinate systems
        # for now this source code is only to fix an issue
        # with the current parser of handling optional parent group
        # required fields cases, as soon as this has been fixed, this section
        # should be moved out here
        # a more complete approach to document coordinate system conventions
        # completely will be made with the em_oim_ms parser
        # print("Parsing coordinate system...")
        prefix = f"/ENTRY[entry{self.entry_id}]/"
        prefix += "COORDINATE_SYSTEM_SET[coordinate_system_set]/"
        # this is likely not yet matching how it should be in NeXus
        grpnm = prefix + "TRANSFORMATIONS[laboratory]/"
        cs_xyz = np.asarray(
            [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], np.float64)
        cs_names = ["x", "y", "z"]
        for i in np.arange(0, 3):
            trg = grpnm + "AXISNAME[" + cs_names[i] + "]"
            template[trg] = cs_xyz[:, i]
            template[trg + "/@transformation_type"] = "translation"
            template[trg + "/@offset"] = np.asarray([0., 0., 0.], np.float64)
            template[trg + "/@offset_units"] = "m"
            template[trg + "/@depends_on"] = "."

        msg = '''
              This way of defining coordinate systems is only a small example of what
              is possible and how it can be done. More discussion among members of
              FAIRmat Area B/A and the EM community is needed!
              '''
        template[prefix + "@comment"] = msg
        return template

    def parse_instrument_header_section(self, template: dict) -> dict:
        """Copy data in instrument header section."""
        # check if required fields exists and are valid
        print("Parsing instrument header...")
        src = "em_lab"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
        assert "instrument_name" in self.yml[src].keys(), \
            "instrument_name " + error_msg
        template[trg + "instrument_name"] = self.yml[src + ":instrument_name"]
        if src + ":location" in self.yml.keys():
            template[trg + "location"] = self.yml[src + ":location"]

        src = "em_lab:fabrication"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/FABRICATION[fabrication]/"
        assert src in self.yml, \
            "em_lab:fabrication is a required group but not found in ELN input!"
        required_field_names = ["vendor", "model"]
        for field_name in required_field_names:
            assert field_name in self.yml[src].keys(), \
                field_name + error_msg
            template[trg + field_name] = self.yml[src + ":" + field_name]

        optional_field_names = ["identifier", "capabilities"]
        for field_name in optional_field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] = self.yml[src + ":" + field_name]
        return template

    def parse_ebeam_column_section(self, template: dict) -> dict:
        """Copy data in ebeam_column section."""
        # print("Parsing ebeam_column...")
        src = "em_lab:ebeam_column:electron_gun"
        assert isinstance(self.yml[src], fd.FlatDict), \
            src + " is a required group but not found in ELN input"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
        trg += "EBEAM_COLUMN[ebeam_column]/electron_gun/"
        error_msg = " is a required field but not found in ELN input!"
        voltage_exists = ("voltage:unit" in self.yml[src].keys()) \
            and ("voltage:value" in self.yml[src].keys())
        assert voltage_exists is True, \
            "voltage " + error_msg
        template[trg + "voltage"] = np.float64(self.yml[src + ":voltage:value"])
        template[trg + "voltage/@units"] = self.yml[src + ":voltage:unit"]
        assert "emitter_type" in self.yml[src].keys(), \
            "emitter_type" + error_msg
        template[trg + "emitter_type"] = self.yml[src + ":" + "emitter_type"]

        # apertures
        src = "em_lab:ebeam_column:aperture_em"
        assert isinstance(self.yml[src], list), \
            "Required section " + src + " does not exist!"
        assert len(self.yml[src]) >= 1, \
            "At least one aperture has to be defined!"
        aperture_id = 1
        for aperture in self.yml[src]:
            trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
            trg += "EBEAM_COLUMN[ebeam_column]/"
            trg += "APERTURE_EM[aperture_em" + str(aperture_id) + "]/"
            assert "value" in aperture.keys(), \
                "value" + error_msg
            template[trg + "value"] = np.float64(aperture["value"])
            # template[trg + "value/@units"] = "NX_UNITLESS"
            assert "name" in aperture.keys(), \
                "name" + error_msg
            template[trg + "name"] = aperture["name"]
            if "description" in aperture.keys():
                template[trg + "description"] = aperture["description"]
            aperture_id += 1
        # the above-mentioned snippet is a blue-print for lenses also...

        # corrector
        src = "em_lab:ebeam_column:aberration_correction"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
        trg += "EBEAM_COLUMN[ebeam_column]/aberration_correction/"
        assert "applied" in self.yml[src].keys(), \
            "applied" + error_msg
        template[trg + "applied"] = self.yml[src + ":applied"]
        return template

    def parse_ibeam_column_section(self, template: dict) -> dict:
        """Copy data in ibeam_column section."""
        # print("Parsing ibeam_column...")
        return template

    def parse_ebeam_deflector_section(self, template: dict) -> dict:
        """Copy data in ebeam_deflector section."""
        # print("Parsing ebeam_deflector...")
        return template

    def parse_ibeam_deflector_section(self, template: dict) -> dict:
        """Copy data in ibeam_deflector section."""
        # print("Parsing ibeam_deflector...")
        return template

    def parse_optics_section(self, template: dict) -> dict:
        """Copy data in optical_system_em section."""
        # print("Parsing optics...")
        src = "em_lab:optical_system_em"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
        trg += "OPTICAL_SYSTEM_EM[optical_system_em]/"
        optional_char_fields = ["beam_current_description"]
        for field_name in optional_char_fields:
            if field_name in self.yml[src].keys():
                template[trg + field_name] = self.yml[src + ":" + field_name]
        optional_ndata_fields = [
            "camera_length", "magnification", "defocus",
            "semi_convergence_angle", "working_distance", "beam_current"]
        for field in optional_ndata_fields:
            if (src + field + ":value" in self.yml[src]) \
               and (src + field + ":unit" in self.yml[src]):
                template[trg + field] \
                    = np.float64(self.yml[src + ":" + field + ":value"])
                template[trg + field + "/@units"] \
                    = self.yml[src + ":" + field + ":unit"]
        return template

    def parse_detector_section(self, template: dict) -> dict:
        """Copy data in detector section."""
        # print("Parsing detector...")
        src = "em_lab:detector"
        assert isinstance(self.yml[src], list), \
            "Required section " + src + " does not exist!"
        assert len(self.yml[src]) >= 1, \
            "List section " + src + " needs to have at least one entry!"
        error_msg = " is a required field but not found in ELN input!"
        detector_id = 1
        for detector in self.yml[src]:
            assert isinstance(detector, dict), \
                "Detector metadata from ELN have to be a list!"
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/DETECTOR[detector{detector_id}]/"
            assert "type" in detector.keys(), "type" + error_msg
            template[trg + "type"] = detector["type"]
            detector_id += 1
        return template

    def parse_stage_lab_section(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage_lab...")
        src = "em_lab:stage_lab"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/stage_lab/"
        assert isinstance(self.yml[src], fd.FlatDict), \
            "Required section " + src + " does not exist!"
        error_msg = " is a required field but not found in ELN input!"
        required_char_fields = ["name"]
        for field_name in required_char_fields:
            assert field_name in self.yml[src].keys(), field_name + error_msg
            template[trg + field_name] = self.yml[src + ":" + field_name]
        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_entry_section(template)
        self.parse_user_section(template)
        self.parse_sample_section(template)
        self.parse_coordinate_system_section(template)
        self.parse_instrument_header_section(template)
        self.parse_ebeam_column_section(template)
        self.parse_ibeam_column_section(template)
        self.parse_ebeam_deflector_section(template)
        self.parse_ibeam_deflector_section(template)
        self.parse_optics_section(template)
        self.parse_detector_section(template)
        self.parse_stage_lab_section(template)

        return template
