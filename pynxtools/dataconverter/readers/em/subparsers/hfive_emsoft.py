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
from pynxtools.dataconverter.readers.em.subparsers.hfive import HdfFiveGenericReader


class HdfFiveEmSoftReader(HdfFiveGenericReader):
    """Read EMsoft H5 (Marc deGraeff Carnegie Mellon)"""
    def __init__(self, file_name: str = ""):
        super().__init__(file_name)
        # this specialized reader implements reading capabilities for the following formats
        self.supported_version = {}
        self.version = {}
        self.supported_version["tech_partner"] = ["EMsoft"]
        self.supported_version["schema_name"] = ["EMsoft"]
        self.supported_version["schema_version"] = ["EMsoft"]
        self.supported_version["writer_name"] = ["EMsoft"]
        self.supported_version["writer_version"] = ["EMsoft"]
        self.supported = True
        # check if instance to process matches any of these constraints
        h5r = h5py.File(self.file_name, "r")
        required_groups = ["CrystalData", "EMData", "EMheader", "NMLfiles", "NMLparameters"]
        for required_group in required_groups:
            if f"/{required_group}" not in h5r:
                self.supported = False
        h5r.close()
        if self.supported is True:
            # print(f"Reading {self.file_name} is supported")
            self.version = self.supported_version.copy()
            # print(f"{self.version['schema_name']}, {self.supported_version['schema_version']}, {self.supported_version['writer_name']}, {self.supported_version['writer_version']}")
        # else:
            # print(f"Reading {self.file_name} is not supported!")
