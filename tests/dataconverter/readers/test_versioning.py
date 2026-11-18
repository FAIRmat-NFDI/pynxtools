# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for the shared version helpers of reader parsers."""

import pytest

from pynxtools.dataconverter.readers.parsers.versioning import (
    format_version,
    is_version_supported,
    normalize_version,
    version_ranges_overlap,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("4.75", (4, 75)),
        ("4", (4,)),
        ("2019R2", (2019, "R", 2)),
        ("v3_1", ("V", 3, 1)),
        ("3-2", (3, 2)),
        ("4.100", (4, 100)),
        ("1.2.3", (1, 2, 3)),
        ("  4.75  ", (4, 75)),  # leading/trailing whitespace stripped
    ],
)
def test_normalize_version(raw, expected):
    assert normalize_version(raw) == expected


@pytest.mark.parametrize(
    "raw, exc",
    [
        (None, TypeError),  # None is rejected explicitly
        ("", ValueError),  # empty string
        ("---", ValueError),  # no alphanumeric tokens
    ],
)
def test_normalize_version_invalid(raw, exc):
    with pytest.raises(exc):
        normalize_version(raw)


@pytest.mark.parametrize(
    "version, expected",
    [
        ((4, 75), "4.75"),
        ((2019, "R", 2), "2019.R.2"),
        ((1,), "1"),
        ((1, 2, 3), "1.2.3"),
    ],
)
def test_format_version(version, expected):
    assert format_version(version) == expected


@pytest.mark.parametrize(
    "version, supported, expected",
    [
        # No version present
        (None, [], True),  # no constraints: files without a version are accepted
        (None, [((4, 0), (5, 0))], False),  # ranges declared: rejected
        # No declared ranges: all versions pass
        ((4, 1), [], True),
        # Half-open range: [lower, upper)
        ((4, 1), [((4, 0), (5, 0))], True),  # inside range
        ((4, 0), [((4, 0), (5, 0))], True),  # on lower bound (inclusive)
        ((5, 0), [((4, 0), (5, 0))], False),  # on upper bound (exclusive)
        ((3, 9), [((4, 0), (5, 0))], False),  # below range
        # Unbounded upper: [lower, inf)
        ((6, 0), [((4, 0), None)], True),
        ((3, 0), [((4, 0), None)], False),
        # Multiple ranges
        ((4, 0), [((4, 0), (5, 0)), ((6, 0), None)], True),
        ((5, 5), [((4, 0), (5, 0)), ((6, 0), None)], False),  # in the gap
    ],
)
def test_is_version_supported(version, supported, expected):
    assert is_version_supported(version, supported) == expected


@pytest.mark.parametrize(
    "version, supported, expected",
    [
        ((4,), [((4, 0), None)], True),  # "4" is the same as "4.0"
        ((4, 0, 0), [((4,), (5,))], True),
        ((5,), [((4, 0), (5, 0))], False),  # "5" is the upper bound "5.0"
    ],
)
def test_trailing_zeros_do_not_matter(version, supported, expected):
    assert is_version_supported(version, supported) == expected


@pytest.mark.parametrize(
    "version, supported, expected",
    [
        # a defined order, not a semantic one: numbers sort before letters
        ((2019, "R", 2), [((2019, 1), None)], True),
        ((2019, "R", 2), [((2019,), None)], True),
        (("V", 3), [((3,), None)], True),
    ],
)
def test_mixed_numbers_and_letters_compare_without_error(version, supported, expected):
    assert is_version_supported(version, supported) == expected


@pytest.mark.parametrize(
    "primary, required, expected",
    [
        ([((4, 0), (5, 0))], [((4, 5), (6, 0))], True),  # partial overlap
        ([((4, 0), (5, 0))], [((5, 0), (6, 0))], False),  # touching, half-open
        ([((4, 0), (5, 0))], [((1, 0), (2, 0))], False),  # disjoint
        ([((4, 0), None)], [((10, 0), None)], True),  # both unbounded
        ([((4, 0), (5, 0))], [((3, 0), None)], True),  # required unbounded
        ([((1, 0), (2, 0)), ((6, 0), None)], [((7, 0), (8, 0))], True),  # 2nd range
        ([], [((1, 0), None)], False),  # nothing declared
        ([((4,), (5,))], [((5, 0), None)], False),  # "5" == "5.0" at the edge
    ],
)
def test_version_ranges_overlap(primary, required, expected):
    assert version_ranges_overlap(primary, required) == expected


def test_version_ranges_overlap_accepts_a_generator():
    """The required ranges are checked against every primary range, also when
    they come as a generator that can only be read once."""
    primary = [((1, 0), (2, 0)), ((6, 0), None)]
    required = (r for r in [((7, 0), (8, 0))])
    assert version_ranges_overlap(primary, required)


MIXED_RANGES = (
    ((2019, 1), (2019, 9)),  # numeric releases 2019.1 - 2019.8
    ((2019, "R", 1), (2019, "R", 5)),  # R releases 2019R1 - 2019R4
)


@pytest.mark.parametrize(
    "raw, expected",
    [("2019.3", True), ("2019R2", True), ("2019R7", False), ("2019.10", False)],
)
def test_separate_ranges_for_numeric_and_lettered_versions(raw, expected):
    """The example from the docs: one range per kind of version."""
    assert is_version_supported(normalize_version(raw), MIXED_RANGES) == expected
