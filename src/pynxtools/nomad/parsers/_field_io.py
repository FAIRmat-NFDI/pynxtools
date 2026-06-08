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
"""
Low-level HDF5 field value extraction helpers shared between parsers.

All functions are pure (no NOMAD imports) and operate directly on h5py nodes.
"""

from __future__ import annotations

import h5py
import numpy as np

from pynxtools.definitions.dev_tools.utils.nxdl_utils import decode_or_not


def get_field_str(hdf_node: h5py.Dataset) -> str | None:
    """Return a scalar string or stringified string array from an h5py.Dataset."""
    if h5py.check_string_dtype(hdf_node.dtype) is not None and hdf_node.dtype in (
        "S",
        "U",
        "O",
    ):
        hdf_value = hdf_node[()]
        if hdf_node.shape == ():
            if isinstance(hdf_value, bytes):
                return str(hdf_value.decode("utf-8"))
            return str(hdf_value)
        else:

            def decode_array(arr):
                result = []
                for value in arr:
                    if isinstance(value, (np.ndarray, list)):
                        result.append(decode_array(value))
                    else:
                        result.append(str(decode_or_not(value)))
                return result

            return str(decode_array(hdf_value))
    return None


def get_field_stats_iuf_chunked(
    hdf_node: h5py.Dataset, use_welford: bool = False
) -> dict:
    """Compute field stats (mean/min/max/size/ndim) for chunked iuf storage."""
    stats: dict = {}
    stats["__min"] = np.float64(+np.inf)
    stats["__max"] = np.float64(-np.inf)
    n = np.int64(0)
    mean = np.float64(0.0)
    mean_sum = np.float64(0.0)

    if not use_welford:
        for chunk in hdf_node.iter_chunks():
            slab = hdf_node[chunk]
            values = slab[np.isfinite(slab)]
            number_of_values = values.size
            if number_of_values > 0:
                stats["__min"] = np.minimum(stats["__min"], values.min())
                stats["__max"] = np.maximum(stats["__max"], values.max())
                mean_sum += np.sum(values, dtype=np.float64)
                n += np.int64(number_of_values)
        mean_result = mean_sum / np.float64(n) if n > 0 else np.float64(np.nan)
    else:
        for chunk in hdf_node.iter_chunks():
            slab = hdf_node[chunk]
            values = slab[np.isfinite(slab)]
            if values.size > 0:
                stats["__min"] = np.minimum(stats["__min"], values.min())
                stats["__max"] = np.maximum(stats["__max"], values.max())
                for x in values:
                    value = np.float64(x)
                    n += np.int64(1)
                    delta = value - mean
                    mean += delta / np.float64(n)
        mean_result = mean if n > 0 else np.float64(np.nan)

    if hdf_node.dtype.kind in "iu":
        stats["__mean"] = np.asarray(mean_result, dtype=hdf_node.dtype).item()
        stats["__min"] = np.asarray(stats["__min"], dtype=hdf_node.dtype).item()
        stats["__max"] = np.asarray(stats["__max"], dtype=hdf_node.dtype).item()
    else:
        stats["__mean"] = mean_result
        stats["__min"] = np.float64(stats["__min"])
        stats["__max"] = np.float64(stats["__max"])

    stats["__size"] = np.int64(np.size(hdf_node))
    stats["__ndim"] = np.uint8(np.ndim(hdf_node))
    return stats


def get_field_stats_iuf_contiguous(hdf_node: h5py.Dataset) -> dict:
    """Compute field stats (mean/min/max/size/ndim) for contiguous iuf storage."""
    stats: dict = {}
    stats["__min"] = np.float64(+np.inf)
    stats["__max"] = np.float64(-np.inf)
    n = np.int64(0)

    field = hdf_node[...]
    mask = np.isfinite(field)
    n_values = np.count_nonzero(mask)
    if n_values > 0:
        stats["__min"] = np.minimum(stats["__min"], np.min(field[mask]))
        stats["__max"] = np.maximum(stats["__max"], np.max(field[mask]))
        total = np.sum(field[mask], dtype=np.float64)
        n += np.int64(n_values)
        mean_result = total / np.float64(n)
    else:
        mean_result = np.float64(np.nan)

    if hdf_node.dtype.kind in "iu":
        stats["__mean"] = np.asarray(mean_result, dtype=hdf_node.dtype).item()
        stats["__min"] = np.asarray(stats["__min"], dtype=hdf_node.dtype).item()
        stats["__max"] = np.asarray(stats["__max"], dtype=hdf_node.dtype).item()
    else:
        stats["__mean"] = mean_result
        stats["__min"] = np.float64(stats["__min"])
        stats["__max"] = np.float64(stats["__max"])

    stats["__size"] = np.int64(np.size(hdf_node))
    stats["__ndim"] = np.uint8(np.ndim(hdf_node))
    return stats


def extract_iuf_scalar(hdf_node: h5py.Dataset) -> tuple[object, dict]:
    """Extract the mean scalar value and stats dict from a numeric iuf/c array field.

    Returns (mean_value, stats_dict). If the array is scalar, returns (scalar, {}).
    The mean is used as the representative quantity value in the NOMAD archive;
    full statistics (__min/__max/__size/__ndim) are in the dict for future use.
    """
    if hdf_node.shape == ():
        val = hdf_node[()]
        return val, {}

    if hdf_node.chunks is not None:
        stats = get_field_stats_iuf_chunked(hdf_node)
    else:
        stats = get_field_stats_iuf_contiguous(hdf_node)

    return stats["__mean"], stats
