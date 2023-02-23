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
from nexusutils.dataconverter.readers.ellips.reader_utils import extract_atom_types

class MockEllips():
    """ A generic class for generating duplicate outputs for ELLIPSOMETRY

        Contains:
        - mock_sample:
            Chooses random entry from sample_list, overwrites sample_name
            and extracts atom_types
        - mock_chemical_formula:
            Creates a list of chemical formulas consisting of two atom types
        - modify_spectral_range:
            Change spectral range (i.e. wavlength array) and step size,
            while length of the wavelength array remains the same.
        - mock_psi_delta:
            Distorts psi and delta, adds noise, and overwrites measured_data
        - mock_template:
            Creates mock ellipsometry data (by calling the above routines)
    """

    def __init__(self, dict):
        self.name = dict["sample_name"]
        self.data_type = dict["data_type"]
        self.data = dict["measured_data"]
        self.atom_types = dict["atom_types"]
        self.sample_list = []
        self.data_types = ["psi/delta", "tan(psi)/cos(delta)", "Jones matrix", "Mueller matrix"]
        self.number_of_signals = 0

    def mock_sample(self, dict) -> None:
        """ Chooses random entry from sample_list, overwrites sample_name
            and extracts atom_types
        """
        self.mock_chemical_formula()
        self.name = random.choice(self.sample_list)
        self.atom_types = extract_atom_types(self.name)
        dict["sample_name"] = self.name
        dict["atom_types"] = self.atom_types

    def choose_data_type(self, dict) -> None:
        """ Chooses random entry from data_types
        """
        self.data_type = random.choice(self.data_types)
        dict["data_type"] = self.data_type
        if self.data_type == "psi/delta" or "tan(psi)/cos(delta)":
            self.number_of_signals = 2
        elif self.data_type == "Jones matrix":
            self.number_of_signals = 4
        elif self.data_type == "Mueller matrix":
            self.number_of_signals = random.range(11,16)

    def mock_chemical_formula(self) -> None:
        """ Creates a list of chemical formulas consisting of two atom types """
        part_1 = ase.atom.chemical_symbols[1:]
        part_2 = list(range(2,20,1))

        for x in part_1:
            for y in part_2:
                for z in part_1:
                    for k in part_2:
                        chemical_formula = f"{x}{y}{z}{k}"
                        self.sample_list.append(chemical_formula)

    def modify_spectral_range(self, dict) -> None:
        """ Change spectral range (i.e. wavlength array) and step size,
            while length of the wavelength array remains the same.
        """
        dict["spectrometer/wavelength"] = random.uniform(0.25,23)*dict["spectrometer/wavelength"]

    def mock_psi_delta(self, dict) -> None:
        """ Distorts psi and delta, adds noise, and overwrites measured_data
        """
        noise=np.random.normal(0,0.5,self.data[0,0,0,0,:].size)
        rand_psi=random.uniform(0.5,1.5)
        rand_delta=random.uniform(0.5,1.)
        number_of_angles = self.data[0,0,:,0,0].size
        for index in range(number_of_angles):
            self.data[0,
                        0,
                        index,
                        0,
                        :] = self.data[0,
                        0,
                        index,
                        0,
                        :]*rand_psi+noise
        for index in range(number_of_angles):
            self.data[0,
                        0,
                        index,
                        1,
                        :] = self.data[0,
                        0,
                        index,
                        1,
                        :]*rand_delta+noise

    def mock_template(self, dict) -> None:
        """ Creates a mock ellipsometry template """
        self.mock_sample(dict)
        self.modify_spectral_range(dict)
        self.choose_data_type(dict)
        if self.data_type == "psi/delta":
            self.mock_psi_delta(dict)