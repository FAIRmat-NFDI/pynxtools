"""parser doc

"""
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
import logging
import numpy as np
from nomad.datamodel import EntryArchive
from nomad.parsing import MatchingParser
# from . import metainfo  # pylint: disable=unused-import
from nexusparser.tools import nexus as read_nexus
from nexusparser.metainfo import nexus


def get_to_new_subsection(hdf_name, nxdef, nxdl_node, act_section):
    """hdf_name         name of the hdf group/field/attribute (None for definition)
    nxdef           application definition
    nxdl_node        node in the nxdl.xml
    act_class       actual class
    act_section     actual section in which the new entry needs to be picked up from
                    Note that if the new element did not exists, it is created now
    return          (new_class, new_section)
    TODO:   try to find also in the base section???

"""
    if hdf_name is None:
        nomad_def_name = 'nx_application_' + nxdef[2:]
        # nomad_class_name = nxdef
    elif nxdl_node.tag.endswith('field'):
        nxdl_f_a_name = nxdl_node.attrib['name'] if 'name' in nxdl_node.attrib else hdf_name
        nomad_def_name = 'nx_field_' + nxdl_f_a_name
        # nomad_class_name = self.get_nomad_classname(nxdl_f_a_name, None, "Field")
    elif nxdl_node.tag.endswith('group'):
        nxdl_g_name = nxdl_node.attrib['name'] \
            if 'name' in nxdl_node.attrib else nxdl_node.attrib['type'][2:].upper()
        nomad_def_name = 'nx_group_' + nxdl_g_name
        # nomad_class_name = self.get_nomad_classname(read_nexus.get_node_name(nxdl_node),
        #                                             nxdl_node.attrib['type'], "Group")
    else:
        nxdl_f_a_name = nxdl_node.attrib['name'] if 'name' in nxdl_node.attrib else hdf_name
        nomad_def_name = 'nx_attribute_' + nxdl_f_a_name
        # nomad_class_name = self.get_nomad_classname(nxdl_f_a_name, None, "Attribute")

    new_def = act_section.m_def.all_sub_sections[nomad_def_name]
    new_class = new_def.section_def.section_cls
    new_section = None
    for section in act_section.m_get_sub_sections(new_def):
        if hdf_name is None or (getattr(section, "nx_name") and section.nx_name == hdf_name):
            new_section = section
            break
    if new_section is None:
        act_section.m_create(new_class)
        new_section = act_section.m_get_sub_section(new_def, -1)
        if hdf_name is not None:
            new_section.nx_name = hdf_name
    return (new_class, new_section)


def get_value(hdf_value):
    """Get value from hdl5 node

"""
    if str(hdf_value.dtype) == 'bool':
        val = bool(hdf_value)
    elif hdf_value.dtype.kind in 'iufc':
        val = hdf_value
    else:
        val = str(hdf_value.astype(str))
    return val


def helper_nexus_populate(nxdl_attribute, act_section, val):
    """Handle info of units attribute, raise error if default or something else is found

"""
    try:
        if nxdl_attribute == "units":
            act_section.nx_unit = val[0]
        elif nxdl_attribute == "default":
            Exception("Quantity default' is not yet added by default to groups in Nomad schema")
    except Exception as exc:  # pylint: disable=broad-except
        print("Problem with storage!!!" + str(exc))


class NexusParser(MatchingParser):
    """NesusParser doc

"""
    def __init__(self):
        super().__init__(
            name='parsers/nexus', code_name='NEXUS', code_homepage='https://www.nexus.eu/',
            mainfile_mime_re=r'(application/.*)|(text/.*)',
            mainfile_name_re=(r'.*\.nxs'),
            supported_compressions=['gz', 'bz2', 'xz']
        )
        self.archive = None
        self.nxroot = None

#     def get_nomad_classname(self, xml_name, xml_type, suffix):
#         """Get nomad classname from xml file

# """
#         if suffix == 'Attribute' or suffix == 'Field' or xml_type[2:].upper() != xml_name:
#             name = xml_name + suffix
#         else:
#             name = xml_type + suffix
#         return name

    def nexus_populate(self, hdf_info, nxdef, nxdl_path, val):
        """Walks through hdf_namelist and generate nxdl nodes

"""
        hdf_path = hdf_info['hdf_path']
        hdf_node = hdf_info['hdf_node']
        print('%%%%%%%%%%%%%%')
        # print(nxdef+':'+'.'.join(p.getroottree().getpath(p) for p in nxdl_path)+
        # ' - '+val[0]+ ("..." if len(val) > 1 else ''))
        if nxdl_path is not None:
            print((nxdef or '???') + ':' + '.'.
                  join(p if isinstance(p, str) else
                       read_nexus.get_node_name(p)
                       for p in nxdl_path) + ' - ' + val[0] + ("..." if len(val) > 1 else ''))
            act_section = self.nxroot
            hdf_namelist = hdf_path.split('/')[1:]
            act_section = get_to_new_subsection(None, nxdef, None, act_section)[1]
            path_level = 1
            for hdf_name in hdf_namelist:
                nxdl_node = nxdl_path[path_level] if path_level < len(nxdl_path) else hdf_name
                act_section = get_to_new_subsection(hdf_name, nxdef,
                                                    nxdl_node, act_section)[1]
                path_level += 1
            if path_level < len(nxdl_path):
                nxdl_attribute = nxdl_path[path_level]
                if isinstance(nxdl_attribute, str):
                    # conventional attribute not in schema. Only necessary,
                    # if schema is not populated according
                    helper_nexus_populate(nxdl_attribute, act_section, val)
                else:
                    # attribute in schema
                    act_section = \
                        get_to_new_subsection(nxdl_attribute.attrib['name'], nxdef,
                                              nxdl_attribute, act_section)[1]
                    try:
                        act_section.nx_value = val[0]
                    except AttributeError as exc:
                        print("Problem with storage!!!" + str(exc))
                    except TypeError as exc:
                        print("Problem with storage!!!" + str(exc))
            else:
                try:
                    data_field = get_value(hdf_node[...])
                    if hdf_node[...].dtype.kind in 'iufc' and \
                            isinstance(data_field, np.ndarray) and \
                            data_field.size > 1:
                        data_field = np.array([
                            np.mean(data_field),
                            np.var(data_field),
                            np.min(data_field),
                            np.max(data_field)
                        ])
                    act_section.nx_value = data_field
                except TypeError as exc:
                    print("Problem with storage!!!" + str(exc))
        else:
            print('NOT IN SCHEMA - skipped')
        print('%%%%%%%%%%%%%%')

    def parse(self, mainfile: str, archive: EntryArchive, logger=None):
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(stdout_handler)

        self.archive = archive
        # TO DO ask Markus S. whether to disable or not this pylint error
        self.archive.m_create(nexus.Nexus)  # pylint: disable=no-member
        self.nxroot = self.archive.nexus

        nexus_helper = read_nexus.HandleNexus(logger, [mainfile])
        nexus_helper.process_nexus_master_file(self.nexus_populate)
