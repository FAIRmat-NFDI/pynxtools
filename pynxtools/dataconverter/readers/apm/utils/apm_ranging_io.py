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

# pylint: disable=no-member

from typing import Dict, Any

import numpy as np

from ase.data import chemical_symbols
# ase encodes the zeroth entry as the unknown element X to have
# atom_numbers all starting with 1 up to len(chemical_symbols) - 1

from ifes_apt_tc_data_modeling.utils.utils \
    import create_isotope_vector, isotope_vector_to_nuclid_list, \
    isotope_vector_to_human_readable_name

from ifes_apt_tc_data_modeling.utils.definitions \
    import MAX_NUMBER_OF_ATOMS_PER_ION, MQ_EPSILON

from ifes_apt_tc_data_modeling.rng.rng_reader import ReadRngFileFormat

from ifes_apt_tc_data_modeling.rrng.rrng_reader import ReadRrngFileFormat

from ifes_apt_tc_data_modeling.fig.fig_reader import ReadFigTxtFileFormat

from pynxtools.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_EXEC_NAME, NX_APM_EXEC_VERSION


def add_unknown_iontype(template: dict, entry_id: int) -> dict:
    """Add default unknown iontype."""
    # all unidentifiable ions are mapped on the unknown type
    trg = f"/ENTRY[entry{entry_id}]/atom_probe/ranging/" \
          f"peak_identification/ION[ion0]/"
    ivec = create_isotope_vector([])
    template[f"{trg}isotope_vector"] \
        = np.reshape(np.asarray(ivec, np.uint16), (1, MAX_NUMBER_OF_ATOMS_PER_ION))
    template[f"{trg}charge_state"] = np.int8(0)
    template[f"{trg}mass_to_charge_range"] \
        = np.reshape(np.asarray([0.0, MQ_EPSILON], np.float32), (1, 2))
    template[f"{trg}mass_to_charge_range/@units"] = "Da"
    nuclid_list = isotope_vector_to_nuclid_list(ivec)
    template[f"{trg}nuclid_list"] = np.asarray(nuclid_list, np.uint16)
    template[f"{trg}name"] = isotope_vector_to_human_readable_name(ivec, 0)

    return template


def add_standardize_molecular_ions(ion_lst: list, template: dict, entry_id: int) -> dict:
    """Added standard formatted molecular ion entries."""
    ion_id = 1
    trg = f"/ENTRY[entry{entry_id}]/atom_probe/ranging/peak_identification/"
    for ion in ion_lst:
        path = f"{trg}ION[ion{ion_id}]/"

        template[f"{path}isotope_vector"] = np.reshape(
            np.asarray(ion.isotope_vector.typed_value, np.uint16),
            (1, MAX_NUMBER_OF_ATOMS_PER_ION))
        template[f"{path}charge_state"] = np.int8(ion.charge_state.typed_value)
        template[f"{path}mass_to_charge_range"] \
            = np.array(ion.ranges.typed_value, np.float32)
        template[f"{path}mass_to_charge_range/@units"] = "Da"  # ion.ranges.unit
        template[f"{path}nuclid_list"] = ion.nuclid_list.typed_value
        template[f"{path}name"] = ion.name.typed_value

        path = f"{trg}ION[ion{ion_id}]/charge_state_model/"
        template[f"{path}min_abundance"] \
            = np.float64(ion.charge_state_model["min_abundance"])
        template[f"{path}min_abundance_product"] \
            = np.float64(ion.charge_state_model["min_abundance_product"])
        template[f"{path}min_half_life"] \
            = np.float64(ion.charge_state_model["min_half_life"])
        template[f"{path}min_half_life/@units"] = "s"
        template[f"{path}sacrifice_isotopic_uniqueness"] \
            = np.uint8(ion.charge_state_model["sacrifice_isotopic_uniqueness"])
        template[f"{path}isotope_matrix"] \
            = {"compress": np.array(ion.charge_state_model["isotope_matrix"],
                                    np.uint16), "strength": 1}
        template[f"{path}charge_state_vector"] \
            = {"compress": np.array(ion.charge_state_model["charge_state_vector"],
                                    np.int8), "strength": 1}
        template[f"{path}mass_vector"] \
            = {"compress": np.array(ion.charge_state_model["mass_vector"],
                                    np.float64), "strength": 1}
        template[f"{path}mass_vector/@units"] = "u"
        template[f"{path}natural_abundance_product_vector"] \
            = {"compress": np.array(ion.charge_state_model["nat_abun_prod_vector"],
                                    np.float64), "strength": 1}
        template[f"{path}min_half_life_vector"] \
            = {"compress": np.array(ion.charge_state_model["min_half_life_vector"],
                                    np.float64), "strength": 1}
        template[f"{path}min_half_life_vector/@units"] = "s"

        ion_id += 1

    trg = f"/ENTRY[entry{entry_id}]/atom_probe/ranging/"
    template[f"{trg}number_of_ion_types"] = np.uint32(ion_id)

    return template


def extract_data_from_rng_file(file_name: str, template: dict, entry_id: int) -> dict:
    """Add those required information which an RNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print(f"Extracting data from RNG file: {file_name}")
    rangefile = ReadRngFileFormat(file_name)

    # ion indices are on the interval [0, 256)
    assert len(rangefile.rng["molecular_ions"]) <= np.iinfo(np.uint8).max + 1, \
        "Current implementation does not support more than 256 ion types"

    add_standardize_molecular_ions(
        rangefile.rng["molecular_ions"], template, entry_id)

    return template


def extract_data_from_rrng_file(file_name: str, template: dict, entry_id) -> dict:
    """Add those required information which an RRNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \er
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print(f"Extracting data from RRNG file: {file_name}")
    rangefile = ReadRrngFileFormat(file_name)

    # ion indices are on the interval [0, 256)
    assert len(rangefile.rrng["molecular_ions"]) <= np.iinfo(np.uint8).max + 1, \
        "Current implementation does not support more than 256 ion types"

    add_standardize_molecular_ions(
        rangefile.rrng["molecular_ions"], template, entry_id)

    return template


def extract_data_from_fig_txt_file(file_name: str, template: dict, entry_id) -> dict:
    """Add those required information which an transcoded Matlab figure TXT file has."""
    print(f"Extracting data from FIG.TXT file: {file_name}")
    rangefile = ReadFigTxtFileFormat(file_name)

    # ion indices are on the interval [0, 256)
    assert len(rangefile.fig["molecular_ions"]) <= np.iinfo(np.uint8).max + 1, \
        "Current implementation does not support more than 256 ion types"

    add_standardize_molecular_ions(
        rangefile.fig["molecular_ions"], template, entry_id)

    return template


class ApmRangingDefinitionsParser:  # pylint: disable=too-few-public-methods
    """Wrapper for multiple parsers for vendor specific files."""

    def __init__(self, file_name: str, entry_id: int):
        self.meta: Dict[str, Any] = {}
        self.meta["file_format"] = "none"
        self.meta["file_name"] = file_name
        self.meta["entry_id"] = entry_id
        index = file_name.lower().rfind(".")
        if index >= 0:
            mime_type = file_name.lower()[index + 1::]
            self.meta["file_format"] = mime_type

    def update_atom_types_ranging_definitions_based(self, template: dict) -> dict:
        """Update the atom_types list in the specimen based on ranging defs."""
        number_of_ion_types = 1
        prefix = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
        if f"{prefix}number_of_ion_types" in template.keys():
            number_of_ion_types = template[f"{prefix}number_of_ion_types"]
        print(f"Auto-detecting elements from ranging {number_of_ion_types} ion types...")

        unique_atom_numbers = set()
        max_atom_number = len(chemical_symbols) - 1
        prefix = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/" \
                 f"ranging/peak_identification/"
        for ion_id in np.arange(1, number_of_ion_types):
            trg = f"{prefix}ION[ion{ion_id}]/nuclid_list"
            if trg in template.keys():
                nuclid_list = template[trg][1, :]
                # second row of NXion/nuclid_list yields atom number to decode element
                for atom_number in nuclid_list:
                    if 0 < atom_number <= max_atom_number:
                        unique_atom_numbers.add(atom_number)
        print(f"Unique atom numbers are: {list(unique_atom_numbers)}")
        unique_elements = set()
        for atom_number in unique_atom_numbers:
            unique_elements.add(chemical_symbols[atom_number])
        print(f"Unique elements are: {list(unique_elements)}")

        atom_types_str = ", ".join(list(unique_elements))
        if atom_types_str != "":
            trg = f"/ENTRY[entry{self.meta['entry_id']}]/specimen/"
            template[f"{trg}atom_types"] = atom_types_str

        return template

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        # resolve the next two program references more informatively
        trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
        template[f"{trg}maximum_number_of_atoms_per_molecular_ion"] = np.uint32(32)

        # mass_to_charge_distribution will be filled by default plot
        # background_quantification data are not available in RNG/RRNG files
        # peak_search_and_deconvolution data are not available in RNG/RRNG files

        trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/" \
              f"ranging/peak_identification/"
        template[f"{trg}PROGRAM[program1]/program"] = NX_APM_EXEC_NAME
        template[f"{trg}PROGRAM[program1]/program/@version"] = NX_APM_EXEC_VERSION

        add_unknown_iontype(template, self.meta["entry_id"])

        if self.meta["file_name"] != "" and self.meta["file_format"] != "none":
            if self.meta["file_format"] == "rng":
                extract_data_from_rng_file(
                    self.meta["file_name"],
                    template,
                    self.meta["entry_id"])
            elif self.meta["file_format"] == "rrng":
                extract_data_from_rrng_file(
                    self.meta["file_name"],
                    template,
                    self.meta["entry_id"])
            elif self.meta["file_format"] == "txt":
                extract_data_from_fig_txt_file(
                    self.meta["file_name"],
                    template,
                    self.meta["entry_id"])
            else:
                trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
                template[f"{trg}number_of_ion_types"] = 1
        else:
            trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
            template[f"{trg}number_of_ion_types"] = 1

        self.update_atom_types_ranging_definitions_based(template)

        return template
