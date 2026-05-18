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
Schema resolution: mapping HDF5 nodes to their NexusNode counterparts.

`NexusSchemaResolver` is visitor-agnostic — any `NexusVisitor` implementation
can hold one and use it to look up the schema node for a given HDF5 path,
without reimplementing appdef discovery, tree caching, or path traversal.
"""

from __future__ import annotations

from typing import Literal, Optional

import h5py

from pynxtools.nexus.nexus_tree import NexusNode, generate_tree_from
from pynxtools.nexus.utils import decode_if_string


def resolve_path(
    root: NexusNode,
    path: str,
    node_type: Literal["group", "field"] | None = None,
    *,
    h5file: h5py.File | None = None,
    hint: Literal["axis", "signal"] | None = None,
    _cache: dict[str, NexusNode | None] | None = None,
) -> NexusNode | None:
    """Resolve an HDF5 path against a NexusNode schema tree.

    Walks *root* segment by segment, selecting the best-matching child at each
    step via :meth:`NexusNode.best_child_for`.

    Attributes are not resolved here because they always live on a parent node
    (group or field) and require knowing that parent's type.  Use
    :meth:`NexusSchemaResolver.attr_node_for` instead.

    Parameters
    ----------
    root:
        Root of the NexusNode schema tree (from :func:`generate_tree_from`).
    path:
        HDF5 path without a leading slash (e.g. ``"entry/instrument/energy"``).
    node_type:
        Type of the *final* segment: ``"group"`` or ``"field"``.
        Intermediate segments are always treated as groups.
    h5file:
        Optional open HDF5 file used to read the ``NX_class`` attribute of
        intermediate group segments.  When provided, only schema groups whose
        NX class matches the file group's ``NX_class`` attribute are considered,
        giving deterministic disambiguation of variadic groups (e.g.
        ``DETECTOR[NXdetector]`` vs ``MONITOR[NXmonitor]``).  Pass ``None``
        to skip NX_class narrowing (pure schema walk).
    hint:
        ``"signal"`` or ``"axis"`` forwarded to ``best_child_for`` for the last
        segment only, to resolve the NXdata signal / axis ambiguity.
    _cache:
        Optional mutable dict for per-segment memoisation.  Both hits and ``None``
        misses are stored so that calls sharing a common path prefix avoid
        redundant tree traversals.  Pass the same dict across multiple calls on
        the same file for best effect.

    Returns
    -------
    NexusNode | None
        The matching node, or ``None`` if any segment has no schema match.
    """
    if not path:
        return root

    segments = [s for s in path.split("/") if s]
    current: NexusNode = root

    for i, seg in enumerate(segments):
        partial = "/".join(segments[: i + 1])

        if _cache is not None and partial in _cache:
            cached = _cache[partial]
            if cached is None:
                return None
            current = cached
            continue

        is_last = i == len(segments) - 1
        seg_node_type = node_type if is_last else "group"

        nx_class: str | None = None
        if h5file is not None and seg_node_type == "group":
            try:
                h5_grp = h5file["/" + partial]
                if isinstance(h5_grp, h5py.Group):
                    raw = h5_grp.attrs.get("NX_class", b"")
                    nx_class = decode_if_string(raw) or None
            except KeyError:
                pass

        seg_hint = hint if is_last else None
        child = current.best_child_for(
            seg, node_type=seg_node_type, nx_class=nx_class, hint=seg_hint
        )

        if _cache is not None:
            _cache[partial] = child

        if child is None:
            return None
        current = child

    return current


class NexusSchemaResolver:
    """Maps HDF5 nodes to their NexusNode schema counterparts.

    Maintains per-instance caches for appdef trees and path lookups,
    amortizing repeated schema resolution during a single file traversal.

    Typical usage inside a ``NexusVisitor``::

        class MyVisitor(NexusVisitor):
            def __init__(self):
                self._resolver = NexusSchemaResolver()

            def on_field(self, hdf_path, hdf_node):
                node = self._resolver.node_for(hdf_path, hdf_node)
                ...
    """

    def __init__(self) -> None:
        self._tree_cache: dict[str, NexusNode | None] = {}
        self._node_cache: dict[str, NexusNode | None] = {}

    # ------------------------------------------------------------------
    # Appdef discovery
    # ------------------------------------------------------------------

    @staticmethod
    def appdef_for(hdf_node: h5py.Group | h5py.Dataset) -> str:
        """Walk up the HDF5 tree to find the governing application definition.

        Returns the ``definition`` field value of the nearest ``NXentry`` ancestor,
        ``"NXroot"`` if no ``definition`` field is present, or
        ``"NO NXentry found"`` if no ``NXentry`` ancestor exists.
        """
        h5file = hdf_node.file
        parts = [p for p in hdf_node.name.split("/") if p]
        for i in range(len(parts), 0, -1):
            path = "/" + "/".join(parts[:i])
            try:
                candidate = h5file[path]
            except KeyError:
                continue
            if not isinstance(candidate, h5py.Group):
                continue
            if decode_if_string(candidate.attrs.get("NX_class", b"")) == "NXentry":
                try:
                    definition = candidate["definition"][()]
                    raw = (
                        definition.decode()
                        if isinstance(definition, bytes)
                        else str(definition)
                    )
                    return raw.strip()
                except (KeyError, AttributeError):
                    return "NXroot"
        return "NO NXentry found"

    # ------------------------------------------------------------------
    # Tree cache
    # ------------------------------------------------------------------

    def tree_for(self, appdef: str) -> NexusNode | None:
        """Return (and cache) the NexusNode tree for *appdef*."""
        if appdef not in self._tree_cache:
            try:
                self._tree_cache[appdef] = generate_tree_from(appdef)
            except Exception:
                self._tree_cache[appdef] = None
        return self._tree_cache[appdef]

    # ------------------------------------------------------------------
    # Node resolution
    # ------------------------------------------------------------------

    def node_for(
        self,
        hdf_path: str,
        hdf_node: h5py.Group | h5py.Dataset,
        hint: Literal["axis", "signal"] | None = None,
    ) -> NexusNode | None:
        """Return the schema NexusNode for the given HDF5 path, or ``None``.

        Path segments are resolved one at a time.  For each intermediate group
        the actual ``NX_class`` attribute is read from the HDF5 file and
        forwarded to :func:`~pynxtools.nexus.nexus_tree.resolve_path` so that
        variadic schema groups (e.g. ``DETECTOR[NXdetector]``) are
        disambiguated deterministically.

        Parameters
        ----------
        hdf_path:
            HDF5 path without a leading slash (e.g. ``"entry/instrument/energy"``).
            Pass an empty string to get the tree root.
        hdf_node:
            The live HDF5 node at *hdf_path*, used to locate the governing
            appdef and to read ``NX_class`` attributes of intermediate groups.
        hint:
            ``"signal"`` or ``"axis"`` — forwarded to the last segment to
            resolve the NXdata signal / axis field ambiguity.
        """
        if not hdf_path:
            return None
        if hdf_path in self._node_cache:
            return self._node_cache[hdf_path]

        appdef = self.appdef_for(hdf_node)
        if appdef == "NO NXentry found":
            return None
        tree = self.tree_for(appdef)
        if tree is None:
            return None

        node_type: Literal["group", "field"] = (
            "field" if isinstance(hdf_node, h5py.Dataset) else "group"
        )
        return resolve_path(
            tree,
            hdf_path,
            node_type=node_type,
            h5file=hdf_node.file,
            hint=hint,
            _cache=self._node_cache,
        )

    def attr_node_for(
        self,
        hdf_path: str,
        attr_name: str,
        parent_hdf: h5py.Group | h5py.Dataset,
    ) -> NexusNode | None:
        """Return the schema NexusNode for attribute *attr_name* on *hdf_path*."""
        parent_node = self.node_for(hdf_path, parent_hdf)
        if parent_node is None:
            return None
        return parent_node.best_child_for(attr_name, node_type="attribute")
