# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
