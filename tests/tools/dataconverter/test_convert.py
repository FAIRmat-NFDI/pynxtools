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
"""Test cases for the convert script used to access the DataConverter."""

import os
from click.testing import CliRunner
import pytest
import h5py

import nexusparser.tools.dataconverter.convert as dataconverter
from nexusparser.tools.dataconverter.readers.base.reader import BaseReader


def test_get_reader():
    """Unit test for the helper function to get a reader."""
    assert isinstance(dataconverter.get_reader("example")(), BaseReader)


def test_get_names_of_all_readers():
    """Unit test for the helper function to get all readers."""
    assert "example" in dataconverter.get_names_of_all_readers()


@pytest.mark.parametrize("cli_inputs", [
    pytest.param([
        "--nxdl",
        "NXtest",
        "--generate-template"
    ], id="generate-template"),
    pytest.param([], id="nxdl-not-provided"),
    pytest.param([
        "--nxdl",
        "NXtest",
        "--input-file",
        "test_input"
    ], id="input-file")
])
def test_cli(caplog, cli_inputs):
    """A test for the convert CLI."""
    runner = CliRunner()
    result = runner.invoke(dataconverter.convert, cli_inputs)
    if "--generate-template" in cli_inputs:
        assert result.exit_code == 0
        assert "\"/ENTRY[entry]/NXODD_name/int_value\": \"None\"," in caplog.text
    elif "--input-file" in cli_inputs:
        assert "test_input" in caplog.text
    elif result.exit_code == 2:
        assert "Error: Missing option '--nxdl'" in result.output


def test_links_and_virtual_datasets(tmp_path):
    """A test for the convert CLI to check whether a Dataset object is created.

When  the template contains links."""
    runner = CliRunner()
    result = runner.invoke(dataconverter.convert, [
        "--nxdl",
        "NXtest",
        "--reader",
        "example",
        "--input-file",
        f"/home/andrea/NOMAD/nomad/dependencies/parsers/nexus/tests/"
        f"data/tools/dataconverter/readers/example/testdata.json",
        "--output",
        os.path.join(tmp_path, "test_output.h5")
    ])
    test_nxs = h5py.File(os.path.join(tmp_path, "test_output.h5"), "r")
    assert result.exit_code == 0
    assert 'entry/test_link/internal_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/internal_link"], h5py.Dataset)
    assert 'entry/test_link/external_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/external_link"], h5py.Dataset)
    assert 'entry/test_virtual_dataset/concatenate_datasets' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/concatenate_datasets"], h5py.Dataset)
