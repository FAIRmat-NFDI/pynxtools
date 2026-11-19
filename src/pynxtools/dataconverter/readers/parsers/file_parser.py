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
``parse`` then reads the file into one ``ParsedData`` per NeXus entry.

A metadata parser reads a file that only adds metadata to the entries of a
primary parser, e.g. a quantification export next to the spectra. It names
the primary parsers it works with in ``compatible_primary``.
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
    is_version_supported,
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


def _format_ranges(ranges: tuple[VersionRange, ...]) -> str:
    """``"1.0 – 2.0, >= 3"`` for the half-open ranges ``ranges``."""
    formatted = [
        f">= {format_version(lower)}"
        if upper is None
        else f"{format_version(lower)} – {format_version(upper)}"
        for lower, upper in ranges
    ]
    return ", ".join(formatted) or "<none>"


class FileParser(ABC):
    """
    A parser for one file format.

    Subclasses set ``supported_file_extensions`` and implement
    ``matches_file`` and ``_parse``. Version-aware parsers also set
    ``supported_versions`` and implement ``detect_version``.

    Attributes:
        supported_file_extensions: The file name endings this parser reads,
            compared without case, e.g. ``(".sle",)`` or ``(".mtex.h5",)``.
            A parser without extensions matches no file.
        supported_versions: Half-open version ranges
            ``(lower_inclusive, upper_exclusive_or_None)``. Empty means any
            file, with or without a version. Otherwise a file must have a
            version within one of the ranges.
        supported_vendor: The instrument or software vendor, for
            documentation. It is not checked.
        role: ``"primary"`` for a parser that creates entries, ``"metadata"``
            for one that adds metadata to the entries of a primary parser.
        compatible_primary: For a metadata parser, the primary parsers
            (including their subclasses) whose entries it can add to.
        supported_primary_versions: For a metadata parser, the versions of
            the primary parser it works with. Empty means any version.
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
        """What the last ``parse`` call read, keyed by NeXus entry name."""
        return self._data

    @classmethod
    def detect_version(cls, probe: FileProbe) -> VersionTuple | None:
        """
        The version of the file format, or ``None`` if the file has none.

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

        Checks the extension, then the version, then ``matches_file``. It
        never raises: an error in ``detect_version`` or ``matches_file``
        becomes the reason of the result.
        """
        name = probe.path.name
        if not any(probe.has_suffix(ext) for ext in cls.supported_file_extensions):
            allowed = ", ".join(cls.supported_file_extensions) or "<none>"
            return MatchResult(
                f"File '{name}' does not have an extension that {cls.__name__} "
                f"supports. Supported extensions: {allowed}."
            )

        try:
            version = cls.detect_version(probe)
        except Exception as error:
            return MatchResult(
                f"{cls.__name__} could not read the version of '{name}': {error}"
            )
        if version is not None and not isinstance(version, tuple):
            return MatchResult(
                f"{cls.__name__}.detect_version returned {version!r} for '{name}' "
                "instead of a version tuple; use normalize_version to convert it."
            )
        if not is_version_supported(version, cls.supported_versions):
            supported = _format_ranges(cls.supported_versions)
            if version is None:
                return MatchResult(
                    f"File '{name}' does not specify a version, but "
                    f"{cls.__name__} requires one. Supported versions: {supported}."
                )
            return MatchResult(
                f"File '{name}' has version {format_version(version)}, which "
                f"{cls.__name__} does not support. Supported versions: {supported}."
            )

        try:
            matches = cls.matches_file(probe)
        except Exception as error:
            return MatchResult(f"{cls.__name__} could not check '{name}': {error}")
        if not matches:
            return MatchResult(
                f"File '{name}' does not match the expected format of {cls.__name__}."
            )
        return MatchResult()

    @classmethod
    def accepts_primary(cls, primary: type["FileParser"]) -> MatchResult:
        """
        Whether this metadata parser can add to the entries of ``primary``,
        and why not if it can't.

        ``primary`` must be one of ``compatible_primary`` or a subclass of
        one. If ``supported_primary_versions`` is set, it must overlap with
        the ``supported_versions`` of ``primary``.
        """
        if cls.role != "metadata":
            return MatchResult(f"{cls.__name__} is not a metadata parser.")
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
        if (
            cls.supported_primary_versions
            and primary.supported_versions
            and not version_ranges_overlap(
                primary.supported_versions, cls.supported_primary_versions
            )
        ):
            return MatchResult(
                f"{cls.__name__} does not work with {primary.__name__}: no overlap "
                f"between its versions {_format_ranges(primary.supported_versions)} "
                f"and the supported versions "
                f"{_format_ranges(cls.supported_primary_versions)}."
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
        """
        self._data = {}
        self._parse(probe, **options)
        for entry in self._data.values():
            if entry.source is None:
                entry.source = probe.path

    @abstractmethod
    def _parse(self, probe: FileProbe, **options: Any) -> None:
        """Read the file of ``probe`` and fill ``self._data``."""
