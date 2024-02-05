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
        self.supported_mime_types = [
            "pos", "epos", "apt", "rrng", "rng", "txt", "yaml", "yml"]
        for mime_type in self.supported_mime_types:
            self.case[mime_type] = []

        self.sort_files_by_mime_type(file_paths)
        self.check_validity_of_file_combinations()

    def sort_files_by_mime_type(self, file_paths: Tuple[str] = None):
        """Sort all input-files based on their mimetype to prepare validity check."""
        for file_name in file_paths:
            index = file_name.lower().rfind(".")
            if index >= 0:
                suffix = file_name.lower()[index + 1::]
                if suffix in self.supported_mime_types:
                    if file_name not in self.case[suffix]:
                        self.case[suffix].append(file_name)

    def check_validity_of_file_combinations(self):
        """Check if this combination of types of files is supported."""
        recon_input = 0  # reconstruction relevant file e.g. POS, ePOS, APT
        range_input = 0  # ranging definition file, e.g. RNG, RRNG
        other_input = 0  # generic ELN or OASIS-specific configurations
        for mime_type, value in self.case.items():
            if mime_type in ["pos", "epos", "apt"]:
                recon_input += len(value)
            elif mime_type in ["rrng", "rng", "txt"]:
                range_input += len(value)
            elif mime_type in ["yaml", "yml"]:
                other_input += len(value)
            else:
                continue

        if (recon_input == 1) and (range_input == 1) and (1 <= other_input <= 2):
            self.is_valid = True
            self.reconstruction: List[str] = []
            self.ranging: List[str] = []
            for mime_type in ["pos", "epos", "apt"]:
                self.reconstruction += self.case[mime_type]
            for mime_type in ["rrng", "rng", "txt"]:
                self.ranging += self.case[mime_type]
            yml: List[str] = []
            for mime_type in ["yaml", "yml"]:
                yml += self.case[mime_type]
            for entry in yml:
                if entry.endswith(".oasis.specific.yaml") \
                        or entry.endswith(".oasis.specific.yml"):
                    self.cfg += [entry]
                else:
                    self.eln += [entry]
