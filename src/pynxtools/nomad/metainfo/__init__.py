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
Public API for pynxtools NeXus NOMAD metainfo.

    from pynxtools.nomad.metainfo import build_package, all_sections

build_package() — assemble and return the SchemaPackage containing all
                   NeXus base class section definitions.
all_sections()  — return a list of all generated Section definitions.
"""

from __future__ import annotations

from nomad.metainfo import SchemaPackage


def build_package() -> SchemaPackage:
    """Assemble and return the NeXus base classes SchemaPackage."""
    from pynxtools.nomad.metainfo._package import build_package as _build

    return _build()


def all_sections() -> list:
    """Return all Section definitions in the NeXus base classes package."""
    pkg = build_package()
    return list(pkg.section_definitions)
