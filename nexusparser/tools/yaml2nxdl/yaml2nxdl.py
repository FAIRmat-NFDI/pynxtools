#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import yaml
from lxml import etree
from yaml2nxdl_utils import nx_base_clss_string_mangling
from yaml2nxdl_utils import nx_base_clss, nx_cand_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt
from yaml2nxdl_read_user_yml_appdef import read_user_appdef
from yaml2nxdl_recursive_build import recursive_build

class yml2nxdl():
    def __init__(self, fn, *args, **kwargs):
        #add check if file exists
        #step1: read the user-specific application definition which was written as a yml file
        self.fnm = fn
        self.yml = read_user_appdef(self.fnm)
        print('Read YAML schema file')

    def parse(self):
        #step2a: create an instantiated NXDL schema XML tree, begin with the header add XML schema/namespaces
        attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        rt = etree.Element('definition', 
                   {attr_qname: 'http://definition.nexusformat.org/nxdl/nxdl.xsd' },
                   nsmap = {None: 'http://definition.nexusformat.org/nxdl/3.1', 
                            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        #step2b: user-defined attributes for the root group
        if 'name' in self.yml.keys():
            rt.set('name', self.yml['name'])
            del self.yml['name']
        else:
            raise ValueError('ERROR: name: keyword not specified !')
        pi = etree.ProcessingInstruction("xml-stylesheet", text='type="text/xsl" href="nxdlformat.xsl"')
        rt.addprevious(pi)
        #evaluate whether we handle an application definition, a contributed or base class
        if 'category' in self.yml.keys():
            if self.yml['category'] == 'application':
                rt.set('category', 'application')
                rt.set('extends', 'NXentry')
            elif self.yml['category'] == 'contributed':
                rt.set('category', 'contributed')
                rt.set('extends', 'NXobject')
            elif self.yml['category'] == 'base':
                rt.set('category', 'base')
                rt.set('extends', 'NXobject')
            else:
                raise ValueError('Top-level keyword category exists in the yml but one of these: application, contributed, base !')
            del self.yml['category']
            rt.set('type', 'group')
        else:
            raise ValueError('Top-level keyword category does not exist in the yml !')
        #step2c: docstring
        if 'doc' in self.yml.keys():
            rt.set('doc', self.yml['doc'])
            del self.yml['doc']
        else:
            raise ValueError('Top-level docstring does not exist in the yml !')
        if 'symbols' in self.yml.keys():
            syms = etree.SubElement(rt, 'symbols')
            if 'doc' in self.yml['symbols'].keys():
                syms.set('doc', self.yml['symbols']['doc'])
                del self.yml['symbols']['doc']
            for kk, vv in iter(self.yml['symbols'].items()):
                sym = etree.SubElement(syms, 'sym')
                sym.set('name', kk)
                sym.set('doc', vv)
            del self.yml['symbols']
        #do not throw in the case of else just accept that we do not have symbols

        #step3: walk the dictionary nested in self.yml to create an instantiated NXDL schema XML tree rt
        recursive_build(rt, self.yml)

        #step4: write the tree to a properly formatted NXDL XML file to disk
        nxdl = etree.ElementTree(rt)
        nxdl.write( self.fnm + '.nxdl.xml', pretty_print=True, xml_declaration=True, encoding="utf-8" )
        print('Parsed YAML to NXDL successfully')

#tests
fnm = 'NXtest_links.yml'
#fnm = 'NXarpes.yml'
#fnm = 'NXmx.yml'
#fnm = 'NXem_base_draft.yml'
#fnm = 'NXellipsometry_base_draft.yml'
#fnm = NXapm_draft.yml

#how to use the parser as a component
cv = yml2nxdl( fnm ).parse()