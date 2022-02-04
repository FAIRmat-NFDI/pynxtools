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

from nomad.metainfo import Definition, MSection, Section
from nomad.datamodel import EntryArchive
from nexusparser.metainfo import nexus
from nexusparser import tools


@pytest.mark.parametrize('path,value', [
    pytest.param('BASE_CLASSES.name', 'nexus_base_classes'),
    pytest.param('BASE_CLASSES.NXobject.name', 'NXobject'),
    pytest.param('BASE_CLASSES.NXentry.nx_kind', 'group'),
    pytest.param('BASE_CLASSES.NXentry.defaultAttribute.nx_value.type', str),
    pytest.param('BASE_CLASSES.NXentry.nx_attribute_default', '*'),
    pytest.param('BASE_CLASSES.NXentry.NXdataGroup', '*'),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField', '*'),
    pytest.param('BASE_CLASSES.NXentry.NXdataGroup.nx_optional', True),
    pytest.param('BASE_CLASSES.NXentry.nx_group_DATA.section_def.nx_kind', 'group'),
    pytest.param('BASE_CLASSES.NXentry.nx_group_DATA.section_def.nx_optional', True),
    pytest.param('BASE_CLASSES.NXentry.nx_group_DATA.section_def.nx_name.type', str),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField.name', 'real_timeField'),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField.nx_type', 'NX_NUMBER'),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField.nx_units', 'NX_TIME'),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField.nx_unit', '*'),
    pytest.param('BASE_CLASSES.NXdetector.real_timeField.nx_value', '*'),
    pytest.param('APPLICATIONS.NXarpes.NXentryGroup.NXdataGroup.nx_optional', False)
])
def test_assert_nexus_metainfo(path: str, value: Any):
    """Test the existance of nexus metainfo

"""
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
    """Test on use of Nexus metainfo

"""
    # pylint: disable=no-member
    archive = EntryArchive()
    archive.nexus = nexus.Nexus()
    archive.nexus.nx_application_arpes = nexus.NXarpes()
    archive.nexus.nx_application_arpes.m_create(nexus.NXarpes.NXentryGroup)
    archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_field_title = \
        nexus.NXarpes.NXentryGroup.titleField()
    archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_field_title.nx_value = 'my title'

    # Entry/default is not overwritten in NXarpes. Therefore technically,
    # there is no attribute section
    # nexus.NXarpes.NXentryGroup.DefaultAttribute. We artifically extented inheritence to
    # include inner section/classes. So both options work:
    # archive.nexus.nx_application_arpes.nx_group_ENTRY.nx_attribute_default =
    # nexus.NXentry.DefaultAttribute()
    archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_attribute_default = \
        nexus.NXarpes.NXentryGroup.defaultAttribute()
    archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_attribute_default.nx_value = \
        'my default'
    # pylint: enable=no-member

    archive = EntryArchive.m_from_dict(archive.m_to_dict())
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_attribute_default.nx_value == \
        'my default'
    assert archive.nexus.nx_application_arpes.nx_group_ENTRY[0].nx_field_title.nx_value == \
        'my title'


@pytest.mark.parametrize('path', [
    pytest.param('NXarpes:app/NXentry:group/title:field/my title:value', id='field'),
    pytest.param('NXarpes:app/NXentry:group/default:attribute/my default:value', id='attribute')
])
def test_use_nexus_metainfo_reflectivly(path):
    """Test of the use of nexus metainfo reflectivly

"""
    archive = EntryArchive()
    archive.nexus = nexus.Nexus()  # pylint: disable=no-member
    parent_object: MSection = archive.nexus
    parent_definition: Section = nexus.Nexus.m_def  # pylint: disable=no-member

    segments = path.split('/')
    for segment in segments:
        name_or_value, kind = segment.split(':')
        if kind in ['app', 'group', 'field', 'attribute']:
            if kind == 'app':
                section_definition = nexus.APPLICATIONS.all_definitions[name_or_value]
                sub_section_definition = \
                    parent_definition.all_sub_sections[name_or_value.replace('NX', '\
nx_application_')]

            if kind == 'group':
                section_definition = \
                    parent_definition.all_inner_section_definitions[f'{name_or_value}Group']
                sub_section_definition = \
                    parent_definition.all_sub_sections[f'nx_group_'
                                                       f'{name_or_value.replace("NX", "").upper()}'
                                                       ]

            if kind == 'field':
                section_definition = \
                    parent_definition.all_inner_section_definitions[f'{name_or_value}Field']
                sub_section_definition = \
                    parent_definition.all_sub_sections[f'nx_field_{name_or_value}']

            if kind == 'attribute':
                section_definition = \
                    parent_definition.all_inner_section_definitions[f'{name_or_value}Attribute']
                sub_section_definition = \
                    parent_definition.all_sub_sections[f'nx_attribute_{name_or_value}']

            new_object = section_definition.section_cls()
            parent_object.m_add_sub_section(sub_section_definition, new_object)

        elif kind == 'value':
            parent_object.m_set(parent_definition.all_quantities['nx_value'], name_or_value)

        else:
            assert False, 'kind does not exist'

        parent_object = new_object
        parent_definition = section_definition


def test_get_nexus_classes_units_attributes():
    """Check the correct parsing of a separate list for:
Nexus classes (base_classes)
Nexus units (memberTypes)
Nexus attribute type (primitiveTypes)
the tested functions can be found in nexus.py file
"""

    # Test 1
    nexus_classes_list = tools.nexus.get_nx_classes()

    assert 'NXbeam' in nexus_classes_list

    # Test 2
    nexus_units_list = tools.nexus.get_nx_units()
    assert 'NX_TEMPERATURE' in nexus_units_list

    # Test 3
    nexus_attribute_list = tools.nexus.get_nx_attribute_type()
    assert 'NX_FLOAT' in nexus_attribute_list
