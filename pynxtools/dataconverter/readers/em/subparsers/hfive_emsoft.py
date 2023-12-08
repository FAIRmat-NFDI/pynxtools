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
"""(Sub-)parser mapping concepts and content from Marc deGraeff's EMsoft *.h5 files on NXem."""

import numpy as np
import h5py
from typing import Dict

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset


class HdfFiveEmSoftReader(HdfFiveBaseParser):
    """Read EMsoft H5 (Marc deGraeff Carnegie Mellon)"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        if self.is_hdf is True:
            self.init_support()
            self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["EMsoft"]
        self.supported_version["schema_name"] = ["EMsoft"]
        self.supported_version["schema_version"] = ["EMsoft"]
        self.supported_version["writer_name"] = ["EMsoft"]
        self.supported_version["writer_version"] = ["EMsoft"]

    def check_if_supported(self):
        """Check if instance matches all constraints to EMsoft"""
        self.supported = True
        with h5py.File(self.file_path, "r") as h5r:
            req_groups = ["CrystalData", "EMData", "EMheader", "NMLfiles", "NMLparameters"]
            for req_group in req_groups:
                if f"/{req_group}" not in h5r:
                    self.supported = False

            if self.supported is True:
                self.version = self.supported_version.copy()

    def parse_and_normalize(self):
        pass
