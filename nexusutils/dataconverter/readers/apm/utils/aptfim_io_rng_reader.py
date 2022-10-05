#!/usr/bin/env python3
"""RNG range file reader used by atom probe microscopists."""

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

import re
import numpy as np

from nexusutils.dataconverter.readers.apm.utils.aptfim_io_utils \
    import NxField, NxIon, significant_range, create_isotope_vector, \
    isotope_vector_to_dict_keyword


def evaluate_rng_range_line(
        i: int, line: str, column_id_to_label: dict, number_of_columns: int) -> dict:
    """Represent information content of a single range line."""
    # example line: '. 107.7240 108.0960 1 0 0 0 0 0 0 0 0 0 3 0 0 0'
    info: dict = {}
    info['identifier'] = 'Range' + str(i)
    info['range'] = None
    info['comp'] = []
    info['color'] = None  # do not parse out user-defined color

    tmp = re.split(r'\s+', line)
    assert len(tmp) is number_of_columns, 'Line ' + line \
        + ' inconsistent number columns!'
    assert tmp[0] == '.', 'Line ' + line + ' has inconsistent line prefix!'

    assert significant_range(
        np.float64(tmp[1]), np.float64(tmp[2])), \
        'Line ' + line + ' insignificant range!'
    info['range'] = np.float64(np.asarray([tmp[1], tmp[2]]))

    # line encodes multiplicity of element via array of multiplicity counts
    flags_all = np.asarray(tmp[3:len(tmp)], np.uint32)
    if np.sum(flags_all) > 0:
        for j in np.arange(0, len(flags_all)):
            assert flags_all[j] >= 0, 'Line ' + line \
                + ' no negative element counts!'
            if flags_all[j] > 0:
                info['comp'] += [column_id_to_label[j + 1]] * flags_all[j]
    else:
        raise ValueError('Line ' + line + ' no element counts!')
    return info


def evaluate_rng_ion_type_header(line: str) -> dict:
    """Represent information content in the key header line."""
    # line = '------------------- Fe Mg Al Mn Si V C Ga Ti Ca O Na Co H'
    info: dict = {}
    info['column_id_to_label'] = {}
    tmp = re.split(r'\s+', line)
    assert len(tmp) > 1, 'RNG file does not contain iontype labels!'
    for i in np.arange(1, len(tmp)):
        info['column_id_to_label'][i] = tmp[i]
    return info


class ReadRngFileFormat():
    """Read *.rng file format."""

    def __init__(self, filename: str):
        assert len(filename) > 4, 'RNG file incorrect filename ending!'
        assert filename.lower().endswith('.rng'), \
            'RNG file incorrect file type!'
        self.filename = filename

        self.rng: dict = {}
        self.rng['ions'] = {}
        self.rng['ranges'] = {}

    def read_rng(self):
        """Read RNG range file content."""
        with open(self.filename, mode='r', encoding='utf8') as rngf:
            txt = rngf.read()

        # windows to unix EOL conversion  # pylint: disable=R0801
        txt = txt.replace('\r\n', '\n')  # pylint: disable=R0801
        # use decimal dots instead of comma  # pylint: disable=R0801
        txt = txt.replace(',', '.')  # pylint: disable=R0801
        txt_stripped = [line for line in txt.split('\n')  # pylint: disable=R0801
                        if line.strip() != '' and line.startswith('#') is False]  # pylint: disable=R0801
        del txt  # pylint: disable=R0801

        # pylint: disable=R0801 # see DOI: 10.1007/978-1-4899-7430-3 for further details to this  # pylint: disable=R0801
        # pylint: disable=R0801 # Oak Ridge National Lab / Oxford *.rng file format  # pylint: disable=R0801
        # pylint: disable=R0801 # only the first ------ line is relevant  # pylint: disable=R0801
        # pylint: disable=R0801 # it details all ion labels aka ions  # pylint: disable=R0801
        # pylint: disable=R0801 # AMETEK's IVAS/APSuite-specific trailing  # pylint: disable=R0801
        # pylint: disable=R0801 # polyatomic extension is redundant info  # pylint: disable=R0801

        tmp = None
        current_line_id = int(0)  # search key header line
        for line in txt_stripped:
            tmp = re.search(r'----', line)
            if tmp is None:
                current_line_id += int(1)
            else:
                break
        assert tmp is not None, 'RNG file does not contain key header line!'

        header = evaluate_rng_ion_type_header(txt_stripped[current_line_id])

        tmp = re.split(r'\s+', txt_stripped[0])
        assert tmp[0].isnumeric() is True, 'Number of species corrupted!'
        number_of_atom_types = int(tmp[0])
        assert number_of_atom_types >= 0, 'No species defined!'
        assert tmp[1].isnumeric() is True, 'Number of ranges corrupted!'
        number_of_ion_types = int(tmp[1])
        assert number_of_ion_types >= 0, 'No ranges defined!'

        for i in np.arange(current_line_id + 1,
                           current_line_id + 1 + number_of_ion_types):
            obj = evaluate_rng_range_line(
                i - current_line_id, txt_stripped[i],
                header['column_id_to_label'],
                number_of_atom_types + 3)

            assert obj is not None, \
                'Line ' + txt_stripped[i] + ' is corrupted!'
            self.rng['ranges'][obj['identifier']] = obj

        for obj in self.rng['ranges'].values():
            hashvector = create_isotope_vector(obj['comp'])
            keyword = isotope_vector_to_dict_keyword(hashvector)

            if keyword not in self.rng['ions'].keys():
                self.rng['ions'][keyword] = NxIon()
                self.rng['ions'][keyword].name = NxField(keyword, None)
                self.rng['ions'][keyword].charge_state = \
                    NxField(np.int32(0), '')
                # RNG files do not store charge state and isotopes explicitly
                self.rng['ions'][keyword].isotope_vector = \
                    NxField(hashvector, None)

            self.rng['ions'][keyword].add_range(
                obj['range'][0], obj['range'][1])

    def report_range(self):
        """Summarize content in a range file."""
        print(self.rng['ions'])
        print(self.rng['ranges'])


if __name__ == 'main':
    pass
    # testing
    # parsedFile = ReadRngFileFormat('../../SeHoKim_R5076_44076_v02.rng')
