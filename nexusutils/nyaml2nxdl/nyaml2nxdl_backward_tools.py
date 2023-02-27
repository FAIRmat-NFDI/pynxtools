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
from nexusutils.dataconverter.helpers import remove_namespace_from_tag
from typing import List


OPSSIBLE_DIM_ATTRS = ['dim', 'ref', 'optional', 'recommended']
OPSSIBLE_DIMENSION_ATTRS = ['rank', 'doc']
DEPTH_SIZE = "  "


class Nxdl2yaml():
    """
        Parse XML file and print a YML file
    """

    def __init__(
            self,
            symbol_list: List[str],
            root_level_definition: List[str],
            root_level_doc='',
            root_level_symbols=''):

        # updated part of yaml_dict
        self.append_flag = True
        self.found_definition = False
        self.root_level_doc = root_level_doc
        self.root_level_symbols = root_level_symbols
        self.root_level_definition = root_level_definition
        self.symbol_list = symbol_list

    def handle_symbols(self, depth, node):
        """Handle symbols field and its childs

        """
        # pylint: disable=consider-using-f-string
        self.root_level_symbols = (
            f"{remove_namespace_from_tag(node.tag)}: "
            f"{node.text.strip() if node.text else ''}"
        )
        depth += 1
        for child in list(node):
            tag = remove_namespace_from_tag(child.tag)
            if tag == 'doc':
                self.symbol_list.append(self.handle_not_root_level_doc(depth,
                                                                  text=child.text))
            elif tag == 'symbol':
                if 'doc' in child.attrib:
                    self.symbol_list.append(self.handle_not_root_level_doc(depth,
                                                                      tag=child.attrib['name'],
                                                                      text=child.attrib['doc']))
                else:
                    for symbol_doc in list(child):
                        tag = remove_namespace_from_tag(symbol_doc.tag)
                        if tag == 'doc':
                            self.symbol_list.append(self.handle_not_root_level_doc(depth,
                                                                              tag=child.attrib['name'],
                                                                              text=symbol_doc.text))

    def handle_definition(self, node):
        """Handle definition group and its attributes

        """
        # pylint: disable=consider-using-f-string
        attribs = node.attrib
        for item in attribs:
            if 'schemaLocation' not in item \
                    and 'name' not in item \
                    and 'extends' not in item \
                    and 'type' not in item:
                self.root_level_definition.append(
                    '{key}: {value}'.format(
                        key=item,
                        value=attribs[item] or ''))
        if 'name' in attribs.keys():
            self.root_level_definition.append(
                '{name}:'.format(
                    name=attribs['name'] or ''))
            if 'extends' in attribs.keys() and attribs["extends"] != "NXobject":
                keyword = self.root_level_definition.pop()
                self.root_level_definition.append(f"{keyword[0:-1]}({attribs['extends']}):")

    def handle_root_level_doc(self, node):
        """Handle the documentation field found at root level"""
        # pylint: disable=consider-using-f-string

        tag = remove_namespace_from_tag(node.tag)
        if tag == ('doc'):
            self.root_level_doc = '{indent}{tag}: | {text}'.format(
                indent=0 * DEPTH_SIZE,
                tag=remove_namespace_from_tag(node.tag),
                text='\n' + DEPTH_SIZE + '\n'.join([f"{1 * DEPTH_SIZE}{s.lstrip()}"
                                                for s in node.text.split('\n')]
                                                if node.text else '').strip())

    def handle_not_root_level_doc(self, depth, text, tag='doc', file_out=None):
        """
        Handle docs field along the yaml file
        """
        # pylint: disable=consider-using-f-string
        if "\n" in text:
            text = '\n' + (depth + 1) * DEPTH_SIZE + '\n'.join([f"{(depth + 1) * DEPTH_SIZE}{s.lstrip()}"
                                                        for s in text.split('\n')]).strip()
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE
        elif text:
            text = '\n' + (depth + 1) * DEPTH_SIZE + text.strip()
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE
        else:
            text = ""
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE

        doc_str = f"{indent}{tag}: | {text}\n"
        if file_out:
            file_out.write(doc_str)
        else:
            return doc_str

    def print_root_level_doc(self, file_out):
        """
        Print at the root level of YML file \
        the general documentation field found in XML file
        """
        # pylint: disable=consider-using-f-string
        file_out.write(
            '{indent}{root_level_doc}\n'.format(
                indent=0 * DEPTH_SIZE,
                root_level_doc=self.root_level_doc))
        self.root_level_doc = ''

    def print_root_level_info(self, depth, file_out):
        """
        Print at the root level of YML file \
        the information stored as definition attributes in the XML file
        """
        # pylint: disable=consider-using-f-string
        if depth >= 0 \
                and ([s for s in self.root_level_definition if "category: application" in s]\
                or [s for s in self.root_level_definition if "category: base" in s]):
            if self.root_level_symbols:
                file_out.write(
                    '{indent}{root_level_symbols}\n'.format(
                        indent=0 * DEPTH_SIZE,
                        root_level_symbols=self.root_level_symbols))
                for symbol in self.symbol_list:
                    file_out.write(
                        '{indent}{symbol}\n'.format(
                            indent=0 * DEPTH_SIZE,
                            symbol=symbol))
            if self.root_level_definition:
                for defs in self.root_level_definition:
                    file_out.write(
                        '{indent}{defs}\n'.format(
                            indent=0 * DEPTH_SIZE,
                            defs=defs))
            self.found_definition = False

    def handle_group_or_field(self, depth, node, file_out):
        """Handle all the possible attributes that come along a field or group"""

        def type_check(type):
            if type == 'NX_CHAR':
                type = ''
            else:
                type = f"({type})"
            return type

        node_attr = node.attrib
        # pylint: disable=consider-using-f-string
        if "name" in node_attr and "type" in node_attr:
            file_out.write(
                '{indent}{name}{type}:\n'.format(
                    indent=depth * DEPTH_SIZE,
                    name=node_attr['name'] or '',
                    type=type_check(node_attr['type'])))

        if "name" in node_attr and "type" not in node_attr:
            file_out.write(
                '{indent}{name}:\n'.format(
                    indent=depth * DEPTH_SIZE,
                    name=node_attr['name'] or ''))

        if "name" not in node_attr and "type" in node_attr:
            file_out.write(
                '{indent}{type}:\n'.format(
                    indent=depth * DEPTH_SIZE,
                    type=type_check(node_attr['type'])))

        if "minOccurs" in node_attr and "maxOccurs" in node_attr:
            file_out.write(
                '{indent}exists: [min, {value1}, max, {value2}]\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE,
                    value1=node_attr['minOccurs'] or '',
                    value2=node_attr['maxOccurs'] or ''))
        elif "minOccurs" in node_attr \
                and "maxOccurs" not in node_attr \
                and node_attr['minOccurs'] == "1":
            file_out.write(
                '{indent}{name}: required \n'.format(
                    indent=(depth + 1) * DEPTH_SIZE,
                    name='exists'))
        elif "maxOccurs" in node_attr:
            file_out.write(
                '{indent}exists: [max, {value1}]\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE,
                    value1=node_attr['maxOccurs'] or ''))

        if "recommended" in node_attr and node_attr['recommended'] == "true":
            file_out.write(
                '{indent}exists: recommended\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE))
        if 'nameType' in node_attr:
            file_out.write(
                '{indent}nameType: {value}\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE,
                    value=node_attr['nameType'] or '')
                    )
        if "units" in node_attr:
            file_out.write(
                '{indent}unit: {value}\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE,
                    value=node_attr['units'] or ''))

    # TODO make code radable by moving rank in a rank variable
    def handle_dimension(self, depth, node, file_out):
        """Handle the dimension field"""
        # pylint: disable=consider-using-f-string

        file_out.write(
            '{indent}{tag}:\n'.format(
                indent=depth * DEPTH_SIZE,
                tag=node.tag.split("}", 1)[1]))

        node_attrs = node.attrib
        for attr, value in node_attrs.items():
            indent = (depth + 1) * DEPTH_SIZE
            file_out.write(f'{indent}{attr}: {value}\n')
        dim_index_value = ''
        dim_other_attr = {}
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            child_attrs = child.attrib
            if tag == ('dim'):
                # taking care of index and value in format [[index, value]]
                dim_index_value = dim_index_value + '[{index}, {value}], '.format(
                    index=child_attrs['index'] if "index" in child_attrs else '',
                    value=child_attrs['value'] if "value" in child_attrs else '')
                if "index" in child_attrs:
                    del child_attrs["index"]
                if "value" in child_attrs:
                    del child_attrs["value"]
            indent = (depth +1) * DEPTH_SIZE
            for attr, value in child_attrs.items():
                if attr in OPSSIBLE_DIM_ATTRS:
                    if attr not in dim_other_attr:
                        dim_other_attr[attr] = []
                    dim_other_attr[attr] = dim_other_attr[attr].append(value)

        # index and value attributes of dim elements
        file_out.write(
            '{indent}dim: [{value}]\n'.format(
                indent=(depth + 1) * DEPTH_SIZE,
                value=dim_index_value[:-2] or ''))
        # other attributes, except index and vale and doc of dim and write as child of dim
        # doc or attributes for each dim come in list
        indent = depth + 2
        for key, value in dim_other_attr.items():
            file_out.write(f"{indent}{key}: {value}\n")

    def handle_enumeration(self, depth, node, file_out):
        """
            Handle the enumeration field parsed from the xml file.

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
                    indent=depth * DEPTH_SIZE,
                    tag=node.tag.split("}", 1)[1]))
            for child in list(node):
                tag = child.tag.split("}", 1)[1]
                if tag == ('item'):
                    file_out.write(
                        '{indent}{value}: \n'.format(
                            indent=(depth + 1) * DEPTH_SIZE,
                            value=child.attrib['value']))
                    if list(child):
                        for item_doc in list(child):
                            item_doc_depth = depth + 2
                            self.handle_not_root_level_doc(item_doc_depth, item_doc.text,
                                                    item_doc.tag, file_out)
        else:
            file_out.write(
                '{indent}{tag}:'.format(
                    indent=depth * DEPTH_SIZE,
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

    def handle_attributes(self, depth, node, file_out):
        """Handle the attributes parsed from the xml file"""
        # pylint: disable=consider-using-f-string

        file_out.write(
            '{indent}{escapesymbol}{key}:\n'.format(
                indent=depth * DEPTH_SIZE,
                escapesymbol=r'\@',
                key=node.attrib['name']))

    def recursion_in_xml_tree(self, depth, xml_tree, output_yml, verbose):
        """
            Descend lower level in xml tree. If we are in the symbols branch, the recursive
        behaviour is not triggered as we already handled the symbols' childs.
        """

        tree = xml_tree['tree']
        node = xml_tree['node']
        for child in list(node):
            xml_tree_children = {'tree': tree, 'node': child}
            self.xmlparse(output_yml, xml_tree_children, depth, verbose)

    def xmlparse(self, output_yml, xml_tree, depth, verbose):
        """
        Main of the nxdl2yaml converter.
        It parses XML tree, then prints recursively each level of the tree
        """
        tree = xml_tree['tree']
        node = xml_tree['node']
        # TODO remove Nxdl2yaml with self object
        if verbose:
            sys.stdout.write(f'Node tag: {remove_namespace_from_tag(node.tag)}\n')
            sys.stdout.write(f'Attributes: {node.attrib}\n')
        with open(output_yml, "a", encoding="utf-8") as file_out:
            tag = remove_namespace_from_tag(node.tag)
            if tag == ('definition'):
                self.found_definition = True
                self.handle_definition( node)
                for child in list(node):
                    tag_tmp = remove_namespace_from_tag(child.tag)
                    if tag_tmp == 'doc':
                        self.handle_root_level_doc(child)
                        node.remove(child)
                    if tag_tmp == 'symbols':
                        self.handle_symbols(depth, child)
                        node.remove(child)

            if tag == ('doc') and depth != 1:
                parent = get_node_parent_info(tree, node)[0]
                doc_parent = remove_namespace_from_tag(parent.tag)
                if doc_parent != 'item':
                    self.handle_not_root_level_doc(depth, text=node.text,
                                              tag=node.tag,
                                              file_out=file_out)
            # End of root level definition parsing. Print root-level definitions in file
            # TODO: remove unecessary append_flag
            if self.root_level_doc \
                    and self.append_flag is True \
                    and (depth in (0, 1)):
                self.print_root_level_doc(file_out)
            if self.found_definition is True and self.append_flag is True:
                self.print_root_level_info(depth, file_out)
            # End of print root-level definitions in file
            if tag in ('field', 'group') and depth != 0:
                self.handle_group_or_field(depth, node, file_out)
            if tag == ('enumeration'):
                self.handle_enumeration(depth, node, file_out)
            if tag == ('attribute'):
                self.handle_attributes(depth, node, file_out)
            if tag == ('dimensions'):
                self.handle_dimension(depth, node, file_out)
        depth += 1
        # Write nested nodes
        self.recursion_in_xml_tree(depth, xml_tree, output_yml, verbose)


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
