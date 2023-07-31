"""
    A short description on SPM reader.
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


from typing import Any, Dict, Tuple, Union
import json
import yaml

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.stm.bias_spec_file_parser import from_dat_file_into_template
from pynxtools.dataconverter.readers.stm.stm_file_parser import STM_Nanonis
from pynxtools.dataconverter.readers.utils import flatten_and_replace, FlattenSettings


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
    'Collectioncolumn': 'COLLECTIONCOLUMN[collectioncolumn]',
    'Energydispersion': 'ENERGYDISPERSION[energydispersion]',
    'Detector': 'DETECTOR[detector]',
    'Environment': 'ENVIRONMENT[environment]',
}

REPLACE_NESTED: Dict[str, str] = {}


# pylint: disable=invalid-name
class STMReader(BaseReader):
    """ Reader for XPS.
    """

    supported_nxdls = ["NXiv_sweep2"]

    def get_input_file_info(self, input_paths: Tuple[str]):
        """get and varify input files.

        Parameters
        ----------
        input_path : tuple
            Tuple of input paths.

        """
        has_sxm_file: bool = False
        sxm_file: str = ""
        has_dat_file: bool = False
        dat_file: str = ""
        config_dict: Union[Dict[str, Any], None] = None
        eln_dict: Union[Dict[str, Any], None] = None

        for file in input_paths:
            ext = file.rsplit('.', 1)[-1]
            fl_obj: object
            if ext == 'sxm':
                has_sxm_file = True
                sxm_file = file
            if ext == 'dat':
                has_dat_file = True
                dat_file = file
            if ext == 'json':
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    config_dict = json.load(fl_obj)
            if ext in ['yaml', 'yml']:
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(fl_obj),
                            CONVERT_DICT,
                            REPLACE_NESTED
                        )
                    )
        return (has_sxm_file, sxm_file, has_dat_file, dat_file, config_dict, eln_dict)

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None):
        """
            General read menthod to prepare the template.
        """

        has_sxm_file: bool = False
        sxm_file: str = ""
        has_dat_file: bool = False
        dat_file: str = ""
        filled_template: Union[Dict, None] = Template()
        config_dict: Union[Dict[str, Any], None] = None
        eln_dict: Union[Dict[str, Any], None] = None

        has_sxm_file, sxm_file, has_dat_file, dat_file, config_dict, eln_dict = \
            self.get_input_file_info(file_paths)

        if not has_dat_file and not has_sxm_file:
            raise ValueError("Not correct file has been found. please render correct input"
                             " file of spm with extension: .dat or .sxm")
        if has_dat_file and has_sxm_file:
            raise ValueError("Only one file from .dat or .sxm can be read.")
        if has_sxm_file and config_dict and eln_dict:
            STM_Nanonis(file_name=sxm_file).from_sxm_file_into_template(template,
                                                                        config_dict,
                                                                        eln_dict)
        elif has_dat_file and config_dict and eln_dict:
            from_dat_file_into_template(template, dat_file, config_dict,
                                        eln_dict)
        else:
            raise ValueError("Not correct input file has been provided.")

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
