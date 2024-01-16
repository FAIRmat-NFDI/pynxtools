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
"""(Sub-)parser for reading content from ThermoFisher Velox *.emd (HDF5) via rosettasciio."""

from typing import Dict, List
from rsciio import emd

from pynxtools.dataconverter.readers.em.subparsers.rsciio_base import RsciioBaseParser


class RsciioVeloxSubParser(RsciioBaseParser):
    """Read Velox EMD File Format emd."""
    def __init__(self, entry_id: int = 1, file_path: str = ""):
        super().__init__(file_path)
        if entry_id > 0:
            self.entry_id = entry_id
        else:
            self.entry_id = 1
        self.id_mgn: Dict = {}
        self.prfx = None
        self.tmp: Dict = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        self.check_if_supported()

    def check_if_supported(self):
        try:
            self.objs = emd.file_reader(self.file_path)
            # TODO::what to do if the content of the file is larger than the available
            # main memory, one approach to handle this is to have the file_reader parsing
            # only the collection of the concepts without the actual instance data
            # based on this one could then plan how much memory has to be reserved
            # in the template and stream out accordingly
            self.supported = True
        except IOError:
            print(f"Loading {self.file_path} using {self.__name__} is not supported !")

    def parse_and_normalize_and_process_into_template(self, template: dict) -> dict:
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            self.tech_partner_to_nexus_normalization(template)
        else:
            print(f"{self.file_path} is not a Velox-specific "
                  f"EMD file that this parser can process !")
        return template

    def tech_partner_to_nexus_normalization(self, template: dict) -> dict:
        """Translate tech partner concepts to NeXus concepts."""
        self.normalize_bfdf_content(template)  # conventional bright/dark field
        self.normalize_adf_content(template)  # (high-angle) annular dark field
        self.normalize_edxs_content(template)  # EDS in the TEM
        self.normalize_eels_content(template)  # electron energy loss spectroscopy
        return template

    def normalize_bfdf_content(self, template: dict) -> dict:
        return template

    def normalize_adf_content(self, template: dict) -> dict:
        return template

    def normalize_edxs_content(self, template: dict) -> dict:
        return template

    def normalize_eels_content(self, template: dict) -> dict:
        return template
