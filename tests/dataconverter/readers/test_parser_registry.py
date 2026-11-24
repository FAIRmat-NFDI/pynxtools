# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for the ParserRegistry that finds the parser for each input file."""

import pytest

from pynxtools.dataconverter.readers.parsers.file_parser import FileParser
from pynxtools.dataconverter.readers.parsers.probe import FileProbe
from pynxtools.dataconverter.readers.parsers.registry import (
    AmbiguousFormatError,
    ParserRegistry,
    UnsupportedFileError,
)


class HeaderParser(FileParser):
    """Accepts ``.txt`` files whose first line is ``header``."""

    supported_file_extensions = (".txt",)
    header = ""

    @classmethod
    def matches_file(cls, probe):
        return probe.head.split(b"\n")[0].decode() == cls.header

    def _parse(self, probe, **options):
        return {}


class SpectrumParser(HeaderParser):
    header = "SPECTRUM"


class ImageParser(HeaderParser):
    header = "IMAGE"


class AnotherSpectrumParser(HeaderParser):
    header = "SPECTRUM"


class ResultsParser(HeaderParser):
    role = "metadata"
    compatible_primary = (SpectrumParser,)
    header = "RESULTS"


class SpectrumNotesParser(HeaderParser):
    role = "metadata"
    compatible_primary = (SpectrumParser,)
    header = "SPECTRUM"


class ImageNotesParser(HeaderParser):
    role = "metadata"
    compatible_primary = (ImageParser,)
    header = "IMAGE NOTES"


class NewResultsParser(ResultsParser):
    """Only works with spectrum files of version 2.0 and newer."""

    supported_primary_versions = (((2, 0), None),)


class GenericTextParser(FileParser):
    """Accepts every ``.txt`` file."""

    supported_file_extensions = (".txt",)

    @classmethod
    def matches_file(cls, probe):
        return True

    def _parse(self, probe, **options):
        return {}


class CalibrationParser(GenericTextParser):
    """Accepts ``.cal.txt`` files."""

    supported_file_extensions = (".cal.txt",)


@pytest.fixture
def write(tmp_path):
    def write_file(name, header):
        path = tmp_path / name
        path.write_text(f"{header}\n1 2 3\n")
        return path

    return write_file


@pytest.fixture
def registry():
    return ParserRegistry([SpectrumParser, ImageParser, ResultsParser])


def test_identify_returns_the_one_matching_parser(registry, write):
    assert (
        registry.identify(FileProbe.from_path(write("a.txt", "IMAGE"))) is ImageParser
    )
    assert (
        registry.identify(FileProbe.from_path(write("b.txt", "RESULTS")))
        is ResultsParser
    )


def test_identify_without_match_lists_every_parser_and_its_reason(registry, write):
    with pytest.raises(UnsupportedFileError) as error:
        registry.identify(FileProbe.from_path(write("a.csv", "IMAGE")))
    assert list(error.value.reasons) == [
        "SpectrumParser",
        "ImageParser",
        "ResultsParser",
    ]
    assert "Supported extensions: .txt" in error.value.reasons["ImageParser"]
    message = str(error.value)
    assert "a.csv" in message
    assert all(name in message for name in error.value.reasons)


def test_identify_with_several_matches_names_them(write):
    registry = ParserRegistry([SpectrumParser, ImageParser, AnotherSpectrumParser])
    with pytest.raises(AmbiguousFormatError) as error:
        registry.identify(FileProbe.from_path(write("a.txt", "SPECTRUM")))
    assert error.value.parsers == [SpectrumParser, AnotherSpectrumParser]
    assert "SpectrumParser, AnotherSpectrumParser" in str(error.value)


def test_the_parser_with_the_longest_matching_extension_wins(write):
    registry = ParserRegistry([GenericTextParser, CalibrationParser])
    calibration = FileProbe.from_path(write("scan.CAL.txt", "anything"))
    plain = FileProbe.from_path(write("scan.txt", "anything"))
    assert registry.claims(calibration) == [GenericTextParser, CalibrationParser]
    assert registry.identify(calibration) is CalibrationParser
    assert registry.identify(plain) is GenericTextParser


def test_a_file_claimed_by_a_primary_and_a_metadata_parser_is_ambiguous(write):
    registry = ParserRegistry([SpectrumParser, SpectrumNotesParser])
    with pytest.raises(AmbiguousFormatError):
        registry.identify(FileProbe.from_path(write("a.txt", "SPECTRUM")))


def test_registry_errors_are_value_errors(registry, write):
    with pytest.raises(ValueError):
        registry.identify(FileProbe.from_path(write("a.txt", "UNKNOWN")))


def test_empty_registry_says_that_no_parsers_are_registered(write):
    with pytest.raises(UnsupportedFileError, match="no parsers are registered"):
        ParserRegistry([]).identify(FileProbe.from_path(write("a.txt", "IMAGE")))


def test_claims_lists_all_accepting_parsers_in_registration_order(write):
    registry = ParserRegistry(
        [AnotherSpectrumParser, ImageParser, SpectrumNotesParser, SpectrumParser]
    )
    probe = FileProbe.from_path(write("a.txt", "SPECTRUM"))
    assert registry.claims(probe) == [
        AnotherSpectrumParser,
        SpectrumNotesParser,
        SpectrumParser,
    ]
    assert registry.claims(FileProbe.from_path(write("b.txt", "OTHER"))) == []


def test_registering_a_parser_twice_keeps_it_once(write):
    registry = ParserRegistry([ImageParser, SpectrumParser, ImageParser])
    assert registry.parsers == (ImageParser, SpectrumParser)
    assert (
        registry.identify(FileProbe.from_path(write("a.txt", "IMAGE"))) is ImageParser
    )


def test_metadata_parsers_for_a_primary_parser():
    registry = ParserRegistry(
        [SpectrumParser, ImageParser, ResultsParser, ImageNotesParser]
    )
    assert registry.metadata_parsers_for(SpectrumParser) == [ResultsParser]
    assert registry.metadata_parsers_for(ImageParser) == [ImageNotesParser]
    assert registry.metadata_parsers_for(ResultsParser) == []


def test_ambiguities_finds_files_claimed_by_several_parsers(write):
    files = [
        write("spectrum.txt", "SPECTRUM"),
        write("image.txt", "IMAGE"),
        write("other.txt", "OTHER"),
    ]
    clean = ParserRegistry([SpectrumParser, ImageParser])
    clashing = ParserRegistry([SpectrumParser, ImageParser, SpectrumNotesParser])
    assert clean.ambiguities(files) == {}
    assert clashing.ambiguities(files) == {
        files[0]: [SpectrumParser, SpectrumNotesParser]
    }


def test_ambiguities_skips_directories_and_files_won_by_a_longer_extension(
    tmp_path, write
):
    (tmp_path / "subfolder").mkdir()
    paths = [
        tmp_path / "subfolder",
        write("scan.cal.txt", "anything"),
        write("scan.txt", "anything"),
    ]
    registry = ParserRegistry([GenericTextParser, CalibrationParser])
    assert registry.ambiguities(paths) == {}


@pytest.mark.parametrize(
    "old_version, new_version",
    [((1, 4), (2, 1)), ("1.4", "2.1")],
    ids=["tuple", "string"],
)
def test_metadata_parsers_for_checks_the_version_of_the_primary_file(
    old_version, new_version
):
    """The version of the primary file decides, given as a tuple or a string."""
    registry = ParserRegistry([SpectrumParser, ResultsParser, NewResultsParser])
    assert registry.metadata_parsers_for(SpectrumParser, version=old_version) == [
        ResultsParser
    ]
    assert registry.metadata_parsers_for(SpectrumParser, version=new_version) == [
        ResultsParser,
        NewResultsParser,
    ]


def test_a_primary_parser_can_also_add_metadata_to_another_primary_parser():
    """A primary parser that names another primary parser is listed, too."""

    class SpectrumExportParser(HeaderParser):
        compatible_primary = (SpectrumParser,)
        header = "EXPORT"

    registry = ParserRegistry([SpectrumParser, ResultsParser, SpectrumExportParser])
    assert SpectrumExportParser.role == "primary"
    assert registry.metadata_parsers_for(SpectrumParser) == [
        ResultsParser,
        SpectrumExportParser,
    ]


class Legacy:
    """A class that is not a FileParser, e.g. a parser written before 2.3."""


class ParserWithoutParse(FileParser):
    """Forgets to implement ``_parse``."""

    supported_file_extensions = (".txt",)

    @classmethod
    def matches_file(cls, probe):
        return True


@pytest.mark.parametrize(
    "parser",
    [
        pytest.param(Legacy, id="not-a-file-parser"),
        pytest.param(SpectrumParser(), id="instance"),
        pytest.param(FileParser, id="base-class"),
        pytest.param(ParserWithoutParse, id="abstract"),
    ],
)
def test_registering_something_other_than_a_parser_class_is_a_type_error(parser):
    with pytest.raises(TypeError, match="concrete FileParser subclasses"):
        ParserRegistry([ImageParser, parser])


def test_two_parsers_with_the_same_name_are_a_type_error():
    def make_parser(first_line):
        class Parser(HeaderParser):
            header = first_line

        return Parser

    with pytest.raises(TypeError, match="more than one parser named 'Parser'"):
        ParserRegistry([make_parser("IMAGE"), make_parser("SPECTRUM")])


def test_ambiguities_rejects_a_single_path(write):
    registry = ParserRegistry([SpectrumParser, SpectrumNotesParser])
    path = write("a.txt", "SPECTRUM")
    for single in (path, str(path)):
        with pytest.raises(TypeError, match="iterable of paths"):
            registry.ambiguities(single)


def test_ambiguities_raises_for_a_missing_file(tmp_path):
    registry = ParserRegistry([SpectrumParser, SpectrumNotesParser])
    with pytest.raises(FileNotFoundError):
        registry.ambiguities([tmp_path / "missing.txt"])
