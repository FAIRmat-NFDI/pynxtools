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

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.stm.bias_spec_file_parser import from_dat_file_into_template
from pynxtools.dataconverter.readers.stm.stm_file_parser import from_sxm_file_into_template


class STMReader(BaseReader):
    """ Reader for XPS.
    """
    # NXroot is a general purpose definition one can review data with this definition
    supported_nxdls = ["NXiv_sweep2"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None):
        """
            General read menthod to prepare the template.
        """

        has_sxm_input_file = False
        sxm_file: str = ""
        has_dat_input_file = False
        dat_file: str = ""
        filled_template: Union[Dict, None] = Template()
        config_dict: Union[Dict, None] = None

        for file in file_paths:
            ext = file.rsplit('.', 1)[-1]

            if ext == 'sxm':
                has_sxm_input_file = True
                sxm_file = file
            if ext == 'dat':
                has_dat_input_file = True
                dat_file = file
            if ext == 'json':
                with open(file, mode="r", encoding="utf-8") as jf:
                    config_dict = json.load(jf)
        if not has_dat_input_file and not has_sxm_input_file:
            raise ValueError("Not correct file has been found. please render correct input"
                             " file of spm with extension: .dat or .sxm")
        if has_dat_input_file and has_sxm_input_file:
            raise ValueError("Only one file from .dat or .sxm can be read.")
        if has_sxm_input_file and config_dict:
            from_sxm_file_into_template(template, sxm_file, config_dict)
        elif has_dat_input_file and config_dict:
            from_dat_file_into_template(template, dat_file, config_dict)
        else:
            raise ValueError("Not correct input file has been provided.")

        for key, val in template.items():

            if val is None:
                del template[key]
            else:
                filled_template[key] = val

        if not filled_template:
            # for key, val in filled_template.items():
            #     print(' ### : ', key)
            return filled_template
        else:
            raise ValueError("Reader could not read anything! Check for input files and the"
                             " corresponding extention.")


READER = STMReader
