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

import numpy as np

# from pint import UnitRegistry

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_utils \
    import np_uint16_to_string, string_to_typed_nparray


class AptFileSectionMetadata():
    """Information content in the header to a section in an APT(6) file."""

    def __init__(self):
        # resolved name of the section
        self.meta = {}
        self.meta['section_name'] = ''
        # section format signature
        # or is the c_signature really uint16 ?
        self.meta['c_signature'] = string_to_typed_nparray('SEC\0', 4, np.uint8)
        # byte length of the section header
        self.meta['i_header_size'] = np.int32(0)
        # version number of the section header
        self.meta['i_header_version'] = np.int32(0)
        # string header/title representation of info content in the section
        self.meta['wc_section_type'] = string_to_typed_nparray('', 32, np.uint16)
        # version of this section data
        self.meta['i_section_version'] = np.int32(0)
        # enum value specifying how the records relate to ion
        # 0 (unknown)
        # 1 (one-to-one mapping)
        # 2 (sparse 64bit ion index as first element)
        # 3 (unrelated)
        # 4 (first element is # of indices, then a list, then the record itself
        self.meta['e_relationship_type'] = np.uint32(0)
        # enum value specifying type of record
        # 0 (unknown)
        # 1 (variable size)
        # 2 (variable indexed)
        self.meta['e_record_type'] = np.uint32(0)
        # enum value specifying data type of records
        # 0 (unknown)
        # 1 (int, iDataTypeSize 8, 16, 32, or 64)
        # 2 (uint, iDataTypeSize arbitrary can bit pack within records)
        # 3 (IEEE float 32 or 64)
        # 4 (char string, iDataTypeSize 8, 16
        # iRecordSize of 0 is null terminated
        # iRecordSize > 0 is fixed length
        # 5 (other))
        self.meta['e_record_data_type'] = np.uint32(0)
        # size in bits of data type
        self.meta['i_data_type_size'] = np.int32(0)
        # size of the record (bytes)
        # this must be a multiple of iDataTypeSize/8
        # or 0 for variable length
        self.meta['i_record_size'] = np.int32(0)
        # string representation the unit of the data
        self.meta['wc_data_unit'] = string_to_typed_nparray('', 16, np.uint16)
        self.accepted_units = ['']
        # number of records following this header
        #  do not use for seeking to next section, use llByteCount instead!
        self.meta['ll_record_count'] = np.int64(0)
        # number of bytes following the header
        # this may be > llRecordCount * iRecordSize to allow for padding!
        self.meta['ll_byte_count'] = np.int64(0)

    # we define setters here to implement type checks and thereby
    # remove type and consistency checks out of the main code
    # because the consumer of an *.apt file should not need to deal
    # with the internal byte and format handling that maps from the
    # conventions AMETEK uses and how this maps to numpy arrays

    def set_section_name(self, value: str):
        """Check and set section name."""
        assert isinstance(value, str), 'SectionName must be a string!'
        assert value != '', 'SectionName must not be an empty string!'
        assert len(value) <= 32, \
            'SectionName must not contain more than 32 characters!'
        # SectionName is not null-terminated!
        self.meta['section_name'] = value

    def set_c_signature(self):
        """Check and set c_signature."""
        # assert isinstance(value, str), \
        #     'cSignature needs to be a string!'
        # assert value is not '', \
        #     'cSignature must not be an empty string!'
        # assert len(value) <= 4, \
        #     'cSignature must not contain more than 4 characters!'
        # assert value[-1] == '\0', \
        #     'cSignature needs to include the null-terminator!
        # assert value == 'SEC\0', \
        #    'cSignature must be SEC\0 which is a string!'
        # so far all example file indicated AMETEK implemented 'SEC\0' hard
        self.meta['c_signature'] = string_to_typed_nparray('SEC\0', 4, np.uint8)

    def set_i_header_size(self, value: int):
        """Check and set i_header_size."""
        # assert isinstance(value, int), \
        #     'iHeaderSize needs to be an int!'
        assert value >= 0, \
            'iHeaderSize needs to be positive or zero!'
        assert value <= np.iinfo(np.int32).max, \
            'iHeaderSize too large, needs to map to np.int32!'
        self.meta['i_header_size'] = np.int32(value)

    def set_i_header_version(self, value: int):
        """Check and size i_header_version."""
        # assert isinstance(value, int), \
        #     'iHeaderVersion needs to be an int!'
        assert value >= 0, \
            'iHeaderVersion needs to be positive or zero!'
        assert value <= np.iinfo(np.int32).max, \
            'iHeaderVersion too large, needs to map to np.int32!'
        self.meta['i_header_version'] = np.int32(value)

    def set_wc_section_type(self, value: str):
        """Check and set wc_section_type."""
        assert isinstance(value, str), \
            'wcSectionType needs to be a string!'
        assert value != '', \
            'cSignature must not be an empty string!'
        assert len(value) <= 32, \
            'wcSectionType string must not contain more than 32 characters!'
        # assert value[-1] == '\0', \
        #     'wcSectionType needs to include the null-terminator!'
        self.meta['wc_section_type'] = string_to_typed_nparray(value, 32, np.uint16)

    def set_i_section_version(self, value: int):
        """Check and set i_section_version."""
        # assert isinstance(value, int), \
        #     'iSectionVersion needs to be an int!'
        assert value >= 0, \
            'iSectionVersion needs to be positive or zero!'
        assert value <= np.iinfo(np.int32).max, \
            'iiSectionVersion too large, needs to map to np.int32!'
        self.meta['i_section_version'] = np.int32(value)

    def set_e_relationship_type(self, value: int):
        """Check and set e_relationship_type."""
        # assert isinstance(value, int), \
        #     'eRelationShipType needs to be an int!'
        assert value in [0, 1, 2, 3, 4], \
            'eRelationShipType needs to be from [0, 1, 2, 3, 4]!'
        assert value == 1, \
            'eRelationShipType cannot process 2, 3, and 4, lacking examples!'
        self.meta['e_relationship_type'] = np.uint32(value)

    def set_e_record_type(self, value: int):
        """Check and set e_record_type."""
        # assert isinstance(value, int), \
        #     'eRecordType needs to be an int!'
        assert value in [0, 1, 2], \
            'eRecordType needs to be from [0, 1, 2]!'
        # assert value != 1, \
        #     'eRecordType cannot process 2, 3, and 4, lacking examples!'
        self.meta['e_record_type'] = np.uint32(value)

    def set_e_record_data_type(self, value: int):
        """Check and set e_record_data_type."""
        # assert isinstance(value, int), \
        #     'e_record_data_type needs to be an int!'
        assert value in [0, 1, 2, 3, 4, 5], \
            'eRecordDataType needs to be from [0, 1, 2, 3, 4, 5]!'
        assert value != 5, \
            'eRecordDataType cannot process 5 due to lacking examples!'
        self.meta['e_record_data_type'] = np.uint32(value)

    def set_i_data_type_size(self, value: int):
        """Check and set i_data_type_size."""
        # assert isinstance(value, int), \
        #     'iDataTypeSize needs to be an int!'
        assert value > 0, \
            'iDataTypeSize needs to be positive and not zero!'
        assert value <= np.iinfo(np.int32).max, \
            'iDataTypeSize too large, needs to map to np.int32!'
        self.meta['i_data_type_size'] = np.int32(value)

    def set_i_record_size(self, value: int):
        """Check and set i_record_size."""
        assert isinstance(value, int), \
            'iDataTypeSize needs to be an int!'
        assert value > 0, \
            'iHeaderVersion needs to be positive and not zero!'
        assert value <= np.iinfo(np.int32).max, \
            'iHeaderVersion too large, needs to map to np.int32!'
        self.meta['i_record_size'] = np.int32(value)

    def set_wc_data_unit(self, value: str):
        """Check and set wc_data_unit."""
        assert isinstance(value, str), \
            'wcDataUnit needs to be a string!'
        # can be the empty string is NX_UNITLESS or NX_DIMENSIONLESS
        assert len(value) <= 16, \
            'wcDataUnit must not contain more than 16 characters!'
        # assert value[-1] == '\0', \
        #     'wcDataUnit needs to include the null-terminator!'
        # so far all example file indicated AMETEK implemented 'SEC\0' hard
        self.meta['wc_data_unit'] = string_to_typed_nparray(value, 16, np.uint16)

    def set_accepted_units(self, value: list):
        """Set which unit strings are accepted."""
        # add further checks using e.g. pint
        self.accepted_units = value

    @classmethod
    def get_numpy_struct(cls) -> np.dtype:  # pylint: disable=R0801
        """Create customized numpy struct to read a section header at once."""  # pylint: disable=R0801
        return np.dtype([('cSignature', np.uint8, (4,)),
                         ('iHeaderSize', np.int32),
                         ('iHeaderVersion', np.int32),
                         ('wcSectionType', np.uint16, 32),
                         ('iSectionVersion', np.int32),
                         ('eRelationshipType', np.uint32),
                         ('eRecordType', np.uint32),
                         ('eRecordDataType', np.uint32),
                         ('iDataTypeSize', np.int32),
                         ('iRecordSize', np.int32),
                         ('wcDataUnit', np.uint16, 16),
                         ('llRecordCount', np.uint64),
                         ('llByteCount', np.uint64)])  # pylint: disable=R0801

    def get_ametek_size(self) -> np.uint64:
        """Compute how many byte raw data in bytes to read from AMETEK defs."""
        return np.uint64(self.meta['ll_byte_count'])

    def get_ametek_type(self) -> str:
        """Interpret numpy endianess/datatype from AMETEK defs."""
        byte_length = self.meta['i_data_type_size'] / 8
        assert self.meta['e_record_data_type'] in [1, 2, 3], 'Section ' \
            + np_uint16_to_string(self.meta['wc_section_type']) \
            + ' get_ametek_type() unsupported e_record_data_type!'
        if self.meta['e_record_data_type'] == 1:
            integer_dtypes = {2: '<i2', 4: '<i4', 8: '<i8'}
            assert byte_length in integer_dtypes.keys(), 'Section ' \
                + np_uint16_to_string(self.meta['wc_section_type']) \
                + ' get_ametek_type() detected unsupported integer type!'
            return integer_dtypes[byte_length]
        if self.meta['e_record_data_type'] == 2:
            # uinteger_dtypes = {2: '<u2', 4: '<u4', 8: '<u8'}
            # assert byte_length in uinteger_dtypes.keys(), \
            #    'Section ' + np_uint16_to_string(self.meta['wc_section_type']) \
            #     + ' get_ametek_type() detected \
            #             unsupported unsigned integer type!'
            assert byte_length == 2, 'Section ' \
                + np_uint16_to_string(self.meta['wc_section_type']) \
                + ' get_ametek_type() detected unsupported uint type!'
            # return uinteger_dtypes[byte_length]
            return '<u2'
        if self.meta['e_record_data_type'] == 3:
            # real_dtypes = {4: '<f4', 8: '<f8'}
            # assert byte_length in real_dtypes.keys(), \
            #    'Section ' + np_uint16_to_string(self.meta['wc_section_type']) \
            #    + ' get_ametek_type() detected unsupported real type!'
            assert byte_length == 4, 'Section ' \
                + np_uint16_to_string(self.meta['wc_section_type']) \
                + ' get_ametek_type() detected unsupported real type!'
            # return real_dtypes[byte_length]
            return '<f4'
        return None

    def get_ametek_count(self) -> np.uint64:
        """Interpret how many quantities from AMETEK defs."""
        # this works only for one-to-one mapping !
        # AMETEK has not communicated if the designed adaptive storage layout
        # for *.apt files has ever been implemented
        return self.meta['ll_record_count'] \
            * np.uint64(self.meta['i_record_size'] / (self.meta['i_data_type_size'] / 8))

    def get_ametek_shape(self) -> list:
        """Interpret final numpy shape to use from AMETEK defs."""
        # this works only for one-to-one mapping !
        # AMETEK has not communicated if the designed adaptive storage layout
        # for *.apt files has ever been implemented
        return [
            np.uint64(self.meta['ll_record_count']),
            np.uint64(np.uint64(self.meta['i_record_size']) / (self.meta['i_data_type_size'] / 8))]

    def matches(self, found_section: np.ndarray) -> bool:
        """Compare a read section against expected versioning."""
        # check if the parsed section's metadata are matching
        # AMETEK expectations, i.e. meeting manufacturers definitions?
        assert np.array_equal(self.meta['c_signature'], found_section['cSignature'][0],
                              equal_nan=True), 'Section cSignature differs, \
            is ' + np_uint16_to_string(found_section['cSignature'][0]) \
            + ' but should be ' + np_uint16_to_string(self.meta['c_signature'])

        assert found_section['iHeaderSize'][0] == self.meta['i_header_size'], \
            'Section iHeaderSize differs, is ' \
            + str(found_section['iHeaderSize'][0]) \
            + ' but should be ' + str(self.meta['i_header_size'])

        assert found_section['iHeaderVersion'][0] == self.meta['i_header_version'], \
            'Section iHeaderVersion differs, is ' \
            + str(found_section['iHeaderVersion'][0]) \
            + ' but should be ' + str(self.meta['i_header_version'])

        assert found_section['iSectionVersion'][0] == self.meta['i_section_version'], \
            'Section iSectionVersion differs, is ' \
            + str(found_section['iSectionVersion'][0]) \
            + ' but should be ' + str(self.meta['i_section_version'])

        assert found_section['eRelationshipType'][0] \
            == self.meta['e_relationship_type'], \
            'Section eRelationshipType differs, is ' \
            + str(found_section['eRelationshipType'][0]) \
            + ' but should be ' + str(self.meta['e_relationship_type'])

        assert found_section['eRecordType'][0] == self.meta['e_record_type'], \
            'Section eRecordType differs, is ' \
            + str(found_section['eRecordType'][0]) \
            + ' but should be ' + str(self.meta['e_record_type'])

        assert found_section['eRecordDataType'][0] \
            == self.meta['e_record_data_type'], \
            'Section eRecordDataType differs, is ' \
            + str(found_section['eRecordDataType'][0]) \
            + ' but should be ' + str(self.meta['e_record_data_type'])

        assert found_section['iDataTypeSize'][0] == self.meta['i_data_type_size'], \
            'Section iDataTypeSize differs, is ' \
            + str(found_section['iDataTypeSize'][0]) + ' but should be ' \
            + str(self.meta['i_data_type_size'])

        assert found_section['iRecordSize'][0] == self.meta['i_record_size'], \
            'Section iRecordSize differs, is ' \
            + str(found_section['iRecordSize'][0]) + ' but should be ' \
            + str(self.meta['i_record_size'])

        # ureg = UnitRegistry()
        # ureg.define('da = Da = amu')
        # check if wcDataUnit is of correct quantity
        assert np_uint16_to_string(found_section['wcDataUnit'][0]) \
            in self.accepted_units, 'Section wcDataUnit differs, is ' \
            + np_uint16_to_string(found_section['wcDataUnit'][0]) \
            + ' but should be from accepted_units: ' \
            + ', '.join(self.accepted_units)
        # Q = ureg.Quantity(1, 'amu')
        # use pint for checking compatible base unit

        # check also special cases which this parser currently cannot handle
        # i.e. meeting what we as the community know about the format
        # and thus can handle only
        assert found_section['llByteCount'][0] > 0, \
            'Section llByteCount indicates llByteCount is not > 0 !'

        # modify dynamic quanities that can only be inferred from the file
        self.meta['ll_record_count'] = found_section['llRecordCount'][0]
        self.meta['ll_byte_count'] = found_section['llByteCount'][0]

        return True

    def get_metadata(self) -> dict:
        """Create dictionary of all AMETEK metadata of the section."""
        return \
            {
                'cSignature': np_uint16_to_string(self.meta['c_signature']),
                'iHeaderSize': self.meta['i_header_size'],
                'iHeaderVersion': self.meta['i_header_version'],
                'wcSectionType': np_uint16_to_string(self.meta['wc_section_type']),
                'iSectionVersion': self.meta['i_section_version'],
                'eRelationshipType': self.meta['e_relationship_type'],
                'eRecordType': self.meta['e_record_type'],
                'eRecordDataType': self.meta['e_record_data_type'],
                'iDataTypeSize': self.meta['i_data_type_size'],
                'iRecordSize': self.meta['i_record_size'],
                'wcDataUnit': np_uint16_to_string(self.meta['wc_data_unit']),
                'llRecordCount': self.meta['ll_record_count'],
                'llByteCount': self.meta['ll_byte_count'],
                'AmetekSize': self.get_ametek_size(),
                'AmetekType': self.get_ametek_type(),
                'AmetekCount': self.get_ametek_count(),
                'AmetekShape': ', '.join([str(x)
                                          for x in self.get_ametek_shape()])
            }

    # def set_ll_record_count(self, value: int):
    #     assert isinstance(value, int), \
    #         'llRecordCount needs to be an int!'
    #     assert value >= 0, \
    #         'llRecordCount needs to be at least zero!'
    #     assert value <= np.iinfo(np.int64).max, 'llRecordCount needs to be \
    #         at most '+(str(np.iinfo(np.int64).max))+'!'
    #     self.meta['ll_record_count'] = np.int64(0)

    # def set_ll_byte_count(self, value: int):
    #     assert isinstance(value, int), \
    #         'llByteCount needs to be an int!'
    #     assert value >= 0, \
    #         'llByteCount needs to be at least zero!'
    #     assert value <= np.iinfo(np.int64).max, 'llRecordCount needs to be \
    #         at most '+(str(np.iinfo(np.int64).max))+'!'
    #     self.meta['ll_byte_count'] = np.int64(0)
