#!/usr/bin/env python3
"""Set of utility tools for parsing file formats used by atom probe."""

# Also convenience functions are included which translate human-readable ion
# names into the isotope_vector description proposed by Kuehbach et al. in
# DOI: 10.1017/S1431927621012241 to the human-readable ion names which are use
# in P. Felfer et al.'s atom probe toolbox

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

# import re

# import typing

# from typing import Tuple

# import mmap

import git

# import numpy as np

# import numpy.typing as npt

# from ase.data import atomic_numbers
# from ase.data import chemical_symbols
# from ase.data.isotopes import download_isotope_data

# restrict the number distinguished ion types
# MAX_NUMBER_OF_ION_SPECIES = 256
# restrict number of atoms for molecular ion fragments
# MAX_NUMBER_OF_ATOMS_PER_ION = 32
# Da or atomic mass unit (amu)
# MQ_EPSILON = np.float32(1.0e-4)


def get_repo_last_commit() -> str:
    """Identify the last commit to the repository."""
    repo = git.Repo(search_parent_directories=True)
    sha = str(repo.head.object.hexsha)
    if sha != "":
        return sha
    return "unknown git commit id or unable to parse git reverse head"


# def rchop(string: str = '', suffix: str = '') -> str:
#     """Right-chop a string."""
#     if suffix and string.endswith(suffix):
#         return string[:-len(suffix)]
#     return string


# def hash_isotope(proton_number: int = 0,
#                  neutron_number: int = 0) -> int:
#     """Encode an isotope to a hashvalue."""
#     n_protons = np.uint16(proton_number)
#     n_neutrons = np.uint16(neutron_number)
#     assert n_protons >= np.uint16(0), 'Proton number >= 0 needed!'
#     assert n_protons < np.uint16(256), 'Proton number < 256 needed!'
#     assert n_neutrons >= np.uint16(0), 'Neutron number >= 0 needed!'
#     assert n_neutrons < np.uint16(256), 'Neutron number < 256 needed!'
#     return int(n_protons + (np.uint16(256) * n_neutrons))


# def unhash_isotope(hashval: int = 0) -> Tuple[int, int]:
#     """Decode a hashvalue to an isotope."""
#     assert isinstance(hashval, int), 'Hashval needs to be integer!'
#     val = np.uint16(hashval)
#     assert val >= np.uint16(0), 'Hashval needs to be an unsigned integer!'
#     assert val <= np.iinfo(np.uint16).max, \
#         'Hashval needs to map on an uint16!'
#     neutron_number = np.uint16(val / np.uint16(256))
#     proton_number = np.uint16(val - neutron_number * np.uint16(256))
#     return (int(proton_number), int(neutron_number))


# def create_isotope_vector(building_blocks: list) -> np.ndarray:
#     """Create an array of isotope hashvalues."""
#     # building_blocks are usually names of elements in the periodic tables
#     # if not we assume the ion is special, a user type

#     # test cases:
#     # create_isotope_vector(['Fe', 'Fe', 'O', 'O', 'O'])
#     # create_isotope_vector([])
#     # create_isotope_vector(['Markus'])

#     # lookup table of known elements
#     # element_symbol = chemical_symbols[1::]
#     element_proton_number = atomic_numbers

#     hashvector = []
#     assert len(building_blocks) <= MAX_NUMBER_OF_ATOMS_PER_ION, \
#         'Faced an ion with an unsupported high complexity!'
#     # MAX_NUMBER_OF_ATOMS_PER_ION can be modified to describe large fragments

#     if building_blocks == []:  # special case unknown ion type
#         return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

#     for block in building_blocks:
#         if block in element_proton_number:
#             proton_number = element_proton_number[block]
#             neutron_number = 0
#             # *.rng, *.rrng files do not resolve isotopes!

#             hashvector.append(hash_isotope(proton_number, neutron_number))
#         else:
#             print('WARNING: Block does not specify a unique element name!')
#             print('WARNING: Importing a user-defined type!')
#             # special case user_defined_type
#             return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

#     assert len(hashvector) <= MAX_NUMBER_OF_ATOMS_PER_ION, \
#         'More than ' + str(MAX_NUMBER_OF_ATOMS_PER_ION) \
#         + ' atoms in the molecular ion!'

#     ivec = np.asarray(hashvector, np.uint16)
#     ivec = np.sort(ivec, kind='stable')[::-1]
#     retval = np.zeros([1, MAX_NUMBER_OF_ATOMS_PER_ION], np.uint16)
#     retval[0, 0:len(ivec)] = ivec
#     return retval


# def charge_estimation_heuristics(ivec, mleft, mright) -> np.int32:
#     """Estimate molecular ion charge based on isotopes and associated range."""
#     # estimate the charge of a molecular ion given its range
#     # assume molecular ion mass is additive based on individual isotope mass
#     # assume mass-to-charge-state-ratio interval [mleft, mright] is reasonably
#     # centered to make an integer estimation

#     # the below code is too simplistic because in general a molecular ion
#     # is the following 1d array
#     # (a_i)^El_i, a_i is a positive integer for an isotope, El an element
#     # 2* \sum_i=0^i=j (a_i)^El_i ) / delta_mass \approximately an int \in [1, 7]
#     # with j number of isotopes/atoms in the molecular ion
#     # the problem is that this is underconstraint equation for j > 1
#     # so especially for atoms with different isotope combinations and hydrogen
#     # or small Z element isotopes added there is uncertainty and missing clarity

#     # a test case
#     # ivec = np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)
#     # ivec[0] = hash_isotope(75, 185-75)
#     # ivec[1] = hash_isotope(75, 187-75)
#     # ivec[2] = hash_isotope(1, 3-1)
#     # mleft = 186.2510
#     # mright = 186.6570
#     # sign = 'positive'

#     isotopes = download_isotope_data()
#     accumulated_mass = 0.
#     for hashvalue in ivec:
#         if hashvalue != 0:
#             protons, neutrons = unhash_isotope(int(hashvalue))
#             # get the mass of this isotope
#             # print('Isotope ' + str(protons) + ', ' + str(neutrons))
#             # print('Mass ' + str(isotopes[int(protons)][int(protons + neutrons)]['mass']))
#             accumulated_mass += isotopes[int(protons)][int(protons + neutrons)]['mass']
#         else:
#             break  # ivec is always sorted in descending order
#     # print('accumulated mass ' + str(accumulated_mass))
#     charge = np.int32(round(2. * accumulated_mass / (mleft + mright)))
#     assert (charge >= 1) & (charge <= 7), \
#         'charge estimated out of reasonable bounds!'
#     return charge


# def ascii_to_paraprobe_iontype(building_blocks: list) -> np.ndarray:
#     """Create a formatted isotope hashvalue list for paraprobe."""
#     # equivalent to translating iontype names from felfer 2 paraprobe notation
#     assert isinstance(building_blocks, list), \
#         'Building blocks needs to be a list !'

#     if building_blocks == []:  # special case unknown ion type
#         return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

#     hashvector = []
#     for block in building_blocks:
#         assert isinstance(block, str), \
#             'block needs to be a string !'
#         # check if the given string represents at all an element
#         tmp = re.findall(r"([A-Z]{1})([a-z]{1})?", block)
#         assert tmp != [], \
#             'block does not seem to specify a string representing an element !'
#         element_name = tmp[0][0] + tmp[0][1]
#         # check if a preceeding isotope number is present
#         tmp = re.findall(r"^(\d+)", block)
#         if tmp == []:
#             mass_number = int(0)
#         else:
#             mass_number = int(tmp[0])
#         # check for eventual preceeding multiplier e.g. H2 meaning two H atoms
#         tmp = re.findall(r"(\d+)$", block)
#         if tmp == []:
#             multiplier = 1
#         else:
#             multiplier = int(tmp[0])

#         if element_name in atomic_numbers:
#             proton_number = atomic_numbers[element_name]
#             if mass_number == 0:
#                 neutron_number = 0
#             else:
#                 neutron_number = mass_number - proton_number
#             for _ in np.arange(0, multiplier):
#                 hashvector.append(hash_isotope(proton_number, neutron_number))
#         else:
#             print('WARNING: Block does not specify a unique element name !')
#             print('WARNING: Importing user-defined iontypes not supported !')
#             # special case user_defined_type
#             return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

#     assert len(hashvector) <= MAX_NUMBER_OF_ATOMS_PER_ION, \
#         'More than ' + str(MAX_NUMBER_OF_ATOMS_PER_ION) \
#         + ' atoms in the molecular ion is currently not supported !'

#     ivec = np.asarray(hashvector, np.uint16)
#     ivec = np.sort(ivec, kind='stable')[::-1]
#     retval = np.zeros([1, MAX_NUMBER_OF_ATOMS_PER_ION], np.uint16)
#     retval[0, 0:len(ivec)] = ivec
#     return retval


# def isotope_vector_to_dict_keyword(uint16_array: np.ndarray) -> str:
#     """Create keyword for dictionary from isotope_vector."""
#     lst = []
#     for value in uint16_array:
#         lst.append(str(value))
#     assert lst, 'List from isotope_vector is empty!'
#     return ','.join(lst)


# def significant_overlap(interval: np.ndarray,
#                         interval_set: np.float64) -> bool:
#     """Check if interval overlaps within with members of interval set."""
#     assert np.shape(interval) == (2,), 'Interval needs to have two columns!'
#     assert np.shape(interval_set)[1] == 2, \
#         'Interval_set needs to have two columns!'
#     # interval = np.array([53.789, 54.343])
#     # interval_set = np.array([[27.778, 28.33]])  # for testing purposes
#     if np.shape(interval_set)[0] >= 1:
#         left_and_right_delta = np.zeros([np.shape(interval_set)[0], 2], bool)
#         left_and_right_delta[:, 0] = (interval_set[:, 0] - interval[1]) \
#             > MQ_EPSILON
#         left_and_right_delta[:, 1] = (interval[0] - interval_set[:, 1]) \
#             > MQ_EPSILON
#         no_overlap = np.array([np.any(i) for i in left_and_right_delta])
#         if np.all(no_overlap):
#             return False
#         return True
#     return False


# def significant_range(left: np.float64, right: np.float64) -> bool:
#     """Check if inclusive interval bounds [left, right] span a finite range."""
#     assert left >= np.float64(0.) and right >= np.float64(0.), \
#         'Left and right bound have to be positive!'
#     if (right - left) > MQ_EPSILON:
#         return True
#     return False


# @typing.no_type_check
# def get_memory_mapped_data(filename: str, data_type: str, oset: int,
#                            strd: int, shp: int):
#     """Memory-maps file plus offset strided read of typed data."""
#     # https://stackoverflow.com/questions/60493766/ \
#     #       read-binary-flatfile-and-skip-bytes for I/O access details

#     with open(filename, 'rb') as file_handle, \
#             mmap.mmap(file_handle.fileno(), length=0, access=mmap.ACCESS_READ) as memory_mapped:
#         return np.ndarray(buffer=memory_mapped, dtype=data_type,
#                           offset=oset, strides=strd, shape=shp).copy()


# class NxField():
#     """Representative of a NeXus field."""

#     def __init__(self, value=None, unit: str = None):
#         self.parent = None
#         self.isa = None  # ontology reference concept ID e.g.
#         self.value = value
#         self.unit = unit
#         self.attributes = None

#     def get_value(self):
#         """Get value."""
#         return self.value

#     def get_unit(self):
#         """Get unit."""
#         return self.unit


# class NxIon():
#     """Representative of a NeXus base class NXion."""

#     def __init__(self, *args, **kwargs):
#         self.ion_type = NxField('', '')
#         self.isotope_vector = NxField(ascii_to_paraprobe_iontype([]), '')
#         if len(args) >= 1:
#             assert isinstance(args[0], list), 'args[0] needs to be a list !'
#             self.isotope_vector \
#                 = NxField(ascii_to_paraprobe_iontype(args[0]), '')
#         elif 'isotope_vector' in kwargs:
#             assert isinstance(kwargs['isotope_vector'], np.ndarray), \
#                 'kwargs isotope_vector needs to be an np.ndarray !'
#             assert len(kwargs['isotope_vector']) \
#                 == MAX_NUMBER_OF_ATOMS_PER_ION, \
#                 'kwargs isotope_vector needs to have ' \
#                 + str(MAX_NUMBER_OF_ATOMS_PER_ION) + ' entries !'
#             self.isotope_vector \
#                 = NxField(np.asarray(kwargs['isotope_vector'], np.uint16), '')
#         # else:
#         #     assert True is False, \
#         #        'Give either a list of isotopes, \
#         #        or an isotope vector as a keyword argument !'
#         self.charge_state = NxField(np.int32(0), 'eV')
#         # if len(args) == 2:
#         #     assert isinstance(args[1], int), 'args[1] needs to be an integer !'
#         #    self.charge_state = NxField(np.int32(args[1], 'eV'))
#         if 'charge_state' in kwargs:
#             assert isinstance(kwargs['charge_state'], int), \
#                 'kwargs charge_state needs to be an int !'
#             assert kwargs['charge_state'] > -8, \
#                 'kwargs charge_state needs to be at least -7 !'
#             assert kwargs['charge_state'] < +8, \
#                 'kwargs charge_state needs to be at most +7 !'
#             self.charge_state = NxField(np.int32(kwargs['charge_state']), 'eV')
#         self.name = NxField('', '')
#         self.ranges = NxField(np.empty((0, 2), np.float64), 'amu')

#     def add_range(self, mqmin: np.float64, mqmax: np.float64):
#         """Adding mass-to-charge-state ratio interval."""
#         assert significant_range(mqmin, mqmax) is True, \
#             'Refusing to add epsilon range!'
#         assert significant_overlap(np.asarray([mqmin, mqmax]),
#                                    self.ranges.value) is False, \
#             'Refusing overlapping range!'
#         self.ranges.value = np.vstack((self.ranges.value,
#                                        np.array([mqmin, mqmax])))

#     def get_human_readable_name(self):
#         """Get human-readable name from isotop_vector."""
#         # equivalent to paraprobe 2 felfer notation
#         # NEW ISSUE: how to display the isotope_vector in LaTeX notation?
#         human_readable = ''
#         for hash_value in self.isotope_vector.value:
#             if hash_value > 0:
#                 protons, neutrons = unhash_isotope(int(hash_value))
#                 if neutrons > 0:
#                     human_readable += str(protons + neutrons) \
#                         + chemical_symbols[protons]
#                 else:
#                     human_readable += chemical_symbols[protons]
#                 human_readable += ' '
#             else:
#                 break
#         if self.charge_state.value > 0:
#             human_readable += '+' * self.charge_state.value
#         elif self.charge_state.value < 0:
#             human_readable += '-' * (-1 * self.charge_state.value)
#         else:
#             human_readable = human_readable[0:-1]
#         return human_readable
