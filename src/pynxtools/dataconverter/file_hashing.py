# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
    except OSError:
        print(f"File {file_name} is not accessible !")

    return sha256_hash.hexdigest()
