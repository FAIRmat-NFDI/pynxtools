# SPDX-FileCopyrightText: The NOMAD Authors
#
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
# Full license text: LICENSES/Apache-2.0.txt. See docs/learn/pynxtools/licensing.md
# for why this package mixes Apache-2.0 and LGPL-3.0-or-later licensed files.
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

    The higher-level (ancestor) concept wins the unqualified name. When a field
    collides with an inherited SubSection, the field is renamed with a
    ``_quantity`` suffix.

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

# TODO: this should be done in code and not hard-coded here, but we have to
# wait until the schema has stabilized.

# Maps NXDL top-level class name → list of fully-qualified NOMAD class names.
# Multiple entries produce multiple extra Python bases, e.g.:
#   "NXentry": ["nomad.datamodel.metainfo.basesections.v2.Activity",
#               "nomad.datamodel.data.EntryData"]
#   → class Entry(Object, basesections.Activity, EntryData)
#
# Targets basesections v2 (nomad.datamodel.metainfo.basesections.v2), not v1.
# "NXobject" also determines Object's own base (the root of every
# generated class): plain ArchiveSection, not BaseSection, so that generated
# classes are not universally EntryData-bearing (independently creatable as a
# standalone NOMAD entry) unless a more specific mapping below says so.
BASESECTIONS_MAP: dict[str, list[str]] = {
    "NXobject": ["nomad.datamodel.data.ArchiveSection"],
    "NXentry": [
        "nomad.datamodel.metainfo.basesections.v2.Activity",
        "nomad.datamodel.data.EntryData",
    ],
    "NXroot": [
        "nomad.datamodel.metainfo.basesections.v2.Experiment",
        "nomad.datamodel.data.EntryData",
    ],
    # NXsubentry is "virtually identical to NXentry", so it gets the same
    # default as Entry: Activity, not Measurement. Unlike Entry, Subentry is
    # a single generic base class (not generated per-application), so it
    # can't opt into Measurement per app the way Mpes/Xps/... do — a
    # subentry can just as well hold simulation-only content (e.g. nested
    # inside an EM entry) as a real measurement.
    "NXsubentry": ["nomad.datamodel.metainfo.basesections.v2.Activity"],
    # NXprocess is data-provenance (program/version/sequence_index/date), not a
    # physical sample transformation — maps to Analysis, not the physical-
    # transformation-only basesections.Process.
    "NXprocess": ["nomad.datamodel.metainfo.basesections.v2.Analysis"],
    # NXsample/NXsample_component both extend NXcomponent at the NXDL level and
    # match System's own shape (formula/geometry/entity identity).
    # The direct-containment vs. sub_systems wrapper mismatch is bridged in
    # Sample.normalize(), not here.
    "NXsample": ["nomad.datamodel.metainfo.basesections.v2.System"],
    "NXsample_component": ["nomad.datamodel.metainfo.basesections.v2.System"],
    "NXfabrication": ["nomad.datamodel.metainfo.basesections.v2.InstrumentEntry"],
    # The in-use, per-activity instrument snapshot — composes a reference to
    # InstrumentEntry rather than inheriting it.
    "NXinstrument": ["nomad.datamodel.metainfo.basesections.v2.Instrument"],
    "NXdata": ["nomad.datamodel.metainfo.basesections.v2.ActivityResult"],
    # NXactivity's only real usage is inside NXhistory, logging physical
    # treatments applied to a sample/instrument. That matches Process's
    # semantics despite its own docstring reading as a generic superclass.
    "NXactivity": ["nomad.datamodel.metainfo.basesections.v2.Process"],
}

# Application definitions (category="application") default to Entry's own base
# (basesections.v2.Activity, via NXentry unwrapping).
# Not every NXentry is a real measurement (simulation-only entries exist), so
# this is an explicit, per-application classification, not something inferred
# from NXDL content. Applications NOT listed here default to also mixing in
# Measurement, to avoid silently changing semantics for any application not
# yet explicitly reviewed. NXem/NXapm entries _can_ be simulation-only and
# should NOT get Measurement.
APPLICATIONS_WITHOUT_MEASUREMENT: frozenset[str] = frozenset({"NXem", "NXapm"})

_MEASUREMENT_FQN = "nomad.datamodel.metainfo.basesections.v2.Measurement"

_DEFAULT_BASE: list[str] = ["nomad.datamodel.data.ArchiveSection"]


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
