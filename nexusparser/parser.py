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

import datetime
import numpy as np
import h5py

from nomad.datamodel import EntryArchive
from nomad.parsing import MatchingParser

from nomad.parsing.file_parser import TextParser, Quantity

from . import metainfo  # pylint: disable=unused-import
from nexusparser.tools import read_nexus
from nexusparser.metainfo import nexus

import sys
import logging


class NexusParser(MatchingParser):
    def __init__(self):
        super().__init__(
            name='parsers/nexus', code_name='NEXUS', code_homepage='https://www.nexus.eu/',
            mainfile_mime_re=r'(application/.*)|(text/.*)',
            mainfile_contents_re=(r'^\s*#\s*This is nexus output'),
            supported_compressions=['gz', 'bz2', 'xz']
        )

    def to_camel_case(self, snake_str: str, upper: bool = False) -> str:
        components = snake_str.split('_')
        if upper:
            return ''.join(f'{x[0].upper()}{x[1:]}' for x in components)

        return components[0] + ''.join(f'{x[0].upper()}{x[1:]}' for x in components[1:])

    def get_nomad_classname(self, xmlName, xmlType, suffix):
        if suffix == 'Attribute' or suffix == 'Field' or xmlType[2:].upper() != xmlName:
            name = self.to_camel_case(xmlName, True) + suffix
        else:
            name = self.to_camel_case(xmlType, True) + suffix
        return name

    def get_to_new_SubSection(self, hdfName, nxdef, nxdlNode, act_class, act_section):
        '''
        hdfName         name of the hdf group/field/attribute (None for definition)
        nxdef           application definition
        nxdlNode        node in the nxdl.xml
        act_class       actual class
        act_section     actual section in which the new entry needs to be picked up from
                        Note that if the new element did not exists, it is created now
        return          (new_class, new_section)
        TODO:   try to find also in the base section???
        '''
        if hdfName is None:
            nomad_def_name = 'nx_application_' + nxdef[2:]
            nomad_class_name = nxdef
        elif nxdlNode.tag.endswith('field'):
            nxdl_F_A_Name = nxdlNode.attrib['name'] if 'name' in nxdlNode.attrib else hdfName
            nomad_def_name = 'nx_field_' + nxdl_F_A_Name
            nomad_class_name = self.get_nomad_classname(nxdl_F_A_Name, None, "Field")
        elif nxdlNode.tag.endswith('group'):
            nxdl_G_Name = nxdlNode.attrib['name'] if 'name' in nxdlNode.attrib else nxdlNode.attrib['type'][2:]
            nomad_def_name = 'nx_group_' + nxdl_G_Name
            nomad_class_name = self.get_nomad_classname(read_nexus.get_node_name(nxdlNode), nxdlNode.attrib['type'], "Group")
        else:
            nxdl_F_A_Name = nxdlNode.attrib['name'] if 'name' in nxdlNode.attrib else hdfName
            nomad_def_name = 'nx_attribute_' + nxdl_F_A_Name
            nomad_class_name = self.get_nomad_classname(nxdl_F_A_Name, None, "Attribute")

        new_def = act_section.m_def.all_sub_sections[nomad_def_name]
        new_class = new_def.section_def.section_cls
        # the above does not work for NXarpes:NXarpes.ENTRY.INSTRUMENT.SOURCE.type - b'Free Electron Laser'
        # as it does not check against the enum: 'Free-Electron Laser'
        # new_def=act_section.m_def.all_properties.get(nomad_def_name, None)
        # new_class = act_class.__dict__[nomad_class_name]
        new_section = None
        new_section = act_section.m_get_sub_section(new_def, -1)
        # for section in act_section.m_get_sub_sections(new_def):
        #    if hdfName is not None and getattr(section,"nx_name") and section.nx_name == hdfName:
        #        new_section = section
        #        break
        if new_section is None:
            act_section.m_create(new_class)
            new_section = act_section.m_get_sub_section(new_def, -1)
            if hdfName is not None:
                new_section.nx_name = hdfName
        return (new_class, new_section)

    def get_value(self, hdfValue):
        if str(hdfValue.dtype) == 'bool':
            val = bool(hdfValue)
        elif hdfValue.dtype.kind in 'iufc':
            val = hdfValue
        else:
            val = str(hdfValue.astype(str))
        return val

    def nexus_populate(self, hdfPath, hdfNode, nxdef, nxdlPath, val):
        print('%%%%%%%%%%%%%%')
        # print(nxdef+':'+'.'.join(p.getroottree().getpath(p) for p in nxdlPath)+' - '+val[0]+ ("..." if len(val) > 1 else ''))
        if nxdlPath is not None:
            print((nxdef or '???') + ':' + '.'.join(p if isinstance(p, str) else read_nexus.get_node_name(p) for p in nxdlPath) + ' - ' + val[0] + ("..." if len(val) > 1 else ''))
            act_section = self.nxroot
            hdfNamelist = hdfPath.split('/')[1:]
            (act_class, act_section) = self.get_to_new_SubSection(None, nxdef, None, nexus, act_section)
            level = 1
            for hdfName in hdfNamelist:
                nxdlNode = nxdlPath[level] if level < len(nxdlPath) else hdfName
                (act_class, act_section) = self.get_to_new_SubSection(hdfName, nxdef, nxdlNode, act_class, act_section)
                level += 1
            if level < len(nxdlPath):
                nxdlNode = nxdlPath[level]
                if isinstance(nxdlNode, str):
                    # conventional attribute not in schema
                    try:
                        if nxdlNode == "units":
                            act_section.nx_unit = val[0]
                        elif nxdlNode == "default":
                            assert 1 == 2, "Quantity 'default' is not yet added by default to groups in Nomad schema"
                    except Exception as e:
                        print("Problem with storage!!!" + str(e))
                else:
                    # attribute in schema
                    (act_class, act_section) = self.get_to_new_SubSection(nxdlNode.attrib['name'], nxdef, nxdlNode, act_class, act_section)
                    try:
                        act_section.nx_value = val[0]
                    except Exception as e:
                        print("Problem with storage!!!" + str(e))
            else:
                try:
                    act_section.nx_value = self.get_value(hdfNode[...])
                except Exception as e:
                    print("Problem with storage!!!" + str(e))
        else:
            print('NOT IN SCHEMA - skipped')
        print('%%%%%%%%%%%%%%')
        pass

    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(stdout_handler)
        logger.info('Hello NeXus World')

        self.archive = archive
        self.archive.m_create(nexus.Nexus)
        self.nxroot = self.archive.nexus

        nexus_helper = read_nexus.HandleNexus(logger, [mainfile])
        nexus_helper.process_nexus_master_file(self.nexus_populate)
