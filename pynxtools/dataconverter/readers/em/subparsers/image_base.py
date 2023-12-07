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
"""Parent class for all tech partner-specific image parsers for mapping on NXem."""

import numpy as np
from typing import Dict, List


class ImgsBaseParser:
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
        else:
            raise ValueError(f"{__name__} needs proper instantiation !")

    def init_named_cache(self, ckey: str):
        """Init a new cache for normalized image data if not existent."""
        # purpose of the cache is to hold normalized information
        if ckey not in self.tmp.keys():
            self.tmp[ckey] = {}
            return ckey
        else:
            raise ValueError(f"Existent named cache {ckey} must not be overwritten !")
