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
import numpy as np
import pytest

from pynxtools.utils import decode_if_string


@pytest.mark.parametrize(
    "string_obj, decode, expected",
    [
        # Test with np.ndarray of bytes (fixed-length)
        (
            np.array([b"fixed1", b"fixed2"], dtype="S10"),
            True,
            np.array(["fixed1", "fixed2"], dtype="U7"),
        ),
        (
            np.array([b"fixed1   ", b"fixed2   "], dtype="S10"),
            False,
            np.array([b"fixed1   ", b"fixed2   "], dtype="S10"),
        ),
        # Variable-length byte arrays
        (
            np.array([b"var1", b"var2", b"var3"]),
            True,
            np.array(["var1", "var2", "var3"], dtype="U4"),
        ),
        (
            np.array([b"var1", b"var2", b"var3"]),
            False,
            np.array([b"var1", b"var2", b"var3"], dtype="S4"),
        ),
        # Empty arrays
        (np.array([], dtype=object), True, np.array([], dtype=object)),
        (np.array([], dtype=object), False, np.array([], dtype=object)),
        # Numpy array with non-byte elements
        (np.array([1, 2, 3]), True, np.array([1, 2, 3])),
        (np.array([1, 2, 3]), False, np.array([1, 2, 3])),
        # Numpy array with mixed types
        (
            np.array([b"bytes", "string"], dtype=object),
            True,
            np.array(["bytes", "string"], dtype="U6"),
        ),
        (
            np.array([b"bytes", "string"], dtype=object),
            False,
            np.array([b"bytes", "string"], dtype=object),
        ),
        # Test with lists of bytes and strings
        ([b"bytes", "string"], True, ["bytes", "string"]),
        ([b"bytes", "string"], False, [b"bytes", "string"]),
        ([b"bytes", b"more_bytes", "string"], True, ["bytes", "more_bytes", "string"]),
        (
            [b"bytes", b"more_bytes", "string"],
            False,
            [b"bytes", b"more_bytes", "string"],
        ),
        ([b"fixed", b"length", b"strings"], True, ["fixed", "length", "strings"]),
        ([b"fixed", b"length", b"strings"], False, [b"fixed", b"length", b"strings"]),
        # Test with nested lists
        ([[b"nested1"], [b"nested2"]], True, [["nested1"], ["nested2"]]),
        ([[b"nested1"], [b"nested2"]], False, [[b"nested1"], [b"nested2"]]),
        # Test with bytes
        (b"single", True, "single"),
        (b"single", False, b"single"),
        # Empty byte string
        (b"", True, ""),
        (b"", False, b""),
        # Test with str
        ("single", True, "single"),
        ("single", False, "single"),
        # Test with non-decodable data types
        (123, True, 123),
        (123, False, 123),
        (None, True, None),
        (None, False, None),
        # Numpy array with nested structure
        (
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
            True,
            np.array([["nested1"], ["nested2"]], dtype="U7"),
        ),
        (
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
            False,
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
        ),
    ],
)
def test_decode_if_string(string_obj, decode, expected):
    result = decode_if_string(elem=string_obj, decode=decode)

    # Handle np.ndarray outputs
    if isinstance(expected, np.ndarray):
        assert isinstance(result, np.ndarray), (
            f"Expected ndarray, but got {type(result)}"
        )
        assert (result == expected).all(), (
            f"Failed for {string_obj} with decode={decode}"
        )
    # Handle list outputs
    elif isinstance(expected, list):
        assert isinstance(result, list), f"Expected list, but got {type(result)}"
    # Handle all other cases
    else:
        assert result == expected, f"Failed for {string_obj} with decode={decode}"
