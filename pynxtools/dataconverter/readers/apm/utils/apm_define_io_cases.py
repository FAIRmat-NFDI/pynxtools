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
"""Utility class to analyze which vendor/community files are passed to em reader."""

# pylint: disable=no-member,duplicate-code

from typing import Tuple, Dict, List
VALID_FILE_NAME_SUFFIX_RECON = [".apt", ".pos", ".epos", ".ato", ".csv", ".h5"]
VALID_FILE_NAME_SUFFIX_RANGE = [".rng", ".rrng", ".env", ".fig.txt", "range_.h5"]
VALID_FILE_NAME_SUFFIX_CONFIG = [".yaml", ".yml"]


class ApmUseCaseSelector:  # pylint: disable=too-few-public-methods
    """Decision maker about what needs to be parsed given arbitrary input.

    Users might invoke this dataconverter with arbitrary input, no input, or
    too much input. The UseCaseSelector decide what to do in each case.
    """

    def __init__(self, file_paths: Tuple[str] = None):
        """Initialize the class.

        dataset injects numerical data and metadata from an analysis.
        eln injects additional metadata and eventually numerical data.
        """
        self.case: Dict[str, list] = {}
        self.eln: List[str] = []
        self.cfg: List[str] = []
        self.reconstruction: List[str] = []
        self.ranging: List[str] = []
        self.is_valid = False
        self.supported_file_name_suffixes = VALID_FILE_NAME_SUFFIX_RECON \
            + VALID_FILE_NAME_SUFFIX_RANGE + VALID_FILE_NAME_SUFFIX_CONFIG
        print(f"self.supported_file_name_suffixes: {self.supported_file_name_suffixes}")
        self.sort_files_by_file_name_suffix(file_paths)
        self.check_validity_of_file_combinations()

    def sort_files_by_file_name_suffix(self, file_paths: Tuple[str] = None):
        """Sort all input-files based on their name suffix to prepare validity check."""
        for suffix in self.supported_file_name_suffixes:
            self.case[suffix] = []
        for fpath in file_paths:
            for suffix in self.supported_file_name_suffixes:
                if suffix not in [".h5", "range_.h5"]:
                    if (fpath.lower().endswith(suffix)) and (fpath not in self.case[suffix]):
                        self.case[suffix].append(fpath)
                        break
                else:
                    if fpath.lower().endswith("range_.h5") == True:
                        self.case["range_.h5"].append(fpath)
                        break
                    elif fpath.lower().endswith(".h5") == True:
                        self.case[".h5"].append(fpath)
                        break
                    else:
                        continue
                # HDF5 files need special treatment, this already shows that magic numbers
                # should better have been used or signatures to avoid having to have as
                # complicated content checks as we had to implement e.g. for the em reader

    def check_validity_of_file_combinations(self):
        """Check if this combination of types of files is supported."""
        recon_input = 0  # reconstruction relevant file e.g. POS, ePOS, APT, ATO, CSV
        range_input = 0  # ranging definition file, e.g. RNG, RRNG, ENV, FIG.TXT
        other_input = 0  # generic ELN or OASIS-specific configurations
        for suffix, value in self.case.items():
            if suffix not in [".h5", "range_.h5"]:
                if suffix in VALID_FILE_NAME_SUFFIX_RECON:
                    recon_input += len(value)
                elif suffix in VALID_FILE_NAME_SUFFIX_RANGE:
                    range_input += len(value)
                elif suffix in VALID_FILE_NAME_SUFFIX_CONFIG:
                    other_input += len(value)
                else:
                    continue
            else:
                if suffix == "range_.h5":
                    range_input += len(value)
                if suffix == ".h5":
                    recon_input += len(value)
        print(f"{recon_input}, {range_input}, {other_input}")

        if (recon_input == 1) and (range_input == 1) and (1 <= other_input <= 2):
            self.is_valid = True
            self.reconstruction: List[str] = []
            self.ranging: List[str] = []
            for suffix in VALID_FILE_NAME_SUFFIX_RECON:
                self.reconstruction += self.case[suffix]
            for suffix in VALID_FILE_NAME_SUFFIX_RANGE:
                self.ranging += self.case[suffix]
            yml: List[str] = []
            for suffix in VALID_FILE_NAME_SUFFIX_CONFIG:
                yml += self.case[suffix]
            for entry in yml:
                if entry.endswith(".oasis.specific.yaml") \
                        or entry.endswith(".oasis.specific.yml"):
                    self.cfg += [entry]
                else:
                    self.eln += [entry]
