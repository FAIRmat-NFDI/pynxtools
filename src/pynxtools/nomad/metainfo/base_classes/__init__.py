# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

# Module-level __getattr__ so that NOMAD can resolve section classes by flat
# qualified name (e.g. "pynxtools.nomad.metainfo.base_classes.Data") from
# archived data.  NOMAD's SectionProxy._resolve_by_definition_name() imports
# this package and calls getattr(module, class_name) — without this hook the
# lookup would always fail because the classes are spread across sub-modules.

_class_cache: dict[str, type] = {}
_PKG_NAME = "pynxtools.nomad.metainfo.base_classes"


def __getattr__(name: str) -> type:
    if name in _class_cache:
        return _class_cache[name]
    try:
        from nomad.metainfo.metainfo import Package

        pkg = Package.registry.get(_PKG_NAME)
        if pkg is not None:
            for sec_def in pkg.section_definitions:
                if sec_def.name == name and sec_def.section_cls is not None:
                    _class_cache[name] = sec_def.section_cls
                    return sec_def.section_cls
    except Exception:
        pass
    raise AttributeError(f"module {_PKG_NAME!r} has no attribute {name!r}")
