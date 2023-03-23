"""
    A short description on STM reader.
"""
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


import os
from pathlib import Path
from typing import Any, Dict, Set, List
from typing import Tuple
import sys
import json

from nexusutils.dataconverter.readers.utils import flatten_and_replace, FlattenSettings
from nexusutils.dataconverter.readers.base.reader import BaseReader

# The bellow dict to replace keywords from provided yaml
CONVERT_DICT = {
    'Instrument': 'INSTRUMENT[instrument]',
    'Analyser': 'ELECTRONANALYSER[electronanalyser]',
    'Beam': 'BEAM[beam]',
    'unit': '@units',
    'version': '@version',
    'Sample': 'SAMPLE[sample]',
    'User': 'USER[user]',
    'Data': 'DATA[data]',
    'Source': 'SOURCE[source]',
    'Collectioncolumn': 'COLLECTIONCOLUMN[collectioncolumn]',
    'Energydispersion': 'ENERGYDISPERSION[energydispersion]',
    'Detector': 'DETECTOR[detector]'
}

REPLACE_NESTED: Dict[str, str] = {}

class STMReader(BaseReader):
    """ Reader for XPS.
    """
   # NXroot is a general purpose definition one can review data with this definition
    supported_nxdls = ["NXroot"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """
        """

        reader_dir = Path(__file__).parent
        config_file = reader_dir.joinpath("config_file.json")

        stm_data_dict: Dict[str, Any] = {}
        eln_data_dict: Dict[str, Any] = {}

        for file in file_paths:
            file_ext = os.path.splitext(file)[1]
            
            # for platening yaml file in python dict
            if file_ext in [".yaml", ".yml"]:
                with open(file, mode="r", encoding="utf-8") as eln:
                    eln_data_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(eln),
                            CONVERT_DICT,
                            REPLACE_NESTED
                        )
                    )
            
        with open(config_file, encoding="utf-8", mode="r") as cfile:
            config_dict = json.load(cfile)

        fill_template_with_xps_data(config_dict,
                                    xps_data_dict,
                                    template,
                                    ENTRY_SET)
        if eln_data_dict:
            fill_template_with_eln_data(eln_data_dict,
                                        config_dict,
                                        template,
                                        ENTRY_SET)
        else:
            raise ValueError("Eln file must be submited with some required fields and attributes.")

        final_template = Template()
        for key, val in template.items():
            if ("/ENTRY[entry]" not in key) and (val is not None):
                final_template[key] = val

        return final_template


READER = XPSReader
