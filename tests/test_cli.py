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
"""CLI tests for the top-level ``pynx`` dispatcher."""

import builtins

import pytest
from click.testing import CliRunner

from pynxtools.cli import pynx


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def without_nomad_lab(monkeypatch):
    """Simulate an environment where the ``nomad`` extra is not installed."""
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "nomad" or name.startswith("nomad."):
            raise ImportError("No module named 'nomad'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)


class TestPynxGroup:
    """Baseline tests for the top-level dispatcher, independent of
    whether the ``nomad`` extra is installed."""

    def test_lists_all_subcommands(self, runner):
        result = runner.invoke(pynx, ["--help"])
        assert result.exit_code == 0
        for name in (
            "read",
            "convert",
            "validate",
            "generate-eln",
            "inspect-appdef",
            "nomad",
        ):
            assert name in result.output

    def test_unknown_command_fails(self, runner):
        result = runner.invoke(pynx, ["does-not-exist"])
        assert result.exit_code != 0


class TestNomadExtraOptional:
    """Regression test: importing pynxtools.nomad requires nomad-lab, but
    that must not break unrelated ``pynx`` commands."""

    def test_help_lists_nomad_without_importing_it(self, runner, without_nomad_lab):
        result = runner.invoke(pynx, ["--help"])
        assert result.exit_code == 0
        assert "nomad" in result.output

    def test_non_nomad_command_still_works(self, runner, without_nomad_lab):
        result = runner.invoke(pynx, ["validate", "--help"])
        assert result.exit_code == 0

    def test_nomad_command_fails_with_actionable_error(self, runner, without_nomad_lab):
        result = runner.invoke(pynx, ["nomad", "--help"])
        assert result.exit_code != 0
        assert "nomad" in result.output
        assert "pip install" in result.output


class TestNomadExtraPresent:
    """With nomad-lab actually installed, the lazy group must behave like a
    normal eagerly-registered click group (this dev environment has the
    ``nomad`` extra installed, so these run against the real import)."""

    def test_nomad_help_lists_subcommands(self, runner):
        result = runner.invoke(pynx, ["nomad", "--help"])
        assert result.exit_code == 0
        assert "generate-metainfo" in result.output

    def test_nomad_generate_metainfo_help(self, runner):
        result = runner.invoke(pynx, ["nomad", "generate-metainfo", "--help"])
        assert result.exit_code == 0
        assert "--nxdl" in result.output

    def test_nomad_unknown_subcommand_fails(self, runner):
        result = runner.invoke(pynx, ["nomad", "does-not-exist"])
        assert result.exit_code != 0
