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

"""Unit tests for the NXDL -> metainfo converter."""

from types import SimpleNamespace

import pytest

import pynxtools.nomad.converters.nxdl_to_metainfo as converter
from pynxtools.nomad.converters._naming import _RESERVED_QUANTITY_NAMES


class FakeField:
    """Minimal field-like node for converter unit tests."""

    nx_type = "field"

    def __init__(
        self,
        name: str,
        dtype: str = "NX_CHAR",
        unit: str | None = None,
        shape=None,
        interpretation: str | None = None,
        long_name: str | None = None,
        items=None,
        open_enum: bool = False,
        optionality: bool = False,
        children=None,
        nxdl_base: str = "NXtest.nxdl.xml",
        doc: str = "",
    ):
        self.name = name
        self.dtype = dtype
        self.unit = unit
        self.shape = shape
        self.interpretation = interpretation
        self.long_name = long_name
        self.items = items
        self.open_enum = open_enum
        self.optionality = optionality
        self.children = children or []
        self.nxdl_base = nxdl_base
        self._doc = doc

    def get_docstring(self, depth=1):
        _ = depth
        return {"en": self._doc}


class FakeAttribute:
    """Minimal attribute-like node for converter unit tests."""

    nx_type = "attribute"

    def __init__(
        self,
        name: str,
        dtype: str = "NX_CHAR",
        shape=None,
        items=None,
        open_enum: bool = False,
        optionality: bool = False,
        nxdl_base: str = "NXtest.nxdl.xml",
        doc: str = "",
    ):
        self.name = name
        self.dtype = dtype
        self.shape = shape
        self.items = items
        self.open_enum = open_enum
        self.optionality = optionality
        self.nxdl_base = nxdl_base
        self._doc = doc

    def get_docstring(self, depth=1):
        _ = depth
        return {"en": self._doc}


class FakeGroup:
    """Minimal group-like node for converter unit tests."""

    nx_type = "group"

    def __init__(
        self,
        name: str,
        nx_class: str,
        name_type: str = "specified",
        variadic: bool = False,
        children=None,
        nxdl_base: str = "NXentry.nxdl.xml",
        doc: str = "",
    ):
        self.name = name
        self.nx_class = nx_class
        self.name_type = name_type
        self.variadic = variadic
        self.children = children or []
        self.nxdl_base = nxdl_base
        self._doc = doc

    def get_docstring(self, depth=1):
        _ = depth
        return {"en": self._doc}


def _patch_fake_node_types(monkeypatch):
    """Route converter runtime type checks to local fake node classes."""
    monkeypatch.setattr(converter, "NexusField", FakeField)
    monkeypatch.setattr(converter, "NexusAttribute", FakeAttribute)
    monkeypatch.setattr(converter, "NXTreeGroup", FakeGroup)


def test_shape_from_node_replaces_none_with_wildcard():
    """Ensure symbolic or unbounded shape dimensions are rendered as wildcard."""
    node = FakeField(name="signal", shape=(2, None, 5))

    shape_from_node = getattr(converter, "_shape_from_node")
    assert shape_from_node(node) == [2, "*", 5]


def test_build_quantity_from_field_maps_transformation_unit(monkeypatch):
    """Verify field quantities keep unit semantics and enum/type conversions."""
    _patch_fake_node_types(monkeypatch)
    monkeypatch.setattr(converter.NXUnitSet, "get_dimensionality", lambda unit: "[]")

    node = FakeField(
        name="value",
        dtype="NX_CHAR",
        unit="NX_TRANSFORMATION",
        shape=(None,),
        items=["a", "b"],
        open_enum=False,
    )

    build_quantity_from_node = getattr(converter, "_build_quantity_from_node")
    qty = build_quantity_from_node(node)

    assert qty.unit == "NX_ANY"
    assert qty.dimensionality == "[]"
    assert qty.shape == ["*"]
    assert qty.python_type == "MEnum(['a', 'b'])"
    assert qty.scalar_items == ["a", "b"]


def test_build_quantity_from_attribute_uses_dtype_mapping(monkeypatch):
    """Verify attribute quantities skip field-only metadata and map dtype."""
    _patch_fake_node_types(monkeypatch)

    node = FakeAttribute(name="status", dtype="NX_BOOLEAN", shape=(None, 1))

    build_quantity_from_node = getattr(converter, "_build_quantity_from_node")
    qty = build_quantity_from_node(node, parent_field="signal")

    assert qty.parent_field == "signal"
    assert qty.unit is None
    assert qty.dimensionality is None
    assert qty.shape == ["*", 1]
    assert qty.python_type == converter.nx_type_to_source("NX_BOOLEAN")


@pytest.mark.parametrize(
    "name_type, variadic, expected_name, expected_literal, expected_variable",
    [
        (
            "specified",
            False,
            converter.nxdl_to_subsection_name("ENTRY"),
            '"ENTRY"',
            False,
        ),
        (
            "partial",
            False,
            converter.nxdl_to_subsection_name("peakPEAK"),
            '"peakPEAK"',
            True,
        ),
        ("any", True, "detector", "None", True),
    ],
)
def test_build_subsection_from_node_by_name_type(
    monkeypatch,
    name_type,
    variadic,
    expected_name,
    expected_literal,
    expected_variable,
):
    """Validate subsection naming and flags for specified, partial, and any groups."""
    _patch_fake_node_types(monkeypatch)
    node = FakeGroup(
        name="ENTRY" if name_type == "specified" else "peakPEAK",
        nx_class="NXdetector",
        name_type=name_type,
        variadic=variadic,
    )

    build_subsection_from_node = getattr(converter, "_build_subsection_from_node")
    section = build_subsection_from_node(
        node,
        section_fqn="pynxtools.nomad.metainfo.base_classes.detector.Detector",
    )

    assert section.python_name == expected_name
    assert section.nx_name_literal == expected_literal
    assert section.variable is expected_variable
    assert section.repeats is variadic


def test_base_from_extends_for_direct_child_with_nomad_base():
    """Check inheritance tuple for direct NXobject children with NOMAD semantic base."""
    root = SimpleNamespace(
        inheritance=[SimpleNamespace(attrib={"extends": "NXobject"})]
    )

    base_from_extends = getattr(converter, "_base_from_extends")
    nomad_base_for_nx_class = getattr(converter, "_nomad_base_for_nx_class")

    base = base_from_extends("NXentry", root)
    expected_nomad_cls, expected_nomad_mod = nomad_base_for_nx_class("NXentry")

    assert base == (
        "Object",
        "pynxtools.nomad.metainfo.base_classes.object",
        True,
        expected_nomad_cls,
        expected_nomad_mod,
    )


def test_build_context_renames_field_when_parent_subsection_conflicts(monkeypatch):
    """Ensure conflict_concept is suffixed for both direct and concept-level conflicts.

        This covers two related runtime rename cases in one build_context call:
    - the current class defines a field whose name already exists as an ancestor
      subsection, so the field becomes ``conflict_concept_field``
    - the current class also defines a named concept group ``conflict_concept``
      whose own field has the same name, and that concept's ancestor chain also
      exposes ``conflict_concept`` as a subsection, so the concept field is
      also renamed with ``_field``

        The pre-computation path in ``_ensure_conflicts_precomputed`` is exercised in
        a separate test below. Here the scan is skipped via state flag so the
        assertions stay focused on build-time rename behavior driven by ancestor
        subsection names.
    """
    _patch_fake_node_types(monkeypatch)

    attr = FakeAttribute(name="units", dtype="NX_CHAR")
    field = FakeField(
        name="conflict_concept",
        dtype="NX_FLOAT",
        children=[attr],
    )
    concept_field = FakeField(name="conflict_concept", dtype="NX_FLOAT")
    nested_conflict_group = FakeGroup(
        name="conflict_concept",
        nx_class="NXconflict_leaf",
    )
    current_group = FakeGroup(
        name="conflict_concept",
        nx_class="NXconflict_parent",
        children=[concept_field, nested_conflict_group],
    )

    root = SimpleNamespace(
        category="base",
        deprecated=False,
        ignore_extra_groups=False,
        ignore_extra_fields=False,
        ignore_extra_attributes=False,
        symbols=[],
        inheritance=[SimpleNamespace(attrib={"extends": "NXancestor"})],
        nxdl_base="NXentry.nxdl.xml",
        children=[field, current_group],
        get_docstring=lambda depth=1: {"en": "Doc."},
    )

    monkeypatch.setattr(converter, "_conflicts_precomputed", True)
    monkeypatch.setattr(converter, "generate_tree_from", lambda _: root)
    monkeypatch.setattr(converter, "_base_class_quantities", lambda _: {})
    monkeypatch.setattr(converter, "_nxdl_category", lambda _: "base_classes")
    monkeypatch.setattr(
        converter,
        "_base_from_extends",
        lambda *_: (
            "Object",
            "pynxtools.nomad.metainfo.base_classes.object",
            True,
            "",
            "",
        ),
    )
    monkeypatch.setattr(
        converter,
        "_all_ancestor_member_names",
        lambda nx_name: (
            (frozenset(), frozenset({"conflict_concept"}))
            if nx_name in {"NXancestor", "NXconflict_parent"}
            else (frozenset(), frozenset())
        ),
    )
    monkeypatch.setattr(converter, "_qty_field_suffix_for", {})

    context = converter.build_context("NXentry")
    names = [q.python_name for q in context["quantities"]]
    concept_qty_names = [
        quantity.python_name for quantity in context["named_concepts"][0].quantities
    ]

    assert names == ["conflict_concept_field", "conflict_concept_field__units"]
    assert context["subsections"][0].python_name == "conflict_concept"
    assert concept_qty_names == ["conflict_concept_field"]


def test_ensure_conflicts_precomputed_marks_ancestor_field_for_group_conflict(
    monkeypatch,
):
    """Ensure pre-computation records `_field` suffixes for ancestor field conflicts.

    This test exercises the dedicated conflict scan used before build_context.
    The setup models a multi-level inheritance chain where:
    - ``NXancestor`` defines a field named ``conflict_concept``
    - ``NXentry`` extends ``NXparent``
    - ``NXentry`` defines a group named ``conflict_concept``

    The scan should therefore mark the ancestor field name for suffixing in
    ``converter._qty_field_suffix_for['NXancestor']`` and yield the effective
    suffixed quantity name ``conflict_concept_field``.
    """
    _patch_fake_node_types(monkeypatch)

    monkeypatch.setattr(converter, "_conflicts_precomputed", False)
    monkeypatch.setattr(converter, "_qty_field_suffix_for", {})
    monkeypatch.setattr(
        converter,
        "_discover_base_classes",
        lambda: ["NXancestor", "NXparent", "NXentry"],
    )
    monkeypatch.setattr(
        converter,
        "_nx_extends",
        lambda nx_name: {
            "NXentry": "NXparent",
            "NXparent": "NXancestor",
            "NXancestor": "NXobject",
            "NXobject": "NXobject",
        }.get(nx_name, "NXobject"),
    )

    roots = {
        "NXancestor": SimpleNamespace(
            nxdl_base="NXancestor.nxdl.xml",
            children=[
                FakeField(
                    name="conflict_concept",
                    dtype="NX_FLOAT",
                    nxdl_base="NXancestor.nxdl.xml",
                )
            ],
        ),
        "NXparent": SimpleNamespace(
            nxdl_base="NXparent.nxdl.xml",
            children=[],
        ),
        "NXentry": SimpleNamespace(
            nxdl_base="NXentry.nxdl.xml",
            children=[
                FakeGroup(
                    name="conflict_concept",
                    nx_class="NXconflict_parent",
                    nxdl_base="NXentry.nxdl.xml",
                    children=[
                        FakeGroup(
                            name="conflict_concept",
                            nx_class="NXconflict_leaf",
                            nxdl_base="NXentry.nxdl.xml",
                        )
                    ],
                )
            ],
        ),
        "NXobject": SimpleNamespace(nxdl_base="NXobject.nxdl.xml", children=[]),
    }
    monkeypatch.setattr(converter, "generate_tree_from", lambda nx_name: roots[nx_name])

    ensure_conflicts_precomputed = getattr(converter, "_ensure_conflicts_precomputed")
    qty_field_suffix_for = getattr(converter, "_qty_field_suffix_for")

    ensure_conflicts_precomputed()

    ancestor = roots["NXancestor"]
    assert f"{ancestor.children[0].name}_field" == "conflict_concept_field"

    assert qty_field_suffix_for["NXancestor"] == frozenset({"conflict_concept"})


@pytest.mark.parametrize("reserved_name", sorted(_RESERVED_QUANTITY_NAMES))
def test_build_context_reserved_quantity_names_are_suffixed(monkeypatch, reserved_name):
    """Ensure reserved quantity names are rewritten with `_field` in build output.

    For each reserved name from naming rules, this checks both:
    - the field quantity name itself
    - the derived field-attribute quantity name
    """
    _patch_fake_node_types(monkeypatch)

    field_units_attr = FakeAttribute(name="units", dtype="NX_CHAR")
    reserved_field = FakeField(
        name=reserved_name,
        dtype="NX_FLOAT",
        children=[field_units_attr],
    )

    root = SimpleNamespace(
        category="base",
        deprecated=False,
        ignore_extra_groups=False,
        ignore_extra_fields=False,
        ignore_extra_attributes=False,
        symbols=[],
        inheritance=[SimpleNamespace(attrib={"extends": "NXobject"})],
        nxdl_base="NXentry.nxdl.xml",
        children=[reserved_field],
        get_docstring=lambda depth=1: {"en": "Doc."},
    )

    monkeypatch.setattr(converter, "_conflicts_precomputed", True)
    monkeypatch.setattr(converter, "generate_tree_from", lambda _: root)
    monkeypatch.setattr(
        converter,
        "_base_from_extends",
        lambda *_: (
            "Object",
            "pynxtools.nomad.metainfo.base_classes.object",
            True,
            "",
            "",
        ),
    )
    monkeypatch.setattr(
        converter,
        "_all_ancestor_member_names",
        lambda _: (frozenset(), frozenset()),
    )
    monkeypatch.setattr(converter, "_qty_field_suffix_for", {})

    context = converter.build_context("NXentry")
    quantity_names = [q.python_name for q in context["quantities"]]
    expected_base = f"{reserved_name}_field"

    assert quantity_names == [expected_base, f"{expected_base}__units"]


def test_write_base_class_dry_run_detects_content_change(monkeypatch, tmp_path):
    """Dry-run should report changes without touching existing files."""
    out_dir = tmp_path / "base_classes"
    out_dir.mkdir(parents=True)
    existing = out_dir / "entry.py"
    existing.write_text("old content\n", encoding="utf-8")

    monkeypatch.setattr(converter, "build_context", lambda _: {"class_name": "Entry"})
    monkeypatch.setattr(converter, "render", lambda _: "new content\n")

    changed = converter.write_base_class(
        "NXentry", dry_run=True, force=False, output_dir=out_dir
    )

    assert changed is True


def test_generate_all_base_classes_counts_only_changed(monkeypatch, tmp_path):
    """Generation count should include only classes reported as changed."""
    monkeypatch.setattr(converter, "_discover_base_classes", lambda: ["NXa", "NXb"])
    monkeypatch.setattr(
        converter,
        "_build_dependency_graph",
        lambda _: {"NXa": set(), "NXb": {"NXa"}},
    )

    changes = {"NXa": False, "NXb": True}

    def fake_write(nx_name, dry_run=False, force=False, output_dir=None):
        _ = (dry_run, force, output_dir)
        return changes[nx_name]

    monkeypatch.setattr(converter, "write_base_class", fake_write)

    written = converter.generate_all_base_classes(output_dir=tmp_path)

    assert written == 1
