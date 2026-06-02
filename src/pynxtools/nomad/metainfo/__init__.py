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
NeXus NOMAD metainfo: public API and schema package entry points.

Programmatic use
----------------
::

    from pynxtools.nomad.metainfo import build_base_classes_package, all_sections

build_base_classes_package()  — assemble and return the SchemaPackage of all NeXus base
                                 class Section definitions.
all_sections()   — shorthand: return the list of Section definitions directly.

NOMAD entry points
------------------
All SchemaPackageEntryPoint objects for schema packages defined under
pynxtools.nomad.metainfo are declared here.
Add new ones in the same pattern as the existing entry points below.

nexus_base_classes — Python-native Section classes for all ~142 NeXus base
                     classes, generated from the NXDL definitions bundled
                     with pynxtools.
"""

from __future__ import annotations

from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.metainfo import SchemaPackage


def build_base_classes_package() -> SchemaPackage:
    """Assemble and return the NeXus base classes SchemaPackage."""
    from pynxtools.nomad.metainfo._package import build_base_classes_package as _build

    return _build()


def all_sections() -> list:
    """Return all Section definitions in the NeXus base classes package."""
    return list(build_base_classes_package().section_definitions)


class NexusBaseClassesEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.metainfo._package import build_base_classes_package

        return build_base_classes_package()


nexus_base_classes = NexusBaseClassesEntryPoint(
    name="NeXus Base Classes",
    description=(
        "Python-native NOMAD metainfo Section classes for all NeXus base classes, "
        "generated from the NXDL definitions bundled with pynxtools."
    ),
)
