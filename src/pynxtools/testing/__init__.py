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
