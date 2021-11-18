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

from nomad.datamodel import EntryArchive
from nomad.parsing import MatchingParser
from nomad.units import ureg as units

from nomad.parsing.file_parser import TextParser, Quantity

from . import metainfo  # pylint: disable=unused-import
from nexusparser.tools.read_nexus import HandleNexus

import sys
import logging

'''
This is a hello world style nexus for an nexus parser/converter.
'''


def str_to_sites(string):
    sym, pos = string.split('(')
    pos = np.array(pos.split(')')[0].split(',')[:3], dtype=float)
    return sym, pos

'''
calculation_parser = TextParser(quantities=[
    Quantity('sites', r'([A-Z]\([\d\.\, \-]+\))', str_operation=str_to_sites, repeats=True),
    Quantity(
        Atoms.lattice_vectors,
        r'(?:latice|cell): \((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*',
        repeats=False),
    Quantity('energy', r'energy: (\d\.\d+)'),
    Quantity('magic_source', r'done with magic source\s*\*{3}\s*\*{3}\s*[^\d]*(\d+)', repeats=False)])

mainfile_parser = TextParser(quantities=[
    Quantity('date', r'(\d\d\d\d\/\d\d\/\d\d)', repeats=False),
    Quantity('program_version', r'super\_code\s*v(\d+)\s*', repeats=False),
    Quantity(
        'calculation', r'\s*system \d+([\s\S]+?energy: [\d\.]+)([\s\S]+\*\*\*)*',
        sub_parser=calculation_parser,
        repeats=True)
])
'''

class NexusParser(MatchingParser):
    def __init__(self):
        super().__init__(
            name='parsers/nexus', code_name='NEXUS', code_homepage='https://www.nexus.eu/',
            mainfile_mime_re=r'(application/.*)|(text/.*)',
            mainfile_contents_re=(r'^\s*#\s*This is nexus output'),
            supported_compressions=['gz', 'bz2', 'xz']
        )

    def nexus_populate(self,hdfPath,hdfNode,nxdef,nxdlPath,val):
        print('%%%%%%%%%%%%%%')
        #print(nxdef+':'+'.'.join(p.getroottree().getpath(p) for p in nxdlPath)+' - '+val[0]+ ("..." if len(val) > 1 else ''))
        if nxdlPath is not None:
            print((nxdef or '???')+':'+'.'.join(str(p) for p in nxdlPath)+' - '+val[0]+ ("..." if len(val) > 1 else ''))
        print('%%%%%%%%%%%%%%')
        pass

    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(stdout_handler)
        logger.info('Hello NeXus World')

        nexus_helper = HandleNexus([mainfile])
        nexus_helper.process_nexus_master_file(self.nexus_populate)



'''

        # Use the previously defined parsers on the given mainfile
        mainfile_parser.mainfile = mainfile
        mainfile_parser.parse()

        # Output all parsed data into the given archive.
        run = archive.m_create(Run)
        date = datetime.datetime.strptime(
            mainfile_parser.get('date'),
            '%Y/%m/%d') - datetime.datetime(1970, 1, 1)
        run.program = Program(
            name = 'super_code',
            version = str(mainfile_parser.get('program_version')),
            compilation_datetime = date.total_seconds())

        for calculation in mainfile_parser.get('calculation'):
            system = run.m_create(System)
            atoms = system.m_create(Atoms)

            atoms.lattice_vectors = calculation.get('lattice_vectors')
            sites = calculation.get('sites')
            atoms.labels = [site[0] for site in sites]
            atom.positions = [site[1] for site in sites]

            scc = run.m_create(Calculation)
            scc.system_ref = system
            scc.m_create(Energy, total = EnergyEntry(value = calculation.get('energy') * unit.eV))
            magic_source = calculation.get('magic_source')
            if magic_source is not None:
                scc.x_nexus_magic_value = magic_source
'''