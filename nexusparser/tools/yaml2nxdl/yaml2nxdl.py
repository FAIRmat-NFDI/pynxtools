#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from lxml import etree
from yaml2nxdl_utils import nx_base_clss, nx_cand_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt
# check duplicates Types with no Name in read_user_appdef: https://stackoverflow.com/questions/33490870/parsing-yaml-in-python-detect-duplicated-keys
from yaml2nxdl_read_user_yml_appdef import read_user_appdef
from yaml2nxdl_recursive_build import recursive_build

from typing import Tuple
import click


@click.command()
@click.option(
    '--input_file',
    #default=['example.yml'],
    multiple=True,
    help='The path to the input data file to read. (Repeat for more than one file.)'
)
def yaml2nxdl(input_file: Tuple[str]):
    # add check if file exists
    # step1: read the user-specific application definition which was written as a yml file
    yml = read_user_appdef(input_file[0])
    # print('Read YAML schema file')

    # step2a: create an instantiated NXDL schema XML tree, begin with the header add XML schema/namespaces
    attr_qname = etree.QName(
        "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    rt = etree.Element('definition',
                       {attr_qname: 'http://definition.nexusformat.org/nxdl/nxdl.xsd'},
                       nsmap={None: 'http://definition.nexusformat.org/nxdl/3.1',
                                 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
                       )
                  # ,
                     # 'schemaLocation'}) ###############àà
      # step2b: user-defined attributes for the root group
    if 'name' in yml.keys():
        rt.set('name', yml['name'])
        del yml['name']
    else:
        raise ValueError('ERROR: name: keyword not specified !')
    pi = etree.ProcessingInstruction(
        "xml-stylesheet", text='type="text/xsl" href="nxdlformat.xsl"')
    rt.addprevious(pi)
        # evaluate whether we handle an application definition, a contributed or base class
    if 'category' in yml.keys():
        if yml['category'] == 'application':
            rt.set('category', 'application')
            rt.set('extends', 'NXentry')
        elif yml['category'] == 'contributed':
            rt.set('category', 'contributed')
            rt.set('extends', 'NXobject')
        elif yml['category'] == 'base':
            rt.set('category', 'base')
            rt.set('extends', 'NXobject')
        else:
            raise ValueError(
            'Top-level keyword category exists in the yml but one of these: application, contributed, base !')
        del yml['category']
        rt.set('type', 'group')
    else:
        raise ValueError(
            'Top-level keyword category does not exist in the yml !')
    # step2c: docstring
    if 'doc' in yml.keys():
        rt.set('doc', yml['doc'])
        del yml['doc']
    else:
        raise ValueError('Top-level docstring does not exist in the yml !')
    if 'symbols' in yml.keys():
        syms = etree.SubElement(rt, 'symbols')
        if 'doc' in yml['symbols'].keys():
            syms.set('doc', yml['symbols']['doc'])
            del yml['symbols']['doc']
        for kk, vv in iter(yml['symbols'].items()):
            sym = etree.SubElement(syms, 'sym')
            sym.set('name', kk)
            sym.set('doc', vv)
        del yml['symbols']
    # do not throw in the case of else just accept that we do not have symbols

        # step3: walk the dictionary nested in yml to create an instantiated NXDL schema XML tree rt
    recursive_build(rt, yml)

        # step4: write the tree to a properly formatted NXDL XML file to disk
    nxdl = etree.ElementTree(rt)
    nxdl.write(input_file[0] + '.nxdl.xml', pretty_print=True,
               xml_declaration=True, encoding="utf-8")
    print('Parsed YAML to NXDL successfully')

# tests
# fnm = 'NXmpes_core_draft.yml'
# fnm = 'NXtest_links.yml'
# fnm = 'NXarpes.yml'
# fnm = 'NXmx.yml'
# fnm = 'NXem_base_draft.yml'
# fnm = 'NXellipsometry_base_draft.yml'
# fnm = NXapm_draft.yml

# how to use the parser as a component
# cv = yml2nxdl( fnm ).parse()


if __name__ == '__main__':
  #  logging.basicConfig(level=logging.DEBUG)
    yaml2nxdl().parse()  # pylint: disable=no-value-for-parameter
