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

from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_utils \
    import string_to_typed_nparray  # , np_uint16_to_string


class AptFileHeaderMetadata():
    """Information content in the header to an APT(6) file."""

    # we make the variable names as close as possible to the original naming
    # scheme from the source code snippets which AMETEK shared with us
    # when developing the parser for their vendor file format
    def __init__(self):
        # file format signature
        self.c_signature = string_to_typed_nparray('APT\0', 4, np.uint8)
        # byte length of the file header
        self.i_header_size = np.int32(540)
        # version number of the file header, currently expecting 2
        self.i_header_version = np.int32(2)
        # original filename, i.e. *.apt filename, null-terminated UTF-16 !
        self.wc_filename = string_to_typed_nparray('', 256, np.uint16)
        # file creation time
        # according to AMETEK is implemented as a VisualStudio C++ FILETIME
        # 64-bit value, which represents the number of 100-nanosecond intervals
        # since January 1, 1601, as per the MSDN specification
        self.ft_creation_time = np.uint64(0)
        # number of ions represented by file
        self.ll_ion_count = np.uint64(0)  # or an int64 ?

    @classmethod
    def get_numpy_struct(cls) -> np.dtype:  # pylint: disable=R0801
        """Create customized numpy struct to read a file header at once."""  # pylint: disable=R0801
        return np.dtype([('cSignature', np.uint8, (4,)),
                         ('iHeaderSize', np.int32),
                         ('iHeaderVersion', np.int32),
                         ('wcFilename', np.uint16, 256),
                         ('ftCreationTime', np.uint64),
                         ('llIonCount', np.uint64)])  # pylint: disable=R0801

    def set_ll_ion_count(self, value: np.uint64):
        """Check and set total ion count."""
        assert isinstance(value, np.uint64), \
            'llIonCount needs to be an int!'
        assert value > 0, \
            'llIonCount needs to be positive and not zero!'
        assert value <= np.iinfo(np.uint64).max, \
            'llIonCount is too large, needs to map to np.uint64!'
        self.ll_ion_count = np.uint64(value)

    def matches(self, found_header: np.ndarray) -> bool:
        """Compare a read header against expectation."""
        assert np.array_equal(self.c_signature,
                              found_header['cSignature'][0],
                              equal_nan=True), \
            'Header cSignature differs!'
        assert self.i_header_size \
            == found_header['iHeaderSize'][0], \
            'Header iHeaderSize differs!'
        assert self.i_header_version \
            == found_header['iHeaderVersion'][0], \
            'Header iHeaderVersion differs!'
        assert found_header['llIonCount'][0] > 0, \
            'Header indicates there are no ions in the file!'

        self.set_ll_ion_count(found_header['llIonCount'][0])
        return True


# define which header and sections to expect in an *.apt file
# the sections below are referred to as branches in the commercial software
# APSuite enables users select prior I/O which of the sections to write
# normally a range file from based on the exchange with AMETEK and
# expected_header = apt6file_header_metadata()
EXPECTED_HEADER = AptFileHeaderMetadata()
