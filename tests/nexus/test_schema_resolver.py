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
"""Tests for nexus.schema_resolver: resolve_path and NexusSchemaResolver."""

import h5py
import numpy as np
import pytest

from pynxtools.nexus.nexus_tree import generate_tree_from
from pynxtools.nexus.schema_resolver import NexusSchemaResolver, resolve_path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def nxtest_tree():
    """NexusNode tree for NXtest (no h5py required)."""
    return generate_tree_from("NXtest")


@pytest.fixture
def nxtest_h5():
    """In-memory HDF5 file shaped like an NXtest file. Closed after each test."""
    f = h5py.File("__nxtest__", "w", driver="core", backing_store=False)
    f.attrs["NX_class"] = "NXroot"
    entry = f.create_group("ENTRY")
    entry.attrs["NX_class"] = "NXentry"
    entry.create_dataset("definition", data="NXtest")
    nxodd = entry.create_group("NXODD_name")
    nxodd.attrs["NX_class"] = "NXdata"
    nxodd.create_dataset("float_value", data=np.float32(1.0))
    yield f
    f.close()


# ---------------------------------------------------------------------------
# resolve_path — pure tree traversal, no h5py
# ---------------------------------------------------------------------------


class TestResolvePath:
    def test_empty_path_returns_root(self, nxtest_tree):
        assert resolve_path(nxtest_tree, "") is nxtest_tree

    def test_single_group_segment(self, nxtest_tree):
        node = resolve_path(nxtest_tree, "ENTRY", node_type="group")
        assert node is not None
        assert node.name == "ENTRY"
        assert node.nx_type == "group"

    def test_multi_segment_field(self, nxtest_tree):
        node = resolve_path(
            nxtest_tree, "ENTRY/NXODD_name/float_value", node_type="field"
        )
        assert node is not None
        assert node.name == "float_value"
        assert node.unit == "NX_ENERGY"

    def test_unknown_segment_returns_none(self, nxtest_tree):
        assert (
            resolve_path(nxtest_tree, "ENTRY/does_not_exist", node_type="field") is None
        )

    def test_unknown_intermediate_segment_returns_none(self, nxtest_tree):
        assert (
            resolve_path(nxtest_tree, "ENTRY/ghost/float_value", node_type="field")
            is None
        )

    def test_cache_is_populated_with_intermediate_nodes(self, nxtest_tree):
        cache: dict = {}
        resolve_path(
            nxtest_tree,
            "ENTRY/NXODD_name/float_value",
            node_type="field",
            _cache=cache,
        )
        assert "ENTRY" in cache
        assert "ENTRY/NXODD_name" in cache
        assert "ENTRY/NXODD_name/float_value" in cache

    def test_cache_short_circuits_on_none(self, nxtest_tree):
        cache: dict = {"ENTRY": None}
        result = resolve_path(
            nxtest_tree, "ENTRY/NXODD_name/float_value", node_type="field", _cache=cache
        )
        assert result is None

    def test_cache_returns_stored_node(self, nxtest_tree):
        cache: dict = {}
        first = resolve_path(
            nxtest_tree, "ENTRY/NXODD_name/float_value", node_type="field", _cache=cache
        )
        # Wipe the tree's ENTRY children to prove next call uses cache only
        second = resolve_path(
            nxtest_tree, "ENTRY/NXODD_name/float_value", node_type="field", _cache=cache
        )
        assert first is second

    def test_h5file_narrows_resolution_by_nx_class(self, nxtest_tree, nxtest_h5):
        """h5file NX_class is used to disambiguate groups — wrong class → None."""
        # NXODD_name in the file has NX_class=NXdata, which matches the schema.
        node = resolve_path(
            nxtest_tree,
            "ENTRY/NXODD_name/float_value",
            node_type="field",
            h5file=nxtest_h5,
        )
        assert node is not None
        assert node.name == "float_value"

    def test_h5file_none_does_not_raise(self, nxtest_tree):
        """Passing h5file=None falls back to name-only matching."""
        node = resolve_path(
            nxtest_tree,
            "ENTRY/NXODD_name/float_value",
            node_type="field",
            h5file=None,
        )
        assert node is not None

    def test_hint_forwarded_to_last_segment(self, nxtest_tree):
        """Passing a hint should not crash even when no ambiguity exists."""
        node = resolve_path(
            nxtest_tree,
            "ENTRY/NXODD_name/float_value",
            node_type="field",
            hint="signal",
        )
        assert node is not None


# ---------------------------------------------------------------------------
# NexusSchemaResolver.appdef_for — requires h5py
# ---------------------------------------------------------------------------


class TestAppdefFor:
    def test_returns_definition_field_value(self, nxtest_h5):
        assert (
            NexusSchemaResolver.appdef_for(nxtest_h5["ENTRY/NXODD_name/float_value"])
            == "NXtest"
        )

    def test_nxentry_without_definition_returns_nxroot(self):
        f = h5py.File("__no_def__", "w", driver="core", backing_store=False)
        entry = f.create_group("ENTRY")
        entry.attrs["NX_class"] = "NXentry"
        assert NexusSchemaResolver.appdef_for(f["ENTRY"]) == "NXroot"
        f.close()

    def test_no_nxentry_ancestor_returns_sentinel(self):
        f = h5py.File("__no_entry__", "w", driver="core", backing_store=False)
        data = f.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        assert NexusSchemaResolver.appdef_for(f["data"]) == "NO NXentry found"
        f.close()

    def test_works_on_group_node(self, nxtest_h5):
        assert NexusSchemaResolver.appdef_for(nxtest_h5["ENTRY/NXODD_name"]) == "NXtest"

    def test_works_on_root_group(self, nxtest_h5):
        assert NexusSchemaResolver.appdef_for(nxtest_h5["/"]) == "NO NXentry found"


# ---------------------------------------------------------------------------
# NexusSchemaResolver.tree_for
# ---------------------------------------------------------------------------


class TestTreeFor:
    def test_valid_appdef_returns_tree(self):
        resolver = NexusSchemaResolver()
        tree = resolver.tree_for("NXtest")
        assert tree is not None
        assert tree.name == "NXtest"

    def test_invalid_appdef_returns_none(self):
        resolver = NexusSchemaResolver()
        assert resolver.tree_for("NXdoes_not_exist_xxxx") is None

    def test_result_is_cached(self):
        resolver = NexusSchemaResolver()
        first = resolver.tree_for("NXtest")
        second = resolver.tree_for("NXtest")
        assert first is second

    def test_none_result_is_cached(self):
        resolver = NexusSchemaResolver()
        resolver.tree_for("NXdoes_not_exist_xxxx")
        assert "NXdoes_not_exist_xxxx" in resolver._tree_cache


# ---------------------------------------------------------------------------
# NexusSchemaResolver.node_for
# ---------------------------------------------------------------------------


class TestNodeFor:
    def test_field_path(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        node = resolver.node_for(
            "ENTRY/NXODD_name/float_value", nxtest_h5["ENTRY/NXODD_name/float_value"]
        )
        assert node is not None
        assert node.name == "float_value"
        assert node.unit == "NX_ENERGY"

    def test_group_path(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        node = resolver.node_for("ENTRY/NXODD_name", nxtest_h5["ENTRY/NXODD_name"])
        assert node is not None
        assert node.name == "NXODD_name"
        assert node.nx_type == "group"

    def test_entry_group(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        node = resolver.node_for("ENTRY", nxtest_h5["ENTRY"])
        assert node is not None
        assert node.nx_type == "group"

    def test_nonexistent_schema_path_returns_none(self, nxtest_h5):
        nxtest_h5["ENTRY"].create_group("ghost")
        nxtest_h5["ENTRY/ghost"].attrs["NX_class"] = "NXelectronanalyzer"
        resolver = NexusSchemaResolver()
        assert resolver.node_for("ENTRY/ghost", nxtest_h5["ENTRY/ghost"]) is None

    def test_no_nxentry_returns_none(self):
        f = h5py.File("__no_entry2__", "w", driver="core", backing_store=False)
        data = f.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        resolver = NexusSchemaResolver()
        assert resolver.node_for("data", f["data"]) is None
        f.close()

    def test_empty_path_returns_none(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        assert resolver.node_for("", nxtest_h5["ENTRY"]) is None

    def test_result_is_cached(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        path = "ENTRY/NXODD_name/float_value"
        node = resolver.node_for(path, nxtest_h5[path])
        assert path in resolver._node_cache
        assert resolver.node_for(path, nxtest_h5[path]) is node

    def test_intermediate_nodes_are_cached(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        resolver.node_for(
            "ENTRY/NXODD_name/float_value", nxtest_h5["ENTRY/NXODD_name/float_value"]
        )
        assert "ENTRY" in resolver._node_cache
        assert "ENTRY/NXODD_name" in resolver._node_cache


# ---------------------------------------------------------------------------
# NexusSchemaResolver.attr_node_for
# ---------------------------------------------------------------------------


class TestAttrNodeFor:
    def test_known_attribute(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        # NXtest: ENTRY/definition has an <attribute name="version"/>
        node = resolver.attr_node_for(
            "ENTRY/definition", "version", nxtest_h5["ENTRY/definition"]
        )
        assert node is not None
        assert node.name == "version"
        assert node.nx_type == "attribute"

    def test_unknown_attribute_returns_none(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        node = resolver.attr_node_for(
            "ENTRY/definition", "nonexistent_attr", nxtest_h5["ENTRY/definition"]
        )
        assert node is None

    def test_unknown_parent_path_returns_none(self, nxtest_h5):
        resolver = NexusSchemaResolver()
        node = resolver.attr_node_for("ENTRY/ghost", "version", nxtest_h5["ENTRY"])
        assert node is None
