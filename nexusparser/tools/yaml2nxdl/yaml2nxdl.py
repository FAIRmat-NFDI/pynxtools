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
import xml.dom.minidom
from yaml2nxdl_utils import nx_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt
from yaml2nxdl_read_yml_appdef import read_application_definition
from yaml2nxdl_recursive_build import recursive_build

from typing import Tuple
import click


def pretty_print_xml_given_root(root, output_xml):
    """
    Print formatted xml file with built-in libraries
    """
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = os.linesep.join([s for s in xml_string.splitlines() if s.strip()]) 
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)

@click.command()
@click.option(
    '--input-file',
    help='The path to the input data file to read. (Repeat for more than one file.)'
)
def yaml2nxdl(input_file: str):

    # step1
    yml_appdef = read_application_definition(input_file)

    # step2a
    attr_qname = ET.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    rt = ET.Element(
        'definition',{attr_qname: 'http://definition.nexusformat.org/nxdl/nxdl.xsd'},
        nsmap={None: 'http://definition.nexusformat.org/nxdl/3.1',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        )
    # step2b
    assert 'name' in yml_appdef, 'keyword not specified' 

    #pi = ET.ProcessingInstruction(
    #    "xml-stylesheet", text='type="text/xsl" href="nxdlformat.xsl"')
    #rt.addprevious(pi) 

    if 'category' in yml_appdef.keys():
        if yml_appdef['category'] == 'application':
            rt.set('category', 'application')
            rt.set('extends', 'NXentry')
        elif yml_appdef['category'] == 'contributed':
            rt.set('category', 'contributed')
            rt.set('extends', 'NXobject')
        elif yml_appdef['category'] == 'base':
            rt.set('category', 'base')
            rt.set('extends', 'NXobject')
        else:
            raise ValueError(
            'Top-level keyword category exists in the yml but one of these: application, contributed, base !')
        del yml_appdef['category']
        rt.set('type', 'group')
    else:
        raise ValueError(
            'Top-level keyword category does not exist in the yml !')
    # step2c
    if 'doc' in yml_appdef.keys():
        rt.set('doc', yml_appdef['doc'])
        del yml_appdef['doc']
    else:
        raise ValueError('Top-level docstring does not exist in the yml !')
    if 'symbols' in yml_appdef.keys():
        syms = ET.SubElement(rt, 'symbols')
        if 'doc' in yml_appdef['symbols'].keys():
            syms.set('doc', yml_appdef['symbols']['doc'])
            del yml_appdef['symbols']['doc']
        for kkeyword, vvalue in iter(yml_appdef['symbols'].items()):
            sym = ET.SubElement(syms, 'sym')
            sym.set('name', kkeyword)
            sym.set('doc', vvalue)
        del yml_appdef['symbols']
    # do not throw in the case of else just accept that we do not have symbols

    # step3
    recursive_build(rt, yml_appdef)

    # step4
    pretty_print_xml_given_root(rt, 'output.xml')
    print('Parsed YAML to NXDL successfully')

if __name__ == '__main__':
    yaml2nxdl().parse()  # pylint: disable=no-value-for-parameter
