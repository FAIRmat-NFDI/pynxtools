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
import re
import xml.etree.ElementTree as ET
import yaml
from typing import Any
import click

from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.template import Template
from pynxtools.nexus.nexus import get_nexus_definitions_path


# TOSO: edit docs
def get_empty_template(nexus_def: str) -> Template:
    """Generate eln in yaml file

    Parameters
    ----------
    nexus_def : str
        Name of NeXus definition e.g. NXmpes
    eln_file : str
        Name of eln file, e.g. NAME or NAME.yaml.

    Return
    ------
        None
    """

    definition_path = get_nexus_definitions_path()

    def_path = os.path.join(definition_path,
                            'contributed_definitions',
                            f"{nexus_def}.nxdl.xml")
    print('def path : ', def_path)
    if os.path.exists(def_path):
        nxdl_root = ET.parse(def_path).getroot()
    else:
        def_path = os.path.join(definition_path,
                                'base_definitions',
                                f"{nexus_def}.nxdl.xml")

    if os.path.exists(def_path):
        nxdl_root = ET.parse(def_path).getroot()
    else:
        def_path = os.path.join(definition_path,
                                'applications',
                                f"{nexus_def}.nxdl.xml")
    if os.path.exists(def_path):
        nxdl_root = ET.parse(def_path).getroot()
    else:
        raise ValueError("Correct definition is rendered, try with correct definition name.")

    template = Template()
    generate_template_from_nxdl(nxdl_root, template)

    return template


def take_care_of_special_concept(key: str):
    """TODO while writting doc mention that
    """

    def unit_concept():
        return {'value': None,
                'unit': None}

    if key == '@units':
        return unit_concept()


def get_recursive_dict(concatenated_key: str,
                       recursive_dict: dict[str, Any],
                       level_to_skip: int) -> None:
    """_summary_

    Parameters
    ----------
    temp_dict : _type_
        _description_
    recursive_dict : _type_
        _description_
    """
    # splitig keys like: '/entry[ENTRY]/position[POSITION]/xx'.
    # skiping the first empty '' and top parts as directed by users.
    key_li = concatenated_key.split('/')[level_to_skip + 1:]
    # list of key for special consideration
    sp_key_li = ['@units']
    last_key = ""
    for key in key_li:
        if '[' in key and '/' not in key:
            key = re.findall(r'\[(.*?)\]', key,)[0].capitalize()
        if not key:
            continue
        last_key = key
        last_dict = recursive_dict
        if key in recursive_dict:
            if recursive_dict[key] is None:
                recursive_dict[key] = {}
                recursive_dict = recursive_dict[key]

            else:
                if key in sp_key_li:
                    recursive_dict.update(take_care_of_special_concept(key))
                else:
                    recursive_dict = recursive_dict[key]
        else:
            if key in sp_key_li:
                recursive_dict.update(take_care_of_special_concept(key))
            else:
                recursive_dict[key] = {}
                recursive_dict = recursive_dict[key]
    # For special key cleaning parts occurs inside take_care_of_special_concept func.
    if last_key not in sp_key_li:
        last_dict[last_key] = None


def generate_eln(nexus_def: str, eln_file: str, level_to_skip: int) -> None:
    """_summary_

    Parameters
    ----------
    nexus_def : str
        _description_
    eln_file : str
        _description_

    Returns:
        None
    """

    template = get_empty_template(nexus_def)
    recursive_dict: dict[str, Any] = {}
    for key, val in template.items():
        get_recursive_dict(key, recursive_dict, level_to_skip)

    name_split = eln_file.rsplit('.')

    if len(name_split) == 2 and not name_split[1] == 'yaml':
        raise ValueError("Eln file should come with 'yaml' extension or without extension.")
    if len(name_split) == 1:
        eln_file = eln_file + '.yaml'

    with open(eln_file, encoding='utf-8', mode='w') as eln_f:
        yaml.dump(recursive_dict, sort_keys=False, stream=eln_f)
