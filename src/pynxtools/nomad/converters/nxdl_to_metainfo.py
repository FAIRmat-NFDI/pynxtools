# SPDX-FileCopyrightText: The NOMAD Authors
#
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
# Full license text: LICENSES/Apache-2.0.txt. See docs/learn/pynxtools/licensing.md
# for why this package mixes Apache-2.0 and LGPL-3.0-or-later licensed files.
"""
Generator: NXDL → Python NOMAD metainfo classes via NexusNode.

All NXDL parsing goes through the NexusNode API from
pynxtools.nexus.nexus_tree. NXTreeField already resolves dtype,
units, shape, enumerations, and optionality through the inheritance chain.

generate_tree_from(nx_name) in nexus_tree.py is the single entry point.
It returns a NexusDefinition root with NexusGroup/NXTreeField/NXTreeAttribute
children. No raw XML parsing happens inside this module.

Entry points
------------
write_base_class(nx_name)       : write one base class .py file
generate_all_base_classes()     : write all base class .py files
"""

from __future__ import annotations

import ast
import re
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

import jinja2
from toposort import toposort_flatten

from pynxtools.dataconverter.helpers import get_nxdl_root_and_path
from pynxtools.nexus.nexus_tree import NexusAttribute as NXTreeAttribute
from pynxtools.nexus.nexus_tree import NexusDefinition as NXTreeDefinition
from pynxtools.nexus.nexus_tree import NexusField as NXTreeField
from pynxtools.nexus.nexus_tree import NexusGroup as NXTreeGroup
from pynxtools.nexus.nexus_tree import NexusLink as NXTreeLink
from pynxtools.nexus.nexus_tree import generate_tree_from
from pynxtools.nexus.utils import get_nexus_definitions_path, strip_nx_prefix
from pynxtools.nomad.converters._mapping import (
    _DEFAULT_BASE,
    BASESECTIONS_MAP,
    field_conflicts_with_group,
    nx_type_to_source,
    nxdl_to_class_name,
    nxdl_to_quantity_name,
    nxdl_to_subsection_name,
)
from pynxtools.units import NXUnitSet

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_DEFAULT_OUTPUT_DIR = Path(__file__).parents[1] / "metainfo"
_DEFAULT_BASE_OUTPUT_DIR = _DEFAULT_OUTPUT_DIR / "base_classes"
_DEFAULT_APPLICATIONS_OUTPUT_DIR = _DEFAULT_OUTPUT_DIR / "applications"

# Python package root for generated FQN strings (e.g. in SubSection section_def=).
# When the schema moves to nomad-measurements, change this constant and regenerate.
_METAINFO_PACKAGE_ROOT = "pynxtools.nomad.metainfo"

# Indentation of description= string continuations in generated files.
# Must match the Quantity/SubSection argument indent in nexus.py.j2.
_DESCRIPTION_INDENT = 12

_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(_TEMPLATE_DIR)),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=jinja2.StrictUndefined,
)


# ---------------------------------------------------------------------------
# Data classes for template context
# ---------------------------------------------------------------------------


@dataclass
class QuantityContext:
    # Values that require a transformation and cannot be read directly from the node.
    python_name: str  # nxdl_to_quantity_name(node.name), may have "__" suffix
    python_type: str  # "MEnum([...])" or nx_type_to_source(node.dtype)
    dimensionality: str | None  # NXUnitSet.get_dimensionality(node.unit)
    default_unit: str | None  # NXUnitSet.get_default_unit(node.unit)
    flexible_unit: bool  # True when unit category is NX_ANY
    shape: list[int | str] | None  # _shape_from_node(node): tuple → list with "*"
    parent_field: str | None  # parent field name (set for attribute-of-field)
    description: str | None  # stripped <doc> text from the primary NXDL element
    # Field-only NXDL attributes (None for attribute nodes).
    unit: str | None  # NX unit category, e.g. "NX_ENERGY" — NXTreeField only
    interpretation: str | None  # NXTreeField only
    long_name: str | None  # NXTreeField only
    # Scalar-only enum items (None when any item is a list; used for MEnum and annotation).
    # NXDL encodes list-valued enum items as Python list literals, e.g. ['kinetic_energy'].
    scalar_items: list[str] | None
    # The originating node — NXTreeField for fields, NXTreeAttribute for attributes.
    node: NXTreeField | NXTreeAttribute
    # ELN component name (e.g. "StringEditQuantity") — None for arrays/Bytes/variadic.
    eln_component: str | None
    # Default value for the ELN annotation; set for single-value MEnum only.
    eln_default: str | None


@dataclass
class SubSectionContext:
    # Values that require a transformation and cannot be read directly from the node.
    python_name: str  # nxdl_to_subsection_name(…)
    section_fqn: str  # fully-qualified string proxy for SubSection.section_def
    repeats: bool  # computed from occurrence_limits + variadic + name_type
    variable: bool  # True when name_type="any"/"partial" (user-named at runtime)
    nx_name_literal: str  # '"name"' for fixed-name groups, 'None' for variadic
    description: str | None  # <doc> text from the group element
    # When True the target class carries a_nexus_group on its own m_def;
    # the SubSection is clean. When False a_nexus_group goes on the SubSection.
    is_named_concept: bool
    # The originating NexusGroup node — all other info is read via node.*
    node: NXTreeGroup


@dataclass
class LinkContext:
    """A NXDL <link> element — emitted as a Quantity with NeXusLink.

    Type, dimensionality, unit, and shape come from the field or attribute the
    link's ``target`` path resolves to (via ``_resolve_link_quantity``).
    For example, a link to an NX_FLOAT field with unit category NX_TIME_OF_FLIGHT
    becomes ``Quantity(type=np.float64, unit="s")``.

    If the target cannot be resolved, ``target_quantity`` is None and the
    Quantity falls back to ``type=str``.
    """

    python_name: str  # nxdl_to_quantity_name(node.name)
    description: str | None  # <doc> text from the link element
    node: NXTreeLink
    # QuantityContext built from the resolved target field/attribute, or None
    # if node.target could not be resolved within the application's tree.
    target_quantity: QuantityContext | None = None


@dataclass
class ChoiceSubSectionContext:
    """One alternative in a NXDL <choice> block — emitted as a SubSection."""

    python_name: str  # "{choice_name}_{class_suffix}", e.g. "pixel_shape_off_geometry"
    group_name: str  # the choice's @name, shared across all alternatives
    section_fqn: str  # fully-qualified string proxy for SubSection.section_def
    description: str | None  # <doc> from the group element inside the choice
    node: NXTreeGroup  # the NexusGroup node for this alternative


@dataclass
class NamedConceptContext:
    """Section class generated for a group occurrence with its own own quantities or children.

    Created when the NXDL group element specifies fields or attributes that
    differ from the parent class (changed optionality, extra fields, different
    type/units/enumeration/description), or when it has sub-group children whose
    ``nx_class`` is not present in the base NXDL class.
    """

    class_name: str  # "EntryThumbnail"
    base_class_name: str  # "Note" — the generic class for the group's nx_type
    base_module: str  # "note" — file stem used to build import path
    nx_name_literal: str  # 'None' or '"thumbnail"'
    variable: bool  # Section(variable=True) when name_type="any"/"partial"
    docstring: str | None
    quantities: list[QuantityContext]  # own fields defined inside the group XML
    links: list[LinkContext]  # own <link> elements defined inside the group XML
    subsections: list[SubSectionContext]  # app-specific child groups not in base class
    node: NXTreeGroup


# ---------------------------------------------------------------------------
# Dimensionality helper (unit category → NOMAD dimensionality string)
# Not available on NexusNode — unit categories are NeXus concepts that
# map to pint dimensionalities only through NXUnitSet.
# ---------------------------------------------------------------------------


def _get_dimensionality(nx_units: str | None) -> str | None:
    if not nx_units:
        return None
    if nx_units == "NX_TRANSFORMATION":
        nx_units = "NX_ANY"
    try:
        dim = NXUnitSet.get_dimensionality(nx_units)
        return str(dim) if dim is not None else None
    except Exception:
        return None


def _get_default_unit(nx_units: str | None) -> str | None:
    """Return the default storage unit for a NXDL unit category, if any."""
    if not nx_units:
        return None
    if nx_units == "NX_TRANSFORMATION":
        nx_units = "NX_ANY"
    return NXUnitSet.get_default_unit(nx_units)


# ---------------------------------------------------------------------------
# Shape conversion: NXTreeField/NXTreeAttribute.shape tuple → template list
#
# None entries in the shape tuple are unbounded or symbolically-named dimensions
# (e.g. "nP", "nz"). NOMAD does not interpret NeXus symbol names, so every
# None entry becomes the wildcard "*". Symbol names are preserved in
# NeXusDefinition.symbols on the top-level class m_def.
# ---------------------------------------------------------------------------


def _shape_from_node(node: NXTreeField | NXTreeAttribute) -> list[int | str] | None:
    if node.shape is None:
        return None
    return [d if d is not None else "*" for d in node.shape]


# ---------------------------------------------------------------------------
# <link target="..."> resolution
#
# Link targets are absolute NXDL concept paths, e.g.
# "/NXentry/NXinstrument/NXdetector/time_of_flight": each segment up to the
# last names a group's nx_class; the last segment names a field or attribute
# on that group. Resolution walks root_node.children (the application's
# NXentry-unwrapped tree) by nx_class, then looks up the final field/attribute
# by name.
# ---------------------------------------------------------------------------


def _resolve_link_target_node(
    root_node: NXTreeDefinition, target: str
) -> NXTreeField | NXTreeAttribute | None:
    """Resolve a <link target="/NXentry/.../field_name"> path to its field/attribute node.

    Returns None if any path segment cannot be matched — links to NX classes
    outside this application's tree (or to concepts not yet represented in
    the tree) simply fall back to type=str in the generated Quantity.
    """
    segments = [s for s in target.split("/") if s]
    if not segments:
        return None

    children = root_node.children
    node: NXTreeField | NXTreeAttribute | NXTreeGroup | None = None
    for i, segment in enumerate(segments):
        is_last = i == len(segments) - 1
        if is_last:
            match = next(
                (
                    c
                    for c in children
                    if c.nx_type in ("field", "attribute") and c.name == segment
                ),
                None,
            )
        else:
            candidates = [
                c for c in children if c.nx_type == "group" and c.nx_class == segment
            ]
            # Prefer the specifically-named group over a variadic placeholder
            # (e.g. "instrument" over "INSTRUMENT", both NXinstrument).
            match = next(
                (c for c in candidates if c.name_type == "specified"), None
            ) or (candidates[0] if candidates else None)
        if match is None:
            return None
        node = match
        if not is_last:
            children = node.children

    return node if isinstance(node, (NXTreeField, NXTreeAttribute)) else None


def _resolve_link_quantity(
    root_node: NXTreeDefinition, link_node: NXTreeLink, python_name: str
) -> QuantityContext | None:
    """Build a QuantityContext from a <link>'s target field/attribute, if resolvable."""
    target_node = _resolve_link_target_node(root_node, link_node.target)
    if target_node is None:
        return None
    return _build_quantity_from_node(target_node, python_name_override=python_name)


# ---------------------------------------------------------------------------
# Cross-category FQN helpers
# ---------------------------------------------------------------------------


_NXDL_CATEGORY_CACHE: dict[str, str] = {}


def _nxdl_category(nx_class: str) -> str:
    """Return the metainfo output sub-package ('base_classes' or 'applications')
    for a given NXDL class name, routing by NXDL category attribute."""
    if nx_class in _NXDL_CATEGORY_CACHE:
        return _NXDL_CATEGORY_CACHE[nx_class]

    try:
        root = generate_tree_from(nx_class)
        result = "applications" if root.category == "application" else "base_classes"
    except Exception:
        result = "base_classes"

    _NXDL_CATEGORY_CACHE[nx_class] = result
    return result


def _target_module_exists(nx_class: str) -> bool:
    """Return True if the generated .py file for nx_class already exists on disk."""
    category = _nxdl_category(nx_class)
    module = _class_module_name(nx_class)
    if category == "applications":
        target = _DEFAULT_APPLICATIONS_OUTPUT_DIR / f"{module}.py"
    else:
        target = _DEFAULT_BASE_OUTPUT_DIR / f"{module}.py"
    return target.exists()


def _class_module_name(nx_class: str) -> str:
    stem = nx_class[2:] if nx_class.startswith("NX") else nx_class
    return stem.lower()


def _section_fqn(nx_class: str) -> str:
    """Return the fully-qualified string proxy for a generated section."""
    module = _class_module_name(nx_class)
    class_name = nxdl_to_class_name(nx_class)
    category = _nxdl_category(nx_class)
    return f"{_METAINFO_PACKAGE_ROOT}.{category}.{module}.{class_name}"


# ---------------------------------------------------------------------------
# Description helpers
# ---------------------------------------------------------------------------


_DOC_WIDTH = 75  # target line width for wrapped doc text


def _plain_description(node) -> str | None:
    """Extract <doc> text as plain wrapped text (no comment prefix).

    Used for class and concept-class docstrings. Paragraphs are separated
    by blank lines; each paragraph is word-wrapped to _DOC_WIDTH characters.
    """
    docs = node.get_docstring(depth=1)
    raw = (next(iter(docs.values()), None) or "").strip()
    if not raw:
        return None
    cleaned = textwrap.dedent(raw).strip()
    wrapped_blocks: list[str] = []
    for paragraph in cleaned.split("\n\n"):
        paragraph = " ".join(paragraph.split())
        wrapped = textwrap.fill(
            paragraph,
            width=_DOC_WIDTH,
            break_long_words=False,
            break_on_hyphens=False,
        )
        wrapped_blocks.append(wrapped)
    return "\n\n".join(wrapped_blocks)


def _description_string(node) -> str | None:
    """Format <doc> text as pre-rendered Python string literal(s) for ``description=``.

    Single-line: returns ``'"text"'``.
    Multi-line: returns implicit string concatenation with each continuation
    line indented by 12 spaces (matching the Quantity arg indent in the template).
    """
    docs = node.get_docstring(depth=1)
    raw = (next(iter(docs.values()), None) or "").strip()
    if not raw:
        return None
    collapsed = " ".join(textwrap.dedent(raw).split())
    escaped = collapsed.replace("\\", "\\\\").replace('"', '\\"')
    wrapped = textwrap.fill(
        escaped,
        width=79 - _DESCRIPTION_INDENT,
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines = wrapped.split("\n")
    if len(lines) == 1:
        return f'"{escaped}"'
    pad = " " * _DESCRIPTION_INDENT
    parts = [f'"{line} "' for line in lines[:-1]] + [f'"{lines[-1]}"']
    return ("\n" + pad).join(parts)


# ---------------------------------------------------------------------------
# Named concept class naming helper
# ---------------------------------------------------------------------------


def _group_has_explicit_name(name: str, nx_class: str) -> bool:
    """Return True if a NXDL ``<group>`` had an explicit ``name=`` attribute.

    Only used to decide the ``a_nexus_group(name=...)`` annotation,
    not for Python attribute naming (which always uses ``node.name``, see
    ``_group_python_name``).

    """
    return name != strip_nx_prefix(nx_class)


def _concept_class_name(parent_class_name: str, node: NXTreeGroup) -> str:
    """Return the Python class name for a named concept class.

    The name is ``{ParentClassName}{Suffix}``.

    ``node.name`` is always populated by ``NexusNode`` — either the NXDL's
    explicit ``name=`` attribute, or (when absent) the NX class stem in
    uppercase (e.g. ``"USER"`` for ``NXuser``). Both variadic and fixed-name
    groups use the same CamelCase-from-name logic. An explicitly-named variadic
    group like ``name="BIAS_SWEEP"`` on a ``nameType="any"`` group becomes
    suffix ``BiasSweep``.

    For partial groups the NXDL name follows the convention
    ``lowercasePrefixUPPERCASE_MARKER``. The full suffix keeps the uppercase
    marker intact. For example, inside ``NXfit`` (parent class ``Fit``), the
    partial group ``peakPEAK`` produces suffix ``PeakPEAK`` and concept class
    ``FitPeakPEAK``.
    """
    return _concept_class_name_from_parts(
        parent_class_name, node.name, node.name_type or "specified"
    )


def _concept_class_name_from_parts(
    parent_class_name: str, name: str, name_type: str
) -> str:
    """Compute concept class name from explicit name/name_type strings.

    A leading redundant parent prefix is stripped from the suffix to avoid
    doubling. For example, ``xps_coordinate_system`` inside ``Xps`` produces
    suffix ``XpsCoordinateSystem``, stripped to ``CoordinateSystem``, giving
    final name ``XpsCoordinateSystem``.

    The circular-inheritance check in ``build_context`` re-adds the prefix
    when the result would equal the base class name, e.g. ``ApmApmMeasurement``
    is intentional and not a bug.
    """
    if name_type == "partial":
        # Partial names are `lowercasePrefix` + `UPPERCASE_MARKER` (e.g.
        # "peakPEAK", "voltage_sensorTAG") — CamelCase the lowercase prefix
        # like the "specified" branch below (so "voltage_sensor" becomes
        # "VoltageSensor", not "Voltage_sensor"), then keep the uppercase
        # marker as-is: "voltage_sensorTAG" -> "VoltageSensorTAG".
        match = re.search(r"[A-Z]", name) if name else None
        split = match.start() if match else len(name or "")
        prefix, marker = name[:split], name[split:]
        prefix_camel = "".join(
            p.capitalize() for p in prefix.lower().replace("-", "_").split("_") if p
        )
        child_suffix = prefix_camel + marker
    else:
        child_suffix = "".join(
            p.capitalize() for p in name.lower().replace("-", "_").split("_") if p
        )
    # Strip redundant parent prefix: "Xps" + "XpsCoordinateSystem" → "XpsCoordinateSystem"
    p = parent_class_name
    if (
        child_suffix.startswith(p)
        and len(child_suffix) > len(p)
        and child_suffix[len(p)].isupper()
    ):
        child_suffix = child_suffix[len(p) :]
    return parent_class_name + child_suffix


# ---------------------------------------------------------------------------
# Build quantity context from a NXTreeField node
# ---------------------------------------------------------------------------


def _eln_component_for(
    python_type: str,
    shape: list | None,
    name_type: str | None,
    scalar_items: list[str] | None,
    field_name: str = "",
) -> tuple[str | None, str | None]:
    """Return (eln_component, eln_default) for a generated Quantity.

    Returns (None, None) for arrays, variadic quantities, Bytes, and link targets.
    Single-value MEnum fields get their sole enum string as ``eln_default``.
    String fields whose name contains "description" get RichTextEditQuantity.
    """
    if shape:  # non-empty list → array; None or [] → scalar
        return None, None
    if (name_type or "specified") in ("any", "partial"):
        return None, None
    if python_type == "Bytes":
        return None, None
    if python_type == "Datetime":
        return "DateTimeEditQuantity", None
    if python_type == "bool":
        return "BoolEditQuantity", None
    if python_type.startswith("MEnum("):
        default = scalar_items[0] if scalar_items and len(scalar_items) == 1 else None
        return "EnumEditQuantity", default
    if python_type == "str":
        if "description" in field_name:
            return "RichTextEditQuantity", None
        return "StringEditQuantity", None
    # Numeric: np.float64, np.int64, np.complex128, int, float
    return "NumberEditQuantity", None


def _build_quantity_from_node(
    node: NXTreeField | NXTreeAttribute,
    parent_field: str | None = None,
    python_name_override: str | None = None,
) -> QuantityContext:
    """Build a QuantityContext from a NXTreeField or NXTreeAttribute node.

    Only the few values that require a non-trivial transformation are stored
    on QuantityContext itself. Everything else is accessed directly through
    the node. Field-only attributes (unit, interpretation, long_name) are
    extracted here and stored as None for NXTreeAttribute nodes.
    """
    if isinstance(node, NXTreeField):
        # NX_TRANSFORMATION means any length/angle/dimensionless → map to NX_ANY.
        raw_unit = node.unit if node.unit != "NX_TRANSFORMATION" else "NX_ANY"
        unit = raw_unit
        dimensionality = _get_dimensionality(raw_unit)
        default_unit = _get_default_unit(raw_unit)
        flexible_unit = node.unit == "NX_ANY"
        shape = _shape_from_node(node)
        interpretation = node.interpretation
        long_name = node.long_name
    else:
        unit = None
        dimensionality = None
        default_unit = None
        flexible_unit = False
        shape = _shape_from_node(node)
        interpretation = None
        long_name = None

    python_name = python_name_override or nxdl_to_quantity_name(
        node.name, has_shape=bool(shape)
    )

    # Enum items whose values are themselves lists (e.g. `['kinetic_energy']`) cannot
    # be used in MEnum (unhashable) or in NeXusQuantity.enumeration (list[str]).
    scalar_items: list[str] | None = None
    if node.items and not any(isinstance(item, list) for item in node.items):
        scalar_items = node.items

    if scalar_items and not node.open_enum:
        python_type = f"MEnum({scalar_items!r})"
    else:
        python_type = nx_type_to_source(node.dtype)

    eln_component, eln_default = _eln_component_for(
        python_type, shape, node.name_type, scalar_items, field_name=node.name or ""
    )

    return QuantityContext(
        python_name=python_name,
        python_type=python_type,
        dimensionality=dimensionality,
        default_unit=default_unit,
        flexible_unit=flexible_unit,
        shape=shape,
        parent_field=parent_field,
        description=_description_string(node),
        unit=unit,
        interpretation=interpretation,
        long_name=long_name,
        scalar_items=scalar_items,
        node=node,
        eln_component=eln_component,
        eln_default=eln_default,
    )


# ---------------------------------------------------------------------------
# Build subsection context from a NXTreeGroup node
# ---------------------------------------------------------------------------


def _build_subsection_from_node(
    node: NXTreeGroup,
    section_fqn: str,
    is_named_concept: bool = False,
) -> SubSectionContext:
    """Build a SubSectionContext from a NexusGroup node.

    ``section_fqn`` is resolved lazily by NOMAD at ``__init_metainfo__()``
    time. Where ``a_nexus_group`` is placed depends on ``is_named_concept``:

    - ``False``: SubSection references a generic class (e.g. ``"...user.User"``);
      ``a_nexus_group`` is on the SubSection.
    - ``True``: SubSection references a named concept class in this same file;
      ``a_nexus_group`` is on the concept's ``m_def``, SubSection is clean.
    """
    nx_name_type = node.name_type or "specified"
    repeats = _repeats_from_node(node)
    variable = nx_name_type in ("any", "partial")

    if nx_name_type == "any":
        # NXDL writes variadic group names in uppercase (e.g. "BIAS_SWEEP",
        # "USER"). Lowercase for a pythonic attribute name.
        python_name = nxdl_to_subsection_name(node.name.lower())
    elif nx_name_type == "partial":
        # Keep the full NXDL name (e.g. "peakPEAK" from NXfit) so the
        # partial-group marker is visible in code and matches the concept
        # class name (e.g. FitPeakPEAK).
        python_name = nxdl_to_subsection_name(node.name)
    else:
        python_name = nxdl_to_subsection_name(node.name)

    # Record what NXDL actually declares: None for anonymous groups (no
    # name= attribute), the literal name otherwise. An "any" group with an
    # explicit name= (e.g. "BIAS_SWEEP") is not anonymous and gets its name.
    # This is independent of python_name above, which always
    # uses node.name regardless
    if nx_name_type == "any" and not _group_has_explicit_name(node.name, node.nx_class):
        nx_name_literal = "None"
    else:
        nx_name_literal = f'"{node.name}"'

    return SubSectionContext(
        python_name=python_name,
        section_fqn=section_fqn,
        repeats=repeats,
        variable=variable,
        nx_name_literal=nx_name_literal,
        description=_description_string(node),
        is_named_concept=is_named_concept,
        node=node,
    )


_base_class_qty_cache: dict[str, dict[str, NXTreeField | NXTreeAttribute]] = {}


_base_group_nx_classes_cache: dict[str, frozenset[str]] = {}


def _quantity_differs_from_base(
    node: NXTreeField | NXTreeAttribute,
    base_lookup: dict[str, NXTreeField | NXTreeAttribute],
) -> bool:
    """Return True if ``node`` is new, has a different dtype/items/unit, or a
    different requiredness than the generic base class — the same checks
    ``_qty_differs_from_base`` makes, minus doc (that alone doesn't warrant a
    class of its own; see ``_build_named_concept``'s ``slot_overridden``).

    Requiredness is included deliberately, not excluded: per
    ``_requiredness_or_doc_differs``, tightening from optional/recommended to
    required is itself a meaningful constraint, and it can be the *only*
    thing an ancestor changes — e.g. NXxrot's own ``polar_angle`` /
    ``beam_center_x`` / ``beam_center_y`` on ``detector`` match generic
    NXdetector's dtype/unit exactly, but NXxrot (an application definition)
    declares them without an explicit ``optional`` attribute, which defaults
    to required, unlike generic NXdetector's own "optional". Dropping
    requiredness here made ``NXxlaueplate`` (which extends NXxrot) skip
    straight past ``XrotInstrumentDetector`` to ``XbaseInstrumentDetector``,
    silently losing the override.
    """
    base_node = base_lookup.get(node.name)
    if base_node is None:
        return True
    if node.dtype != base_node.dtype or node.items != base_node.items:
        return True
    if (
        isinstance(node, NXTreeField)
        and isinstance(base_node, NXTreeField)
        and node.unit != base_node.unit
    ):
        return True
    return node.optionality != base_node.optionality


def _optionality_from_attrib(attrib: dict) -> str | None:
    """Compute NXDL optionality from a raw XML element's attributes directly,
    mirroring ``NexusNode._set_optionality``'s precedence, or ``None`` if none
    of ``recommended``/``required``/``optional``/``minOccurs`` is present.

    Needed because that method only ever computes optionality for a node's
    own most-derived declaration (``inheritance[0]``); this lets us ask the
    same question about an arbitrary ancestor level's raw declaration
    instead, without constructing a full node for it.

    ``None`` (rather than falling back to NeXus's own "required" default) is
    deliberate: that default is category-dependent — base classes default to
    optional, application definitions to required — so an appdef that simply
    reuses a base class's group (e.g. NXsensor_scan's own bare ``<group
    type="NXdata">``, no attributes at all) looks "required" by convention
    alone, even with zero intent to narrow it from the generic "optional".
    Treating that as a real override would report an ancestor as generating
    its own concept when ``_build_named_concept`` never actually emits one,
    producing a class reference that does not exist (confirmed via
    NXsensor_scan's ``data``, which was wrongly triggering exactly this).
    """
    if attrib.get("recommended"):
        return "recommended"
    min_occurs = attrib.get("minOccurs")
    if attrib.get("required") or (min_occurs is not None and int(min_occurs) > 0):
        return "required"
    if attrib.get("optional") or min_occurs == "0":
        return "optional"
    return None


def _parent_generates_concept_at(child: NXTreeGroup, idx: int) -> bool:
    """Return whether the ancestor at ``idx`` generates its own concept.

    An ancestor generates a concept if, at that specific level, it: declares
    a field/attribute that differs from the generic base's (dtype, items,
    unit — see ``_quantity_differs_from_base``); declares a child group not
    already part of the base class for ``child.nx_class``; gives ``child``
    itself different occurrence limits or optionality than the generic
    enclosing class declares for this same slot; or nests a group (already a
    generic type) that itself adds any of the above one or more levels down.

    Presence alone isn't enough for any of these — an ancestor can redeclare
    a field, or write an attribute like ``optional="true"``, purely for
    documentation, with the value identical to the generic default (e.g.
    NXxbase's ``source`` redeclares ``type``/``name``/``probe`` unchanged;
    NXoptical_spectroscopy's ``waveplate`` writes ``optional="true"`` when
    that's already the generic default). A presence-only check would claim
    an ancestor generates its own concept when ``_build_named_concept`` —
    using this same precise comparison — never actually emits one, producing
    a class reference that does not exist. Doc is excluded even so: see
    ``_build_named_concept``'s ``slot_overridden`` for why.

    The recursion into nested groups matters because ``_parent_app_concept_override``
    only descends into a group's own children (e.g. ``detector`` inside
    ``instrument``) once the enclosing group's own override succeeds — so
    ``instrument`` itself must be able to see that ``detector``, though
    itself a generic type, adds real fields several levels down (e.g.
    NXxbase's ``instrument`` only has directly generic children, but its own
    ``detector`` gives it fields no generic ``NXdetector`` has).
    """
    if idx >= len(child.inheritance):
        return False
    elem = child.inheritance[idx]
    parent = child.parent
    if isinstance(parent, NXTreeGroup):
        base_sibling = _base_class_group_nodes(parent.nx_class).get(
            _group_python_name(child)
        )
        own_optionality = _optionality_from_attrib(elem.attrib)
        if (
            base_sibling is not None
            and own_optionality is not None
            and own_optionality != base_sibling.optionality
        ):
            return True
    return _declares_content_at(child, elem.base)


def _declares_content_at(
    node: NXTreeGroup, ancestor_file: str, _depth: int = 0
) -> bool:
    """Return True if ``node``'s declaration at ``ancestor_file`` differs from
    the generic definition of ``node.nx_class``, checking own fields/
    attributes and nested groups' occurrence/optionality precisely, and
    recursing into nested groups for content further down. Depth-capped
    against pathological self-referential NXDL structures (e.g. NXnote
    containing NXnote); real NXDL nesting never comes close to this depth.

    Looks at every child of ``node``, not only those whose ``nxdl_base``
    exactly equals ``ancestor_file``: a more-derived application can
    redeclare a child purely to nest further content of its own (e.g.
    NXsts's ``bias_spectroscopy_environment`` redeclares NXspm's own
    ``NXspm_bias_spectroscopy`` group just to add a ``z_controller``
    underneath it), which reassigns ``nxdl_base`` to that more-derived level
    even though ``ancestor_file`` still genuinely introduces the same child —
    it still appears in the child's own ``inheritance``. Filtering on
    ``nxdl_base`` alone would make that content invisible when checking
    whether ``ancestor_file`` itself generates a concept here.
    """
    if _depth > 10:
        return False
    base_group_nx = _base_class_group_nx_classes(node.nx_class)
    base_lookup = _base_class_quantities(node.nx_class)
    base_group_nodes = _base_class_group_nodes(node.nx_class)
    for c in node.children:
        own_elem = next(
            (elem for elem in c.inheritance if elem.base == ancestor_file), None
        )
        if own_elem is None:
            continue
        if c.nx_type == "link":
            # A <link> at this level is always new content: matching
            # _build_named_concept's own_links, which adds every link
            # unconditionally (no base_lookup comparison — generic base
            # classes essentially never declare links to sibling groups,
            # since a link's whole purpose is app-specific entry wiring).
            # Missing this made e.g. NXxbase's own "data" (a bare link to
            # the detector's data field, no fields/attributes/nested groups
            # of its own) invisible, so NXxeuler (which extends NXxbase)
            # fell through XbaseData straight to generic Data.
            #
            # Still can't see a link shadowed by a same-named field at a
            # more-derived level (NXxrd vs. NXmonopd) — known, not fixed;
            # NXxrd is expected to change once nomad-measurements lands.
            return True
        if c.nx_type == "choice":
            # A <choice> block is always new content, for the same reason as
            # <link> above: build_context's top-level loop (the "choice"
            # branch) adds one SubSection per alternative unconditionally,
            # with no base_lookup comparison. No current application
            # definition declares its own <choice> (the one in this corpus,
            # NXdetector's, lives on a base class only), so this can't fire
            # today — kept for when one does, rather than waiting for the
            # same class of bug to resurface a fourth time.
            return True
        if isinstance(c, (NXTreeField, NXTreeAttribute)):
            if _quantity_differs_from_base(c, base_lookup):
                return True
        elif isinstance(c, NXTreeGroup):
            if c.nx_class not in base_group_nx:
                return True
            base_sibling = base_group_nodes.get(_group_python_name(c))
            if base_sibling is None:
                # Same nx_class as some generic child, but no generic sibling
                # under this exact name (e.g. NXxrd's "raw_data" vs generic
                # NXdetector's own unnamed NXdata child) — a genuinely new,
                # separately-named SubSection, matching how
                # ``_build_named_concept``'s ``is_collision`` treats the same
                # situation.
                return True
            if _repeats_from_node(c) != _repeats_from_node(base_sibling):
                return True
            own_optionality = _optionality_from_attrib(own_elem.attrib)
            if (
                own_optionality is not None
                and own_optionality != base_sibling.optionality
            ):
                return True
            if _declares_content_at(c, ancestor_file, _depth + 1):
                return True
    return False


def _parent_app_concept_override(
    child: NXTreeGroup,
    parent_apps: list[tuple[str, str, str]] | None,
) -> tuple[tuple[str, str] | None, str | None, list[tuple[str, str, str]] | None]:
    """Determine whether a group's concept should inherit from a parent application.

    When multiple applications in an inheritance chain declare the same group,
    the generated concept should inherit from the nearest ancestor application
    that actually generates a concept for that group, rather than from the
    generic base class. This preserves concepts introduced by parent
    applications (e.g. additional child groups).

    Ancestors are checked in order from nearest to furthest. An ancestor that
    does not declare the group, or declares it without generating a concept,
    is skipped so that a further ancestor can still provide the base class.

    Returns:
        A tuple ``(base_class_override, parent_concept_file,
        child_parent_apps)``. ``child_parent_apps`` updates every remaining
        candidate's naming base to what *it* calls this enclosing concept
        (not just the matched one) so nested groups inherit correctly even
        when a fallback candidate ends up providing their base a level
        further down — e.g. for ``source`` nested in ``instrument``, where
        ``instrument`` itself resolved to ``XrotInstrument`` but ``source``
        isn't declared by Xrot at all: the fallback candidate for Xbase must
        already be named "XbaseInstrument", not bare "Xbase", or the nested
        concept ends up misnamed "XbaseSource" instead of
        "XbaseInstrumentSource".
    """
    if not parent_apps:
        return None, None, None
    child_files = [elem.base for elem in child.inheritance]

    def _renamed_for_this_level(
        app_file: str, app_module: str, naming_base: str
    ) -> tuple[str, str, str]:
        try:
            idx = child_files.index(app_file)
        except ValueError:
            return app_file, app_module, naming_base
        naming = child.group_naming_at(idx)
        if naming is None:
            return app_file, app_module, naming_base
        name, name_type, _ = naming
        return (
            app_file,
            app_module,
            _concept_class_name_from_parts(naming_base, name, name_type),
        )

    for i, (parent_app_file, parent_app_module, parent_naming_base) in enumerate(
        parent_apps
    ):
        try:
            parent_idx = child_files.index(parent_app_file)
        except ValueError:
            continue  # this ancestor doesn't touch the group at all — try further back
        if not _parent_generates_concept_at(child, parent_idx):
            continue  # touches it but adds nothing new here — try further back
        parent_naming = child.group_naming_at(parent_idx)
        if parent_naming is None:
            continue
        p_name, p_name_type, _p_nx_class = parent_naming
        parent_concept_name = _concept_class_name_from_parts(
            parent_naming_base, p_name, p_name_type
        )
        child_parent_apps = [
            (parent_app_file, parent_app_module, parent_concept_name)
        ] + [_renamed_for_this_level(*candidate) for candidate in parent_apps[i + 1 :]]
        return (
            (parent_concept_name, parent_app_module),
            parent_app_file,
            child_parent_apps,
        )
    return None, None, None


def _base_class_group_nx_classes(nx_class: str) -> frozenset[str]:
    """Return the set of nx_class strings of direct group children in the base NXDL class.

    Used to detect application-specific sub-groups: if a child group's nx_class
    is NOT in this set, it's an application-specific addition that warrants a
    named concept on the parent group.
    """
    if nx_class in _base_group_nx_classes_cache:
        return _base_group_nx_classes_cache[nx_class]
    try:
        base_root = generate_tree_from(nx_class)
    except Exception:
        _base_group_nx_classes_cache[nx_class] = frozenset()
        return frozenset()
    nx_classes: set[str] = set()
    for child in base_root.children:
        if isinstance(child, NXTreeGroup) and child.nx_class:
            nx_classes.add(child.nx_class)
    result = frozenset(nx_classes)
    _base_group_nx_classes_cache[nx_class] = result
    return result


def _group_python_name(node: NXTreeGroup) -> str:
    """Return the Python attribute name a SubSection for ``node`` would get.

    Mirrors the naming rule in ``_build_subsection_from_node``: variadic
    (``name_type="any"``) groups are lowercased; other groups use
    ``node.name`` as-is.

    For example, a variadic ``NXdetector`` with no explicit name becomes
    ``"detector"``; one explicitly named ``"BIAS_SWEEP"`` becomes
    ``"bias_sweep"``; a specified group named ``"analyser"`` stays
    ``"analyser"``.
    """
    nx_name_type = node.name_type or "specified"
    if nx_name_type == "any":
        return nxdl_to_subsection_name(node.name.lower())
    return nxdl_to_subsection_name(node.name)


def _repeats_from_node(node: NXTreeGroup) -> bool:
    """Return whether a SubSection for ``node`` should be repeatable.

    Mirrors the rule in ``_build_subsection_from_node``: variadic (nameType
    any/partial) groups repeat unless ``maxOccurs`` is explicitly 1;
    specified groups don't repeat unless ``maxOccurs`` is explicitly > 1.
    """
    max_occurs = node.occurrence_limits[1]  # None means unbounded
    if node.variadic:
        return max_occurs is None or max_occurs > 1
    return max_occurs is not None and max_occurs > 1


_base_group_nodes_cache: dict[str, dict[str, NXTreeGroup]] = {}


def _base_class_group_nodes(nx_class: str) -> dict[str, NXTreeGroup]:
    """Return a python_name → node lookup of direct group children in the generic class.

    Used to tell a new child group apart from one that merely re-specifies a
    slot the generic class already exposes under the same name, and — via
    the node — to compare occurrence limits between the two.

    For example, ``analyser`` inside NXarpes's ``instrument`` is new — the
    generic class has no SubSection under that name. A ``source`` group named
    "source" is not new — the generic class already has a variadic
    ``source`` SubSection.
    """
    if nx_class in _base_group_nodes_cache:
        return _base_group_nodes_cache[nx_class]
    try:
        base_root = generate_tree_from(nx_class)
    except Exception:
        _base_group_nodes_cache[nx_class] = {}
        return {}
    lookup: dict[str, NXTreeGroup] = {}
    for child in base_root.children:
        if isinstance(child, NXTreeGroup) and child.nx_class:
            lookup[_group_python_name(child)] = child
    _base_group_nodes_cache[nx_class] = lookup
    return lookup


def _base_class_quantities(nx_class: str) -> dict[str, NXTreeField | NXTreeAttribute]:
    """Return a name→node lookup of direct fields/attributes in the generic class."""
    if nx_class in _base_class_qty_cache:
        return _base_class_qty_cache[nx_class]
    try:
        base_root = generate_tree_from(nx_class)
    except Exception:
        _base_class_qty_cache[nx_class] = {}
        return {}
    lookup: dict[str, NXTreeField | NXTreeAttribute] = {}
    for child in base_root.children:
        if isinstance(child, (NXTreeField, NXTreeAttribute)):
            lookup[child.name] = child
    _base_class_qty_cache[nx_class] = lookup
    return lookup


def _own_doc(node: NXTreeGroup | NXTreeField | NXTreeAttribute) -> str:
    """Return this node's own doc text (not its ancestors'), stripped."""
    return (next(iter(node.get_docstring(depth=1).values()), None) or "").strip()


def _requiredness_or_doc_differs(
    node: NXTreeGroup | NXTreeField | NXTreeAttribute,
    base_node: NXTreeGroup | NXTreeField | NXTreeAttribute,
) -> bool:
    """Return True if optionality or own doc text differs from the base node.

    Shared by fields and groups. Requiredness counts as a difference:
    tightening from "optional"/"recommended" to "required" is itself a
    meaningful constraint, and the round-trip exporter needs a concrete
    declaration to recover it. So does a more specific doc — e.g.
    NXspm_bias_spectroscopy's ``acquisition_time`` vs NXcircuit's generic one.
    """
    if node.optionality != base_node.optionality:
        return True
    return _own_doc(node) != _own_doc(base_node)


def _qty_differs_from_base(
    qty: QuantityContext, base_lookup: dict[str, NXTreeField | NXTreeAttribute]
) -> bool:
    """Return True if this quantity is new or has different properties in the base class."""
    base_node = base_lookup.get(qty.node.name)
    if base_node is None:
        return True  # quantity not in generic class — new
    if qty.node.dtype != base_node.dtype:
        return True
    if qty.node.items != base_node.items:
        return True
    if (
        isinstance(qty.node, NXTreeField)
        and isinstance(base_node, NXTreeField)
        and qty.node.unit != base_node.unit
    ):
        return True
    return _requiredness_or_doc_differs(qty.node, base_node)


def _build_named_concept(
    concept_class_name: str,
    node: NXTreeGroup,
    root_node: NXTreeDefinition,
    base_class_override: tuple[str, str] | None = None,
    parent_concept_file: str | None = None,
    module_name: str | None = None,
    category: str | None = None,
    seen_concept: set[str] | None = None,
    naming_base: str | None = None,
    parent_apps: list[tuple[str, str, str]] | None = None,
) -> tuple[NamedConceptContext, list[NamedConceptContext]]:
    """Build a NamedConceptContext for a named group occurrence.

    Reads fields and attributes defined one level inside the group element
    and packages them as Quantities of the concept class.

    Sub-groups that introduce new concepts absent from the parent class are
    processed recursively (e.g. ``analyser`` inside NXarpes's ``instrument``).
    Their concepts are returned in the second tuple element; the caller adds
    them to the file's named-concept list.

    Returns empty ``quantities`` / ``links`` / ``subsections`` if nothing differs
    from the parent class — callers skip generating a class in that case.

    ``module_name`` / ``category`` name the output file — all named concepts
    for one NXDL class share a single generated file. ``seen_concept`` is
    shared across the recursion to prevent name collisions.

    ``naming_base`` is the prefix for nested concept names. It matches
    ``concept_class_name`` in most cases. The exception: when a class was
    re-prefixed for circular inheritance (e.g. ``EmEmMeasurement``), its
    ``naming_base`` is the un-doubled form ``EmMeasurement``, so nested
    concepts do not double-prefix (``EmMeasurementInstrument``, not
    ``EmEmMeasurementInstrument``).

    **Symmetric inheritance rule.**
    The higher-level concept keeps the unqualified name.

    - Own field vs. ancestor GROUP: field renamed to ``<name>_quantity``.
    - Own GROUP vs. ancestor field: SubSection renamed to ``<name>_group``,
      local to this concept only.
    """
    _seen_concept = seen_concept if seen_concept is not None else set()
    _naming_base = naming_base if naming_base is not None else concept_class_name
    nx_name_type = node.name_type or "specified"
    variable = nx_name_type in ("any", "partial")

    # None for a fully anonymous group (no name= attribute at all — NXDL
    # gives no template name); the literal name otherwise, even for "any"
    # groups that do have an explicit template name (e.g. "BIAS_SWEEP"). For
    # partial groups this preserves the full name (e.g. "peakPEAK") so the
    # parser can extract the prefix matching rule.
    if nx_name_type == "any" and not _group_has_explicit_name(node.name, node.nx_class):
        nx_name_literal = "None"
    else:
        nx_name_literal = f'"{node.name}"'

    if base_class_override is not None:
        base_class_name, base_module = base_class_override
    else:
        base_class_name = nxdl_to_class_name(node.nx_class)
        base_module = _class_module_name(node.nx_class)
    base_lookup = _base_class_quantities(node.nx_class)

    # Collect member names from the full ancestor chain of the base class.
    # qty_names: detect group-vs-field conflicts (group gets _group suffix).
    # sub_names: detect field-vs-group conflicts (field gets _quantity suffix).
    concept_ancestor_qty_names, concept_ancestor_sub_names = _all_ancestor_member_names(
        node.nx_class
    )

    # Own quantities: fields and attributes defined inside the group in NXDL
    # that differ from the parent class (new field, different
    # optionality, different type/units/enumeration).
    own_quantities: list[QuantityContext] = []
    own_links: list[LinkContext] = []
    seen: set[str] = set()
    # Use own_children() to restrict to the current NXDL definition level.
    # This prevents named concepts in derived applications from claiming
    # members defined in parent applications (e.g. XpsInstrument must not
    # include quantities from MpesInstrument).
    node_children = node.own_children()
    for child in node_children:
        if child.nx_type == "link":
            python_name = nxdl_to_quantity_name(child.name)
            # Ancestor SubSection wins: if the link name collides with an
            # inherited SubSection, rename with _quantity suffix.
            if python_name in concept_ancestor_sub_names:
                python_name = field_conflicts_with_group(python_name)
            if python_name not in seen:
                seen.add(python_name)
                own_links.append(
                    LinkContext(
                        python_name=python_name,
                        description=_description_string(child),
                        node=child,
                        target_quantity=_resolve_link_quantity(
                            root_node, child, python_name
                        ),
                    )
                )
            continue
        if child.nx_type not in ("field", "attribute") or not isinstance(
            child, (NXTreeField, NXTreeAttribute)
        ):
            continue
        qty = _build_quantity_from_node(child)
        # Suppress ELN annotation when the override has no explicit shape but
        # the base class field is multi-dimensional: NOMAD's __init_metainfo__
        # inherits the parent's shape, making the ELN validator fail with
        # "Only scalars or lists can be edited."
        if qty.eln_component is not None and not qty.shape:
            base_node = base_lookup.get(child.name)
            if (
                base_node is not None
                and isinstance(base_node, NXTreeField)
                and base_node.shape is not None
                and len(base_node.shape) > 1
            ):
                qty.eln_component = None
                qty.eln_default = None
        # Ancestor SubSection wins: field Quantity gets _quantity suffix.
        if qty.python_name in concept_ancestor_sub_names:
            qty.python_name = field_conflicts_with_group(qty.python_name)
        if qty.python_name in seen:
            continue
        seen.add(qty.python_name)
        if _qty_differs_from_base(qty, base_lookup):
            own_quantities.append(qty)
        # Field-level attribute children.
        if child.nx_type == "field":
            for attr in child.children:
                if attr.nx_type != "attribute" or not isinstance(
                    attr, (NXTreeField, NXTreeAttribute)
                ):
                    continue
                attr_key = f"{qty.python_name}__{nxdl_to_quantity_name(attr.name)}"
                if attr_key in seen:
                    continue
                seen.add(attr_key)
                attr_qty = _build_quantity_from_node(
                    attr,
                    parent_field=qty.node.name,
                    python_name_override=attr_key,
                )
                if _qty_differs_from_base(attr_qty, base_lookup):
                    own_quantities.append(attr_qty)

    # Application-specific sub-groups: children whose Python SubSection name
    # isn't already provided by the parent class, and isn't already declared
    # by the parent concept class either (if one exists).
    #
    # E.g. "analyser" inside NXarpes's "instrument" is new — NXinstrument only
    # has a variadic "detector". MpesInstrument already declaring a slot means
    # XpsInstrument doesn't need to redeclare it.
    base_group_nodes = _base_class_group_nodes(node.nx_class)
    # Compared by python_name (slot identity), not nx_class (type): two
    # groups of the same NX class but different explicit names are different
    # slots, not duplicates of each other (e.g. a generic "environment" vs.
    # a distinctly-named "scan_environment").
    parent_concept_group_names: frozenset[str] = (
        frozenset(
            _group_python_name(c)
            for c in node.children_at_definition(parent_concept_file)
            if isinstance(c, NXTreeGroup)
        )
        if parent_concept_file is not None
        else frozenset()
    )
    own_subsections: list[SubSectionContext] = []
    extra_concepts: list[NamedConceptContext] = []
    seen_sub: set[str] = set()
    for child in node_children:
        if not isinstance(child, NXTreeGroup):
            continue
        sub_python_name = _group_python_name(child)
        if sub_python_name in parent_concept_group_names:
            continue  # already declared in parent concept class
        if sub_python_name in seen_sub:
            continue
        # A collision with a SubSection the generic class already exposes
        # (e.g. "source" on NXinstrument) is only worth its own nested
        # concept when it actually redefines something — e.g. NXarpes
        # narrows `probe` to `["x-ray"]` on its instrument/source, warranting
        # ArpesInstrumentSource(Source). Otherwise the inherited SubSection
        # already covers it and nothing is emitted here.
        base_group_node = base_group_nodes.get(sub_python_name)
        is_collision = base_group_node is not None
        # A collision can still narrow/widen occurrence limits or differ in
        # requiredness/doc (via the same _requiredness_or_doc_differs used
        # for fields) without adding any fields of its own — that has no own
        # content either, but still needs its own SubSection (still pointing
        # at the generic class) to carry the child's own values, rather than
        # being dropped in favor of the inherited one.
        slot_overridden = is_collision and (
            _repeats_from_node(child) != _repeats_from_node(base_group_node)
            or _requiredness_or_doc_differs(child, base_group_node)
        )

        # Symmetric inheritance rule: if the ancestor chain defines a field/
        # attribute with this name, the group introduced at this level is the
        # lower-level concept and gets a _group suffix, leaving the ancestor
        # field's name unchanged.
        effective_python_name = sub_python_name
        if sub_python_name in concept_ancestor_qty_names:
            effective_python_name = f"{sub_python_name}_group"

        if effective_python_name in seen_sub:
            continue

        # New, specifically-named sub-group: recursively check whether it adds
        # quantities/links/subsections of its own beyond its parent class —
        # if so it gets its own nested named concept; otherwise it just gets a
        # SubSection pointing at the parent class with this specific name (or,
        # for a collision, nothing — the inherited SubSection already applies).
        sub_section: SubSectionContext | None = None
        if module_name is not None and category is not None:
            child_naming_base = _concept_class_name(_naming_base, child)
            child_concept_name = child_naming_base
            if child_concept_name == nxdl_to_class_name(child.nx_class):
                child_concept_name = _naming_base + nxdl_to_class_name(child.nx_class)
            if child_concept_name not in _seen_concept:
                _seen_concept.add(child_concept_name)
                # Inherit the parent app's concept for nested groups too
                # (same rule build_context applies to top-level children).
                (
                    _child_override,
                    _child_parent_concept_file,
                    _child_parent_apps,
                ) = _parent_app_concept_override(
                    child,
                    parent_apps,
                )
                nested_concept, nested_extra = _build_named_concept(
                    child_concept_name,
                    child,
                    root_node,
                    base_class_override=_child_override,
                    parent_concept_file=_child_parent_concept_file,
                    module_name=module_name,
                    category=category,
                    seen_concept=_seen_concept,
                    naming_base=child_naming_base,
                    parent_apps=_child_parent_apps,
                )
                if (
                    nested_concept.quantities
                    or nested_concept.links
                    or nested_concept.subsections
                ):
                    target_fqn = (
                        f"{_METAINFO_PACKAGE_ROOT}.{category}.{module_name}"
                        f".{child_concept_name}"
                    )
                    extra_concepts.append(nested_concept)
                    extra_concepts.extend(nested_extra)
                    sub_section = _build_subsection_from_node(
                        child, section_fqn=target_fqn, is_named_concept=True
                    )
        if sub_section is None:
            if is_collision and not slot_overridden:
                continue  # no own content — inherited SubSection already covers this
            sub_section = _build_subsection_from_node(
                child, section_fqn=_section_fqn(child.nx_class)
            )

        sub_section.python_name = effective_python_name
        seen_sub.add(effective_python_name)
        own_subsections.append(sub_section)

    return (
        NamedConceptContext(
            class_name=concept_class_name,
            base_class_name=base_class_name,
            base_module=base_module,
            nx_name_literal=nx_name_literal,
            variable=variable,
            docstring=_plain_description(node),
            quantities=own_quantities,
            links=own_links,
            subsections=own_subsections,
            node=node,
        ),
        extra_concepts,
    )


# ---------------------------------------------------------------------------
# Build full template context for one NXDL class
# ---------------------------------------------------------------------------


_nx_extends_cache: dict[str, str] = {}


def _nx_extends(nx_class: str) -> str:
    """Return the value of the NXDL 'extends' attribute for nx_class.

    Reads only the root XML element (no full tree traversal). Defaults to
    'NXobject' when the attribute is absent or the file cannot be found.
    """
    if nx_class in _nx_extends_cache:
        return _nx_extends_cache[nx_class]

    import glob as _glob
    import xml.etree.ElementTree as _ET

    defs = get_nexus_definitions_path()
    for folder in ("base_classes", "applications", "contributed_definitions"):
        matches = _glob.glob(str(defs / folder / f"{nx_class}.nxdl.xml"))
        if matches:
            try:
                root_el = _ET.parse(matches[0]).getroot()
                result = root_el.attrib.get("extends", "NXobject")
            except Exception:
                result = "NXobject"
            _nx_extends_cache[nx_class] = result
            return result

    _nx_extends_cache[nx_class] = "NXobject"
    return "NXobject"


_chain_members_cache: dict[str, tuple[frozenset[str], frozenset[str]]] = {}


def _all_ancestor_member_names(nx_class: str) -> tuple[frozenset[str], frozenset[str]]:
    """Return (all_qty_names, all_sub_names) from the full NeXus ancestor chain.

    Walks the extends chain starting from nx_class itself (inclusive) and
    collects all Quantity and SubSection python_names. Uses generate_tree_from
    directly (not build_context) to avoid circularity: NXobject has a DATA group
    (NXdata), so build_context("NXobject") would call _all_ancestor_member_names
    ("NXdata") while "NXdata" is still being computed, producing empty results.
    """
    if nx_class in _chain_members_cache:
        return _chain_members_cache[nx_class]

    qty_names: set[str] = set()
    sub_names: set[str] = set()
    visited: set[str] = set()
    current: str | None = nx_class

    while current and current not in visited:
        visited.add(current)
        try:
            root = generate_tree_from(current)
            primary = root.nxdl_base
            for c in root.children:
                if c.nxdl_base != primary:
                    continue
                if c.nx_type == "group":
                    nx_name_type = c.name_type or "specified"
                    if nx_name_type == "any":
                        sub_names.add(nxdl_to_subsection_name(c.name.lower()))
                    else:
                        sub_names.add(nxdl_to_subsection_name(c.name))
                elif c.nx_type in ("field", "attribute"):
                    qty_names.add(nxdl_to_quantity_name(c.name))
        except FileNotFoundError:
            pass
        parent = _nx_extends(current)
        if parent == current or not parent:
            break
        current = parent

    result = (frozenset(qty_names), frozenset(sub_names))
    _chain_members_cache[nx_class] = result
    return result


def _nomad_base_for_nx_class(nx_class: str) -> list[str]:
    """Walk the NeXus extends chain starting from nx_class to find the best
    NOMAD base sections.

    Returns the list of fully-qualified class names from BASESECTIONS_MAP found
    while walking the chain, or _DEFAULT_BASE if none is found.
    """
    visited: set[str] = set()
    current = nx_class
    while current and current not in visited:
        if current in BASESECTIONS_MAP:
            return BASESECTIONS_MAP[current]
        visited.add(current)
        parent = _nx_extends(current)
        if parent == current or parent == "NXobject":
            break
        current = parent
    return _DEFAULT_BASE


def _split_fqn(fqn: str) -> tuple[str, str]:
    """Split 'a.b.c.ClassName' → ('a.b.c', 'ClassName')."""
    last_dot = fqn.rfind(".")
    if last_dot < 0:
        return "", fqn
    return fqn[:last_dot], fqn[last_dot + 1 :]


def _base_from_extends(
    nx_name: str, root_node: NXTreeDefinition
) -> tuple[str, str, bool, list[str]]:
    """Return (class_name, import_path, is_generated, nomad_fqns).

    ``nomad_fqns`` is a list of fully-qualified NOMAD class names to add as
    extra Python bases (e.g. ["nomad.datamodel.metainfo.basesections.Measurement",
    "nomad.datamodel.data.EntryData"]).  Empty list → no extra bases.

    Every generated class (except NXobject itself) has the generated NXobject
    class as its NeXus base, either directly or via an intermediate generated
    class. When a NOMAD base section is appropriate (from BASESECTIONS_MAP or
    the extends chain), it is added as explicit extra base(s) — but only when
    the parent's inheritance chain does not already provide it (avoids redundant
    diamond bases that NOMAD's metaclass cannot resolve).

    - NXobject → Object(BaseSection) — root class, single base only
    - Direct NXobject children → Foo(Object[, NomadBases...])
    - Deeper descendants → Foo(ParentClass[, NomadBases...]) where bases are only
      added when the parent chain does not already provide them
    """
    extends_nx_class: str = (
        root_node.inheritance[0].attrib.get("extends", "NXobject")
        if root_node.inheritance
        else "NXobject"
    )

    # NXobject is the NeXus root — inherits from the BASESECTIONS_MAP entry.
    # Use "basesections.ClassName" so the template imports via the module only.
    if nx_name == "NXobject":
        nomad_fqns = _nomad_base_for_nx_class(nx_name)
        _, base_class_name = _split_fqn(nomad_fqns[0])
        return f"basesections.{base_class_name}", "", False, []

    # NOMAD semantic bases for this class (walks up extends chain to BASESECTIONS_MAP)
    nomad_fqns = _nomad_base_for_nx_class(nx_name)
    nomad_primary = _split_fqn(nomad_fqns[0])[1] if nomad_fqns else "BaseSection"

    if extends_nx_class in ("NXobject", nx_name):
        # Direct child of NXobject — use generated Object as primary NeXus base
        obj_path = _METAINFO_PACKAGE_ROOT + ".base_classes.object"
        if nomad_primary != "BaseSection":
            return "Object", obj_path, True, nomad_fqns
        return "Object", obj_path, True, []

    # Non-trivial NeXus parent — use the generated parent class as primary base
    parent_category = _nxdl_category(extends_nx_class)
    if parent_category in ("base_classes", "applications"):
        ext_module = _class_module_name(extends_nx_class)
        ext_class = nxdl_to_class_name(extends_nx_class)
        ext_path = f"{_METAINFO_PACKAGE_ROOT}.{parent_category}.{ext_module}"
        # Only add NOMAD secondary bases when the parent's chain doesn't already
        # provide them (e.g. ApmRanging extends NXprocess which IS ActivityStep —
        # adding ActivityStep again would create an unresolvable diamond in NOMAD).
        parent_nomad_fqns = _nomad_base_for_nx_class(extends_nx_class)
        parent_primary = (
            _split_fqn(parent_nomad_fqns[0])[1] if parent_nomad_fqns else "BaseSection"
        )
        if nomad_primary != parent_primary:
            return ext_class, ext_path, True, nomad_fqns
        return ext_class, ext_path, True, []

    # Cross-category parent: fall back to generated Object (no raw NOMAD bases).
    # Object already inherits from BaseSection so transitivity is preserved.
    obj_path = _METAINFO_PACKAGE_ROOT + ".base_classes.object"
    return "Object", obj_path, True, []


def build_context(nx_name: str) -> dict:
    """Build the Jinja2 template context for a single NXDL base class.

    Uses generate_tree_from() as the single entry point into NexusNode.
    All NXDL attributes are read exclusively through NexusNode properties —
    no raw XML attribute access inside this function.
    """
    root_node: NXTreeDefinition = generate_tree_from(nx_name)

    nx_category = root_node.category

    # Application definitions wrap exactly one NXentry group at the top level.
    # Unwrap it: Xps(Entry) is correct; Xps(Object) containing an entry is not.
    # Exception: if the application extends another application/contributed class
    # (e.g. NXafm extends NXspm), inherit from that class instead of Entry.
    _unwrapped_children = None
    if nx_category == "application":
        _nx_entry_child = next(
            (
                c
                for c in root_node.children
                if c.nx_type == "group" and c.nx_class == "NXentry"
            ),
            None,
        )
        if _nx_entry_child is not None:
            _unwrapped_children = _nx_entry_child.children

    class_name = nxdl_to_class_name(nx_name)
    parent_module = _class_module_name(nx_name)

    # Ordered chain of ancestor application definitions this one (transitively)
    # extends, nearest first. Passed to _parent_app_concept_override, which
    # tries each in turn rather than only the direct parent.
    _parent_apps: list[tuple[str, str, str]] = []

    if _unwrapped_children is not None:
        # Use Entry as Python base (NXentry's generated class), not the extends chain.
        # The extends chain for application defs is always NXobject which would give Object;
        # but the semantic base is Entry since we've unwrapped the NXentry level.
        _extends_nx_name = (
            root_node.inheritance[0].attrib.get("extends", "NXobject")
            if root_node.inheritance
            else "NXobject"
        )
        if _nxdl_category(_extends_nx_name) == "applications":
            # Extends another application — use that as base (same unwrapping applies).
            # Capture parent metadata so we can derive named concept inheritance directly
            # from child.inheritance (no re-parsing of the parent NXDL).
            (
                base_class,
                base_import,
                base_is_generated,
                nomad_extra_bases,
            ) = _base_from_extends(nx_name, root_node)
            # root_node.inheritance[1:] are the ancestor applications' own definition
            # elements, in order, out to (but excluding) the first non-application
            # ancestor (NXobject, always the eventual terminus for application defs).
            for _ancestor_elem in root_node.inheritance[1:]:
                _ancestor_name = _ancestor_elem.attrib.get("name")
                if (
                    not _ancestor_name
                    or _nxdl_category(_ancestor_name) != "applications"
                ):
                    break
                _parent_apps.append(
                    (
                        _ancestor_elem.base,
                        _class_module_name(_ancestor_name),
                        nxdl_to_class_name(_ancestor_name),
                    )
                )
        else:
            # Standard application: unwrap NXentry → base is Entry
            base_class = "Entry"
            base_import = _METAINFO_PACKAGE_ROOT + ".base_classes.entry"
            base_is_generated = True
            nomad_extra_bases = []
    else:
        (
            base_class,
            base_import,
            base_is_generated,
            nomad_extra_bases,
        ) = _base_from_extends(nx_name, root_node)

    docstring = (
        _plain_description(root_node) or f"NOMAD metainfo class for NeXus {nx_name}."
    )

    quantities: list[QuantityContext] = []
    subsections: list[SubSectionContext] = []
    named_concepts: list[NamedConceptContext] = []
    links: list[LinkContext] = []
    choices: list[ChoiceSubSectionContext] = []
    seen_quantities: set[str] = set()
    seen_subsections: set[str] = set()
    seen_concept: set[str] = set()
    # (module_path, class_name) pairs for concept base imports — only for classes
    # with own quantities. Imports are wrapped in try/except in the template.
    concept_imports: list[tuple[str, str]] = []

    # Collect ancestor member names for two-direction conflict detection:
    # - parent_sub_names: ancestor SubSection names → child Quantity renamed _quantity
    # - parent_qty_names: ancestor Quantity names → child SubSection renamed _group
    # (Symmetric inheritance rule: whichever concept is higher in the NeXus chain
    # keeps the unqualified name; the lower-level concept is renamed.)
    parent_sub_names: frozenset[str] = frozenset()
    parent_qty_names: frozenset[str] = frozenset()
    if base_is_generated:
        if _unwrapped_children is not None:
            # Python base is Entry (from NXentry unwrapping); use NXentry's ancestor
            # chain for conflict detection so that Entry's SubSections (e.g. 'notes')
            # are included in parent_sub_names.
            _conflict_ancestor = "NXentry"
        else:
            _conflict_ancestor = (
                root_node.inheritance[0].attrib.get("extends", "NXobject")
                if root_node.inheritance
                else "NXobject"
            )
        parent_qty_names, parent_sub_names = _all_ancestor_member_names(
            _conflict_ancestor
        )

    # For unwrapped application definitions, children come from the NXentry group;
    # for all others, from root_node directly.
    # primary_nxdl filter is relaxed for unwrapped children (they belong to the
    # NXentry element, whose nxdl_base may differ from the application root).
    effective_children = (
        _unwrapped_children if _unwrapped_children is not None else root_node.children
    )
    primary_nxdl = root_node.nxdl_base

    # Pre-scan: collect subsection python_names defined in this class so that
    # a same-class field with the same name (e.g. NXsample.sample_component field
    # vs NXsample_component variadic group) can be suffixed before processing.
    own_sub_names: set[str] = set()
    for child in effective_children:
        if child.nx_type != "group":
            continue
        if child.nxdl_base != primary_nxdl:
            continue
        nx_nt = child.name_type or "specified"
        if nx_nt == "any":
            own_sub_names.add(nxdl_to_subsection_name(child.name.lower()))
        else:
            own_sub_names.add(nxdl_to_subsection_name(child.name))

    all_sub_names = parent_sub_names | own_sub_names

    for child in effective_children:
        if child.nx_type == "group" and child.nxdl_base != primary_nxdl:
            continue

        if child.nx_type == "attribute":
            qty = _build_quantity_from_node(child)
            # Ancestor SubSection wins: rename field with _quantity suffix.
            if qty.python_name in all_sub_names:
                qty.python_name = field_conflicts_with_group(qty.python_name)
            if qty.python_name in seen_quantities:
                continue
            seen_quantities.add(qty.python_name)
            quantities.append(qty)

        elif child.nx_type == "field":
            qty = _build_quantity_from_node(child)
            if qty.python_name in all_sub_names:
                qty.python_name = field_conflicts_with_group(qty.python_name)
            if qty.python_name in seen_quantities:
                continue
            seen_quantities.add(qty.python_name)
            quantities.append(qty)

            for attr_child in child.children:
                if attr_child.nx_type != "attribute" or not isinstance(
                    attr_child, NXTreeAttribute
                ):
                    continue
                attr_key = (
                    f"{qty.python_name}__{nxdl_to_quantity_name(attr_child.name)}"
                )
                if attr_key in seen_quantities:
                    continue
                seen_quantities.add(attr_key)
                quantities.append(
                    _build_quantity_from_node(
                        attr_child,
                        parent_field=qty.node.name,
                        python_name_override=attr_key,
                    )
                )

        elif child.nx_type == "group":
            # Skip cross-category references whose target module has not been
            # generated yet — NOMAD's __init_metainfo__() would fail to resolve
            # the string FQN.
            if not _target_module_exists(child.nx_class):
                continue

            concept_name = _concept_class_name(class_name, child)
            if concept_name in seen_concept:
                # Collision: two groups mapping to the same concept name.
                # Fall back to full group name regardless of name_type.
                child_suffix = "".join(
                    p.capitalize()
                    for p in child.name.lower().replace("-", "_").split("_")
                    if p
                )
                concept_name = class_name + child_suffix
                if concept_name in seen_concept:
                    continue  # still a collision — skip (rare)
            seen_concept.add(concept_name)

            # If concept name would equal the base class name → circular inheritance.
            # Disambiguate by re-prefixing with the full type-based name.
            # e.g. NXapm.measurement (type NXapm_measurement):
            #   concept "ApmMeasurement" == base "ApmMeasurement" → "ApmApmMeasurement"
            # Nested concepts are named from the un-doubled name (_naming_base):
            # ApmApmMeasurement's "instrument" child becomes
            # "ApmMeasurementInstrument", not "ApmApmMeasurementInstrument".
            _naming_base = concept_name
            if concept_name == nxdl_to_class_name(child.nx_class):
                concept_name = class_name + nxdl_to_class_name(child.nx_class)

            # Inherit the parent app's concept (XpsInstrument(MpesInstrument))
            # instead of the generic base; applied recursively for nested groups.
            (
                _base_class_override,
                _parent_concept_file,
                _child_parent_apps,
            ) = _parent_app_concept_override(child, _parent_apps)
            _parent_category = _nxdl_category(nx_name)
            concept, extra_concepts = _build_named_concept(
                concept_name,
                child,
                root_node,
                base_class_override=_base_class_override,
                parent_concept_file=_parent_concept_file,
                module_name=parent_module,
                category=_parent_category,
                seen_concept=seen_concept,
                naming_base=_naming_base,
                parent_apps=_child_parent_apps,
            )

            if concept.quantities or concept.links or concept.subsections:
                named_concepts.append(concept)
                target_fqn = f"{_METAINFO_PACKAGE_ROOT}.{_parent_category}.{parent_module}.{concept_name}"

                # Track import for concept base class (skip self-referencing groups).
                for _c in (concept, *extra_concepts):
                    if _c.base_module != parent_module:
                        _base_category = _nxdl_category(f"NX{_c.base_module}")
                        import_entry = (
                            f"{_METAINFO_PACKAGE_ROOT}.{_base_category}.{_c.base_module}",
                            _c.base_class_name,
                        )
                        if import_entry not in concept_imports:
                            concept_imports.append(import_entry)
                named_concepts.extend(extra_concepts)

                sub_section = _build_subsection_from_node(
                    child, section_fqn=target_fqn, is_named_concept=True
                )
            else:
                # Group is semantically identical to its generic class and has a
                # specified (fixed) name → SubSection points directly to the generic
                # class via string FQN.
                target_fqn = _section_fqn(child.nx_class)
                sub_section = _build_subsection_from_node(child, section_fqn=target_fqn)
            # Symmetric inheritance rule: if this group conflicts with an ancestor
            # Quantity of the same name, the group gets _group suffix here.
            if sub_section.python_name in parent_qty_names:
                sub_section.python_name = f"{sub_section.python_name}_group"
            if sub_section.python_name in seen_subsections:
                # Two named groups with the same subsection name — disambiguate.
                if not child.variadic:
                    sub_section.python_name = nxdl_to_subsection_name(
                        f"{child.name}_{child.nx_class[2:].lower()}"
                    )
                else:
                    continue
            seen_subsections.add(sub_section.python_name)
            subsections.append(sub_section)
        elif child.nx_type == "link":
            python_name = nxdl_to_quantity_name(child.name)
            if python_name in seen_quantities:
                continue
            seen_quantities.add(python_name)
            links.append(
                LinkContext(
                    python_name=python_name,
                    description=_description_string(child),
                    node=child,
                    target_quantity=_resolve_link_quantity(
                        root_node, child, python_name
                    ),
                )
            )

        elif child.nx_type == "choice":
            # A <choice> block contains NexusGroup children, one per alternative.
            # Each alternative becomes its own SubSection named
            # "{choice_name}_{class_suffix}" (e.g. "pixel_shape_off_geometry").
            for alt_group in child.children:
                if alt_group.nx_type != "group":
                    continue
                if _nxdl_category(alt_group.nx_class) != "base_classes":
                    continue
                class_suffix = nxdl_to_quantity_name(alt_group.nx_class[2:])
                python_name = f"{nxdl_to_quantity_name(child.name)}_{class_suffix}"
                if python_name in seen_subsections:
                    continue
                seen_subsections.add(python_name)
                choices.append(
                    ChoiceSubSectionContext(
                        python_name=python_name,
                        group_name=child.name,
                        section_fqn=_section_fqn(alt_group.nx_class),
                        description=_description_string(alt_group),
                        node=alt_group,
                    )
                )

    needs_m_enum = any(
        q.python_type.startswith("MEnum")
        for q in quantities + [q for c in named_concepts for q in c.quantities]
    )

    # Remove concept imports already covered by the main generated-base import.
    if base_is_generated:
        concept_imports = [
            (mod, cls)
            for mod, cls in concept_imports
            if not (mod == base_import and cls == base_class)
        ]

    is_contributed = "contributed_definitions" in (root_node.nxdl_base or "")

    nomad_extra_bases_list = [_split_fqn(fqn) for fqn in nomad_extra_bases]
    needs_basesections = "basesections." in base_class or any(
        mod == "nomad.datamodel.metainfo.basesections"
        for mod, _ in nomad_extra_bases_list
    )

    return {
        "class_name": class_name,
        "nx_name": nx_name,
        "nx_category": nx_category,
        "is_contributed": is_contributed,
        "nx_deprecated": root_node.deprecated,
        "ignore_extra_groups": root_node.ignore_extra_groups,
        "ignore_extra_fields": root_node.ignore_extra_fields,
        "ignore_extra_attributes": root_node.ignore_extra_attributes,
        "nx_symbols": root_node.symbols,
        "base_class": base_class,
        "base_import": base_import,
        "base_is_generated": base_is_generated,
        "nomad_extra_bases": nomad_extra_bases_list,
        "needs_basesections": needs_basesections,
        "docstring": docstring,
        "class_doc_url": root_node.get_link(),
        "quantities": quantities,
        "subsections": subsections,
        "named_concepts": named_concepts,
        "links": links,
        "choices": choices,
        "concept_imports": sorted(concept_imports),
        "needs_m_enum": needs_m_enum,
    }


# ---------------------------------------------------------------------------
# Render and format
# ---------------------------------------------------------------------------


def render(context: dict, out_path: Path | None = None) -> str:
    """Render the Jinja2 template and format with ruff."""
    template = _jinja_env.get_template("nexus.py.j2")
    raw = template.render(**context)
    # Use the real output path as stdin-filename so ruff picks up pyproject.toml
    stdin_filename = str(out_path) if out_path is not None else "generated.py"
    try:
        result = subprocess.run(
            ["ruff", "check", "--fix", f"--stdin-filename={stdin_filename}", "-"],
            input=raw,
            capture_output=True,
            text=True,
            check=False,
        )
        checked = result.stdout if result.stdout else raw
    except Exception:
        checked = raw
    try:
        result = subprocess.run(
            ["ruff", "format", f"--stdin-filename={stdin_filename}", "-"],
            input=checked,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except Exception:
        return checked


# ---------------------------------------------------------------------------
# Additive-only write
# ---------------------------------------------------------------------------


def _existing_member_names(source: str) -> set[str]:
    """Parse a Python source file and return top-level class member names."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            names.add(target.id)
                elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(child.name)
    return names


def write_class(
    nx_name: str,
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> bool:
    """Generate and write the Python file for any NXDL class (base or application).

    Returns True if the file content changed (or was created), False if unchanged.
    In dry_run mode: returns True if the file would differ, raises nothing.

    output_dir should be the parent of base_classes/ and applications/ — the generator
    appends the correct subfolder automatically. Defaults to the pynxtools-internal
    metainfo/ directory. Pass an explicit path to generate into a different package
    (e.g. --output-dir ../nomad-measurements/src/nomad_measurements/nexus/metainfo).
    """
    module_name = _class_module_name(nx_name)
    is_application = _nxdl_category(nx_name) == "applications"
    subfolder = "applications" if is_application else "base_classes"
    if output_dir is not None:
        dest = output_dir / subfolder
    elif is_application:
        dest = _DEFAULT_APPLICATIONS_OUTPUT_DIR
    else:
        dest = _DEFAULT_BASE_OUTPUT_DIR
    out_path = dest / f"{module_name}.py"

    context = build_context(nx_name)
    new_source = render(context, out_path=out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists():
        existing_source = out_path.read_text(encoding="utf-8")

        if dry_run:
            return new_source != existing_source

        if force:
            pass
        else:
            if existing_source == new_source:
                return False
            existing_members = _existing_member_names(existing_source)
            new_members = _existing_member_names(new_source)
            user_added = existing_members - new_members
            if user_added:
                return False

    if dry_run:
        return True

    out_path.write_text(new_source, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Topological sort: generate files in dependency order
# ---------------------------------------------------------------------------


def _nxdl_category_attr(nx_class: str) -> str:
    """Read the category attribute from the NXDL <definition> element directly."""
    try:
        root = generate_tree_from(nx_class)
        return root.category or "base"
    except Exception:
        return "base"


def _discover_all_nxdl_classes() -> list[str]:
    """Return all NXDL class names across all definition folders."""
    defs = get_nexus_definitions_path()
    result: list[str] = []
    for folder in ("base_classes", "applications", "contributed_definitions"):
        folder_dir = defs / folder
        if folder_dir.exists():
            result.extend(
                f.stem.replace(".nxdl", "") for f in folder_dir.glob("*.nxdl.xml")
            )
    return sorted(set(result))


def _discover_base_classes() -> list[str]:
    """Return all NXDL classes with category='base'."""
    return [
        nx for nx in _discover_all_nxdl_classes() if _nxdl_category_attr(nx) == "base"
    ]


def _discover_applications() -> list[str]:
    """Return all NXDL classes with category='application'."""
    return [
        nx
        for nx in _discover_all_nxdl_classes()
        if _nxdl_category_attr(nx) == "application"
    ]


def _build_dependency_graph(nx_names: list[str]) -> dict[str, set[str]]:
    deps: dict[str, set[str]] = {}
    for nx_name in nx_names:
        try:
            xml_root, _ = get_nxdl_root_and_path(nx_name)
        except Exception:
            deps[nx_name] = set()
            continue
        extends = xml_root.attrib.get("extends", "NXobject")
        d: set[str] = set()
        if extends and extends != nx_name:
            d.add(extends)
        deps[nx_name] = d
    return deps


def write_base_class(
    nx_name: str,
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> bool:
    """Backward-compatible alias for write_class."""
    return write_class(nx_name, dry_run=dry_run, force=force, output_dir=output_dir)


def _generate_nx_classes(
    nx_names: list[str],
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> int:
    """Generate Python files for a list of NXDL classes in dependency order."""
    dep_graph = _build_dependency_graph(nx_names)
    ordered = toposort_flatten(dep_graph, sort=True)

    written = 0
    for nx_name in ordered:
        if nx_name not in dep_graph:
            continue
        try:
            changed = write_class(
                nx_name, dry_run=dry_run, force=force, output_dir=output_dir
            )
        except Exception as exc:
            print(f"  SKIP {nx_name}: {exc}")
            continue
        if changed:
            written += 1
    return written


def generate_all_base_classes(
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> int:
    """Generate Python files for all NXDL base-category classes in dependency order."""
    return _generate_nx_classes(
        _discover_base_classes(), dry_run=dry_run, force=force, output_dir=output_dir
    )


def generate_all_applications(
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> int:
    """Generate Python files for all NXDL application-category classes in dependency order."""
    return _generate_nx_classes(
        _discover_applications(), dry_run=dry_run, force=force, output_dir=output_dir
    )
