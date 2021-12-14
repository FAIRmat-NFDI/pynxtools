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
from xml.dom import minidom
from yaml2nxdl_utils import nx_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt
from yaml2nxdl_read_yml_appdef import read_application_definition
from yaml2nxdl_recursive_build import recursive_build
import subprocess
import click

#import NEXUS definitions, i.e. NIAC-approved application definitions, base and contributed classes
try:
    #either given by sys env
    nexusDefPath = os.environ['NEXUS_DEF_PATH']
except:
    #or it should be available locally under the dir 'definitions'
    localDir=os.path.abspath(os.path.dirname(__file__))
    nexusDefPath=os.path.join(localDir,'definitions')
    if not os.path.exists(nexusDefPath):
        #check the definitions out if it has not been done yet
        cwd=os.getcwd()
        os.chdir(localDir)
        subprocess.call(['git','clone','https://github.com/nexusformat/definitions'])
        os.chdir(cwd)

def pretty_print_xml(xml_root, output_xml):
    """
    Print better human-readable idented and formatted xml file using built-in libraries and add preceding XML processing instruction
    """
    # lack of "xml_declaration" for python<=3.7
    try:
        dom = minidom.parseString(ET.tostring(
        xml_root, encoding = "UTF-8", xml_declaration = True, method = "xml"))
    except TypeError:
        dom = minidom.parseString(ET.tostring(
        xml_root, encoding = "UTF-8", method = "xml"))
    pi = dom.createProcessingInstruction('xml-stylesheet',
    'type="text/xsl" href="nxdlformat.xslt"')
    root = dom.firstChild
    dom.insertBefore(pi, root)
    xml_string = dom.toprettyxml()
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)


@click.command()
@click.option(
    '--input-file',
    help='The path to the yaml-formatted input data file to read and create a NXDL XML file from. (Repeat for more than one file.)'
)
def yaml2nxdl(input_file: str):
    """
    main of the yaml2nxdl converter, creates XML tree, namespace and schema, then evaluates a dictionary 
    nest of groups recursively and fields or (their) attributes as childs of the groups
    """
    
    # step1
    yml_appdef = read_application_definition(input_file)

    # step2 XML schema, namespace
    xml_root = ET.Element(
        'definition', {
        ET.QName("xmlns"): 'http://definition.nexusformat.org/nxdl/3.1', 
        ET.QName("xmlns:xsi"): 'http://www.w3.org/2001/XMLSchema-instance',
        ET.QName("xsi:schemaLocation"): 'http://www.w3.org/2001/XMLSchema-instance'
        }
    )
    
    assert 'name' in yml_appdef.keys(), 'keyword not specified'

    #step 3 define which NeXus object the yaml file conceptualized
    if 'category' in yml_appdef.keys():
        if yml_appdef['category'] == 'application':
            xml_root.set('category', 'application')
            xml_root.set('extends', 'NXentry')
        elif yml_appdef['category'] == 'contributed':
            xml_root.set('category', 'contributed')
            xml_root.set('extends', 'NXobject')
        elif yml_appdef['category'] == 'base':
            xml_root.set('category', 'base')
            xml_root.set('extends', 'NXobject')
        else:
            raise ValueError('Top-level keyword category exists in the yml but one of these: application, contributed, base !')
        xml_root.set('type', 'group')
    else:
        raise ValueError('Top-level keyword category does not exist in the yml !')

    if 'doc' in yml_appdef.keys():
        xml_root.set('doc', yml_appdef['doc'])
    else:
        raise ValueError('Top-level docstring does not exist in the yml !')

    # step4 traverse nested dictionaries representing groups and fields of NeXus and their attributes
    recursive_build(xml_root, yml_appdef)

    # step5 I/O
    pretty_print_xml(xml_root, input_file[:-4] + '.nxdl.xml')
    print('Parsed YAML to NXDL successfully')

if __name__ == '__main__':
    yaml2nxdl().parse()  # pylint: disable=no-value-for-parameter
