#!/usr/bin/env python3
"""AMETEK APT(6) data exchange file reader used by atom probe microscopists."""

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

import os

# import mmap

import numpy as np

import pandas as pd

# from pint import UnitRegistry

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_utils \
    import np_uint16_to_string
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_headers \
    import AptFileHeaderMetadata
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_sections \
    import AptFileSectionMetadata
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_sections_branches \
    import EXPECTED_SECTIONS
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_utils \
    import NxField, get_memory_mapped_data


class ReadAptFileFormat():
    """Read AMETEK's open exchange *.apt file format."""

    def __init__(self, filename: str):
        assert len(filename) > 4, 'APT file incorrect filename ending!'
        assert filename.lower().endswith('.apt'), \
            'APT file incorrect file type!'
        self.filename = filename

        self.filesize = os.path.getsize(self.filename)
        print('Reading ' + self.filename + ' which is ' + str(self.filesize) + ' bytes')

        self.header_section = None
        self.byte_offsets = {}
        self.available_sections = {}
        # where do sections start bytes from beginning of the file?
        self.apt = {}

        self.parse_file_structure()

    def parse_file_structure(self):
        """Parse APT file header plus flat collection of metadata/data pairs.

        Each pair has a so-called section header and a corresponding raw data
        block. Section headers detail the content of the immediately trailing
        raw data block.
        An APT file can store none, some, or all of the possible sections.
        Furthermore the file can contain additional pieces of information
        which this parser cannot read-out because the APT format is maintained
        by AMETEK. The AMETEK source code is the only reliable source of
        information about which content the sections encode and how these
        get formatted when exporting an APT file from APSuite for a specific
        version and build number and type of experiment plus
        combinations of settings.
        Parse header of the file and check which parsable sections the file
        contains get the byte offsets of the sections from the beginning
        relative to the start/beginning of the file.
        """
        self.byte_offsets = {}
        self.header_section = None
        self.available_sections = {}

        with open(self.filename, 'rb') as file_handle:
            self.dummy_header = AptFileHeaderMetadata()
            found_header = np.fromfile(file_handle,
                                       self.dummy_header.get_numpy_struct(),
                                       count=1)

            assert self.dummy_header.matches(found_header), \
                'Found an unexpectedly formatted/versioned header! \
                Please contact the development team to help us inspect \
                the matter.'
            print('File describes ' + str(found_header['llIonCount'][0]) + ' ions')

            self.header_section = found_header
            self.byte_offsets['header'] = np.uint64(file_handle.tell())
            print(self.byte_offsets['header'])

            end_of_file_not_reached = b'yes'
            while end_of_file_not_reached != b'':
                # probe for end of file
                end_of_file_not_reached = file_handle.read(1)
                if end_of_file_not_reached != b'':
                    file_handle.seek(-1, os.SEEK_CUR)
                else:
                    print('End of file at ' + str(file_handle.tell()) + ' bytes')
                    break

                dummy_section = AptFileSectionMetadata()
                found_section = np.fromfile(file_handle,
                                            dummy_section.get_numpy_struct(),
                                            count=1)
                keyword = np_uint16_to_string(
                    found_section['wcSectionType'][0])

                assert keyword not in self.available_sections.keys(), \
                    'Found a duplicate of an already parsed section! Please \
                    contact the development team as we have never encountered \
                    an example of such a section duplication and here seems \
                    to be an example to inspect the matter.'
                assert keyword in EXPECTED_SECTIONS.keys(), \
                    'Found an unknown section, seems like an unknown/new \
                    branch! Please contact the development team to enable us \
                    to contact AMETEK and discuss the situation.'

                metadata_section = EXPECTED_SECTIONS[keyword]
                assert metadata_section.matches(found_section), \
                    'Found an uninterpretable section! Please contact the \
                    development team to help us fixing this.'
                self.available_sections[keyword] = metadata_section

                self.byte_offsets[keyword] = np.uint64(file_handle.tell())
                if keyword == 'Position':
                    # special case six IEEE 32-bit floats preceeding raw data
                    self.byte_offsets[keyword] += np.uint64(6 * 4)
                self.byte_offsets[keyword] += np.uint64(
                    found_section['llByteCount'][0])
                print('Byte offset for reading data for section: ' + keyword)
                print(self.byte_offsets[keyword])
                # print(file_handle.tell())
                file_handle.seek(self.byte_offsets[keyword], os.SEEK_SET)
                # print(file_handle.tell())

    # one convenience reader function for every known section
    # is useful because it structures the parsers, enables reading the file
    # partially and reduces main memory consumption during full parsing
    def get_header(self):
        """Report metadata in the header."""
        metadata_dict = {
            'cSignature':
                np_uint16_to_string(self.header_section['cSignature'][0]),
            'iHeaderSize':
                np.int32(self.header_section['iHeaderSize'][0]),
            'iHeaderVersion':
                np.int32(self.header_section['iHeaderVersion'][0]),
            'wcFilename':
                np_uint16_to_string(self.header_section['wcFilename'][0]),
            'ftCreationTime':
                np.uint64(self.header_section['ftCreationTime'][0]),
            'llIonCount':
                np.uint64(self.header_section['llIonCount'][0])}
        # check e.g. https://gist.github.com/Mostafa-Hamdy-Elgiar/
        # 9714475f1b3bc224ea063af81566d873 repo
        # for converting Windows/MSDN time to Python time
        for key, value in iter(metadata_dict.items()):
            print(key + ': ' + str(value))

    def get_metadata(self, keyword: str):
        """Report available metadata for quantity if it exists."""
        if keyword in self.available_sections.keys() \
           and keyword in self.byte_offsets.keys():
            metadata_dict = self.available_sections[keyword].get_metadata()
            for key, value in iter(metadata_dict.items()):
                print(key + ': ' + str(value))

    def get_metadata_table(self):
        """Create table from all metadata for each section."""
        column_names = ['section']  # header
        assert 'Mass' in self.available_sections.keys(), \
            'Cannot create table, Mass section not available to guide \
                the creation of the table header!'
        for key in self.available_sections['Mass'].get_metadata().keys():
            column_names.append(key)
        data_frame = pd.DataFrame(columns=column_names)

        for keyword, value in self.available_sections.items():
            row = {'section': keyword}
            row = row | value.get_metadata()
            data_frame = data_frame.append(row, ignore_index=True)

        return data_frame

    def get_named_quantity(self, keyword: str):
        """Read quantity with name in keyword from APT file if it exists."""
        if keyword in self.available_sections.keys() \
           and keyword in self.byte_offsets.keys():
            byte_position_start = self.byte_offsets[keyword] \
                - self.available_sections[keyword].get_ametek_size()
            print('Reading section ' + keyword + ' at ' + str(byte_position_start))

            dtype = self.available_sections[keyword].get_ametek_type()
            offset = byte_position_start
            stride = np.uint64(
                self.available_sections[keyword].meta['i_data_type_size'] / 8)
            count = self.available_sections[keyword].get_ametek_count()

            data = get_memory_mapped_data(
                self.filename, dtype, offset, stride, count)

            shape = tuple(self.available_sections[keyword].get_ametek_shape())
            unit = self.available_sections[keyword].meta['wc_data_unit']

            return NxField(
                np.reshape(data, newshape=shape), np_uint16_to_string(unit))

        return NxField()

    def get_mass_to_charge_state_ratios(self):
        """Read mass-to-charge."""
        return self.get_named_quantity('Mass')

    def get_reconstructed_positions(self):
        """Read reconstructed positions."""
        return self.get_named_quantity('Position')


# examples how to use functionalities of this file format parser
# prefix = 'E:/Theobook165/GITHUB/FAIRMAT-PARSER/fairmat_areab_parser \
#    /tutorials/aptfim/examples/deu_duesseldorf_mpie'
# prefix = 'E:/Theobook165/FHI_FHI_FHI/Paper/xxxx_ParaprobeAnalytics \
#    AsAFairMatPlugin/research/database/ger_duesseldorf_antonov'
# prefix = prefix = 'E:/Theobook165/FHI_FHI_FHI/Paper/xxxx_ParaprobeAnalytics \
#    AsAFairMatPlugin/research/database/ger_duesseldorf_saxena'
# these two files are corrupted
# TEST_FILE_NAME = 'FlatTest_f903a3f2-6aa0-4019-9890-3c983b43d513.apt'
# TEST_FILE_NAME = prefix + '/' + 'c2fe4adf-f6f4-44aa-b6ec-76345fe88269.apt'
# tested with the next three worked nicely the above two were created with
# development stage APSuite versions, it turned out that file corruptions
# were tracable with the above two thus representing case of bugs in APSuite
# TEST_FILE_NAME = prefix + '/' + 'R5006_29110_Top_Level_ROI.apt'
# TEST_FILE_NAME = prefix + '/' + 'D1_High_Hc_R5076_52126.apt'
# test cases how to use the parser
# TEST_FILE_NAME = '70_50_50.apt'  # Xuyang Zhou's (MPIE) \
# Alexander Reichmann's (Leoben) test case
# parsedFile = ReadAptFileFormat(TEST_FILE_NAME)
# metadata_table = parsedFile.get_metadata_table()
# parsedFile.get_metadata('Position')
# parsedFile.get_header()
# xyz = parsedFile.get_reconstructed_positions()
# mq = parsedFile.get_mass_to_charge_state_ratios()
# mq = parsedFile.get_named_quantity('Mass')
