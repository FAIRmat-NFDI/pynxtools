# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""The base class for parsers of one file format.

A parser declares which files it reads (extensions, versions, vendor) and
recognizes them from a ``FileProbe``, without creating a parser or opening
the file again. ``match`` says whether a file belongs to the parser, and why
not if it doesn't, so a reader can explain a file that no parser accepted.
``parse`` then reads the file into one ``ParsedData`` objects.

A parser can also add metadata to the entries of another parser, e.g. a
quantification export next to the spectra. It names those primary parsers
in ``compatible_primary``. A metadata parser only does that, while a primary
parser with ``compatible_primary`` can also create entries on its own.
"""

import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Literal

from pynxtools.dataconverter.readers.parsers.parsed_data import ParsedData
from pynxtools.dataconverter.readers.parsers.probe import FileProbe
from pynxtools.dataconverter.readers.parsers.versioning import (
    VersionRange,
    VersionTuple,
    format_version,
    format_version_ranges,
    is_version_supported,
    normalize_version,
    version_ranges_overlap,
)


@dataclass(frozen=True)
class MatchResult:
    """
    The outcome of a check: true if it passed, otherwise false with a reason.

    Attributes:
        reason: Why the check failed, or ``None`` if it passed.
    """

    reason: str | None = None

    def __bool__(self) -> bool:
        return self.reason is None


def _as_version_tuple(version: Any) -> VersionTuple | None:
    """
    ``version`` as a version tuple: a string goes through
    ``normalize_version``, a tuple or ``None`` is kept.

    Raises:
        TypeError: If ``version`` is of another type.
        ValueError: If a string has no version in it.
    """
    if version is None or isinstance(version, tuple):
        return version
    if isinstance(version, str):
        return normalize_version(version)
    raise TypeError(
        f"got {version!r} instead of a version tuple or a string, e.g. '1.2'."
    )


class FileParser(ABC):
    """
    A parser for one file format.

    Subclasses set ``supported_file_extensions`` and implement
    ``matches_file`` and ``_parse``. Version-aware parsers also set
    ``supported_versions`` and implement ``detect_version``.

    Attributes:
        supported_file_extensions: The file name endings this parser reads,
            e.g. ``(".sle",)`` or ``(".mtex.h5",)``. Upper and lower case
            are treated alike, so ``.sle`` also matches ``scan.SLE``.
            A parser without extensions matches no file.
        supported_versions: Half-open version ranges
            ``(lower_inclusive, upper_exclusive_or_None)``. Empty means any
            file, with or without a version. Otherwise a file must have a
            version within one of the ranges.
        supported_vendor: The instrument or software vendor, for
            documentation. It is not checked.
        role: ``"primary"`` for a parser that can create entries on its own,
            ``"metadata"`` for one that only adds metadata to the entries of
            the parsers in ``compatible_primary``.
        compatible_primary: The primary parsers (including their subclasses)
            whose entries this parser can add metadata to, whatever its
            ``role``. Empty means none.
        supported_primary_versions: The versions of those primary parsers
            this parser works with. Empty means any version.
    """

    supported_file_extensions: ClassVar[tuple[str, ...]] = ()
    supported_versions: ClassVar[tuple[VersionRange, ...]] = ()
    supported_vendor: ClassVar[str | None] = None
    role: ClassVar[Literal["primary", "metadata"]] = "primary"
    compatible_primary: ClassVar[tuple[type["FileParser"], ...]] = ()
    supported_primary_versions: ClassVar[tuple[VersionRange, ...]] = ()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Check the declarations of a parser class when it is defined, so that
        mistakes show up at import instead of as rejected files.

        Raises:
            TypeError: If ``matches_file`` or ``detect_version`` is not a
                classmethod, or ``supported_file_extensions`` is not a tuple
                of non-empty strings.
        """
        super().__init_subclass__(**kwargs)
        for name in ("matches_file", "detect_version"):
            if not isinstance(inspect.getattr_static(cls, name), classmethod):
                raise TypeError(
                    f"{cls.__name__}.{name} must be a classmethod that takes a "
                    "FileProbe, e.g. `@classmethod def "
                    f"{name}(cls, probe): ...`."
                )
        extensions = cls.supported_file_extensions
        if not isinstance(extensions, tuple) or not all(
            isinstance(ext, str) and ext for ext in extensions
        ):
            raise TypeError(
                f"{cls.__name__}.supported_file_extensions must be a tuple of "
                f"non-empty strings, e.g. ('.sle',), not {extensions!r}."
            )

    def __init__(self) -> None:
        self._data: dict[str, ParsedData] = {}

    @property
    def data(self) -> dict[str, ParsedData]:
        """What the last ``parse`` call read, keyed by a name the parser chooses."""
        return self._data

    @classmethod
    def detect_version(cls, probe: FileProbe) -> VersionTuple | str | None:
        """
        The version of the file format, or ``None`` if the file has none.

        Return a version tuple, or the version string as it is written in
        the file, e.g. ``"4.75"``; ``match`` converts a string with
        ``normalize_version``.

        Override this in version-aware parsers, e.g. to read a version from
        the file header in ``probe.head``.
        """
        return None

    @classmethod
    @abstractmethod
    def matches_file(cls, probe: FileProbe) -> bool:
        """
        Whether the file has the structure of this format.

        Check the content, not only the file name, e.g. a header line, HDF5
        keys or TIFF tags of ``probe``. The check should be cheap, since it
        runs for every input file and every parser.
        """

    @classmethod
    def match(cls, probe: FileProbe) -> MatchResult:
        """
        Whether this parser reads the file of ``probe``, and why not if it
        doesn't.

        Checks the extension, then ``matches_file``, then the version. So a
        file of another format with the same extension is rejected for its
        format, and ``detect_version`` only reads files of this format. It
        never raises: an error in ``matches_file`` or ``detect_version``
        becomes the reason of the result.
        """
        name = probe.path.name
        if not any(probe.has_suffix(ext) for ext in cls.supported_file_extensions):
            allowed = ", ".join(cls.supported_file_extensions) or "<none>"
            return MatchResult(
                f"File '{name}' does not have an extension that {cls.__name__} "
                f"supports. Supported extensions: {allowed}."
            )
        # matches_file and detect_version are plugin code, so any error is
        # possible (e.g. sqlite3.DatabaseError, zipfile.BadZipFile). It
        # becomes the reason, so one parser failing on another format's file
        # does not stop the other parsers from being checked.
        try:
            matches = cls.matches_file(probe)
        except Exception as error:
            return MatchResult(
                f"{cls.__name__} could not check '{name}': "
                f"{type(error).__name__}: {error}"
            )
        if not matches:
            return MatchResult(
                f"File '{name}' does not match the expected format of {cls.__name__}."
            )

        try:
            version = _as_version_tuple(cls.detect_version(probe))
        except Exception as error:
            return MatchResult(
                f"{cls.__name__} could not read the version of '{name}': "
                f"{type(error).__name__}: {error}"
            )
        if not is_version_supported(version, cls.supported_versions):
            supported = format_version_ranges(cls.supported_versions)
            if version is None:
                return MatchResult(
                    f"File '{name}' does not specify a version, but "
                    f"{cls.__name__} requires one. Supported versions: {supported}."
                )
            return MatchResult(
                f"File '{name}' has version {format_version(version)}, which "
                f"{cls.__name__} does not support. Supported versions: {supported}."
            )
        return MatchResult()

    @classmethod
    def accepts_primary(
        cls,
        primary: type["FileParser"],
        version: VersionTuple | str | None = None,
    ) -> MatchResult:
        """
        Whether this parser can add metadata to the entries of ``primary``,
        and why not if it can't. This works for any ``role``: what counts is
        ``compatible_primary``.

        ``primary`` must be one of ``compatible_primary`` or a subclass of
        one. If ``supported_primary_versions`` is set, the version is checked
        as well:

        - with ``version``, the version of the primary file that was read
          (from ``primary.detect_version``), that version must be within
          ``supported_primary_versions``;
        - without it, ``supported_primary_versions`` must overlap with the
          ``supported_versions`` of ``primary``. That only says that the two
          parsers work together for some files, so pass ``version`` whenever
          a primary file is known.
        """
        if not cls.compatible_primary:
            return MatchResult(
                f"{cls.__name__} declares no compatible primary parsers."
            )
        if not issubclass(primary, cls.compatible_primary):
            expected = ", ".join(parser.__name__ for parser in cls.compatible_primary)
            return MatchResult(
                f"{cls.__name__} does not work with {primary.__name__}. "
                f"Compatible primary parsers: {expected}."
            )
        if not cls.supported_primary_versions:
            return MatchResult()
        supported = format_version_ranges(cls.supported_primary_versions)
        try:
            version = _as_version_tuple(version)
        except (TypeError, ValueError) as error:
            return MatchResult(f"{cls.__name__} could not use the version: {error}")
        if version is not None:
            if not is_version_supported(version, cls.supported_primary_versions):
                return MatchResult(
                    f"{cls.__name__} does not work with {primary.__name__} files "
                    f"of version {format_version(version)}. Supported versions "
                    f"of {primary.__name__}: {supported}."
                )
            return MatchResult()
        if primary.supported_versions and not version_ranges_overlap(
            primary.supported_versions, cls.supported_primary_versions
        ):
            primary_versions = format_version_ranges(primary.supported_versions)
            return MatchResult(
                f"{cls.__name__} does not work with {primary.__name__}: no overlap "
                f"between its versions {primary_versions} "
                f"and the supported versions {supported}."
            )
        return MatchResult()

    def parse(self, probe: FileProbe, **options: Any) -> None:
        """
        Read the file of ``probe`` into ``data``.

        This does not repeat the checks of ``match``: call it only for files
        that matched. Entries from an earlier call are dropped. Every entry
        without a ``source`` gets the parsed file as its source.

        Args:
            probe: The file to read.
            **options: Options of this parser, passed on to ``_parse``.

        Raises:
            TypeError: If ``_parse`` does not return a dict of ``ParsedData``.
        """
        self._data = {}  # a failed _parse leaves no entries of an earlier file
        data = self._parse(probe, **options)
        if not isinstance(data, dict) or not all(
            isinstance(entry, ParsedData) for entry in data.values()
        ):
            raise TypeError(
                f"{type(self).__name__}._parse must return a dict of ParsedData, "
                f"not {data!r:.80}."
            )
        for entry in data.values():
            if entry.source is None:
                entry.source = probe.path
        self._data = data

    @abstractmethod
    def _parse(self, probe: FileProbe, **options: Any) -> dict[str, ParsedData]:
        """Read the file of ``probe`` and return what it holds, by name."""
