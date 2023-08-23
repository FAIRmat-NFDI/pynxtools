"""
    A short description on STS reader which also suitable for file from STM .
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
from collections.abc import Callable
import json
import yaml

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.sts.sts_file_parser import from_dat_file_into_template
from pynxtools.dataconverter.readers.sts.stm_file_parser import STM_Nanonis
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
    'Environment': 'ENVIRONMENT[environment]',
    'Sample_bias': 'SAMPLE_BIAS[sample_bias]'
}
# For flatened key-value pair from nested dict.
REPLACE_NESTED: Dict[str, str] = {}


# pylint: disable=too-few-public-methods
class StmNanonisGeneric5e:
    """Class to handle 'stm' experiment of software version 'Generic 5e' from 'nanonis'
    vendor.
    """

    def __call__(self, template: Dict, data_file: str, config_dict: str, eln_dict: Dict) -> None:
        """Convert class instace as callable function.

        Parameters
        ----------
        template : Dict
            Template that will be filled.
        data_file : str
            The file from experiment
        config_dict : str
            Config file to map application definition to the raw file
        eln_dict : Dict
            user provided dict
        """

        STM_Nanonis(file_name=data_file).from_sxm_file_into_template(template,
                                                                     config_dict,
                                                                     eln_dict)


# pylint: disable=too-few-public-methods
class StsNanonisGeneric5e:
    """Class to handle 'sts' experiment of software version 'Generic 5e' from 'nanonis'
    vendor.
    """
    def __call__(self, template: Dict, data_file: str, config_dict: Dict, eln_dict: Dict) -> None:
        """Convert class instace as callable function.

        Parameters
        ----------
        template : Dict
            Template that will be filled.
        data_file : str
            The file from experiment
        config_dict : str
            Config file to map application definition to the raw file
        eln_dict : Dict
            user provided dict
        """
        from_dat_file_into_template(template, data_file,
                                    config_dict, eln_dict)


# pylint: disable=too-few-public-methods
class Spm:
    """This class is intended for taking care of vendor's name,
    experiment (stm, sts, afm) and software versions.

    Raises
    ------
    ValueError
        If experiment is not in ['sts', 'stm', 'afm']
    ValueError
        if vendor's name is not in ['nanonis']
    ValueError
        if software version is not in ['Generic 5e']
    """

    # parser navigate type
    par_nav_t = Dict[str, Union['par_nav_t', Callable]]
    __parser_navigation: Dict[str, par_nav_t] = \
        {'stm': {'nanonis': {'Generic 5e': StmNanonisGeneric5e}},
            'sts': {'nanonis': {'Generic 5e': StsNanonisGeneric5e}}
         }

    def get_appropriate_parser(self, eln_dict: Dict) -> Callable:
        """Search for appropriate prser and pass it the reader.

        Parameters
        ----------
        eln_dict : str
            User provided eln file (yaml) that must contain all the info about
            experiment, vendor's name and version of the vendor's software.

        Returns
        -------
            Return callable function that has capability to run the correponding parser.
        """

        experiment_t_key: str = "/ENTRY[entry]/experiment_type"
        experiment_t: str = eln_dict[experiment_t_key]
        try:
            experiment_dict: Spm.par_nav_t = self.__parser_navigation[experiment_t]
        except KeyError as exc:
            raise KeyError(f"Add correct experiment type in ELN file "
                           f" from {list(self.__parser_navigation.keys())}.") from exc

        vendor_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/SOFTWARE[software]/vendor"
        vendor_t: str = eln_dict[vendor_key]
        try:
            vendor_dict: Spm.par_nav_t = experiment_dict[vendor_t]  # type: ignore[assignment]
        except KeyError as exc:
            raise KeyError(f"Add correct vendor name in ELN file "
                           f" from {list(experiment_dict.keys())}.") from exc

        software_v_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/SOFTWARE[software]/@version"
        software_v: str = eln_dict[software_v_key]
        try:
            parser_cls: Callable = vendor_dict[software_v]  # type: ignore[assignment]
            # cls instance
            parser = parser_cls()
        except KeyError as exc:
            raise KeyError(f"Add correct software version in ELN file "
                           f" from {list(vendor_dict.keys())}.") from exc

        # Return callable function
        return parser


# pylint: disable=invalid-name, too-few-public-methods
class STMReader(BaseReader):
    """ Reader for XPS.
    """

    supported_nxdls = ["NXsts"]

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
            fl_obj: object
            if ext in ['sxm', 'dat']:
                data_file = file
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

        # Get callable object that has parser inside
        parser = Spm().get_appropriate_parser(eln_dict)
        parser(template, data_file, config_dict, eln_dict)

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
