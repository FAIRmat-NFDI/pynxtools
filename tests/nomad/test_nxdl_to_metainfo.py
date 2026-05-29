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


def test_build_quantity_from_field_maps_length_unit(monkeypatch):
    """Verify field quantities keep unit semantics and enum/type conversions."""
    _patch_fake_node_types(monkeypatch)
    monkeypatch.setattr(converter.NXUnitSet, "get_dimensionality", lambda unit: "[]")

    node = FakeField(
        name="value",
        dtype="NX_CHAR",
        unit="NX_LENGTH",
        shape=(None,),
        items=["a", "b"],
        open_enum=False,
    )

    build_quantity_from_node = getattr(converter, "_build_quantity_from_node")
    qty = build_quantity_from_node(node)

    assert qty.unit == "NX_LENGTH"
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
    """Ensure quantity names are suffixed when an ancestor subsection uses the same name."""
    _patch_fake_node_types(monkeypatch)

    attr = FakeAttribute(name="units", dtype="NX_CHAR")
    field = FakeField(name="signal", dtype="NX_FLOAT", children=[attr])

    root = SimpleNamespace(
        category="base",
        deprecated=False,
        ignore_extra_groups=False,
        ignore_extra_fields=False,
        ignore_extra_attributes=False,
        symbols=[],
        inheritance=[SimpleNamespace(attrib={"extends": "NXobject"})],
        nxdl_base="NXentry",
        children=[field],
        get_docstring=lambda depth=1: {"en": "Doc."},
    )

    monkeypatch.setattr(converter, "_ensure_conflicts_precomputed", lambda: None)
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
        lambda _: (frozenset(), frozenset({"signal"})),
    )
    monkeypatch.setattr(converter, "_qty_field_suffix_for", {})

    context = converter.build_context("NXentry")
    names = [q.python_name for q in context["quantities"]]

    assert names == ["signal_field", "signal_field__units"]


@pytest.mark.parametrize("reserved_name", sorted(_RESERVED_QUANTITY_NAMES))
def test_build_context_reserved_quantity_names_are_suffixed(monkeypatch, reserved_name):
    """Ensure all reserved names from naming rules are emitted with _field suffix."""
    _patch_fake_node_types(monkeypatch)

    attr = FakeAttribute(name="units", dtype="NX_CHAR")
    field = FakeField(name=reserved_name, dtype="NX_FLOAT", children=[attr])

    root = SimpleNamespace(
        category="base",
        deprecated=False,
        ignore_extra_groups=False,
        ignore_extra_fields=False,
        ignore_extra_attributes=False,
        symbols=[],
        inheritance=[SimpleNamespace(attrib={"extends": "NXobject"})],
        nxdl_base="NXentry.nxdl.xml",
        children=[field],
        get_docstring=lambda depth=1: {"en": "Doc."},
    )

    monkeypatch.setattr(converter, "_ensure_conflicts_precomputed", lambda: None)
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
    names = [q.python_name for q in context["quantities"]]

    assert names == [f"{reserved_name}_field", f"{reserved_name}_field__units"]


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
