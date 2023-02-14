#!/usr/bin/env python3
"""This file collects the function used in the reverse tool nxdl2yaml.

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
from nexusutils.dataconverter import helpers


def handle_not_root_level_doc(depth, text, tag='doc', file_out=None):
    """
    Handle docs field along the yaml file
    """
    # pylint: disable=consider-using-f-string
    if "\n" in text:
        text = '\n' + (depth + 1) * '  ' + '\n'.join([f"{(depth + 1) * '  '}{s.lstrip()}"
                                                            for s in text.split('\n')]
                                                           ).strip()
        if "}" in tag:
            tag = helpers.remove_namespace_from_tag(tag)
        indent = depth * '  '
    elif text:
        text = '\n' + (depth + 1) * '  ' + text.strip()
        if "}" in tag:
            tag = helpers.remove_namespace_from_tag(tag)
        indent = depth * '  '
    else:
        text = ""
        if "}" in tag:
            tag = helpers.remove_namespace_from_tag(tag)
        indent = depth * '  '


    doc_str = f"{indent}{tag}: |{text}\n"
    if file_out:
        file_out.write(doc_str)
    else:
        return doc_str


def handle_group_or_field(depth, node, file_out):
    """Handle all the possible attributes that come along a field or group"""
    # pylint: disable=consider-using-f-string
    if "name" in node.attrib and "type" in node.attrib:
        file_out.write(
            '{indent}{name}({value1}):\n'.format(
                indent=depth * '  ',
                name=node.attrib['name'] or '',
                value1=node.attrib['type'] or ''))
    if "name" in node.attrib and "type" not in node.attrib:
        file_out.write(
            '{indent}{name}:\n'.format(
                indent=depth * '  ',
                name=node.attrib['name'] or ''))
    if "name" not in node.attrib and "type" in node.attrib:
        file_out.write(
            '{indent}({type}):\n'.format(
                indent=depth * '  ',
                type=node.attrib['type'] or ''))
    if "minOccurs" in node.attrib and "maxOccurs" in node.attrib:
        file_out.write(
            '{indent}exists: [min, {value1}, max, {value2}]\n'.format(
                indent=(depth + 1) * '  ',
                value1=node.attrib['minOccurs'] or '',
                value2=node.attrib['maxOccurs'] or ''))
    if "minOccurs" in node.attrib \
            and "maxOccurs" not in node.attrib \
            and node.attrib['minOccurs'] == "1":
        file_out.write(
            '{indent}{name}: required \n'.format(
                indent=(depth + 1) * '  ',
                name='exists'))
    if "recommended" in node.attrib and node.attrib['recommended'] == "true":
        file_out.write(
            '{indent}exists: recommended\n'.format(
                indent=(depth + 1) * '  '))
    if "units" in node.attrib:
        file_out.write(
            '{indent}unit: {value}\n'.format(
                indent=(depth + 1) * '  ',
                value=node.attrib['units'] or ''))


def handle_dimension(depth, node, file_out):
    """Handle the dimension field"""
    # pylint: disable=consider-using-f-string

    file_out.write(
        '{indent}{tag}:\n'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1]))
    if 'rank' in node.attrib:
        file_out.write(
            '{indent}rank: {rank}\n'.format(
                indent=(depth + 1) * '  ',
                rank=node.attrib['rank']))
    dim_list = ''
    for child in list(node):
        tag = child.tag.split("}", 1)[1]
        if tag == ('dim'):
            dim_list = dim_list + '[{index}, {value}], '.format(
                index=child.attrib['index'],
                value=child.attrib['value'])
    file_out.write(
        '{indent}dim: [{value}]\n'.format(
            indent=(depth + 1) * '  ',
            value=dim_list[:-2] or ''))


def handle_attributes(depth, node, file_out):
    """Handle the attributes parsed from the xml file"""
    # pylint: disable=consider-using-f-string

    file_out.write(
        '{indent}{escapesymbol}{key}:\n'.format(
            indent=depth * '  ',
            escapesymbol=r'\@',
            key=node.attrib['name']))


def handle_enumeration(depth, node, file_out):
    """Handle the enumeration field parsed from the xml file.

If the enumeration items contain a doc field, the yaml file will contain items as child
fields of the enumeration field.

If no doc are inherited in the enumeration items, a list of the items is given for the
enumeration list.

"""
    # pylint: disable=consider-using-f-string

    check_doc = []
    for child in list(node):
        if list(child):
            check_doc.append(list(child))
    if check_doc:
        file_out.write(
            '{indent}{tag}: \n'.format(
                indent=depth * '  ',
                tag=node.tag.split("}", 1)[1]))
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('item'):
                file_out.write(
                    '{indent}{value}: \n'.format(
                        indent=(depth + 1) * '  ',
                        value=child.attrib['value']))
                if list(child):
                    for item_doc in list(child):
                        item_doc_depth = depth + 2
                        handle_not_root_level_doc(item_doc_depth, item_doc.text,
                                                  item_doc.tag, file_out)
    else:
        file_out.write(
            '{indent}{tag}:'.format(
                indent=depth * '  ',
                tag=node.tag.split("}", 1)[1]))
        enum_list = ''
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('item'):
                enum_list = enum_list + '{value}, '.format(
                    value=child.attrib['value'])
        file_out.write(
            ' [{enum_list}]\n'.format(
                enum_list=enum_list[:-2] or ''))


def get_node_parent_info(tree, node):
    """Return tuple of (parent, index) where:
        parent = node of parent within tree
        index = index of node under parent"""

    parent_map = {c: p for p in tree.iter() for c in p}
    parent = parent_map[node]
    return parent, list(parent).index(node)


def compare_niac_and_my(tree, tree2, verbose, node, root_no_duplicates):
    """This function creates two trees with Niac XML file and My XML file.
The main aim is to compare the two trees and create a new one that is the
union of the two initial trees.

"""
    root = tree.getroot()
    root2 = tree2.getroot()
    attrs_list_niac = []
    for nodo in root.iter(node):
        attrs_list_niac.append(nodo.attrib)
    if verbose:
        sys.stdout.write('Attributes found in Niac file: \n')
        sys.stdout.write(str(attrs_list_niac) + '\n')
        sys.stdout.write('  \n')
        sys.stdout.write('Started merging of Niac and My file... \n')
    for elem in root.iter(node):
        if verbose:
            sys.stdout.write('- Niac element inserted: \n')
            sys.stdout.write(str(elem.attrib) + '\n')
        index = get_node_parent_info(tree, elem)[1]
        root_no_duplicates.insert(index, elem)

    for elem2 in root2.iter(node):
        index = get_node_parent_info(tree2, elem2)[1]
        if elem2.attrib not in attrs_list_niac:
            if verbose:
                sys.stdout.write('- My element inserted: \n')
                sys.stdout.write(str(elem2.attrib) + '\n')
            root_no_duplicates.insert(index, elem2)

    if verbose:
        sys.stdout.write('     \n')
    return root_no_duplicates
