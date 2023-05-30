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
import random
import numpy as np
import ase
from pynxtools.dataconverter.helpers import extract_atom_types


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
            Mock data if data_type is Psi/Delta or tan(Psi)/cos(Delta)
        - mock_mueller_matrix:
            Mock data if data_type is Mueller matrix
        - mock_template:
            Creates mock ellipsometry data (by calling the above routines)
    """

    def __init__(self, data_template) -> None:
        self.data = data_template["measured_data"]
        self.wavelength = data_template["data_collection/NAME_spectrum[wavelength_spectrum]"]
        self.atom_types = data_template["atom_types"]
        self.sample_list: list = []
        self.data_types = ["Psi/Delta", "tan(Psi)/cos(Delta)", "Mueller matrix"]
        self.angles: list = []
        self.number_of_signals = 0

    def mock_sample(self, data_template) -> None:
        """ Chooses random entry from sample_list, overwrites sample_name
            and extracts atom_types
        """
        self.mock_chemical_formula()
        name = random.choice(self.sample_list)
        self.atom_types = extract_atom_types(name)
        data_template["sample_name"] = name
        data_template["atom_types"] = self.atom_types
        data_template["layer_structure"] = f"{name} bulk"
        data_template["experiment_description"] = f"RC2 scan on {name} bulk"

    def choose_data_type(self, data_template) -> None:
        """ Chooses random entry from data_types
        """
        data_type = random.choice(self.data_types)
        data_template["data_type"] = data_type
        if data_type == "Mueller matrix":
            self.number_of_signals = 16
        elif data_type in ("Psi/Delta", "tan(Psi)/cos(Delta)"):
            self.number_of_signals = 2

    def mock_chemical_formula(self) -> None:
        """ Creates a list of chemical formulas consisting of two atom types """
        part_1 = ase.atom.chemical_symbols[1:]
        part_2 = list(range(2, 20, 1))

        for el1 in part_1:
            for na1 in part_2:
                for el2 in part_1:
                    for na2 in part_2:
                        chemical_formula = f"{el1}{na1}{el2}{na2}"
                        if el1 != el2:
                            self.sample_list.append(chemical_formula)

    def mock_angles(self, data_template) -> None:
        """ Change value and number of incident angles
        """
        angle_list = [40, 45, 50, 55, 60, 65, 70, 75, 80]
        for _ in range(random.randrange(1, 4)):
            angle = random.choice(angle_list)
            self.angles.append(angle)
            angle_list.remove(angle)
        self.angles.sort()
        data_template["angle_of_incidence"] = self.angles
        if self.number_of_signals == 2:
            self.mock_signals(data_template)
        elif self.number_of_signals == 16:
            self.mock_mueller_matrix(data_template)

    def mock_signals(self, data_template) -> None:
        """ Mock data if data_type is Psi/Delta or tan(Psi)/cos(Delta)
            considering the (new) number of incident angles
        """
        my_numpy_array = np.empty([
            len(self.angles),
            self.number_of_signals,
            len(self.wavelength)
        ])
        for index in range(0, len(self.angles)):
            noise = np.random.normal(0, 0.5, self.data[0, 0, :].size)
            my_numpy_array[index] = self.data[0] * random.uniform(0.5, 1.5) + noise
        self.data = my_numpy_array
        data_template["measured_data"] = my_numpy_array

    def mock_mueller_matrix(self, data_template) -> None:
        """ Mock data if data_type is Mueller matrix (i.e. 16 elements/signals)
            considering the (new) number of incident angles
        """
        my_numpy_array = np.empty([
            len(self.angles),
            self.number_of_signals,
            len(self.wavelength)
        ])
        for idx in range(0, len(self.angles)):
            noise = np.random.normal(0, 0.1, self .data[0, 0, :].size)
            for m_idx in range(1, self.number_of_signals):
                my_numpy_array[idx][m_idx] = self.data[0][0] * random.uniform(.5, 1.)
                my_numpy_array[idx][m_idx] += noise
            my_numpy_array[idx][0] = my_numpy_array[0][0] / my_numpy_array[0][0]
        data_template["measured_data"] = my_numpy_array

    def modify_spectral_range(self, data_template) -> None:
        """ Change spectral range (i.e. wavlength array) and step size,
            while length of the wavelength array remains the same.
        """
        temp = random.uniform(0.25, 23)
        data_template["data_collection/NAME_spectrum[wavelength_spectrum]"] = \
            temp * data_template["data_collection/NAME_spectrum[wavelength_spectrum]"]

    def mock_template(self, data_template) -> None:
        """ Creates a mock ellipsometry template """
        self.mock_sample(data_template)
        self.modify_spectral_range(data_template)
        self.choose_data_type(data_template)
        self.mock_angles(data_template)
