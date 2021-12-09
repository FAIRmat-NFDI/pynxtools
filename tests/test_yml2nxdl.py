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

import pytest
import logging

from nomad.datamodel import EntryArchive
import os
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')

from nexusparser.tools.yaml2nxdl import yaml2nxdl


@pytest.fixture
def parser():
    return yaml2nxdl.yaml2nxdl()


def test_link(parser):
    archive = EntryArchive()
    localDir = os.path.abspath(os.path.dirname(__file__))
    ref_xml_data = os.path.join(localDir, 'yaml2nxdl_test_data/Ref_NXtest_links.yml.nxdl.xml')
    with open(ref_xml_data, 'r') as file:
        xml_reference = file.readlines()
        #xml_reference = file.read()
    for i,line in enumerate(xml_reference):
            if '<link>' in line:
                a = line
                b = i
    print(type(xml_reference))

    parser.parse('yaml2nxdl/tests/yaml2nxdl_test_data/NXtest_links.yml', archive, logging.getLogger())
    parsed_xml_data = os.path.join(localDir, 'yaml2nxdl_test_data/NXtest_links.yml.nxdl.xml')
    with open(parsed_xml_data, 'r') as file:
        #xml_parsed = file.read()
        xml_parsed = file.readlines()
    for i,line in enumerate(xml_parsed):
            if '<link>' in line:
                assert line == a
                assert i == b
    print(type(xml_parsed))

    assert xml_reference == xml_parsed
    # load a txt file
    # xml file from parser
    # reference file
    '''
    run = archive.section_run[0]
    assert len(run.system) == 2
    assert len(run.calculation) == 2
    assert run.calculation[0].x_nexus_magic_value == 42
    '''

if __name__ == '__main__':
    p = parser()
    test_link(p)
    #nexus_helper = HandleNexus(sys.argv[1:])
    #nexus_helper.process_nexus_master_file(None)
