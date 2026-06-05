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

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

import pynxtools.nomad.converters.nxdl_to_metainfo as converter
from pynxtools.nexus.nexus_tree import (
    NexusAttribute,
    NexusField,
    NexusGroup,
    generate_tree_from,
)


def _class_members(source: str) -> dict[str, dict[str, str]]:
    """Return {class_name: {member_name: constructor}} for every class in source.

    Only ``Quantity`` and ``SubSection`` assignments are collected; ``m_def``
    (a ``Section`` call) is excluded because its content differs structurally
    between the main class and named-concept sub-classes and is not the subject
    of section-by-section field/group comparison.
    """
    result: dict[str, dict[str, str]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            members: dict[str, str] = {}
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for tgt in item.targets:
                        if isinstance(tgt, ast.Name) and tgt.id != "m_def":
                            call = item.value
                            if isinstance(call, ast.Call):
                                fn = call.func
                                if isinstance(fn, ast.Name):
                                    kind = fn.id
                                elif isinstance(fn, ast.Attribute):
                                    kind = fn.attr
                                else:
                                    continue
                                members[tgt.id] = kind
            result[node.name] = members
    return result


def _class_bases(source: str) -> dict[str, list[str]]:
    """Return {class_name: [base, ...]} for every class in source."""
    result: dict[str, list[str]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute) and isinstance(
                    base.value, ast.Name
                ):
                    bases.append(f"{base.value.id}.{base.attr}")
            result[node.name] = bases
    return result


_GOLDEN_DIR = (
    Path(__file__).parents[2]
    / "src"
    / "pynxtools"
    / "nomad"
    / "metainfo"
    / "base_classes"
)

# Golden files generated from controlled fixture NXDLs (NXtestBase, NXtest,
# NXtest_extended) — independent of the live NeXus definitions repo.
_CONVERTER_GOLDEN_DIR = Path(__file__).parent.parent / "data" / "nomad" / "converter"


def test_build_quantity_from_field_maps_transformation_unit(monkeypatch):
    """Verify field quantities keep unit semantics and enum/type conversions."""
    # NXUnitSet.get_dimensionality requires the full NOMAD unit database at runtime.
    # The lambda isolates this test from that external dependency.
    monkeypatch.setattr(converter.NXUnitSet, "get_dimensionality", lambda unit: "[]")

    node = NexusField(name="value")
    node.dtype = "NX_CHAR"
    node.unit = "NX_TRANSFORMATION"
    node.shape = (None,)
    node.items = ["a", "b"]
    node.open_enum = False

    build_quantity_from_node = getattr(converter, "_build_quantity_from_node")
    qty = build_quantity_from_node(node)

    assert qty.unit == "NX_ANY"
    assert qty.dimensionality == "[]"
    assert qty.shape == ["*"]
    assert qty.python_type == "MEnum(['a', 'b'])"
    assert qty.scalar_items == ["a", "b"]


def test_build_quantity_from_attribute_uses_dtype_mapping():
    """Verify attribute quantities skip field-only metadata and map dtype."""
    node = NexusAttribute(name="status")
    node.dtype = "NX_BOOLEAN"
    node.shape = (None, 1)  # multi-dim: exercises (None, 1) → ["*", 1] conversion

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
        # name_type="any": python_name is derived from nx_class ("NXdetector" → "detector"),
        # not from the element name — the element name is irrelevant for variadic groups.
        ("any", True, "detector", "None", True),
    ],
)
def test_build_subsection_from_node_by_name_type(
    name_type,
    variadic,
    expected_name,
    expected_literal,
    expected_variable,
):
    """Validate subsection naming and flags for specified, partial, and any groups."""
    node = NexusGroup(
        nx_class="NXdetector",
        name="ENTRY" if name_type == "specified" else "peakPEAK",
        nx_type="group",
        name_type=name_type,
        variadic=variadic,
    )

    build_subsection_from_node = getattr(converter, "_build_subsection_from_node")
    # section_fqn is stored as a plain string and never validated against the NXDL
    # definitions — any FQN works, so we use a mock to avoid coupling to real classes.
    section = build_subsection_from_node(
        node,
        section_fqn="test.module.TestSection",
    )

    assert section.python_name == expected_name
    assert section.nx_name_literal == expected_literal
    assert section.variable is expected_variable
    assert section.repeats is variadic


def test_base_from_extends_for_direct_child_with_nomad_base():
    """Check inheritance tuple for direct NXobject children with NOMAD semantic base.

    Uses a real ``NexusDefinition`` from ``generate_tree_from("NXentry")`` so the
    XML inheritance chain is exercised without any mocking.
    """
    root = generate_tree_from("NXentry")

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
    attr = NexusAttribute(name="units")
    attr.dtype = "NX_CHAR"
    field = NexusField(name="conflict_concept")
    field.dtype = "NX_FLOAT"
    attr.parent = field

    concept_field = NexusField(name="conflict_concept")
    concept_field.dtype = "NX_FLOAT"
    current_group = NexusGroup(
        nx_class="NXconflict_parent",
        name="conflict_concept",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    # nested_conflict_group makes current_group a named concept (groups with only
    # fields but no child groups would be inlined; a child group triggers concept
    # class generation, which is the path under test).
    nested_conflict_group = NexusGroup(
        nx_class="NXconflict_leaf",
        name="conflict_concept",
        nx_type="group",
    )
    concept_field.parent = current_group
    nested_conflict_group.parent = current_group

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
    """Ensure pre-computation records ``_field`` suffixes for ancestor field conflicts.

    The setup models a multi-level inheritance chain where:
    - ``NXancestor`` defines a field named ``conflict_concept``
    - ``NXentry`` extends ``NXparent``
    - ``NXentry`` defines a group named ``conflict_concept``

    The scan should therefore mark the ancestor field name for suffixing in
    ``converter._qty_field_suffix_for['NXancestor']`` and yield the effective
    suffixed quantity name ``conflict_concept_field``.
    """
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

    ancestor_field = NexusField(
        name="conflict_concept", nxdl_base="NXancestor.nxdl.xml"
    )
    ancestor_field.dtype = "NX_FLOAT"

    leaf_group = NexusGroup(
        nx_class="NXconflict_leaf",
        name="conflict_concept",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    parent_group = NexusGroup(
        nx_class="NXconflict_parent",
        name="conflict_concept",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    leaf_group.parent = parent_group

    roots = {
        "NXancestor": SimpleNamespace(
            nxdl_base="NXancestor.nxdl.xml",
            children=[ancestor_field],
        ),
        "NXparent": SimpleNamespace(
            nxdl_base="NXparent.nxdl.xml",
            children=[],
        ),
        "NXentry": SimpleNamespace(
            nxdl_base="NXentry.nxdl.xml",
            children=[parent_group],
        ),
        "NXobject": SimpleNamespace(nxdl_base="NXobject.nxdl.xml", children=[]),
    }
    monkeypatch.setattr(converter, "generate_tree_from", lambda nx_name: roots[nx_name])

    ensure_conflicts_precomputed = getattr(converter, "_ensure_conflicts_precomputed")
    qty_field_suffix_for = getattr(converter, "_qty_field_suffix_for")

    ensure_conflicts_precomputed()

    ancestor = roots["NXancestor"]
    # The function records the rename in _qty_field_suffix_for without modifying
    # the NexusField node itself; the node name stays "conflict_concept".
    assert ancestor.children[0].name == "conflict_concept"
    assert qty_field_suffix_for["NXancestor"] == frozenset({"conflict_concept"})


@pytest.mark.parametrize("reserved_name", ("name", "lab_id", "description"))
def test_build_context_reserved_quantity_names_are_suffixed(monkeypatch, reserved_name):
    """Ensure reserved quantity names are rewritten with ``_field`` in build output.

    Covers the NX_CHAR-typed names in ``_RESERVED_QUANTITY_NAMES`` (name, lab_id,
    description) which shadow ``BaseSection`` attributes and must be suffixed to
    avoid silently overriding them.  ``datetime`` uses a different dtype and is
    not included here.
    """
    reserved_field = NexusField(name=reserved_name)
    reserved_field.dtype = "NX_CHAR"

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

    assert quantity_names == [expected_base]


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


# ---------------------------------------------------------------------------
# Full-pipeline integration tests (controlled NXtestBase fixture → Python source)
# ---------------------------------------------------------------------------


def test_write_base_class_nxtestbase_full_pipeline(tmp_path):
    """Full-pipeline: NXtestBase generates valid Python covering key converter features.

    NXtestBase (src/pynxtools/data/NXtestBase.nxdl.xml) is a controlled fixture that
    covers: NX_CHAR, NX_FLOAT with units, NX_INT, NX_BOOLEAN, closed enum, group
    reference, and group-level attribute.  Using a fixture NXDL keeps this test
    independent of live NeXus definition changes while still exercising the full
    generate_tree_from → build_context → render → write pipeline.
    """
    converter.write_base_class("NXtestBase", output_dir=tmp_path, force=True)
    source = (tmp_path / "testbase.py").read_text(encoding="utf-8")

    assert "class Testbase(Object):" in source
    assert 'nx_class="NXtestBase"' in source
    assert "label = Quantity(" in source
    assert "energy = Quantity(" in source
    assert "count = Quantity(" in source
    assert "flag = Quantity(" in source
    assert "mode = Quantity(" in source
    assert "data = SubSection(" in source
    assert "version = Quantity(" in source
    compile(source, "testbase.py", "exec")


def test_write_base_class_nxtestbase_matches_golden():
    """Generated NXtestBase output must be byte-identical to the stored golden file.

    The golden file lives in tests/data/nomad/converter/testbase.py and was produced
    by running the converter against NXtestBase.nxdl.xml.  A failure here means the
    converter template or NXtestBase.nxdl.xml changed without regenerating the golden
    file.  Fix by running::

        python -c "
        import pynxtools.nomad.converters.nxdl_to_metainfo as c
        open('tests/data/nomad/converter/testbase.py','w').write(c.render(c.build_context('NXtestBase')))
        "
    """
    golden = (_CONVERTER_GOLDEN_DIR / "testbase.py").read_text(encoding="utf-8")
    generated = converter.render(converter.build_context("NXtestBase"))
    assert generated == golden


@pytest.mark.parametrize(
    "nx_class, module_name",
    [
        ("NXobject", "object"),
        ("NXdata", "data"),
        ("NXentry", "entry"),
        ("NXsample", "sample"),
    ],
)
def test_committed_base_class_matches_generator(nx_class, module_name):
    """Committed Python metainfo file must be identical to what the generator produces.

    A failure here means the NXDL definition or the Jinja2 template changed but
    the corresponding ``.py`` file in ``src/pynxtools/nomad/metainfo/base_classes/``
    was not regenerated. Fix by running::

        pynx nomad generate-metainfo --nx-class <NX_CLASS>
    """
    golden = (_GOLDEN_DIR / f"{module_name}.py").read_text(encoding="utf-8")
    generated = converter.render(converter.build_context(nx_class))
    assert generated == golden


# ---------------------------------------------------------------------------
# NXtest / NXtest_extended: full-pipeline section-by-section golden tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "nx_class, golden_file",
    [
        ("NXtest", "test.py"),
        ("NXtest_extended", "test_extended.py"),
    ],
)
def test_nxtest_fixture_sections_match_golden(nx_class, golden_file):
    """Generated classes from NXtest fixtures match the stored golden section structure.

    Compares class inheritance and member names/kinds (Quantity, SubSection) for
    every class in the generated file against the golden stored in
    tests/data/nomad/converter/.  The comparison is structural — formatting,
    docstring text, and annotation keyword ordering do not affect the result.
    NXtest and NXtest_extended are application definitions used here as controlled
    fixtures; they cover the full converter path including named concept groups,
    inheritance from base classes, and multi-class output files.

    A failure here means the NXtest*.nxdl.xml fixture or the Jinja2 template
    changed without regenerating the golden.  Fix by running::

        python -c "
        import pynxtools.nomad.converters.nxdl_to_metainfo as c
        open('tests/data/nomad/converter/<golden_file>', 'w').write(
            c.render(c.build_context('<nx_class>'))
        )
        "
    """
    golden = (_CONVERTER_GOLDEN_DIR / golden_file).read_text(encoding="utf-8")
    generated = converter.render(converter.build_context(nx_class))

    assert _class_bases(generated) == _class_bases(golden), (
        f"{nx_class}: class inheritance mismatch"
    )
    assert _class_members(generated) == _class_members(golden), (
        f"{nx_class}: class member mismatch (name or Quantity/SubSection kind changed)"
    )
