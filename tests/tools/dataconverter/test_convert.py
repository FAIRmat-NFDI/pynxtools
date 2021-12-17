"""Test cases for the convert script used to access the DataConverter."""

from click.testing import CliRunner
import pytest

import nexusparser.tools.dataconverter.convert as dataconverter
from nexusparser.tools.dataconverter.readers.base_reader import BaseReader


def test_get_reader():
    """Unit test for the helper function to get a reader."""
    assert isinstance(dataconverter.get_reader("example")(), BaseReader)


def test_get_names_of_all_readers():
    """Unit test for the helper function to get all readers."""
    assert "base" in dataconverter.get_names_of_all_readers()


@pytest.mark.parametrize("cli_inputs", [
    pytest.param([
        "--nxdl",
        "tests/data/dataconverter/NXspe.nxdl.xml",
        "--generate-template"
    ], id="generate-template"),
    pytest.param([], id="nxdl-not-provided"),
    pytest.param([
        "--nxdl",
        "tests/data/dataconverter/NXspe.nxdl.xml",
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
        assert ("\"/ENTRY[entry]/INSTRUMENT[instrument]/FERMI_CHOPPER"
                "[fermi_chopper]/energy\": \"None\",") in caplog.text
    elif "--input-file" in cli_inputs:
        assert "test_input" in caplog.text
    elif result.exit_code == 2:
        assert "Error: Missing option '--nxdl'" in result.output
