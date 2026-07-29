# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
NeXus NOMAD metainfo: public API and schema package entry points.

Programmatic use
----------------
::

    from pynxtools.nomad.metainfo import build_base_classes_package, build_applications_package

NOMAD entry points
------------------
nexus_base_classes   — Python-native Section classes for all NeXus base classes
                       (category='base'), generated from NXDL.
nexus_applications   — Python-native Section classes for all NeXus application
                       and contributed definitions (category='application').
"""

from __future__ import annotations

from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.metainfo import SchemaPackage


def build_base_classes_package() -> SchemaPackage:
    """Assemble and return the NeXus base classes SchemaPackage."""
    from pynxtools.nomad.metainfo._package import build_base_classes_package as _build

    return _build()


def build_applications_package() -> SchemaPackage:
    """Assemble and return the NeXus applications SchemaPackage."""
    from pynxtools.nomad.metainfo._package import build_applications_package as _build

    return _build()


def all_sections() -> list:
    """Return all Section definitions in the NeXus base classes package."""
    return list(build_base_classes_package().section_definitions)


class NexusBaseClassesEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.metainfo._package import build_base_classes_package

        return build_base_classes_package()


class NexusApplicationsEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.metainfo._package import build_applications_package

        return build_applications_package()


nexus_base_classes = NexusBaseClassesEntryPoint(
    name="NeXus Base Classes",
    description=(
        "Python-native NOMAD Metainfo Section classes for all NeXus base classes, "
        "generated from the NXDL definitions bundled with pynxtools."
    ),
)

nexus_applications = NexusApplicationsEntryPoint(
    name="NeXus Application Definitions",
    description=(
        "Python-native NOMAD Metainfo Section classes for all NeXus application "
        "and contributed definitions, generated from the NXDL definitions bundled "
        "with pynxtools."
    ),
)
