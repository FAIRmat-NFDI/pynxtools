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
"""Base class to inherit sub-parser from when interacting with rosettasciio."""

# this subparser is currently implemented such that it represents the first
# and the second step of a parsing and mapping workflow whereby concepts and
# instance data within the representation realm of a tech partner is mapped
# onto the realm of NeXus e.g. to offer normalized content to e.g. NOMAD OASIS

# the first step is the reading of information (all code relevant to enable
# information extraction from a specific file of a tech partner
# the second step is normalization of the information
# the third step is (currently performed) with the nxs_hyperspy.py parser
# which finally processes the already normalized information into the
# template object that is thereafter consumed by the convert.py and writer.py
# functionalities to create a serialized NeXus data artifact

from typing import Dict


class RsciioBaseParser:
    def __init__(self, file_path: str = ""):
        # self.supported_version = VERSION_MANAGEMENT
        # self.version = VERSION_MANAGEMENT
        # tech_partner the company which designed this format
        # schema_name the specific name of the family of schemas supported by this reader
        # schema_version the specific version(s) supported by this reader
        # writer_name the specific name of the tech_partner's (typically proprietary) software
        self.prfx = None
        self.tmp: Dict = {}
        if file_path is not None and file_path != "":
            self.file_path = file_path
