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
"""Utility class handling which community/technology partner files for em_om reader."""

# pylint: disable=no-member,duplicate-code

from typing import Tuple, Dict, List


class EmOmUseCaseSelector:  # pylint: disable=too-few-public-methods
    """Decision maker about what needs to be parsed given arbitrary input.

    Users might invoke this dataconverter with arbitrary input, no input, or
    too much input. The UseCaseSelector decides what to do in each case.
    """

    def __init__(self, file_paths: Tuple[str] = None):
        """Analyze with which parser(s) (if any) input can be handled."""
        self.mime_types: Dict[str, list] = {}
        self.eln_parser_type: str = "none"
        self.eln: List[str] = []
        self.dat_parser_type: str = "none"
        self.dat: List[str] = []
        self.is_valid = False

        self.analyze_mime_types(file_paths)
        self.identify_case()

    def analyze_mime_types(self, file_paths: Tuple[str] = None):
        """Accept/reject and organize input-files based on mime-type."""
        self.supported_mime_types = ["yaml", "yml", "h5oina", "mtex", "zip", "dream3d"]
        # "score", "qube", "paradis", "ang", "cpr", "crc", "damask via dream3d"
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

        # (heavy) data from community or technology partners
        if self.needs_orix_parser() is True:
            self.dat += self.mime_types["h5oina"]
            if len(self.dat) == 1:
                self.dat_parser_type = "orix"
        elif self.needs_mtex_parser() is True:
            self.dat += self.mime_types["mtex"]
            if len(self.dat) == 1:
                self.dat_parser_type = "mtex"
        elif self.needs_zip_parser() is True:
            self.dat += self.mime_types["zip"]
            if len(self.dat) == 1:
                self.dat_parser_type = "zip"
        elif self.needs_dreamthreed_parser() is True:
            self.dat += self.mime_types["dream3d"]
            if len(self.dat) == 1:
                self.dat_parser_type = "dream3d"
        # elif self.needs_kikuchipy_parser() is True:
        #     self.dat_parser_type = "kikuchipy"
        # elif self.needs_score_parser() is True:
        #     self.dat_parser_type = "score"
        # elif self.needs_qube_parser() is True:
        #     self.dat_parser_type = "qube"
        # elif self.needs_paradis_parser() is True:
        #     self.dat_parser_type = "paradis"
        # elif self.needs_brinckmann_parser() is True:
        #     self.dat_parser_type = "brinckmann"
        else:
            self.dat_parser_type = "none"

        # if self.eln_parser_type != "none":  # and (self.dat_parser_type != "none"):
        print("Input suggests to use the following sub-parsers:")
        print(f"ELN parser: {self.eln_parser_type}")
        print(self.eln)
        print(f"Data parser: {self.dat_parser_type}")
        print(self.dat)
        # self.is_valid = True
        print(f"Input suggests that parsing is valid: {self.is_valid}")

    def needs_orix_parser(self):
        """Check if input suggests to use orix parser or not."""
        if "h5oina" in self.mime_types:
            if len(self.mime_types["h5oina"]) == 1:
                return True
        return False

    def needs_mtex_parser(self):
        """Check if input suggests to use MTex parser or not."""
        if "mtex" in self.mime_types:
            if len(self.mime_types["mtex"]) == 1:
                return True
        return False

    def needs_zip_parser(self):
        """Check if input suggests to use zipfile parser for generic pattern or not."""
        if "mtex" in self.mime_types:
            if len(self.mime_types["zip"]) == 1:
                return True
        return False

    def needs_dreamthreed_parser(self):
        """Check if input suggests to use DREAM.3D parser or not."""
        if "dream3d" in self.mime_types:
            if len(self.mime_types["dream3d"]) == 1:
                return True
        return False

    def needs_kikuchipy_parser(self):
        """Check if input suggests to use kikuchipy parser or not."""
        return False

    def needs_score_parser(self):
        """Check if input suggests to use SCORE cellular automaton model parser or not."""
        return False

    def needs_qube_parser(self):
        """Check if input suggests to use Bruker QUBE parser or not."""
        return False

    def needs_paradis_parser(self):
        """Check if input suggests to use ParaDIS DDD parser or not."""
        return False

    def needs_brinckmann_parser(self):
        """Check if input suggests to use S. Brinckmann's EBSD parser or not."""
        return False

    #     """Check if input suggests to use Brinckmann parser or not."""
    #     if len(self.mime_types["cpr"]) == 1 and len(self.mime_types["crc"]) == 1:
    #         # HKL Channel 5 cpr/crc file should be a pair with the same file name
    #         if self.mime_types["cpr"][0].lower().replace(".cpr", "") \
    #             == self.mime_types["crc"][0].lower().replace(".crc", ""):
    #             # add files to self.dat
    #             return True
    #     if len(self.mime_types["ang"]) == 1:
    #         # consider in the future to use rather the kikuchipy or MTex parser
    #         # add files to self.dat
    #         return True
    #     return False
