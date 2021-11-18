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

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
from nexusparser import NexusParser


@pytest.fixture
def parser():
    return NexusParser()


def test_example(parser):
    archive = EntryArchive()
    #parser.parse('tests/data/nexus.out', archive, logging)
    parser.parse('/home/sanya/work/FAIRmat/nexus/ARPES/201805_WSe2_arpes.nxs', archive, logging.getLogger())
    '''
    run = archive.section_run[0]
    assert len(run.system) == 2
    assert len(run.calculation) == 2
    assert run.calculation[0].x_nexus_magic_value == 42
    '''

if __name__ == '__main__':
    p = parser()
    test_example(p)
    #nexus_helper = HandleNexus(sys.argv[1:])
    #nexus_helper.process_nexus_master_file(None)
