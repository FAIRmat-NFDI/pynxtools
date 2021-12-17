#!/usr/bin/env python3
"""
#This tool accomplishes some tests for the yaml2nxdl parser
"""
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

import os
import sys
from datetime import datetime
from pathlib import Path
import pytest
from click.testing import CliRunner
import nexusparser.tools.yaml2nxdl.yaml2nxdl as yaml2nxdl

sys.path.insert(0, '../nexusparser/tools')
sys.path.insert(0, '../nexusparser/tools/yaml2nxdl')

LOCALDIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def test_links():
    """
    # first test: check the correct parsing of links
    """
    # Files
    ref_xml_link_file = os.path.join(LOCALDIR, 'data/yaml2nxdl_test_data/Ref_NXtest_links.nxdl.xml')
    test_yml_link_file = 'data/yaml2nxdl_test_data/NXtest_links.yml'
    test_xml_link_file = os.path.join(LOCALDIR, 'data/yaml2nxdl_test_data/NXtest_links.nxdl.xml')
    test_match_string = '<link>'

    # Reference file is called
    with open(ref_xml_link_file, 'r') as file:
        xml_reference = file.readlines()
    for i, line in enumerate(xml_reference):
        if test_match_string in line:
            ref_line = line
            ref_line_index = i

    # Test file is generated and called
    result = CliRunner().invoke(yaml2nxdl.yaml2nxdl, ['--input-file', test_yml_link_file])
    assert result.exit_code == 0
    path = Path(test_xml_link_file)
    timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    assert timestamp == now, 'xml file not generated'
    with open(test_xml_link_file, 'r') as file:
        xml_tested = file.readlines()
    for i, line in enumerate(xml_tested):
        if test_match_string in line:
            assert line == ref_line
            assert i == ref_line_index


def test_symbols():
    """
    # second test: check the correct parsing of symbols
    """
    # Files
    ref_xml_symbol_file = os.path.join(
        LOCALDIR, 'data/yaml2nxdl_test_data/Ref_NXnested_symbols.nxdl.xml')
    test_yml_symbol_file = 'data/yaml2nxdl_test_data/NXnested_symbols.yml'
    test_xml_symbol_file = os.path.join(
        LOCALDIR, 'data/yaml2nxdl_test_data/NXnested_symbols.nxdl.xml')
    test_match_string = '<symbol>'

    # Reference file is called
    with open(ref_xml_symbol_file, 'r') as file:
        xml_reference = file.readlines()
    for i, line in enumerate(xml_reference):
        if test_match_string in line:
            ref_line = line
            ref_line_index = i

    # Test file is generated and called
    result = CliRunner().invoke(yaml2nxdl.yaml2nxdl, ['--input-file', test_yml_symbol_file])
    assert result.exit_code == 0
    path = Path(test_xml_symbol_file)
    timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    assert timestamp == now, 'xml file not generated'
    with open(test_xml_symbol_file, 'r') as file:
        xml_tested = file.readlines()
    for i, line in enumerate(xml_tested):
        if test_match_string in line:
            assert line == ref_line
            assert i == ref_line_index


if __name__ == '__main__':
    test_links()
    test_symbols()
