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
    import nomad
except ImportError:
    pytest.skip(
        "Skipping NOMAD example tests because nomad is not installed",
        allow_module_level=True,
    )

from pynxtools.nomad.apis import ontology_service
from pynxtools.nomad.entrypoints import simple_nexus_example
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
    "examples",
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


def test_ontology_service_entry_point():
    """Test that the ontology service entry point exposes the FastAPI app."""
    assert hasattr(ontology_service, "app")
    assert ontology_service.app.title == "Ontology Service"
    if hasattr(ontology_service, "ontology_service_entry_point"):
        ep = ontology_service.ontology_service_entry_point
        assert ep.name == "ontology_service"
        assert ep.prefix == "/ontology_service"
