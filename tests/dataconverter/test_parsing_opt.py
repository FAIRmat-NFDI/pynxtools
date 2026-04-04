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
        pytest.param("chunked_compressed", "u1", warnings, id="chunked-compressed-u1"),
        pytest.param("chunked_compressed", "u2", warnings, id="chunked-compressed-u2"),
        pytest.param("chunked_compressed", "u4", warnings, id="chunked-compressed-u4"),
        pytest.param("chunked_compressed", "u8", warnings, id="chunked-compressed-u8"),
        pytest.param("chunked_compressed", "i1", warnings, id="chunked-compressed-i1"),
        pytest.param("chunked_compressed", "i2", warnings, id="chunked-compressed-i2"),
        pytest.param("chunked_compressed", "i4", warnings, id="chunked-compressed-i4"),
        pytest.param("chunked_compressed", "i8", warnings, id="chunked-compressed-i8"),
        pytest.param("chunked_compressed", "f2", warnings, id="chunked-compressed-f2"),
        pytest.param("chunked_compressed", "f4", warnings, id="chunked-compressed-f4"),
        pytest.param("chunked_compressed", "f8", warnings, id="chunked-compressed-f8"),
        pytest.param(
            "chunked_compressed", "f16", warnings, id="chunked-compressed-f16"
        ),
        pytest.param("chunked_compressed", "c2", warnings, id="chunked-compressed-c2"),
        pytest.param("chunked_compressed", "c4", warnings, id="chunked-compressed-c4"),
        pytest.param("chunked_compressed", "c8", warnings, id="chunked-compressed-c8"),
        pytest.param(
            "chunked_compressed", "c16", warnings, id="chunked-compressed-c16"
        ),
        pytest.param(
            "chunked_uncompressed", "u1", warnings, id="chunked-uncompressed-u1"
        ),
        pytest.param(
            "chunked_uncompressed", "u2", warnings, id="chunked-uncompressed-u2"
        ),
        pytest.param(
            "chunked_uncompressed", "u4", warnings, id="chunked-uncompressed-u4"
        ),
        pytest.param(
            "chunked_uncompressed", "u8", warnings, id="chunked-uncompressed-u8"
        ),
        pytest.param(
            "chunked_uncompressed", "i1", warnings, id="chunked-uncompressed-i1"
        ),
        pytest.param(
            "chunked_uncompressed", "i2", warnings, id="chunked-uncompressed-i2"
        ),
        pytest.param(
            "chunked_uncompressed", "i4", warnings, id="chunked-uncompressed-i4"
        ),
        pytest.param(
            "chunked_uncompressed", "i8", warnings, id="chunked-uncompressed-i8"
        ),
        pytest.param(
            "chunked_uncompressed", "f2", warnings, id="chunked-uncompressed-f2"
        ),
        pytest.param(
            "chunked_uncompressed", "f4", warnings, id="chunked-uncompressed-f4"
        ),
        pytest.param(
            "chunked_uncompressed", "f8", warnings, id="chunked-uncompressed-f8"
        ),
        pytest.param(
            "chunked_uncompressed", "f16", warnings, id="chunked-uncompressed-f16"
        ),
        pytest.param(
            "chunked_uncompressed", "c2", warnings, id="chunked-uncompressed-c2"
        ),
        pytest.param(
            "chunked_uncompressed", "c4", warnings, id="chunked-uncompressed-c4"
        ),
        pytest.param(
            "chunked_uncompressed", "c8", warnings, id="chunked-uncompressed-c8"
        ),
        pytest.param(
            "chunked_uncompressed", "c16", warnings, id="chunked-uncompressed-c16"
        ),
        pytest.param("contiguous", "u1", warnings, id="contiguous-u1"),
        pytest.param("contiguous", "u2", warnings, id="contiguous-u2"),
        pytest.param("contiguous", "u4", warnings, id="contiguous-u4"),
        pytest.param("contiguous", "u8", warnings, id="contiguous-u8"),
        pytest.param("contiguous", "i1", warnings, id="contiguous-i1"),
        pytest.param("contiguous", "i2", warnings, id="contiguous-i2"),
        pytest.param("contiguous", "i4", warnings, id="contiguous-i4"),
        pytest.param("contiguous", "i8", warnings, id="contiguous-i8"),
        pytest.param("contiguous", "f2", warnings, id="contiguous-f2"),
        pytest.param("contiguous", "f4", warnings, id="contiguous-f4"),
        pytest.param("contiguous", "f8", warnings, id="contiguous-f8"),
        pytest.param("contiguous", "f16", warnings, id="contiguous-f16"),
        pytest.param("contiguous", "c2", warnings, id="contiguous-c2"),
        pytest.param("contiguous", "c4", warnings, id="contiguous-c4"),
        pytest.param("contiguous", "c8", warnings, id="contiguous-c8"),
        pytest.param("contiguous", "c16", warnings, id="contiguous-c16"),
    ],
)
def test_parse_file_array_statistics(
    storage_layout, data_type, tmp_path, caplog, expected_warnings
):
    """Test validation of a NeXus/HDF5 with the same content but different storage layout."""
    file_path = tmp_path / f"{storage_layout}.nxs"
    # prng = np.random.default_rng(seed=42)  # deterministic seeding
    n_values = 100 * 50**2
    with h5py.File(file_path, "w", track_order=True) as h5w:
        gcpl = h5w.id.get_create_plist()
        flags = gcpl.get_link_creation_order()
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
        # real = np.asarray(prng.random(size=n_values), np.float32).reshape(-1, 50, 50)
        real = np.ones((n_values // 50**2, 50, 50), np.float32)
        grp.attrs["NX_class"] = "NXdata"
        grp.attrs["axes"] = axes
        grp.attrs["signal"] = "real"
        for idx, axis in enumerate(axes):
            grp.attrs[f"{axis}_indices"] = np.int32(idx)  # should be NX_UINT
        if storage_layout == "chunked_uncompressed":
            dst = h5w.create_dataset(f"{trg}/real", data=real, chunks=chunking)
        elif storage_layout == "chunked_compressed":
            dst = h5w.create_dataset(
                f"{trg}/real",
                data=real,
                chunks=chunking,
                compression="gzip",
                compression_opts=1,
            )
        else:  # contiguous
            dst = h5w.create_dataset(f"{trg}/real", data=real)
        dst.attrs["long_name"] = "real"
        for idx, axis in enumerate(axes):
            dst = h5w.create_dataset(
                f"{trg}/{axis}",
                data=np.asarray(np.arange(np.shape(real)[idx]), np.int32),
            )
            dst.attrs["long_name"] = axis
        dst = h5w.create_dataset("/entry1/definition", data="NXem")

    assert os.path.isfile(file_path)

    validate(file_path)

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


x32 = np.array([1.1, 2.2, 3.3, 4.4], dtype=np.float32)
x64 = x32.astype(np.float64)
x128 = x32.astype(np.float128)
mean64 = np.mean(x64, dtype=np.float64)
mean128 = np.mean(x128, dtype=np.float128)
atol = np.finfo(np.float64).eps
is_close = np.isclose(mean128, mean64, atol=atol, rtol=0.0)
print(mean128, mean64, is_close)
