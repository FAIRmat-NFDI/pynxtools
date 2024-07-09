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
"""Compute hashes of files for provenance tracking of data sources."""

import hashlib


def get_file_hashvalue(file_name: str) -> str:
    """Compute a hashvalue of given file, here SHA256."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_name, "rb") as file_handle:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: file_handle.read(4096), b""):
                sha256_hash.update(byte_block)
    except IOError:
        print(f"File {file_name} is not accessible !")

    return sha256_hash.hexdigest()
