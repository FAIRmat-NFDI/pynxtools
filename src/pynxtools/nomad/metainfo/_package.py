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
Assembles generated NeXus metainfo sections into NOMAD Packages.

Public functions:
    build_base_classes_package()   — all category='base' classes
    build_applications_package()   — all category='application' classes

Deduplication note
------------------
NOMAD's metaclass auto-adds every Section to a per-module Package when the
class body is executed (metainfo.py ~line 939). If those per-module Packages
are left in place, NOMAD's all_metainfo_packages() scan finds them alongside
our assembled Package and each section appears twice. We prevent this by
replacing each module's m_package attribute with our assembled Package after
import; the scan then finds only the assembled Package for all modules.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from nomad.metainfo import Package

import pynxtools.nomad.annotations  # noqa: F401 — registers NeXusGroup / NeXusQuantity

_BASE_CLASSES_DIR = Path(__file__).parent / "base_classes"
_APPLICATIONS_DIR = Path(__file__).parent / "applications"

_m_base_package: Package | None = None
_m_applications_package: Package | None = None


def _is_generated_section(obj: object, module_name: str) -> bool:
    """Return True if obj is a Section definition generated in this module."""
    from nomad.metainfo.metainfo import Section as NomadSection

    m_def = getattr(obj, "m_def", None)
    if not isinstance(m_def, NomadSection):
        return False
    defining_module = getattr(obj, "__module__", None)
    return defining_module == module_name


def _build_package_from_dir(category_dir: Path, package_name: str) -> Package:
    """Import all *.py modules in category_dir and assemble a single Package."""
    m_package = Package(name=package_name)

    py_files = sorted(category_dir.glob("*.py"))
    for py_file in py_files:
        if py_file.stem == "__init__":
            continue
        module_name = f"{package_name}.{py_file.stem}"
        mod = importlib.import_module(module_name)
        setattr(mod, "m_package", m_package)
        for attr_name in dir(mod):
            obj = getattr(mod, attr_name, None)
            if _is_generated_section(obj, module_name):
                m_package.section_definitions.append(obj.m_def)

    m_package.__init_metainfo__()
    return m_package


def build_base_classes_package() -> Package:
    """Import all generated base class modules and assemble a single Package."""
    global _m_base_package
    if _m_base_package is not None:
        return _m_base_package
    _m_base_package = _build_package_from_dir(
        _BASE_CLASSES_DIR, "pynxtools.nomad.metainfo.base_classes"
    )
    return _m_base_package


def build_applications_package() -> Package:
    """Import all generated application modules and assemble a single Package.

    Ensures base_classes are loaded first so cross-package FQN references
    (application SubSections pointing at base class named-concept classes) resolve.
    """
    global _m_applications_package
    if _m_applications_package is not None:
        return _m_applications_package
    # Base classes must be imported (and their sections registered) before
    # application sections can resolve SubSection FQNs that point into base_classes.
    build_base_classes_package()
    _m_applications_package = _build_package_from_dir(
        _APPLICATIONS_DIR, "pynxtools.nomad.metainfo.applications"
    )
    return _m_applications_package
