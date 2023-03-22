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

import xml.etree.ElementTree as ET
import click

from nexusutils.nyaml2nxdl.nyaml2nxdl_forward_tools import nyaml2nxdl, pretty_print_xml
from nexusutils.nyaml2nxdl.nyaml2nxdl_backward_tools import (Nxdl2yaml,
                                                             compare_niac_and_my)


DEPTH_SIZE = "    "


def print_yml(input_file, verbose):
    """
        Parse an XML file provided as input and print a YML file
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
    root_no_duplicates = compare_niac_and_my(tree, tree2, verbose,
                                             group,
                                             root_no_duplicates)
    field = '{http://definition.nexusformat.org/nxdl/3.1}field'
    root_no_duplicates = compare_niac_and_my(tree, tree2, verbose,
                                             field,
                                             root_no_duplicates)
    attribute = '{http://definition.nexusformat.org/nxdl/3.1}attribute'
    root_no_duplicates = compare_niac_and_my(tree, tree2, verbose,
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
