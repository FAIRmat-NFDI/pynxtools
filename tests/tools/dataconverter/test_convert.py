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


@pytest.mark.parametrize("cli_inputs", [
    pytest.param([
        "--nxdl",
        "NXcontainer",
    ], id="exists-in-contributed"),
    pytest.param([
        "--nxdl",
        "NXarchive",
    ], id="exists-in-applications"),
    pytest.param([
        "--nxdl",
        "NXdoesnotexist",
    ], id="does-not-exist")
])
def test_find_nxdl(cli_inputs):
    """Unit test to check if dataconverter can find NXDLs in contributed/applications folder."""
    runner = CliRunner()
    result = runner.invoke(dataconverter.convert_cli, cli_inputs)
    if "NXdoesnotexist" in cli_inputs:
        assert isinstance(result.exception, FileNotFoundError)
    else:
        assert isinstance(result.exception, Exception)
        assert "The chosen NXDL isn't supported by the selected reader." in str(result.exception)


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
    result = runner.invoke(dataconverter.convert_cli, cli_inputs)
    if "--generate-template" in cli_inputs:
        assert result.exit_code == 0
        assert "\"/ENTRY[entry]/NXODD_name/int_value\": \"None\"," in caplog.text
    elif "--input-file" in cli_inputs:
        assert "test_input" in caplog.text
    elif result.exit_code == 2:
        assert "Error: Missing option '--nxdl'" in result.output


def test_links_and_virtual_datasets():
    """A test for the convert CLI to check whether a Dataset object is created,

when  the template contains links."""

    dirpath = os.path.join(os.path.dirname(__file__),
                           "../../data/tools/dataconverter/readers/example")
    runner = CliRunner()
    result = runner.invoke(dataconverter.convert_cli, [
        "--nxdl",
        "NXtest",
        "--reader",
        "example",
        "--input-file",
        os.path.join(dirpath, "testdata.json"),
        "--output",
        os.path.join(dirpath, "test_output.h5")
    ])

    assert result.exit_code == 0
    test_nxs = h5py.File(os.path.join(dirpath, "test_output.h5"), "r")
    assert 'entry/test_link/internal_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/internal_link"], h5py.Dataset)
    assert 'entry/test_link/external_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/external_link"], h5py.Dataset)
    assert 'entry/test_virtual_dataset/concatenate_datasets' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/concatenate_datasets"], h5py.Dataset)


def test_compression():
    """A test for the convert CLI to check whether a Dataset object is compressed."""

    dirpath = os.path.join(os.path.dirname(__file__),
                           "../../data/tools/dataconverter/readers/ellips")
    runner = CliRunner()
    result = runner.invoke(dataconverter.convert_cli, [
        "--nxdl",
        "NXellipsometry",
        "--reader",
        "ellips",
        "--input-file",
        os.path.join(dirpath, "test.yaml"),
        "--output",
        os.path.join(dirpath, "ellips.test.nxs")
    ])

    assert result.exit_code == 0

    test_h5 = h5py.File(os.path.join(dirpath, "test.h5"), "r")
    assert 'wavelength' in test_h5 \
        and isinstance(test_h5['wavelength'], h5py.Dataset) \
        and test_h5['wavelength'].compression is 'gzip'

    test_nxs = h5py.File(os.path.join(dirpath, "ellips.test.nxs"), "r")
    assert 'entry/sample/wavelength' in test_nxs \
        and isinstance(test_nxs['entry/sample/wavelength'], h5py.Dataset) \
        and test_nxs['entry/sample/wavelength'].compression is 'gzip'

    assert 'entry/sample/measured_data' in test_nxs \
        and isinstance(test_nxs['entry/sample/measured_data'], h5py.Dataset) \
        and test_nxs['entry/sample/measured_data'].compression is 'gzip'

    assert 'entry/instrument/angular_spread' in test_nxs \
        and isinstance(test_nxs['entry/instrument/angular_spread'], h5py.Dataset) \
        and test_nxs['entry/instrument/angular_spread'].compression is not 'gzip'

    assert 'entry/experiment_identifier' in test_nxs \
        and isinstance(test_nxs['entry/experiment_identifier'], h5py.Dataset) \
        and test_nxs['entry/experiment_identifier'].compression is not 'gzip'


def test_mpes_writing():
    """Check if mpes example can be reproduced"""
    dirpath = os.path.join(os.path.dirname(__file__), "../../data/tools/dataconverter/readers/mpes")
    dataconverter.convert((os.path.join(dirpath, "MoTe_xarray_final.h5"),
                           os.path.join(dirpath, "config_file.json")),
                          "mpes", "NXmpes",
                          os.path.join(dirpath, "mpes2.test.nxs"),
                          False, False)
