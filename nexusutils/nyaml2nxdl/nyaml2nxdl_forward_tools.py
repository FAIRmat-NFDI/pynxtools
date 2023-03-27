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
from xml.dom import minidom
import os
import textwrap

import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor

from yaml.nodes import ScalarNode
from yaml.resolver import BaseResolver
from yaml.loader import Loader

from nexusutils.nexus import nexus
from nexusutils.nyaml2nxdl.nyaml2nxdl_helper import (get_yaml_escape_char_reverter_dict,
                                                     cleaning_empty_lines)


DOM_COMMENT = ("\n"
               "# NeXus - Neutron and X-ray Common Data Format\n"
               "# \n"
               "# Copyright (C) 2014-2022 NeXus International Advisory Committee (NIAC)\n"
               "# \n"
               "# This library is free software; you can redistribute it and/or\n"
               "# modify it under the terms of the GNU Lesser General Public\n"
               "# License as published by the Free Software Foundation; either\n"
               "# version 2 of the License, or (at your option) any later version.\n"
               "#\n"
               "# This library is distributed in the hope that it will be useful,\n"
               "# but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
               "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\n"
               "# Lesser General Public License for more details.\n"
               "#\n"
               "# You should have received a copy of the GNU Lesser General Public\n"
               "# License along with this library; if not, write to the Free Software\n"
               "# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA\n"
               "#\n"
               "# For further information, see http://www.nexusformat.org\n")
NX_CLSS = nexus.get_nx_classes()
NX_NEW_DEFINED_CLASSES = ['NX_COMPLEX']
NX_TYPE_KEYS = nexus.get_nx_attribute_type()
NX_ATTR_IDNT = '\\@'
NX_UNIT_IDNT = 'unit'
DEPTH_SIZE = "    "
NX_UNIT_TYPES = nexus.get_nx_units()

# Attributes for definition attributs
# Keep the order as it is NIAC branch


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


def check_for_skiped_attributes(component, value, allowed_attr=None, verbose=False):
    """
        Check for any attributes have been skipped or not.
        NOTE: We should we should keep in mind about 'doc'
    """
    block_tag = ['enumeration']
    if value:
        for attr, val in value.items():
            if attr in ['doc']:
                continue
            if '__line__' in attr or attr in block_tag:
                continue
            line_number = f'__line__{attr}'
            if verbose:
                print(f"__line__ : {value[line_number]}")
            if not isinstance(val, dict) \
                and '\\@' not in attr\
                and attr not in allowed_attr\
                    and 'NX' not in attr and val:

                raise ValueError(f"An attribute '{attr}' in part '{component}' has been found"
                                 f". Please check arround line '{value[line_number]}. At this "
                                 f"moment. The allowed attrbutes are {allowed_attr}")


def check_optionality_and_write(obj, opl_key, opl_val):
    """
    Taking care of optinality.
    """
    if opl_key == 'optional':
        if opl_val == 'false':
            obj.set('required', 'true')
    elif opl_key == 'minOccurs':
        if opl_val == '0':
            pass
        else:
            obj.set(opl_key, str(opl_val))


def format_nxdl_doc(string):
    """NeXus format for doc string
    """
    string = check_for_mapping_char_other(string)
    formatted_doc = ''
    if "\n" not in string:
        if len(string) > 80:
            wrapped = textwrap.TextWrapper(width=80,
                                           break_long_words=False,
                                           replace_whitespace=False)
            string = '\n'.join(wrapped.wrap(string))
        formatted_doc = '\n' + f"{string}"
    else:
        text_lines = string.split('\n')
        text_lines = cleaning_empty_lines(text_lines)
        formatted_doc += "\n" + "\n".join(text_lines)
    if not formatted_doc.endswith("\n"):
        formatted_doc += "\n"
    return formatted_doc


def check_for_mapping_char_other(text):
    """
    Check for mapping char \':\' which does not be passed through yaml library.
    Then replace it by ':'.
    """
    if not text:
        text = ''
    text = str(text)
    if text == 'True':
        text = 'true'
    if text == 'False':
        text = 'false'
    # Some escape char is not valid in yaml libray which is written while writting
    # yaml file. In the time of writting nxdl revert to that escape char.
    escape_reverter = get_yaml_escape_char_reverter_dict()
    for key, val in escape_reverter.items():
        if key in text:
            text = text.replace(key, val)
    return str(text)


def xml_handle_doc(obj, value: str):
    """This function creates a 'doc' element instance, and appends it to an existing element

    """

    doctag = ET.SubElement(obj, 'doc')
    text = format_nxdl_doc(check_for_mapping_char_other(value)).strip()
    # To keep the doc middle of doc tag.
    doctag.text = f"\n{text}\n"


def xml_handle_units(obj, value):
    """This function creates a 'units' element instance, and appends it to an existing element

    """
    obj.set('units', str(value))


# pylint: disable=too-many-branches
def xml_handle_exists(dct, obj, keyword, value):
    """
    This function creates an 'exists' element instance, and appends it to an existing element
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
        elif len(value) == 4 and value[0] == 'max' and value[2] == 'min':
            obj.set('minOccurs', str(value[3]))
            if str(value[1]) != 'infty':
                obj.set('maxOccurs', str(value[3]))
            else:
                obj.set('maxOccurs', 'unbounded')
        elif len(value) == 4 and (value[0] != 'min' or value[2] != 'max'):
            raise ValueError(f'Line {dct[line_number]}: exists keyword'
                             f'needs to go either with an optional [recommended] list with two '
                             f'entries either [min, <uint>] or [max, <uint>], or a list of four '
                             f'entries [min, <uint>, max, <uint>] !')
        else:
            raise ValueError(f'Line {dct[line_number]}: exists keyword '
                             f'needs to go either with optional, recommended, a list with two '
                             f'entries either [min, <uint>] or [max, <uint>], or a list of four '
                             f'entries [min, <uint>, max, <uint>] !')
    else:
        if value == 'optional':
            obj.set('optional', 'true')
        elif value == 'recommended':
            obj.set('recommended', 'true')
        elif value == 'required':
            obj.set('required', 'true')
        else:
            obj.set('minOccurs', '0')


# pylint: disable=too-many-branches
def xml_handle_group(obj, keyword, value, verbose=False):
    """
    The function deals with group instances
    """

    list_of_attr = ['name', 'type', 'nameType', 'deprecated', 'optional', 'recommended',
                    'exists', 'unit']
    l_bracket = -1
    r_bracket = -1
    if keyword.count('(') == 1:
        l_bracket = keyword.index('(')
    if keyword.count(')') == 1:
        r_bracket = keyword.index(')')

    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    if not keyword_name and not keyword_type:
        raise ValueError("A group must have both value and name. Check for group.")
    grp = ET.SubElement(obj, 'group')

    # type come first
    if l_bracket == 0 and r_bracket > 0:
        grp.set('type', keyword_type)
        if keyword_name:
            grp.set('name', keyword_name)
    elif l_bracket > 0:
        grp.set('name', keyword_name)
        if keyword_type:
            grp.set('type', keyword_type)
    else:
        grp.set('name', keyword_name)

    if value:
        rm_key_list = []
        for attr, vval in value.items():
            if '__line__' in attr:
                continue
            line_number = f"__line__{attr}"
            if attr == 'doc':
                xml_handle_doc(grp, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr == 'exists' and vval:
                xml_handle_exists(value, grp, attr, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr == 'unit':
                xml_handle_units(grp, vval)
            elif attr in list_of_attr and not isinstance(vval, dict) and vval:
                validate_field_attribute_and_value(attr, vval, list_of_attr, value)
                grp.set(attr, check_for_mapping_char_other(vval))
                rm_key_list.append(attr)
                rm_key_list.append(line_number)

        for key in rm_key_list:
            del value[key]
        # Check for skipped attrinutes
        check_for_skiped_attributes('group', value, list_of_attr, verbose)
    if isinstance(value, dict) and value != {}:
        recursive_build(grp, value, verbose)


def xml_handle_dimensions(dct, obj, keyword, value: dict):
    """
    This function creates a 'dimensions' element instance, and appends it to an existing element

    NOTE: we could create xml_handle_dim() function.
        But, the dim elements in yaml file is defined as dim =[[index, value]]
        but dim has other attributes such as 'ref' and also might have doc as chlid.
        so in that sense dim should have come as dict keeping attributes and child as members of
        dict.
        Regarding this situation all the attributes and child doc has been included here.
    """

    possible_dimension_attrs = ['rank']
    line_number = f'__line__{keyword}'
    assert 'dim' in value.keys(), (f"Line {dct[line_number]}: No dim as child of dimension has "
                                   f"been found.")
    dims = ET.SubElement(obj, 'dimensions')
    # Consider all the childs under dimension is dim element and
    # its attributes
#    val_attrs = list(value.keys())
    rm_key_list = []
    rank = ''
    for key, val in value.items():
        if '__line__' in key:
            continue
        line_number = f"__line__{key}"

        if key == 'rank':
            rank = val or ''
            if isinstance(rank, int) and rank < 0:
                raise ValueError(f"Dimension must have some info about rank which is not "
                                 f"available. Please check arround Line: {dct[line_number]}")
            dims.set(key, str(val))
            rm_key_list.append(key)
            rm_key_list.append(line_number)
        # Check dimension doc and handle it
        elif key == 'doc' and isinstance(val, str):
            xml_handle_doc(dims, val)
            rm_key_list.append(key)
            rm_key_list.append(line_number)
        elif key in possible_dimension_attrs and not isinstance(val, dict):
            dims.set(key, str(val))
            rm_key_list.append(key)
            rm_key_list.append(line_number)

    for key in rm_key_list:
        del value[key]

    xml_handle_dim_from_dimension_dict(dct, dims, keyword, value, rank=False)

    if isinstance(value, dict) and value != {}:
        recursive_build(dims, value, verbose=None)


# pylint: disable=too-many-locals, too-many-arguments
def xml_handle_dim_from_dimension_dict(dct, dims_obj, keyword, value, rank, verbose=False):
    """
        Handling dim element.
        NOTE: The inputs 'keyword' and 'value' are as input for xml_handle_dimensions
        function. please also read note in xml_handle_dimensions.
    """

    possible_dim_attrs = ['ref', 'optional', 'recommended', 'required', 'incr', 'refindex']
    header_line_number = f"__line__{keyword}"

    dim_list = []
    rm_key_list = []
    # NOTE: dim doc and other attributes except 'index' and 'value' will come as list of value
    # under dim_parameters
    if not value:
        return
    rank = ''
    # pylint: disable=too-many-nested-blocks
    for attr, vvalue in value.items():
        if '__line__' in attr:
            continue

        line_number = f"__line__{attr}"
        # dim comes in precedence
        if attr == 'dim':
            # dim consists of list of [index, value]
            llist_ind_value = vvalue
            assert isinstance(llist_ind_value, list), (f'Line {value[line_number]}: dim'
                                                       f'argument not a list !')
            if isinstance(rank, int) and rank > 0:
                assert rank == len(llist_ind_value), (
                    f"Wrong dimension rank check around Line {dct[header_line_number]}.\n"
                    f"Line {[dct[header_line_number]]} rank value {rank} "
                    f"is not the same as dim array = "
                    f"{len(llist_ind_value)}.")
            # Taking care of ind and value that comes as list of list
            for dim_ind_val in llist_ind_value:
                dim = ET.SubElement(dims_obj, 'dim')

                # Taking care of multidimensions or rank
                if len(dim_ind_val) >= 1 and dim_ind_val[0]:
                    dim.set('index', str(dim_ind_val[0]))
                if len(dim_ind_val) == 2 and dim_ind_val[1]:
                    dim.set('value', str(dim_ind_val[1]))
                dim_list.append(dim)
            rm_key_list.append(attr)
            rm_key_list.append(line_number)

        elif attr == 'dim_parameters' and isinstance(vvalue, dict):
            for kkkey, vvval in vvalue.items():
                if '__line__' in kkkey:
                    continue
                if kkkey == 'doc' and dim_list:
                    # doc comes as list of doc
                    for i, dim in enumerate(dim_list):
                        if isinstance(vvval, list) and i < len(vvval):
                            tmp_val = vvval[i]
                            xml_handle_doc(dim, vvval[i])
                        # Check all the dim have doc if not skip
                        elif isinstance(vvval, list) and i >= len(vvval):
                            pass
                else:
                    for i, dim in enumerate(dim_list):
                        # all atribute of dims comes as list
                        if isinstance(vvval, list) and i < len(vvval):
                            tmp_val = vvval[i]
                            dim.set(kkkey, str(tmp_val))

                        # Check all the dim have doc if not skip
                        elif isinstance(vvval, list) and i >= len(vvval):
                            pass
                        # All dim might have the same value for the same attribute
                        elif not isinstance(vvval, list):
                            tmp_val = value
                            dim.set(kkkey, str(tmp_val))
            rm_key_list.append(attr)
            rm_key_list.append(line_number)
        else:
            raise ValueError(f"Got unexpected block except 'dim' and 'dim_parameters'."
                             f"Please check arround line {line_number}")

    for key in rm_key_list:
        del value[key]

    check_for_skiped_attributes('dim', value, possible_dim_attrs, verbose)


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


# pylint: disable=unused-argument
def xml_handle_link(dct, obj, keyword, value, verbose):
    """
        If we have an NXDL link we decode the name attribute from <optional string>(link)[:-6]
    """

    possible_attrs = ['name', 'target', 'napimount']
    name = keyword[:-6]
    link_obj = ET.SubElement(obj, 'link')
    link_obj.set('name', str(name))

    if value:
        rm_key_list = []
        for attr, vval in value.items():
            if '__line__' in attr:
                continue
            line_number = f"__line__{attr}"
            if attr == 'doc':
                xml_handle_doc(link_obj, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr in possible_attrs and not isinstance(vval, dict):
                if vval:
                    link_obj.set(attr, str(vval))
                rm_key_list.append(attr)
                rm_key_list.append(line_number)

        for key in rm_key_list:
            del value[key]
        # Check for skipped attrinutes
        check_for_skiped_attributes('link', value, possible_attrs, verbose)

    if isinstance(value, dict) and value != {}:
        recursive_build(link_obj, value, verbose=None)


def xml_handle_choice(dct, obj, keyword, value, verbose=False):
    """
        Build choice xml elements. That consists of groups.
    """
    possible_attr = []
    choice_obj = ET.SubElement(obj, 'choice')
    # take care of special attributes
    name = keyword[:-8]
    choice_obj.set('name', name)

    if value:
        rm_key_list = []
        for attr, vval in value.items():
            if '__line__' in attr:
                continue
            line_number = f"__line__{attr}"
            if attr == 'doc':
                xml_handle_doc(choice_obj, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr in possible_attr and not isinstance(vval, dict):
                if vval:
                    choice_obj.set(attr, str(vval))
                rm_key_list.append(attr)
                rm_key_list.append(line_number)

        for key in rm_key_list:
            del value[key]
        # Check for skipped attrinutes
        check_for_skiped_attributes('choice', value, possible_attr, verbose)

    if isinstance(value, dict) and value != {}:
        recursive_build(choice_obj, value, verbose=None)


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
    rm_key_list = []
    for kkeyword, vvalue in value.items():
        if '__line__' in kkeyword:
            continue
        if kkeyword != 'doc':
            line_number = f'__line__{kkeyword}'
            assert vvalue is not None and isinstance(
                vvalue, str), f'Line {value[line_number]}: put a comment in doc string !'
            sym = ET.SubElement(syms, 'symbol')
            sym.set('name', str(kkeyword))
            # sym_doc = ET.SubElement(sym, 'doc')
            xml_handle_doc(sym, vvalue)
            rm_key_list.append(kkeyword)
            rm_key_list.append(line_number)
            # sym_doc.text = '\n' + textwrap.fill(vvalue, width=70) + '\n'
    for key in rm_key_list:
        del value[key]


def check_keyword_variable(verbose, dct, keyword, value):
    """
    Check whether both keyword_name and keyword_type are empty,
        and complains if it is the case
    """
    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    if verbose:
        sys.stdout.write(
            f'{keyword_name}({keyword_type}): value type is {type(value)}\n')
    if keyword_name == '' and keyword_type == '':
        line_number = f'__line__{keyword}'
        raise ValueError(f'Line {dct[line_number]}: found an improper yaml key !')


def helper_keyword_type(kkeyword_type):
    """
        This function is returning a value of keyword_type if it belong to NX_TYPE_KEYS
    """
    if kkeyword_type in NX_TYPE_KEYS:
        return kkeyword_type
    return None


def verbose_flag(verbose, keyword, value):
    """
        Verbose stdout printing for nested levels of yaml file, if verbose flag is active
    """
    if verbose:
        sys.stdout.write(f'  key:{keyword}; value type is {type(value)}\n')


def attribute_handle_attributes(dct, obj, keyword, value, verbose):
    """Handle the attributes found connected to attribute field"""
    # list of possible attribute of xml attribute elementsa
    attr_attr_list = ['name', 'type', 'unit', 'nameType',
                      'optional', 'recommended', 'minOccurs',
                      'maxOccurs', 'deprecated', 'exists']
    # as an attribute identifier
    keyword_name, keyword_typ = nx_name_type_resolving(keyword)
    line_number = f'__line__{keyword}'
    if verbose:
        print(f"__line__ : {dct[line_number]}")
    if keyword_name == '' and keyword_typ == '':
        raise ValueError(f'Line {dct[line_number]}: found an improper yaml key !')
    elemt_obj = ET.SubElement(obj, 'attribute')
    elemt_obj.set('name', keyword_name[2:])
    if keyword_typ:
        elemt_obj.set('type', keyword_typ)

    rm_key_list = []
    if value and value:
        # taking care of attributes of attributes
        for attr, attr_val in value.items():
            if '__line__' in attr:
                continue
            line_number = f"__line__{attr}"

            if attr in ['doc', *attr_attr_list] and not isinstance(attr_val, dict):
                if attr == 'unit':
                    elemt_obj.set(f"{attr}s", str(value[attr]))
                    rm_key_list.append(attr)
                    rm_key_list.append(line_number)
                elif attr == 'exists' and attr_val:
                    xml_handle_exists(value, elemt_obj, attr, attr_val)
                    rm_key_list.append(attr)
                    rm_key_list.append(line_number)
                elif attr == 'unit':
                    xml_handle_units(elemt_obj, attr_val)
                elif attr == 'doc':
                    xml_handle_doc(elemt_obj, format_nxdl_doc(attr_val))
                    rm_key_list.append(attr)
                    rm_key_list.append(line_number)
                else:
                    elemt_obj.set(attr, check_for_mapping_char_other(attr_val))
                    rm_key_list.append(attr)
                    rm_key_list.append(line_number)

        for key in rm_key_list:
            del value[key]
        # Check cor skiped attribute
        check_for_skiped_attributes('Attribute', value, attr_attr_list, verbose)
    if value:
        recursive_build(elemt_obj, value, verbose)


def validate_field_attribute_and_value(v_attr, vval, allowed_attribute, value):
    """
    Check for any attributes that comes with invalid name,
        and invalid value.
    """

    # check for empty val
    if (not isinstance(vval, dict)
            and not str(vval)):  # check for empty value

        line_number = f"__line__{v_attr}"
        raise ValueError(f"In a field a valid attrbute ('{v_attr}') found that is not stored."
                         f" Please check arround line {value[line_number]}")

    # The bellow elements might come as child element
    skipped_child_name = ['doc', 'dimension', 'enumeration', 'choice', 'exists']
    # check for invalid key or attributes
    if (v_attr not in [*skipped_child_name, *allowed_attribute]
        and '__line__' not in v_attr
        and not isinstance(vval, dict)
        and '(' not in v_attr           # skip only groups and field that has name and type
            and '\\@' not in v_attr):     # skip nexus attributes

        line_number = f"__line__{v_attr}"
        raise ValueError(f"In a field or group a invalid attribute ('{v_attr}') or child has found."
                         f" Please check arround line {value[line_number]}.")


def xml_handle_fields(obj, keyword, value, verbose=False):
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
    allowed_attr = ['name', 'type', 'nameType', 'unit', 'minOccurs', 'long_name',
                    'axis', 'signal', 'deprecated', 'axes', 'exists',
                    'data_offset', 'interpretation', 'maxOccurs',
                    'primary', 'recommended', 'optional', 'stride']

    l_bracket = -1
    r_bracket = -1
    if keyword.count('(') == 1:
        l_bracket = keyword.index('(')
    if keyword.count(')') == 1:
        r_bracket = keyword.index(')')

    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    if not keyword_type and not keyword_name:
        raise ValueError("Check for name or type in field.")
    elemt_obj = ET.SubElement(obj, 'field')

    # type come first
    if l_bracket == 0 and r_bracket > 0:
        elemt_obj.set('type', keyword_type)
        if keyword_name:
            elemt_obj.set('name', keyword_name)
    elif l_bracket > 0:
        elemt_obj.set('name', keyword_name)
        if keyword_type:
            elemt_obj.set('type', keyword_type)
    else:
        elemt_obj.set('name', keyword_name)

    if value:
        rm_key_list = []
        for attr, vval in value.items():
            if '__line__' in attr:
                continue
            line_number = f"__line__{attr}"
            if attr == 'doc':
                xml_handle_doc(elemt_obj, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr == 'exists' and vval:
                xml_handle_exists(value, elemt_obj, attr, vval)
                rm_key_list.append(attr)
                rm_key_list.append(line_number)
            elif attr == 'unit':
                xml_handle_units(elemt_obj, vval)
            elif attr in allowed_attr and not isinstance(vval, dict) and vval:
                validate_field_attribute_and_value(attr, vval, allowed_attr, value)
                elemt_obj.set(attr, check_for_mapping_char_other(vval))
                rm_key_list.append(attr)
                rm_key_list.append(line_number)

        for key in rm_key_list:
            del value[key]
        # Check for skipped attrinutes
        check_for_skiped_attributes('field', value, allowed_attr, verbose)

    if isinstance(value, dict) and value != {}:
        recursive_build(elemt_obj, value, verbose)


def recursive_build(obj, dct, verbose):
    """obj is the current node of the XML tree where we want to append to,
    dct is a dictionary object which represents the content of a child to obj
    dct may contain further dictionary nests, representing NXDL groups,
    which trigger recursive processing
    NXDL fields may contain attributes but trigger no recursion so attributes are leafs.

    """
    for keyword, value in iter(dct.items()):
        if '__line__' in keyword:
            continue
        line_number = f"__line__{keyword}"
        keyword_name, keyword_type = nx_name_type_resolving(keyword)
        check_keyword_variable(verbose, dct, keyword, value)
        if verbose:
            sys.stdout.write(
                f'keyword_name:{keyword_name} keyword_type {keyword_type}\n')

        if keyword[-6:] == '(link)':
            xml_handle_link(dct, obj, keyword, value, verbose)
        elif keyword[-8:] == '(choice)':
            xml_handle_choice(dct, obj, keyword, value)
        elif keyword_type == '' and keyword_name == 'symbols':
            xml_handle_symbols(dct, obj, keyword, value)

        elif ((keyword_type in NX_CLSS) or (keyword_type not in
                                            [*NX_TYPE_KEYS, '', *NX_NEW_DEFINED_CLASSES])):
            # we can be sure we need to instantiate a new group
            xml_handle_group(obj, keyword, value, verbose)

        elif keyword_name[0:2] == NX_ATTR_IDNT:  # check if obj qualifies
            attribute_handle_attributes(dct, obj, keyword, value, verbose)
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
        else:
            raise ValueError(f"An unfamiliar type of element {keyword} has been found which is "
                             f"not be able to be resolved. Chekc arround line {dct[line_number]}")


def pretty_print_xml(xml_root, output_xml):
    """
    Print better human-readable indented and formatted xml file using
    built-in libraries and preceding XML processing instruction
    """
    dom = minidom.parseString(ET.tostring(
        xml_root, encoding='utf-8', method='xml'))
    proc_instractionn = dom.createProcessingInstruction(
        'xml-stylesheet', 'type="text/xsl" href="nxdlformat.xsl"')
    dom_comment = dom.createComment(DOM_COMMENT)
    root = dom.firstChild
    dom.insertBefore(proc_instractionn, root)
    dom.insertBefore(dom_comment, root)
    xml_string = dom.toprettyxml(indent=1 * DEPTH_SIZE, newl='\n', encoding='UTF-8')
    with open('tmp.xml', "wb") as file_tmp:
        file_tmp.write(xml_string)
    flag = False
    with open('tmp.xml', "r", encoding="utf-8") as file_out:
        with open(output_xml, "w", encoding="utf-8") as file_out_mod:
            for i in file_out.readlines():
                if '<doc>' not in i and '</doc>' not in i and flag is False:
                    file_out_mod.write(i)
                elif '<doc>' in i and '</doc>' in i:
                    file_out_mod.write(i)
                elif '<doc>' in i and '</doc>' not in i:
                    flag = True
                    white_spaces = len(i) - len(i.lstrip())
                    file_out_mod.write(i)
                elif '<doc>' not in i and '</doc>' not in i and flag is True:
                    file_out_mod.write((white_spaces + 5) * ' ' + i)
                elif '<doc>' not in i and '</doc>' in i and flag is True:
                    file_out_mod.write(white_spaces * ' ' + i)
                    flag = False
    os.remove('tmp.xml')


# pylint: disable=too-many-statements
def nyaml2nxdl(input_file: str, verbose: bool):
    """
    Main of the nyaml2nxdl converter, creates XML tree, namespace and
    schema, definitions then evaluates a dictionary nest of groups recursively and
    fields or (their) attributes as childs of the groups
    """

    def_attributes = ['deprecated', 'ignoreExtraGroups', 'category', 'type',
                      'ignoreExtraFields', 'ignoreExtraAttributes', 'restricts']
    yml_appdef = yml_reader(input_file)

    if verbose:
        sys.stdout.write(f'input-file: {input_file}\n')
        sys.stdout.write('application/base contains the following root-level entries:\n')
        sys.stdout.write(str(yml_appdef.keys()))
    xml_root = ET.Element('definition', {})
    assert 'category' in yml_appdef.keys(
    ), 'Required root-level keyword category is missing!'
    assert yml_appdef['category'] in ['application', 'base'], 'Only \
application and base are valid categories!'
    assert 'doc' in yml_appdef.keys(), 'Required root-level keyword doc is missing!'

    name_extends = ''
    yml_appdef_copy = yml_appdef.copy()
    for kkey, vvalue in yml_appdef_copy.items():
        if '__line__' in kkey:
            continue
        line_number = f"__line__{kkey}"
        if not isinstance(vvalue, dict) and kkey in def_attributes:
            xml_root.set(kkey, str(vvalue) or '')
            del yml_appdef[line_number]
            del yml_appdef[kkey]
        # Taking care or name and extends
        elif 'NX' in kkey:
            # Tacking the attribute order but the correct value will be stored later
            # check for name first or type first if (NXobject)NXname then type first
            l_bracket_ind = kkey.rfind('(')
            r_bracket_ind = kkey.rfind(')')
            if l_bracket_ind == 0:
                extend = kkey[1:r_bracket_ind]
                name = kkey[r_bracket_ind + 1:]
                xml_root.set('extends', extend)
                xml_root.set('name', name)
            elif l_bracket_ind > 0:
                name = kkey[0:l_bracket_ind]
                extend = kkey[l_bracket_ind + 1: r_bracket_ind]
                xml_root.set('name', name)
                xml_root.set('extends', extend)
            else:
                name = kkey
                xml_root.set('name', name)
                xml_root.set('extends', 'NXobject')
            name_extends = kkey

    if 'type' not in xml_root.attrib:
        xml_root.set('type', "group")
    # Taking care of namespaces
    namespaces = {'xmlns': 'http://definition.nexusformat.org/nxdl/3.1',
                  'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                  'xsi:schemaLocation': 'http://definition.nexusformat.org/nxdl/3.1 ../nxdl.xsd'}
    for key, ns_ in namespaces.items():
        xml_root.attrib[key] = ns_
    if 'symbols' in yml_appdef.keys():
        xml_handle_symbols(yml_appdef,
                           xml_root,
                           'symbols',
                           yml_appdef['symbols'])

        del yml_appdef['symbols']
#        del yml_appdef["__line__symbols"]

    assert isinstance(yml_appdef['doc'], str) and yml_appdef['doc'] != '', 'Doc \
has to be a non-empty string!'

    doctag = ET.SubElement(xml_root, 'doc')
    doctag.text = format_nxdl_doc(yml_appdef['doc'])

    del yml_appdef['doc']

    root_keys = 0
    for key in yml_appdef.keys():
        if '__line__' not in key:
            root_keys += 1
            extra_key = key

    assert root_keys == 1, (f"Accepting at most keywords: category, doc, symbols, and NX... "
                            f"at root-level! check key at root level {extra_key}")

    assert ('NX' in name_extends and len(name_extends) > 2), 'NX \
keyword has an invalid pattern, or is too short!'
    # Taking care if definition has empty content
    if yml_appdef[name_extends]:
        recursive_build(xml_root, yml_appdef[name_extends], verbose)

    pretty_print_xml(xml_root, input_file.rsplit(".", 1)[0] + '.nxdl.xml')
    if verbose:
        sys.stdout.write('Parsed YAML to NXDL successfully\n')
