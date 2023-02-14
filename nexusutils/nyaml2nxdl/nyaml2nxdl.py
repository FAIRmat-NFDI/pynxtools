#!/usr/bin/env python3
"""Main file of yaml2nxdl tool.
Users create NeXus instances by writing a YAML file
which details a hierarchy of data/metadata elements

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
import os
import sys
from typing import List

import xml.etree.ElementTree as ET
from xml.dom import minidom
import click

from nexusutils.dataconverter import helpers
from nexusutils.nyaml2nxdl import nyaml2nxdl_forward_tools
from nexusutils.nyaml2nxdl import nyaml2nxdl_backward_tools


def pretty_print_xml(xml_root, output_xml):
    """
    Print better human-readable indented and formatted xml file using
    built-in libraries and add preceding XML processing instruction
    """
    dom = minidom.parseString(ET.tostring(
        xml_root, encoding='utf-8', method='xml'))
    sibling = dom.createProcessingInstruction(
        'xml-stylesheet', 'type="text/xsl" href="nxdlformat.xsl"')
    root = dom.firstChild
    dom.insertBefore(sibling, root)
    xml_string = dom.toprettyxml(indent='    ', newl='\n')
    with open('tmp.xml', "w", encoding="utf-8") as file_tmp:
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
    schema, then evaluates a dictionary nest of groups recursively and
    fields or (their) attributes as childs of the groups
    """
    yml_appdef = nyaml2nxdl_forward_tools.yml_reader(input_file)

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

    if 'symbols' in yml_appdef.keys():
        nyaml2nxdl_forward_tools.xml_handle_symbols(yml_appdef,
                                                    xml_root,
                                                    'symbols',
                                                    yml_appdef['symbols'])
        del yml_appdef['symbols']

    assert isinstance(yml_appdef['doc'], str) and yml_appdef['doc'] != '', 'Doc \
has to be a non-empty string!'

    doctag = ET.SubElement(xml_root, 'doc')
    doctag.text = nyaml2nxdl_forward_tools.format_nxdl_doc(yml_appdef['doc'])

    del yml_appdef['doc']

    root_keys = 0
    for key in yml_appdef.keys():
        if '__line__' not in key:
            root_keys += 1

    assert root_keys == 1, 'Accepting at most keywords: category, \
doc, symbols, and NX... at root-level!'

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

    nyaml2nxdl_forward_tools.recursive_build(xml_root, yml_appdef[keyword], verbose)

    pretty_print_xml(xml_root, input_file.rsplit(".", 1)[0] + '.nxdl.xml')
    if verbose:
        sys.stdout.write('Parsed YAML to NXDL successfully\n')


def get_node_parent_info(tree, node):
    """
    Return tuple of (parent, index) where: parent = node of parent within tree
    index = index of node under parent
    """

    parent_map = {c: p for p in tree.iter() for c in p}
    parent = parent_map[node]
    return parent, list(parent).index(node)


class Nxdl2yaml():
    """Parse XML file and print a YML file

"""

    def __init__(
            self,
            symbol_list: List[str],
            root_level_definition: List[str],
            root_level_doc='',
            root_level_symbols=''):
        self.append_flag = True
        self.found_definition = False
        self.jump_symbol_child = False
        self.root_level_doc = root_level_doc
        self.root_level_symbols = root_level_symbols
        self.root_level_definition = root_level_definition
        self.symbol_list = symbol_list

    def handle_symbols(self, depth, node):
        """Handle symbols field and its childs

        """
        # pylint: disable=consider-using-f-string
        self.root_level_symbols = (
            f"{helpers.remove_namespace_from_tag(node.tag)}: "
            f"{node.text.strip() if node.text else ''}"
        )
        depth += 1
        for child in list(node):
            tag = helpers.remove_namespace_from_tag(child.tag)
            if tag == 'doc':
                self.symbol_list.append(nyaml2nxdl_backward_tools.handle_not_root_level_doc(depth,
                                                                                            text=child.text))
            elif tag == 'symbol':
                if 'doc' in child.attrib:
                    self.symbol_list.append(nyaml2nxdl_backward_tools.handle_not_root_level_doc(depth,
                                                                                                text=child.attrib['doc']))
                else:
                    for symbol_doc in list(child):
                        tag = helpers.remove_namespace_from_tag(symbol_doc.tag)
                        if tag == 'doc':
                            self.symbol_list.append(nyaml2nxdl_backward_tools.handle_not_root_level_doc(depth,
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

        for child in list(node):
            tag = helpers.remove_namespace_from_tag(child.tag)
            if tag == ('doc'):
                self.root_level_doc = '{indent}{tag}: | {text}\n'.format(
                    indent=0 * '  ',
                    tag=helpers.remove_namespace_from_tag(child.tag),
                    text='\n' + '  ' + '\n'.join([f"{1 * '  '}{s.lstrip()}"
                                                  for s in child.text.split('\n')]
                                                 if child.text else '').strip())
                node.remove(child)

    def print_root_level_doc(self, file_out):
        """
        Print at the root level of YML file \
        the general documentation field found in XML file
        """
        # pylint: disable=consider-using-f-string
        file_out.write(
            '{indent}{root_level_doc}'.format(
                indent=0 * '  ',
                root_level_doc=self.root_level_doc))
        self.root_level_doc = ''

    def print_root_level_info(self, depth, file_out):
        """
        Print at the root level of YML file \
        the information stored as definition attributes in the XML file
        """
        # pylint: disable=consider-using-f-string
        if depth > 0 \
                and [s for s in self.root_level_definition if "category: application" in s]\
                or depth == 1 \
                and [s for s in self.root_level_definition if "category: base" in s]:
            if self.root_level_symbols:
                file_out.write(
                    '{indent}{root_level_symbols}\n'.format(
                        indent=0 * '  ',
                        root_level_symbols=self.root_level_symbols))
                for symbol in self.symbol_list:
                    file_out.write(
                        '{indent}{symbol}\n'.format(
                            indent=0 * '  ',
                            symbol=symbol))
            if self.root_level_definition:
                for defs in self.root_level_definition:
                    file_out.write(
                        '{indent}{defs}\n'.format(
                            indent=0 * '  ',
                            defs=defs))
            self.found_definition = False

    def recursion_in_xml_tree(self, depth, xml_tree, output_yml, verbose):
        """Descend lower level in xml tree. If we are in the symbols branch, \
the recursive behaviour is not triggered as we already handled the symbols' childs
"""
        tree = xml_tree['tree']
        node = xml_tree['node']
        if self.jump_symbol_child is True:
            self.jump_symbol_child = False
        else:
            for child in list(node):
                xml_tree_children = {'tree': tree, 'node': child}
                Nxdl2yaml.xmlparse(self, output_yml, xml_tree_children, depth, verbose)

    def xmlparse(self, output_yml, xml_tree, depth, verbose):
        """Main of the nxdl2yaml converter.
It parses XML tree,
then prints recursively each level of the tree

    """
        tree = xml_tree['tree']
        node = xml_tree['node']

        if verbose:
            sys.stdout.write(f'Node tag: {helpers.remove_namespace_from_tag(node.tag)}\n')
            sys.stdout.write(f'Attributes: {node.attrib}\n')
        with open(output_yml, "a", encoding="utf-8") as file_out:
            tag = helpers.remove_namespace_from_tag(node.tag)
            if tag == ('definition'):
                self.found_definition = True
                Nxdl2yaml.handle_definition(self, node)
            if depth == 0 and not self.root_level_doc:
                Nxdl2yaml.handle_root_level_doc(self, node)
            if tag == ('doc') and depth != 1:
                parent = get_node_parent_info(tree, node)[0]
                doc_parent = helpers.remove_namespace_from_tag(parent.tag)
                if doc_parent != 'item':
                    nyaml2nxdl_backward_tools.handle_not_root_level_doc(depth, node.text,
                                                                        tag=node.tag,
                                                                        file_out=file_out )
            if tag == ('symbols'):
                Nxdl2yaml.handle_symbols(self, depth, node)
                self.jump_symbol_child = True
            # End of root level definition parsing. Print root-level definitions in file
            if self.root_level_doc \
                    and self.append_flag is True \
                    and (depth in (0, 1)):
                Nxdl2yaml.print_root_level_doc(self, file_out)
            if self.found_definition is True and self.append_flag is True:
                Nxdl2yaml.print_root_level_info(self, depth, file_out)
            # End of print root-level definitions in file
            if tag in ('field', 'group') and depth != 0:
                nyaml2nxdl_backward_tools.handle_group_or_field(depth, node, file_out)
            if tag == ('enumeration'):
                nyaml2nxdl_backward_tools.handle_enumeration(depth, node, file_out)
            if tag == ('attribute'):
                nyaml2nxdl_backward_tools.handle_attributes(depth, node, file_out)
            if tag == ('dimensions'):
                nyaml2nxdl_backward_tools.handle_dimension(depth, node, file_out)
        depth += 1
        # Write nested nodes
        Nxdl2yaml.recursion_in_xml_tree(self, depth, xml_tree, output_yml, verbose)


def print_yml(input_file, verbose):
    """Parse an XML file provided as input and print a YML file

"""
    output_yml = input_file[:-9] + '_parsed.yaml'
    if os.path.isfile(output_yml):
        os.remove(output_yml)
    my_file = Nxdl2yaml([], [])
    depth = 0
    tree = ET.parse(input_file)
    xml_tree = {'tree': tree.getroot(), 'node': tree.getroot()}
    my_file.xmlparse(output_yml, xml_tree, depth, verbose)


def append_yml(input_file, append, verbose):
    """Append to an existing NeXus base class new elements provided in YML input file \
and print both an XML and YML file of the extended base class.

"""
    nexus_def_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../definitions')
    assert [s for s in os.listdir(os.path.join(nexus_def_path, 'base_classes')
                                  ) if append.strip() == s.replace('.nxdl.xml', '')], \
        'Your base class extension does not match any existing NeXus base classes'
    tree = ET.parse(os.path.join(nexus_def_path + '/base_classes', append + '.nxdl.xml'))
    root = tree.getroot()
    # warning: tmp files are printed on disk and removed at the ends!!
    pretty_print_xml(root, 'tmp.nxdl.xml')
    print_yml('tmp.nxdl.xml', verbose)
    nyaml2nxdl('tmp_parsed.yaml', verbose)
    tree = ET.parse('tmp_parsed.nxdl.xml')
    tree2 = ET.parse(input_file)
    root_no_duplicates = ET.Element(
        'definition', {'xmlns': 'http://definition.nexusformat.org/nxdl/3.1',
                       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xsi:schemaLocation': 'http://www.w3.org/2001/XMLSchema-instance'
                       }
    )
    for attribute_keys in root.attrib.keys():
        if attribute_keys != '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
            attribute_value = root.attrib[attribute_keys]
            root_no_duplicates.set(attribute_keys, attribute_value)
    for elems in root.iter():
        if 'doc' in elems.tag:
            root_doc = ET.SubElement(root_no_duplicates, 'doc')
            root_doc.text = elems.text
            break
    group = '{http://definition.nexusformat.org/nxdl/3.1}group'
    root_no_duplicates = nyaml2nxdl_backward_tools.compare_niac_and_my(tree, tree2, verbose,
                                                                       group,
                                                                       root_no_duplicates)
    field = '{http://definition.nexusformat.org/nxdl/3.1}field'
    root_no_duplicates = nyaml2nxdl_backward_tools.compare_niac_and_my(tree, tree2, verbose,
                                                                       field,
                                                                       root_no_duplicates)
    attribute = '{http://definition.nexusformat.org/nxdl/3.1}attribute'
    root_no_duplicates = nyaml2nxdl_backward_tools.compare_niac_and_my(tree, tree2, verbose,
                                                                       attribute,
                                                                       root_no_duplicates)
    pretty_print_xml(root_no_duplicates, f"{input_file.replace('.nxdl.xml', '')}"
                     f"_appended.nxdl.xml")
    print_yml(input_file.replace('.nxdl.xml', '') + "_appended.nxdl.xml", verbose)
    nyaml2nxdl(input_file.replace('.nxdl.xml', '') + "_appended_parsed.yaml", verbose)
    os.rename(f"{input_file.replace('.nxdl.xml', '')}_appended_parsed.yaml",
              f"{input_file.replace('.nxdl.xml', '')}_appended.yaml")
    os.rename(f"{input_file.replace('.nxdl.xml', '')}_appended_parsed.nxdl.xml",
              f"{input_file.replace('.nxdl.xml', '')}_appended.nxdl.xml")
    os.remove('tmp.nxdl.xml')
    os.remove('tmp_parsed.yaml')
    os.remove('tmp_parsed.nxdl.xml')


@click.command()
@click.option(
    '--input-file',
    required=True,
    help='The path to the XML or YAML input data file to read and create \
a YAML or XML file from, respectively.'
)
@click.option(
    '--append',
    help='Parse xml file and append to base class, given that the xml file has same name \
of an existing base class'
)
@click.option(
    '--verbose',
    is_flag=True,
    default=False,
    help='Print in standard output keywords and value types to help \
possible issues in yaml files'
)
def launch_tool(input_file, verbose, append):
    """
    Main function that distiguishes the input file format and launches the tools.
    """
    if input_file.rsplit(".", 1)[1] in ('yml', 'yaml'):
        nyaml2nxdl(input_file, verbose)
        if append:
            append_yml(input_file.rsplit(".", 1)[0] + '.nxdl.xml',
                       append,
                       verbose
                       )
        else:
            pass
    elif input_file.rsplit(".", 2)[1] == 'nxdl':
        if not append:
            print_yml(input_file, verbose)
        else:
            append_yml(input_file, append, verbose)


if __name__ == '__main__':
    launch_tool().parse()  # pylint: disable=no-value-for-parameter
