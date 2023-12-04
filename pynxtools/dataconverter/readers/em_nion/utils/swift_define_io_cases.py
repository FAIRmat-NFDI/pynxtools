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
"""Utility class handling which community/technology partner files for em_nion reader."""

# pylint: disable=no-member,duplicate-code,too-few-public-methods

from typing import Tuple, Dict, List


class EmNionUseCaseSelector:
    """Decision maker about what needs to be parsed given arbitrary input.

    Users might invoke this dataconverter with arbitrary input, no input, or
    too much input. The UseCaseSelector decides what to do in each case.
    """

    def __init__(self, file_paths: Tuple[str] = None):
        """Analyze with which parser(s) (if any) input can be handled."""
        self.mime_types: Dict[str, list] = {}
        self.eln_parser_type: str = "none"
        self.eln: List[str] = []
        self.prj_parser_type: str = "none"
        self.prj: List[str] = []
        self.is_valid = False

        self.analyze_mime_types(file_paths)
        self.identify_case()

    def analyze_mime_types(self, file_paths: Tuple[str] = None):
        """Accept/reject and organize input-files based on mime-type."""
        self.supported_mime_types = ["yaml", "yml", "nionswift"]
        for mime_type in self.supported_mime_types:
            self.mime_types[mime_type] = []
        for file_name in file_paths:
            index = file_name.lower().rfind(".")
            if index >= 0:
                suffix = file_name.lower()[index + 1::]
                add = (suffix in self.supported_mime_types) \
                    and (file_name not in self.mime_types[suffix])
                if add is True:
                    self.mime_types[suffix].append(file_name)
        print(self.mime_types)

    def identify_case(self):
        """Identify which sub-parsers to use if any based on input mime_types."""
        # eln
        self.is_valid = False
        for mime_type in ["yaml", "yml"]:
            self.eln += self.mime_types[mime_type]
        if len(self.eln) == 1:
            self.eln_parser_type = "generic"
            self.is_valid = True
        else:
            self.eln_parser_type = "none"

        if "nionswift" in self.mime_types:
            if len(self.mime_types["nionswift"]) == 1:
                self.prj += self.mime_types["nionswift"]
                self.prj_parser_type = "nionswift"
            else:
                self.is_valid = False

        print("Input suggests to use the following sub-parsers:")
        print(f"ELN parser: {self.eln_parser_type}")
        print(self.eln)
        print(f"Data parser: {self.prj_parser_type}")
        print(self.prj)
        print(f"Input suggests that parsing is valid: {self.is_valid}")
