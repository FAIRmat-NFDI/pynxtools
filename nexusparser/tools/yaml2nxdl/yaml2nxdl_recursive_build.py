#!/usr/bin/env python3
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

import os
import sys
import yaml
import xml.etree.ElementTree as ET
from yaml2nxdl_utils import nx_name_type_resolving
from yaml2nxdl_utils import nx_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt


def xml_handle_docstring(obj, keyword, value):
    obj.set('doc', str(value))


def xml_handle_units(obj, keyword, value):
    obj.set('units', value)


def xml_handle_exists(obj, keyword, value):
    if value is not None:
        if isinstance(value, list):
            if len(value) == 2:
                if value[0] == 'min':
                    obj.set('minOccurs', str(value[1]))
                if value[0] == 'max':
                    obj.set('maxOccurs', str(value[1]))
            elif len(value) == 4:
                if value[0] == 'min' and value[2] == 'max':
                    obj.set('minOccurs', str(value[1]))
                    if str(value[3]) != 'infty':
                        obj.set('maxOccurs', str(value[3]))
                    else:
                        obj.set('maxOccurs', 'unbounded')
                else:
                    raise ValueError('exists keyword needs to go either with optional, recommended, a list with two entries either [min, <uint>] or [max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
            else:
                raise ValueError('exists keyword needs to go either with optional, recommended, a list with two entries either [min, <uint>] or [max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
        else:
            if value == 'optional':
                obj.set('optional', 'true')
            elif value == 'recommended':
                obj.set('recommended', 'true')
            elif value == 'required':
                obj.set('minOccurs', '1')
            else:
                obj.set('minOccurs', '0')
    else:
        raise ValueError('exists keyword found but value is None !')


def xml_handle_dimensions(obj, keyword, value):
    if value is not None:
        if isinstance(value, dict):
            if 'rank' in value and 'dim' in value:
                dims = ET.SubElement(obj, 'dimensions')
                dims.set('rank', str(value['rank']))
                for m in value['dim']:
                    if isinstance(m, list):
                        if len(m) >= 2:
                            dim = ET.SubElement(dims, 'dim')
                            dim.set('index', str(m[0]))
                            dim.set('value', str(m[1]))
                        if len(m) == 3:
                            if m[2] == 'optional':
                                dim.set('required', 'false')
                            else:
                                print('WARNING: ' + keyword + ' dimensions with len(3) list with non-optional argument, unexpected case !')
                    else:
                        raise ValueError('WARNING: ' + keyword + ' dimensions list item needs to have at least two members !')
            else:
                raise ValueError('exists keyword found, value is dict but has no keys rank and dim !')
        else:
            raise ValueError('exists keyword found but value is not a dictionary !')
    else:
        raise ValueError('exists keyword found but value is None !')


def xml_handle_enumeration(obj, keyword, value):
    enum = ET.SubElement(obj, 'enumeration')
    # assume we get a list as the value argument
    if value is not None:
        if isinstance(value, list):
            for m in value:
                itm = ET.SubElement(enum, 'item')
                itm.set('value', str(m))
        else:
            raise ValueError(keyword + ' we found an enumeration key-value pair but the value is not an ordinary Python list !')
    else:
        raise ValueError(keyword + ' we found an enumeration key-value pair but the value is None !')


def xml_handle_link(obj, keyword, value):
    """ 
    # if we have an NXDL link we decode the name attribute from <optional string>(link)[:-6]
    """
    if len(keyword[:-6]) >= 1 and isinstance(value, dict) and 'target' in value.keys():
        if isinstance(value['target'], str) and len(value['target']) >= 1:
            lnk = ET.SubElement(obj, 'link')
            lnk.set('name', keyword[:-6])
            lnk.set('target', value['target'])
        else:
            raise ValueError(keyword + ' value for target member of a link is invalid !')
    else:
        raise ValueError(keyword + ' the formatting of what seems to be a link is invalid in the yml file !')

def xml_handle_symbols(obj, value):
    """
    handle a set of NXDL symbols as a child to obj
    """
    syms = ET.SubElement(obj, 'symbols')
    if value is not None:
        if isinstance(value, dict):
            if 'doc' in value.keys():
                syms.set('doc', value['doc'])
                for kkeyword, vvalue in value.items():
                    assert vvalue is not None, 'Found an empty doc string while processing symbols table. Specify the doc string!'
                    assert isinstance(vvalue, str)
                    sym = ET.SubElement(syms, 'sym')
                    sym.set('name', kkeyword)
                    sym.set('doc', vvalue)


def recursive_build(obj, dct):
    """
    obj is the current node of the XML tree where we want to append to,
    dct is a dictionary object which represents the content of a child to obj
    dct may contain further dictionary nests, representing NXDL groups, which trigger recursive processing
    NXDL fields may contain attributes but trigger no recursion so attributes are leafs.
    """
    for keyword, value in iter(dct.items()):
        kName, kType = nx_name_type_resolving(keyword)
        print('kName: ' + kName + ' kType: ' + kType)
        if kName == '' and kType == '':
            raise ValueError('Found an improper YML key !')
        elif keyword[-6:] == '(link)': 
            xml_handle_link(obj, keyword, value)

        elif kType == '' and kName == 'symbols':
            #print(value.key(), type(value.key()), value.value(), type(value.value()))
            xml_handle_symbols(obj,value)

        elif (kType in nx_clss) or (kType not in nx_type_keys + ['']):
            # we can be sure we need to instantiate a new group
            grp = ET.SubElement(obj, 'group')
            if kName != '':  # use the custom name for the group
                grp.set('name', kName)
            grp.set('type', kType)
            if value is not None:
                if isinstance(value, dict):
                    if value != {}:
                        recursive_build(grp, value)
        elif kName[0:2] == nx_attr_idnt:  # check if obj qualifies as an attribute identifier
            attr = ET.SubElement(obj, 'attribute')
            attr.set('name', kName[2:])
            if value is not None:
                if isinstance(value, dict):
                    for kkeyword, vvalue in iter(value.items()):
                        if kkeyword == 'name':
                            attr.set('name', vvalue)
                        elif kkeyword == 'doc':
                            attr.set('doc', vvalue)
                        elif kkeyword == 'type':
                            attr.set('type', vvalue.upper())
                        elif kkeyword == 'enumeration':
                            xml_handle_enumeration(attr, kkeyword, vvalue)
                        else:
                            raise ValueError(kkeyword + ' facing an unknown situation while processing attributes of an attribute !')
        # handle special keywords (symbols), assumed that you do not encounter further symbols nested inside
        elif keyword == 'doc':
            xml_handle_docstring(obj, keyword, value)
        elif keyword == 'enumeration':
            xml_handle_enumeration(obj, keyword, value)
        elif keyword == 'dimensions':
            xml_handle_dimensions(obj, keyword, value)
        elif keyword == 'exists':
            xml_handle_exists(obj, keyword, value)
        elif kName != '':
            typ = 'NX_CHAR'
            if kType in nx_type_keys:
                typ = kType
            # assume type is NX_CHAR, a NeXus default assumption if in doubt
            fld = ET.SubElement(obj, 'field')
            fld.set('name', kName)
            fld.set('type', typ)
            if value is not None:  # a field may have subordinated attributes
                if isinstance(value, dict):
                    for kkeyword, vvalue in iter(value.items()):
                        if kkeyword[0:2] == nx_attr_idnt:
                            attr = ET.SubElement(fld, 'attribute')
                            # attributes may also come with an nx_type specifier which we need to decipher first
                            kkName, kkType = nx_name_type_resolving(kkeyword[2:])
                            attr.set('name', kkName)
                            typ = 'NX_CHAR'
                            if kkType in nx_type_keys:
                                typ = kkType
                            attr.set('type', typ)
                            if vvalue is not None:
                                if isinstance(vvalue, dict):
                                    for kkkeyword, vvvalue in iter(vvalue.items()):
                                        if kkkeyword == 'doc':
                                            attr.set('doc', vvvalue)
                                        elif kkkeyword == 'exists':
                                            xml_handle_exists(attr, kkkeyword, vvvalue)
                                        elif kkkeyword == 'enumeration':
                                            xml_handle_enumeration(attr, kkkeyword, vvvalue)
                                        else:
                                            raise ValueError(keyword + ' ' + kkeyword + ' ' + kkkeyword + ' attribute handling !')
                        elif kkeyword == 'doc':
                            fld.set('doc', str(vvalue))
                        elif kkeyword == nx_unit_idnt:
                            xml_handle_units(fld, kkeyword, vvalue)
                        elif kkeyword == 'exists':
                            xml_handle_exists(fld, kkeyword, vvalue)
                        elif kkeyword == 'dimensions':
                            xml_handle_dimensions(fld, kkeyword, vvalue)
                        elif kkeyword == 'enumeration':
                            xml_handle_enumeration(fld, kkeyword, vvalue)
                        elif kkeyword == 'link':
                            fld.set('link', '')
                        else:
                            raise ValueError(keyword + ' ' + kkeyword + ' faced unknown situation !')
            else:
                if keyword == 'doc':
                    xml_handle_docstring(fld, keyword, value)
                elif keyword == nx_unit_idnt:
                    xml_handle_units(fld, keyword, value)
                elif keyword[0:2] == nx_attr_idnt:  # attribute of a field
                    raise ValueError(keyword + ' unknown attribute of a field case coming from no dict !')
                elif keyword == 'exists':
                    xml_handle_exists(fld, keyword, value)
                elif keyword == 'dimensions':
                    raise ValueError(keyword + ' unknown dimensions of a field case coming from no dict !')
                else:
                    pass
        else:
            pass
