# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Public API for the ``pynxtools.eln_mapper`` sub-package.

ElnGenerator
    Abstract base class for ELN YAML template generators.
ReaderElnGenerator
    Generates an ELN YAML template suitable for use with pynxtools readers.
NomadElnGenerator
    Generates a NOMAD-compatible ELN YAML schema from a NeXus application
    definition.
"""

_LAZY: dict[str, str] = {
    "ElnGenerator": "pynxtools.eln_mapper.eln",
    "ReaderElnGenerator": "pynxtools.eln_mapper.reader_eln",
    "NomadElnGenerator": "pynxtools.eln_mapper.schema_eln",
}

__all__ = list(_LAZY)


def __getattr__(name: str):
    if name in _LAZY:
        import importlib

        module = importlib.import_module(_LAZY[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
