"""This test is dedicated generate_eln converter tool.
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
from typing import Dict
from click import testing


import yaml
from pynxtools.eln_mapper import eln_mapper


def check_keys_from_two_dict(dict1: Dict, dict2: Dict):
    """Compare keys of two dicts.

    Parameters
    ----------
    dict1 : Dict
        Dict-1 to compare the key with Dict-2
    dict2 : Dict
        Dict-2 to compare the key with Dict-1
    """
    for (key1, val1), (key2, val2) in zip(dict1.items(), dict2.items()):
        assert key1 == key2, "Test and Ref yaml file have different keys."
        if isinstance(val1, dict) and isinstance(val2, dict):
            check_keys_from_two_dict(val1, val2)


def test_reader_eln(tmp_path):
    """Test eln that goes with reader.

    Parameters
    ----------
    tmp_path : pathlib.Path
        A temporary path that is created for pytest
    """

    local_dir = os.path.abspath(os.path.dirname(__file__))
    ref_file = os.path.join(local_dir, '../data/eln_mapper/eln.yaml')

    test_file = os.path.join(tmp_path, 'eln.yaml')
    cli_run = testing.CliRunner()
    cli_run.invoke(eln_mapper.get_eln, [
        "--nxdl",
        "NXmpes",
        "--skip-top-levels",
        1,
        "--output-file",
        test_file,
        "--eln-type",
        'eln'])

    with open(ref_file, encoding='utf-8', mode='r') as ref_f:
        ref_dict = yaml.safe_load(ref_f)

    with open(test_file, encoding='utf-8', mode='r') as test_f:
        test_dict = yaml.safe_load(test_f)

    check_keys_from_two_dict(ref_dict, test_dict)


def test_scheme_eln(tmp_path):
    """Test Eln that goes in Nomad

    Parameters
    ----------
    tmp_path : pathlib.Path
        A temporary path that is created for pytest
    """

    local_dir = os.path.abspath(os.path.dirname(__file__))
    ref_file = os.path.join(local_dir, '../data/eln_mapper/mpes.scheme.archive.yaml')

    test_file = os.path.join(tmp_path, '.scheme.archive.yaml')
    cli_run = testing.CliRunner()
    cli_run.invoke(eln_mapper.get_eln, [
        "--nxdl",
        "NXmpes",
        "--output-file",
        test_file,
        "--eln-type",
        'scheme_eln'])
    with open(ref_file, encoding='utf-8', mode='r') as ref_f:
        ref_dict = yaml.safe_load(ref_f)

    with open(test_file, encoding='utf-8', mode='r') as test_f:
        test_dict = yaml.safe_load(test_f)

    check_keys_from_two_dict(ref_dict, test_dict)
