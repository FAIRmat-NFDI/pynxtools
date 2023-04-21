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

# pylint: disable=E1101, R0801

from typing import Tuple, Dict, List


class ApmUseCaseSelector:  # pylint: disable=R0903
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
        self.is_valid = False
        self.supported_mime_types = [
            "pos", "epos", "apt", "rrng", "rng", "yaml", "yml"]
        for mime_type in self.supported_mime_types:
            self.case[mime_type] = []
        for file_name in file_paths:
            index = file_name.lower().rfind(".")
            if index >= 0:
                suffix = file_name.lower()[index + 1::]
                if suffix in self.supported_mime_types:
                    if file_name not in self.case[suffix]:
                        self.case[suffix].append(file_name)
        recon_input = 0
        range_input = 0
        for mime_type, value in self.case.items():
            if mime_type in ["pos", "epos", "apt"]:
                recon_input += len(value)
            if mime_type in ["rrng", "rng"]:
                range_input += len(value)
        eln_input = len(self.case["yaml"]) + len(self.case["yml"])
        if (recon_input == 1) and (range_input == 1) and (eln_input == 1):
            self.is_valid = True
            self.reconstruction: List[str] = []
            self.ranging: List[str] = []
            for mime_type in ["pos", "epos", "apt"]:
                self.reconstruction += self.case[mime_type]
            for mime_type in ["rrng", "rng"]:
                self.ranging += self.case[mime_type]
            self.eln: List[str] = []
            for mime_type in ["yaml", "yml"]:
                self.eln += self.case[mime_type]
