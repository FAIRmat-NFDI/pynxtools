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
    """Validate subsection naming and flags for specified, partial, and any groups."""
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
    """Check inheritance tuple for direct NXobject children with NOMAD semantic base.

    Uses a real ``NexusDefinition`` from ``generate_tree_from("NXentry")`` so the
    XML inheritance chain is exercised without any mocking.  NXentry extends
    NXobject directly, so the primary base is the generated ``Object`` class and
    the NOMAD semantic bases from ``BASESECTIONS_MAP`` are added alongside it.
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

    ``build_context`` reaches outside the node tree in exactly two places that a
    synthetic ``NexusDefinition`` cannot satisfy: it resolves the Python base via
    ``_base_from_extends`` (which parses the real NXDL of whatever ``extends``
    names) and it collects inherited member names via ``_all_ancestor_member_names``
    (which walks the real inheritance chain).  Both are replaced with fixed values
    so the assertions isolate the conflict-renaming rules themselves.  Everything
    else — node traversal, quantity building, subsection building — runs for real.

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
    """Fields are renamed ``<name>_quantity`` when a SubSection owns the name.

    NOMAD raises MetainfoError rather than silently replacing when a SubSection
    and a Quantity of the same name meet in an inheritance chain, so the
    generator renames the Quantity.  Two independent sources feed the same
    rename and both are covered in one build:

    - ``parent_sub_names`` — a SubSection inherited from an ancestor class
    - ``own_sub_names`` — a group declared in this very class

    A field's own attributes are keyed off the *renamed* quantity, so the
    attribute quantity name must carry the suffix too.
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
    """Groups are renamed ``<name>_group`` when an ancestor Quantity owns the name.

    This is the mirror image of the rename above.  The symmetric inheritance rule
    is that whichever concept sits *higher* in the NeXus chain keeps the
    unqualified name; here the ancestor's Quantity wins and the group declared in
    this class is suffixed.
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
    """Ensure reserved quantity names are rewritten with ``_quantity`` in build output.

    Covers the names in ``_BASESECTION_RESERVED_NAMES`` (name, lab_id,
    description) which shadow ``BaseSection`` attributes.  The suffix applies to
    *array-shaped* fields: a scalar of the same name may safely override the
    inherited quantity, but an array cannot, because ``BaseSection.normalize()``
    and related logic treat those attributes as scalars throughout.  The field
    here is therefore given a shape.
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
    """Dry-run should report changes without touching existing files.

    ``output_dir`` is the *parent* of ``base_classes/``; write_class appends the
    category subfolder itself based on the NXDL's category.
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
    """Generation count should include only classes reported as changed."""
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
    """Full-pipeline: NXtestBase generates valid Python covering key converter features.

    NXtestBase (src/pynxtools/data/NXtestBase.nxdl.xml) is a controlled fixture that
    covers: NX_CHAR, NX_FLOAT with units, NX_INT, NX_BOOLEAN, closed enum, group
    reference, and group-level attribute.  Using a fixture NXDL keeps this test
    independent of live NeXus definition changes while still exercising the full
    generate_tree_from → build_context → render → write pipeline.
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
    """Generated NXtestBase class structure must match the stored golden file.

    The golden file lives in tests/data/nomad/converter/testbase.py and was produced
    by running the converter against NXtestBase.nxdl.xml.  Compares class inheritance
    and member names/kinds (Quantity, SubSection) for every class; formatting,
    docstring text, and annotation keyword ordering do not affect the result.  A
    failure here means the converter template or NXtestBase.nxdl.xml changed without
    regenerating the golden file.  Fix with the snippet in
    ``test_nxtest_fixture_sections_match_golden`` below, which covers this class
    too.
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
    """Generated classes from NXtest fixtures match the stored golden section structure.

    Compares class inheritance and member names/kinds (Quantity, SubSection) for
    every class in the generated file against the golden stored in
    tests/data/nomad/converter/.  The comparison is structural — formatting,
    docstring text, and annotation keyword ordering do not affect the result.
    NXtest and NXtest_extended are application definitions used here as controlled
    fixtures; they cover the full converter path including named concept groups,
    inheritance from base classes, and multi-class output files.

    A failure here means the NXtest*.nxdl.xml fixture or the Jinja2 template
    changed without regenerating the golden.  Regenerate from the repository
    root with::

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
            # These fixtures resolve through _NXDL_SPECIAL_NAMES to absolute
            # paths, which would otherwise leak the generating machine's layout
            # into the doc links stored in the golden.
            pathlib.Path("tests/data/nomad/converter", fname).write_text(
                src.replace(repo, ""), encoding="utf-8"
            )
        EOF
    """
    golden = (_CONVERTER_GOLDEN_DIR / golden_file).read_text(encoding="utf-8")
    generated = converter.render(converter.build_context(nx_class))

    assert _class_bases(generated) == _class_bases(golden), (
        f"{nx_class}: class inheritance mismatch"
    )
    assert _class_members(generated) == _class_members(golden), (
        f"{nx_class}: class member mismatch (name or Quantity/SubSection kind changed)"
    )
