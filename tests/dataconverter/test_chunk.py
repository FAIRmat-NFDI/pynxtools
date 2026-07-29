# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Test cases chunking and compression."""

import numpy as np
import pytest

from pynxtools.dataconverter.chunk import prioritized_axes_heuristic


@pytest.mark.parametrize(
    "axes, expected",
    [
        ((0, 1, 2), (1, 250, 1000)),
        ((0, 2, 1), (1, 250, 1000)),
        ((1, 2, 0), (7, 32, 1000)),
        ((1, 0, 2), (7, 32, 1000)),
        ((2, 0, 1), (8, 250, 125)),
        ((2, 1, 0), (8, 250, 125)),
        ((), True),
        ((0,), True),
        (
            (
                0,
                1,
            ),
            True,
        ),
        ((0, 0), True),
        ((0, 1, 1), True),
        ((0, 1, 2, 3), True),
        ((0, 1, 2, 2), True),
    ],
    ids=[
        "intentional-small",
        "awkward-small",
        "awkward-small",
        "awkward-small",
        "awkward-small",
        "awkward-small",
        "scalar",
        "oned",
        "twod",
        "twod-multiples",
        "threed-multiples",
        "fourd",
        "fourd-multiples",
    ],
)
def test_prioritized_axes_heuristic_small(
    axes: tuple[int, ...], expected: tuple[int, ...] | bool
):
    array = np.zeros((8, 250, 1000), np.float32)
    assert prioritized_axes_heuristic(array, axes) == expected


@pytest.mark.parametrize(
    "axes, expected",
    [
        ((0, 1, 2), (1, 125, 2000)),
        ((0, 2, 1), (1, 1000, 250)),
        ((1, 2, 0), (128, 1, 2000)),
        ((1, 0, 2), (128, 1, 2000)),
        ((2, 0, 1), (87, 1000, 2)),
        ((2, 1, 0), (87, 1000, 2)),
    ],
    ids=[
        "intentional-large",
        "awkward-large",
        "awkward-large",
        "awkward-large",
        "awkward-large",
        "awkward-large",
    ],
)
def test_prioritized_axes_heuristic_large(
    axes: tuple[int, ...], expected: tuple[int, ...]
):
    array = np.zeros((128, 1000, 2000), np.float32)
    assert prioritized_axes_heuristic(array, axes) == expected


# unlimited axis
