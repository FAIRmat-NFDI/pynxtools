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
from ifes_apt_tc_data_modeling.utils.utils \
    import create_isotope_vector, isotope_vector_to_nuclid_list, \
    isotope_vector_to_human_readable_name
from ifes_apt_tc_data_modeling.utils.definitions \
    import MAX_NUMBER_OF_ATOMS_PER_ION, MQ_EPSILON, MAX_NUMBER_OF_ION_SPECIES
from ifes_apt_tc_data_modeling.env.env_reader import ReadEnvFileFormat
from ifes_apt_tc_data_modeling.fig.fig_reader import ReadFigTxtFileFormat
from ifes_apt_tc_data_modeling.pyccapt.pyccapt_reader import ReadPyccaptRangingFileFormat
from ifes_apt_tc_data_modeling.rng.rng_reader import ReadRngFileFormat
from ifes_apt_tc_data_modeling.rrng.rrng_reader import ReadRrngFileFormat
from pynxtools.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_EXEC_NAME, NX_APM_EXEC_VERSION
from pynxtools.dataconverter.readers.apm.utils.apm_define_io_cases \
    import VALID_FILE_NAME_SUFFIX_RANGE

WARNING_TOO_MANY_DEFINITIONS \
    = f"WARNING::Range file contains more than {MAX_NUMBER_OF_ION_SPECIES} " \
      f"WARNING::definitions! This is often a signature of duplicates or " \
      f"WARNING::contradicting definitions."


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
    template[f"{trg}mass_to_charge_range/@units"] = "u"
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
            np.asarray(ion.isotope_vector.values, np.uint16),
            (1, MAX_NUMBER_OF_ATOMS_PER_ION))
        template[f"{path}charge_state"] = np.int8(ion.charge_state.values)
        template[f"{path}mass_to_charge_range"] \
            = np.asarray(ion.ranges.values, np.float32)
        template[f"{path}mass_to_charge_range/@units"] = "u"  # ion.ranges.unit
        template[f"{path}nuclid_list"] = ion.nuclid_list.values
        template[f"{path}name"] = ion.name.values

        if ion.charge_state_model["n_cand"] > 0:
            path = f"{trg}ION[ion{ion_id}]/charge_state_analysis/"
            template[f"{path}min_abundance"] \
                = np.float64(ion.charge_state_model["min_abundance"])
            template[f"{path}min_abundance_product"] \
                = np.float64(ion.charge_state_model["min_abundance_product"])
            template[f"{path}min_half_life"] \
                = np.float64(ion.charge_state_model["min_half_life"])
            template[f"{path}min_half_life/@units"] = "s"
            template[f"{path}sacrifice_isotopic_uniqueness"] \
                = np.uint8(ion.charge_state_model["sacrifice_isotopic_uniqueness"])
            if ion.charge_state_model["n_cand"] == 1:
                template[f"{path}isotope_matrix"] \
                    = np.asarray(ion.charge_state_model["isotope_matrix"], np.uint16)
                template[f"{path}charge_state_vector"] \
                    = np.int8(ion.charge_state_model["charge_state_vector"])
                template[f"{path}mass_vector"] \
                    = np.float64(ion.charge_state_model["mass_vector"])
                template[f"{path}mass_vector/@units"] \
                    = "u"
                template[f"{path}natural_abundance_product_vector"] \
                    = np.float64(ion.charge_state_model["nat_abun_prod_vector"])
                template[f"{path}min_half_life_vector"] \
                    = np.float64(ion.charge_state_model["min_half_life_vector"])
                template[f"{path}min_half_life_vector/@units"] \
                    = "s"
            else:
                template[f"{path}isotope_matrix"] \
                    = {"compress": np.asarray(ion.charge_state_model["isotope_matrix"],
                                              np.uint16), "strength": 1}
                template[f"{path}charge_state_vector"] \
                    = {"compress": np.asarray(ion.charge_state_model["charge_state_vector"],
                                              np.int8), "strength": 1}
                template[f"{path}mass_vector"] \
                    = {"compress": np.asarray(ion.charge_state_model["mass_vector"],
                                              np.float64), "strength": 1}
                template[f"{path}mass_vector/@units"] \
                    = "u"
                template[f"{path}natural_abundance_product_vector"] \
                    = {"compress": np.asarray(ion.charge_state_model["nat_abun_prod_vector"],
                                              np.float64), "strength": 1}
                template[f"{path}min_half_life_vector"] \
                    = {"compress": np.asarray(ion.charge_state_model["min_half_life_vector"],
                                              np.float64), "strength": 1}
                template[f"{path}min_half_life_vector/@units"] \
                    = "s"
        ion_id += 1

    trg = f"/ENTRY[entry{entry_id}]/atom_probe/ranging/"
    template[f"{trg}number_of_ion_types"] = np.uint32(ion_id)
    return template

# modify the template to take into account ranging
# ranging is currently not resolved recursively because
# ranging(NXprocess) is a group which has a minOccurs=1, \er
#     maxOccurs="unbounded" set of possible named
# NXion members, same case for more than one operator
# ion indices are on the interval [0, 256)


def extract_data_from_env_file(file_path: str, template: dict, entry_id: int) -> dict:
    """Add those required information which a ENV file has."""
    print(f"Extracting data from ENV file: {file_path}")
    rangefile = ReadEnvFileFormat(file_path)
    if len(rangefile.env["molecular_ions"]) > np.iinfo(np.uint8).max + 1:
        print(WARNING_TOO_MANY_DEFINITIONS)

    add_standardize_molecular_ions(
        rangefile.env["molecular_ions"], template, entry_id)
    return template


def extract_data_from_fig_txt_file(file_path: str, template: dict, entry_id: int) -> dict:
    """Add those required information which a FIG.TXT file has."""
    print(f"Extracting data from FIG.TXT file: {file_path}")
    rangefile = ReadFigTxtFileFormat(file_path)
    if len(rangefile.fig["molecular_ions"]) > np.iinfo(np.uint8).max + 1:
        print(WARNING_TOO_MANY_DEFINITIONS)

    add_standardize_molecular_ions(
        rangefile.fig["molecular_ions"], template, entry_id)
    return template


def extract_data_from_pyccapt_file(file_path: str, template: dict, entry_id: int) -> dict:
    """Add those required information which a pyccapt/ranging HDF5 file has."""
    print(f"Extracting data from pyccapt/ranging HDF5 file: {file_path}")
    rangefile = ReadPyccaptRangingFileFormat(file_path)
    if len(rangefile.rng["molecular_ions"]) > np.iinfo(np.uint8).max + 1:
        print(WARNING_TOO_MANY_DEFINITIONS)

    add_standardize_molecular_ions(
        rangefile.rng["molecular_ions"], template, entry_id)
    return template


def extract_data_from_rng_file(file_path: str, template: dict, entry_id: int) -> dict:
    """Add those required information which an RNG file has."""
    print(f"Extracting data from RNG file: {file_path}")
    rangefile = ReadRngFileFormat(file_path)
    if len(rangefile.rng["molecular_ions"]) > np.iinfo(np.uint8).max + 1:
        print(WARNING_TOO_MANY_DEFINITIONS)

    add_standardize_molecular_ions(
        rangefile.rng["molecular_ions"], template, entry_id)
    return template


def extract_data_from_rrng_file(file_path: str, template: dict, entry_id) -> dict:
    """Add those required information which an RRNG file has."""
    print(f"Extracting data from RRNG file: {file_path}")
    rangefile = ReadRrngFileFormat(file_path)
    if len(rangefile.rrng["molecular_ions"]) > np.iinfo(np.uint8).max + 1:
        print(WARNING_TOO_MANY_DEFINITIONS)

    add_standardize_molecular_ions(
        rangefile.rrng["molecular_ions"], template, entry_id)
    return template


class ApmRangingDefinitionsParser:  # pylint: disable=too-few-public-methods
    """Wrapper for multiple parsers for vendor specific files."""

    def __init__(self, file_path: str, entry_id: int):
        self.meta: Dict[str, Any] = {"file_format": None,
                                     "file_path": file_path,
                                     "entry_id": entry_id}
        for suffix in VALID_FILE_NAME_SUFFIX_RANGE:
            if file_path.lower().endswith(suffix) is True:
                self.meta["file_format"] = suffix
                break
        if self.meta["file_format"] is None:
            raise ValueError(f"{file_path} is not a supported ranging definitions file!")

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
        template[f"{trg}maximum_number_of_atoms_per_molecular_ion"] \
            = np.uint32(MAX_NUMBER_OF_ATOMS_PER_ION)

        # mass_to_charge_distribution will be filled by default plot
        # background_quantification data are not available in RNG/RRNG files
        # peak_search_and_deconvolution data are not available in RNG/RRNG files

        trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/" \
              f"ranging/peak_identification/"
        template[f"{trg}PROGRAM[program1]/program"] = NX_APM_EXEC_NAME
        template[f"{trg}PROGRAM[program1]/program/@version"] = NX_APM_EXEC_VERSION

        add_unknown_iontype(template, self.meta["entry_id"])

        if self.meta["file_path"] != "" and self.meta["file_format"] is not None:
            if self.meta["file_format"] == ".env":
                extract_data_from_env_file(self.meta["file_path"],
                                           template, self.meta["entry_id"])
            elif self.meta["file_format"] == ".fig.txt":
                extract_data_from_fig_txt_file(self.meta["file_path"],
                                               template, self.meta["entry_id"])
            elif self.meta["file_format"] == "range_.h5":
                extract_data_from_pyccapt_file(self.meta["file_path"],
                                               template, self.meta["entry_id"])
            elif self.meta["file_format"] == ".rng":
                extract_data_from_rng_file(self.meta["file_path"],
                                           template, self.meta["entry_id"])
            elif self.meta["file_format"] == ".rrng":
                extract_data_from_rrng_file(self.meta["file_path"],
                                            template, self.meta["entry_id"])
            else:
                trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
                template[f"{trg}number_of_ion_types"] = 1
        else:
            trg = f"/ENTRY[entry{self.meta['entry_id']}]/atom_probe/ranging/"
            template[f"{trg}number_of_ion_types"] = 1

        self.update_atom_types_ranging_definitions_based(template)
        return template
