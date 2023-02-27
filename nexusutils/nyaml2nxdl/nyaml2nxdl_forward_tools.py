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
from . import check_escape_sequence_in_text

NX_CLSS = nexus.get_nx_classes()
NX_NEW_DEFINED_CLASSES = ['NX_COMPLEX']
NX_TYPE_KEYS = nexus.get_nx_attribute_type()
NX_ATTR_IDNT = '\\@'
NX_UNIT_IDNT = 'unit'
NX_UNIT_TYPES = nexus.get_nx_units()
# Attributes for definition attributs
rare_def_attributes = ['deprecated', 'ignoreExtraGroups','ignoreExtraFields',
                       'ignoreExtraAttributes']
# Keep the order as it is NIAC branch
# TODO try to move in one place as it is in for forward and backward
# dim should precedent
OPSSIBLE_DIM_ATTRS = ['dim', 'ref', 'optional', 'recommended', 'doc']
POSSIBLE_DIMENSION_ATTRS = ['doc', 'rank']


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
    # Consider all the childs under dimension is dim element and
    # its attributes
    val_attrs = list(value.keys())
    if 'rank' in value:
        rank = value['rank']
    else:
        rank = -1

    # taking care of dim elements
    dim_list = []
    for attr in OPSSIBLE_DIM_ATTRS:
        line_number = f'__line__{attr}'
        if attr not in val_attrs:
            continue

        # dim comes in precedence
        if attr == 'dim':
            assert isinstance(value[attr], list), (f'Line {value[line_number]}: dim'
                                        f'argument not a list !')
            if isinstance(rank, int) and rank>0 :
                assert rank == len(value[attr]), (f"Line {[value[line_number]]} rank value {rank} "
                                                  f"is not the same as dim array "
                                                  f"{len(value[attr])}")
                for dim_no in range(rank):
                    dim = ET.SubElement(dims, 'dim')
                    dim_list.append(dim)

                    # Taking care of multidimensions or rank
                    dim.set('index', str(value[attr][dim_no][0])
                            if len(value[attr][dim_no]) >= 1 else '')
                    dim.set('value', str(value[attr][dim_no][1])
                            if len(value[attr][dim_no]) == 2 else '')
            assert attr in val_attrs and line_number in val_attrs, (f"Line {value[line_number]} does not"
                                                                  f" have attribute {val_attrs}.")
            val_attrs.remove(attr)
            val_attrs.remove(line_number)
        elif attr == 'optional'and not dim_list:
            for i, dim in enumerate(dim_list):
                # value[attr] is list for multiple elements or single value
                bool_ = value[attr][i] if isinstance(value[attr], list) else value[attr]
                dim.set('required', 'false' if bool_=='true' else 'true' )
            val_attrs.remove(attr)
            val_attrs.remove(line_number)
        elif attr == 'doc' and not dim_list:
            for i, dim in enumerate(dim_list):
                # value[attr] is list for multiple elements or single value
                doc = value[attr][i] if isinstance(value[attr],  list) else value[attr]
                xml_handle_doc(dim, doc)
            val_attrs.remove(attr)
            val_attrs.remove(line_number)
        elif not dim_list:
            for i, dim in enumerate(dim_list):
                val = value[attr][i] if isinstance(value[attr], list) else value[attr]
                # value[attr] is list for multiple elements or single value
                dim.set(attr, val)
            val_attrs.remove(attr)
            val_attrs.remove(line_number)
    # Takeing care dimention element
    for attr in POSSIBLE_DIMENSION_ATTRS:
        if attr not in val_attrs:
            continue
        line_number = f'__line__{attr}'
        if isinstance(rank, str):
        # Rank could be undefined means it might have different patterns,
        # different ranks or dynamic
            val_attrs.remove(attr)
            val_attrs.remove(line_number)
            break
        if attr == 'rank':
            rank = value[attr]
        line_number = f'__line__{attr}'
        dims.set(attr, str(value[attr]))
        val_attrs.remove(attr)
        val_attrs.remove(line_number)

    line_number = '__line__dim'
    assert len(val_attrs) == 0, (f'Line {value[line_number]}: dim argument '
                                 f'is a list with unexpected number of entries!')


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
                if isinstance(value[element], dict):
                    recursive_build(itm, value[element], verbose)

# TODO change obj in xml_obj
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
    # TODO: remove else: pass clause
    else:
        pass

# TODO Change doc string here as it is!
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


def attribute_attributes_handle(dct, obj, keyword, value, verbose):
    """Handle the attributes found connected to attribute field"""
    # list of possible attribute of xml attribute elementsa
    attr_list = ['name', 'type', 'units', 'nameType']
    # as an attribute identifier
    keyword_name, keyword_typ = nx_name_type_resolving(keyword)
    line_number = f'__line__{keyword}'
    elemt_obj = ET.SubElement(obj, 'attribute')
    elemt_obj.set('name', keyword_name[2:])
    elemt_obj.set('type', keyword_typ)
    if value:
        val_attr = list(value.keys())
    else:
        val_attr = []

    if value and val_attr:
        # taking care of attributes of attributes
        for attr in attr_list:
            line_number = f'__line__{attr}'
            if attr in val_attr:
                elemt_obj.set(attr, value[attr])
                del value[attr]
                del value[line_number]
        if value:
            recursive_build(elemt_obj, value, verbose)


# Rename it as xml_handle_filed
def xml_handle_fields(obj, keyword, value, verbose):
    """
    Handle a field in yaml file.
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

    # List of possible attributes of xml elements
    field_attr = ['name', 'type', 'nameType', 'units', 'axis', 'signal']
    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    # Consider by default type is NX_CHAR
    typ = ''
    if keyword_type in NX_TYPE_KEYS + NX_NEW_DEFINED_CLASSES and keyword_type != 'NX_CHAR':
        typ = keyword_type
    # assume type is NX_CHAR, a NeXus default assumption if in doubt
    elemt_obj = ET.SubElement(obj, 'field')
    elemt_obj.set('name', keyword_name)
    if typ:
        elemt_obj.set('type', typ)
    if isinstance(value, dict):
        val_attr = list(value.keys())
    else:
        val_attr = []

    for attr in field_attr:
        line_number = f'__line__{attr}'
        if attr in ['name', 'type'] and attr in val_attr:
            del value[attr]
            del value[line_number]
        elif attr in val_attr and line_number in val_attr:
            elemt_obj.set(attr, str(value[attr]))
            del value[attr]
            del value[line_number]

    if isinstance(value, dict) and value:
        recursive_build(obj=elemt_obj, dct=value, verbose=verbose)


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
            xml_handle_symbols(dct, obj, keyword, value)

        elif ((keyword_type in NX_CLSS) or (keyword_type not in
                                            NX_TYPE_KEYS + [''] + NX_NEW_DEFINED_CLASSES)) \
                and '__line__' not in keyword_name:
            # we can be sure we need to instantiate a new group
            xml_handle_group(verbose, obj, value, keyword_name, keyword_type)

        elif keyword_name[0:2] == NX_ATTR_IDNT:  # check if obj qualifies
            attribute_attributes_handle(dct, obj, keyword, value, verbose )
        elif keyword == 'doc':
            xml_handle_doc(obj, value)
        elif keyword == NX_UNIT_IDNT:
             xml_handle_units(obj, value)
        elif keyword == 'enumeration':
            xml_handle_enumeration(dct, obj, keyword, value, verbose)

        elif keyword == 'dimensions':
            xml_handle_dimensions(dct, obj, keyword, value)

        elif keyword == 'exists':
            xml_handle_exists(dct, obj, keyword, value)
        # Handles fileds e.g. AXISNAME
        elif keyword_name != '' and '__line__' not in keyword_name:
            xml_handle_fields(obj, keyword, value, verbose)
