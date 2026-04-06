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
"""Test cases for the Writer class used by the DataConverter"""

import logging
import os
from pathlib import Path

import h5py
import numpy as np
import pytest

# import h5py.h5p as h5p
from pynxtools.dataconverter.validate_file import validate

try:
    from nomad.datamodel import EntryArchive
    from nomad.units import ureg
    from nomad.utils import get_logger
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from pynxtools.nomad.parsers.parser import NexusParser

# import flatdict as fd

warnings = [
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@axis_i_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@axis_j_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@indices_image_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The required group /entry1/measurement/instrument hasn't been supplied.",
    "WARNING: The required group /entry1/sampleID hasn't been supplied.",
    "WARNING: The required attribute /entry1/measurement/event1/image1/stack_2d/@AXISNAME_indices hasn't been supplied.",
    "WARNING: The required field /entry1/start_time hasn't been supplied.",
]


@pytest.mark.parametrize(
    "storage_layout, data_type, expected_warnings",
    [
        pytest.param("compressed", "uint8", warnings, id="compressed-uint8"),
        pytest.param("compressed", "uint16", warnings, id="compressed-uint16"),
        pytest.param("compressed", "uint32", warnings, id="compressed-uint32"),
        pytest.param("compressed", "uint64", warnings, id="compressed-uint64"),
        pytest.param("compressed", "int8", warnings, id="compressed-int8"),
        pytest.param("compressed", "int16", warnings, id="compressed-int16"),
        pytest.param("compressed", "int32", warnings, id="compressed-int32"),
        pytest.param("compressed", "int64", warnings, id="compressed-int64"),
        pytest.param("compressed", "float16", warnings, id="compressed-float16"),
        pytest.param("compressed", "float32", warnings, id="compressed-float32"),
        pytest.param("compressed", "float64", warnings, id="compressed-float64"),
        pytest.param("compressed", "float128", warnings, id="compressed-float128"),
        # pytest.param("compressed", "complex32", warnings, id="compressed-complex32"),
        # pytest.param("compressed", "complex64", warnings, id="compressed-complex64"),
        # pytest.param("compressed", "complex128", warnings, id="compressed-complex128"),
        pytest.param("uncompressed", "uint8", warnings, id="uncompressed-uint8"),
        pytest.param("uncompressed", "uint16", warnings, id="uncompressed-uint16"),
        pytest.param("uncompressed", "uint32", warnings, id="uncompressed-uint32"),
        pytest.param("uncompressed", "uint64", warnings, id="uncompressed-uint64"),
        pytest.param("uncompressed", "int8", warnings, id="uncompressed-int8"),
        pytest.param("uncompressed", "int16", warnings, id="uncompressed-int16"),
        pytest.param("uncompressed", "int32", warnings, id="uncompressed-int32"),
        pytest.param("uncompressed", "int64", warnings, id="uncompressed-int64"),
        pytest.param("uncompressed", "float16", warnings, id="uncompressed-float16"),
        pytest.param("uncompressed", "float32", warnings, id="uncompressed-float32"),
        pytest.param("uncompressed", "float64", warnings, id="uncompressed-float64"),
        pytest.param("uncompressed", "float128", warnings, id="uncompressed-float128"),
        # pytest.param("uncompressed", "complex32", warnings, id="uncompressed-complex32"),
        # pytest.param("uncompressed", "complex64", warnings, id="uncompressed-complex64"),
        # pytest.param("uncompressed", "complex128", warnings, id="uncompressed-complex128"),
        pytest.param("contiguous", "uint8", warnings, id="contiguous-uint8"),
        pytest.param("contiguous", "uint16", warnings, id="contiguous-uint16"),
        pytest.param("contiguous", "uint32", warnings, id="contiguous-uint32"),
        pytest.param("contiguous", "uint64", warnings, id="contiguous-uint64"),
        pytest.param("contiguous", "int8", warnings, id="contiguous-int8"),
        pytest.param("contiguous", "int16", warnings, id="contiguous-int16"),
        pytest.param("contiguous", "int32", warnings, id="contiguous-int32"),
        pytest.param("contiguous", "int64", warnings, id="contiguous-int64"),
        pytest.param("contiguous", "float16", warnings, id="contiguous-float16"),
        pytest.param("contiguous", "float32", warnings, id="contiguous-float32"),
        pytest.param("contiguous", "float64", warnings, id="contiguous-float64"),
        pytest.param("contiguous", "float128", warnings, id="contiguous-float128"),
        # pytest.param("contiguous", "complex32", warnings, id="contiguous-complex32"),
        # pytest.param("contiguous", "complex64", warnings, id="contiguous-complex64"),
        # pytest.param("contiguous", "complex128", warnings, id="contiguous-complex128"),
    ],
)
def test_parse_file_array_statistics(
    storage_layout, data_type, tmp_path, caplog, expected_warnings
):
    """Test validation of a NeXus/HDF5 with the same content but different storage layout."""
    file_path = tmp_path / f"{storage_layout}.{data_type}.nxs"
    prng = np.random.default_rng(seed=42)  # deterministic seeding
    n_values = 100 * 50**2
    with h5py.File(file_path, "w", track_order=True) as h5w:
        # gcpl = h5w.id.get_create_plist()
        # flags = gcpl.get_link_creation_order()
        # bool(flags & h5p.CRT_ORDER_TRACKED)
        # bool(flags & h5p.CRT_ORDER_INDEXED)

        trg = "/entry1/measurement/event1/image1/stack_2d"
        for idx, class_name in enumerate(
            ["ENTRY", "EM_MEASUREMENT", "EM_EVENT_DATA", "IMAGE"]
        ):
            grp = h5w.create_group(f"{'/'.join(trg.split('/')[0 : idx + 2])}")
            grp.attrs["NX_class"] = f"NX{class_name.lower()}"
        grp = h5w.create_group(f"{trg}")

        chunking = (10, 50, 50)
        axes = ["indices_image", "axis_j", "axis_i"]
        mean = np.float128(np.nan)
        if np.issubdtype(data_type, np.unsignedinteger):
            dat = prng.integers(
                0, np.iinfo(data_type).max, size=n_values, dtype=data_type
            ).reshape(-1, 50, 50)
            mean = np.sum(dat, dtype=np.float128) / np.float128(dat.size)
        elif np.issubdtype(data_type, np.integer):
            dat = prng.integers(
                np.iinfo(data_type).min,
                np.iinfo(data_type).max,
                size=n_values,
                dtype=data_type,
            ).reshape(-1, 50, 50)
            mean = np.sum(dat, dtype=np.float128) / np.float128(dat.size)
        elif np.issubdtype(data_type, np.floating):
            dat = prng.random(size=n_values).astype(data_type).reshape(-1, 50, 50)
            mean = np.sum(dat, dtype=np.float128) / np.float128(dat.size)
        # elif np.issubdtype(data_type, np.complexfloating):
        #     real_dtype = np.empty((), dtype=data_type).real.dtype  # half the itemsize
        #     real = prng.random(size=n_values).astype(real_dtype)
        #     imag = prng.random(size=n_values).astype(real_dtype)
        #     dat = (real + 1j * imag).astype(data_type).reshape(-1, 50, 50)
        #     # no stats for complex
        else:
            raise TypeError(f"Unsupported dtype: {data_type}")

        grp.attrs["NX_class"] = "NXdata"
        grp.attrs["axes"] = axes
        signal = (
            "real" if not np.issubdtype(data_type, np.complexfloating) else "complex"
        )
        grp.attrs["signal"] = signal
        for idx, axis in enumerate(axes):
            grp.attrs[f"{axis}_indices"] = np.uint32(idx)
        if storage_layout == "uncompressed":
            dst = h5w.create_dataset(f"{trg}/{signal}", data=dat, chunks=chunking)
        elif storage_layout == "compressed":
            dst = h5w.create_dataset(
                f"{trg}/{signal}",
                data=dat,
                chunks=chunking,
                compression="gzip",
                compression_opts=1,
            )
        else:  # contiguous
            dst = h5w.create_dataset(f"{trg}/{signal}", data=dat)
        dst.attrs["long_name"] = signal
        for idx, axis in enumerate(axes):
            dst = h5w.create_dataset(
                f"{trg}/{axis}",
                data=np.asarray(np.arange(np.shape(dat)[idx]), np.uint32),
            )
            dst.attrs["long_name"] = axis
        dst = h5w.create_dataset("/entry1/definition", data="NXem")

    assert os.path.isfile(file_path)

    print(f">>>> {mean}")

    archive = EntryArchive()
    NexusParser().parse(str(file_path), archive, get_logger(__name__))
    # for key, obj in fd.FlatDict(archive.m_to_dict(), delimiter="/").items():
    #     # if key == "results":
    #     print(f"{key}, {obj}")

    """
    with caplog.at_level(logging.INFO):
        observed_warnings = [
            rec.message
            for rec in caplog.records
            if rec.levelno == logging.WARNING
            and not rec.message.startswith(
                "WARNING: Invalid: The entry `entry1` in file"
            )
        ]
        assert observed_warnings == expected_warnings

    os.remove(file_path)
    """


"""
x32 = np.array([1.1, 2.2, 3.3, 4.4], dtype=np.float32)
x64 = x32.astype(np.float64)
x128 = x32.astype(np.float128)
mean64 = np.mean(x64, dtype=np.float64)
mean128 = np.mean(x128, dtype=np.float128)
atol = np.finfo(np.float64).eps
is_close = np.isclose(mean128, mean64, atol=atol, rtol=0.0)
print(mean128, mean64, is_close)
"""
