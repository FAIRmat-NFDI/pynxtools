#!/usr/bin/env python3
"""Parse metadata in specific custom NOMAD OASIS ELN schema to an NXem NXS."""

# -*- coding: utf-8 -*-
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

# pylint: disable=E1101

import numpy as np

import flatdict as fd

import yaml

# import matplotlib.pyplot as plt
# from ase.data import atomic_numbers
from ase.data import chemical_symbols


def get_dct_value(flat_dict: fd.FlatDict, keyword_path: str):
    """Extract value from a dict nest under keyword_path."""
    # keyword_path = 'NXapm/entry/specimen/name'  #'/name'
    # keyword_path = 'NXapm/entry/atom_probe/pulser/pulse_frequency/value'
    # dct = yml
    # print(keyword_path)
    is_leaf = (keyword_path in flat_dict.keys()) \
        & (isinstance(flat_dict[keyword_path], fd.FlatDict) is False)
    if is_leaf is True:
        return flat_dict[keyword_path]
    return None


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

    def __init__(self, file_name: str):
        # file_name = 'eln_data.yaml'
        with open(file_name, 'r') as stream:
            self.yml = fd.FlatDict(yaml.safe_load(stream), delimiter=':')

    def parse_entry_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        src = "entry"
        appdef_version = "NeXus 2022.06 commitID "
        appdef_version += "d9574a8f90626a929c677f1505729d1751170989 NXem"
        appdef_name = "NXem"
        assert self.yml[src + ":attr_version"] == appdef_version, \
            "Facing an ELN schema instance whose NXem version is not supported!"
        assert self.yml[src + ":definition"] == appdef_name, \
            "Facing an ELN schema instance whose appdef name is not NXem!"
        req_field_names = [
            "program", "start_time", "end_time", "experiment_identifier"]
        opt_field_names = [
            "experiment_description", "experiment_documentation"]
        for required in req_field_names:
            assert required in self.yml[src].keys(), \
                required + " is a required field but not found in ELN input!"
        assert "program__attr_version" in self.yml[src].keys(), \
            "program__attr_version is a required field but not found in ELN input!"

        trg = "/ENTRY[entry]/"
        template[trg + "@version"] = appdef_version
        template[trg + "definition"] = appdef_name
        template[trg + "program/@version"] \
            = get_dct_value(self.yml, src + ":program__attr_version")
        field_names = req_field_names + opt_field_names
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] \
                    = get_dct_value(self.yml, src + ":" + field_name)
        return template

    def parse_operator_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        src = "operator"
        assert isinstance(self.yml[src], list), \
            "Facing an ELN schema instance with an incorrect operator section!"
        assert len(self.yml[src]) >= 1, \
            "Facing an ELN schema instance with an empty operator section!"
        req_field_names = ["name", "email"]
        opt_field_names = [
            "affiliation", "address", "orcid", "telephone_number", "role",
            "social_media_name", "social_media_platform"]
        # there is a bug in NXem, it should not be operator but NXuser
        # USER(NXuser) therefore we need to overwrite for now
        # and take only the first entry
        for operators in self.yml[src]:
            for required in req_field_names:
                assert required in operators.keys(), \
                    required + " is a required field but not found in ELN input!"

        field_names = req_field_names + opt_field_names
        # if there is only a single operator
        trg = "/ENTRY[entry]/operator/"
        for field_name in field_names:
            if field_name in self.yml[src][0].keys():
                template[trg + field_name] = self.yml[src][0][field_name]
        # else ##MK::NXem appdef has to be fixed
        # remove OPERATOR prefix to (NXuser) !
        # user_id = 1
        # for user in yml[src]:
        #     trg = "/ENTRY[entry]/USER[user_" + str(user_id) + "]"
        #     for field_name in field_names:
        #         if field_name in user.keys():
        #             print(user[field_name])
        #             template[trg + field_name] = user[field_name]
        #         user_id += 1
        return template

    def parse_sample_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        src = "sample"
        assert isinstance(self.yml[src + ":atom_types"], list), \
            "Facing an ELN schema instance with an incorrect atom_types info!"
        assert len(self.yml[src + ":atom_types"]) >= 1, \
            "Facing an ELN schema instance with an empty atom_types info!"
        for symbol in self.yml[src + ":atom_types"]:
            assert isinstance(symbol, str), \
                "Facing an atom_types list entry which is not a string!"
            assert (symbol in chemical_symbols) & (symbol != 'X'), \
                "Facing an atom_types list entry which is not an element!"
        thickness_exists = ("thickness:value" in self.yml[src].keys()) \
            and ("thickness:unit" in self.yml[src].keys())
        assert thickness_exists is True, \
            "Required field thickness is available in the ELN data!"
        density_exists = ("density:value" in self.yml[src].keys()) \
            and ("density:unit" in self.yml[src].keys())
        req_field_names = [
            "method", "name", "sample_history", "preparation_date"]
        opt_field_names = [
            "short_title", "description"]
        for required in req_field_names:
            assert required in self.yml[src].keys(), \
                required + " is a required field but not found in ELN input!"

        trg = "/ENTRY[entry]/SAMPLE/"
        template[trg + "atom_types"] = self.yml[src + ":atom_types"]
        template[trg + "thickness"] \
            = np.float64(get_dct_value(self.yml, src + ":thickness:value"))
        template[trg + "thickness/@units"] \
            = get_dct_value(self.yml, src + ":thickness:unit")
        field_names = req_field_names + opt_field_names
        for field_name in field_names:
            if field_name in self.yml[src].keys():
                template[trg + field_name] \
                    = get_dct_value(self.yml, src + ":" + field_name)
        # optional value fields
        if density_exists is True:
            template[trg + "density"] \
                = np.float64(self.yml["sample:density:value"])
            template[trg + "density/@units"] = self.yml["sample:density:unit"]
        return template

    def parse_instrument_section(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        src = "em_lab"
        error_msg = " is a required field but not found in ELN input!"
        assert "instrument_name" in self.yml[src].keys(), \
            "instrument_name " + error_msg
        assert "manufacturer:name" in self.yml[src].keys(), \
            "manufacturer:name" + error_msg
        assert "manufacturer:model" in self.yml[src].keys(), \
            "manufacturer:model" + error_msg
        voltage_exists = \
            ("ebeam_column:electron_gun:voltage:unit" in self.yml[src].keys()) \
            and ("ebeam_column:electron_gun:voltage:value" in self.yml[src].keys())
        assert voltage_exists is True, \
            "voltage" + error_msg
        beam_current_exists = \
            ("electro_magnetical_system_em:beam_current:unit" in self.yml[src].keys()) \
            and ("electro_magnetical_system_em:beam_current:value" in self.yml[src].keys())
        assert beam_current_exists is True, \
            "beam_current" + error_msg
        camera_length_exists = \
            ("optical_system_em:camera_length:unit" in self.yml[src].keys()) \
            and ("optical_system_em:camera_length:value" in self.yml[src].keys())
        assert camera_length_exists is True, \
            "camera_length" + error_msg
        magnification_exists = \
            ("optical_system_em:magnification:unit" in self.yml[src].keys()) \
            and ("optical_system_em:magnification:value" in self.yml[src].keys())
        assert magnification_exists is True, \
            "magnification" + error_msg
        src = "em_lab:aperture"
        assert "em_lab:aperture" in self.yml.keys(), \
            "aperture" + error_msg
        assert len(self.yml[src]) >= 1, \
            "At least one  aperture (the condenser) aperture has to be defined!"
        assert "name" in self.yml[src][0].keys(), \
            "aperture name" + error_msg
        assert "value" in self.yml[src][0].keys(), \
            "aperture value" + error_msg
        aperture_size_exists = \
            ("unit" in self.yml[src][0]["value"].keys()) \
            and ("value" in self.yml[src][0]["value"].keys())
        assert aperture_size_exists is True, \
            "aperture value (size) " + error_msg

        trg = "/ENTRY[entry]/em_lab/"
        src = "em_lab:"
        template[trg + "instrument_name"] = self.yml[src + "instrument_name"]
        template[trg + "location"] = self.yml[src + "location"]
        trg = "/ENTRY[entry]/em_lab/MANUFACTURER[manufacturer]/"
        src = "em_lab:manufacturer:"
        field_names = ["name", "model"]
        for field_name in field_names:
            template[trg + field_name] = self.yml[src + field_name]
            # this is why ideally the fields in the ELN should get the same
            # name as in the application definition
        trg = "/ENTRY[entry]/em_lab/EBEAM_COLUMN[ebeam_column]"
        trg += "/SOURCE[electron_gun]/"
        src = "em_lab:ebeam_column:electron_gun:"
        template[trg + "voltage"] = np.float64(self.yml[src + "voltage:value"])
        template[trg + "voltage/@units"] = self.yml[src + "voltage:unit"]
        trg = "/ENTRY[entry]/em_lab/EBEAM_COLUMN[ebeam_column]"
        trg += "/APERTURE_EM[aperture_em]/"
        src = "em_lab:aperture"
        template[trg + "name"] = self.yml[src][0]["name"]
        template[trg + "value"] = np.float64(self.yml[src][0]["value"]["value"])
        template[trg + "value/@units"] = self.yml[src][0]["value"]["unit"]
        trg = "/ENTRY[entry]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/"
        src = "em_lab:optical_system_em:"
        template[trg + "camera_length"] \
            = np.float64(self.yml[src + "camera_length:value"])
        template[trg + "camera_length/@units"] \
            = self.yml[src + "camera_length:unit"]
        template[trg + "magnification"] \
            = np.float64(self.yml[src + "magnification:value"])
        template[trg + "magnification/@units"] \
            = self.yml[src + "magnification:unit"]
        # beam current
        trg = "/ENTRY[entry]/em_lab/DETECTOR[detector]/"
        src = "em_lab:detector:"
        template[trg + "type"] = self.yml[src + "type"]
        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance."""
        self.parse_entry_section(template)
        self.parse_operator_section(template)
        self.parse_sample_section(template)
        self.parse_instrument_section(template)
        return template
