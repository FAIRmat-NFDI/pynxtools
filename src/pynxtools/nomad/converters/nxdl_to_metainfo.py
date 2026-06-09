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
from pynxtools.nexus.utils import get_nexus_definitions_path
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
    """A NXDL <link> element — emitted as a Quantity(type=str) with NeXusLink."""

    python_name: str  # nxdl_to_quantity_name(node.name)
    description: str | None  # <doc> text from the link element
    node: NXTreeLink


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
    """Section class for a group occurrence that defines its own quantities or children.

    Generated when the NXDL group element specifies fields/attributes that
    differ from the generic class (changed optionality, extra fields, different
    type/units/enumeration) OR has sub-group children with nx_class not present
    in the base NXDL class (application-specific nested groups, e.g.
    NXelectronanalyzer inside NXinstrument in NXmpes).

    Inherits from the specific generic class (e.g. ``Note`` for NXnote) so that
    all base class quantities are available. The import is wrapped in
    ``try/except ImportError`` in the generated file to handle the rare case of
    circular NXDL group references. The SubSection pointing to this class
    carries a_nexus_group; this class carries only the differing members.
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
    # Wrap to (79 - 12 col indent) = 67 chars
    wrapped = textwrap.fill(
        escaped, width=67, break_long_words=False, break_on_hyphens=False
    )
    lines = wrapped.split("\n")
    if len(lines) == 1:
        return f'"{escaped}"'
    pad = " " * 12
    parts = [f'"{line} "' for line in lines[:-1]] + [f'"{lines[-1]}"']
    return ("\n" + pad).join(parts)


# ---------------------------------------------------------------------------
# Named concept class naming helper
# ---------------------------------------------------------------------------


def _concept_class_name(parent_class_name: str, node: NXTreeGroup) -> str:
    """Return the Python class name for a named concept class.

    For variadic groups (name_type="any") the NX class name is the suffix,
    e.g. ``ObjectLog`` for any NXlog inside NXobject.

    For partial groups (name_type="partial") the NXDL name follows the
    convention ``fixedPrefixVARIABLE_SUFFIX`` — the upper-case part marks the
    user-chosen portion. Only the lower-case prefix is meaningful, e.g.
    ``peakPEAK`` → ``"peak"`` → ``FitPeak``.

    For fixed-name groups (name_type="specified") the full name is used in
    CamelCase, e.g. ``temperature_log`` → ``SampleTemperatureLog``.
    """
    return _concept_class_name_from_parts(
        parent_class_name, node.name, node.name_type or "specified", node.nx_class
    )


def _concept_class_name_from_parts(
    parent_class_name: str, name: str, name_type: str, nx_class: str
) -> str:
    """Compute concept class name from explicit name/name_type/nx_class parts.

    Used when the source is a raw inheritance XML element (via ``group_naming_at``)
    rather than a full NexusGroup node.
    """
    if name_type == "any":
        child_suffix = nxdl_to_class_name(nx_class)
    elif name_type == "partial":
        child_suffix = name[0].upper() + name[1:] if name else ""
    else:
        child_suffix = "".join(
            p.capitalize() for p in name.lower().replace("-", "_").split("_") if p
        )
    return parent_class_name + child_suffix


# ---------------------------------------------------------------------------
# Build quantity context from a NXTreeField node
# ---------------------------------------------------------------------------


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
    python_name = python_name_override or nxdl_to_quantity_name(node.name)

    if isinstance(node, NXTreeField):
        # NX_TRANSFORMATION means any length/angle/dimensionless → map to NX_ANY.
        raw_unit = node.unit if node.unit != "NX_TRANSFORMATION" else "NX_ANY"
        unit = raw_unit
        dimensionality = _get_dimensionality(raw_unit)
        shape = _shape_from_node(node)
        interpretation = node.interpretation
        long_name = node.long_name
    else:
        unit = None
        dimensionality = None
        shape = _shape_from_node(node)
        interpretation = None
        long_name = None

    # Enum items whose values are themselves lists (e.g. `['kinetic_energy']`) cannot
    # be used in MEnum (unhashable) or in NeXusQuantity.enumeration (list[str]).
    scalar_items: list[str] | None = None
    if node.items and not any(isinstance(item, list) for item in node.items):
        scalar_items = node.items

    if scalar_items and not node.open_enum:
        python_type = f"MEnum({scalar_items!r})"
    else:
        python_type = nx_type_to_source(node.dtype)

    return QuantityContext(
        python_name=python_name,
        python_type=python_type,
        dimensionality=dimensionality,
        shape=shape,
        parent_field=parent_field,
        description=_description_string(node),
        unit=unit,
        interpretation=interpretation,
        long_name=long_name,
        scalar_items=scalar_items,
        node=node,
    )


# ---------------------------------------------------------------------------
# Build subsection context from a NXTreeGroup node
# ---------------------------------------------------------------------------


def _build_subsection_from_node(
    node: NXTreeGroup,
    section_fqn: str,
    is_named_concept: bool = False,
) -> SubSectionContext:
    """Build a SubSectionContext from a NexusGroup (group) node.

    ``section_fqn`` is the fully-qualified string proxy that NOMAD resolves at
    __init_metainfo__() time. For groups with no own quantities this points to
    the generic class (e.g. "...user.User") and ``is_named_concept=False``.
    For groups with own quantities it points to the named concept class defined
    in this same file and ``is_named_concept=True``.

    When ``is_named_concept=True`` the concept class carries a_nexus_group on
    its own m_def and the SubSection is rendered clean (no annotation).
    When ``is_named_concept=False`` a_nexus_group is rendered on the SubSection.
    """
    nx_name_type = node.name_type or "specified"

    repeats: bool = node.variadic
    variable = nx_name_type in ("any", "partial")

    if nx_name_type == "any":
        stem = (
            node.nx_class[2:].lower()
            if node.nx_class.startswith("NX")
            else node.nx_class.lower()
        )
        python_name = nxdl_to_subsection_name(stem)
        nx_name_literal = "None"
    elif nx_name_type == "partial":
        # Partial groups: use the full NXDL name as the python attribute name
        # (e.g. "peakPEAK") so the partial-group nature is visible in code and
        # the name is consistent with the concept class name (FitPeakPEAK).
        python_name = nxdl_to_subsection_name(node.name)
        nx_name_literal = f'"{node.name}"'
    else:
        python_name = nxdl_to_subsection_name(node.name)
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


def _parent_generates_concept(child: NXTreeGroup, parent_app_file: str) -> bool:
    """Return True if the parent application defines a named concept for ``child``.

    Uses ``child.children_at_definition(parent_app_file)`` — the NexusNode API
    that selects children defined at a specific NXDL level without re-parsing.
    """
    base_group_nx = _base_class_group_nx_classes(child.nx_class)
    for c in child.children_at_definition(parent_app_file):
        if c.nx_type in ("field", "attribute", "link"):
            return True
        if c.nx_type == "group" and getattr(c, "nx_class", None) not in base_group_nx:
            return True
    return False


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


def _qty_differs_from_base(
    qty: QuantityContext, base_lookup: dict[str, NXTreeField | NXTreeAttribute]
) -> bool:
    """Return True if this quantity is new or has different properties in the base class."""
    base_node = base_lookup.get(qty.node.name)
    if base_node is None:
        return True  # quantity not in generic class — genuinely new
    if qty.node.dtype != base_node.dtype:
        return True
    if qty.node.optionality != base_node.optionality:
        return True
    if qty.node.items != base_node.items:
        return True
    if (
        isinstance(qty.node, NXTreeField)
        and isinstance(base_node, NXTreeField)
        and qty.node.unit != base_node.unit
    ):
        return True
    return False


def _build_named_concept(
    concept_class_name: str,
    node: NXTreeGroup,
    base_class_override: tuple[str, str] | None = None,
    parent_concept_file: str | None = None,
) -> NamedConceptContext:
    """Build a NamedConceptContext for a group occurrence.

    Collects the fields/attributes defined *inside* the group XML element
    (one level deep) as own Quantities of the concept class. Returns a
    context whose ``quantities`` list is empty when the group occurrence
    adds nothing beyond what the generic class already provides — callers
    use that to decide whether a named concept class is needed at all.
    """
    nx_name_type = node.name_type or "specified"
    variable = nx_name_type in ("any", "partial")

    if nx_name_type == "any":
        nx_name_literal = "None"
    else:
        # specified or partial — store the NXDL name.
        # For partial groups this preserves the full name (e.g. "peakPEAK") so
        # the parser can extract the prefix matching rule.
        nx_name_literal = f'"{node.name}"'

    if base_class_override is not None:
        base_class_name, base_module = base_class_override
    else:
        base_class_name = nxdl_to_class_name(node.nx_class)
        base_module = _class_module_name(node.nx_class)
    base_lookup = _base_class_quantities(node.nx_class)

    # Collect SubSection names from the full ancestor chain of the base class
    # so we can detect Quantity-vs-SubSection conflicts in own quantities.
    _, concept_ancestor_sub_names = _all_ancestor_member_names(node.nx_class)
    concept_field_suffix = _qty_field_suffix_for.get(node.nx_class, frozenset())

    # Own quantities: fields and attributes defined inside the group in NXDL
    # that genuinely differ from the generic class (new field, different
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
            # Apply conflict resolution: if the link name collides with an
            # inherited SubSection or a known field-suffix conflict, rename.
            if python_name in concept_field_suffix:
                python_name = field_conflicts_with_group(python_name)
            elif python_name in concept_ancestor_sub_names:
                python_name = field_conflicts_with_group(python_name)
            if python_name not in seen:
                seen.add(python_name)
                own_links.append(
                    LinkContext(
                        python_name=python_name,
                        description=_description_string(child),
                        node=child,
                    )
                )
            continue
        if child.nx_type not in ("field", "attribute") or not isinstance(
            child, (NXTreeField, NXTreeAttribute)
        ):
            continue
        qty = _build_quantity_from_node(child)
        # Apply same conflict resolution as top-level quantities: ancestor
        # SubSection wins, field Quantity gets _field suffix.
        if qty.python_name in concept_field_suffix:
            qty.python_name = field_conflicts_with_group(qty.python_name)
        elif qty.python_name in concept_ancestor_sub_names:
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

    # Application-specific sub-groups: group children whose nx_class is NOT
    # present in the base NXDL class AND not already declared by the parent
    # concept class (if one exists, e.g. MpesInstrument for XpsInstrument).
    base_group_nx_classes = _base_class_group_nx_classes(node.nx_class)
    # Sub-groups already covered by the parent concept class (to avoid duplication)
    parent_concept_nx_classes: frozenset[str] = (
        frozenset(
            getattr(c, "nx_class", None)
            for c in node.children_at_definition(parent_concept_file)
            if isinstance(c, NXTreeGroup)
        )
        if parent_concept_file is not None
        else frozenset()
    )
    own_subsections: list[SubSectionContext] = []
    seen_sub: set[str] = set()
    for child in node_children:
        if not isinstance(child, NXTreeGroup):
            continue
        if child.nx_class in base_group_nx_classes:
            continue  # already covered by the base NX class
        if child.nx_class in parent_concept_nx_classes:
            continue  # already declared in parent concept class
        sub_section = _build_subsection_from_node(
            child, section_fqn=_section_fqn(child.nx_class)
        )
        if sub_section.python_name not in seen_sub:
            seen_sub.add(sub_section.python_name)
            own_subsections.append(sub_section)

    return NamedConceptContext(
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
                    nx_nt = c.name_type or "specified"
                    if nx_nt == "any":
                        stem = (
                            c.nx_class[2:].lower()
                            if c.nx_class.startswith("NX")
                            else c.nx_class.lower()
                        )
                        sub_names.add(nxdl_to_subsection_name(stem))
                    else:
                        sub_names.add(nxdl_to_subsection_name(c.name))
                elif c.nx_type in ("field", "attribute"):
                    qty_names.add(nxdl_to_quantity_name(c.name))
        except Exception:
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


_qty_field_suffix_for: dict[str, frozenset[str]] = {}
_conflicts_precomputed: bool = False


def _ensure_conflicts_precomputed() -> None:
    """Precompute which Quantity python_names in which NXDL classes need a
    ``_field`` suffix to avoid NOMAD ``MetainfoError: Cannot inherit from
    different property types``.

    Rule: when a descendant class defines a GROUP named X and an ancestor
    defines a FIELD named X, the ancestor's field is renamed to X_field.
    Groups always win the unqualified name.

    This scan runs once (lazily on the first ``build_context`` call) and
    caches results in ``_qty_field_suffix_for``. It uses only
    ``generate_tree_from`` (no ``build_context``) to avoid circularity.
    """
    global _conflicts_precomputed
    if _conflicts_precomputed:
        return
    _conflicts_precomputed = True

    all_classes = _discover_base_classes() + _discover_applications()

    # Pass 1: collect own group python_names per class
    class_group_names: dict[str, set[str]] = {}
    for nx_class in all_classes:
        group_names: set[str] = set()
        try:
            root = generate_tree_from(nx_class)
            primary = root.nxdl_base
            for c in root.children:
                if c.nx_type != "group" or c.nxdl_base != primary:
                    continue
                nx_nt = c.name_type or "specified"
                if nx_nt == "any":
                    stem = (
                        c.nx_class[2:].lower()
                        if c.nx_class.startswith("NX")
                        else c.nx_class.lower()
                    )
                    group_names.add(nxdl_to_subsection_name(stem))
                else:
                    group_names.add(nxdl_to_subsection_name(c.name))
        except Exception:
            pass
        class_group_names[nx_class] = group_names

    # Pass 2: for each class, walk ancestor chain to find conflicting fields
    pending: dict[str, set[str]] = {}
    for nx_class, group_names in class_group_names.items():
        if not group_names:
            continue
        visited: set[str] = set()
        current: str | None = _nx_extends(nx_class)
        while current and current not in visited:
            visited.add(current)
            try:
                root = generate_tree_from(current)
                primary = root.nxdl_base
                for c in root.children:
                    if c.nx_type == "field" and c.nxdl_base == primary:
                        py_name = nxdl_to_quantity_name(c.name)
                        if py_name in group_names:
                            pending.setdefault(current, set()).add(py_name)
            except Exception:
                pass
            parent = _nx_extends(current)
            if parent == current or parent == "NXobject":
                if "NXobject" not in visited:
                    visited.add("NXobject")
                    try:
                        root = generate_tree_from("NXobject")
                        primary = root.nxdl_base
                        for c in root.children:
                            if c.nx_type == "field" and c.nxdl_base == primary:
                                py_name = nxdl_to_quantity_name(c.name)
                                if py_name in group_names:
                                    pending.setdefault("NXobject", set()).add(py_name)
                    except Exception:
                        pass
                break
            current = parent

    _qty_field_suffix_for.update({k: frozenset(v) for k, v in pending.items()})


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

    # NXobject is the NeXus root — BaseSection only, no generated parent
    if nx_name == "NXobject":
        cls, mod = _split_fqn(_DEFAULT_BASE[0])
        return cls, mod, False, []

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

    # Cross-category parent or self-referential: fall back to NOMAD bases only
    cls, mod = _split_fqn(nomad_fqns[0]) if nomad_fqns else _split_fqn(_DEFAULT_BASE[0])
    return cls, mod, False, []


def build_context(nx_name: str) -> dict:
    """Build the Jinja2 template context for a single NXDL base class.

    Uses generate_tree_from() as the single entry point into NexusNode.
    All NXDL attributes are read exclusively through NexusNode properties —
    no raw XML attribute access inside this function.
    """
    _ensure_conflicts_precomputed()
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

    # File path of the direct parent application definition, used to locate
    # each child group's "parent version" in child.inheritance without re-parsing.
    _parent_app_file: str | None = None
    _parent_class_name: str | None = None
    _parent_module: str | None = None
    _parent_primary_nxdl: str | None = None  # nxdl_base of groups defined in parent

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
            # root_node.inheritance[1] is the parent application's definition element
            if len(root_node.inheritance) > 1:
                _parent_app_file = root_node.inheritance[1].base
                _parent_class_name = nxdl_to_class_name(_extends_nx_name)
                _parent_module = _class_module_name(_extends_nx_name)
                _parent_primary_nxdl = root_node.inheritance[1].base
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

    # Collect all SubSection python_names from the full ancestor chain to detect
    # Quantity-vs-SubSection type conflicts. When a child Quantity has the same
    # python_name as an ancestor SubSection, the Quantity is renamed to _field.
    # The reverse direction (child SubSection vs ancestor Quantity) is handled by
    # _ensure_conflicts_precomputed() which marks the ancestor Quantity for _field.
    parent_sub_names: frozenset[str] = frozenset()
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
        _, parent_sub_names = _all_ancestor_member_names(_conflict_ancestor)

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
            stem = (
                child.nx_class[2:].lower()
                if child.nx_class.startswith("NX")
                else child.nx_class.lower()
            )
            own_sub_names.add(nxdl_to_subsection_name(stem))
        else:
            own_sub_names.add(nxdl_to_subsection_name(child.name))

    all_sub_names = parent_sub_names | own_sub_names

    for child in effective_children:
        if child.nx_type == "group" and child.nxdl_base != primary_nxdl:
            continue

        if child.nx_type == "attribute":
            qty = _build_quantity_from_node(child)
            # Group wins: if a descendant uses this name for a group, the field
            # was precomputed to need _field suffix.
            if qty.python_name in _qty_field_suffix_for.get(nx_name, frozenset()):
                qty.python_name = field_conflicts_with_group(qty.python_name)
            elif qty.python_name in all_sub_names:
                qty.python_name = field_conflicts_with_group(qty.python_name)
            if qty.python_name in seen_quantities:
                continue
            seen_quantities.add(qty.python_name)
            quantities.append(qty)

        elif child.nx_type == "field":
            qty = _build_quantity_from_node(child)
            if qty.python_name in _qty_field_suffix_for.get(nx_name, frozenset()):
                qty.python_name = field_conflicts_with_group(qty.python_name)
            elif qty.python_name in all_sub_names:
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
            # the string FQN.  Once Phase 2 generates all application modules,
            # regenerate base classes with --force to capture these references.
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
            if concept_name == nxdl_to_class_name(child.nx_class):
                concept_name = class_name + nxdl_to_class_name(child.nx_class)

            # If the parent application defines a specialization for this group,
            # use it as the base instead of the generic NX class.
            # e.g. XpsInstrument(MpesInstrument) rather than XpsInstrument(Instrument).
            # Uses child.children (already populated across all inheritance levels by
            # generate_tree_from + populate_tree_from_parents) filtered by nxdl_base.
            _base_class_override: tuple[str, str] | None = None
            if (
                _parent_app_file is not None
                and _parent_class_name is not None
                and _parent_module is not None
                and child.definition_file_at(1) == _parent_app_file
                and _parent_generates_concept(child, _parent_app_file)
            ):
                # Use group_naming_at(1) — the parent's XML attributes for this group
                # — to compute the concept name as the parent would have generated it.
                # This handles variadic-to-specific specialization: the parent may have
                # a variadic "TASKCONFIG" slot that the derived app fills as "cameca_to_nexus";
                # we need "ApmParaprobeToolConfigApmParaprobeToolParameters" (parent's name)
                # not "ApmParaprobeToolConfigCamecaToNexus" (derived app's name).
                parent_naming = child.group_naming_at(1)
                if parent_naming is not None:
                    p_name, p_name_type, p_nx_class = parent_naming
                    parent_concept_name = _concept_class_name_from_parts(
                        _parent_class_name, p_name, p_name_type, p_nx_class
                    )
                    _base_class_override = (parent_concept_name, _parent_module)
            concept = _build_named_concept(
                concept_name,
                child,
                base_class_override=_base_class_override,
                parent_concept_file=_parent_app_file
                if _base_class_override is not None
                else None,
            )

            if concept.quantities or concept.links or concept.subsections:
                named_concepts.append(concept)
                _parent_category = _nxdl_category(nx_name)
                target_fqn = f"{_METAINFO_PACKAGE_ROOT}.{_parent_category}.{parent_module}.{concept_name}"

                # Track import for concept base class (skip self-referencing groups).
                if concept.base_module != parent_module:
                    _base_category = _nxdl_category(f"NX{concept.base_module}")
                    import_entry = (
                        f"{_METAINFO_PACKAGE_ROOT}.{_base_category}.{concept.base_module}",
                        concept.base_class_name,
                    )
                    if import_entry not in concept_imports:
                        concept_imports.append(import_entry)

                sub_section = _build_subsection_from_node(
                    child, section_fqn=target_fqn, is_named_concept=True
                )
            else:
                # Group is semantically identical to its generic class and has a
                # specified (fixed) name → SubSection points directly to the generic
                # class via string FQN.
                target_fqn = _section_fqn(child.nx_class)
                sub_section = _build_subsection_from_node(child, section_fqn=target_fqn)
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
        "nomad_extra_bases": [_split_fqn(fqn) for fqn in nomad_extra_bases],
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
