#!/usr/bin/env python3
"""Wrapping multiple parsers for vendor files with ranging definition files."""

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

from typing import Dict

import numpy as np

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_utils \
    import unhash_isotope  # , hash_isotope

from nexusparser.tools.dataconverter.readers.apm.utils.apm_nexus_base_classes \
    import NxObject

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_rng_reader \
    import ReadRngFileFormat

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_rrng_reader \
    import ReadRrngFileFormat


def extract_data_from_rng_file(file_name: str, template: dict) -> dict:
    """Add those required information which an RNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print('Extracting data from RNG file: ' + file_name)
    rangefile = ReadRngFileFormat(file_name)

    rangefile.read_rng()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    trg = '/ENTRY[entry]/atom_probe/ranging/'
    template[trg + 'number_of_ion_types'] \
        = np.int32(len(rangefile.rng['ions'].keys()))

    ion_id = 1
    trg = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rng['ions'].values():
        path = trg + 'ION[ion' + str(ion_id) + ']/'

        template[path + 'isotope_vector'] \
            = np.array(ion_obj.isotope_vector.value, np.uint16)
        template[path + 'isotope_vector/@units'] = 'NX_UNITLESS'
        template[path + 'charge_state'] = np.int8(ion_obj.charge_state.value)
        template[path + 'charge_state/@units'] = 'eV'
        template[path + 'mass_to_charge_range'] \
            = np.array(ion_obj.ranges.value, np.float32)
        template[path + 'mass_to_charge_range/@units'] = ion_obj.ranges.unit
        nuclid_list = np.zeros([2, 32], np.uint16)
        ivec = ion_obj.isotope_vector.value.flatten()
        i = 0
        for hash_value in ivec:
            if hash_value != 0:
                ZN = unhash_isotope(int(hash_value))
                if ZN[1] > 0: # convention if only the element known
                    nuclid_list[0, i] = ZN[0] + ZN[1]
                else:
                    nuclid_list[0, i] = 0
                nuclid_list[1, i] = ZN[0]
            i += 1
        template[path + "nuclid_list"] = nuclid_list
        template[path + "nuclid_list/@units"] = "NX_UNITLESS"
        # template[path + 'ion_type'] = np.uint8(ion_id)
        # template[path + 'name'] = ion_obj.name.value
        # charge_state and name is not included in rng rangefiles
        ion_id += 1

    return template


def extract_data_from_rrng_file(file_name: str, template: dict) -> dict:
    """Add those required information which an RRNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print('Extracting data from RRNG file: ' + file_name)
    rangefile = ReadRrngFileFormat(file_name)

    rangefile.read_rrng()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rrng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    trg = '/ENTRY[entry]/atom_probe/ranging/'
    template[trg + "number_of_ion_types"] \
        = np.int32(len(rangefile.rrng['ions'].keys()))

    ion_id = 1
    trg = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rrng['ions'].values():
        path = trg + 'ION[ion' + str(ion_id) + ']/'

        template[path + 'isotope_vector'] \
            = np.array(ion_obj.isotope_vector.value, np.uint16)
        template[path + 'isotope_vector/@units'] = 'NX_UNITLESS'
        template[path + 'charge_state'] = np.int8(ion_obj.charge_state.value)
        template[path + 'charge_state/@units'] = 'eV'
        template[path + 'mass_to_charge_range'] \
            = np.array(ion_obj.ranges.value, np.float32)
        template[path + 'mass_to_charge_range/@units'] = ion_obj.ranges.unit
        nuclid_list = np.zeros([2, 32], np.uint16)
        ivec = ion_obj.isotope_vector.value.flatten()
        i = 0
        for hash_value in ivec:
            if hash_value != 0:
                ZN = unhash_isotope(int(hash_value))
                if ZN[1] > 0: # convention if only the element known
                    nuclid_list[0, i] = ZN[0] + ZN[1]
                else:
                    nuclid_list[0, i] = 0
                nuclid_list[1, i] = ZN[0]
            i += 1
        template[path + "nuclid_list"] = np.asarray(nuclid_list, np.uint16)
        template[path + "nuclid_list/@units"] = "NX_UNITLESS"
        # template[path + 'ion_type'] = np.uint8(ion_id)
        # template[path + 'name'] = ion_obj.name.value
        # charge_state and name is not included in rrng rangefiles
        ion_id += 1

    return template


class ApmRangingDefinitionsParser:  # pylint: disable=R0903
    """Wrapper for multiple parsers for vendor specific files."""

    def __init__(self, file_name: str):
        self.meta: Dict[str, NxObject] = {}
        self.meta["file_format"] = 'none'
        self.meta["file_name"] = file_name
        index = file_name.lower().rfind('.')
        if index >= 0:
            mime_type = file_name.lower()[index + 1::]
            if mime_type == 'rng':
                self.meta["file_format"] = 'rng'
            if mime_type == 'rrng':
                self.meta["file_format"] = 'rrng'

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        # resolve the next two program references more informatively
        trg = "/ENTRY[entry]/atom_probe/ranging/"
        template[trg + "program"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document with which program it was generated!"
        template[trg + "program/@version"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document with which program version it was generated!"
        template[trg + "number_of_ion_types"] = 0
        template[trg + "number_of_ion_types/@units"] \
            = "NX_UNITLESS"
        template[trg + "maximum_number_of_atoms_per_molecular_ion"] = np.uint32(32)
        template[trg + 'maximum_number_of_atoms_per_molecular_ion/@units'] \
            = 'NX_UNITLESS'

        # mass_to_charge_distribution will be filled by default plot
        # background_quantification data are not available in RNG/RRNG files
        # peak_search_and_deconvolution data are not available in RNG/RRNG files

        trg = "/ENTRY[entry]/atom_probe/ranging/peak_identification/"
        template[trg + "program"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document which program was used for peak_identification!"
        template[trg + "program/@version"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document which program version was used for peak_identification!"

        path = trg + "ION[ion0]/"
        template[path + 'isotope_vector'] \
            = np.reshape(np.asarray(([0] * 32), np.uint16), (1, 32))
        template[path + 'isotope_vector/@units'] = "NX_UNITLESS"
        template[path + 'charge_state'] = np.int8(0)
        template[path + 'charge_state/@units'] = 'eV'
        template[path + 'mass_to_charge_range'] \
            = np.reshape(np.asarray([0.0, 0.001], np.float32), (1, 2))
        template[path + 'mass_to_charge_range/@units'] = "Da"
        nuclid_list = np.zeros([2, 32], np.uint16)
        template[path + "nuclid_list"] = nuclid_list
        template[path + "nuclid_list/@units"] = "NX_UNITLESS"

        if self.meta["file_name"] != '' and self.meta["file_format"] != 'none':
            if self.meta["file_format"] == 'rng':
                extract_data_from_rng_file(
                    self.meta["file_name"],
                    template)
            if self.meta["file_format"] == 'rrng':
                extract_data_from_rrng_file(
                    self.meta["file_name"],
                    template)
        return template
