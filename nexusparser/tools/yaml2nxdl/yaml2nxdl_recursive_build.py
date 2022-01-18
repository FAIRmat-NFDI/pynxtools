#!/usr/bin/env python3
"""Creates an instantiated NXDL schema XML tree by walking the dictionary nest

"""
# -*- coding: utf-8 -*-
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
from nexusparser.tools.yaml2nxdl import yaml2nxdl_utils


def xml_handle_doc(obj, value: str):
    """This function creates a 'doc' element instance, and appends it to an existing element

    """
    doctag = ET.SubElement(obj, 'doc')
    doctag.text = value


def xml_handle_units(obj, value):
    """This function creates a 'units' element instance, and appends it to an existing element

    """
    obj.set('units', value)


def xml_handle_exists(obj, value):
    """This function creates an 'exists' element instance, and appends it to an existing element

    """
    assert value is not None, 'xml_handle_exists, value must not be None!'
    if isinstance(value, list):
        if len(value) == 2 and value[0] == 'min':
            obj.set('minOccurs', str(value[1]))
        elif len(value) == 2 and value[0] == 'max':
            obj.set('maxOccurs', str(value[1]))
        elif len(value) == 4 and value[0] == 'min' and value[2] == 'max':
            obj.set('minOccurs', str(value[1]))
            if str(value[3]) != 'infty':
                obj.set('maxOccurs', str(value[3]))
            else:
                obj.set('maxOccurs', 'unbounded')
        elif len(value) == 4 and (value[0] != 'min' or value[2] != 'max'):
            raise ValueError('exists keyword needs to go either with an optional \
[recommended] list with two entries either [min, <uint>] or \
[max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
        else:
            raise ValueError('exists keyword needs to go either with optional, \
recommended, a list with two entries either [min, <uint>] or \
[max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
    else:
        if value == 'optional':
            obj.set('optional', 'true')
        elif value == 'recommended':
            obj.set('recommended', 'true')
        elif value == 'required':
            obj.set('minOccurs', '1')
        else:
            obj.set('minOccurs', '0')


def xml_handle_group(verbose, obj, value, keyword_name, keyword_type):
    """The function deals with group instances

"""
    grp = ET.SubElement(obj, 'group')
    if keyword_name != '':  # use the custom name for the group
        grp.set('name', keyword_name)
    grp.set('type', keyword_type)
    if isinstance(value, dict) and value != {}:
        recursive_build(grp, value, verbose)


def xml_handle_dimensions(obj, value: dict):
    """This function creates a 'dimensions' element instance, and appends it to an existing element

    """
    assert 'rank' in value.keys() and 'dim' in value.keys(), 'xml_handle_dimensions \
rank and/or dim not keys in value dict!'
    dims = ET.SubElement(obj, 'dimensions')
    dims.set('rank', str(value['rank']))
    for element in value['dim']:
        assert isinstance(element, list), 'xml_handle_dimensions, element is not a list!'
        assert len(element) >= 2, 'xml_handle_dimensions, list element has less than two entries!'
        dim = ET.SubElement(dims, 'dim')
        dim.set('index', str(element[0]))
        dim.set('value', str(element[1]))
        if len(element) == 3:
            assert element[2] == 'optional', 'xml_handle_dimensions element is \
a list with unexpected number of entries!'
            dim.set('required', 'false')


def xml_handle_enumeration(obj, value: list):
    """This function creates an 'enumeration' element instance,
and appends it to an existing element

    """
    enum = ET.SubElement(obj, 'enumeration')
    assert len(value) >= 1, 'xml_handle_enumeration, value must not be an empty list!'
    for element in value:
        itm = ET.SubElement(enum, 'item')
        itm.set('value', str(element))


def xml_handle_link(obj, keyword, value):
    """If we have an NXDL link we decode the name attribute from <optional string>(link)[:-6]

    """
    if len(keyword[:-6]) >= 1 and isinstance(value, dict) and 'target' in value.keys():
        if isinstance(value['target'], str) and len(value['target']) >= 1:
            lnk = ET.SubElement(obj, 'link')
            lnk.set('name', keyword[:-6])
            lnk.set('target', value['target'])
        else:
            raise ValueError(keyword + ' value for target member of a link is invalid !')
    else:
        raise ValueError(keyword + ' the formatting of what seems to be a link \
is invalid in the yml file !')


def xml_handle_symbols(obj, value: dict):
    """Handle a set of NXDL symbols as a child to obj

    """
    assert len(list(value.keys())) >= 1, 'xml_handle_symbols, symbols tables must not be empty!'
    syms = ET.SubElement(obj, 'symbols')
    if 'doc' in value.keys():
        doctag = ET.SubElement(syms, 'doc')
        doctag.text = value['doc']
    for kkeyword, vvalue in value.items():
        if kkeyword != 'doc':
            assert vvalue is not None and isinstance(vvalue, str), 'Put a comment in doc string!'
            sym = ET.SubElement(syms, 'symbol')
            sym.set('name', kkeyword)
            sym.set('doc', vvalue)


def check_keyword_variable(verbose, keyword_name, keyword_type, value):
    """Check whether both keyword_name and keyword_type are empty, and complains if it is the case

"""
    if verbose:
        print('keyword_name:', keyword_name, 'keyword_type:', keyword_type)
        print('value:', '[' + str(type(value)) + ']')
    if keyword_name == '' and keyword_type == '':
        raise ValueError('Found an improper YML key !')


def second_nested_level_handle(verbose, fld, value):
    """When a second dictionary is found inside a value, a new cycle of handlings is run

"""
    if isinstance(value, dict):
        for kkeyword, vvalue in iter(value.items()):
            if verbose:
                print('  kkeyword:', kkeyword)
                print('  vvalue:', '[' + str(type(vvalue)) + ']')
            if kkeyword[0:2] == yaml2nxdl_utils.NX_ATTR_IDNT:
                attr = ET.SubElement(fld, 'attribute')
                # attributes may also come with an nx_type specifier
                # which we need to decipher first
                kkeyword_name, kkeyword_type = \
                    yaml2nxdl_utils.nx_name_type_resolving(kkeyword[2:])
                attr.set('name', kkeyword_name)
                typ = 'NX_CHAR'
                if kkeyword_type in yaml2nxdl_utils.NX_TYPE_KEYS:
                    typ = kkeyword_type
                attr.set('type', typ)
                if isinstance(vvalue, dict):
                    for kkkeyword, vvvalue in iter(vvalue.items()):
                        third_nested_level_handle(verbose, attr, kkeyword, kkkeyword, vvvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(fld, vvalue)
            elif kkeyword == yaml2nxdl_utils.NX_UNIT_IDNT:
                xml_handle_units(fld, vvalue)
            elif kkeyword == 'exists':
                xml_handle_exists(fld, vvalue)
            elif kkeyword == 'dimensions':
                xml_handle_dimensions(fld, vvalue)
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(fld, vvalue)
            elif kkeyword == 'link':
                fld.set('link', '')
            else:
                raise ValueError(kkeyword, ' faced unknown situation !')


def third_nested_level_handle(verbose, attr, kkeyword, kkkeyword, vvvalue):
    """When a third dictionary is found inside a value, a new cycle of handlings is run

"""
    if verbose:
        print('    kkkeyword:', kkkeyword)
        print('    vvvalue:', '[' + str(type(vvvalue)) + ']')
    if kkkeyword == 'doc':
        xml_handle_doc(attr, vvvalue)
    elif kkkeyword == 'exists':
        xml_handle_exists(attr, vvvalue)
    elif kkkeyword == 'enumeration':
        xml_handle_enumeration(attr, vvvalue)
    else:
        raise ValueError(
            kkeyword, kkkeyword, ' attribute handling !')


def attribute_attributes_handle(verbose, obj, value, keyword_name):
    """Handle the attributes found connected to attribute field"""
    # as an attribute identifier
    attr = ET.SubElement(obj, 'attribute')
    attr.set('name', keyword_name[2:])
    if value is not None:
        assert isinstance(value, dict), 'the keyword is an attribute, \
its value must be a dict!'
        for kkeyword, vvalue in iter(value.items()):
            if verbose:
                print('  kkeyword:', kkeyword)
                print('  vvalue:', '[' + str(type(vvalue)) + ']')
            if kkeyword == 'name':
                attr.set('name', vvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(attr, vvalue)
            elif kkeyword == 'type':
                attr.set('type', vvalue.upper())
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(attr, vvalue)
            elif kkeyword == 'exists':
                xml_handle_exists(attr, vvalue)
            else:
                raise ValueError(kkeyword + ' facing an unknown situation \
while processing attributes of an attribute ! Node tag:', obj.tag, 'Node content:', obj.attrib)
# handle special keywords (symbols),
# assumed that you do not encounter further symbols nested inside


def second_level_attributes_handle(fld, keyword, value):
    """If value is not a dictionary, this function handles the attributes of a nested field

"""
    if not isinstance(value, dict):
        if keyword == 'doc':
            xml_handle_doc(fld, value)
        elif keyword == yaml2nxdl_utils.NX_UNIT_IDNT:
            xml_handle_units(fld, value)
        elif keyword[0:2] == yaml2nxdl_utils.NX_ATTR_IDNT:  # attribute of a field
            raise ValueError(keyword, ' unknown attribute \
    of a field case coming from no dict !')
        elif keyword == 'exists':
            xml_handle_exists(fld, value)
        elif keyword == 'dimensions':
            raise ValueError(keyword, ' unknown dimensions \
    of a field case coming from no dict !')
        else:
            pass


def empty_keyword_name_handle(obj, keyword_type, keyword_name):
    """When an empty keyword_name is found, this simple function will define a new node of xml tree

"""
    typ = 'NX_CHAR'
    if keyword_type in yaml2nxdl_utils.NX_TYPE_KEYS:
        typ = keyword_type
    # assume type is NX_CHAR, a NeXus default assumption if in doubt
    fld = ET.SubElement(obj, 'field')
    fld.set('name', keyword_name)
    fld.set('type', typ)
    return fld


def recursive_build(obj, dct, verbose):
    """obj is the current node of the XML tree where we want to append to,
    dct is a dictionary object which represents the content of a child to obj
    dct may contain further dictionary nests, representing NXDL groups,
    which trigger recursive processing
    NXDL fields may contain attributes but trigger no recursion so attributes are leafs.

    """
    for keyword, value in iter(dct.items()):
        keyword_name, keyword_type = yaml2nxdl_utils.nx_name_type_resolving(keyword)

        check_keyword_variable(verbose, keyword_name, keyword_type, value)

        if keyword[-6:] == '(link)':
            xml_handle_link(obj, keyword, value)

        elif keyword_type == '' and keyword_name == 'symbols':
            # print(value.key(), type(value.key()), value.value(), type(value.value()))
            xml_handle_symbols(obj, value)

        elif (keyword_type in yaml2nxdl_utils.NX_CLSS) or \
             (keyword_type not in yaml2nxdl_utils.NX_TYPE_KEYS + ['']):
            # we can be sure we need to instantiate a new group
            xml_handle_group(verbose, obj, value, keyword_name, keyword_type)

        elif keyword_name[0:2] == yaml2nxdl_utils.NX_ATTR_IDNT:  # check if obj qualifies
            attribute_attributes_handle(verbose, obj, value, keyword_name)
        elif keyword == 'doc':
            xml_handle_doc(obj, value)

        elif keyword == 'enumeration':
            xml_handle_enumeration(obj, value)

        elif keyword == 'dimensions':
            xml_handle_dimensions(obj, value)

        elif keyword == 'exists':
            xml_handle_exists(obj, value)

        elif keyword_name != '':
            fld = empty_keyword_name_handle(obj, keyword_type, keyword_name)
            second_nested_level_handle(verbose, fld, value)
            second_level_attributes_handle(fld, keyword, value)
        else:
            pass
