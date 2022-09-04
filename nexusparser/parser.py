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

from typing import Optional, Tuple
import xml.etree.ElementTree as ET

import numpy as np

from nomad.datamodel import EntryArchive
from nomad.metainfo import MSection, Quantity
from nomad.parsing import MatchingParser
from nexusparser.tools import nexus as read_nexus
from nexusparser.metainfo import nexus
from nomad.units import ureg


def _to_group_name(nx_node: ET.Element):
    '''
    Normalise the given group name
    '''
    return nx_node.attrib.get('name', nx_node.attrib['type'][2:].upper())


# noinspection SpellCheckingInspection
def _to_section(
        hdf_name: Optional[str], nx_def: str, nx_node: Optional[ET.Element],
        current: MSection) -> MSection:
    '''
    Args:
        hdf_name : name of the hdf group/field/attribute (None for definition)
        nx_def : application definition
        nx_node : node in the nxdl.xml
        current : current section in which the new entry needs to be picked up from

    Note that if the new element did not exist, it will be created

    Returns:
        tuple: the new subsection

    The strict mapping is available between metainfo and nexus:
        Group <-> SubSection
        Field <-> Quantity
        Attribute <-> SubSection.Attribute or Quantity.Attribute

    If the given nxdl_node is a Group, return the corresponding SubSection.
    If the given nxdl_node is a Field, return the SubSection contains it.
    If the given nxdl_node is a Attribute, return the associated SubSection or the
    SubSection contains the associated Quantity.
    '''

    if hdf_name is None:
        nomad_def_name = nx_def
    elif nx_node.tag.endswith('group'):
        # it is a new group
        nomad_def_name = _to_group_name(nx_node)
    else:
        # no need to change section for quantities and attributes
        return current

    # for groups, get the definition from the package
    new_def = current.m_def.all_sub_sections[nomad_def_name]

    new_section: MSection = None  # type:ignore

    for section in current.m_get_sub_sections(new_def):
        if hdf_name is None or getattr(section, 'nx_name', None) == hdf_name:
            new_section = section
            break

    if new_section is None:
        current.m_create(new_def.section_def.section_cls)
        new_section = current.m_get_sub_section(new_def, -1)
        new_section.__dict__['nx_name'] = hdf_name

    return new_section


def _get_value(hdf_node):
    '''
    Get value from hdl5 node
    '''

    hdf_value = hdf_node[...]
    if str(hdf_value.dtype) == 'bool':
        val = bool(hdf_value)
    elif hdf_value.dtype.kind in 'iufc':
        val = hdf_value
    else:
        try:
            val = str(hdf_value.astype(str))
        except UnicodeDecodeError:
            val = str(hdf_node[()].decode())
    return val


def _retrieve_definition(name: str, section: MSection) -> Quantity:
    '''
    Retrieve field definition by its name
    '''
    for quantity in section.m_def.all_properties.values():
        if quantity.name == name or name in quantity.aliases:
            return quantity

    # this, by given both definition and data, should never happen
    # if it raises, the data must be wrong
    raise ValueError(f'Cannot find the given name {name} in the definition.')


def _populate_data(
        depth: int, nx_path: list, nx_def: str, hdf_node, val, current: MSection,
        log_str: str, log_lvl: str) -> Tuple[str, str]:
    '''
    Populate attributes and fields
    '''

    if depth < len(nx_path):
        # it is an attribute of either field or group
        nx_attr = nx_path[depth]
        nx_parent: ET.Element = nx_path[depth - 1]
        if isinstance(nx_attr, str):
            if nx_attr == "units":
                metainfo_def = _retrieve_definition(nx_parent.get('name'), current)
                if not metainfo_def.variable:
                    metainfo_def.dimensionality = val[0]
        else:
            # get the name of parent (either field or group)
            # which will be used to set attribute
            # this is required by the syntax of metainfo mechanism
            # due to variadic/template quantity names
            parent_type = nx_parent.get('type').replace('NX', '').upper()
            parent_name = nx_parent.get('name', parent_type)  # type: ignore

            attr_name = nx_attr.get('name')
            # by default, we assume it is a 1D array
            attr_value = [value for value in hdf_node.attrs[attr_name]]
            if len(attr_value) == 1:
                attr_value = attr_value[0]

            current = _to_section(attr_name, nx_def, nx_attr, current)

            try:
                current.m_set_attribute(parent_name, attr_name, attr_value)
            except Exception as exc:
                log_str += f'Problem with storage!!!\n{str(exc)}\n'
                log_lvl = 'error'
    else:
        # it is a field
        field = _get_value(hdf_node)
        # if hdf_node[...].dtype.kind in 'iufc' and isinstance(
        #         field, np.ndarray) and field.size > 1:
        #     field = np.array([
        #         np.mean(field), np.var(field), np.min(field), np.max(field)])

        # get the corresponding field name
        metainfo_def = _retrieve_definition(nx_path[-1].get('name'), current)

        if metainfo_def.variable:
            new_def = metainfo_def.m_copy()
            new_def.name = hdf_node.name.split('/')[-1]
        else:
            new_def = metainfo_def
        # check if unit is given
        unit = hdf_node.attrs.get('units', None)
        if unit:
            if unit == 'counts':
                new_def.unit = '1'
            else:
                new_def.unit = unit
            field = ureg.Quantity(field, new_def.unit)

        # may need to check if the given unit is in the allowable list

        try:
            current.m_set(new_def, field, new_def.variable)
        except Exception as exc:
            log_str += f'Problem with storage!!!\n{str(exc)}\n'
            log_lvl = 'error'

    return log_str, log_lvl


def _add_log(nx_def: Optional[str], nx_path: list, val, log_str: str) -> str:
    '''
    Add log entry for the given node
    '''

    log_str += '???' if nx_def is None else nx_def
    log_str += ':'

    first = True
    for p_node in nx_path:
        if first:
            first = False
        else:
            log_str += '.'
        if isinstance(p_node, str):
            log_str += p_node
        else:
            read_nexus.get_node_name(p_node)

    log_str += ' - ' + val[0]
    if len(val) > 1:
        log_str += '...'

    return log_str + '\n'


class NexusParser(MatchingParser):
    '''
    NexusParser doc
    '''

    def __init__(self):
        super().__init__(
            name='parsers/nexus', code_name='NEXUS',
            code_homepage='https://www.nexus.eu/',
            mainfile_mime_re=r'(application/.*)|(text/.*)',
            mainfile_name_re=r'.*\.nxs',
            supported_compressions=['gz', 'bz2', 'xz']
        )
        self.archive: Optional[EntryArchive] = None
        self.nx_root = None

    def __nexus_populate(self, params, attr=None):
        '''
        Walks through name_list and generate nxdl nodes
        (hdf_info, nx_def, nx_path, val, logger) = params
        '''

        hdf_info: dict
        nx_def: str
        nx_path: list

        (hdf_info, nx_def, nx_path, val, logger) = params

        hdf_path: str = hdf_info['hdf_path']
        hdf_node = hdf_info['hdf_node']

        log_str: str = f'{hdf_path}{f"@{attr}" if attr else ""}\n'
        log_lvl: str = 'info'

        if nx_path is None:
            log_str += 'NOT IN SCHEMA - skipped\n'
            log_lvl = 'warning'
        else:
            log_str = _add_log(nx_def, nx_path, val, log_str)

            current: MSection = _to_section(None, nx_def, None, self.nx_root)
            depth: int = 1
            for name in hdf_path.split('/')[1:]:
                nx_node = nx_path[depth] if depth < len(nx_path) else name
                current = _to_section(name, nx_def, nx_node, current)
                depth += 1

            log_str, log_lvl = _populate_data(
                depth, nx_path, nx_def, hdf_node, val, current, log_str, log_lvl)

        if log_lvl == 'info':
            logger.info('Parsing', nexusparser=log_str)
        elif log_lvl == 'warning':
            logger.warning('Parsing', nexusparser=log_str)
        elif log_lvl == 'error':
            logger.error('Parsing', nexusparser=log_str)
        else:
            logger.critical('Parsing', nexusparser=log_str + 'NOT HANDLED\n')

    def parse(
            self, mainfile: str, archive: EntryArchive, logger=None, child_archives=None):
        self.archive = archive
        self.archive.m_create(nexus.NeXus)  # type: ignore # pylint: disable=no-member
        self.nx_root = self.archive.nexus

        nexus_helper = read_nexus.HandleNexus(logger, [mainfile])
        nexus_helper.process_nexus_master_file(self.__nexus_populate)

        if archive.metadata is None:
            return

        app_def: str = ''
        for var in dir(archive.nexus):
            if getattr(archive.nexus, var, None) is not None:
                app_def = var

        archive.metadata.entry_type = app_def
