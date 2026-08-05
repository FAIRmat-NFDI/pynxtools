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

"""Tests for the NXDL -> NOMAD metainfo converter.

Goal
    Pin the converter's transformation rules: how an NXDL node becomes a
    ``Quantity`` or ``SubSection``, how names are resolved when they collide,
    and how a whole NXDL renders to Python source.

Flow
    Two layers, in file order.

    1. Unit tests on single converter functions — ``_build_quantity_from_node``,
       ``_build_subsection_from_node``, ``_base_from_extends``,
       ``build_context``, ``write_base_class``, ``generate_all_base_classes``.
       Input nodes are constructed directly rather than parsed.
    2. Golden tests that render the fixture NXDLs end to end and compare the
       result against stored output.

Dependencies
    - Fixture NXDLs in ``src/pynxtools/data/``: ``NXtestBase``, ``NXtest``,
      ``NXtest_extended``. The golden tests reach the live NeXus definitions
      only through these, so upstream definition changes cannot break them.
    - Golden files in ``tests/data/nomad/converter/``. Its ``conftest.py`` sets
      ``collect_ignore_glob`` because ``test.py`` and ``test_extended.py`` match
      pytest's discovery pattern but are reference data, not tests.
    - No test depends on another. Each builds its own input and asserts on its
      own output, so they can run in any order or alone.

Regenerating the golden files
    Needed when a fixture NXDL or the Jinja2 template changes. Run from the
    repository root::

        python - <<'EOF'
        import pathlib
        import pynxtools.nomad.converters.nxdl_to_metainfo as c

        repo = str(pathlib.Path.cwd()) + "/"
        for nx, fname in (
            ("NXtestBase", "testbase.py"),
            ("NXtest", "test.py"),
            ("NXtest_extended", "test_extended.py"),
        ):
            src = c.render(c.build_context(nx))
            # The fixtures resolve through _NXDL_SPECIAL_NAMES to absolute paths.
            # Without this replace, the generating machine's layout ends up in
            # the doc links stored in the golden.
            pathlib.Path("tests/data/nomad/converter", fname).write_text(
                src.replace(repo, ""), encoding="utf-8"
            )
        EOF

    Review the resulting diff before committing: a structural change there is
    exactly what the golden tests exist to make visible.
"""

import ast
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import pynxtools.nomad.converters.nxdl_to_metainfo as converter
from pynxtools.nexus.nexus_tree import (
    NexusAttribute,
    NexusDefinition,
    NexusField,
    NexusGroup,
    generate_tree_from,
)
from pynxtools.nomad.converters._mapping import _BASESECTION_RESERVED_NAMES

_NX_NS = "http://definition.nexusformat.org/nxdl/3.1"


def _make_definition(
    nx_name: str,
    *,
    extends: str = "NXobject",
    doc: str = "",
) -> NexusDefinition:
    """Build a minimal NexusDefinition for testing without parsing NXDL files.

    Creates a bare ``<definition>`` XML element with the given ``extends`` and
    optional ``<doc>`` text, then wraps it in a real ``NexusDefinition`` so that
    ``_set_definition_attrs()``, ``get_docstring()``, and ``get_link()`` all work
    without any additional mocking.  Children are attached afterward via the
    standard anytree pattern: ``child.parent = root``.
    """
    elem = ET.Element(f"{_NX_NS}definition")
    elem.attrib["name"] = nx_name
    elem.attrib["category"] = "base"
    elem.attrib["extends"] = extends
    if doc:
        ET.SubElement(elem, f"{{{_NX_NS}}}doc").text = doc
    return NexusDefinition(
        name=nx_name,
        nxdl_base=f"{nx_name}.nxdl.xml",
        inheritance=[elem],
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


# Golden files generated from the fixture NXDLs (NXtestBase, NXtest,
# NXtest_extended) — independent of the live NeXus definitions repo.
_CONVERTER_GOLDEN_DIR = Path(__file__).parent.parent / "data" / "nomad" / "converter"


def test_build_quantity_from_field_maps_transformation_unit(monkeypatch):
    """Field nodes carry unit, shape and enum semantics onto a QuantityContext.

    ``NX_TRANSFORMATION`` collapses to ``NX_ANY`` and a closed enum becomes
    ``MEnum``; both reach the template verbatim, so a wrong mapping corrupts
    every generated Quantity silently.
    """
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
    """Attribute nodes keep the parent-field link and carry no unit metadata.

    Attributes have no NXDL unit, so ``unit`` and ``dimensionality`` must stay
    None while ``shape`` still converts ``(None, 1)`` to ``["*", 1]``.
    """
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
    "node_name, name_type, variadic, expected_name, expected_literal, expected_variable",
    [
        (
            "ENTRY",
            "specified",
            False,
            converter.nxdl_to_subsection_name("ENTRY"),
            '"ENTRY"',
            False,
        ),
        (
            "peakPEAK",
            "partial",
            False,
            converter.nxdl_to_subsection_name("peakPEAK"),
            '"peakPEAK"',
            True,
        ),
        # An anonymous nameType="any" group carries no name= in the NXDL, so
        # NexusNode fills node.name with the uppercase class stem ("DETECTOR").
        # python_name lowercases it and nx_name_literal stays None, recording
        # that NXDL declared no name.
        ("DETECTOR", "any", True, "detector", "None", True),
    ],
)
def test_build_subsection_from_node_by_name_type(
    node_name,
    name_type,
    variadic,
    expected_name,
    expected_literal,
    expected_variable,
):
    """SubSection naming and flags follow the group's nameType.

    ``specified`` keeps a fixed name; ``partial`` stays variable with the NXDL
    literal preserved; ``any`` lowercases the class stem and leaves
    ``nx_name_literal`` None, recording that NXDL declared no name at all.
    ``repeats`` tracks variadic independently of naming.
    """
    node = NexusGroup(
        nx_class="NXdetector",
        name=node_name,
        nx_type="group",
        name_type=name_type,
        variadic=variadic,
    )

    build_subsection_from_node = getattr(converter, "_build_subsection_from_node")
    # section_fqn is stored verbatim and resolved lazily by NOMAD at
    # __init_metainfo__() time, so any dotted string works here.
    section = build_subsection_from_node(
        node,
        section_fqn="test.module.TestSection",
    )

    assert section.python_name == expected_name
    assert section.nx_name_literal == expected_literal
    assert section.variable is expected_variable
    assert section.repeats is variadic


def test_base_from_extends_for_direct_child_with_nomad_base():
    """A direct NXobject child gets generated ``Object`` plus its NOMAD semantic bases.

    Runs on the real ``NXentry`` tree, so the XML inheritance chain is exercised
    unmocked and the expected NOMAD bases are read from ``BASESECTIONS_MAP``
    rather than hard-coded.
    """
    root = generate_tree_from("NXentry")

    base_from_extends = getattr(converter, "_base_from_extends")
    nomad_base_for_nx_class = getattr(converter, "_nomad_base_for_nx_class")

    base = base_from_extends("NXentry", root)
    expected_nomad_fqns = nomad_base_for_nx_class("NXentry")

    assert base == (
        "Object",
        "pynxtools.nomad.metainfo.base_classes.object",
        True,
        expected_nomad_fqns,
    )


def _patch_isolated_build_context(monkeypatch, root, ancestor_members):
    """Point build_context at ``root`` with a fixed ancestor member set.

    ``build_context`` reaches outside the node tree in exactly two places a
    synthetic definition cannot satisfy: ``_base_from_extends`` parses the real
    NXDL named by ``extends``, and ``_all_ancestor_member_names`` walks the real
    inheritance chain. Both are stubbed so the assertions isolate the
    conflict-renaming rules; node traversal, quantity and subsection building
    all still run for real.

    ``ancestor_members`` is the ``(quantity_names, subsection_names)`` pair the
    ancestor chain is taken to expose.
    """
    monkeypatch.setattr(converter, "generate_tree_from", lambda _: root)
    monkeypatch.setattr(
        converter,
        "_base_from_extends",
        lambda *_: (
            "Object",
            "pynxtools.nomad.metainfo.base_classes.object",
            True,
            [],
        ),
    )
    monkeypatch.setattr(
        converter, "_all_ancestor_member_names", lambda _: ancestor_members
    )


def test_build_context_suffixes_field_conflicting_with_subsection(monkeypatch):
    """A Quantity is renamed ``<name>_quantity`` when a SubSection owns the name.

    NOMAD raises MetainfoError instead of silently replacing when a SubSection
    and a Quantity of the same name meet in an inheritance chain, so the
    generator renames the Quantity. Both sources of the clash are covered in one
    build: a SubSection inherited from an ancestor, and a group declared by this
    class. A field's attributes key off the renamed quantity, so they carry the
    suffix too.
    """
    inherited_conflict = NexusField(name="inherited_conflict")
    inherited_conflict.dtype = "NX_FLOAT"
    units_attr = NexusAttribute(name="units")
    units_attr.dtype = "NX_CHAR"
    units_attr.parent = inherited_conflict

    own_conflict_field = NexusField(name="own_conflict")
    own_conflict_field.dtype = "NX_FLOAT"

    unaffected = NexusField(name="unaffected")
    unaffected.dtype = "NX_FLOAT"

    root = _make_definition("NXentry", extends="NXancestor", doc="Doc.")
    # The group is declared by this class, so its subsection name lands in
    # own_sub_names during build_context's pre-scan. nxdl_base must match the
    # definition's own file or the group is treated as inherited and skipped.
    own_conflict_group = NexusGroup(
        nx_class="NXdata",
        name="own_conflict",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    inherited_conflict.parent = root
    own_conflict_field.parent = root
    unaffected.parent = root
    own_conflict_group.parent = root

    _patch_isolated_build_context(
        monkeypatch,
        root,
        ancestor_members=(frozenset(), frozenset({"inherited_conflict"})),
    )

    context = converter.build_context("NXentry")
    quantity_names = [q.python_name for q in context["quantities"]]
    subsection_names = [s.python_name for s in context["subsections"]]

    assert quantity_names == [
        "inherited_conflict_quantity",
        "inherited_conflict_quantity__units",
        "own_conflict_quantity",
        "unaffected",
    ]
    # The SubSection keeps the unqualified name in both directions.
    assert subsection_names == ["own_conflict"]


def test_build_context_suffixes_subsection_conflicting_with_ancestor_quantity(
    monkeypatch,
):
    """A group is renamed ``<name>_group`` when an ancestor Quantity owns the name.

    Mirror image of the rename above: whichever concept sits higher in the NeXus
    chain keeps the unqualified name, so here the ancestor's Quantity wins.
    """
    root = _make_definition("NXentry", extends="NXancestor", doc="Doc.")
    conflicting_group = NexusGroup(
        nx_class="NXdata",
        name="ancestor_quantity_name",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    plain_group = NexusGroup(
        nx_class="NXnote",
        name="plain_group",
        nx_type="group",
        nxdl_base="NXentry.nxdl.xml",
    )
    conflicting_group.parent = root
    plain_group.parent = root

    _patch_isolated_build_context(
        monkeypatch,
        root,
        ancestor_members=(frozenset({"ancestor_quantity_name"}), frozenset()),
    )

    context = converter.build_context("NXentry")
    subsection_names = [s.python_name for s in context["subsections"]]

    assert subsection_names == ["ancestor_quantity_name_group", "plain_group"]


@pytest.mark.parametrize("reserved_name", ("name", "lab_id", "description"))
def test_build_context_reserved_quantity_names_are_suffixed(monkeypatch, reserved_name):
    """Array fields named like a BaseSection attribute get a ``_quantity`` suffix.

    ``name``, ``lab_id`` and ``description`` (``_BASESECTION_RESERVED_NAMES``)
    shadow ``BaseSection``. A scalar of the same name may override safely, an
    array may not — ``BaseSection.normalize()`` treats them as scalars — so the
    field under test is given a shape.
    """
    reserved_field = NexusField(name=reserved_name)
    reserved_field.dtype = "NX_CHAR"
    reserved_field.shape = (None,)

    root = _make_definition("NXentry", extends="NXobject")
    reserved_field.parent = root

    _patch_isolated_build_context(
        monkeypatch, root, ancestor_members=(frozenset(), frozenset())
    )

    context = converter.build_context("NXentry")
    quantity_names = [q.python_name for q in context["quantities"]]
    expected_base = f"{reserved_name}_quantity"

    assert quantity_names == [expected_base]


def test_write_base_class_dry_run_detects_content_change(monkeypatch, tmp_path):
    """Dry-run reports a content difference without writing the file.

    ``output_dir`` is the *parent* of ``base_classes/`` — ``write_class`` appends
    the category folder itself from the NXDL's category.
    """
    out_dir = tmp_path / "base_classes"
    out_dir.mkdir(parents=True)
    existing = out_dir / "entry.py"
    existing.write_text("old content\n", encoding="utf-8")

    monkeypatch.setattr(converter, "build_context", lambda _: {"class_name": "Entry"})
    monkeypatch.setattr(
        converter, "render", lambda _context, out_path=None: "new content\n"
    )

    changed = converter.write_base_class(
        "NXentry", dry_run=True, force=False, output_dir=tmp_path
    )

    assert changed is True


def test_generate_all_base_classes_counts_only_changed(monkeypatch, tmp_path):
    """The returned count includes only the classes reported as changed.

    ``write_class`` is the seam to replace: ``_generate_nx_classes`` calls it,
    and ``write_base_class`` is a thin alias over it.
    """
    monkeypatch.setattr(converter, "_discover_base_classes", lambda: ["NXa", "NXb"])
    monkeypatch.setattr(
        converter,
        "_build_dependency_graph",
        lambda _: {"NXa": set(), "NXb": {"NXa"}},
    )

    changes = {"NXa": False, "NXb": True}

    # write_base_class is a thin alias; _generate_nx_classes calls write_class,
    # so that is the seam to replace.
    def fake_write(nx_name, dry_run=False, force=False, output_dir=None):
        _ = (dry_run, force, output_dir)
        return changes[nx_name]

    monkeypatch.setattr(converter, "write_class", fake_write)

    written = converter.generate_all_base_classes(output_dir=tmp_path)

    assert written == 1


# ---------------------------------------------------------------------------
# Full-pipeline integration tests (controlled NXtestBase fixture → Python source)
# ---------------------------------------------------------------------------


def test_write_base_class_nxtestbase_full_pipeline(tmp_path):
    """NXtestBase renders through the whole pipeline to compilable Python.

    Runs ``generate_tree_from`` → ``build_context`` → ``render`` → write with no
    stubs. The fixture covers NX_CHAR, NX_FLOAT with units, NX_INT, NX_BOOLEAN, a
    closed enum, a group reference and a group-level attribute in one pass, and
    keeps the test independent of live NeXus definition changes.
    """
    converter.write_base_class("NXtestBase", output_dir=tmp_path, force=True)

    # NXtestBase declares category="base", so write_class routes it into
    # <output_dir>/base_classes/ rather than <output_dir> directly.
    source = (tmp_path / "base_classes" / "testbase.py").read_text(encoding="utf-8")

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
    """NXtestBase's class structure matches its stored golden, rendered in memory.

    Same assertions as the parametrized golden test below, which also covers
    NXtestBase; this one is kept separate because it renders without touching the
    filesystem, isolating a structural drift from a write-path failure.
    """
    golden = (_CONVERTER_GOLDEN_DIR / "testbase.py").read_text(encoding="utf-8")
    generated = converter.render(converter.build_context("NXtestBase"))
    assert _class_bases(generated) == _class_bases(golden), (
        "NXtestBase: class inheritance mismatch"
    )
    assert _class_members(generated) == _class_members(golden), (
        "NXtestBase: class member mismatch (name or Quantity/SubSection kind changed)"
    )


# ---------------------------------------------------------------------------
# NXtest / NXtest_extended: full-pipeline section-by-section golden tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "nx_class, golden_file",
    [
        ("NXtestBase", "testbase.py"),
        ("NXtest", "test.py"),
        ("NXtest_extended", "test_extended.py"),
    ],
)
def test_nxtest_fixture_sections_match_golden(nx_class, golden_file):
    """Each fixture NXDL renders to the class structure stored in its golden.

    Compares class bases and member names/kinds per class. The comparison is
    structural, so formatting, docstring text and keyword order cannot fail it —
    only a real change in what the schema declares. NXtest and NXtest_extended
    are application definitions and add named-concept groups, base-class
    inheritance and multi-class output on top of what NXtestBase covers.

    A failure means a fixture NXDL or the Jinja2 template changed; regenerate the
    golden files as described in this module's docstring.
    """
    golden = (_CONVERTER_GOLDEN_DIR / golden_file).read_text(encoding="utf-8")
    generated = converter.render(converter.build_context(nx_class))

    assert _class_bases(generated) == _class_bases(golden), (
        f"{nx_class}: class inheritance mismatch"
    )
    assert _class_members(generated) == _class_members(golden), (
        f"{nx_class}: class member mismatch (name or Quantity/SubSection kind changed)"
    )
