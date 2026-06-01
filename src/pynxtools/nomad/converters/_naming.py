"""
Naming utilities for converting NXDL names to Python / NOMAD conventions.
"""

from __future__ import annotations

# NOMAD BaseSection quantity names that conflict with NXDL field names.
# Fields with these names get a `_field` suffix to avoid shadowing.
_RESERVED_QUANTITY_NAMES: frozenset[str] = frozenset(
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


def nxdl_to_quantity_name(nxdl_name: str) -> str:
    """Convert an NXDL field/attribute name to a safe Python quantity name.

    Fields whose names collide with NOMAD BaseSection quantities get a
    ``_field`` suffix.

    Examples
    --------
    >>> nxdl_to_quantity_name("start_time")
    'start_time'
    >>> nxdl_to_quantity_name("name")
    'name_field'
    """
    if nxdl_name in _RESERVED_QUANTITY_NAMES:
        return f"{nxdl_name}_field"
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
    without the NX prefix as the subsection name.
    """
    if nxdl_name in _RESERVED_QUANTITY_NAMES:
        return f"{nxdl_name}_group"
    return nxdl_name


# ---------------------------------------------------------------------------
# Base section mapping
# ---------------------------------------------------------------------------

# Maps NXDL top-level class name → (Python class name, dotted import path)
BASESECTIONS_MAP: dict[str, tuple[str, str]] = {
    "NXobject": ("BaseSection", "nomad.datamodel.metainfo.basesections"),
    "NXentry": ("Measurement", "nomad.datamodel.metainfo.basesections"),
    "NXprocess": ("ActivityStep", "nomad.datamodel.metainfo.basesections"),
    "NXsample": ("CompositeSystem", "nomad.datamodel.metainfo.basesections"),
    "NXsample_component": ("Component", "nomad.datamodel.metainfo.basesections"),
    "NXfabrication": ("Instrument", "nomad.datamodel.metainfo.basesections"),
    "NXdata": ("ActivityResult", "nomad.datamodel.metainfo.basesections"),
}

_DEFAULT_BASE: tuple[str, str] = (
    "BaseSection",
    "nomad.datamodel.metainfo.basesections",
)


def get_base_section(nx_name: str) -> tuple[str, str]:
    """Return (class_name, import_module) for the NOMAD base section that
    a given NXDL top-level class should inherit from.

    Falls back to (BaseSection, nomad.datamodel.metainfo.basesections) for
    all classes not explicitly listed.
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
