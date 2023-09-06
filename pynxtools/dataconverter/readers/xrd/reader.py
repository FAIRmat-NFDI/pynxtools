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


from typing import Tuple, Any, Dict, Union
import json
from pynxtools.dataconverter.readers.xrd.xrd_parser import parse_and_convert_file
from pynxtools.dataconverter.readers.utils import flatten_and_replace, FlattenSettings
import yaml
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.base.reader import BaseReader


CONVERT_DICT = {
    'Instrument': 'INSTRUMENT[instrument]',
    'Software': 'SOFTWARE[software]',
    'Hardware': 'Hardware[hardware]',
    'Analyser': 'ELECTRONANALYSER[electronanalyser]',
    'Beam': 'BEAM[beam]',
    'unit': '@units',
    'version': '@version',
    'Sample': 'SAMPLE[sample]',
    'User': 'USER[user]',
    'Data': 'DATA[data]',
    'Source': 'SOURCE[source]',
    'Environment': 'ENVIRONMENT[environment]',
    'Sample_bias': 'SAMPLE_BIAS[sample_bias]'
}

REPLACE_NESTED: Dict[str, str] = {}


class STMReader(BaseReader):
    """ Reader for XPS.
    """

    supported_nxdls = ["NXroot"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None):
        """
            General read menthod to prepare the template.
        """
        # has_sxm_file: bool = False
        # sxm_file: str = ""
        # has_dat_file: bool = False
        # dat_file: str = ""
        filled_template: Union[Dict, None] = Template()
        # config_dict: Union[Dict[str, Any], None] = None
        eln_dict: Union[Dict[str, Any], None] = None
        config_dict: Dict = {}

        data_file: str = ""
        for file in file_paths:
            ext = file.rsplit('.', 1)[-1]
            if ext == 'json':
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    config_dict = json.load(fl_obj)
            elif ext in ['yaml', 'yml']:
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(fl_obj),
                            CONVERT_DICT,
                            REPLACE_NESTED
                        )
                    )
            else:
                xrd_dict = parse_and_convert_file(file)
        # TODO combine nyaml, json, and xrd data here

        # Get rid of empty concept and cleaning up Template
        for key, val in template.items():

            if val is None:
                del template[key]
            else:
                filled_template[key] = val
        if not filled_template.keys():
            raise ValueError("Reader could not read anything! Check for input files and the"
                             " corresponding extention.")
        return filled_template


READER = STMReader
