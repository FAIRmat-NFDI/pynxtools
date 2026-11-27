# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Find the one parser that reads an input file.

A reader registers its ``FileParser`` classes in a ``ParserRegistry`` and asks
it which parser reads each file. The registry raises a clear error when no
parser or more than one parser accepts a file, so files are never skipped or
read by the wrong parser without the user noticing.
"""

import inspect
import os
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from pynxtools.dataconverter.readers.parsers.file_parser import FileParser, MatchResult
from pynxtools.dataconverter.readers.parsers.probe import FileProbe
from pynxtools.dataconverter.readers.parsers.versioning import VersionTuple


class UnsupportedFileError(ValueError):
    """
    No registered parser accepts a file.

    Attributes:
        path: The file.
        reasons: Why each parser rejected the file, by parser class name.
    """

    def __init__(self, path: Path, reasons: dict[str, str]) -> None:
        self.path = path
        self.reasons = reasons
        if reasons:
            details = "\n".join(
                f"  - {name}: {reason}" for name, reason in reasons.items()
            )
        else:
            details = "  (no parsers are registered)"
        super().__init__(f"No parser supports file '{path.name}':\n{details}")


class AmbiguousFormatError(ValueError):
    """
    More than one registered parser accepts a file.

    Attributes:
        path: The file.
        parsers: The parsers that accept it, in registration order.
    """

    def __init__(self, path: Path, parsers: list[type[FileParser]]) -> None:
        self.path = path
        self.parsers = parsers
        names = ", ".join(parser.__name__ for parser in parsers)
        super().__init__(
            f"File '{path.name}' is accepted by more than one parser: {names}. "
            "Their checks must be made stricter so that only one accepts it."
        )


def _as_probe(file: FileProbe | str | os.PathLike) -> FileProbe:
    """Returns ``file`` as a ``FileProbe``. A path is probed first."""
    return file if isinstance(file, FileProbe) else FileProbe.from_path(file)


def _most_specific(
    probe: FileProbe, parsers: list[type[FileParser]]
) -> list[type[FileParser]]:
    """The parsers in ``parsers`` whose matching extension is the longest."""

    def matched_length(parser: type[FileParser]) -> int:
        return max(
            (
                len(ext)
                for ext in parser.supported_file_extensions
                if probe.has_suffix(ext)
            ),
            default=0,
        )

    if not parsers:
        return []
    longest = max(map(matched_length, parsers))
    return [parser for parser in parsers if matched_length(parser) == longest]


class ParserRegistry:
    """
    The parsers of a reader, and the choice of parser for each file.

    Attributes:
        parsers: The registered parsers, in registration order and without
            duplicates.
    """

    def __init__(self, parsers: Iterable[type[FileParser]]) -> None:
        """
        Raises:
            TypeError: If an item is not a concrete ``FileParser`` subclass,
                or two parsers have the same class name (errors name parsers
                by class name, so they could not be told apart).
        """
        self.parsers: tuple[type[FileParser], ...] = tuple(dict.fromkeys(parsers))
        for parser in self.parsers:
            if (
                not isinstance(parser, type)
                or not issubclass(parser, FileParser)
                or inspect.isabstract(parser)
            ):
                raise TypeError(
                    "ParserRegistry takes concrete FileParser subclasses "
                    "(classes, not instances, that implement matches_file and "
                    f"_parse), not {parser!r}."
                )
        counts = Counter(parser.__name__ for parser in self.parsers)
        for name, count in counts.items():
            if count > 1:
                raise TypeError(
                    f"ParserRegistry got more than one parser named '{name}'; "
                    "give each parser a unique class name."
                )

    def _match_all(self, probe: FileProbe) -> dict[type[FileParser], MatchResult]:
        return {parser: parser.match(probe) for parser in self.parsers}

    def claims(self, file: FileProbe | str | os.PathLike) -> list[type[FileParser]]:
        """
        Returns every parser that accepts ``file``, in the order they were
        registered.

        ``file`` can be a path, e.g. ``"spectrum.txt"``, or a ``FileProbe``.
        """
        probe = _as_probe(file)
        return [parser for parser, result in self._match_all(probe).items() if result]

    def identify(self, file: FileProbe | str | os.PathLike) -> type[FileParser]:
        """
        Returns the one parser that reads ``file``.

        ``file`` can be a path, e.g. ``"spectrum.txt"``, or a ``FileProbe``.
        If you also parse the file afterwards, create the ``FileProbe``
        yourself and pass it both here and to ``parse``, so the file is
        probed only once.

        If several parsers accept the file, the one with the longest matching
        extension wins, so a ``.mtex.h5`` parser is chosen over a generic
        ``.h5`` parser. Primary and metadata parsers are checked alike: a file
        accepted by a primary and a metadata parser with equally long
        extensions is ambiguous.

        Raises:
            UnsupportedFileError: If no parser accepts the file.
            AmbiguousFormatError: If more than one parser accepts it with
                equally long extensions.
        """
        probe = _as_probe(file)
        results = self._match_all(probe)
        accepted = [parser for parser, result in results.items() if result]
        if not accepted:
            reasons = {
                parser.__name__: str(result.reason)
                for parser, result in results.items()
            }
            raise UnsupportedFileError(probe.path, reasons)
        candidates = _most_specific(probe, accepted)
        if len(candidates) > 1:
            raise AmbiguousFormatError(probe.path, candidates)
        return candidates[0]

    def metadata_parsers_for(
        self, primary: type[FileParser], version: VersionTuple | str | None = None
    ) -> list[type[FileParser]]:
        """
        The registered parsers that can add metadata to the entries of
        ``primary``.

        These are the parsers that name ``primary`` in ``compatible_primary``,
        whatever their ``role``: a primary parser can add metadata to another
        primary parser's entries, too (see ``FileParser.accepts_primary``).

        Pass ``version``, the version of the primary file that was read (a
        tuple or a string such as ``"1.2"``), to check it against each
        parser's ``supported_primary_versions``.
        """
        return [
            parser
            for parser in self.parsers
            if parser.accepts_primary(primary, version)
        ]

    def ambiguities(
        self, paths: Iterable[str | os.PathLike]
    ) -> dict[Path, list[type[FileParser]]]:
        """
        The files in ``paths`` for which ``identify`` would raise an
        ``AmbiguousFormatError``, with the parsers involved. Directories are
        skipped.

        Meant for tests: a plugin passes its example files, e.g.
        ``Path("tests/data").rglob("*")``, and checks that the result is
        empty.

        Raises:
            TypeError: If ``paths`` is a single path instead of an iterable
                of paths.
            FileNotFoundError: If a path does not exist, so that a wrong path
                cannot make the check pass without checking anything.
        """
        if isinstance(paths, (str, bytes, os.PathLike)):
            raise TypeError(
                "ambiguities takes an iterable of paths, e.g. "
                f"list(Path({str(paths)!r}).rglob('*')), not a single path."
            )
        found: dict[Path, list[type[FileParser]]] = {}
        for path in map(Path, paths):
            if path.is_dir():
                continue
            probe = FileProbe.from_path(path)
            candidates = _most_specific(probe, self.claims(probe))
            if len(candidates) > 1:
                found[path] = candidates
        return found
