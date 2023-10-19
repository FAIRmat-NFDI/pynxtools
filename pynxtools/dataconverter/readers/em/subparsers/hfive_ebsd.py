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
"""(Sub-)parser mapping concepts and content from community *.h5/*.h5ebsd files on NXem."""

import numpy as np
import h5py
from pynxtools.dataconverter.readers.em.subparsers.hfive import HdfFiveGenericReader


class HdfFiveCommunityReader(HdfFiveGenericReader):
    """Read modified H5EBSD (likely from Britton group)"""
    def __init__(self, file_name: str = ""):
        super().__init__(file_name)
        # this specialized reader implements reading capabilities for the following formats
        self.supported_version = {}
        self.version = {}
        self.supported_version["tech_partner"] = ["xcdskd"]
        self.supported_version["schema_name"] = ["H5EBSD"]
        self.supported_version["schema_version"] = ["0.1"]
        self.supported_version["writer_name"] = ["not standardized"]
        self.supported_version["writer_version"] = ["0.1"]
        self.supported = True
        # check if instance to process matches any of these constraints
        h5r = h5py.File(self.file_name, "r")
        if "/Manufacturer" in h5r:
            self.version["tech_partner"] \
                = super().read_strings_from_dataset(h5r["/Manufacturer"][()])
            # print(f"britton {self.version['tech_partner']}")
            if self.version["tech_partner"] not in self.supported_version["tech_partner"]:
                # print(f"{self.version['tech_partner']} is not {self.supported_version['tech_partner']} !")
                self.supported = False
        else:
            self.supported = False
        if "/Version" in h5r:
            self.version["schema_version"] \
                = super().read_strings_from_dataset(h5r["/Version"][()])
            # print(f"britton {self.version['schema_version']}")
            if self.version["schema_version"] not in self.supported_version["schema_version"]:
                # print(f"{self.version['schema_version']} is not any of {self.supported_version['schema_version']} !")
                self.supported = False
        else:
            self.supported = False
        h5r.close()

        if self.supported is True:
            # print(f"Reading {self.file_name} is supported")
            self.version["schema_name"] = self.supported_version["schema_name"]
            self.version["writer_name"] = self.supported_version["writer_name"]
            self.version["writer_version"] = self.supported_version["writer_version"]
            # print(f"{self.version['schema_name']}, {self.supported_version['schema_version']}, {self.supported_version['writer_name']}, {self.supported_version['writer_version']}")
        # else:
            # print(f"Reading {self.file_name} is not supported!")
