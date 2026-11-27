# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Version helpers for file parsers.

A parser declares the file-format versions it supports as half-open ranges
``(lower_inclusive, upper_exclusive_or_None)`` of version tuples, and checks a
file's version against them.
"""

import logging
import re
from collections.abc import Iterable
from typing import TypeAlias

VersionTuple: TypeAlias = tuple[int | str, ...]
VersionRange: TypeAlias = tuple[VersionTuple, VersionTuple | None]

_TOKEN_RE = re.compile(r"\d+|[A-Za-z]+")
logger = logging.getLogger("pynxtools")


def format_version(version: VersionTuple) -> str:
    """Join a version tuple with dots, e.g. ``(2019, "R", 2)`` -> ``"2019.R.2"``."""
    return ".".join(str(x) for x in version)


def format_version_ranges(ranges: tuple[VersionRange, ...]) -> str:
    """
    Describe half-open version ranges for messages, e.g.
    ``">= 1.0 and < 2.0, or >= 3"`` for ``(((1, 0), (2, 0)), ((3,), None))``.

    No ranges means any version, as in ``is_version_supported``.
    """
    formatted = [
        f">= {format_version(lower)}"
        if upper is None
        else f">= {format_version(lower)} and < {format_version(upper)}"
        for lower, upper in ranges
    ]
    return ", or ".join(formatted) or "any"


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


def _mixes_numbers_and_letters(first: VersionTuple, second: VersionTuple) -> bool:
    """Whether ordering the two versions needs the numbers-before-letters rule.

    True if, at the first position where they differ, one has a number and the
    other has letters, e.g. ``(2019, 1)`` and ``(2019, "R", 2)``.
    """
    for first_part, second_part in zip(_sort_key(first), _sort_key(second)):
        if first_part != second_part:
            return first_part[0] != second_part[0]
    return False


def _log_fallback_order(
    pairs: Iterable[tuple[VersionTuple, VersionTuple]], accepted: bool
) -> None:
    """Log an info message if a decision relied on the numbers-before-letters rule.

    ``pairs`` are the version pairs whose order decided the result: the bounds
    of the accepting range, or all compared bounds if nothing was accepted.
    Only pairs with a number and letters at the deciding position are reported.
    """
    mixed = [
        f"{format_version(first)} vs. {format_version(second)}"
        for first, second in pairs
        if _mixes_numbers_and_letters(first, second)
    ]
    if mixed:
        logger.info(
            f"Version check {'passed' if accepted else 'failed'}; these versions "
            "were compared by the fallback rule that numbers sort before letters: "
            f"{', '.join(mixed)}. If the file format uses both kinds of versions, "
            "declare separate version ranges for each kind."
        )


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
    compared: list[tuple[VersionTuple, VersionTuple]] = []

    for lower, upper in ranges:
        bounds = [(version, lower)] + ([] if upper is None else [(version, upper)])
        if _sort_key(lower) <= key and (upper is None or key < _sort_key(upper)):
            _log_fallback_order(bounds, accepted=True)
            return True
        compared.extend(bounds)

    _log_fallback_order(compared, accepted=False)
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
    compared: list[tuple[VersionTuple, VersionTuple]] = []
    for primary_lower, primary_upper in primary_parser_versions:
        for required_lower, required_upper in required:
            bounds: list[tuple[VersionTuple, VersionTuple]] = []
            if required_upper is not None:
                bounds.append((primary_lower, required_upper))
            if primary_upper is not None:
                bounds.append((required_lower, primary_upper))
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
                _log_fallback_order(bounds, accepted=True)
                return True
            compared.extend(bounds)
    _log_fallback_order(compared, accepted=False)
    return False
