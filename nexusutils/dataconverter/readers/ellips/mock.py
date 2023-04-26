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

"""A generic class for generating duplicate outputs for ellipsometry"""
from typing import Tuple, Any
import random
import numpy as np
import ase
# from nexusutils.dataconverter.readers.ellips.reader_utils import extract_atom_types
from nexusutils.dataconverter.readers.xps.reader import extract_atom_types


class MockEllips():
    """ A generic class for generating duplicate outputs for ELLIPSOMETRY

        Contains:
        - mock_sample:
            Chooses random entry from sample_list, overwrites sample_name
            and extracts atom_types
        - mock_chemical_formula:
            Creates a list of chemical formulas consisting of two atom types
        - modify_spectral_range:
            Change spectral range (i.e. wavelength array) and step size.
        - mock_angles:
            Change value and number of incident angles
        - choose_data_type:
            Chooses random entry from data_types
        - mock_signals:
            Mock data if data_type is psi/delta or tan(psi)/cos(delta)
        - mock_Mueller_matrix:
            Mock data if data_type is Mueller matrix
        - mock_template:
            Creates mock ellipsometry data (by calling the above routines)
    """

    def __init__(self, dict):
        self.name = dict["sample_name"]
        self.data_type = dict["data_type"]
        self.data = dict["measured_data"]
        self.wavelength = dict["spectrometer/wavelength"]
        self.atom_types = dict["atom_types"]
        self.sample_list = []
        self.data_types = ["psi/delta", "tan(psi)/cos(delta)", "Mueller matrix"]
        self.angles = []
        self.number_of_signals = 0
        self.angle_list = [40, 45, 50, 55, 60, 65, 70, 75, 80]

    def mock_sample(self, dict) -> None:
        """ Chooses random entry from sample_list, overwrites sample_name
            and extracts atom_types
        """
        self.mock_chemical_formula()
        self.name = random.choice(self.sample_list)
        self.atom_types = extract_atom_types(self.name)
        dict["sample_name"] = self.name
        dict["atom_types"] = self.atom_types
        dict["layer_structure"] = f"{self.name} bulk"
        dict["experiment_description"] = f"RC2 scan on {self.name} bulk"

    def choose_data_type(self, dict) -> None:
        """ Chooses random entry from data_types
        """
        self.data_type = random.choice(self.data_types)
        dict["data_type"] = self.data_type
        if self.data_type == "Mueller matrix":
            self.number_of_signals = 16
        elif self.data_type == "psi/delta" or self.data_type == "tan(psi)/cos(delta)":
            self.number_of_signals = 2

    def mock_chemical_formula(self) -> None:
        """ Creates a list of chemical formulas consisting of two atom types """
        part_1 = ase.atom.chemical_symbols[1:]
        part_2 = list(range(2, 20, 1))

        for x in part_1:
            for y in part_2:
                for z in part_1:
                    for k in part_2:
                        chemical_formula = f"{x}{y}{z}{k}"
                        if x != z:
                            self.sample_list.append(chemical_formula)

    def mock_angles(self, dict) -> None:
        """ Change value and number of incident angles
        """
        for index in range(random.randrange(1, 4)):
            angle = random.choice(self.angle_list)
            self.angles.append(angle)
            self.angle_list.remove(angle)
        self.angles.sort()
        dict["angle_of_incidence"] = self.angles
        if self.number_of_signals == 2:
            self.mock_signals(dict)
        elif self.number_of_signals == 16:
            self.mock_Mueller_matrix(dict)

    def mock_signals(self, dict) -> None:
        """ Mock data if data_type is psi/delta or tan(psi)/cos(delta)
            considering the (new) number of incident angles
        """
        my_numpy_array = np.empty([1,
                                   1,
                                   len(self.angles),
                                   self.number_of_signals,
                                   len(self.wavelength)
                                   ])
        for index in range(0, len(self.angles)):
            noise = np.random.normal(0, 0.5, self.data[0, 0, 0, 0, :].size)
            my_numpy_array[0][0][index] = self.data[0][0][0] * random.uniform(0.5, 1.5) + noise
        self.data = my_numpy_array
        dict["measured_data"] = my_numpy_array

    def mock_Mueller_matrix(self, dict) -> None:
        """ Mock data if data_type is Mueller matrix (i.e. 16 elements/signals)
            considering the (new) number of incident angles
        """
        my_numpy_array = np.empty([1,
                                   1,
                                   len(self.angles),
                                   self.number_of_signals,
                                   len(self.wavelength)
                                   ])
        for index in range(0, len(self.angles)):
            noise = np.random.normal(0, 0.1, self .data[0, 0, 0, 0, :].size)
            for mm_index in range(1, self.number_of_signals):
                my_numpy_array[0][0][index][mm_index] = self.data[0][0][0][0] * random.uniform(0.5, 1.5) + noise
            my_numpy_array[0][0][index][0] = my_numpy_array[0][0][0][0] / my_numpy_array[0][0][0][0]
        dict["measured_data"] = my_numpy_array

    def modify_spectral_range(self, dict) -> None:
        """ Change spectral range (i.e. wavlength array) and step size,
            while length of the wavelength array remains the same.
        """
        dict["spectrometer/wavelength"] = random.uniform(0.25, 23) * dict["spectrometer/wavelength"]

    def mock_template(self, dict) -> None:
        """ Creates a mock ellipsometry template """
        self.mock_sample(dict)
        self.modify_spectral_range(dict)
        self.choose_data_type(dict)
        self.mock_angles(dict)
