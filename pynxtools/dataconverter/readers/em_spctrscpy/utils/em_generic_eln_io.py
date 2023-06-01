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

# pylint: disable=no-member,duplicate-code

import numpy as np

import flatdict as fd

import yaml

from ase.data import chemical_symbols

from pynxtools.dataconverter.readers.em_spctrscpy.utils.em_versioning \
    import NX_EM_ADEF_NAME, NX_EM_ADEF_VERSION, NX_EM_EXEC_NAME, NX_EM_EXEC_VERSION


class NxEmNomadOasisElnSchemaParser:
    """Parse eln_data.yaml dump file content generated from a NOMAD OASIS YAML.

    This parser implements a design where an instance of a specific NOMAD
    custom schema ELN template is used to fill pieces of information which
    are typically not contained in files from technology partners
    (e.g. bcf, emd, dm3, ...). Until now, this custom schema and
    the NXem application definition do not use a fully harmonized vocabulary.
    Therefore, the here hardcoded implementation is needed which maps specifically
    named pieces of information from the custom schema instance on named fields
    in an instance of NXem

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

    def parse_entry_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # print("Parsing entry...")
        trg = f"/ENTRY[entry{self.entry_id}]/"
        src = "entry"
        if isinstance(self.yml[src], fd.FlatDict):
            if (self.yml[f"{src}:attr_version"] == NX_EM_ADEF_VERSION) \
                    and (self.yml[f"{src}:definition"] == NX_EM_ADEF_NAME):
                template[f"{trg}@version"] = NX_EM_ADEF_VERSION
                template[f"{trg}definition"] = NX_EM_ADEF_NAME
                template[f"{trg}PROGRAM[program1]/program"] = NX_EM_EXEC_NAME
                template[f"{trg}PROGRAM[program1]/program/@version"] = NX_EM_EXEC_VERSION
            if ("program" in self.yml[src].keys()) \
                    and ("program__attr_version" in self.yml[src].keys()):
                template[f"{trg}PROGRAM[program2]/program"] = self.yml[f"{src}:program"]
                template[f"{trg}PROGRAM[program2]/program/@version"] \
                    = self.yml[f"{src}:program__attr_version"]

        field_names = ["experiment_identifier", "start_time", "end_time",
                       "experiment_description", "experiment_documentation"]
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_user_section(self, template: dict) -> dict:
        """Copy data in user section."""
        # print("Parsing user...")
        src = "user"
        if isinstance(self.yml[src], list):
            if len(self.yml[src]) >= 1:
                user_id = 1
                for user_list in self.yml[src]:
                    char_field_names = ["name", "email", "affiliation", "address",
                                        "orcid", "orcid_platform",
                                        "telephone_number", "role",
                                        "social_media_name", "social_media_platform"]

                    trg = f"/ENTRY[entry{self.entry_id}]/USER[user{user_id}]/"
                    for field_name in char_field_names:
                        if field_name in user_list.keys():
                            template[f"{trg}{field_name}"] = user_list[f"{field_name}"]
                    user_id += 1

        return template

    def parse_sample_section(self, template: dict) -> dict:
        """Copy data in sample section."""
        # check if required fields exists and are valid
        # print("Parsing sample...")
        src = "sample"
        trg = f"/ENTRY[entry{self.entry_id}]/sample/"
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

        char_req_field_names = ["method", "name", "sample_history", "preparation_date"]
        for field_name in char_req_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]
        char_opt_field_names = ["short_title", "description"]
        for field_name in char_opt_field_names:
            if field_name in self.yml[src].keys():
                template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        float_field_names = ["thickness", "density"]
        for field_name in float_field_names:
            if (f"{field_name}:value" in self.yml[src].keys()) \
                    and (f"{field_name}:unit" in self.yml[src].keys()):
                template[f"{trg}{field_name}"] \
                    = np.float64(self.yml[f"{src}:{field_name}:value"])
                template[f"{trg}{field_name}/@units"] = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_coordinate_system_section(self, template: dict) -> dict:
        """Define the coordinate systems to be used."""
        # ##MK::the COORDINATE_SYSTEM_SET section depends often on conventions
        # which are neither explicitly documented in instances of
        # files from technology partners nor many ELNs
        # E.g. SEM/EBSD TSL, the specific coordinate system conventions used
        # are defined in the famous "coin selector GUI window from TSL e.g."
        # but these values do not get stored in technology partner files.
        # Oxford Instruments nowadays stores coordinate systems implicitly by
        # communicating the specification of their file format (like H5OINA)
        # print("Parsing coordinate system...")
        prefix = f"/ENTRY[entry{self.entry_id}]/" \
                 f"COORDINATE_SYSTEM_SET[coordinate_system_set]/"
        # this is likely not yet matching how it should be in NeXus
        grpnm = f"{prefix}TRANSFORMATIONS[laboratory]/"
        cs_xyz = np.asarray(
            [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], np.float64)
        cs_names = ["x", "y", "z"]
        for i in np.arange(0, 3):
            trg = f"{grpnm}AXISNAME[{cs_names[i]}]"
            template[trg] = cs_xyz[:, i]
            template[f"{trg}/@offset"] = np.asarray([0., 0., 0.], np.float64)
            template[f"{trg}/@offset_units"] = "m"
            template[f"{trg}/@depends_on"] = "."

        msg = '''
              This way of defining coordinate systems is only a small example of what
              is possible and how it can be done. More discussion among members of
              FAIRmat Areas A, B, C, and D and the EM community is needed !
              '''
        template[f"{prefix}@comment"] = msg

        return template

    def parse_instrument_header_section(self, template: dict) -> dict:
        """Copy data in instrument header section."""
        # check if required fields exists and are valid
        print("Parsing instrument header...")
        src = "em_lab"
        if isinstance(self.yml[src], fd.FlatDict):
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/"

            char_field_names = ["instrument_name", "location"]
            for field_name in char_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        src = "em_lab:fabrication"
        if isinstance(self.yml[src], fd.FlatDict):
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/FABRICATION[fabrication]/"
            char_field_names = ["vendor", "model", "identifier", "capabilities"]
            for field_name in char_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        return template

    def parse_ebeam_column_section(self, template: dict) -> dict:
        """Copy data in ebeam_column section."""
        # print("Parsing ebeam_column...")

        src = "em_lab:ebeam_column:electron_source"
        if isinstance(self.yml[src], fd.FlatDict):
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/" \
                  f"EBEAM_COLUMN[ebeam_column]/electron_source/"

            float_field_names = ["voltage"]
            for field_name in float_field_names:
                if (f"{field_name}:value" in self.yml[src].keys()) \
                        and (f"{field_name}:unit" in self.yml[src].keys()):
                    template[f"{trg}{field_name}"] \
                        = np.float64(self.yml[f"{src}:{field_name}:value"])
                    template[f"{trg}{field_name}/@units"] \
                        = self.yml[f"{src}:{field_name}:unit"]

            char_field_names = ["emitter_type"]
            for field_name in char_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

        src = "em_lab:ebeam_column:aperture_em"
        if isinstance(self.yml[src], list):
            if len(self.yml[src]) >= 1:
                aperture_id = 1
                for aperture in self.yml[src]:
                    trg = f"/ENTRY[entry{self.entry_id}]/em_lab/" \
                          f"EBEAM_COLUMN[ebeam_column]/" \
                          f"APERTURE_EM[aperture_em{aperture_id}]/"
                    if "value" in aperture.keys():
                        template[f"{trg}value"] = np.float64(aperture["value"])
                    char_field_names = ["name", "description"]
                    for field_name in char_field_names:
                        if field_name in aperture.keys():
                            template[f"{trg}{field_name}"] = aperture[f"{field_name}"]
                    aperture_id += 1

        # the above-mentioned snippet is a blue-print for lenses also...

        # corrector_cs
        src = "em_lab:ebeam_column:aberration_correction"
        trg = f"/ENTRY[entry{self.entry_id}]/em_lab/" \
              f"EBEAM_COLUMN[ebeam_column]/aberration_correction/"
        if "applied" in self.yml[src].keys():
            template[f"{trg}applied"] = self.yml[f"{src}:applied"]

        # the inject of corrector metadata is highly instrument specific, e.g.
        # for Nion microscopes these settings are available from nionswift
        # for ThermoFisher/FEI microscopes like the Titan there is an HTML output file
        # from the Zemlin tableau analysis

        # NEW ISSUE: support parsing of corrector data (pre2 for Thilo)

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
        if isinstance(self.yml[src], fd.FlatDict):
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/" \
                  f"OPTICAL_SYSTEM_EM[optical_system_em]/"

            char_field_names = ["beam_current_description"]
            for field_name in char_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

            float_field_names = ["camera_length", "magnification", "defocus",
                                 "semi_convergence_angle", "working_distance",
                                 "beam_current"]
            for field_name in float_field_names:
                if (f"{field_name}:value" in self.yml[src].keys()) \
                        and (f"{field_name}:unit" in self.yml[src].keys()):
                    template[f"{trg}{field_name}"] \
                        = np.float64(self.yml[f"{src}:{field_name}:value"])
                    template[f"{trg}{field_name}/@units"] \
                        = self.yml[f"{src}:{field_name}:unit"]

        return template

    def parse_detector_section(self, template: dict) -> dict:
        """Copy data in detector section."""
        # print("Parsing detector...")
        src = "em_lab:detector"
        if not isinstance(self.yml[src], list):
            return template

        if len(self.yml[src]) >= 1:
            detector_id = 1
            for detector in self.yml[src]:
                if isinstance(detector, dict):
                    trg = f"/ENTRY[entry{self.entry_id}]/em_lab/" \
                          f"DETECTOR[detector{detector_id}]/"

                    char_field_names = ["local_name"]
                    for field_name in char_field_names:
                        if field_name in detector.keys():
                            template[f"{trg}{field_name}"] = detector[f"{field_name}"]
                detector_id += 1

        return template

    def parse_stage_lab_section(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage_lab...")
        src = "em_lab:stage_lab"
        if isinstance(self.yml[src], fd.FlatDict):
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/stage_lab/"

            char_field_names = ["name"]
            for field_name in char_field_names:
                if field_name in self.yml[src].keys():
                    template[f"{trg}{field_name}"] = self.yml[f"{src}:{field_name}"]

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
