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
