"""parser doc

"""
from typing import Optional
import xml.etree.ElementTree as ET

import numpy as np

from nomad.datamodel import EntryArchive
from nomad.metainfo import MSection, Quantity, MetainfoError
from nomad.parsing import MatchingParser
# from . import metainfo  # pylint: disable=unused-import
from nexusparser.tools import nexus as read_nexus
from nexusparser.metainfo import nexus


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


def to_group_name(nxdl_node: ET.Element):
    return 'nx_group_' + nxdl_node.attrib.get('name', nxdl_node.attrib['type'][2:].upper())


# noinspection SpellCheckingInspection
def to_new_section(
        hdf_name: Optional[str],
        nxdef: str,
        nxdl_node: ET.Element,
        act_section: MSection
) -> MSection:
    '''
    Args:
        hdf_name : name of the hdf group/field/attribute (None for definition)
        nxdef : application definition
        nxdl_node : node in the nxdl.xml
        act_section : actual section in which the new entry needs to be picked up from

    Note that if the new element did not exists, it is created now

    Returns:
        tuple: the new subsection

    The strict mapping is available between metainfo and nexus:
        Group <-> SubSection
        Field <-> Quantity
        Attribute <-> SubSection.Attribute or Quantity.Attribute

    If the given nxdl_node is a Group, return the corresponding SubSection.
    If the given nxdl_node is a Field, return the SubSection contains it.
    If the given nxdl_node is a Attribute, return the associated SubSection or the SubSection contains
        the associated Quantity.

    TODO:   try to find also in the base section???
    '''

    if hdf_name is None:
        nomad_def_name = 'nx_application_' + nxdef[2:]
    elif nxdl_node.tag.endswith('group'):
        # it is a new group
        nomad_def_name = to_group_name(nxdl_node)
    else:
        # no need to change section for quantities and attributes
        return act_section

    new_def = act_section.m_def.all_sub_sections[nomad_def_name]

    new_section: MSection = None  # type:ignore

    for section in act_section.m_get_sub_sections(new_def):
        if hdf_name is None or getattr(section, 'nx_name', None) == hdf_name:
            new_section = section
            break

    if new_section is None:
        act_section.m_create(new_def.section_def.section_cls)
        new_section = act_section.m_get_sub_section(new_def, -1)
        new_section.__dict__['nx_name'] = hdf_name

    return new_section


def get_value(hdf_node):
    """Get value from hdl5 node

"""
    hdf_value = hdf_node[...]
    if str(hdf_value.dtype) == 'bool':
        val = bool(hdf_value)
    elif hdf_value.dtype.kind in 'iufc':
        val = hdf_value
    else:
        try:
            # todo: this may be an array of strings, need to convert properly
            val = str(hdf_value.astype(str))
        except UnicodeDecodeError:
            val = str(hdf_node[()].decode())
    return val


def _get_definition_by_name(name: str, section: MSection) -> Optional[Quantity]:
    for quantity in section.m_def.all_properties.values():
        if quantity.name == name or name in quantity.aliases:
            return quantity

    return None


def nexus_populate_helper(params):
    """helper for nexus_populate"""
    (path_level, nxdl_path, act_section, logstr, val, loglev, nxdef, hdf_node) = params
    if path_level < len(nxdl_path):
        nxdl_attribute = nxdl_path[path_level]
        parent_node = nxdl_path[path_level - 1]
        if isinstance(nxdl_attribute, str):
            if nxdl_attribute == "units":
                metainfo_def = _get_definition_by_name(parent_node.attrib['name'], act_section)
                metainfo_def.dimensionality = val[0]
        else:
            # attribute in schema
            attribute_name = nxdl_attribute.get('name')
            act_section = to_new_section(attribute_name, nxdef, nxdl_attribute, act_section)

            parent_name = parent_node.get('name', parent_node.attrib['type'][2:].upper())

            try:
                act_section.m_set_attribute(parent_name, attribute_name, val[0])
            except Exception:
                logstr += f'{parent_name} --> {attribute_name}'
                loglev = 'ERROR'
    else:
        data_field = get_value(hdf_node)
        if hdf_node[...].dtype.kind in 'iufc' and \
                isinstance(data_field, np.ndarray) and \
                data_field.size > 1:
            data_field = np.array([
                np.mean(data_field),
                np.var(data_field),
                np.min(data_field),
                np.max(data_field)
            ])
        metainfo_def = _get_definition_by_name(nxdl_path[-1].attrib['name'], act_section)
        unit = hdf_node.attrs.get('units', None)
        if unit:
            if unit == 'counts':
                metainfo_def.unit = '1'
            else:
                metainfo_def.unit = unit
        try:
            act_section.m_set(metainfo_def, data_field)
        except Exception as e:
            logstr += str(e)
            loglev = 'ERROR'
    return [logstr, loglev]


def add_log(params, logstr):
    """adds log entry for the given node"""
    if params[1] is not None:
        logstr += params[1]
    else:
        logstr += '???'
    logstr += ':'
    first = True
    for p_node in params[2]:
        if first:
            first = False
        else:
            logstr += '.'
        if isinstance(p_node, str):
            logstr += p_node
        else:
            read_nexus.get_node_name(p_node)
    logstr += ' - ' + params[3][0]
    if len(params[3]) > 1:
        logstr += '...'
    logstr += '\n'
    return logstr


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

    def nexus_populate(self, params, attr=None):
        """Walks through hdf_namelist and generate nxdl nodes
        (hdf_info, nxdef, nxdl_path, val, logger) = params"""
        hdf_path = params[0]['hdf_path']
        hdf_node = params[0]['hdf_node']
        logstr = hdf_path + (("@" + attr) if attr else '') + '\n'
        loglev = 'info'
        if params[2] is not None:
            logstr = add_log(params, logstr)
            act_section = self.nxroot
            hdf_namelist = hdf_path.split('/')[1:]
            act_section = to_new_section(None, params[1], None, act_section)
            path_level = 1
            for hdf_name in hdf_namelist:
                nxdl_node = params[2][path_level] if path_level < len(params[2]) else hdf_name
                act_section = to_new_section(hdf_name, params[1], nxdl_node, act_section)
                path_level += 1
            helper_params = (path_level, params[2], act_section, logstr, params[3],
                             loglev, params[1], hdf_node)
            (logstr, loglev) = nexus_populate_helper(helper_params)
        else:
            logstr += ('NOT IN SCHEMA - skipped') + '\n'
            loglev = 'warning'
        if loglev == 'info':
            params[4].info('Parsing', nexusparser=logstr)
        elif loglev == 'warning':
            params[4].warning('Parsing', nexusparser=logstr)
        elif loglev == 'error':
            params[4].error('Parsing', nexusparser=logstr)
        else:
            params[4].critical('Parsing', nexusparser=logstr + 'NOT HANDLED\n')

    def parse(self, mainfile: str, archive: EntryArchive, logger=None, child_archives=None):
        nexus.init_nexus_metainfo()

        self.archive = archive
        self.archive.m_create(nexus.Nexus)  # type: ignore[attr-defined] # pylint: disable=no-member
        self.nxroot = self.archive.nexus

        nexus_helper = read_nexus.HandleNexus(logger, [mainfile])
        nexus_helper.process_nexus_master_file(self.nexus_populate)

        appdef = ""
        for var in dir(archive.nexus):
            if var.startswith("nx_application") and getattr(archive.nexus, var, None) is not None:
                appdef = var[len("nx_application_"):]

        if archive.metadata is not None:
            archive.metadata.entry_type = f"NX{appdef}"
