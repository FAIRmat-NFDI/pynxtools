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

"""A generic reader for loading XPS-specs (X-ray Photoelectron Spectroscopy) file
    into XPS-specs data model.
"""

from nexusutils.dataconverter.readers.base.reader import BaseReader
from typing import Tuple

import xml.etree.ElementTree as ET
import os
from typing import Any
import numpy as np
import sys
from .reader_utils import XpsDataFileParser
np.set_printoptions(threshold=sys.maxsize)

class XPS_Reader(BaseReader):

    supported_nxdls = ["NXtest", "NXroot"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""

        file = '/home/rubel/Nomad-FAIRmat/NomadGH/Nomad_work/XPS_Data_Analysis/copy_In-situ_PBTTT_XPS_SPECS.xml'
        Xps_paser_object = XpsDataFileParser(file_path=file)
        data_dict = Xps_paser_object.get_dict()

        if not template.items():
            # intended for NXroot
            for key, val in data_dict.items():
                if key[-1] == "/":
                    key = key[:-1]
                if val not in ["None"]:
                    template[key] = val

        elif template.items():
            # intended for NXtest
            for key, val in data_dict.items():
                if key[-1] == "/":
                    key = key[:-1]

                if val not in ["None"]:
                    template[key] = val

        return template


READER = XPS_Reader