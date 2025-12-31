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
"""Use-case-specific configurations to optimize performance for chunked storage."""

# https://github.com/h5py/h5py/blob/master/docs/high/file.rst

CHUNK_CONFIG_HFIVEPY: dict[str, int | float] = {
    "byte_size": 1 * 1024 * 1024,
    "rdcc_nbytes": 1 * 1024 * 1024,  # 1 MiB before HDF2.0, will be 8 MiB for HDF2.0
    "rdcc_nslots": 521,
    "rdcc_w0": 0.75,
}
CHUNK_CONFIG_SSD_NVM: dict[str, int | float] = {
    "byte_size": 1 * 1024 * 1024,
    "rdcc_nbytes": 128 * 1024 * 1024,
    "rdcc_nslots": 4093,
    "rdcc_w0": 0.75,
}
CHUNK_CONFIG_HDD: dict[str, int | float] = {
    "byte_size": 4 * 1024 * 1024,
    "rdcc_nbytes": 256 * 1024 * 1024,
    "rdcc_nslots": 1021,
    "rdcc_w0": 0.75,
}
CHUNK_CONFIG_GPFS: dict[str, int | float] = {
    "byte_size": 8 * 1024 * 1024,
    "rdcc_nbytes": 256 * 1024 * 1024,
    "rdcc_nslots": 521,
    "rdcc_w0": 0.75,
}

CHUNK_CONFIG_LUSTRE: dict[str, int | float] = {
    # set stripe size before creating a file!
    "byte_size": 8 * 1024 * 1024,
    "rdcc_nbytes": 256 * 1024 * 1024,
    "rdcc_nslots": 521,
    "rdcc_w0": 0.75,
}

CHUNK_CONFIG_DEFAULT = CHUNK_CONFIG_SSD_NVM
