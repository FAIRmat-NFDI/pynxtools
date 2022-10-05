#!/usr/bin/env python3
"""RRNG range file reader used by atom probe microscopists."""

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


def evaluate_rrng_range_line(i: int, line: str, ion_type_names: list) -> dict:
    """Evaluate information content of a single range line."""
    # example line 'Range7 = 42.8160 43.3110 vol:0.04543
    #     Al:1 O:1 Name: AlO Color:00FFFF'
    # according to DOI: 10.1007/978-1-4614-8721-0
    # mqmin, mqmax, vol, ion composition is required,
    #     name and color fields are optional
    info: dict = {}
    info['identifier'] = 'Range' + str(i)
    info['range'] = None
    info['comp'] = []
    info['volume'] = None  # do not parse out volume
    info['color'] = None  # do not parse out user-defined color

    tmp = re.split(r'[\s=]+', line)
    assert len(tmp) >= 6, 'Line ' + line + \
        ' does not contain all required fields!'
    assert tmp[0] == 'Range' + str(i), 'Line ' + line + \
        ' has inconsistent line prefix!'

    assert significant_range(np.float64(tmp[1]), np.float64(tmp[2])), \
        'Line ' + line + ' insignificant range!'
    info['range'] = np.float64(np.asarray([tmp[1], tmp[2]]))

    # assert tmp[3].lower().startswith('vol:'), 'Line ' + line + \
    #    ' vol syntax corrupted!'
    # V = re.split(r':', tmp[3])[1]
    # assert tmp[-1].lower().startswith('color:'), 'Line ' + line + \
    #    ' color syntax corrupted!'
    # if tmp[-1].lower().startswith('color:') and len(re.split(r':',
    # tmp[-1])[1]) == 6 and self.color = '#' + re.split(r':', tmp[-1])[1]
    # HEX_COLOR_REGEX = r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    # replace r'^#( ...
    # regexp = re.compile(HEX_COLOR_REGEX)
    # if regexp.search(tmp[-1].split(r':')):

    for information in tmp[4:-1]:
        ion_type_multiplicity = re.split(r':+', information)
        assert len(ion_type_multiplicity) == 2, \
            'Information incorrectly formatted!'
        # skip vol, namee, and color information
        if ion_type_multiplicity[0].lower() \
           not in ['vol', 'color', 'name']:
            assert ion_type_multiplicity[0] in ion_type_names, \
                'Line ' + line + ' unknown iontype!'
            assert np.uint32(ion_type_multiplicity[1]) > 0, \
                'Line ' + line + ' zero or negative multiplicity!'
            assert np.uint32(ion_type_multiplicity[1]) < 256, \
                'Line ' + line + ' unsupport high multiplicity!'
            info['comp'] += [ion_type_multiplicity[0]] \
                * int(ion_type_multiplicity[1])
    return info


class ReadRrngFileFormat():
    """Read *.rrng file format."""

    def __init__(self, filename: str):
        assert len(filename) > 5, 'RRNG file incorrect filename ending!'
        assert filename.lower().endswith('.rrng'), \
            'RRNG file incorrect file type!'
        self.filename = filename

        self.rrng: dict = {}
        self.rrng['ionnames'] = []
        self.rrng['ranges'] = {}
        self.rrng['ions'] = {}

    def read_rrng(self):
        """Read content of an RRNG range file."""
        with open(self.filename, mode='r', encoding='utf8') as rrngf:
            txt = rrngf.read()

        txt = txt.replace('\r\n', '\n')  # pylint: disable=R0801 # windows to unix EOL conversion
        txt = txt.replace(',', '.')  # pylint: disable=R0801 # use decimal dots instead of comma
        txt_stripped = [line for line in txt.split('\n')  # pylint: disable=R0801
                        if line.strip() != '' and line.startswith('#') is False]  # pylint: disable=R0801
        del txt  # pylint: disable=R0801

        # see DOI: 10.1007/978-1-4899-7430-3 for further details to this  # pylint: disable=R0801
        # AMETEK/Cameca's *.rrng file format  # pylint: disable=R0801

        # pylint: disable=R0801 # first, parse [Ions] section, which holds a list of element names
        # pylint: disable=R0801 # there are documented cases where experimentalists add custom strings
        # pylint: disable=R0801 # to specify ranges they consider special
        # pylint: disable=R0801 # these are loaded as user types
        # pylint: disable=R0801 # with isotope_vector np.iinfo(np.uint16).max
        where = [idx for idx, element in
                 enumerate(txt_stripped) if element == '[Ions]']
        assert isinstance(where, list), 'Section [Ions] not found!'
        assert len(where) == 1, 'Section [Ions] not found or ambiguous!'
        current_line_id = where[0] + 1

        tmp = re.split(r'[\s=]+', txt_stripped[current_line_id])
        assert len(tmp) == 2, '[Ions]/Number line corrupted!'
        assert tmp[0] == 'Number', '[Ions]/Number incorrectly formatted!'
        assert tmp[1].isnumeric(), '[Ions]/Number not a number!'
        number_of_ion_names = int(tmp[1])
        assert number_of_ion_names > 0, 'No ion names defined!'
        current_line_id += 1
        for i in np.arange(0, number_of_ion_names):
            tmp = re.split(r'[\s=]+', txt_stripped[current_line_id + i])
            assert len(tmp) == 2, '[Ions]/Ion line corrupted!'
            assert tmp[0] == 'Ion' + str(i + 1), \
                '[Ions]/Ion incorrectly formatted!'
            assert isinstance(tmp[1], str), '[Ions]/Name not a string!'
            self.rrng['ionnames'].append(tmp[1])  # [tmp[0]] = tmp[1]

        # second, parse [Ranges] section
        where = [idx for idx, element in
                 enumerate(txt_stripped) if element == '[Ranges]']
        assert isinstance(where, list), 'Section [Ranges] not found!'
        assert len(where) == 1, 'Section [Ranges] not found or ambiguous!'
        current_line_id = where[0] + 1

        tmp = re.split(r'[\s=]+', txt_stripped[current_line_id])
        assert len(tmp) == 2, '[Ranges]/Number line corrupted!'
        assert tmp[0] == 'Number', '[Ranges]/Number incorrectly formatted!'
        assert tmp[1].isnumeric(), '[Ranges]/Number not a number!'
        number_of_ranges = int(tmp[1])
        assert number_of_ranges > 0, 'No ranges defined!'
        current_line_id += 1

        for i in np.arange(0, number_of_ranges):
            obj = evaluate_rrng_range_line(
                i + 1, txt_stripped[current_line_id + i], self.rrng['ionnames'])

            assert obj != {}, \
                'Line ' + txt_stripped[current_line_id + i] + ' is corrupted!'
            self.rrng['ranges'][obj['identifier']] = obj

        for obj in self.rrng['ranges'].values():
            hashvector = create_isotope_vector(obj['comp'])
            keyword = isotope_vector_to_dict_keyword(hashvector)

            if keyword not in self.rrng['ions'].keys():
                self.rrng['ions'][keyword] = NxIon()
                self.rrng['ions'][keyword].name = NxField(keyword, None)
                self.rrng['ions'][keyword].charge_state = \
                    NxField(np.int32(0), '')
                # RRNG files do not store charge state and isotopes explicitly
                self.rrng['ions'][keyword].isotope_vector = \
                    NxField(hashvector, None)

            self.rrng['ions'][keyword].add_range(
                obj['range'][0], obj['range'][1])

    def report_range(self):
        """Summarize content in a range file."""
        print(self.rrng['ions'])
        print(self.rrng['ranges'])


if __name__ == 'main':
    pass
    # testing
    # parsedFile = ReadRrngFileFormat('../../R31_06365-v02.rrng')
