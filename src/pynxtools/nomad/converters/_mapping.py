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
Naming utilities for converting NXDL names to Python / NOMAD conventions.
"""

from __future__ import annotations

# NOMAD BaseSection quantity names that every generated class inherits via
# Object(basesections.BaseSection). Used by both naming functions below, for
# two different reasons:
# - nxdl_to_subsection_name: a SubSection can never override a same-named
#   Quantity (different property kinds) — NOMAD raises MetainfoError
#   ("Cannot inherit from different property types") rather than replacing
#   it. Confirmed by NXlauetof's NXdata group literally named "name", which
#   fails to load without the suffix.
# - nxdl_to_quantity_name: a scalar field MAY safely override (NOMAD replaces
#   cleanly, confirmed type-compatible across the whole NXDL corpus), but an
#   array-shaped one should not — BaseSection's own normalize() and related
#   logic (e.g. `archive.metadata.entry_name = self.name`,
#   `Workflow(name=self.name)`) treats these as scalars throughout, so an
#   array override is allowed by NOMAD but silently wrong: confirmed by
#   NXmicrostructure_score_config's array-of-strings "name" field, which is
#   deliberately not a scalar (see nexus_definitions#428 — rejected, the
#   array is intentional, one name per texture component).
_BASESECTION_RESERVED_NAMES: frozenset[str] = frozenset(
    {"name", "datetime", "lab_id", "description"}
)


def nxdl_to_class_name(nx_name: str) -> str:
    """Convert an NXDL class name (e.g. 'NXoptical_spectroscopy') to a
    Python CamelCase class name ('OpticalSpectroscopy').

    Examples
    --------
    >>> nxdl_to_class_name("NXentry")
    'Entry'
    >>> nxdl_to_class_name("NXxps")
    'Xps'
    >>> nxdl_to_class_name("NXoptical_spectroscopy")
    'OpticalSpectroscopy'
    """
    stem = nx_name[2:] if nx_name.startswith("NX") else nx_name
    parts = stem.split("_")
    return "".join(p.capitalize() for p in parts if p)


def nxdl_to_quantity_name(nxdl_name: str, has_shape: bool = False) -> str:
    """Convert an NXDL field/attribute name to a safe Python quantity name.

    Python keywords always get a ``_quantity`` suffix. A *scalar* field named
    like a NOMAD BaseSection quantity (``name``, ``datetime``, ``lab_id``,
    ``description``) is *not* suffixed — NOMAD allows a subclass to directly
    override an inherited quantity, replacing it cleanly (confirmed type-
    compatible across the whole NXDL corpus, and confirmed by reading
    ``Section.__init_metainfo__()`` that NOMAD never raises for this, only
    for a property-kind mismatch). An *array-shaped* field with one of these
    names still gets the suffix, even though NOMAD would also accept that
    override without error: BaseSection's own ``normalize()`` and related
    logic treat ``self.name``/``self.datetime``/etc. as scalars throughout
    its inheritance chain, so an array silently breaks that — not something
    the generator can rely on NOMAD to catch for us, unlike the property-kind
    mismatch case.

    Examples
    --------
    >>> nxdl_to_quantity_name("start_time")
    'start_time'
    >>> nxdl_to_quantity_name("name")
    'name'
    >>> nxdl_to_quantity_name("name", has_shape=True)
    'name_quantity'
    >>> nxdl_to_quantity_name("lambda")
    'lambda_quantity'
    """
    import keyword

    if keyword.iskeyword(nxdl_name):
        return f"{nxdl_name}_quantity"
    if has_shape and nxdl_name in _BASESECTION_RESERVED_NAMES:
        return f"{nxdl_name}_quantity"
    return nxdl_name


def field_conflicts_with_group(python_name: str) -> str:
    """Return a renamed Quantity python_name that no longer collides with a SubSection.

    Groups always win the unqualified name. The conflicting field Quantity is
    renamed with a ``_quantity`` suffix.

    Examples
    --------
    >>> field_conflicts_with_group("sample_component")
    'sample_component_quantity'
    >>> field_conflicts_with_group("magnetic_field")
    'magnetic_field_quantity'
    """
    return f"{python_name}_quantity"


def nxdl_to_subsection_name(nxdl_name: str) -> str:
    """Convert an NXDL group name to a safe Python subsection name.

    Variadic groups (nameType=any/partial) use the lowercase NXDL class name
    without the NX prefix as the subsection name. Groups named like a NOMAD
    BaseSection quantity get a ``_group`` suffix — see
    _BASESECTION_RESERVED_NAMES.

    Examples
    --------
    >>> nxdl_to_subsection_name("instrument")
    'instrument'
    >>> nxdl_to_subsection_name("name")
    'name_group'
    """
    if nxdl_name in _BASESECTION_RESERVED_NAMES:
        return f"{nxdl_name}_group"
    return nxdl_name


# ---------------------------------------------------------------------------
# Base section mapping
# ---------------------------------------------------------------------------

# TODO: this should be done in code and
# Maps NXDL top-level class name → list of fully-qualified NOMAD class names.
# Multiple entries produce multiple extra Python bases, e.g.:
#   "NXentry": ["nomad.datamodel.metainfo.basesections.Measurement",
#               "nomad.datamodel.data.EntryData"]
#   → class Entry(Object, basesections.Measurement, EntryData)
BASESECTIONS_MAP: dict[str, list[str]] = {
    "NXobject": ["nomad.datamodel.metainfo.basesections.BaseSection"],
    "NXentry": [
        "nomad.datamodel.metainfo.basesections.Measurement",
        "nomad.datamodel.data.EntryData",
    ],
    "NXprocess": ["nomad.datamodel.metainfo.basesections.ActivityStep"],
    "NXsample": ["nomad.datamodel.metainfo.basesections.CompositeSystem"],
    "NXsample_component": ["nomad.datamodel.metainfo.basesections.Component"],
    "NXfabrication": ["nomad.datamodel.metainfo.basesections.Instrument"],
    "NXdata": ["nomad.datamodel.metainfo.basesections.ActivityResult"],
}

_DEFAULT_BASE: list[str] = ["nomad.datamodel.metainfo.basesections.BaseSection"]


def get_base_section(nx_name: str) -> list[str]:
    """Return list of fully-qualified NOMAD class names for the extra Python bases
    that a given NXDL top-level class should inherit from.

    Each string is a dotted module.ClassName path. The last component is the
    class name; everything before it is the import module.
    Falls back to ["nomad.datamodel.metainfo.basesections.BaseSection"].
    """
    return BASESECTIONS_MAP.get(nx_name, _DEFAULT_BASE)


# ---------------------------------------------------------------------------
# NX type → NOMAD type string (as used in generated source code)
# ---------------------------------------------------------------------------

# Values are the string expressions written into generated .py files.
# numpy types are written as np.<name> so the template must import numpy as np.
NX_TYPE_TO_SOURCE: dict[str, str] = {
    "NX_FLOAT": "np.float64",
    "NX_INT": "np.int64",
    "NX_UINT": "np.int64",  # NOMAD has no unsigned int; annotation preserves intent
    "NX_NUMBER": "np.float64",
    "NX_POSINT": "np.int64",
    "NX_COMPLEX": "np.complex128",
    "NX_CHAR": "str",
    "NX_BOOLEAN": "bool",
    "NX_BINARY": "Bytes",  # nomad.metainfo.data_type.Bytes
    "NX_DATE_TIME": "Datetime",  # from nomad.metainfo.data_type
    "NX_CHAR_OR_NUMBER": "np.float64",
}

_DEFAULT_NX_TYPE_SOURCE = "str"


def nx_type_to_source(nx_type: str | None) -> str:
    """Return the Python source expression for a given NX primitive type."""
    if not nx_type:
        return _DEFAULT_NX_TYPE_SOURCE
    return NX_TYPE_TO_SOURCE.get(nx_type, _DEFAULT_NX_TYPE_SOURCE)
