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


'''This tool is reading the xml file'''

import re
import os
import os.path
import sys
from typing import Dict, Union, Optional
import xml.etree.ElementTree as ET

import numpy as np

from nomad.utils import strip
from nomad.metainfo import Section, Package, SubSection, Definition, Datetime, Bytes, MEnum, Quantity, Property, \
    Attribute
from nomad.datamodel import EntryArchive
from nexusparser.tools import nexus

# URL_REGEXP from
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
URL_REGEXP = re.compile(
    r'(https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*))')
XML_NAMESPACES = {'nx': 'http://definition.nexusformat.org/nxdl/3.1'}

# TO DO the validation still show some problems. Most notably there are a few higher
# dimensional fields with non number types, which the metainfo does not support

_current_package: Package = None  # type: ignore
_definition_sections: Dict[str, Section] = dict()

VALIDATE = False

_XML_PARENT_MAP: Dict[ET.Element, ET.Element] = None  # type: ignore
_NX_DOC_BASE = 'https://manual.nexusformat.org/classes'
_NX_TYPES = {  # Primitive Types,  'ISO8601' is the only type not defined here
    'NX_COMPLEX': np.dtype(np.float64),
    'NX_FLOAT': np.dtype(np.float64),
    'NX_CHAR': str,
    'NX_BOOLEAN': bool,
    'NX_INT': np.dtype(np.int64),
    'NX_UINT': np.dtype(np.uint64),
    'NX_NUMBER': np.dtype(np.number),
    'NX_POSINT': np.dtype(np.uint64),
    'NX_BINARY': Bytes,
    'NX_DATE_TIME': Datetime
}


class NXUnitSet:
    # maps from `NX_` token to dimensionality
    # None -> disable dimensionality check
    # '1' -> dimensionless quantities
    # 'transformation' -> Specially handled in metainfo
    mapping: dict = {
        'NX_ANGLE': '[angle]',
        'NX_ANY': None,
        'NX_AREA': '[area]',
        'NX_CHARGE': '[charge]',
        'NX_COUNT': '1',
        'NX_CROSS_SECTION': '[area]',
        'NX_CURRENT': '[current]',
        'NX_DIMENSIONLESS': '1',
        'NX_EMITTANCE': '[length] * [angle]',
        'NX_ENERGY': '[energy]',
        'NX_FLUX': '1 / [time] / [area]',
        'NX_FREQUENCY': '[frequency]',
        'NX_LENGTH': '[length]',
        'NX_MASS': '[mass]',
        'NX_MASS_DENSITY': '[mass] / [volume]',
        'NX_MOLECULAR_WEIGHT': '[mass] / [substance]',
        'NX_PERIOD': '[time]',
        'NX_PER_AREA': '1 / [area]',
        'NX_PER_LENGTH': '1 / [length]',
        'NX_POWER': '[power]',
        'NX_PRESSURE': '[pressure]',
        'NX_PULSES': '1',
        'NX_SCATTERING_LENGTH_DENSITY': '1 / [area]',
        'NX_SOLID_ANGLE': '[angle] * [angle]',
        'NX_TEMPERATURE': '[temperature]',
        'NX_TIME': '[time]',
        'NX_TIME_OF_FLIGHT': '[time]',
        'NX_TRANSFORMATION': 'transformation',
        'NX_UNITLESS': '1',
        'NX_VOLTAGE': '[energy] / [current] / [time]',
        'NX_VOLUME': '[volume]',
        'NX_WAVELENGTH': '[length]',
        'NX_WAVENUMBER': '1 / [length]'
    }

    @staticmethod
    def normalise(value: str) -> str:
        '''
        Normalise the given token
        '''
        value = value.upper()
        if not value.startswith('NX_'):
            value = 'NX_' + value
        return value

    @staticmethod
    def is_nx_token(value: str) -> bool:
        '''
        Check if a given token is one of NX tokens
        '''
        return NXUnitSet.normalise(value) in NXUnitSet.mapping.keys()


def __to_camel_case(snake_str: str, upper: bool = False) -> str:
    '''
    Take as input a snake case variable and return a camel case one
    '''
    components = snake_str.split('_')

    if upper:
        return ''.join(x.capitalize() for x in components)

    return components[0] + ''.join(x.capitalize() for x in components[1:])


def __if_base(xml_node: ET.Element) -> bool:
    '''
    retrieves the category from the root element
    '''
    elem = xml_node
    while True:
        parent = _XML_PARENT_MAP.get(elem)
        if parent is None:
            break
        elem = parent

    return elem.attrib['category'] == 'base'


def __if_repeats(name: str, max_occurs: str) -> bool:
    repeats = any(char.isupper() for char in name) or max_occurs == 'unbounded'

    if max_occurs.isdigit():
        repeats = repeats or int(max_occurs) > 1

    return repeats


def __if_template(name: Optional[str]) -> bool:
    return name is None or name.lower() != name


def __get_documentation_url(xml_node: ET.Element, nx_type: Optional[str]) -> Optional[str]:
    '''
    Get documentation url
    '''
    if nx_type is None:
        return None

    anchor_segments = []
    if nx_type != 'class':
        anchor_segments.append(nx_type)

    while True:
        segment = xml_node.get('name', xml_node.get('type'))
        anchor_segments.append(segment.replace('NX', '').replace('_', '-'))

        xml_parent = xml_node
        xml_node = _XML_PARENT_MAP.get(xml_node)
        if xml_node is None:
            break

    nx_package = xml_parent.get('nxdl_base').split('/')[-1]
    anchor = "-".join([name.lower() for name in reversed(anchor_segments)])
    return f'{_NX_DOC_BASE}/{nx_package}/{anchor_segments[-1]}.html#{anchor}'


def __go_to_section(name: str, **kwargs) -> Section:
    '''
    Returns the 'existing' metainfo section for a given top-level nexus base-class name.

    This function ensures that sections for these base-classes are only created one.
    This allows to access the metainfo section even before it is generated from the base-class
    nexus definition.
    '''
    if name in _definition_sections:
        section = _definition_sections[name]
        section.more.update(**kwargs)
        return section

    section = Section(validate=VALIDATE, name=name, **kwargs)

    _current_package.section_definitions.append(section)
    _definition_sections[section.name] = section

    return section


def __get_enumeration(xml_node: ET.Element) -> Optional[MEnum]:
    '''
    Get the enumeration field from xml node
    '''

    enumeration = xml_node.find('nx:enumeration', XML_NAMESPACES)
    if enumeration is None:
        return None

    enum_values: list = []
    for enum_value in enumeration.findall('nx:item', XML_NAMESPACES):
        enum_values.append(enum_value.attrib['value'])
    return MEnum(*enum_values)


def __add_common_properties(xml_node: ET.Element, definition: Definition):
    '''
    Adds general metainfo definition properties (e.g., deprecated, docs, optional, ...)
    from the given nexus XML node to the given metainfo definition.
    '''
    xml_attrs = xml_node.attrib

    # Read properties from potential base section. Those are not inherited, but we
    # duplicate them for a nicer presentation
    if isinstance(definition, Section) and definition.base_sections:
        if definition.base_sections[0].description:
            definition.description = definition.base_sections[0].description
        if definition.base_sections[0].deprecated:
            definition.deprecated = definition.base_sections[0].deprecated
        if definition.base_sections[0].more:
            definition.more.update(**definition.base_sections[0].more)

    links = []
    doc_url = __get_documentation_url(xml_node, definition.more.get('nx_kind'))
    if doc_url:
        links.append(doc_url)

    doc = xml_node.find('nx:doc', XML_NAMESPACES)
    if doc is not None and doc.text is not None:
        definition.description = strip(doc.text)
        links.extend([match[0] for match in URL_REGEXP.findall(definition.description)])

    if links:
        definition.links = links

    for k, v in xml_attrs.items():
        if 'deprecated' == k:
            definition.deprecated = v
            continue
        definition.more['nx_' + k] = v

    if 'optional' not in xml_attrs:
        definition.more['nx_optional'] = __if_base(xml_node)


def __create_attributes(xml_node: ET.Element, definition: Union[SubSection, Property]):
    '''
    Add all attributes in the given nexus XML node to the given
    Quantity or SubSection using the Attribute class (new mechanism).

    todo: account for more attributes of attribute, e.g., default, minOccurs
    '''
    for attribute in xml_node.findall('nx:attribute', XML_NAMESPACES):
        name = attribute.get('name')
        nx_type = attribute.attrib.get('type', 'NX_CHAR')
        repeats = __if_repeats(name, attribute.attrib.get('maxOccurs', '0'))
        definition.attributes.append(Attribute(
            name=name,
            variable=__if_template(name),
            shape=['0..*'] if repeats else [],
            type=_NX_TYPES[nx_type]))


def __create_field(xml_node: ET.Element, container: Section) -> Quantity:
    '''
    Creates a metainfo quantity from the nexus field given as xml node.
    '''
    xml_attrs = xml_node.attrib

    # name
    assert 'name' in xml_attrs, 'Expecting name to be present'
    name = xml_attrs['name']

    # type
    nx_type = xml_attrs.get('type', 'NX_CHAR')
    if nx_type not in _NX_TYPES:
        raise NotImplementedError(f'type {nx_type} is not supported for {name}')
    metainfo_type = _NX_TYPES[nx_type]

    # enumeration
    enum_type = __get_enumeration(xml_node)

    # dimensionality
    nx_dimensionality = xml_attrs.get('units', None)
    dimensionality = NXUnitSet.mapping[nx_dimensionality] if nx_dimensionality else None

    # shape
    shape: list = []
    dimensions = xml_node.find('nx:dimensions', XML_NAMESPACES)
    if dimensions is not None:
        for dimension in dimensions.findall('nx:dim', XML_NAMESPACES):
            dimension_value: str = dimension.attrib.get('value', '*')
            if dimension_value.isdigit():
                dimension_value: int = int(dimension_value)

            shape.append(dimension_value)

    value_quantity: Quantity = None  # type: ignore

    if container.base_sections is not None:
        base_quantity: Quantity = container.base_sections[0].all_quantities.get(name)
        if base_quantity:
            value_quantity = base_quantity.m_copy(deep=True)

    if value_quantity is None:
        # create quantity
        value_quantity = Quantity(name=name)

    value_quantity.variable = __if_template(name)
    value_quantity.type = enum_type if enum_type else metainfo_type
    value_quantity.dimensionality = dimensionality
    value_quantity.shape = shape
    value_quantity.more.update(dict(nx_kind='field', nx_type=nx_type))

    __add_common_properties(xml_node, value_quantity)
    __create_attributes(xml_node, value_quantity)

    container.quantities.append(value_quantity)

    return value_quantity


def __create_group(xml_node: ET.Element, section: Section):
    '''
    Adds all properties that can be generated from the given nexus group XML node to
    the given (empty) metainfo section definition.
    '''
    for group in xml_node.findall('nx:group', XML_NAMESPACES):
        xml_attrs = group.attrib

        assert 'type' in xml_attrs, 'Expecting type to be present'
        typ = xml_attrs['type']
        name = xml_attrs.get('name', typ)

        group_section = Section(validate=VALIDATE, nx_kind='group', name=name)
        __attach_base_section(group_section, section, __go_to_section(typ))

        __add_common_properties(group, group_section)

        __create_group(group, group_section)

        section.inner_section_definitions.append(group_section)

        name = xml_attrs.get('name', typ.replace('NX', '').upper())
        group_subsection = SubSection(
            section_def=group_section,
            nx_kind='group',
            name=name,
            repeats=__if_repeats(name, xml_attrs.get('maxOccurs', '0')),
            variable=__if_template(name))

        __create_attributes(group, group_subsection)

        section.sub_sections.append(group_subsection)

    for field in xml_node.findall('nx:field', XML_NAMESPACES):
        __create_field(field, section)


def __attach_base_section(section: Section, container: Section, default_base_section: Section = None):
    '''
    Potentially adds a base section to the given section, if the given container has
    a base-section with a suitable base.
    '''
    base_section = container.all_inner_section_definitions.get(section.name)
    if base_section:
        assert base_section.nx_kind == section.nx_kind, 'base section has wrong nexus kind'
    else:
        base_section = default_base_section

    if base_section:
        section.base_sections = [base_section]


def __create_class_section(xml_node: ET.Element) -> Section:
    '''
    Creates a metainfo section from the top-level nexus definition given as xml node.
    '''
    xml_attrs = xml_node.attrib
    assert 'name' in xml_attrs, 'Expecting name to be present'
    assert 'type' in xml_attrs, 'Expecting type to be present'
    assert 'category' in xml_attrs, 'Expecting category to be present'

    class_section = __go_to_section(
        xml_attrs['name'], nx_kind=xml_attrs['type'], nx_category=xml_attrs['category'])

    if 'extends' in xml_attrs:
        base_section = __go_to_section(xml_attrs['extends'])
        class_section.base_sections = [base_section]

    __add_common_properties(xml_node, class_section)
    __create_group(xml_node, class_section)

    return class_section


def __sort_nxdl_files(paths):
    '''
    Sort all definitions based on dependencies
    '''

    def compare_dependencies(nxdl1, nxdl2):
        if 'extends' in nxdl1.attrib and nxdl1.attrib['extends'] == nxdl2.attrib['name']:
            return True
        for group1 in nxdl1.iter("*"):
            if group1.tag[group1.tag.rindex("}") + 1:] == 'group' and \
                    group1.attrib['type'] == nxdl2.attrib['name']:
                break
        else:
            return False
        for group2 in nxdl2.iter("*"):
            if group2.tag[group2.tag.rindex("}") + 1:] == 'group' and \
                    group2.attrib['type'] == nxdl1.attrib['name']:
                return False
        return True

    list_of_nxdl = []
    for path in paths:
        for nxdl_file in sorted(os.listdir(path)):
            if not nxdl_file.endswith('.nxdl.xml'):
                continue
            xml_tree = ET.parse(os.path.join(path, nxdl_file))
            xml_node = xml_tree.getroot()
            xml_node.set('nxdl_base', path)
            assert xml_node.attrib.get('type') == 'group', 'definition is not a group'
            list_of_nxdl.append(xml_node)
    sorted_index = 0
    while sorted_index < len(list_of_nxdl):
        current_index = sorted_index + 1
        while current_index < len(list_of_nxdl):
            if compare_dependencies(list_of_nxdl[sorted_index], list_of_nxdl[current_index]):
                list_of_nxdl.append(list_of_nxdl[sorted_index])
                list_of_nxdl.__delitem__(sorted_index)
                break
            current_index = current_index + 1
        if current_index == len(list_of_nxdl):
            sorted_index = sorted_index + 1
    # print('\n'.join([nxdl.attrib['name'] for nxdl in list_of_nxdl]))
    return list_of_nxdl


def __add_section_from_nxdl(xml_node):
    '''
    Creates a metainfo section from a nxdl file.
    '''
    try:
        global _XML_PARENT_MAP  # pylint: disable=global-statement
        _XML_PARENT_MAP = {child: parent for parent in xml_node.iter() for child in parent}

        # The section gets already implicitly added to _current_package by get_or_create_section
        __create_class_section(xml_node)

    except NotImplementedError as err:
        print('Exception while mapping ' + xml_node.attrib["name"] + ':', err, file=sys.stderr)


def __create_package_from_nxdl_directories(paths) -> Package:
    '''
    Creates a metainfo package from the given nexus directory. Will generate the respective
    metainfo definitions from all the nxdl files in that directory.
    '''
    global _current_package  # pylint: disable=global-statement
    _current_package = Package(name=f'nexus')

    for nxdl_file in __sort_nxdl_files(paths):
        __add_section_from_nxdl(nxdl_file)

    return _current_package


nexus_metainfo_package: Package = None  # type: ignore


def init_nexus_metainfo():
    global nexus_metainfo_package

    if nexus_metainfo_package is not None:
        return

    # separated metainfo package for the nexus base classes, application defs and contributed classes.
    directories = [os.path.join(
        nexus.get_nexus_definitions_path(), v) for v in ('base_classes', 'contributed_definitions', 'applications')]

    nexus_metainfo_package = __create_package_from_nxdl_directories(directories)

    # We take the application definitions and create a common parent section that allows to
    # include nexus in an EntryArchive.
    nexus_section = Section(validate=VALIDATE, name='Nexus')

    for application_section in nexus_metainfo_package.section_definitions:  # pylint: disable=not-an-iterable
        if application_section.more.get('nx_category') == 'application':
            sub_section = SubSection(
                section_def=application_section,
                name=application_section.name.replace('NX', ''))
            nexus_section.sub_sections.append(sub_section)

    EntryArchive.nexus = SubSection(name='nexus', section_def=nexus_section)
    EntryArchive.nexus.init_metainfo()
    EntryArchive.m_def.sub_sections.append(EntryArchive.nexus)

    nexus_metainfo_package.section_definitions.append(nexus_section)

    # We need to initialize the metainfo definitions. This is usually done automatically,
    # when the metainfo schema is defined though MSection Python classes.
    nexus_metainfo_package.init_metainfo()

    # We skip the Python code generation for now and offer Python classes as variables
    # TO DO not necessary right now, could also be done case-by-case by the nexus parser
    python_module = sys.modules[__name__]
    for section in nexus_metainfo_package.section_definitions:  # pylint: disable=not-an-iterable
        setattr(python_module, section.name, section.section_cls)


init_nexus_metainfo()
