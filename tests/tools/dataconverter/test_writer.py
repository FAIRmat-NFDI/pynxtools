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
import numpy as np

from nexusparser.tools.dataconverter.writer import Writer


@pytest.fixture(name="writer")
def fixture_writer(tmp_path):
    """pytest fixture to setup Writer object to be used by tests with dummy data."""
    writer = Writer(
        {
            "/ENTRY[my_entry]/NXODD_name/int_value": 2,
            "/ENTRY[my_entry]/NXODD_name/int_value/@units": "eV",
            "/ENTRY[my_entry]/NXODD_name/posint_value": np.zeros(3),
            "/ENTRY[my_entry]/NXODD_name/posint_value/@units": "kg"
        },
        "tests/data/dataconverter/NXtest.nxdl.xml",
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
