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
"""CLI smoke tests for pynx read and pynx inspect-appdef."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from pynxtools.nexus.cli import inspect_appdef


@pytest.fixture()
def runner():
    return CliRunner()


class TestInspectAppdef:
    def test_lists_required_fields(self, runner):
        result = runner.invoke(inspect_appdef, ["NXarpes"])
        assert result.exit_code == 0
        assert "NXarpes" in result.output
        assert "[required+]" in result.output

    def test_optional_level(self, runner):
        result = runner.invoke(inspect_appdef, ["NXarpes", "--level", "optional"])
        assert result.exit_code == 0
        assert "[optional+]" in result.output

    def test_unknown_appdef_fails(self, runner):
        result = runner.invoke(inspect_appdef, ["NXnonexistent_fake_appdef"])
        assert result.exit_code != 0
        assert "not a known application definition" in result.output
