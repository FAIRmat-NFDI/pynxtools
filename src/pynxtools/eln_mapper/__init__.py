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
