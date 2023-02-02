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


class EmUseCaseSelector:  # pylint: disable=R0903
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
        self.vendor_parser = "none"
        self.vendor: List[str] = []
        self.eln: List[str] = []
        self.eln_parser = "none"
        self.is_valid = False
        self.supported_mime_types = ["bcf", "emd", "dm3", "h5oina", "yaml", "yml"]
        for mime_type in self.supported_mime_types:
            self.case[mime_type] = []
        for file_name in file_paths:
            index = file_name.lower().rfind(".")
            if index >= 0:
                suffix = file_name.lower()[index + 1::]
                add = (suffix in self.supported_mime_types) \
                    and (file_name not in self.case[suffix])
                if add is True:
                    self.case[suffix].append(file_name)
        # the em reader currently supports a combination of one vendor file and
        # one ELN/YAML file, vendor files can come from different microscopes
        # which requires to distinguish between which reader has to be used
        # the OxfordInstrument reader for H5OINA
        # or the HyperSpy reader for Bruker BCF, Velox EMD, or Digital Micrograph DM3
        oina_input = 0
        for mime_type, value in self.case.items():
            if mime_type in ["h5oina"]:
                oina_input += len(value)
        hspy_input = 0
        for mime_type, value in self.case.items():
            if mime_type in ["bcf", "dm3", "emd"]:
                hspy_input += len(value)

        assert (oina_input == 1) or (hspy_input == 1), \
            "Currently the reader supports to have only one vendor input file!"
        if oina_input == 1:
            self.vendor += self.case["h5oina"]
            self.vendor_parser = "oina"
        if hspy_input == 1:
            for mime_type in ["bcf", "emd", "dm3"]:
                self.vendor += self.case[mime_type]
                self.vendor_parser = "hspy"

        eln_input = len(self.case["yaml"]) + len(self.case["yml"])
        assert eln_input == 1, \
            "Currently the reader supports to have only one YAML input-file!"

        for mime_type in ["yaml", "yml"]:
            self.eln += self.case[mime_type]
            self.eln_parser = "nomad-oasis"

        self.is_valid = True

# test = EmUseCaseSelector(("a.bcf", "b.yaml", "c.apt", "d.h5oina"))
