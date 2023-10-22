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
"""(Sub-)parser mapping concepts and content from EDAX/AMETEK *.oh5/*.h5 (OIM Analysis) files on NXem."""

import numpy as np
import h5py
from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import read_strings_from_dataset


class HdfFiveEdaxOimAnalysisReader(HdfFiveBaseParser):
    """Read EDAX (O)H5"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp = {}
        self.supported_version = {}
        self.version = {}
        self.init_support()
        self.supported = False
        self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version["tech_partner"] = ["EDAX"]
        self.supported_version["schema_name"] = ["H5"]
        self.supported_version["schema_version"] \
            = ["OIM Analysis 8.6.0050 x64 [18 Oct 2021]", "OIM Analysis 8.5.1002 x64 [07-17-20]"]
        self.supported_version["writer_name"] = ["OIM Analysis"]
        self.supported_version["writer_version"] \
            = ["OIM Analysis 8.6.0050 x64 [18 Oct 2021]", "OIM Analysis 8.5.1002 x64 [07-17-20]"]

    def check_if_supported(self):
        """Check if instance matches all constraints to qualify as old EDAX"""
        self.supported = False
        with h5py.File(self.file_path, "r") as h5r:
            if "/Manufacturer" in h5r:
                self.version["tech_partner"] \
                    = super().read_strings_from_dataset(h5r["/Manufacturer"][()])
                # for 8.6.0050 but for 8.5.1002 it is a matrix, this is because how strings end up in HDF5 allowed for so much flexibility!
                if self.version["tech_partner"] not in self.supported_version["tech_partner"]:
                    self.supported = False
            else:
                self.supported = False
            if "/Version" in h5r:
                self.version["schema_version"] \
                    = super().read_strings_from_dataset(h5r["/Version"][()])
                if self.version["schema_version"] not in self.supported_version["schema_version"]:
                    self.supported = False
            else:
                self.supported = False

            if self.supported is True:
                self.version["schema_name"] = self.supported_version["schema_name"]
                self.version["writer_name"] = self.supported_version["writer_name"]
                self.version["writer_version"] = self.supported_version["writer_version"]
