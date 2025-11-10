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
import re
from typing import Any

import numpy as np

from pynxtools.definitions.dev_tools.utils.nxdl_utils import decode_or_not

ISO8601 = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:"
    r"\.\d*)?)(((?!-00:00)(\+|-)(\d{2}):(\d{2})|Z){1})$"
)

RESERVED_PREFIXES = {
    "attribute": {
        "@BLUESKY_": None,  # do not use anywhere
        "@DECTRIS_": "NXmx",
        "@IDF_": None,  # do not use anywhere
        "@NDAttr": None,
        "@NX_": "all",
        "@PDBX_": None,  # do not use anywhere
        "@SAS_": "NXcanSAS",
        "@SILX_": None,  # do not use anywhere
        "identifier": "all",
    },
    "field": {
        "DECTRIS_": "NXmx",
    },
}

RESERVED_SUFFIXES = (
    "_end",
    "_increment_set",
    "_errors",
    "_indices",
    "_mask",
    "_set",
    "_weights",
    "_scaling_factor",
    "_offset",
)


def decode_if_string(
    elem: Any, encoding: str = "utf-8", decode: bool = True
) -> Any | None:
    """
    Decodes a numpy ndarray or list of byte objects or byte strings to strings.
    If `decode` is False, returns the input value unchanged. Non-byte/str types
    are returned without modification.

    Args:
        elem: A numpy ndarray, list, bytes, or any other object.
        encoding: The encoding scheme to use. Default is "utf-8".
        decode: A boolean flag indicating whether to perform decoding.

    Returns:
        A decoded string, a numpy array of decoded strings, a list of decoded strings,
        or the input value if not decodable.
        Returns None if the input is empty or invalid.

    Raises:
        ValueError: If decoding fails on bytes or numpy array elements.
    """
    # Early return if decoding is disabled
    if not decode:
        return elem

    # Handle numpy arrays of bytes or strings
    if isinstance(elem, np.ndarray):
        if elem.size == 0:
            return elem  # Return the empty array unchanged

        # This only checks for null-terminated strings,
        # may need to be updated in the future: https://api.h5py.org/h5t.html
        if elem.dtype.kind == "S":  # Check if it's a bytes array (fixed-length strings)
            decoded_array = np.vectorize(
                lambda x: x.decode(encoding).rstrip("\x00")
                if isinstance(x, bytes)
                else x
            )(elem)
            return decoded_array.astype(str)  # Ensure the dtype is str

        # Handle mixed-type arrays
        if elem.dtype == object:
            decoded_array = np.vectorize(
                lambda x: x.decode(encoding) if isinstance(x, bytes) else x
            )(elem)
            return decoded_array.astype(str)  # Ensure all elements are strings

    return decode_or_not(elem, encoding, decode)
