"""This is a code that performs several tests on nexus tool

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
import logging
import xml.etree.ElementTree as ET

from pynxtools.nexus import nexus


def test_get_nexus_classes_units_attributes():
    """Check the correct parsing of a separate list for:
Nexus classes (base_classes)
Nexus units (memberTypes)
Nexus attribute type (primitiveTypes)
the tested functions can be found in nexus.py file
"""

    # Test 1
    nexus_classes_list = nexus.get_nx_classes()

    assert 'NXbeam' in nexus_classes_list

    # Test 2
    nexus_units_list = nexus.get_nx_units()
    assert 'NX_TEMPERATURE' in nexus_units_list

    # Test 3
    nexus_attribute_list = nexus.get_nx_attribute_type()
    assert 'NX_FLOAT' in nexus_attribute_list


def test_nexus(tmp_path):
    """
    The nexus test function
    """
    local_dir = os.path.abspath(os.path.dirname(__file__))
    example_data = os.path.join(local_dir, '../data/nexus/201805_WSe2_arpes.nxs')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.\
        FileHandler(os.path.join(tmp_path, 'nexus_test.log'), 'w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, example_data, None, None)
    nexus_helper.process_nexus_master_file(None)

    with open(os.path.join(tmp_path, 'nexus_test.log'), 'r', encoding='utf-8') as logfile:
        log = logfile.readlines()
    with open(
        os.path.join(local_dir, '../data/nexus/Ref_nexus_test.log'),
        'r',
        encoding='utf-8'
    ) as reffile:
        ref = reffile.readlines()
    assert log == ref

    # import filecmp
    # # didn't work with filecmp library
    # log = os.path.join(local_dir, '../data/nexus_test_data/nexus_test.log')
    # ref = os.path.join(local_dir, '../data/nexus_test_data/Ref_nexus_test.log')
    # print(filecmp.cmp(log, ref, shallow=False))

    # print('Testing of nexus.py is SUCCESSFUL.')


def test_get_node_at_nxdl_path():
    """Test to verify if we receive the right XML element for a given NXDL path"""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nxdl_file_path = os.path.join(local_dir, "../data/dataconverter/NXtest.nxdl.xml")
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path("/ENTRY/NXODD_name", elem=elem)
    assert node.attrib["type"] == "NXdata"
    assert node.attrib["name"] == "NXODD_name"

    node = nexus.get_node_at_nxdl_path("/ENTRY/NXODD_name/float_value", elem=elem)
    assert node.attrib["type"] == "NX_FLOAT"
    assert node.attrib["name"] == "float_value"

    node = nexus.get_node_at_nxdl_path("/ENTRY/NXODD_name/AXISNAME/long_name", elem=elem)
    assert node.attrib["name"] == "long_name"

    nxdl_file_path = os.path.join(
        local_dir,
        "../../pynxtools/definitions/contributed_definitions/NXem.nxdl.xml"
    )
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/measurement/EVENT_DATA_EM/USER/affiliation",
        elem=elem)
    assert node.attrib["name"] == "affiliation"

    node = nexus.get_node_at_nxdl_path("/ENTRY/measurement", elem=elem)
    assert node.attrib["type"] == "NXevent_data_em_set"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/measurement/EVENT_DATA_EM/SPECTRUM_SET/summary", elem=elem)
    assert node.attrib["type"] == "NXdata"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/measurement/EVENT_DATA_EM/SPECTRUM_SET/summary/DATA", elem=elem)
    assert node.attrib["type"] == "NX_NUMBER"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/measurement/EVENT_DATA_EM/SPECTRUM_SET/summary/AXISNAME_indices",
        elem=elem)
    assert node.attrib["name"] == "AXISNAME_indices"

    node = nexus.get_node_at_nxdl_path("/ENTRY/COORDINATE_SYSTEM_SET", elem=elem)
    assert node.attrib["type"] == "NXcoordinate_system_set"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/COORDINATE_SYSTEM_SET/TRANSFORMATIONS", elem=elem)
    assert node.attrib["type"] == "NXtransformations"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/COORDINATE_SYSTEM_SET/TRANSFORMATIONS/AXISNAME", elem=elem)
    assert node.attrib["type"] == "NX_NUMBER"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/COORDINATE_SYSTEM_SET/TRANSFORMATIONS/AXISNAME/transformation_type",
        elem=elem)
    assert node.attrib["name"] == "transformation_type"

    nxdl_file_path = os.path.join(
        local_dir,
        "../../pynxtools/definitions/contributed_definitions/NXiv_temp.nxdl.xml"
    )
    elem = ET.parse(nxdl_file_path).getroot()
    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller",
        elem=elem)
    assert node.attrib["name"] == "voltage_controller"

    node = nexus.get_node_at_nxdl_path(
        "/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller/calibration_time",
        elem=elem)
    assert node.attrib["name"] == "calibration_time"


def test_get_inherited_nodes():
    """Test to verify if we receive the right XML element list for a given NXDL path."""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nxdl_file_path = os.path.join(
        local_dir,
        "../../pynxtools/definitions/contributed_definitions/NXiv_temp.nxdl.xml"
    )
    elem = ET.parse(nxdl_file_path).getroot()
    (_, _, elist) = nexus.get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT",
        elem=elem)
    assert len(elist) == 3

    (_, _, elist) = nexus.get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller",
        elem=elem)
    assert len(elist) == 4

    (_, _, elist) = nexus.get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller",
        nx_name="NXiv_temp")
    assert len(elist) == 4


def test_c_option(tmp_path):
    """
    To check -c option from IV_temp.nxs.
    """

    local_path = os.path.dirname(__file__)
    path_to_ref_files = os.path.join(local_path, '../data/nexus/')
    ref_file = path_to_ref_files + 'Ref1_c_option_test.log'
    tmp_file = os.path.join(tmp_path, 'c_option_1_test.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(tmp_file, 'w')

    with open(ref_file, encoding='utf-8', mode='r') as ref_f:
        ref = ref_f.readlines()

    handler = logging.FileHandler(tmp_file, 'w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, None, None, '/NXbeam')
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding='utf-8', mode='r') as tmp_f:
        tmp = tmp_f.readlines()

    assert tmp == ref

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, 'w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, None, None, '/NXdetector/data')
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding='utf-8', mode='r') as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == 'INFO: entry/instrument/analyser/data\n'

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, 'w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, None, None, '/NXdata@signal')
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding='utf-8', mode='r') as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == 'INFO: entry/data@signal\n'


def test_d_option(tmp_path):
    """
    To check -d option for default NXarpes test data file.
    """

    tmp_file = os.path.join(tmp_path, 'd_option_1_test.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(tmp_file, 'w')

    handler = logging.FileHandler(tmp_file, 'w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, None, '/entry/instrument/analyser/data', None)
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding='utf-8', mode='r') as tmp_f:
        tmp = tmp_f.readlines()

    assert tmp[0] == 'DEBUG: ===== FIELD (//entry/instrument/analyser/data): ' + \
        '<HDF5 dataset "data": shape (80, 146, 195), type "<f4">\n'
