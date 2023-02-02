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
"""Wrapping multiple parsers for vendor files with ranging definition files."""

# pylint: disable=E1101

from typing import Dict, Any

import numpy as np

from ifes_apt_tc_data_modeling.utils.utils \
    import create_isotope_vector, isotope_vector_to_nuclid_list, \
    isotope_vector_to_human_readable_name
from ifes_apt_tc_data_modeling.utils.definitions \
    import MAX_NUMBER_OF_ATOMS_PER_ION, MQ_EPSILON

from ifes_apt_tc_data_modeling.rng.rng_reader import ReadRngFileFormat

from ifes_apt_tc_data_modeling.rrng.rrng_reader import ReadRrngFileFormat


def add_unknown_iontype(template: dict, entry_id: int) -> dict:
    """Add default unknown iontype."""
    # all unidentifiable ions are mapped on the unknown type
    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/"
    trg += "ranging/peak_identification/ION[ion0]/"
    ivec = create_isotope_vector([])
    template[trg + "isotope_vector"] \
        = np.reshape(np.asarray(ivec, np.uint16),
                     (1, MAX_NUMBER_OF_ATOMS_PER_ION))
    # template[trg + "isotope_vector/@units"] = ""
    template[trg + "charge_state"] = np.int8(0)
    template[trg + "charge_state/@units"] = "eV"
    template[trg + "mass_to_charge_range"] \
        = np.reshape(np.asarray([0.0, MQ_EPSILON], np.float32), (1, 2))
    template[trg + "mass_to_charge_range/@units"] = "Da"
    nuclid_list = isotope_vector_to_nuclid_list(ivec)
    template[trg + "nuclid_list"] = np.asarray(nuclid_list, np.uint16)
    # template[trg + "nuclid_list/@units"] = ""
    template[trg + "name"] = isotope_vector_to_human_readable_name(ivec, 0)

    return template


def add_standardize_molecular_ions(ion_lst: list, template: dict, entry_id: int) -> dict:
    """Added standard formatted molecular ion entries."""
    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/ranging/"
    template[trg + "number_of_ion_types"] = np.int32(len(ion_lst))

    ion_id = 1
    trg = "/ENTRY[entry" + str(entry_id) + "]/atom_probe/ranging/peak_identification/"
    for ion in ion_lst:
        path = trg + "ION[ion" + str(ion_id) + "]/"

        template[path + "isotope_vector"] \
            = np.reshape(np.asarray(ion.isotope_vector.typed_value, np.uint16),
                                   (1, MAX_NUMBER_OF_ATOMS_PER_ION))
        # template[path + "isotope_vector/@units"] = ""
        template[path + "charge_state"] = np.int8(ion.charge.typed_value)
        template[path + "charge_state/@units"] = ion.charge.unit
        template[path + "mass_to_charge_range"] \
            = np.array(ion.ranges.typed_value, np.float32)
        template[path + "mass_to_charge_range/@units"] = ion.ranges.unit
        template[path + "nuclid_list"] = ion.nuclid_list.typed_value
        # template[path + "nuclid_list/@units"] = ""
        template[path + "name"] = ion.name.typed_value
        ion_id += 1
    return template


def extract_data_from_rng_file(file_name: str, template: dict, entry_id: int) -> dict:
    """Add those required information which an RNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print("Extracting data from RNG file: " + file_name)
    rangefile = ReadRngFileFormat(file_name)

    # ion indices are on the interval [0, 256)
    assert len(rangefile.rng["molecular_ions"].keys()) <= np.iinfo(np.uint8).max + 1, \
        "Current implementation does not support more than 256 ion types"

    add_standardize_molecular_ions(
        rangefile.rng["molecular_ions"], template, entry_id)

    return template


def extract_data_from_rrng_file(file_name: str, template: dict, entry_id) -> dict:
    """Add those required information which an RRNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print("Extracting data from RRNG file: " + file_name)
    rangefile = ReadRrngFileFormat(file_name)
    # rangefile.read_rrng()

    # ion indices are on the interval [0, 256)
    assert len(rangefile.rrng["molecular_ions"]) <= np.iinfo(np.uint8).max + 1, \
        "Current implementation does not support more than 256 ion types"

    add_standardize_molecular_ions(
        rangefile.rrng["molecular_ions"], template, entry_id)

    return template


class ApmRangingDefinitionsParser:  # pylint: disable=R0903
    """Wrapper for multiple parsers for vendor specific files."""

    def __init__(self, file_name: str, entry_id: int):
        self.meta: Dict[str, Any] = {}
        self.meta["file_format"] = "none"
        self.meta["file_name"] = file_name
        self.meta["entry_id"] = entry_id
        index = file_name.lower().rfind(".")
        if index >= 0:
            mime_type = file_name.lower()[index + 1::]
            if mime_type == "rng":
                self.meta["file_format"] = "rng"
            if mime_type == "rrng":
                self.meta["file_format"] = "rrng"

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        # resolve the next two program references more informatively
        trg = "/ENTRY[entry" + str(self.meta["entry_id"]) + "]/atom_probe/ranging/"
        template[trg + "program"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document with which program it was generated!"
        template[trg + "program/@version"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document with which program version it was generated!"
        template[trg + "number_of_ion_types"] = 0
        template[trg + "number_of_ion_types/@units"] \
            = ""
        template[trg + "maximum_number_of_atoms_per_molecular_ion"] = np.uint32(32)
        template[trg + "maximum_number_of_atoms_per_molecular_ion/@units"] \
            = ""

        # mass_to_charge_distribution will be filled by default plot
        # background_quantification data are not available in RNG/RRNG files
        # peak_search_and_deconvolution data are not available in RNG/RRNG files

        trg = "/ENTRY[entry" + str(self.meta["entry_id"]) + "]/atom_probe/"
        trg += "ranging/peak_identification/"
        template[trg + "program"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document which program was used for peak_identification!"
        template[trg + "program/@version"] \
            = "unclear, " + self.meta["file_format"] + " range file format" \
            + " does not document which program version was used for peak_identification!"

        add_unknown_iontype(template, self.meta["entry_id"])

        if self.meta["file_name"] != "" and self.meta["file_format"] != "none":
            if self.meta["file_format"] == "rng":
                extract_data_from_rng_file(
                    self.meta["file_name"],
                    template,
                    self.meta["entry_id"])
            if self.meta["file_format"] == "rrng":
                extract_data_from_rrng_file(
                    self.meta["file_name"],
                    template,
                    self.meta["entry_id"])
        return template
