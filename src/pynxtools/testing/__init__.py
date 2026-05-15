# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Public API for the ``pynxtools.testing`` sub-package.

ReaderTest
    Pytest-compatible test class for validating pynxtools reader plugins.
    Provides parametrized round-trip conversion tests against reference NeXus
    files and optional NOMAD-parsing smoke tests.

NOMAD example utilities (require ``nomad-lab`` + pytest):

get_file_parameter(example_path)
    Collect all example files under a plugin's example-upload path.
parse_nomad_examples(mainfile)
    Parse a NOMAD example upload entry and return the resulting archive dict.
example_upload_entry_point_valid(entry_points, tmp_path)
    Pytest fixture-style validator for NOMAD ExampleUpload entry points.
"""

from pynxtools.testing.nexus_conversion import ReaderTest

__all__ = [
    "ReaderTest",
    # NOMAD example helpers — available when nomad-lab is installed
    "get_file_parameter",
    "parse_nomad_examples",
    "example_upload_entry_point_valid",
]

_NOMAD_EXAMPLE = "pynxtools.testing.nomad_example"

_LAZY: dict[str, str] = {
    "get_file_parameter": _NOMAD_EXAMPLE,
    "parse_nomad_examples": _NOMAD_EXAMPLE,
    "example_upload_entry_point_valid": _NOMAD_EXAMPLE,
}


def __getattr__(name: str):
    if name in _LAZY:
        import importlib

        module = importlib.import_module(_LAZY[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
