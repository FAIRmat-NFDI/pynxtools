#!/usr/bin/env python3
"""
# Main file of yaml2nxdl tool. \
# Users create NeXus instances by writing a YAML file \
# which details a hierarchy of data/metadata elements
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

import xml.etree.ElementTree as ET
from xml.dom import minidom
import click

from nexusparser.tools.yaml2nxdl import yaml2nxdl_read_yml_file as read
from nexusparser.tools.yaml2nxdl import yaml2nxdl_recursive_build as recursive_build


def pretty_print_xml(xml_root, output_xml):
    """
    # Print better human-readable idented and formatted xml file
    # using built-in libraries and add preceding XML processing instruction
    """
    dom = minidom.parseString(ET.tostring(xml_root, encoding="UTF-8", method="xml"))
    sibling = dom.createProcessingInstruction(
        'xml-stylesheet', 'type="text/xsl" href="nxdlformat.xslt"')
    root = dom.firstChild
    dom.insertBefore(sibling, root)
    xml_string = dom.toprettyxml()
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)


@click.command()
@click.option(
    '--input-file',
    help='The path to the yaml-formatted input data file to read and create \
        a NXDL XML file from. (Repeat for more than one file.)'
)
def yaml2nxdl(input_file: str):
    """
    main of the yaml2nxdl converter, creates XML tree, \
    namespace and schema, then evaluates a dictionary
    nest of groups recursively and fields or (their) attributes as childs of the groups
    """
    yml_appdef = read.yml_reader(input_file)

    print('input-file: ' + input_file)
    print('application/base contains the following root-level entries:')
    print(list(yml_appdef.keys()))
    xml_root = ET.Element(
        'definition', {
            'xmlns': 'http://definition.nexusformat.org/nxdl/3.1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    )

    assert 'category' in yml_appdef.keys(), 'Required root-level keyword category is missing!'
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

    recursive_build.recursive_build(xml_root, yml_appdef[keyword])

    pretty_print_xml(xml_root, input_file[:-4] + '.nxdl.xml')
    print('Parsed YAML to NXDL successfully')


if __name__ == '__main__':
    yaml2nxdl().parse()  # pylint: disable=no-value-for-parameter
