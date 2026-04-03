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


# parameterized ["chunked_uncompressed", "chunked_compressed", "contiguous"]:
def test_validate_file_different_storage_layouts(storage_layout: str, caplog):
    """Test validation of a NeXus/HDF5 with the same content but different storage layout."""
    file_path = f"{storage_layout}.nxs"  # prefix
    prng = np.random.default_rng(seed=42)  # deterministic seeding
    n_values = 1000 * 50 * 50
    with h5py.File(file_path, "w", track_order=True) as h5w:
        gcpl = h5w.id.get_create_plist()
        flags = gcpl.get_link_creation_order()
        # bool(flags & h5p.CRT_ORDER_TRACKED)
        # bool(flags & h5p.CRT_ORDER_INDEXED)

        trg = "/entry1/measurement/event1/image1/stack_2d"
        for idx, class_name in enumerate(["ENTRY", "EM_MEASUREMENT", "EM_EVENT_DATA", "IMAGE"]):
            grp = h5w.create_group(f"{'/'.join(trg.split('/')[0:idx + 2])}")
            grp.attrs["NX_class"] = f"NX{class_name.lower()}"
        grp = h5w.create_group(f"{trg}")

        chunking = (100, 50, 50)
        axes = ["indices_image", "axis_j", "axis_i"]
        real = np.asarray(prng.random(size=n_values), np.float32).reshape(-1, 50, 50)
        # [0, 1), last is fastest
        grp.attrs["NX_class"] = "NXdata"
        grp.attrs["axes"] = axes
        grp.attrs["signal"] = "real"
        for idx, axis in enumerate(axes):
            grp.attrs[f"{axis}_indices"] = np.int32(idx)  # should be NX_UINT
        if storage_layout == "chunked_uncompressed":
            dst = h5w.create_dataset(f"{trg}/real", data=real, chunks=chunking)
        elif storage_layout == "chunked_compressed":
            dst = h5w.create_dataset(f"{trg}/real", data=real, chunks=chunking, compression="gzip", compression_opts=1)
        else:  # contiguous
            dst = h5w.create_dataset(f"{trg}/real", data=real)
        dst.attrs["long_name"] = "real"
        for idx, axis in enumerate(axes):
            dst = h5w.create_dataset(f"{trg}/{axis}", data=np.asarray(np.arange(np.shape(real)[idx]), np.int32))
            dst.attrs["long_name"] = axis
        dst = h5w.create_dataset("/entry1/definition", data="NXem")

    assert os.path.isfile(file_path)

    validate(file_path)

    with caplog.at_level(logging.INFO):
        observed_infos = [
            rec.getMessage() for rec in caplog.records if rec.levelno == logging.INFO
        ]

    os.remove(file_path)


def test_validate_file_positive_int(storage_layout: str, positive: bool, dtype, caplog):
    file_path = f"{storage_layout}.nxs"  # prefix
    n_values = 1000 * 50 * 50
    # FIX
    with h5py.File(file_path, "w", track_order=True) as h5w:
        trg = "/entry1/measurement/event1/image1/stack_2d"
        for idx, class_name in enumerate(["ENTRY", "EM_MEASUREMENT", "EM_EVENT_DATA", "IMAGE"]):
            grp = h5w.create_group(f"{'/'.join(trg.split('/')[0:idx + 2])}")
            grp.attrs["NX_class"] = f"NX{class_name.lower()}"
        grp = h5w.create_group(f"{trg}")

        chunking = (100, 50, 50)
        axes = ["indices_image", "axis_j", "axis_i"]
        real = np.asarray(np.ones(size=n_values), dtype)
        if not positive:
            real[0:n_values:int(np.prod(chunking))] = -1
        real.reshape(-1, 50, 50)

        grp.attrs["NX_class"] = "NXdata"
        grp.attrs["axes"] = axes
        grp.attrs["signal"] = "real"
        for idx, axis in enumerate(axes):
            grp.attrs[f"{axis}_indices"] = np.int32(idx)  # should be NX_UINT
        if storage_layout == "chunked_uncompressed":
            dst = h5w.create_dataset(f"{trg}/real", data=real, chunks=chunking)
        elif storage_layout == "chunked_compressed":
            dst = h5w.create_dataset(f"{trg}/real", data=real, chunks=chunking, compression="gzip", compression_opts=1)
        else:  # contiguous
            dst = h5w.create_dataset(f"{trg}/real", data=real)
        dst.attrs["long_name"] = "real"
        for idx, axis in enumerate(axes):
            dst = h5w.create_dataset(f"{trg}/{axis}", data=np.asarray(np.arange(np.shape(real)[idx]), np.int32))
            dst.attrs["long_name"] = axis
        dst = h5w.create_dataset("/entry1/definition", data="NXem")

    assert os.path.isfile(file_path)

    validate(file_path)

    with caplog.at_level(logging.INFO):
        observed_infos = [
            rec.getMessage() for rec in caplog.records if rec.levelno == logging.INFO
        ]

    os.remove(file_path)
