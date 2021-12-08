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

from nexusparser.tools import read_nexus
import os
from nexusparser import NexusParser
import pytest
import logging

from nomad.datamodel import EntryArchive

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')


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
    nexus_helper.process_nexus_master_file(None, logger)

    # check logging result
    with open(os.path.join(localDir, 'data/read_nexus_test.log'), "r") as file:
        number_of_lines = len(file.readlines())
        file.seek(0)
        sum_char_values = sum(map(ord, file.read()))
    assert number_of_lines == 1653
    assert sum_char_values == 4419958
    print('Testing of read_nexus.py is SUCCESSFUL.')


def test_example(parser):
    archive = EntryArchive()
    parser.parse('tests/data/nexus.out', archive, logging)
    run = archive.section_run[0]
    assert len(run.system) == 2
    assert len(run.calculation) == 2
    assert run.calculation[0].x_nexus_magic_value == 42


if __name__ == '__main__':
    p = parser()
    test_read_nexus()
    # test_example(p)
