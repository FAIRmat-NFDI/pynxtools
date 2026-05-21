# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Test for NOMAD examples in reader plugins."""

import os

import pytest

try:
    import nomad
except ImportError:
    pytest.skip(
        "Skipping NOMAD example tests because nomad is not installed",
        allow_module_level=True,
    )

from pynxtools.nomad.example_uploads import simple_nexus_example
from pynxtools.testing.nomad_example import (
    example_upload_entry_point_valid,
    get_file_parameter,
    parse_nomad_examples,
)

EXAMPLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "src",
    "pynxtools",
    "nomad",
    "example_uploads",
    "iv_temp_example",
)


@pytest.mark.parametrize(
    "mainfile",
    get_file_parameter(EXAMPLE_PATH),
)
def test_parse_nomad_examples(mainfile):
    """Test if NOMAD examples work."""
    archive_dict = parse_nomad_examples(mainfile)


@pytest.mark.parametrize(
    ("entrypoint", "example_path"),
    [
        pytest.param(
            simple_nexus_example,
            os.path.join(EXAMPLE_PATH, "."),
            id="simple_nexus_example",
        ),
    ],
)
def test_example_upload_entry_point_valid(entrypoint, example_path):
    """Test if NOMAD ExampleUploadEntryPoint works."""
    example_upload_entry_point_valid(
        entrypoint=entrypoint,
        example_path=example_path,
    )
