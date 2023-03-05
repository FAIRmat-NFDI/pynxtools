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

NX_CLSS = nexus.get_nx_classes()
NX_NEW_DEFINED_CLASSES = ['NX_COMPLEX']
NX_TYPE_KEYS = nexus.get_nx_attribute_type()
NX_ATTR_IDNT = '\\@'
NX_UNIT_IDNT = 'unit'
DEPTH_SIZE = "    "
NX_UNIT_TYPES = nexus.get_nx_units()
# Attributes for definition attributs
rare_def_attributes = ['deprecated', 'ignoreExtraGroups', 'ignoreExtraFields',
                       'ignoreExtraAttributes', 'restricts']
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


def check_for_skiped_attributes(component, value, allowed_attr=None):
    """
        Check for any attributes have been skipped or not.
        NOTE: We should we should keep in mind about 'doc'
    """
    if value:
        for attr, val in value.items():
            if attr in ['doc']:
                continue
            if '__line__' in attr:
                continue
            line_number = f'__line__{attr}'
            if not isinstance(val, dict) \
                and '(' not in attr \
                and ')' not in attr\
                    and 'NX' not in attr:

                raise ValueError(f"An attribute '{attr}' in part '{component}' has been found"
                                 f". Please check arround line '{line_number}. At this moment"
                                 f"The allowed attrbutes are {allowed_attr}")


def check_for_optionality(obj, opl_key, opl_val):
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
    """
    The function deals with group instances

    """
    list_of_attr = ['name', 'type', 'nameType', 'deprecated']
    grp = ET.SubElement(obj, 'group')
    if keyword_name != '':  # use the custom name for the group
        grp.set('name', keyword_name)
    grp.set('type', keyword_type)
    for attr in list_of_attr:
        line_number = f"__line__{attr}"
        if attr in ['name', 'type'] or not value:
            continue
        if attr in value and not isinstance(value[attr], dict):
            validate_field_attribute_and_value(attr, value[attr], list_of_attr, value)
            grp.set(attr, value[attr])
            del value[attr]
            del value[line_number]

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
    assert 'dim' in value.keys(), f'Line {dct[line_number]}: dim is not a key in dimensions dict !'
    dims = ET.SubElement(obj, 'dimensions')
    # Consider all the childs under dimension is dim element and
    # its attributes
    val_attrs = list(value.keys())
    if 'rank' in value:
        rank = value['rank']
    else:
        rank = ''

    if isinstance(rank, int) and rank < 0:
        raise ValueError(f"Dimension must have some info about rank which is not available"
                         f". Please check arround Line: {dct[line_number]}")
    # value keys might contain two 'doc's the doc that contains list of doc
    # this is registred for dim's doc according to order in dim = [[index, value], ...]
    # so check for the doc with string

    for attr in val_attrs:
        line_number = f'__line__{attr}'
        if attr == 'doc' and not isinstance(value[attr], list):
            xml_handle_doc(dims, value[attr])
            del value[attr]
            del value[line_number]

    # Takeing care dimention element
    for attr in possible_dimension_attrs:
        if attr not in val_attrs or not value[attr]:
            continue
        line_number = f'__line__{attr}'
        dims.set(attr, str(value[attr]))
        val_attrs.remove(attr)
        val_attrs.remove(line_number)
        del value[attr]
        del value[line_number]
    xml_handle_dim_from_dimension_dict(dct, dims, keyword, value, rank)

    if isinstance(value, dict) and value != {}:
        recursive_build(dims, value, verbose=None)


# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
def xml_handle_dim_from_dimension_dict(dct, dims_obj, keyword, value, rank):
    """
        Handling dim element.
        NOTE: The inputs 'keyword' and 'value' are as input for xml_handle_dimensions
        function. please also read note in xml_handle_dimensions.
    """

    header_line_number = f"__line__{keyword}"
    possible_dim_attrs = ['ref', 'optional', 'recommended', 'required', 'incr', 'refindex']
    val_attrs = list(value.keys())

    dim_list = []
    # NOTE: dim_doc is a list of docs that come from dim
    for attr in ['dim', 'dim_doc', *possible_dim_attrs]:
        if attr not in val_attrs:
            continue
        line_number = f"__line__{attr}"
        # dim comes in precedence
        if attr == 'dim':
            # dim consists of list of [index, value]
            llist_ind_value = value[attr]
            assert isinstance(llist_ind_value, list), (f'Line {dct[line_number]}: dim'
                                                       f'argument not a list !')
            if isinstance(rank, int) and rank > 0:
                assert rank == len(llist_ind_value), (
                    f"check around Line {dct[line_number]}.\n"
                    f"Line {[value[line_number]]} rank value {rank} "
                    f"is not the same as dim array "
                    f"{len(llist_ind_value)}.")
            # Taking care of ind and value that comes as list of list
            for dim_ind_val in llist_ind_value:
                dim = ET.SubElement(dims_obj, 'dim')
                dim_list.append(dim)

                # Taking care of multidimensions or rank
                dim.set('index', str(dim_ind_val[0])
                        if len(dim_ind_val) >= 1 else '')
                dim.set('value', str(dim_ind_val[1])
                        if len(dim_ind_val) == 2 else '')
            assert attr in val_attrs and line_number in val_attrs, (
                f"Line {dct[line_number]} does not"
                f" have attribute {val_attrs}.")
            del value[attr]
            del value[line_number]

        elif attr == 'optional' and dim_list:
            for i, dim in enumerate(dim_list):
                # value[attr] is list for multiple elements or single value
                bool_ = value[attr][i] if isinstance(value[attr], list) else value[attr]
                dim.set('required', 'false' if bool_ == 'true' else 'true')
            del value[attr]
            del value[line_number]
        elif attr == 'dim_doc' and dim_list:
            # doc example '['doc_1', 'doc_2']
            doc_list = value[attr][1:-1]
            doc_list = [doc.strip()[1:-1] for doc in doc_list.split(',')]
            for i, dim in enumerate(dim_list):
                # value[attr] is list for multiple elements or single value
                doc = doc_list[i]  # if isinstance(value[attr], list) else value[attr]
                xml_handle_doc(dim, doc)
            del value[attr]
            del value[line_number]
        elif dim_list:
            for i, dim in enumerate(dim_list):
                try:
                    val = value[attr][i] if isinstance(value[attr], list) else value[attr]
                # value[attr] is list for multiple elements or single value
                    dim.set(attr, val)
                except Exception as ex:
                    raise IndexError(f"Each of the dimensions ('dim') should contain all "
                                     f"the same type of attributes.")
            del value[attr]
            del value[line_number]

    check_for_skiped_attributes('dim', value, possible_dim_attrs)


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


def xml_handle_link(dct, obj, keyword, value):
    """
        If we have an NXDL link we decode the name attribute from <optional string>(link)[:-6]
    """

    possible_attrs = ['target', 'napimount']

    val_attr = list(value.keys())
    name = keyword[:-6]
    link_obj = ET.SubElement(obj, 'link')
    link_obj.set('name', name)

    for attr in possible_attrs:
        line_number = f"__line__{attr}"
        if attr in val_attr and not isinstance(value[attr], dict):
            link_obj.set(attr, value[attr])
            del value[attr]
            del value[line_number]

    # Check for skipped attrinutes
    check_for_skiped_attributes('link', value, possible_attrs)

    if isinstance(value, dict) and value != {}:
        recursive_build(link_obj, value, verbose=None)


def xml_handle_choice(dct, obj, keyword, value):
    """
        Build choice xml elements. That consists of groups.
    """
    possible_attr = []
    choice_obj = ET.SubElement(obj, 'choice')
    # take care of special attributes
    name = keyword[:-8]
    choice_obj.set('name', name)

    if value and len(name) >= 1 and \
       isinstance(value, dict):
        for kkey, vvalue in value.items():
            if '__line__' in kkey:
                continue
            line_number = f"__line__{kkey}"
            if not isinstance(vvalue, dict) and \
               kkey in possible_attr:
                choice_obj.set(kkey, vvalue)

                del value[kkey]
                del value[line_number]

            elif not isinstance(vvalue, dict) and \
                    kkey not in possible_attr:
                raise ValueError(f"A attribute has been found in choice section, that is"
                                 f"not familiar. Please check arround line {value[line_number]}")
    else:
        line_number = f"__line__{keyword}"
        raise ValueError(f"A choice must have name attibute. Please check choice aound"
                         f" line {dct[line_number]}")

    check_for_skiped_attributes('choice', value, possible_attr)

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


def attribute_attributes_handle(dct, obj, keyword, value, verbose):
    """Handle the attributes found connected to attribute field"""
    # list of possible attribute of xml attribute elementsa
    attr_attr_list = ['name', 'type', 'unit', 'nameType',
                      'optional', 'recommended', 'minOccurs',
                      'maxOccurs']
    # as an attribute identifier
    keyword_name, keyword_typ = nx_name_type_resolving(keyword)
    line_number = f'__line__{keyword}'
    if keyword_name == '' and keyword_typ == '':
        raise ValueError(f'Line {dct[line_number]}: found an improper yaml key !')
    elemt_obj = ET.SubElement(obj, 'attribute')
    elemt_obj.set('name', keyword_name[2:])
    if keyword_typ:
        elemt_obj.set('type', keyword_typ)
    if value:
        val_attr = list(value.keys())
    else:
        val_attr = []

    if value and val_attr:
        # taking care of attributes of attributes
        for attr in attr_attr_list:
            line_number = f'__line__{attr}'
            if attr == 'unit' and attr in val_attr:
                elemt_obj.set(f"{attr}s", str(value[attr]))
                del value[attr]
                del value[line_number]
            elif attr in ['minOccurs', 'optional'] and attr in val_attr:
                if 'minOccurs' in val_attr and 'maxOccurs' in val_attr:
                    continue
                check_for_optionality(elemt_obj, attr, value[attr])
                del value[attr]
                del value[line_number]
            elif attr in val_attr:
                elemt_obj.set(attr, str(value[attr]))
                del value[attr]
                del value[line_number]
    if value:
        recursive_build(elemt_obj, value, verbose)


def validate_field_attribute_and_value(v_attr, vval, allowed_attribute, value):
    """
    Check for any attributes that comes with invalid name,
        and invalid value.
    """

    # check for empty val
    if (v_attr in allowed_attribute
        and not isinstance(vval, dict)
            and not vval):  # check for empty value

        line_number = f"__line__{v_attr}"
        raise ValueError(f"In a filed a valid attrbute ('{v_attr}') found. Please"
                         f"check arround line {value[line_number]}")

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
    allowed_attr = ['name', 'type', 'nameType', 'unit', 'minOccurs',
                    'axis', 'signal', 'deprecated', 'axes',
                    'data_offset', 'interpretation', 'maxOccurs',
                    'primary', 'recommended', 'optional', 'stride',
                    ]
    keyword_name, keyword_type = nx_name_type_resolving(keyword)
    line_number = f"__line__{keyword}"
    # Consider by default type is NX_CHAR
    typ = ''
    if keyword_type in NX_TYPE_KEYS + NX_NEW_DEFINED_CLASSES and keyword_type != 'NX_CHAR':
        typ = keyword_type
    # assume type is NX_CHAR, a NeXus default assumption if in doubt
    elemt_obj = ET.SubElement(obj, 'field')
    elemt_obj.set('name', keyword_name)
    if typ:
        elemt_obj.set('type', typ)
    if isinstance(value, dict) and value:
        val_attr = list(value.keys())
    else:
        val_attr = []

    for attr in allowed_attr:
        line_number = f'__line__{attr}'
        if attr in ['name', 'type'] and attr in val_attr:
            del value[attr]
            del value[line_number]
        elif attr in ['optional', 'minOccurs'] and attr in val_attr:
            validate_field_attribute_and_value(attr, value[attr], allowed_attr, value)
            if 'minOccurs' in val_attr and 'maxOccurs' in val_attr:
                continue
            check_for_optionality(elemt_obj, attr, value[attr])
            del value[attr]
            del value[line_number]
        elif attr == 'unit' and attr in val_attr:
            validate_field_attribute_and_value(attr, value[attr], allowed_attr, value)
            elemt_obj.set(f"{attr}s", str(value[attr]))
            del value[attr]
            del value[line_number]
        elif attr in val_attr:
            validate_field_attribute_and_value(attr, value[attr], allowed_attr, value)
            elemt_obj.set(attr, str(value[attr]))
            del value[attr]
            del value[line_number]

    # check for any invalid name of attrinbutes or child come with yaml
    if value:
        for attr, vvalue in value.items():
            validate_field_attribute_and_value(attr, vvalue, allowed_attr, value)

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
        if '__line__' in keyword:
            continue
        line_number = f"__line__{keyword}"
        keyword_name, keyword_type = nx_name_type_resolving(keyword)
        check_keyword_variable(verbose, dct, keyword, value)
        if verbose:
            sys.stdout.write(
                f'keyword_name:{keyword_name} keyword_type {keyword_type}\n')

        if keyword[-6:] == '(link)':
            xml_handle_link(dct, obj, keyword, value)
        elif keyword[-8:] == '(choice)':
            xml_handle_choice(dct, obj, keyword, value)
        elif keyword_type == '' and keyword_name == 'symbols':
            xml_handle_symbols(dct, obj, keyword, value)

        elif ((keyword_type in NX_CLSS) or (keyword_type not in
                                            [*NX_TYPE_KEYS, '', *NX_NEW_DEFINED_CLASSES])):
            # we can be sure we need to instantiate a new group
            xml_handle_group(verbose, obj, value, keyword_name, keyword_type)

        elif keyword_name[0:2] == NX_ATTR_IDNT:  # check if obj qualifies
            attribute_attributes_handle(dct, obj, keyword, value, verbose)
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
    sibling = dom.createProcessingInstruction(
        'xml-stylesheet', 'type="text/xsl" href="nxdlformat.xsl"')
    root = dom.firstChild
    dom.insertBefore(sibling, root)
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


def nyaml2nxdl(input_file: str, verbose: bool):
    """
    Main of the nyaml2nxdl converter, creates XML tree, namespace and
    schema, definitions then evaluates a dictionary nest of groups recursively and
    fields or (their) attributes as childs of the groups
    """

    rare_def_attributes = ['deprecated', 'ignoreExtraGroups',
                           'ignoreExtraFields', 'ignoreExtraAttributes', 'restricts']
    yml_appdef = yml_reader(input_file)

    if verbose:
        sys.stdout.write(f'input-file: {input_file}\n')
        sys.stdout.write('application/base contains the following root-level entries:\n')
        sys.stdout.write(str(yml_appdef.keys()))
    xml_root = ET.Element(
        'definition', {
            'xmlns': 'http://definition.nexusformat.org/nxdl/3.1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://definition.nexusformat.org/nxdl/3.1 ../nxdl.xsd'
        }
    )
    assert 'category' in yml_appdef.keys(
    ), 'Required root-level keyword category is missing!'
    assert yml_appdef['category'] in ['application', 'base'], 'Only \
application and base are valid categories!'
    assert 'doc' in yml_appdef.keys(), 'Required root-level keyword doc is missing!'

    xml_root.set('type', 'group')

    if yml_appdef['category'] == 'application':
        xml_root.set('category', 'application')
    else:
        xml_root.set('category', 'base')
    del yml_appdef['category']

    # check for rare attributes
    for attr in rare_def_attributes:
        if attr in yml_appdef:
            attr_val = str(yml_appdef[attr])
            xml_root.set(attr, attr_val)
            del yml_appdef[attr]

    if 'symbols' in yml_appdef.keys():
        xml_handle_symbols(yml_appdef,
                           xml_root,
                           'symbols',
                           yml_appdef['symbols'])

        del yml_appdef['symbols']

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

    keyword = list(yml_appdef.keys())[0]
    if "(" in keyword:
        extends = keyword[keyword.rfind("(") + 1:-1]
        name = keyword[0:keyword.rfind("(")]
    else:
        name = keyword
        extends = "NXobject"

    xml_root.set('name', name)
    xml_root.set('extends', extends)

    assert (keyword[0:2] == 'NX' and len(keyword) > 2), 'NX \
keyword has an invalid pattern, or is too short!'
    # Taking care if definition has empty content
    if yml_appdef[keyword]:
        recursive_build(xml_root, yml_appdef[keyword], verbose)

    pretty_print_xml(xml_root, input_file.rsplit(".", 1)[0] + '.nxdl.xml')
    if verbose:
        sys.stdout.write('Parsed YAML to NXDL successfully\n')