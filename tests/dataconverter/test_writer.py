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
"""Test cases for the Writer class used by the DataConverter"""

import os

import pytest
import h5py
from pynxtools.dataconverter.exceptions import InvalidDictProvided


from pynxtools.dataconverter.writer import Writer
from .test_helpers import fixture_filled_test_data, fixture_template, alter_dict  # pylint: disable=unused-import


@pytest.mark.usefixtures("filled_test_data")
@pytest.fixture(name="writer")
def fixture_writer(filled_test_data, tmp_path):
    """pytest fixture to setup Writer object to be used by tests with dummy data."""
    writer = Writer(
        filled_test_data,
        os.path.join("tests", "data", "dataconverter", "NXtest.nxdl.xml"),
        os.path.join(tmp_path, "test.nxs")
    )
    yield writer
    del writer


def test_init(writer):
    """Test to verify Writer's initialization works."""
    assert isinstance(writer, Writer)


def test_write(writer):
    """Test for the Writer's write function. Checks whether entries given above get written out."""
    writer.write()
    test_nxs = h5py.File(writer.output_path, "r")
    assert test_nxs["/my_entry/NXODD_name/int_value"][()] == 2
    assert test_nxs["/my_entry/NXODD_name/int_value"].attrs["units"] == "eV"
    assert test_nxs["/my_entry/NXODD_name/posint_value"].shape == (3,)  # pylint: disable=no-member


def test_write_link(writer):
    """Test for the Writer's write function.

Checks whether entries given above get written out when a dictionary containing a link is
given in the template dictionary."""
    writer.write()
    test_nxs = h5py.File(writer.output_path, "r")
    assert isinstance(test_nxs["/my_entry/links/ext_link"], h5py.Dataset)


@pytest.mark.usefixtures("filled_test_data")
def test_wrong_dict_provided_in_template(filled_test_data, tmp_path):
    """Tests if the writer correctly fails when a wrong dictionary is provided"""
    writer = Writer(
        alter_dict(filled_test_data,
                   "/ENTRY[my_entry]/links/ext_link",
                   {"not a link or anything": 2.0}),
        os.path.join("tests", "data", "dataconverter", "NXtest.nxdl.xml"),
        os.path.join(tmp_path, "test.nxs")
    )
    with pytest.raises(InvalidDictProvided) as execinfo:
        writer.write()
        assert str(execinfo.value) == ("pynxtools.dataconverter.exceptions.InvalidDictProvided: "
                                       "A dictionary was provided to the template but it didn't "
                                       "fall into any of the know cases of handling dictionaries"
                                       ". This occured for: ext_link")
