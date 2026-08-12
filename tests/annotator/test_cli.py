# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""CLI smoke tests for pynx read."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from pynxtools.annotator.cli import read

ARPES_FILE = str(
    Path(__file__).parent.parent.parent
    / "src"
    / "pynxtools"
    / "data"
    / "201805_WSe2_arpes.nxs"
)


@pytest.fixture()
def runner():
    return CliRunner()


class TestRead:
    def test_annotates_file(self, runner):
        result = runner.invoke(read, [ARPES_FILE])
        assert result.exit_code == 0
        assert len(result.output) > 0

    def test_documentation_option(self, runner):
        result = runner.invoke(read, [ARPES_FILE, "-d", "/entry/instrument/analyser"])
        assert result.exit_code == 0

    def test_concept_option(self, runner):
        result = runner.invoke(
            read, [ARPES_FILE, "-c", "NXarpes/ENTRY/INSTRUMENT/analyser"]
        )
        assert result.exit_code == 0
        assert "entry/instrument/analyser" in result.output

    def test_mutual_exclusion_raises(self, runner):
        result = runner.invoke(
            read,
            [
                ARPES_FILE,
                "-d",
                "/entry/instrument/analyser",
                "-c",
                "/NXarpes/ENTRY/INSTRUMENT/analyser",
            ],
        )
        assert result.exit_code != 0
        assert "Only one option" in result.output

    def test_deprecation_warning_read_nexus(self, runner):
        result = runner.invoke(read, [ARPES_FILE], catch_exceptions=False)
        assert result.exit_code == 0
        # Deprecation warning should NOT appear when invoked via 'read' (not 'read_nexus')
        assert "DeprecationWarning" not in result.output
