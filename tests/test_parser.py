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
import pytest
import logging
from nomad.datamodel import EntryArchive

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
from nexusparser.tools import read_nexus  # noqa: E402
from nexusparser import NexusParser  # noqa: E402


@pytest.fixture
def parser():
    return NexusParser()


def test_read_nexus():
    localDir = os.path.abspath(os.path.dirname(__file__))
    example_data = os.path.join(localDir, 'data/nexus_test_data/201805_WSe2_arpes.nxs')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(localDir, 'data/read_nexus_test.log'), 'w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = read_nexus.HandleNexus(logger, [example_data])
    nexus_helper.process_nexus_master_file(None)

    # check logging result
    with open(os.path.join(localDir, 'data/read_nexus_test.log'), "r") as file:
        number_of_lines = len(file.readlines())
        file.seek(0)
        sum_char_values = sum(map(ord, file.read()))
    assert number_of_lines == 1653
    assert sum_char_values == 4419958
    print('Testing of read_nexus.py is SUCCESSFUL.')


@pytest.mark.skip(reason="not to test it alone")
def testing_nxdl_to_attr_obj_1(example_path, result_str):
    result = read_nexus.nxdl_to_attr_obj(example_path)
    assert result.attrib['type'] == result_str, "failed on: " + example_path + "expected type: " + result_str


def test_nxdl_to_attr_obj():
    testing_nxdl_to_attr_obj_1('NXsqom:/ENTRY/instrument/SOURCE', "NXsource")
    testing_nxdl_to_attr_obj_1('NXspe:/ENTRY/NXSPE_info', "NXcollection")
    # test_nxdl_to_attr_obj_1('NXem_base_draft.yml:/ENTRY/SUBENTRY/thumbnail/mime_type', "")


def test_example(parser):
    archive = EntryArchive()
    localDir = os.path.abspath(os.path.dirname(__file__))
    example_data = os.path.join(localDir, 'data/nexus_test_data/201805_WSe2_arpes.nxs')
    parser.parse(example_data, archive, logging.getLogger())
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_SAMPLE[0].nx_field_pressure.nx_unit == "millibar"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_SAMPLE[0].nx_field_pressure.m_def.nx_units == "NX_PRESSURE"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_MONOCHROMATOR[0].nx_field_energy.nx_value == 36.49699020385742
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_INSTRUMENT[0].nx_group_MONOCHROMATOR[0].nx_field_energy.nx_name == 'energy'
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[0].nx_name == "angles"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[1].nx_name == "delays"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[2].nx_name == "energies"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[0].nx_unit == "1/Å"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[1].nx_unit == "fs"
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_group_DATA[0].nx_field_VARIABLE[2].nx_unit == "eV"


if __name__ == '__main__':
    # test_read_nexus()
    # test_nxdl_to_attr_obj()
    p = parser()
    test_example(p)
