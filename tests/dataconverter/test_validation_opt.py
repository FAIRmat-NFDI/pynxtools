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

import h5py
import numpy as np
import pytest

# import h5py.h5p as h5p
from pynxtools.dataconverter.validate_file import validate
from pathlib import Path


warnings_storage_layouts = [
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@axis_i_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@axis_j_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The value at /entry1/measurement/event1/image1/stack_2d/@indices_image_indices should be one of the following Python types: (<class 'numpy.unsignedinteger'>,), as defined in the NXDL as NX_UINT.",
    "WARNING: The required group /entry1/measurement/instrument hasn't been supplied.",
    "WARNING: The required group /entry1/sampleID hasn't been supplied.",
    "WARNING: The required attribute /entry1/measurement/event1/image1/stack_2d/@AXISNAME_indices hasn't been supplied.",
    "WARNING: The required field /entry1/start_time hasn't been supplied.",
]


@pytest.mark.parametrize(
    "storage_layout, expected_warnings",
    [
        pytest.param(
            "chunked_uncompressed",
            warnings_storage_layouts,
            id="chunked-uncompressed",
        ),
        pytest.param(
            "chunked_compressed",
            warnings_storage_layouts,
            id="chunked-compressed",
        ),
        pytest.param(
            "contiguous",
            warnings_storage_layouts,
            id="contiguous",
        ),
    ],
)
def test_validate_file_storage_layouts(
    storage_layout, tmp_path, caplog, expected_warnings
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


positive_false_long = [
    "WARNING: The value at /entry/instrument/electronanalyzer/electron_detector/raw_data/pixel_y should be a positive int, but is -512.",
    "WARNING: The value at /entry/instrument/electronanalyzer/electron_detector/raw_data/pixel_x should be a positive int, but is -512.",
    "WARNING: The required group /entry/instrument/beam_probe hasn't been supplied.",
    "WARNING: The required attribute /entry/definition/@version hasn't been supplied.",
    "WARNING: The required field /entry/start_time hasn't been supplied.",
    "WARNING: The required field /entry/title hasn't been supplied.",
]

positive_true_long = [
    "WARNING: The value at /entry/instrument/electronanalyzer/electron_detector/raw_data/pixel_y should be a positive int, but is 0.",
    "WARNING: The value at /entry/instrument/electronanalyzer/electron_detector/raw_data/pixel_x should be a positive int, but is 0.",
    "WARNING: The required group /entry/instrument/beam_probe hasn't been supplied.",
    "WARNING: The required attribute /entry/definition/@version hasn't been supplied.",
    "WARNING: The required field /entry/start_time hasn't been supplied.",
    "WARNING: The required field /entry/title hasn't been supplied.",
]


@pytest.mark.parametrize(
    "storage_layout, positive, data_type, expected_warnings",
    [
        pytest.param(
            "chunked_uncompressed",
            False,
            np.int64,
            positive_false_long,
            id="chunked-uncompressed-false-int64",
        ),
        pytest.param(
            "chunked_uncompressed",
            True,
            np.int64,
            positive_true_long,
            id="chunked-uncompressed-true-int64",
        ),
        pytest.param(
            "chunked_compressed",
            False,
            np.int64,
            positive_false_long,
            id="chunked-compressed-false-int64",
        ),
        pytest.param(
            "chunked_compressed",
            True,
            np.int64,
            positive_true_long,
            id="chunked-compressed-true-int64",
        ),
        pytest.param(
            "contiguous",
            False,
            np.int64,
            positive_false_long,
            id="contiguous-false-int64",
        ),
        pytest.param(
            "contiguous",
            True,
            np.int64,
            positive_true_long,
            id="contiguous-true-int64",
        ),
    ],
)
def test_validate_file_positive_int(
    storage_layout, tmp_path, positive, data_type, caplog, expected_warnings
):
    file_path = tmp_path / f"{storage_layout}.nxs"
    # FIX
    with h5py.File(file_path, "w", track_order=True) as h5w:
        trg = "/entry/instrument/electronanalyzer/electron_detector/raw_data"
        for idx, class_name in enumerate(
            ["ENTRY", "INSTRUMENT", "ELECTRONANALYZER", "ELECTRON_DETECTOR"]
        ):
            grp = h5w.create_group(f"{'/'.join(trg.split('/')[0 : idx + 2])}")
            grp.attrs["NX_class"] = f"NX{class_name.lower()}"

        axes = ["pixel_y", "pixel_x"]
        grp = h5w.create_group(f"{trg}")
        grp.attrs["NX_class"] = "NXdata"
        grp.attrs["axes"] = axes
        grp.attrs["signal"] = "raw"
        for idx, axis in enumerate(axes):
            grp.attrs[f"{axis}_indices"] = np.int32(idx)  # should be NX_UINT
        dst = h5w.create_dataset(f"{trg}/raw", data=np.zeros((1024, 1024), np.float32))
        for idx, axis in enumerate(axes):
            if positive:
                pixel = np.linspace(
                    0, 1024 - 1, num=1024, endpoint=True, dtype=data_type
                )
            else:
                pixel = np.linspace(
                    -512, 1024 - 1 - 512, num=1024, endpoint=True, dtype=data_type
                )
            if storage_layout == "chunked_uncompressed":
                dst = h5w.create_dataset(f"{trg}/{axis}", data=pixel, chunks=(128,))
            elif storage_layout == "chunked_compressed":
                dst = h5w.create_dataset(
                    f"{trg}/{axis}",
                    data=pixel,
                    chunks=(128,),
                    compression="gzip",
                    compression_opts=1,
                )
            else:  # contiguous
                dst = h5w.create_dataset(f"{trg}/{axis}", data=pixel)
        dst = h5w.create_dataset("/entry/definition", data="NXmpes")

    assert os.path.isfile(file_path)

    validate(file_path)

    with caplog.at_level(logging.INFO):
        observed_warnings = [
            rec.message
            for rec in caplog.records
            if rec.levelno == logging.WARNING
            and not rec.message.startswith(
                "WARNING: Invalid: The entry `entry` in file"
            )
        ]
        assert observed_warnings == expected_warnings

    os.remove(file_path)
