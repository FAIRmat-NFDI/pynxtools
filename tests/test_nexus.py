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

from typing import cast, Any

import pytest

from nomad.metainfo import Definition, Section
from nomad.datamodel import EntryArchive
from nomad.metainfo import nexus
from nexusparser import tools


@pytest.mark.parametrize('path,value', [
    pytest.param('nexus_metainfo_package.name', 'nexus'),
    pytest.param('nexus_metainfo_package.NXobject.name', 'NXobject'),
    pytest.param('nexus_metainfo_package.NXentry.nx_kind', 'group'),
    pytest.param('nexus_metainfo_package.NXentry.NXdata', '*'),
    pytest.param('nexus_metainfo_package.NXdetector.real_time', '*'),
    pytest.param('nexus_metainfo_package.NXentry.NXdata.nx_optional', True),
    pytest.param('nexus_metainfo_package.NXentry.DATA.section_def.nx_kind', 'group'),
    pytest.param('nexus_metainfo_package.NXentry.DATA.section_def.nx_optional', True),
    pytest.param('nexus_metainfo_package.NXentry.DATA.section_def.name', 'NXdata'),
    pytest.param('nexus_metainfo_package.NXdetector.real_time.name', 'real_time'),
    pytest.param('nexus_metainfo_package.NXdetector.real_time.nx_type', 'NX_NUMBER'),
    pytest.param('nexus_metainfo_package.NXdetector.real_time.nx_units', 'NX_TIME'),
    pytest.param('nexus_metainfo_package.NXarpes.NXentry.NXdata.nx_optional', False),
    pytest.param('nexus_metainfo_package.NXentry.nx_category', 'base'),
    pytest.param('nexus_metainfo_package.NXapm.nx_category', 'application')
])
def test_assert_nexus_metainfo(path: str, value: Any):
    '''
    Test the existence of nexus metainfo
    '''

    segments = path.split('.')
    package, definition_names = segments[0], segments[1:]

    current: Definition = getattr(nexus, package)
    for name in definition_names:
        for content in current.m_contents():
            if getattr(content, 'name', None) == name:
                current = cast(Definition, content)
                break

        else:
            current = getattr(current, name, None)

        if current is None:
            assert False, f'{path} does not exist'

    if value == '*':
        assert current is not None, f'{path} does not exist'
    elif value is None:
        assert current is None, f'{path} does exist'
    else:
        assert current == value, f'{path} has wrong value'

    if isinstance(current, Section):
        assert current.nx_kind is not None
        for base_section in current.all_base_sections:
            assert base_section.nx_kind == current.nx_kind


def test_use_nexus_metainfo():
    '''
    Test on use of Nexus metainfo
    '''

    # pylint: disable=no-member
    archive = EntryArchive()
    archive.nexus = nexus.NeXus()
    archive.nexus.NXarpes = nexus.NXarpes()
    archive.nexus.NXarpes.m_create(nexus.NXarpes.NXentry)
    archive.nexus.NXarpes.ENTRY[0].title = 'my_title'

    archive = EntryArchive.m_from_dict(archive.m_to_dict())

    assert archive.nexus.NXarpes.ENTRY[0].title == 'my_title'


def test_get_nexus_classes_units_attributes():
    '''
        Check the correct parsing of a separate list for:
            Nexus classes (base_classes)
            Nexus units (memberTypes)
            Nexus attribute type (primitiveTypes)
        The tested functions can be found in nexus.py file
    '''

    # Test 1
    nexus_classes_list = tools.nexus.get_nx_classes()

    assert 'NXbeam' in nexus_classes_list

    # Test 2
    nexus_units_list = tools.nexus.get_nx_units()
    assert 'NX_TEMPERATURE' in nexus_units_list

    # Test 3
    nexus_attribute_list = tools.nexus.get_nx_attribute_type()
    assert 'NX_FLOAT' in nexus_attribute_list
