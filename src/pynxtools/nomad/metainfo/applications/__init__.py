# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

# Module-level __getattr__ so that NOMAD can resolve application section classes
# by flat qualified name (e.g. "pynxtools.nomad.metainfo.applications.Arpes").
#
# Application classes are split across one SchemaPackage per technique, not one
# "applications" package, so this  scans every technique package instead of a
# single fixed package name.

_class_cache: dict[str, type] = {}
# Derived from this module's own __name__/__package__, not hardcoded, so this
# stays correct if this package is ever moved.
_PKG_NAME = __name__
_METAINFO_ROOT = __package__.rsplit(".", 1)[0]  # strip trailing ".applications"


def __getattr__(name: str) -> type:
    if name in _class_cache:
        return _class_cache[name]
    try:
        from nomad.metainfo.metainfo import Package

        from pynxtools.nomad.metainfo import packages

        candidate_names = [_PKG_NAME] + [
            f"{_METAINFO_ROOT}.{technique}" for technique in packages
        ]
        for pkg_name in candidate_names:
            pkg = Package.registry.get(pkg_name)
            if pkg is None:
                continue
            for sec_def in pkg.section_definitions:
                if sec_def.name == name and sec_def.section_cls is not None:
                    _class_cache[name] = sec_def.section_cls
                    return sec_def.section_cls
    except Exception:
        pass
    raise AttributeError(f"module {_PKG_NAME!r} has no attribute {name!r}")
