# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for the FileParser base class of file-format parsers."""

from pathlib import Path

import pytest

from pynxtools.dataconverter.readers.parsers.file_parser import FileParser
from pynxtools.dataconverter.readers.parsers.parsed_data import ParsedData
from pynxtools.dataconverter.readers.parsers.probe import FileProbe
from pynxtools.dataconverter.readers.parsers.versioning import normalize_version


class ToyParser(FileParser):
    """Reads text files that start with ``TOY``, one entry per line."""

    supported_file_extensions = (".toy", ".mtex.h5")

    @classmethod
    def matches_file(cls, probe):
        return probe.head.startswith(b"TOY")

    def _parse(self, probe, **options):
        lines = probe.path.read_text().splitlines()[1:]
        for number, line in enumerate(lines):
            self._data[f"entry{number}"] = ParsedData(metadata={"line": line})
        self._data.setdefault("options", ParsedData(metadata=dict(options)))


class VersionedToyParser(ToyParser):
    """Reads ``TOY <version>`` files with a version from 1.0 up to 2.0."""

    supported_versions = (((1, 0), (2, 0)),)

    @classmethod
    def detect_version(cls, probe):
        words = probe.head.split(b"\n")[0].split()
        return normalize_version(words[1].decode()) if len(words) > 1 else None


class ToyMetadataParser(ToyParser):
    """Adds metadata to the entries of ``VersionedToyParser``."""

    role = "metadata"
    compatible_primary = (VersionedToyParser,)
    supported_primary_versions = (((1, 5), None),)


def probe_of(path: Path, content: str) -> FileProbe:
    path.write_text(content)
    return FileProbe.from_path(path)


@pytest.mark.parametrize("name", ["scan.toy", "scan.TOY", "scan.MTEX.h5"])
def test_match_accepts_declared_and_compound_suffixes_in_any_case(tmp_path, name):
    result = ToyParser.match(probe_of(tmp_path / name, "TOY\n"))
    assert result
    assert result.reason is None


def test_match_rejects_other_extensions_and_names_the_allowed_ones(tmp_path):
    result = ToyParser.match(probe_of(tmp_path / "scan.h5", "TOY\n"))
    assert not result
    assert "scan.h5" in result.reason
    assert ".toy, .mtex.h5" in result.reason


def test_parser_without_extensions_matches_no_file(tmp_path):
    class NoExtensionParser(ToyParser):
        supported_file_extensions = ()

    result = NoExtensionParser.match(probe_of(tmp_path / "scan.toy", "TOY\n"))
    assert not result
    assert "<none>" in result.reason


@pytest.mark.parametrize(
    "header, accepted, reason_part",
    [
        ("TOY 1.0", True, None),
        ("TOY 1.9.3", True, None),
        ("TOY 2.0", False, "version 2.0"),
        ("TOY 0.9", False, "version 0.9"),
        ("TOY", False, "does not specify a version"),
    ],
)
def test_match_checks_the_detected_version(tmp_path, header, accepted, reason_part):
    result = VersionedToyParser.match(probe_of(tmp_path / "scan.toy", f"{header}\n"))
    assert bool(result) is accepted
    if reason_part:
        assert reason_part in result.reason
        assert "1.0 – 2.0" in result.reason


def test_parser_without_versions_accepts_files_without_version(tmp_path):
    assert ToyParser.match(probe_of(tmp_path / "scan.toy", "TOY\n"))


def test_match_rejects_files_with_other_content(tmp_path):
    result = ToyParser.match(probe_of(tmp_path / "scan.toy", "NOT A TOY\n"))
    assert not result
    assert "does not match the expected format" in result.reason
    assert "ToyParser" in result.reason


def test_match_never_raises_and_reports_the_error(tmp_path):
    class BrokenMatchParser(ToyParser):
        @classmethod
        def matches_file(cls, probe):
            raise KeyError("missing header")

    class BrokenVersionParser(VersionedToyParser):
        @classmethod
        def detect_version(cls, probe):
            raise ValueError("unreadable header")

    probe = probe_of(tmp_path / "scan.toy", "TOY 1.0\n")
    match_result = BrokenMatchParser.match(probe)
    version_result = BrokenVersionParser.match(probe)
    assert not match_result
    assert "missing header" in match_result.reason
    assert not version_result
    assert "unreadable header" in version_result.reason


def test_match_needs_no_parser_instance_and_no_file_access(tmp_path):
    class NoInstanceParser(ToyParser):
        def __init__(self):
            raise AssertionError("match must not create a parser")

    path = tmp_path / "scan.toy"
    probe = probe_of(path, "TOY\n")
    path.unlink()
    assert NoInstanceParser.match(probe)


def test_parse_fills_entries_and_passes_options(tmp_path):
    parser = ToyParser()
    parser.parse(probe_of(tmp_path / "scan.toy", "TOY\nfirst\nsecond\n"), mode="fast")
    assert list(parser.data) == ["entry0", "entry1", "options"]
    assert parser.data["entry1"].get_metadata("line") == "second"
    assert parser.data["options"].metadata == {"mode": "fast"}


def test_parse_sets_the_source_of_each_entry_unless_the_parser_did(tmp_path):
    other = tmp_path / "other.toy"

    class SourceParser(ToyParser):
        def _parse(self, probe, **options):
            self._data["own"] = ParsedData(source=other)
            self._data["default"] = ParsedData()

    path = tmp_path / "scan.toy"
    parser = SourceParser()
    parser.parse(probe_of(path, "TOY\n"))
    assert parser.data["own"].source == other
    assert parser.data["default"].source == path


def test_parse_does_not_repeat_the_checks(tmp_path):
    probe = probe_of(tmp_path / "scan.txt", "NOT A TOY\nline\n")
    assert not ToyParser.match(probe)
    parser = ToyParser()
    parser.parse(probe)
    assert parser.data["entry0"].get_metadata("line") == "line"


def test_parse_again_drops_the_entries_of_the_previous_file(tmp_path):
    parser = ToyParser()
    parser.parse(probe_of(tmp_path / "first.toy", "TOY\na\nb\n"))
    parser.parse(probe_of(tmp_path / "second.toy", "TOY\nc\n"))
    assert list(parser.data) == ["entry0", "options"]


def test_metadata_parser_accepts_compatible_primary_parsers():
    class NewerPrimary(VersionedToyParser):
        supported_versions = (((1, 8), (3, 0)),)

    assert ToyMetadataParser.accepts_primary(VersionedToyParser)
    assert ToyMetadataParser.accepts_primary(NewerPrimary)


def test_metadata_parser_rejects_other_parsers_with_reason():
    result = ToyMetadataParser.accepts_primary(ToyParser)
    assert not result
    assert "VersionedToyParser" in result.reason


def test_metadata_parser_rejects_primary_parsers_without_version_overlap():
    class OldPrimary(VersionedToyParser):
        supported_versions = (((1, 0), (1, 5)),)

    result = ToyMetadataParser.accepts_primary(OldPrimary)
    assert not result
    assert "no overlap" in result.reason


def test_only_metadata_parsers_accept_primary_parsers():
    class EmptyMetadataParser(ToyParser):
        role = "metadata"

    primary_result = VersionedToyParser.accepts_primary(VersionedToyParser)
    empty_result = EmptyMetadataParser.accepts_primary(VersionedToyParser)
    assert not primary_result
    assert "not a metadata parser" in primary_result.reason
    assert not empty_result
    assert "no compatible primary parsers" in empty_result.reason


def test_match_rejects_a_version_that_is_not_a_tuple(tmp_path):
    class TextVersionParser(VersionedToyParser):
        @classmethod
        def detect_version(cls, probe):
            return "1.2"

    result = TextVersionParser.match(probe_of(tmp_path / "scan.toy", "TOY 1.2\n"))
    assert not result
    assert "'1.2'" in result.reason
    assert "normalize_version" in result.reason


@pytest.mark.parametrize("name", ["matches_file", "detect_version"])
def test_checks_must_be_class_methods(name):
    def instance_check(self, file):
        return True

    with pytest.raises(TypeError, match=f"{name} must be a classmethod"):
        type("OldStyleParser", (ToyParser,), {name: instance_check})


@pytest.mark.parametrize("extensions", [".toy", ("",), (".toy", None)])
def test_extensions_must_be_a_tuple_of_non_empty_strings(extensions):
    with pytest.raises(TypeError, match="tuple of non-empty strings"):
        type(
            "BadExtensionParser",
            (ToyParser,),
            {"supported_file_extensions": extensions},
        )
