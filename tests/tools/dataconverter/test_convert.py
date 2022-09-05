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
from distutils import file_util
import logging
from click.testing import CliRunner
import pytest
import h5py
from nomad.datamodel import EntryArchive
from nexusparser.tools import nexus  # noqa: E402
import nexusparser.tools.dataconverter.convert as dataconverter
from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
from nexusparser.parser import NexusParser  # noqa: E402


def move_xarray_file_to_tmp(tmp_path):
    """Moves the xarray file, which is used to test linking into the tmp_path directory."""
    test_file_path = os.path.join(os.path.dirname(__file__),
                                  "../../data/tools/dataconverter/readers/mpes")
    file_util.copy_file(os.path.join(test_file_path, "xarray_saved_small_calibration.h5"),
                        os.path.join(tmp_path, "xarray_saved_small_calibration.h5"))


def restore_xarray_file_from_tmp(tmp_path):
    """Restores the xarray file from the tmp_path directory."""
    test_file_path = os.path.join(os.path.dirname(__file__),
                                  "../../data/tools/dataconverter/readers/mpes")
    os.remove(os.path.join(test_file_path, "xarray_saved_small_calibration.h5"))
    file_util.move_file(os.path.join(tmp_path, "xarray_saved_small_calibration.h5"),
                        os.path.join(test_file_path, "xarray_saved_small_calibration.h5"))


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


def test_links_and_virtual_datasets(tmp_path):
    """A test for the convert CLI to check whether a Dataset object is created,

when  the template contains links."""
    move_xarray_file_to_tmp(tmp_path)

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
        os.path.join(tmp_path, "test_output.h5")
    ])

    assert result.exit_code == 0
    test_nxs = h5py.File(os.path.join(tmp_path, "test_output.h5"), "r")
    assert 'entry/test_link/internal_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/internal_link"], h5py.Dataset)
    assert 'entry/test_link/external_link' in test_nxs
    assert isinstance(test_nxs["entry/test_link/external_link"], h5py.Dataset)
    assert 'entry/test_virtual_dataset/concatenate_datasets' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/concatenate_datasets"], h5py.Dataset)
    assert 'entry/test_virtual_dataset/sliced_dataset' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/sliced_dataset"], h5py.Dataset)
    assert test_nxs["entry/test_virtual_dataset/sliced_dataset"].shape == (10, 10, 5)
    assert 'entry/test_virtual_dataset/sliced_dataset2' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/sliced_dataset2"], h5py.Dataset)
    assert test_nxs["entry/test_virtual_dataset/sliced_dataset2"].shape == (10, 10, 10)
    assert 'entry/test_virtual_dataset/sliced_dataset3' in test_nxs
    assert isinstance(test_nxs["entry/test_virtual_dataset/sliced_dataset3"], h5py.Dataset)
    assert test_nxs["entry/test_virtual_dataset/sliced_dataset3"].shape == (10, 10, 10, 2)

    restore_xarray_file_from_tmp(tmp_path)


def test_compression(tmp_path):
    """A test for the convert CLI to check whether a Dataset object is compressed."""

    dirpath = os.path.join(os.path.dirname(__file__),
                           "../../data/tools/dataconverter/readers/example")

    move_xarray_file_to_tmp(tmp_path)

    dataconverter.convert(
        [os.path.join(dirpath, "testdata.json")],
        "example",
        "NXtest",
        os.path.join(tmp_path, "test_output.h5")
    )

    test_nxs = h5py.File(os.path.join(tmp_path, "test_output.h5"), "r")
    assert 'entry/test_compression/compressed_data' in test_nxs
    assert isinstance(test_nxs['/entry/test_compression/compressed_data'], h5py.Dataset)
    assert test_nxs['/entry/test_compression/compressed_data'].compression is 'gzip'
    assert test_nxs['/entry/test_compression/not_to_compress'].compression is None

    restore_xarray_file_from_tmp(tmp_path)


def test_mpes_writing(tmp_path):
    """Check if mpes example can be reproduced"""
    # dataconverter
    dirpath = os.path.join(os.path.dirname(__file__), "../../data/tools/dataconverter/readers/mpes")
    dataconverter.convert((os.path.join(dirpath, "xarray_saved_small_calibration.h5"),
                           os.path.join(dirpath, "config_file.json")),
                          "mpes", "NXmpes",
                          os.path.join(tmp_path, "mpes.small_test.nxs"),
                          False, False)
    # check generated nexus file
    example_data = os.path.join(tmp_path, 'mpes.small_test.nxs')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.\
        FileHandler(os.path.join(tmp_path, 'nexus_test.log'), 'w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, [example_data])
    nexus_helper.process_nexus_master_file(None)
    with open(os.path.join(tmp_path, 'nexus_test.log'), 'r') as logfile:
        log = logfile.readlines()
    with open(os.path.join(dirpath, 'Ref_nexus_mpes.log'), 'r') as logfile:
        Ref_log = logfile.readlines()
    assert log == Ref_log
    # parsing to NOMAD
    archive = EntryArchive()
    import structlog
    NexusParser().parse(example_data, archive, structlog.get_logger())
    assert archive.nexus.nx_application_mpes.\
        nx_group_ENTRY[0].nx_group_PROCESS[0].nx_group_energy_calibration.\
        nx_field_calibrated_axis.nx_value[0] == pytest.approx(-14.264604, rel=1e-6)


def test_inheritance(tmp_path):
    """Checks that appdef inheritance is working correctly"""
    dirpath = os.path.join(os.path.dirname(__file__), "../../data/tools/dataconverter/readers/mpes")

    dataconverter.convert((os.path.join(dirpath, "xarray_saved_small_calibration.h5"),
                           os.path.join(dirpath, "config_file.json"),
                           os.path.join(dirpath, "extended_data.json")),
                          "mpes", "NXmpes_extended",
                          os.path.join(tmp_path, "mpes.small_test.nxs"),
                          False, False)

    with pytest.raises(Exception) as e_info:
        dataconverter.convert((os.path.join(dirpath, "xarray_saved_small_calibration.h5"),
                               os.path.join(dirpath, "config_file.json")),
                              "mpes", "NXmpes_extended",
                              os.path.join(tmp_path, "mpes.small_test.nxs"),
                              False, False)

        assert e_info == \
            "The data entry corresponding to /ENTRY[entry]/test " + \
            "is required and hasn't been supplied by the reader."

    with pytest.raises(Exception):
        dataconverter.convert((os.path.join(dirpath, "extended_data.json")),
                              "mpes", "NXmpes_extended",
                              os.path.join(tmp_path, "mpes.small_test.nxs"),
                              False, False)
