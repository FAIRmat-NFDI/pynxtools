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

import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor

from yaml.nodes import ScalarNode
from yaml.resolver import BaseResolver
from yaml.loader import Loader

from nexusutils.nexus import nexus


NX_CLSS = nexus.get_nx_classes()
NX_NEW_DEFINED_CLASSES = ['NX_COMPLEX']
NX_TYPE_KEYS = nexus.get_nx_attribute_type()
NX_ATTR_IDNT = '\\@'
NX_UNIT_IDNT = 'unit'
NX_UNIT_TYPES = nexus.get_nx_units()


class LineLoader(Loader):  # pylint: disable=too-many-ancestors
    """
    LineLoader parses a yaml into a python dictionary extended with extra items.
    The new items have as keys __line__<yaml_keyword> and as values the yaml file line number
    """

    def compose_node(self, parent, index):
        # the line number where the previous token has ended (plus empty lines)
        node = Composer.compose_node(self, parent, index)
        node.__line__ = self.line + 1
        return node

    def construct_mapping(self, node, deep=False):
        node_pair_lst = node.value
        node_pair_lst_for_appending = []

        for key_node in node_pair_lst:
            shadow_key_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value='__line__' + key_node[0].value)
            shadow_value_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value=key_node[0].__line__)
            node_pair_lst_for_appending.append(
                (shadow_key_node, shadow_value_node))

        node.value = node_pair_lst + node_pair_lst_for_appending
        return Constructor.construct_mapping(self, node, deep=deep)


def yml_reader(inputfile):
    """
    This function launches the LineLoader class.
    It parses the yaml in a dict and extends it with line tag keys for each key of the dict.
    """

    with open(inputfile, "r", encoding="utf-8") as plain_text_yaml:
        loader = LineLoader(plain_text_yaml)
        return loader.get_single_data()


def yml_reader_nolinetag(inputfile):
    """
    pyyaml based parsing of yaml file in python dict
    """
    with open(inputfile, 'r', encoding="utf-8") as stream:
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


def format_nxdl_doc(string):
    """NeXus format for doc string
    """
    formatted_doc = ''
    formatted_doc += "\n"
    if "\n" not in string:
        if len(string) > 80:
            wrapped = textwrap.TextWrapper(width=80,
                                           break_long_words=False,
                                           replace_whitespace=False)
            string = '\n'.join(wrapped.wrap(string))
        formatted_doc += f"{string}"
    else:
        formatted_doc += f"{string}"
    if string.endswith("\n"):
        pass
    else:
        formatted_doc += "\n"
    return formatted_doc


def xml_handle_doc(obj, value: str):
    """This function creates a 'doc' element instance, and appends it to an existing element

    """
    doctag = ET.SubElement(obj, 'doc')
    doctag.text = format_nxdl_doc(value)


def xml_handle_units(obj, value):
    """This function creates a 'units' element instance, and appends it to an existing element

    """
    obj.set('units', value)


def xml_handle_exists(dct, obj, keyword, value):
    """This function creates an 'exists' element instance, and appends it to an existing element

    """

    line_number = f'__line__{keyword}'
    assert value is not None, f'Line {dct[line_number]}: exists argument must not be None !'
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
            raise ValueError(f'Line {dct[line_number]}: exists keyword'
                             f'needs to go either with an optional [recommended] list with two'
                             f'entries either [min, <uint>] or [max, <uint>], or a list of four'
                             f'entries [min, <uint>, max, <uint>] !')
        else:
            raise ValueError(f'Line {dct[line_number]}: exists keyword'
                             f'needs to go either with optional, recommended, a list with two'
                             f'entries either [min, <uint>] or [max, <uint>], or a list of four'
                             f'entries [min, <uint>, max, <uint>] !')
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


def xml_handle_dimensions(dct, obj, keyword, value: dict):
    """This function creates a 'dimensions' element instance, and appends it to an existing element

    """
    line_number = f'__line__{keyword}'
    assert 'dim' in value.keys(), f'Line {dct[line_number]}: dim is not a key in dimensions dict !'
    dims = ET.SubElement(obj, 'dimensions')
    if 'rank' in value.keys():
        dims.set('rank', str(value['rank']))
    for element in value['dim']:
        line_number = '__line__dim'
        assert isinstance(element, list), f'Line {value[line_number]}: dim argument not a list !'
        assert len(
            element) >= 2, f'Line {value[line_number]}: dim list has less than two entries !'
        dim = ET.SubElement(dims, 'dim')
        dim.set('index', str(element[0]))
        dim.set('value', str(element[1]))
        if len(element) == 3:
            assert element[2] == 'optional', f'Line {value[line_number]}: dim argument \
is a list with unexpected number of entries!'
            dim.set('required', 'false')


def xml_handle_enumeration(dct, obj, keyword, value, verbose):
    """This function creates an 'enumeration' element instance.

Two cases are handled:
1) the items are in a list
2) the items are dictionaries and may contain a nested doc

"""
    enum = ET.SubElement(obj, 'enumeration')
    line_number = f'__line__{keyword}'
    assert value is not None, f'Line {dct[line_number]}: enumeration must \
bear at least an argument !'
    assert len(
        value) >= 1, f'Line {dct[line_number]}: enumeration must not be an empty list!'
    if isinstance(value, list):
        for element in value:
            itm = ET.SubElement(enum, 'item')
            itm.set('value', str(element))
    if isinstance(value, dict) and value != {}:
        for element in value.keys():
            if '__line__' not in element:
                itm = ET.SubElement(enum, 'item')
                itm.set('value', str(element))
                recursive_build(itm, value[str(element)], verbose)


def xml_handle_link(dct, obj, keyword, value):
    """If we have an NXDL link we decode the name attribute from <optional string>(link)[:-6]

    """
    if '__line__' not in keyword:
        if len(keyword[:-6]) >= 1 and \
           isinstance(value, dict) and \
           'target' in value.keys():
            if isinstance(value['target'], str) and len(value['target']) >= 1:
                lnk = ET.SubElement(obj, 'link')
                lnk.set('name', keyword[:-6])
                lnk.set('target', value['target'])
            else:
                line_number = '__line__target'
                raise ValueError(
                    keyword + f'Line {value[line_number]}: target argument of link is invalid !')
        else:
            line_number = f'__line__{keyword}'
            raise ValueError(
                keyword + f'Line {dct[line_number]}: the link formatting is invalid !')
    else:
        pass


def xml_handle_symbols(dct, obj, keyword, value: dict):
    """Handle a set of NXDL symbols as a child to obj

    """
    line_number = f'__line__{keyword}'
    assert len(list(value.keys())
               ) >= 1, f'Line {dct[line_number]}: symbols table must not be empty !'
    syms = ET.SubElement(obj, 'symbols')
    if 'doc' in value.keys():
        doctag = ET.SubElement(syms, 'doc')
        doctag.text = '\n' + textwrap.fill(value['doc'], width=70) + '\n'
    for kkeyword, vvalue in value.items():
        if kkeyword != 'doc' and '__line__' not in kkeyword:
            line_number = f'__line__{kkeyword}'
            assert vvalue is not None and isinstance(
                vvalue, str), f'Line {value[line_number]}: put a comment in doc string !'
            sym = ET.SubElement(syms, 'symbol')
            sym.set('name', kkeyword)
            sym_doc = ET.SubElement(sym, 'doc')
            sym_doc.text = '\n' + textwrap.fill(vvalue, width=70) + '\n'


def check_keyword_variable(verbose, dct, keyword, value):
    """Check whether both keyword_name and keyword_type are empty, and complains if it is the case

"""
    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    if verbose:
        sys.stdout.write(
            f'{keyword_name}({keyword_type}): value type is {type(value)}\n')
    if keyword_name == '' and keyword_type == '':
        line_number = f'__line__{keyword}'
        raise ValueError(f'Line {dct[line_number]}: found an improper yaml key !')


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


def second_nested_level_handle(verbose, dct, fld):
    """When a second dictionary is found inside a value, a new cycle of handlings is run

"""
    if isinstance(dct, dict):
        for kkeyword, vvalue in iter(dct.items()):
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
                    third_nested_level_handle(verbose, attr, vvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(fld, vvalue)
            elif kkeyword == NX_UNIT_IDNT:
                xml_handle_units(fld, vvalue)
            elif kkeyword == 'exists':
                xml_handle_exists(dct, fld, kkeyword, vvalue)
            elif kkeyword == 'dimensions':
                xml_handle_dimensions(dct, fld, kkeyword, vvalue)
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(dct, fld, kkeyword, vvalue, verbose)
            elif kkeyword == 'link':
                fld.set('link', '')
            elif '__line__' in kkeyword:
                pass
            else:
                line_number = f'__line__{kkeyword}'
                raise ValueError(
                    kkeyword, f' Line {dct[line_number]}: faced unknown situation !')


def third_nested_level_handle(verbose, attr, vvalue_dct):
    """When a third dictionary is found inside a value, a new cycle of handlings is run

"""
    for kkkeyword, vvvalue in iter(vvalue_dct.items()):
        verbose_flag(verbose, kkkeyword, vvvalue)
        if kkkeyword == 'doc':
            xml_handle_doc(attr, vvvalue)
        elif kkkeyword == 'exists':
            xml_handle_exists(vvalue_dct, attr, kkkeyword, vvvalue)
        elif kkkeyword == 'enumeration':
            xml_handle_enumeration(vvalue_dct, attr, kkkeyword, vvvalue, verbose)
        elif '__line__' in kkkeyword:
            pass
        else:
            line_number = f'__line__{kkkeyword}'
            raise ValueError(
                kkkeyword, f' Line {vvalue_dct[line_number]}: attribute handling error !')


def attribute_attributes_handle(verbose, dct, obj, value, keyword):
    """Handle the attributes found connected to attribute field"""
    # as an attribute identifier
    keyword_name = nx_name_type_resolving(keyword)
    line_number = f'__line__{keyword}'
    attr = ET.SubElement(obj, 'attribute')
    attr.set('name', keyword_name[0][2:])
    if value is not None:
        assert isinstance(value, dict), f'Line {dct[line_number]}: the attribute must be a dict!'
        for kkeyword, vvalue in iter(value.items()):
            verbose_flag(verbose, kkeyword, vvalue)
            if kkeyword == 'name':
                attr.set('name', vvalue)
            elif kkeyword == 'doc':
                xml_handle_doc(attr, vvalue)
            elif kkeyword == 'type':
                attr.set('type', vvalue.upper())
            elif kkeyword == 'enumeration':
                xml_handle_enumeration(value, attr, kkeyword, vvalue, verbose)
            elif kkeyword == 'exists':
                xml_handle_exists(value, attr, kkeyword, vvalue)
            elif '__line__' in kkeyword:
                pass
            else:
                line_number = f'__line__{kkeyword}'
                raise ValueError(kkeyword + f'Line {value[line_number]}: facing an unknown \
situation while processing attributes of an attribute !')
# handle special keywords (symbols),
# assumed that you do not encounter further symbols nested inside


def second_level_attributes_handle(dct, fld, keyword, value):
    """If value is not a dictionary, this function handles the attributes of a nested field

"""
    if not isinstance(value, dict):
        if keyword == 'doc':
            xml_handle_doc(fld, value)
        elif keyword == NX_UNIT_IDNT:
            xml_handle_units(fld, value)
        elif keyword[0:2] == NX_ATTR_IDNT:  # attribute of a field
            line_number = f'__line__{keyword}'
            raise ValueError(keyword, f' unknown attribute \
    of a field case at line {dct[line_number]} !')
        elif keyword == 'exists':
            xml_handle_exists(dct, fld, keyword, value)
        elif keyword == 'dimensions':
            line_number = f'__line__{keyword}'
            raise ValueError(keyword, f' Line {dct[line_number]}: unknown dimensions \
    of a field case !')
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
        check_keyword_variable(verbose, dct, keyword, value)
        if verbose:
            sys.stdout.write(
                f'keyword_name:{keyword_name} keyword_type {keyword_type}\n')
        if keyword[-6:] == '(link)':
            xml_handle_link(dct, obj, keyword, value)

        elif keyword_type == '' and keyword_name == 'symbols':
            # print(value.key(), type(value.key()), value.value(), type(value.value()))
            xml_handle_symbols(dct, obj, keyword, value)

        elif ((keyword_type in NX_CLSS) or (keyword_type not in
                                            NX_TYPE_KEYS + [''] + NX_NEW_DEFINED_CLASSES)) \
                and '__line__' not in keyword_name:
            # we can be sure we need to instantiate a new group
            xml_handle_group(verbose, obj, value, keyword_name, keyword_type)

        elif keyword_name[0:2] == NX_ATTR_IDNT:  # check if obj qualifies
            attribute_attributes_handle(verbose, dct, obj, value, keyword)
        elif keyword == 'doc':
            xml_handle_doc(obj, value)

        elif keyword == 'enumeration':
            xml_handle_enumeration(dct, obj, keyword, value, verbose)

        elif keyword == 'dimensions':
            xml_handle_dimensions(dct, obj, keyword, value)

        elif keyword == 'exists':
            xml_handle_exists(dct, obj, keyword, value)

        elif keyword_name != '' and '__line__' not in keyword_name:
            fld = not_empty_keyword_name_handle(
                obj, keyword_type, keyword_name)
            second_nested_level_handle(verbose, value, fld)
            second_level_attributes_handle(dct, fld, keyword, value)
