#!/usr/bin/env python3
"""Set of utility tools for parsing file formats used by atom probe."""

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

from typing import Tuple

import mmap

import numpy as np

from ase.data import atomic_numbers

# restrict the number distinguished ion types
MAX_NUMBER_OF_ION_SPECIES = 256
# restrict number of atoms for molecular ion fragments
MAX_NUMBER_OF_ATOMS_PER_ION = 32
# Da or atomic mass unit (amu)
MQ_EPSILON = np.float32(1.0e-4)


def rchop(string: str = '', suffix: str = '') -> str:
    """Right-chop a string."""
    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]
    return string


def hash_isotope(proton_number: np.uint8 = 0,
                 neutron_number: np.uint8 = 0) -> np.uint16:
    """Encode an isotope to a hashvalue."""
    assert proton_number >= 0, 'Proton number >= 0 needed!'
    assert proton_number < 256, 'Proton number < 256 needed!'
    assert neutron_number >= 0, 'Neutron number >= 0 needed!'
    assert neutron_number < 256, 'Neutron number < 256 needed!'
    return np.uint16(proton_number) \
        + np.uint16(256) * np.uint16(neutron_number)


def unhash_isotope(hashval: np.uint16 = 0) -> Tuple[np.uint8]:
    """Decode a hashvalue to an isotope."""
    assert isinstance(hashval, int), 'Hashval needs to be integer!'
    assert hashval >= 0, 'Hashval needs to be an unsigned integer!'
    assert hashval <= np.iinfo(np.uint16).max, \
        'Hashval needs to map on an uint16!'
    neutron_number = np.uint16(hashval / np.uint16(256))
    proton_number = np.uint16(hashval - neutron_number * np.uint16(256))
    return (proton_number, neutron_number)


def create_isotope_vector(building_blocks: list) -> np.ndarray:
    """Create an array of isotope hashvalues."""
    # building_blocks are usually names of elements in the periodic tables
    # if not we assume the ion is special, a user type

    # test cases:
    # create_isotope_vector(['Fe', 'Fe', 'O', 'O', 'O'])
    # create_isotope_vector([])
    # create_isotope_vector(['Markus'])

    # lookup table of known elements
    # element_symbol = chemical_symbols[1::]
    element_proton_number = atomic_numbers

    hashvector = []
    assert len(building_blocks) <= MAX_NUMBER_OF_ATOMS_PER_ION, \
        'Faced an ion with an unsupported high complexity!'
    # MAX_NUMBER_OF_ATOMS_PER_ION can be modified to describe large fragments

    if building_blocks == []:  # special case unknown ion type
        return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

    for block in building_blocks:
        if block in element_proton_number.keys():
            proton_number = element_proton_number[block]
            neutron_number = 0
            # *.rng, *.rrng files do not resolve isotopes!

            hashvector.append(hash_isotope(proton_number, neutron_number))
        else:
            print('WARNING: Block does not specify a unique element name!')
            print('WARNING: Importing a user-defined type!')
            # special case user_defined_type
            return np.array([0] * MAX_NUMBER_OF_ATOMS_PER_ION, dtype=np.uint16)

    assert len(hashvector) <= MAX_NUMBER_OF_ATOMS_PER_ION, \
        'More than ' + MAX_NUMBER_OF_ATOMS_PER_ION \
        + ' atoms in the molecular ion!'

    hashvector = np.asarray(hashvector, np.uint16)
    hashvector = np.sort(hashvector, kind='stable')[::-1]
    retval = np.zeros([1, MAX_NUMBER_OF_ATOMS_PER_ION], np.uint16)
    retval[0, 0:len(hashvector)] = hashvector
    return retval


def isotope_vector_to_dict_keyword(uint16_array: np.ndarray) -> str:
    """Create keyword for dictionary from isotope_vector."""
    lst = []
    for value in uint16_array:
        lst.append(str(value))
    assert lst != [], 'List from isotope_vector is empty!'
    return ','.join(lst)


def significant_overlap(interval: np.float64,
                        interval_set: np.float64) -> bool:
    """Check if interval overlaps within with members of interval set."""
    assert np.shape(interval) == (2,), 'Interval needs to have two columns!'
    assert np.shape(interval_set)[1] == 2, \
        'Interval_set needs to have two columns!'
    # interval = np.array([53.789, 54.343])
    # interval_set = np.array([[27.778, 28.33]])  # for testing purposes
    if np.shape(interval_set)[0] >= 1:
        left_and_right_delta = np.zeros([np.shape(interval_set)[0], 2], bool)
        left_and_right_delta[:, 0] = (interval_set[:, 0] - interval[1]) \
            > MQ_EPSILON
        left_and_right_delta[:, 1] = (interval[0] - interval_set[:, 1]) \
            > MQ_EPSILON
        no_overlap = np.array([np.any(i) for i in left_and_right_delta])
        if np.all(no_overlap):
            return False
        return True
    return False


def significant_range(left: np.float64, right: np.float64) -> bool:
    """Check if inclusive interval bounds [left, right] span a finite range."""
    assert left >= np.float64(0.) and right >= np.float64(0.), \
        'Left and right bound have to be positive!'
    if (right - left) > MQ_EPSILON:
        return True
    return False


def get_memory_mapped_data(filename: str, data_type: str, oset: int,
                           strd: int, shp: int) -> np.ndarray:
    """Memory-maps file plus offset strided read of typed data."""
    # https://stackoverflow.com/questions/60493766/ \
    #       read-binary-flatfile-and-skip-bytes for I/O access details

    with open(filename, 'rb') as file_handle, \
            mmap.mmap(file_handle.fileno(), length=0, access=mmap.ACCESS_READ) as memory_mapped:
        return np.ndarray(buffer=memory_mapped, dtype=data_type,
                          offset=oset, strides=strd, shape=shp).copy()


class NxField():
    """Representative of a NeXus field."""

    def __init__(self, value: str = None, unit: str = None):
        self.parent = None
        self.isa = None  # ontology reference concept ID e.g.
        self.value = value
        self.unit = unit
        self.attributes = None

    def get_value(self):
        """Get value."""
        return self.value

    def get_unit(self):
        """Get unit."""
        return self.unit


class NxIon():
    """Representative of a NeXus base class NXion."""

    def __init__(self):
        self.ion_type = NxField('', '')
        self.isotope_vector = NxField(np.empty(0, np.uint16), '')
        self.charge_state = NxField(np.int32(0), '')
        self.name = NxField('', '')
        self.ranges = NxField(np.empty((0, 2), np.float64), 'amu')

    def add_range(self, mqmin: np.float64, mqmax: np.float64):
        """Adding mass-to-charge-state ratio interval."""
        assert significant_range(mqmin, mqmax) is True, \
            'Refusing to add epsilon range!'
        assert significant_overlap(np.asarray([mqmin, mqmax]),
                                   self.ranges.value) is False, \
            'Refusing overlapping range!'
        self.ranges.value = np.vstack((self.ranges.value,
                                       np.array([mqmin, mqmax])))

    def get_human_readable_name(self):
        """Get human-readable name from isotop_vector."""
        # NEW ISSUE: how to display the isotope_vector in LaTeX notation?
        return self.name.value


# a = NxIon()
# a.add_range(1., 2.)
# a.add_range(2.2, 3.)
# a.add_range(0.1, 0.99)
