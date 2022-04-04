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

import sys
import xml.etree.ElementTree as ET
import textwrap

from pyaml import yaml

from nexusparser.tools import nexus


NX_CLSS = nexus.get_nx_classes()
NX_NEW_DEFINED_CLASSES = ['NX_COMPLEX']
NX_TYPE_KEYS = nexus.get_nx_attribute_type()
NX_ATTR_IDNT = '\\@'
NX_UNIT_IDNT = 'unit'
NX_UNIT_TYPS = nexus.get_nx_units()


def yml_reader(inputfile):
    """
    Yaml module based reading of .yml file
    """
    with open(inputfile, 'r') as stream:
        parsed_yaml = yaml.safe_load(stream)
        return parsed_yaml


def nx_name_type_resolving(tmp):
    """
    extracts the eventually custom name {optional_string}
    and type {nexus_type} from a YML section string.
    YML section string syntax: optional_string(nexus_type)
    """
    if tmp.count('(') == 1 and tmp.count(')') == 1:
        # we can safely assume that every valid YML key resolves
        # either an nx_ (type, base, candidate) class contains only 1 '(' and ')'
        index_start = tmp.index('(')
        index_end = tmp.index(')', index_start + 1)
        typ = tmp[index_start + 1:index_end]
        nam = tmp.replace('(' + typ + ')', '')
        return nam, typ
    # or a name for a member
    typ = ''
    nam = tmp
    return nam, typ


def xml_handle_doc(obj, value: str):
    """This function creates a 'doc' element instance, and appends it to an existing element

    """
    doctag = ET.SubElement(obj, 'doc')
    doctag.text = '\n' + textwrap.fill(value, width=70) + '\n'


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
    assert 'dim' in value.keys(), 'xml_handle_dimensions \
rank and/or dim not keys in value dict!'
    dims = ET.SubElement(obj, 'dimensions')
    if 'rank' in value.keys():
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


def xml_handle_enumeration(obj, value, verbose):
    """This function creates an 'enumeration' element instance.

Two cases are handled:
1) the items are in a list
2) the items are dictionaries and may contain a nested doc

"""
    enum = ET.SubElement(obj, 'enumeration')
    assert len(value) >= 1, 'xml_handle_enumeration, value must not be an empty list!'
    if isinstance(value, list):
        for element in value:
            itm = ET.SubElement(enum, 'item')
            itm.set('value', str(element))
    if isinstance(value, dict) and value != {}:
        for element in value.keys():
            itm = ET.SubElement(enum, 'item')
            itm.set('value', str(element))
            recursive_build(itm, value[str(element)], verbose)


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
        doctag.text = '\n' + textwrap.fill(value['doc'], width=70) + '\n'
    for kkeyword, vvalue in value.items():
        if kkeyword != 'doc':
            assert vvalue is not None and isinstance(vvalue, str), 'Put a comment in doc string!'
            sym = ET.SubElement(syms, 'symbol')
            sym.set('name', kkeyword)
            sym_doc = ET.SubElement(sym, 'doc')
            sym_doc.text = '\n' + textwrap.fill(vvalue, width=70) + '\n'


def check_keyword_variable(verbose, keyword_name, keyword_type, value):
    """Check whether both keyword_name and keyword_type are empty, and complains if it is the case

"""
    if verbose:
        sys.stdout.write(f'{keyword_name}({keyword_type}): value type is {type(value)}\n')
    if keyword_name == '' and keyword_type == '':
        raise ValueError('Found an improper YML key !')


def helper_keyword_type(kkeyword_type):
    """This function is returning a value of keyword_type if it belong to NX_TYPE_KEYS

"""
    if kkeyword_type in NX_TYPE_KEYS:
        return kkeyword_type
    return None


def verbose_flag(verbose, keyword, value):
    """Verbose stdout printing for nested levels of yaml file, if verbose flag is active

"""
    if verbose:
        sys.stdout.write(f'  key:{keyword}; value type is {type(value)}\n')


def second_nested_level_handle(verbose, fld, value):
    """When a second dictionary is found inside a value, a new cycle of handlings is run

"""
    if isinstance(value, dict):
        for kkeyword, vvalue in iter(value.items()):
            verbose_flag(verbose, kkeyword, vvalue)
            if kkeyword[0:2] == NX_ATTR_IDNT:
                attr = ET.SubElement(fld, 'attribute')
                # attributes may also come with an nx_type specifier
                # which we need to decipher first
                kkeyword_name, kkeyword_type = \
                    nx_name_type_resolving(kkeyword[2:])
                attr.set('name', kkeyword_name)
                # typ = 'NX_CHAR'
                typ = helper_keyword_type(kkeyword_type) or 'NX_CHAR'
                attr.set('type', typ)
                if isinstance(vvalue, dict):
                    for kkkeyword, vvvalue in iter(vvalue.items()):
                        third_nested_level_handle(verbose, attr, kkeyword, kkkeyword, vvvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(fld, vvalue)
            elif kkeyword == NX_UNIT_IDNT:
                xml_handle_units(fld, vvalue)
            elif kkeyword == 'exists':
                xml_handle_exists(fld, vvalue)
            elif kkeyword == 'dimensions':
                xml_handle_dimensions(fld, vvalue)
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(fld, vvalue, verbose)
            elif kkeyword == 'link':
                fld.set('link', '')
            else:
                raise ValueError(kkeyword, ' faced unknown situation !')


def third_nested_level_handle(verbose, attr, kkeyword, kkkeyword, vvvalue):
    """When a third dictionary is found inside a value, a new cycle of handlings is run

"""
    verbose_flag(verbose, kkkeyword, vvvalue)
    if kkkeyword == 'doc':
        xml_handle_doc(attr, vvvalue)
    elif kkkeyword == 'exists':
        xml_handle_exists(attr, vvvalue)
    elif kkkeyword == 'enumeration':
        xml_handle_enumeration(attr, vvvalue, verbose)
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
            verbose_flag(verbose, kkeyword, vvalue)
            if kkeyword == 'name':
                attr.set('name', vvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(attr, vvalue)
            elif kkeyword == 'type':
                attr.set('type', vvalue.upper())
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(attr, vvalue, verbose)
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
        elif keyword == NX_UNIT_IDNT:
            xml_handle_units(fld, value)
        elif keyword[0:2] == NX_ATTR_IDNT:  # attribute of a field
            raise ValueError(keyword, ' unknown attribute \
    of a field case coming from no dict !')
        elif keyword == 'exists':
            xml_handle_exists(fld, value)
        elif keyword == 'dimensions':
            raise ValueError(keyword, ' unknown dimensions \
    of a field case coming from no dict !')
        else:
            pass


def not_empty_keyword_name_handle(obj, keyword_type, keyword_name):
    """Handle a field in yaml file.
When a keyword is NOT:
symbol,
NX baseclass member,
attribute (\\@),
doc,
enumerations,
dimension,
exists,
then the not empty keyword_name is a field!
This simple function will define a new node of xml tree

"""
    typ = 'NX_CHAR'
    if keyword_type in NX_TYPE_KEYS + NX_NEW_DEFINED_CLASSES:
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
        keyword_name, keyword_type = nx_name_type_resolving(keyword)
        check_keyword_variable(verbose, keyword_name, keyword_type, value)
        if verbose:
            sys.stdout.write(f'keyword_name:{keyword_name} keyword_type {keyword_type}\n')
        if keyword[-6:] == '(link)':
            xml_handle_link(obj, keyword, value)

        elif keyword_type == '' and keyword_name == 'symbols':
            # print(value.key(), type(value.key()), value.value(), type(value.value()))
            xml_handle_symbols(obj, value)

        elif (keyword_type in NX_CLSS) or \
             (keyword_type not in NX_TYPE_KEYS + [''] + NX_NEW_DEFINED_CLASSES):
            # we can be sure we need to instantiate a new group
            xml_handle_group(verbose, obj, value, keyword_name, keyword_type)

        elif keyword_name[0:2] == NX_ATTR_IDNT:  # check if obj qualifies
            attribute_attributes_handle(verbose, obj, value, keyword_name)
        elif keyword == 'doc':
            xml_handle_doc(obj, value)

        elif keyword == 'enumeration':
            xml_handle_enumeration(obj, value, verbose)

        elif keyword == 'dimensions':
            xml_handle_dimensions(obj, value)

        elif keyword == 'exists':
            xml_handle_exists(obj, value)

        elif keyword_name != '':
            fld = not_empty_keyword_name_handle(obj, keyword_type, keyword_name)
            second_nested_level_handle(verbose, fld, value)
            second_level_attributes_handle(fld, keyword, value)
        else:
            pass
