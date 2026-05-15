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
Public API for the ``pynxtools.dataconverter`` sub-package.

Reader interface
----------------
BaseReader
    Abstract base class for all pynxtools reader plugins.
MultiFormatReader
    Concrete base reader that dispatches to per-format file handlers.
    Subclass this to build a new reader plugin.
JsonMapReader
    Built-in MultiFormatReader that reads data from HDF5/JSON/YAML files
    combined with a JSON config/mapping file.

Template
--------
Template
    Dict-like container that tracks NeXus template paths by optionality
    (required / recommended / optional / undocumented).

Conversion
----------
convert(...)
    Convert experimental data to NeXus/HDF5 using a named reader.
get_reader(name)
    Load a reader by entry-point name.
get_names_of_all_readers()
    List all installed reader entry-point names.
ValidationFailed
    Exception raised when converted data fails NeXus schema validation.

Validation
----------
validate_hdf_group_against(appdef, hdf_group, ...)
    Validate an HDF5 group against a NeXus application definition.
validate_dict_against(appdef, data_dict)
    Validate a flat data dictionary against a NeXus application definition.
"""

# Lazy re-exports to avoid the circular import:
#   nexus.nexus_tree → dataconverter.helpers → (this __init__) → convert/validation
#   → nexus_tree shim → nexus.nexus_tree  (partially initialized → ImportError)
_TEMPLATE = "pynxtools.dataconverter.template"
_CONVERT = "pynxtools.dataconverter.convert"
_BASE_READER = "pynxtools.dataconverter.readers.base.reader"
_MULTI_READER = "pynxtools.dataconverter.readers.multi.reader"
_JSON_MAP_READER = "pynxtools.dataconverter.readers.json_map.reader"
_VALIDATION = "pynxtools.dataconverter.validation"
_HELPERS = "pynxtools.dataconverter.helpers"

_LAZY: dict[str, str] = {
    # Reader interface
    "BaseReader": _BASE_READER,
    "MultiFormatReader": _MULTI_READER,
    "JsonMapReader": _JSON_MAP_READER,
    # Template
    "Template": _TEMPLATE,
    # Conversion
    "convert": _CONVERT,
    "get_reader": _CONVERT,
    "get_names_of_all_readers": _CONVERT,
    "ValidationFailed": _CONVERT,
    # Template generation
    "generate_template_from_nxdl": _HELPERS,
    # Validation
    "validate_hdf_group_against": _VALIDATION,
    "validate_dict_against": _VALIDATION,
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


# Backwards compatibility: helpers.validate_data_dict is defined directly in helpers.py as a lazy
# forwarder to break the circular import that would arise from an eager import here:
#   nexus.nexus_tree → dataconverter.helpers → (this __init__) → validation → nexus.nexus_tree
# Call _apply_monkey_patch() if the real function object is needed (e.g. identity checks).
def _apply_monkey_patch() -> None:
    """Replace the lazy forwarder with the real validate_data_dict from validation."""
    from pynxtools.dataconverter import helpers, validation

    helpers.validate_data_dict = validation.validate_data_dict  # type: ignore
