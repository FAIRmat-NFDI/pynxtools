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

# pylint: disable=E1101


import os
import sys
from io import StringIO
from typing import List

import xml.etree.ElementTree as ET
from xml.dom import minidom
import click

from nexusparser.tools.yaml2nxdl import yaml2nxdl_read_yml_file as read
from nexusparser.tools.yaml2nxdl import yaml2nxdl_recursive_build as recursive_build


def pretty_print_xml(xml_root, output_xml):
    """Print better human-readable idented and formatted xml file
using built-in libraries and add preceding XML processing instruction

    """
    dom = minidom.parseString(ET.tostring(
        xml_root, encoding='utf-8', method='xml'))
    sibling = dom.createProcessingInstruction(
        'xml-stylesheet', 'type="text/xsl" href="nxdlformat.xsl"')
    root = dom.firstChild
    dom.insertBefore(sibling, root)
    xml_string = dom.toprettyxml()
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)


def yaml2nxdl(input_file: str, verbose: bool):
    """Main of the yaml2nxdl converter, creates XML tree,
namespace and schema, then evaluates a dictionary
nest of groups recursively and fields or (their) attributes as childs of the groups

    """
    yml_appdef = read.yml_reader(input_file)

    if verbose:
        sys.stdout.write('input-file: ' + input_file)
        sys.stdout.write('application/base contains the following root-level entries:')
        sys.stdout.write(str(yml_appdef.keys()))
    xml_root = ET.Element(
        'definition', {
            'xmlns': 'http://definition.nexusformat.org/nxdl/3.1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    )
    assert 'category' in yml_appdef.keys(
    ), 'Required root-level keyword category is missing!'
    assert yml_appdef['category'] in ['application', 'base'], 'Only \
application and base are valid categories!'
    assert 'doc' in yml_appdef.keys(), 'Required root-level keyword doc is missing!'

    xml_root.set('extends', 'NXobject')
    xml_root.set('type', 'group')
    if yml_appdef['category'] == 'application':
        xml_root.set('category', 'application')
        del yml_appdef['category']
    else:
        xml_root.set('category', 'base')
        del yml_appdef['category']

    assert isinstance(yml_appdef['doc'], str) and yml_appdef['doc'] != '', 'Doc \
has to be a non-empty string!'
    doctag = ET.SubElement(xml_root, 'doc')
    doctag.text = yml_appdef['doc']
    del yml_appdef['doc']

    if 'symbols' in yml_appdef.keys():
        recursive_build.xml_handle_symbols(xml_root, yml_appdef['symbols'])
        del yml_appdef['symbols']

    assert len(yml_appdef.keys()) == 1, 'Accepting at most keywords: category, \
doc, symbols, and NX... at root-level!'
    keyword = list(yml_appdef.keys())[0]  # which is the only one
    assert (keyword[0:3] == '(NX' and keyword[-1:] == ')' and len(keyword) > 4), 'NX \
keyword has an invalid pattern, or is too short!'
    xml_root.set('name', keyword[1:-1])
    recursive_build.recursive_build(xml_root, yml_appdef[keyword], verbose)

    pretty_print_xml(xml_root, input_file.split(".", 1)[0] + '.nxdl.xml')
    if verbose:
        sys.stdout.write('Parsed YAML to NXDL successfully')


def handle_group_or_field(depth, node, file_out):
    """Handle all the possible attributes that come along a field or group

"""
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
    """Handle the dimension field

"""
    file_out.write(
        '{indent}{tag}:\n'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1]))
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
    """Handle the attributes parsed from the xml file

"""
    file_out.write(
        '{indent}{escapesymbol}{key}:\n'.format(
            indent=depth * '  ',
            escapesymbol=r'\@',
            key=node.attrib['name']))


def handle_enumeration(depth, node, file_out):
    """Handle the enumeration field parsed from the xml file

"""
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


def handle_not_root_level_doc(depth, node, file_out):
    """Handle docs field along the yaml file

"""
    file_out.write(
        '{indent}{tag}: "{text}"\n'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1],
            text=node.text.strip().replace('\"', '\'') if node.text else ''))


def get_node_parent_info(tree, node):
    """Return tuple of (parent, index) where:
        parent = node of parent within tree
        index = index of node under parent"""

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
        self.root_level_symbols = '{indent}{tag}: {text}'.format(
            indent=0 * '  ',
            tag=node.tag.split("}", 1)[1],
            text=node.text.strip() if node.text else '')
        depth += 1
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('doc'):
                self.symbol_list.append(
                    '{indent}{tag}: "{text}"'.format(
                        indent=1 * '  ',
                        tag=child.tag.split("}", 1)[1],
                        text=child.text.strip().replace('\"', '\'') if child.text else ''))
            elif tag == ('symbol'):
                self.symbol_list.append(
                    '{indent}{key}: "{value}"'.format(
                        indent=1 * '  ',
                        key=child.attrib['name'],
                        value=child.attrib['doc'] or ''))

    def handle_definition(self, node):
        """Handle definition group and its attributes

        """
        for item in node.attrib:
            if 'schemaLocation' not in item \
                    and 'name' not in item \
                    and 'extends' not in item \
                    and 'type' not in item:
                self.root_level_definition.append(
                    '{key}: {value}'.format(
                        key=item,
                        value=node.attrib[item] or ''))
        if 'name' in node.attrib.keys():
            self.root_level_definition.append(
                '({value}):'.format(
                    value=node.attrib['name'] or ''))

    def handle_root_level_doc(self, node):
        """Handle the documentation field found at root level

"""
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('doc'):
                self.root_level_doc = '{indent}{tag}: "{text}"'.format(
                    indent=0 * '  ',
                    tag=child.tag.split("}", 1)[1],
                    text=child.text.strip().replace('\"', '\'') if child.text else '')
                node.remove(child)

    def print_root_level_doc(self, file_out):
        """Print at the root level of YML file \
the general documentation field found in XML file

 """
        file_out.write(
            '{indent}{root_level_doc}\n'.format(
                indent=0 * '  ',
                root_level_doc=self.root_level_doc))
        self.root_level_doc = ''

    def print_root_level_info(self, depth, file_out):
        """Print at the root level of YML file \
the information stored as definition attributes in the XML file

"""
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

    def recursion_in_xml_tree(self, depth, node, output_yml, verbose):
        """Descend lower level in xml tree. If we are in the symbols branch, \
the recursive behaviour is not triggered as we already handled the symbols' childs
"""
        if self.jump_symbol_child is True:
            self.jump_symbol_child = False
        else:
            for child in list(node):
                Nxdl2yaml.xmlparse(self, output_yml, child, depth, verbose)

    def xmlparse(self, output_yml, node, depth, verbose):
        """Main of the nxdl2yaml converter.
It parses XML tree,
then prints recursively each level of the tree

    """
        if verbose:
            sys.stdout.write(str(depth))
            sys.stdout.write(str(node.attrib))
        with open(output_yml, "a") as file_out:
            tag = node.tag.split("}", 1)[1]
            if tag == ('definition'):
                self.found_definition = True
                Nxdl2yaml.handle_definition(self, node)
            if depth == 0 and not self.root_level_doc:
                Nxdl2yaml.handle_root_level_doc(self, node)
            if tag == ('doc') and depth != 1:
                handle_not_root_level_doc(depth, node, file_out)
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
                handle_group_or_field(depth, node, file_out)
            if tag == ('enumeration'):
                handle_enumeration(depth, node, file_out)
            if tag == ('attribute'):
                handle_attributes(depth, node, file_out)
            if tag == ('dimensions'):
                handle_dimension(depth, node, file_out)
        depth += 1
        # Write nested nodes
        Nxdl2yaml.recursion_in_xml_tree(self, depth, node, output_yml, verbose)


def print_yml(input_file, verbose):
    """Parse an XML file provided as input and print a YML file

"""
    output_yml = input_file[:-9] + '_parsed.yml'
    if os.path.isfile(output_yml):
        os.remove(output_yml)
    my_file = Nxdl2yaml([], [])
    depth = 0
    tree = ET.parse(input_file)
    my_file.xmlparse(output_yml, tree.getroot(), depth, verbose)


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


def append_yml(input_file, append_to_base, verbose):
    """Append to an existing Nexus base class new elements provided in YML input file \
and print both an XML and YML file of the extended base class.

"""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nexus_def_path = os.path.join(local_dir, '../../definitions')
    base_classes_list_files = os.listdir(
        os.path.join(nexus_def_path, 'base_classes'))
    assert [s for s in base_classes_list_files if append_to_base.strip() == s.strip('.nxdl.xml')], \
        'Your base class extension does not match any existing Nexus base classes'
    base_class = os.path.join(
        nexus_def_path + '/base_classes', append_to_base + '.nxdl.xml')
    tree = ET.parse(base_class)
    root = tree.getroot()
    # warning: tmp files are printed on disk and removed at the ends!!
    tmp_nxdl_xml = 'tmp.nxdl.xml'
    tmp_parsed_yml = 'tmp_parsed.yml'
    tmp_parsed_nxdl_xml = 'tmp_parsed.nxdl.xml'
    pretty_print_xml(root, tmp_nxdl_xml)
    print_yml(tmp_nxdl_xml, verbose)
    yaml2nxdl(tmp_parsed_yml, verbose)
    tree = ET.parse(tmp_parsed_nxdl_xml)
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
    root_no_duplicates = compare_niac_and_my(tree, tree2, verbose,
                                             '{http://definition.nexusformat.org/nxdl/3.1}group',
                                             root_no_duplicates)
    root_no_duplicates = compare_niac_and_my(tree, tree2, verbose,
                                             '{http://definition.nexusformat.org/nxdl/3.1}field',
                                             root_no_duplicates)
    pretty_print_xml(root_no_duplicates, f'{input_file.split(".", 1)[0]}'
                     f'_appended.nxdl.xml')
    print_yml(input_file.split(".", 1)[0] + '_appended.nxdl.xml', verbose)
    yaml2nxdl(input_file.split(".", 1)[0] + '_appended_parsed.yml', verbose)
    os.rename(f'{input_file.split(".", 1)[0]}_appended_parsed.yml',
              f'{input_file.split(".", 1)[0]}_appended.yml')
    os.rename(f'{input_file.split(".", 1)[0]}_appended_parsed.nxdl.xml',
              f'{input_file.split(".", 1)[0]}_appended.nxdl.xml')
    #os.remove(tmp_nxdl_xml)
    #os.remove(tmp_parsed_nxdl_xml)
    #os.remove(tmp_parsed_yml)


@click.command()
@click.option(
    '--input-file',
    help='The path to the XML or YAML input data file to read and create \
a YAML or XML file from, respectively.'
)
@click.option(
    '--append-to-base',
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
def launch_tool(input_file, verbose, append_to_base):
    """Main function that distiguishes the input file format and launches the tools.

"""
    if input_file.split(".", 1)[1] == ('yml' or 'yaml'):
        yaml2nxdl(input_file, verbose)
        if append_to_base:
            append_yml(input_file.split(".", 1)[0] + '.nxdl.xml', append_to_base, verbose)
        else:
            pass
    elif input_file.split(".", 1)[1] == ('nxdl.xml'):
        if not append_to_base:
            print_yml(input_file, verbose)
        else:
            append_yml(input_file, append_to_base, verbose)


if __name__ == '__main__':
    launch_tool().parse()  # pylint: disable=no-value-for-parameter
