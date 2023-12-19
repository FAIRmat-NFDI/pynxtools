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
"""(Sub-)parser for reading content from Bruker *.BCF files via rosettasciio."""

from typing import Dict, List
from rsciio import bruker

from pynxtools.dataconverter.readers.em.subparsers.rsciio_base import RsciioBaseParser


class RsciioBrukerSubParser(RsciioBaseParser):
    """Read Bruker BCF File Format bcf."""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp: Dict = {}
        self.objs: List = []
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        self.check_if_supported()

    def check_if_supported(self):
        try:
            self.objs = bruker.file_reader(self.file_path)
            # TODO::what to do if the content of the file is larger than the available
            # main memory, one approach to handle this is to have the file_reader parsing
            # only the collection of the concepts without the actual instance data
            # based on this one could then plan how much memory has to be reserved
            # in the template and stream out accordingly
            self.supported = True
        except IOError:
            print(f"Loading {self.file_path} using {self.__name__} is not supported !")

    def parse_and_normalize(self):
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            print(f"Parsing with {self.__name__}...")
            self.tech_partner_to_nexus_normalization()
        else:
            print(f"{self.file_path} is not a Bruker-specific "
                  f"BCF file that this parser can process !")

    def tech_partner_to_nexus_normalization(self):
        """Translate tech partner concepts to NeXus concepts."""
        self.normalize_eds_content()
        self.normalize_eels_content()

    def normalize_eds_content(self):
        pass

    def normalize_eels_content(self):
        pass

    def process_into_template(self, template: dict) -> dict:
        if self.supported is True:
            self.process_event_data_em_metadata(template)
            self.process_event_data_em_data(template)
        return template

    def process_event_data_em_metadata(self, template: dict) -> dict:
        return template

    def process_event_data_em_data(self, template: dict) -> dict:
        return template
