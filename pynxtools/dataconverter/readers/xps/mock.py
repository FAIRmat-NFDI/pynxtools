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

"""A generic class for generating duplicate XPS output."""
from pynxtools.dataconverter.helpers import extract_atom_types
from typing import Set, Tuple, Any
from pynxtools.dataconverter.template import Template
import numpy as np
import random


class MockXPS():
    """Defining Different functions for generating XPS mock nxs data file."""

    def __init__(self, data_template) -> None:
        """Initialize class variables"""

        self.data = data_template
        self.template = Template()
        self.max_detector_num = 9
        self.scan_max = 20
        self.rand_int_max = 50
        self.rand_float_max = 0.2

    def mock_one_dot_six(self) -> None:
        """Generating mock data for specs verions 1.6."""

        self.sample_list = ["(C12H6N4)", "(C12H6N4)SO4"]
        self.entry_list = ["specs__PBY__C1s", "specs__PBY__F1s",
                           "specs__PBY__S_2p", "specs__PBY__survey",
                           "specs__PTBY__C1s", "specs__PTBY__F1s",
                           "specs__PTBY__S_2p", "specs__PTBY__survey",
                           "specs__PBTY_1.2__C1s", "specs__PBTY_1.2__F1s",
                           "specs__PBTY_1.2__S_2p", "specs__PBTY_1.2__survey",
                           "specs__PBTT_1.2__K1s", "specs__PBTT_1.2__S1s",
                           "specs__PBTT_1.2__K2p", "specs__PBTY_2.0__survey",
                           "specs__PTTT_1.2__C1s", "specs__PTTT_1.2__F1s",
                           "specs__PTTT_1.2__S_2p", "specs__PTTT_1.0__survey"]

        self.detec_num = random.randint(1, self.max_detector_num)
        self.scan_num = random.randint(1, self.max_detector_num)
        # Track detector scans in data sector so that confined number of
        # detectors and scans according to randomly create number.
        self.detector_track: dict = {}
        self.scan_track: dict = {}
        # maximum detectors to be allowed
        self.entry_replacement: dict = {}
        self.sample_replacement: str = ""

        for key, value in self.data.items():
            key = self.mock_entry(key)
            if "chemical_formula" in key or "atom_types" in key:
                self.mock_sample(key, value)
            elif "DETECTOR[detector_" in key:
                self.mock_detector_grp(key, value)
            elif "DATA[" in key:
                self.mock_data_grp(key, value)
            else:
                self.template[key] = value

        self.check_duplicate_group_reach_to_max_rand()

    def get_mock_data(self) -> Template:
        """Return fullfiled template."""
        self.mock_one_dot_six()
        return self.template

    # For detector raw value and scan values
    def mock_array(self, key, value) -> Tuple(str, Any):
        "add sum random noise in numpy array."

        # skip BE binding energy value
        if "BE" != key.split("/")[-1]:
            rand_norm = np.random.rand(np.size(value))
            value = value + rand_norm * self.rand_int_max
        self.template[key] = value

        return key, value

    def mock_sample(self, key, value) -> None:
        """Mocking Sample Name."""

        if "chemical_formula" in key:
            if not self.sample_replacement:
                self.sample_replacement = random.choice(self.sample_list)
                self.sample_list.remove(self.sample_replacement)

            self.template[key] = self.sample_replacement

        if "atom_types" in key:
            if not self.sample_replacement:
                self.sample_replacement = random.choice(self.sample_list)
                self.sample_list.remove(self.sample_replacement)
            self.template[key] = extract_atom_types(self.sample_replacement)

    def mock_detector_grp(self, key, value) -> None:
        """Mock detector."""
        detect_ind = int(key.split("DETECTOR[detector_")[-1][0])
        if detect_ind < self.detec_num:
            if isinstance(value, np.ndarray):
                key, value = self.mock_array(key, value)
                self.detector_track[key] = value
            else:
                self.template[key] = value

    def mock_data_grp(self, key, value) -> None:
        """Mock DATA group."""
        # Collect scan values if scans are bellow randomly created number
        if isinstance(value, np.ndarray):

            if "/cycle0_scan" in key:
                scan_ind = int(key.split("/cycle0_scan")[-1][0])
                if scan_ind < self.scan_num - 1:
                    key, value = self.mock_array(key, value)
                    self.scan_track[key] = value
                    return
            else:
                _, _ = self.mock_array(key, value)
                return

        self.template[key] = value

    def mock_entry(self, key) -> str:
        """Mock entry name."""
        entry = ""
        if "/ENTRY[" not in key:
            return key
        part2 = key.split("/ENTRY[")[-1]
        trimed_key = part2

        for char in part2:
            if char == "]":
                break
            entry = entry + char
            trimed_key = trimed_key[1:]

        if entry in self.entry_replacement:
            new_entry_nm = self.entry_replacement[entry]
        else:
            new_entry_nm = random.choice(self.entry_list)
            self.entry_list.remove(new_entry_nm)
            self.entry_replacement[entry] = new_entry_nm

        key = f"/ENTRY[{new_entry_nm}{trimed_key}"

        return key

    def check_duplicate_group_reach_to_max_rand(self) -> None:
        """Reach to predifined random number of the scan_data and detector."""

        # check for detector
        tot_dect = len(self.detector_track)
        last_detec = list(self.detector_track.keys())[-1]
        last_value = self.detector_track[last_detec]

        if tot_dect < self.detec_num:
            for new_detect_num in np.arange(tot_dect, self.detec_num):
                detec_ind = int(last_detec.split("DETECTOR[detector_")[-1][0])
                new_key = last_detec.replace(f"DETECTOR[detector_{detec_ind}",
                                             f"DETECTOR[detector_{new_detect_num}")
                _, _ = self.mock_array(new_key, last_value)

        # check for data scan
        tot_scan = len(self.scan_track)
        last_scan = list(self.scan_track.keys())[-1]
        last_value = self.scan_track[last_scan]

        if tot_scan < self.scan_num:
            for new_scan_num in np.arange(tot_scan, self.scan_num):
                scan_ind = int(last_scan.split("/cycle0_scan")[-1][0])
                new_key = last_scan.replace(f"/cycle0_scan{scan_ind}",
                                            f"/cycle0_scan{new_scan_num}")
                _, _ = self.mock_array(new_key, last_value)

        self.template["/@default"] = random.choice(list(self.entry_replacement.values()))
