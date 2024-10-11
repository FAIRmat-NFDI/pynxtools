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
import pytest

try:
    from nomad.parsing.parser import ArchiveParser
    from nomad.datamodel import EntryArchive, Context
except ImportError:
    pytest.skip(
        "Skipping NOMAD example tests because nomad is not installed",
        allow_module_level=True,
    )


def get_file_parameter():
    example_files = [
        "schema.archive.yaml",
        "schema.archive.json",
        "intra-entry.archive.json",
    ]
    path = os.walk(os.path.join(os.path.dirname(__file__), "../../examples/nomad"))
    for root, _, files in path:
        for file in files:
            if os.path.basename(file) in example_files:
                yield pytest.param(os.path.join(root, file), id=file)


@pytest.mark.parametrize("mainfile", get_file_parameter())
def test_nomad_example(mainfile, no_warn):
    """Test if NOMAD example works."""
    archive = EntryArchive()
    archive.m_context = Context()
    ArchiveParser().parse(mainfile, archive)
    archive.m_to_dict()
