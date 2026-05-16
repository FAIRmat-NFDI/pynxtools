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
pynxtools.dataconverter.nexus_tree.  NexusEntity already resolves dtype,
units, shape, enumerations, and optionality through the inheritance chain.
Attributes not exposed by NexusNode (interpretation, long_name, deprecated)
are available as properties added to NexusEntity / NexusGroup.

build_base_class_node(nx_name) in nexus_tree.py is the single entry point
for building a NexusGroup with pre-populated children — no raw XML parsing
happens inside this module.

Entry points
------------
write_base_class(nx_name)       — write one base class .py file
generate_all_base_classes()     — write all base class .py files
"""

from __future__ import annotations

import ast
import subprocess
from dataclasses import dataclass
from pathlib import Path

import jinja2
from toposort import toposort_flatten

from pynxtools.dataconverter.helpers import get_nxdl_root_and_path
from pynxtools.dataconverter.nexus_tree import NexusEntity, build_base_class_node
from pynxtools.dataconverter.nexus_tree import NexusGroup as NXTreeGroup
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path
from pynxtools.nomad.converters._naming import (
    get_base_section,
    nx_type_to_source,
    nxdl_to_class_name,
    nxdl_to_quantity_name,
    nxdl_to_subsection_name,
)
from pynxtools.units import NXUnitSet

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_DEFAULT_OUTPUT_DIR = Path(__file__).parents[1] / "metainfo" / "base_classes"

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
    # The originating NexusEntity node — all other info is read via node.*
    node: NexusEntity


@dataclass
class SubSectionContext:
    # Values that require a transformation and cannot be read directly from the node.
    python_name: str  # nxdl_to_subsection_name(…)
    section_fqn: str  # fully-qualified string proxy for SubSection.section_def
    repeats: bool  # computed from occurrence_limits + variadic + name_type
    nx_name_literal: str  # Python source literal: '"name"' or 'None'
    # The originating NexusGroup node — all other info is read via node.*
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
# Shape conversion: NexusEntity.shape tuple → template list
#
# NexusEntity._set_shape() returns None when rank is symbolic (e.g. rank="n").
# In that case we report a wildcard shape of rank 1 rather than omitting shape
# entirely — the correct rank cannot be determined statically.
# ---------------------------------------------------------------------------


def _shape_from_node(node: NexusEntity) -> list[int | str] | None:
    if node.shape is not None:
        return [d if d is not None else "*" for d in node.shape]
    # Symbolic rank: node.shape is None even though dimensions exist.
    # Return None so the Quantity is emitted without an explicit shape.
    return None


# ---------------------------------------------------------------------------
# Cross-category FQN helpers
# ---------------------------------------------------------------------------


_NXDL_CATEGORY_CACHE: dict[str, str] = {}


def _nxdl_category(nx_class: str) -> str:
    """Return the metainfo sub-package name ('base_classes', 'applications',
    or 'contributed') for a given NXDL class name."""
    if nx_class in _NXDL_CATEGORY_CACHE:
        return _NXDL_CATEGORY_CACHE[nx_class]

    import glob as _glob

    defs = get_nexus_definitions_path()
    cat_map = {
        "base_classes": "base_classes",
        "applications": "applications",
        "contributed_definitions": "contributed",
    }
    for folder, metainfo_sub in cat_map.items():
        if _glob.glob(str(defs / folder / f"{nx_class}.nxdl.xml")):
            _NXDL_CATEGORY_CACHE[nx_class] = metainfo_sub
            return metainfo_sub

    _NXDL_CATEGORY_CACHE[nx_class] = "base_classes"
    return "base_classes"


def _class_module_name(nx_class: str) -> str:
    stem = nx_class[2:] if nx_class.startswith("NX") else nx_class
    return stem.lower()


def _section_fqn(nx_class: str) -> str:
    """Return the fully-qualified string proxy for a generated section."""
    module = _class_module_name(nx_class)
    class_name = nxdl_to_class_name(nx_class)
    category = _nxdl_category(nx_class)
    return f"pynxtools.nomad.metainfo.{category}.{module}.{class_name}"


# ---------------------------------------------------------------------------
# Build quantity context from a NexusEntity node
# ---------------------------------------------------------------------------


def _build_quantity_from_node(
    node: NexusEntity,
    parent_field: str | None = None,
    python_name_override: str | None = None,
) -> QuantityContext:
    """Build a QuantityContext from a NexusEntity (field or attribute).

    Only the few values that require a non-trivial transformation are stored
    on QuantityContext itself.  Everything else is accessed directly through
    the NexusEntity node.
    """
    python_name = python_name_override or nxdl_to_quantity_name(node.name)

    # dimensionality uses NXUnitSet which has no Jinja2 equivalent.
    # NX_TRANSFORMATION means any length/angle/dimensionless — map to NX_ANY.
    units = node.unit if node.unit != "NX_TRANSFORMATION" else "NX_ANY"
    dimensionality = _get_dimensionality(units)

    # shape needs tuple → list[int | "*"] conversion.
    shape = _shape_from_node(node)

    if node.items and not node.open_enum:
        python_type = f"MEnum({node.items!r})"
    else:
        python_type = nx_type_to_source(node.dtype)

    return QuantityContext(
        python_name=python_name,
        python_type=python_type,
        dimensionality=dimensionality,
        shape=shape,
        parent_field=parent_field,
        node=node,
    )


# ---------------------------------------------------------------------------
# Build subsection context from a NXTreeGroup node
# ---------------------------------------------------------------------------


def _build_subsection_from_node(node: NXTreeGroup) -> SubSectionContext:
    """Build a SubSectionContext from a NexusGroup (group) node.

    Only the few values that require a non-trivial transformation are stored
    on SubSectionContext itself.  Everything else is accessed through the node.
    """
    nx_name_type = node.name_type or "specified"
    _, max_occurs = node.occurrence_limits

    repeats: bool = (
        node.variadic
        or nx_name_type in ("any", "partial")
        or max_occurs is None
        or (isinstance(max_occurs, int) and max_occurs > 1)
    )

    if node.variadic or nx_name_type in ("any", "partial"):
        stem = (
            node.nx_class[2:].lower()
            if node.nx_class.startswith("NX")
            else node.nx_class.lower()
        )
        python_name = nxdl_to_subsection_name(stem)
        nx_name_literal = "None"
    else:
        python_name = nxdl_to_subsection_name(node.name)
        nx_name_literal = f'"{node.name}"'

    return SubSectionContext(
        python_name=python_name,
        section_fqn=_section_fqn(node.nx_class),
        repeats=repeats,
        nx_name_literal=nx_name_literal,
        node=node,
    )


# ---------------------------------------------------------------------------
# Build full template context for one NXDL class
# ---------------------------------------------------------------------------


def build_context(nx_name: str) -> dict:
    """Build the Jinja2 template context for a single NXDL base class.

    Uses build_base_class_node() as the single entry point into NexusNode.
    All NXDL attributes are read exclusively through NexusNode properties —
    no raw XML attribute access inside this function.
    """
    root_node = build_base_class_node(nx_name)

    nx_category = root_node.category
    is_base_class = nx_category == "base"

    class_name = nxdl_to_class_name(nx_name)
    base_class, base_import = get_base_section(nx_name)

    # Docstring: use get_docstring(depth=1) to read only from the primary
    # definition element (not parent classes).
    docs = root_node.get_docstring(depth=1)
    raw_doc = (next(iter(docs.values()), None) or "").strip()
    docstring = raw_doc or f"NOMAD metainfo class for NeXus {nx_name}."
    if len(docstring) > 500:
        docstring = docstring[:497] + "..."

    quantities: list[QuantityContext] = []
    subsections: list[SubSectionContext] = []
    seen_qty: set[str] = set()
    seen_ss: set[str] = set()

    for child in root_node.children:
        if child.nx_type == "attribute":
            qty = _build_quantity_from_node(child)
            if qty.python_name in seen_qty:
                continue
            seen_qty.add(qty.python_name)
            quantities.append(qty)

        elif child.nx_type == "field":
            qty = _build_quantity_from_node(child)
            if qty.python_name in seen_qty:
                continue
            seen_qty.add(qty.python_name)
            quantities.append(qty)

            # Field-level attribute sub-children pre-populated by build_base_class_node.
            for attr_child in child.children:
                if attr_child.nx_type != "attribute":
                    continue
                if not isinstance(attr_child, NexusEntity):
                    continue
                attr_key = (
                    f"{qty.python_name}__{nxdl_to_quantity_name(attr_child.name)}"
                )
                if attr_key in seen_qty:
                    continue
                seen_qty.add(attr_key)
                attr_qty = _build_quantity_from_node(
                    attr_child,
                    parent_field=qty.node.name,
                    python_name_override=attr_key,
                )
                quantities.append(attr_qty)

        elif child.nx_type == "group":
            ss = _build_subsection_from_node(child)
            if ss.python_name in seen_ss:
                # Two named groups with the same class — disambiguate by name.
                if not child.variadic:
                    ss.python_name = nxdl_to_subsection_name(
                        f"{child.name}_{child.nx_class[2:].lower()}"
                    )
                else:
                    continue
            seen_ss.add(ss.python_name)
            subsections.append(ss)
        # links and choices are skipped in Phase 1

    nx_optionality = "optional" if is_base_class else "required"
    needs_m_enum = any(q.python_type.startswith("MEnum") for q in quantities)

    return {
        "class_name": class_name,
        "nx_name": nx_name,
        "nx_category": nx_category,
        "nx_optionality": nx_optionality,
        "nx_deprecated": root_node.deprecated,
        "nx_restricts": root_node.restricts,
        "ignore_extra_groups": root_node.ignore_extra_groups,
        "ignore_extra_fields": root_node.ignore_extra_fields,
        "ignore_extra_attributes": root_node.ignore_extra_attributes,
        "nx_symbols": root_node.symbols,
        "base_class": base_class,
        "base_import": base_import,
        "docstring": docstring,
        "quantities": quantities,
        "subsections": subsections,
        "needs_m_enum": needs_m_enum,
    }


# ---------------------------------------------------------------------------
# Render and format
# ---------------------------------------------------------------------------


def render(context: dict) -> str:
    """Render the Jinja2 template and format with ruff."""
    template = _jinja_env.get_template("base_class.py.j2")
    raw = template.render(**context)
    try:
        result = subprocess.run(
            ["ruff", "format", "-"],
            input=raw,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except Exception:
        return raw


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


def write_base_class(
    nx_name: str,
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> bool:
    """Generate and write the Python file for one base class.

    Returns True if the file content changed (or was created), False if unchanged.
    In dry_run mode: returns True if the file would differ, raises nothing.

    output_dir defaults to the pynxtools-internal base_classes directory.
    Pass an explicit path to target a different package (e.g. nomad-measurements).
    """
    context = build_context(nx_name)
    new_source = render(context)

    module_name = _class_module_name(nx_name)
    dest = output_dir if output_dir is not None else _DEFAULT_OUTPUT_DIR
    out_path = dest / f"{module_name}.py"
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
            truly_new = new_members - existing_members
            if not truly_new:
                return False

    if dry_run:
        return True

    out_path.write_text(new_source, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Topological sort: generate files in dependency order
# ---------------------------------------------------------------------------


def _discover_base_classes() -> list[str]:
    defs = get_nexus_definitions_path()
    bc_dir = defs / "base_classes"
    return sorted(f.stem.replace(".nxdl", "") for f in bc_dir.glob("*.nxdl.xml"))


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


def generate_all_base_classes(
    dry_run: bool = False,
    force: bool = False,
    output_dir: Path | None = None,
) -> int:
    """Generate Python files for all NXDL base classes in dependency order.

    Returns the number of files written (dry_run: number that would change).

    output_dir defaults to the pynxtools-internal base_classes directory.
    Pass an explicit path to target a different package (e.g. nomad-measurements).
    """
    nx_names = _discover_base_classes()
    dep_graph = _build_dependency_graph(nx_names)
    ordered = toposort_flatten(dep_graph, sort=True)

    written = 0
    for nx_name in ordered:
        if nx_name not in dep_graph:
            continue
        try:
            changed = write_base_class(
                nx_name, dry_run=dry_run, force=force, output_dir=output_dir
            )
        except Exception as exc:
            print(f"  SKIP {nx_name}: {exc}")
            continue
        if changed:
            written += 1
    return written
