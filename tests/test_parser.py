"""Test scripts for parser.py tool

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

import xml.etree.ElementTree as ET
import sys
import os
import logging
import pytest
from nomad.datamodel import EntryArchive
from nexusparser.tools import nexus  # noqa: E402
from nexusparser.parser import NexusParser  # noqa: E402
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')


@pytest.fixture
def parser():
    """Helper function to launch NexusParser class

"""
    return NexusParser()


def test_nexus(tmp_path):
    """The nexus test function

"""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    example_data = os.path.join(local_dir, 'data/nexus_test_data/201805_WSe2_arpes.nxs')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.\
        FileHandler(os.path.join(tmp_path, 'nexus_test.log'), 'w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, [example_data])
    nexus_helper.process_nexus_master_file(None)

    with open(os.path.join(tmp_path, 'nexus_test.log'), 'r') as logfile:
        log = logfile.readlines()
    with open(os.path.join(local_dir, 'data/nexus_test_data/Ref_nexus_test.log'), 'r') as reffile:
        ref = reffile.readlines()

    assert log == ref

    # didn't work with filecmp library
    # log = os.path.join(local_dir, 'data/nexus_test_data/nexus_test.log')
    # ref = os.path.join(local_dir, 'data/nexus_test_data/Ref2_nexus_test.log')
    # print('yoyo', filecmp.cmp(log, ref, shallow=False))

    print('Testing of nexus.py is SUCCESSFUL.')


def test_get_node_at_nxdl_path():
    """Test to verify if we receive the right XML element for a given NXDL path"""
    nxdl_file_path = "tests/data/tools/dataconverter/NXtest.nxdl.xml"
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/NXODD_name", elem=elem)
    assert node.attrib["type"] == "NXdata"
    assert node.attrib["name"] == "NXODD_name"

    node = nexus.get_node_at_nxdl_path("/ENTRY/NXODD_name/float_value", elem=elem)
    assert node.attrib["type"] == "NX_FLOAT"
    assert node.attrib["name"] == "float_value"

    nxdl_file_path = "nexusparser/definitions/contributed_definitions/NXellipsometry.nxdl.xml"
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/derived_parameters", elem=elem)
    assert node.attrib["type"] == "NXprocess"

    nxdl_file_path = "nexusparser/definitions/contributed_definitions/NXem_nion.nxdl.xml"
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/em_lab/hadf/SCANBOX_EM", elem=elem)
    assert node.attrib["type"] == "NXscanbox_em"

    nxdl_file_path = "nexusparser/definitions/contributed_definitions/NXmpes.nxdl.xml"
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/DATA/VARIABLE", elem=elem)
    assert node.attrib["name"] == "VARIABLE"

    nxdl_file_path = "nexusparser/definitions/contributed_definitions/NXmpes.nxdl.xml"
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/USER/role", elem=elem)
    assert node.attrib["name"] == "role"


def test_example():
    """Tests if parser can parse our example data

"""
    archive = EntryArchive()

    import structlog

    # local_dir = os.path.abspath(os.path.dirname(__file__))
    # example_data = os.path.join(local_dir, 'data/nexus_test_data/em0001.test.nxs')
    # parser().parse(example_data, archive, structlog.get_logger())
    # assert archive.nexus.nx_application_em_nion.\
    #     nx_group_ENTRY[0].nx_group_operator.nx_field_affiliation.nx_value ==
    #     "Humboldt Universität zu Berlin"

    # local_dir = os.path.abspath(os.path.dirname(__file__))
    # example_data = os.path.join(local_dir, 'data/nexus_test_data/mpes2.test.nxs')
    # parser().parse(example_data, archive, structlog.get_logger())
    # assert archive.nexus.nx_application_mpes.\
    #     nx_group_ENTRY[0].nx_field_definition.nx_value == "NXmpes"

    local_dir = os.path.abspath(os.path.dirname(__file__))
    example_data = os.path.join(local_dir, 'data/nexus_test_data/201805_WSe2_arpes.nxs')
    parser().parse(example_data, archive, structlog.get_logger())
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_SAMPLE[0].nx_field_pressure.nx_value == 3.27e-10
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_SAMPLE[0].nx_field_pressure.nx_unit == "millibar"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_SAMPLE[0].nx_field_pressure.m_def.nx_units == "NX_PRESSURE"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_INSTRUMENT[0].\
        nx_group_monochromator.nx_field_energy.nx_value == 36.49699020385742
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_INSTRUMENT[0].\
        nx_group_monochromator.nx_field_energy.nx_name == 'energy'
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_analyser.\
        nx_field_entrance_slit_size.nx_value == 750
    # good ENUM - x-ray
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_SOURCE[0].\
        nx_field_probe.nx_value == 'x-ray'
    # wrong inherited ENUM - Burst
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_SOURCE[0].\
        nx_field_mode.nx_value is None
    # wrong inherited ENUM for extended field - 'Free Electron Laser'
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_SOURCE[0].\
        nx_field_type.nx_value is None
    # 1D datasets
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[0].nx_name == "angles"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[1].nx_name == "delays"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[2].nx_name == "energies"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[0].nx_unit == "1/Å"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[1].nx_unit == "fs"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[2].nx_unit == "eV"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[0].nx_value[0] == 0.10033616393632831
    # 2D datasets
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_DATA[0].nx_name == "data"
    assert archive.nexus.nx_application_arpes.\
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_DATA[0].nx_value[2] == 0.0
    assert pytest.approx(
        archive.nexus.nx_application_arpes.
        nx_group_ENTRY[0].nx_group_DATA[0].nx_field_DATA[0].nx_value[3] - 0.00078192557) \
        == 0.0
