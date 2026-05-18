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
Assembles all generated NeXus base class sections into a single NOMAD Package.

build_package() is the only public function.  It:
1. Imports all 142 generated base_classes/*.py modules.
2. Collects each module's top-level generated Section definition.
3. Combines them into a single Package and calls __init_metainfo__() to
   resolve all string-proxy SubSection references.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from nomad.metainfo import Package

import pynxtools.nomad.annotations  # noqa: F401 — registers NeXusGroup / NeXusQuantity

_BASE_CLASSES_DIR = Path(__file__).parent / "base_classes"
_PACKAGE_NAME = "pynxtools.nomad.metainfo.base_classes"

_m_package: Package | None = None


def _is_generated_section(obj: object, module_name: str) -> bool:
    """Return True if obj is a Section definition generated in this module."""
    from nomad.metainfo.metainfo import Section as NomadSection

    m_def = getattr(obj, "m_def", None)
    if not isinstance(m_def, NomadSection):
        return False
    # Only pick up classes whose m_def was created in this specific module
    # (not imported helpers like BaseSection, Quantity, etc.)
    defining_module = getattr(obj, "__module__", None)
    return defining_module == module_name


def build_package() -> Package:
    """Import all generated base class modules and assemble a single Package."""
    global _m_package
    if _m_package is not None:
        return _m_package

    m_package = Package(name=_PACKAGE_NAME)

    py_files = sorted(_BASE_CLASSES_DIR.glob("*.py"))
    for py_file in py_files:
        if py_file.stem == "__init__":
            continue
        module_name = f"{_PACKAGE_NAME}.{py_file.stem}"
        mod = importlib.import_module(module_name)
        for attr_name in dir(mod):
            obj = getattr(mod, attr_name, None)
            if _is_generated_section(obj, module_name):
                m_package.section_definitions.append(obj.m_def)

    try:
        m_package.__init_metainfo__()
    except Exception as exc:
        # Phase 1: base_classes only.  Cross-category SubSection references
        # (e.g. NXphase → contributed NXmicrostructure_ipf) cannot be resolved
        # until Phase 2 generates those modules.  Warn and continue; the
        # affected subsections will be unresolvable until then.
        import warnings

        warnings.warn(
            f"Package initialization incomplete: {exc}. "
            "Some cross-category SubSection references may be unresolved.",
            stacklevel=2,
        )
    _m_package = m_package
    return m_package


build_package()
