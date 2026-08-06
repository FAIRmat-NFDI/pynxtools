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

Pins how an NXDL node becomes a Quantity or a SubSection, how names are resolved
when they collide, and how a whole NXDL renders to Python source.

The unit tests cover one conversion rule each. Their input nodes are attached
directly to a root read from a fixture NXDL instead of being resolved from the
NeXus tree, so every test states its input in full. The reference tests then run
the fixture NXDLs through the real pipeline and compare the result against
stored output. That comparison is structural, via ``ast``, so formatting and
docstring changes cannot fail it.

The fixture NXDLs (``NXtestBase``, ``NXtest``, ``NXtest_extended`` in
``src/pynxtools/data/``) keep the reference tests independent of the live NeXus
definitions. A few unit tests use the real ``NXentry`` tree on purpose, to pin
behavior against an actual inheritance chain.

Run ``scripts/generate_metainfo_reference_files.py`` to refresh the reference
files in ``tests/data/nomad/converter/``.
"""

from collections.abc import Callable

import pytest

import pynxtools.nomad.converters.nxdl_to_metainfo as converter
from pynxtools.nexus.nexus_tree import (
    NexusAttribute,
    NexusDefinition,
    NexusField,
    NexusGroup,
    generate_tree_from,
)
from pynxtools.nexus.utils import get_nxdl_root_and_path


@pytest.fixture
def definition_factory() -> Callable[[str], NexusDefinition]:
    """Build a fixture NXDL's ``<definition>`` element as a childless root node.

    The real NXDL file is read, so ``category``, ``extends`` and ``symbols`` are
    genuine, but nothing is resolved from the inheritance chain. A test attaches
    exactly the nodes it wants to assert on. Pass ``NXtestBase``: an application
    definition would have its children replaced by those of its ``NXentry``
    group.
    """

    def factory(nx_name: str) -> NexusDefinition:
        elem, path = get_nxdl_root_and_path(nx_name)
        return NexusDefinition(name=nx_name, nxdl_base=path, inheritance=[elem])

    return factory


def test_build_quantity_from_field_maps_transformation_unit():
    """Field nodes carry unit, shape and enum semantics onto a QuantityContext.

    Builds one field with a transformation unit and a closed enum, then checks
    the converted values: ``NX_TRANSFORMATION`` collapses to ``NX_ANY``, which is
    deliberately dimensionless, and the enum becomes ``MEnum``.
    """
    node = NexusField(name="value")
    node.dtype = "NX_CHAR"
    node.unit = "NX_TRANSFORMATION"
    node.shape = (None,)
    node.items = ["a", "b"]
    node.open_enum = False

    qty = converter._build_quantity_from_node(node)

    assert qty.unit == "NX_ANY"
    assert qty.dimensionality is None
    assert qty.shape == ["*"]
    assert qty.python_type == "MEnum(['a', 'b'])"
    assert qty.scalar_items == ["a", "b"]


def test_build_quantity_from_attribute_uses_dtype_mapping():
    """Attribute nodes keep the parent-field link and carry no unit metadata.

    Attributes have no NXDL unit, so ``unit`` and ``dimensionality`` stay None.
    The shape is two-dimensional to cover the ``(None, 1)`` to ``["*", 1]``
    conversion.
    """
    node = NexusAttribute(name="status")
    node.dtype = "NX_BOOLEAN"
    node.shape = (None, 1)  # multi-dim: exercises (None, 1) → ["*", 1] conversion

    qty = converter._build_quantity_from_node(node, parent_field="signal")

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

    One case per ``nameType``: ``specified`` keeps a fixed name, ``partial``
    stays variable with the NXDL literal preserved, and ``any`` lowercases the
    class stem with no name literal. ``repeats`` follows ``variadic``
    independently of naming.
    """
    node = NexusGroup(
        nx_class="NXdetector",
        name=node_name,
        nx_type="group",
        name_type=name_type,
        variadic=variadic,
    )

    # section_fqn is stored verbatim and resolved lazily by NOMAD at
    # __init_metainfo__() time, so any dotted string works here.
    section = converter._build_subsection_from_node(
        node,
        section_fqn="test.module.TestSection",
    )

    assert section.python_name == expected_name
    assert section.nx_name_literal == expected_literal
    assert section.variable is expected_variable
    assert section.repeats is variadic


def test_base_from_extends_for_direct_child_with_nomad_base():
    """A direct NXobject child gets the ``Object`` base plus its NOMAD bases."""
    root = generate_tree_from("NXentry")

    base = converter._base_from_extends("NXentry", root)
    expected_nomad_fqns = converter._nomad_base_for_nx_class("NXentry")

    assert expected_nomad_fqns == [
        "nomad.datamodel.metainfo.basesections.Measurement",
        "nomad.datamodel.data.EntryData",
    ]
    assert base == (
        "Object",
        "pynxtools.nomad.metainfo.base_classes.object",
        True,
        expected_nomad_fqns,
    )


def _patch_isolated_build_context(monkeypatch, root, ancestor_members):
    """Run build_context against ``root`` with a fixed set of ancestor members.

    Two lookups reach outside the node tree — the base class named by
    ``extends``, and the member names inherited from the chain — and a root
    holding only the nodes under test cannot satisfy them. Stubbing both leaves
    the name-conflict rules as the only thing under test; node traversal and
    quantity and subsection building still run for real. ``ancestor_members`` is
    a ``(quantity_names, subsection_names)`` pair.
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


def test_build_context_suffixes_field_conflicting_with_subsection(
    monkeypatch, definition_factory
):
    """A Quantity is renamed ``<name>_quantity`` when a SubSection owns the name."""
    inherited_conflict = NexusField(name="inherited_conflict")
    inherited_conflict.dtype = "NX_FLOAT"
    units_attr = NexusAttribute(name="units")
    units_attr.dtype = "NX_CHAR"
    units_attr.parent = inherited_conflict

    own_conflict_field = NexusField(name="own_conflict")
    own_conflict_field.dtype = "NX_FLOAT"

    unaffected = NexusField(name="unaffected")
    unaffected.dtype = "NX_FLOAT"

    root = definition_factory("NXtestBase")
    # The group is declared by this class, so its subsection name lands in
    # own_sub_names during build_context's pre-scan. nxdl_base must match the
    # definition's own file or the group is treated as inherited and skipped.
    own_conflict_group = NexusGroup(
        nx_class="NXdata",
        name="own_conflict",
        nx_type="group",
        nxdl_base=root.nxdl_base,
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

    context = converter.build_context("NXtestBase")
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
    monkeypatch, definition_factory
):
    """A group is renamed ``<name>_group`` when an ancestor Quantity owns the same name."""
    root = definition_factory("NXtestBase")
    conflicting_group = NexusGroup(
        nx_class="NXdata",
        name="ancestor_quantity_name",
        nx_type="group",
        nxdl_base=root.nxdl_base,
    )
    plain_group = NexusGroup(
        nx_class="NXnote",
        name="plain_group",
        nx_type="group",
        nxdl_base=root.nxdl_base,
    )
    conflicting_group.parent = root
    plain_group.parent = root

    _patch_isolated_build_context(
        monkeypatch,
        root,
        ancestor_members=(frozenset({"ancestor_quantity_name"}), frozenset()),
    )

    context = converter.build_context("NXtestBase")
    subsection_names = [s.python_name for s in context["subsections"]]

    assert subsection_names == ["ancestor_quantity_name_group", "plain_group"]


@pytest.mark.parametrize(
    "nxdl_name, shape, expected_name",
    [
        # An ordinary field name is carried through untouched.
        ("start_time", None, "start_time"),
        # A scalar named like a BaseSection attribute keeps its name: NOMAD lets
        # a subclass override an inherited quantity outright.
        ("name", None, "name"),
        ("datetime", None, "datetime"),
        ("lab_id", None, "lab_id"),
        ("description", None, "description"),
        # The same name with a shape cannot override: BaseSection.normalize()
        # treats these as scalars, so an array is suffixed instead.
        ("name", (None,), "name_quantity"),
        ("datetime", (None,), "datetime_quantity"),
        ("lab_id", (None,), "lab_id_quantity"),
        ("description", (None,), "description_quantity"),
        # A Python keyword is unusable as an attribute name either way.
        ("lambda", None, "lambda_quantity"),
        ("lambda", (None,), "lambda_quantity"),
    ],
)
def test_build_context_reserved_quantity_names_are_suffixed(
    monkeypatch, definition_factory, nxdl_name, shape, expected_name
):
    """A field name is suffixed only when it cannot be used as it stands.

    Covers the two reasons the converter renames, and the cases it leaves alone:
    a Python keyword is always suffixed, a name shadowing a BaseSection
    attribute only when the field has a shape, and any other name never is. The
    whole ``_BASESECTION_RESERVED_NAMES`` set is exercised in both shapes.
    """
    field = NexusField(name=nxdl_name)
    field.dtype = "NX_CHAR"
    field.shape = shape

    root = definition_factory("NXtestBase")
    field.parent = root

    _patch_isolated_build_context(
        monkeypatch, root, ancestor_members=(frozenset(), frozenset())
    )

    context = converter.build_context("NXtestBase")
    quantity_names = [q.python_name for q in context["quantities"]]

    assert quantity_names == [expected_name]


def test_write_base_class_dry_run_detects_content_change(monkeypatch, tmp_path):
    """A dry run reports a content difference without writing the file."""

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
    # "Dry run" is the other half of the contract: the difference is reported,
    # but the file on disk still holds its original content.
    assert existing.read_text(encoding="utf-8") == "old content\n"


def test_generate_all_base_classes_counts_only_changed(monkeypatch, tmp_path):
    """The returned count includes only the classes reported as changed.

    Two classes are discovered and the writer is stubbed to report a change for
    one of them.
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
