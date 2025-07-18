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
"""Test for NOMAD examples in reader plugins."""

import os
import tempfile
from typing import Any

import pytest

try:
    from nomad.config.models.plugins import ExampleUploadEntryPoint
    from nomad.datamodel import Context, EntryArchive
    from nomad.parsing.parser import ArchiveParser
except ImportError:
    pytest.skip(
        "Skipping NOMAD example tests because nomad is not installed",
        allow_module_level=True,
    )


def get_file_parameter(example_path: str):
    """
    Get all example files for the plugin.

    This function searches for specific example files in the given directory path.

    Args:
        example_path (str): Path to the directory containing example files.

    Yields:
        pytest.param: A pytest parameter object with the file path and file ID.
    """
    example_files = (
        "schema.archive.yaml",
        "schema.archive.yml",
        "scheme.archive.yaml",
        "scheme.archive.yml",
        "schema.archive.json",
        "scheme.archive.json",
        "intra-entry.archive.json",
    )

    # Check if the provided path exists
    if not os.path.exists(example_path):
        raise FileNotFoundError(f"The directory '{example_path}' does not exist.")

    # Walk through the specified directory
    for root, _, files in os.walk(example_path):
        for file in files:
            normalized_file = file.lower()  # Normalize to lower case
            if os.path.basename(normalized_file).endswith(example_files):
                yield pytest.param(os.path.join(root, file), id=file)


def parse_nomad_examples(mainfile: str) -> dict[str, Any]:
    """Parse a NOMAD example file and return its dictionary representation.

    Args:
        mainfile (str): The path to the NOMAD example file to be parsed.

    Returns:
        dict[str, Any]: A dictionary representation of the parsed NOMAD example.

    Raises:
        FileNotFoundError: If the mainfile does not exist.
    """
    if not os.path.exists(mainfile):
        raise FileNotFoundError(f"The specified file '{mainfile}' does not exist.")

    archive = EntryArchive()
    archive.m_context = Context()

    ArchiveParser().parse(mainfile, archive)
    return archive.m_to_dict()


def example_upload_entry_point_valid(
    entrypoint: ExampleUploadEntryPoint, example_path: str
) -> None:
    """
    Test if NOMAD ExampleUploadEntryPoint works.

    Args:
        entrypoint (nomad.config.models.plugins.ExampleUploadEntryPoint): The entry point to test.
        example_path (str): String path of the example.

    """
    expected_upload_files = []
    for dirpath, dirnames, filenames in os.walk(example_path):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(dirpath, filename), example_path)
            expected_upload_files.append(file_path)

    with tempfile.TemporaryDirectory() as tmp_upload_directory:
        entrypoint.load(tmp_upload_directory)

        # Add upload folder as root to all expected upload_filepath
        expected_upload_files = [
            os.path.join(tmp_upload_directory, path) for path in expected_upload_files
        ]

        # Check that all expected upload_files are created
        real_upload_files = []
        for dirpath, _, filenames in os.walk(tmp_upload_directory):
            for filename in filenames:
                real_upload_files.append(
                    os.path.abspath(os.path.join(dirpath, filename))
                )

        assert sorted(real_upload_files) == sorted(expected_upload_files), (
            f"Uploaded files {real_upload_files} do not match the expected files: {expected_upload_files}"
        )
