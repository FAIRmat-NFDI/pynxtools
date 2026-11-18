# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Version helpers for file parsers.

A parser declares the file-format versions it supports as half-open ranges
``(lower_inclusive, upper_exclusive_or_None)`` of version tuples, and checks a
file's version against them. Moved here from pynxtools-xps, where the same
code was also copied into pynxtools-xas and pynxtools-raman.
"""

import re
from collections.abc import Iterable
from typing import TypeAlias

VersionTuple: TypeAlias = tuple[int | str, ...]
VersionRange: TypeAlias = tuple[VersionTuple, VersionTuple | None]

_TOKEN_RE = re.compile(r"\d+|[A-Za-z]+")


def format_version(version: VersionTuple) -> str:
    """Join a version tuple with dots, e.g. ``(2019, "R", 2)`` -> ``"2019.R.2"``."""
    return ".".join(str(x) for x in version)


def normalize_version(raw: str) -> VersionTuple:
    """
    Normalize a vendor version string into a comparable tuple.

    Tokenization rules
    ------------------
    - Consecutive digits are parsed as integers.
    - Consecutive letters are upper cased and kept as strings.
    - All other characters act as separators.

    Examples
    --------
    "4.75"    -> (4, 75)
    "4"       -> (4,)
    "2019R2"  -> (2019, "R", 2)
    "v3_1"    -> ("V", 3, 1)
    "3-2"     -> (3, 2)
    "4.100"   -> (4, 100)
    """
    if raw is None:
        raise TypeError("Version string must not be None.")

    raw = raw.strip()
    if not raw:
        raise ValueError("Version string must not be empty.")

    tokens = _TOKEN_RE.findall(raw)
    if not tokens:
        raise ValueError(f"Could not extract version tokens from '{raw}'.")

    return tuple(int(token) if token.isdigit() else token.upper() for token in tokens)


def _sort_key(version: VersionTuple) -> tuple[tuple[int, int | str], ...]:
    """Key that orders version tuples without comparing numbers with letters.

    Trailing zeros are ignored, so ``(4,)`` equals ``(4, 0)``. At the same
    position a number sorts before letters, so ``(3,) < ("V", 3)``. This is a
    defined order, not a claim about which vendor version is newer.
    """
    parts = list(version)
    while parts and parts[-1] == 0:
        parts.pop()
    return tuple((0, part) if isinstance(part, int) else (1, part) for part in parts)


def is_version_supported(
    version: VersionTuple | None,
    supported_versions: Iterable[VersionRange],
) -> bool:
    """
    Determine whether a normalized version tuple is supported.

    Parameters
    ----------
    version
        Normalized version tuple, or ``None`` if the file carries no version.
    supported_versions
        Iterable of half-open version intervals:
        ``(lower_inclusive, upper_exclusive_or_None)``.
        An empty iterable means no version constraint: all files are accepted,
        including those without a version.
        A non-empty iterable implicitly requires a version: ``None`` is
        rejected because it cannot fall within any declared range.

    Returns
    -------
    bool
    """
    ranges = tuple(supported_versions)
    if not ranges:
        return True

    if version is None:
        return False

    key = _sort_key(version)
    for lower, upper in ranges:
        if _sort_key(lower) <= key and (upper is None or key < _sort_key(upper)):
            return True

    return False


def version_ranges_overlap(
    primary_parser_versions: Iterable[VersionRange],
    required_parser_versions: Iterable[VersionRange],
) -> bool:
    """Return True if any range in *primary_parser_versions* overlaps with any
    range in *required_parser_versions*.

    Ranges are half-open intervals ``[lower, upper)`` with ``upper=None``
    meaning unbounded. Two intervals overlap if the lower bound of each one is
    strictly below the upper bound of the other, treating ``None`` as +inf.

    Used to check whether a metadata parser's ``supported_primary_parser_versions``
    is compatible with a primary parser's ``supported_versions``.
    """
    required = tuple(required_parser_versions)
    for primary_lower, primary_upper in primary_parser_versions:
        for required_lower, required_upper in required:
            primary_starts_before_required_ends = required_upper is None or (
                _sort_key(primary_lower) < _sort_key(required_upper)
            )
            required_starts_before_primary_ends = primary_upper is None or (
                _sort_key(required_lower) < _sort_key(primary_upper)
            )
            if (
                primary_starts_before_required_ends
                and required_starts_before_primary_ends
            ):
                return True
    return False
