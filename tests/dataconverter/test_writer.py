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

import h5py
import numpy as np
import pytest

from pynxtools.dataconverter.exceptions import InvalidDictProvided
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.writer import Writer

from .test_helpers import (  # pylint: disable=unused-import
    alter_dict,
    fixture_filled_test_data,
    fixture_template,
)


@pytest.fixture(name="writer")
def fixture_writer(filled_test_data, tmp_path):
    """pytest fixture to setup Writer object to be used by tests with dummy data."""
    writer = Writer(
        filled_test_data,
        os.path.join(os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"),
        os.path.join(tmp_path, "test.nxs"),
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
    assert test_nxs["/my_entry/nxodd_name/int_value"][()] == 2
    assert test_nxs["/my_entry/nxodd_name/int_value"].attrs["units"] == "eV"
    assert test_nxs["/my_entry/nxodd_name/posint_value"].shape == (3,)  # pylint: disable=no-member


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
        alter_dict(
            filled_test_data,
            "/ENTRY[my_entry]/links/ext_link",
            {"not a link or anything": 2.0},
        ),
        os.path.join(os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"),
        os.path.join(tmp_path, "test.nxs"),
    )
    with pytest.raises(InvalidDictProvided) as execinfo:
        writer.write()
        assert str(execinfo.value) == (
            "pynxtools.dataconverter.exceptions.InvalidDictProvided: "
            "A dictionary was provided to the template but it didn't "
            "fall into any of the know cases of handling dictionaries"
            ". This occurred for: ext_link"
        )


# @pytest.mark.usefixtures("filled_test_data")
@pytest.fixture(name="writer_append")
def fixture_add_to_empty_file_then_attempt_to_append(filled_test_data, tmp_path):
    """pytest fixture to setup Writer object with append mode."""
    with h5py.File(os.path.join(tmp_path, "append.nxs"), "w") as append_file:
        append_file["/already/existing_value"] = 1
    # print(
    #     f">>>>>>>>>>>usual data>>>>>>>>{os.path.join(tmp_path, 'append.nxs')}, {os.path.getsize(os.path.join(tmp_path, 'append.nxs'))}"
    # )

    # "/already/existing_value" is not a key in filled_test_data
    writer = Writer(
        filled_test_data,
        os.path.join(os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"),
        os.path.join(tmp_path, "append.nxs"),
        append=True,
    )
    yield writer
    # print(
    #     f">>>>>>>>>>>after append>>>>>>>>{os.path.join(tmp_path, 'append.nxs')}, {os.path.getsize(os.path.join(tmp_path, 'append.nxs'))}"
    # )
    del writer


def test_append(writer_append):
    """Test whether append is correctly working for the writer."""
    writer_append.write()
    with h5py.File(writer_append.output_path, "r") as append_file:
        assert append_file["/already/existing_value"][()] == 1
        assert append_file["/my_entry/definition"].asstr()[...] == "NXtest"  # pylint: disable=no-member


# @pytest.mark.skip("TODO refactor, test string, scalar, and array datasets")
# @pytest.mark.usefixtures("filled_test_data")
@pytest.fixture(name="writer_overwrite")
def fixture_normal_write_then_attempt_append(writer):
    """pytest fixture to setup Writer object, try to overwrite existent attributes, datasets, and groups."""
    writer.write()
    # = Writer(
    #    filled_test_data,
    #    os.path.join(os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"),
    # #   os.path.join(tmp_path, "overwrite.nxs"),
    # del writer
    print(
        f">>>>>>>>>>>usual data>>>>>>>>{writer.output_path}, {os.path.getsize(writer.output_path)}"
    )

    template = Template()
    template.clear()
    template["/ENTRY[my_entry]/definition"] = "NXtest"
    template["/ENTRY[my_entry]/definition/@version"] = "2.4.6"
    template["/ENTRY[my_entry]/required_group/description"] = "An example description"
    template["/already/existing_value"] = np.zeros((125000,), dtype=np.float64)
    overwrite = Writer(
        template,
        os.path.join(os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"),
        writer.output_path,
        append=True,
    )
    yield overwrite
    print(
        f">>>>>>>>>>>after overwriting>>>>>>>>{overwrite.output_path}, {os.path.getsize(overwrite.output_path)}"
    )
    del writer, overwrite


def test_overwrite(writer_overwrite):
    """Test whether append is correctly working for the writer."""
    writer_overwrite.write()
    # with h5py.File(writer_overwrite.output_path, "r") as append_file:
    #     assert append_file["/already/existing_value"][()] == 1
    #     assert append_file["/my_entry/definition"].asstr()[...] == "NXtest"  # pylint: disable=no-member
