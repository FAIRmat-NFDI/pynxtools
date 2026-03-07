#
# Copyright The pynxtools Authors.
#
# This file is part of pynxtools.
# See https://github.com/FAIRmat-NFDI/pynxtools for further info.
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
Unified NeXus file handler.

`NexusFileHandler` walks an HDF5/NeXus file and dispatches each node to a
`NexusVisitor` implementation.  Callers choose *what to do* per node by
supplying the right visitor; the handler owns only traversal and file I/O.

Visitor interface
-----------------
Every visitor implements the same set of typed hooks:

* ``on_group(hdf_path, hdf_node)`` – called for every HDF5 group, including the
  root (whose *hdf_path* is an empty string ``""``).
* ``on_field(hdf_path, hdf_node)`` – called for every HDF5 dataset.
* ``on_attribute(hdf_path, attr_name, attr_value, parent)`` – called for every
  attribute of every group and dataset, **after** the node itself has been
  dispatched.
* ``on_complete(root)`` – called once after the full traversal.

Supported visitor use-cases:

* **Annotation** – `nexus.annotation.Annotator`
* **Validation** – `dataconverter.validation.ValidationVisitor`
* **NOMAD parsing** – `nomad.parser.NomadVisitor`

Migration note
--------------
The legacy `HandleNexus` class in `nexus.nexus` is a thin wrapper around
`NexusFileHandler` + `Annotator`.  It is kept for backward
compatibility and will be deprecated in a future release.
"""

from __future__ import annotations

import os
from typing import Any, Union

import h5py


class NexusVisitor:
    """
    Base class for NeXus file visitors.

    All hooks are no-ops by default.  Subclasses override only what they need.
    Every concrete visitor should implement the same set of methods so that
    they can be used interchangeably with `NexusFileHandler`.

    Hook call order for each node:

    1. ``on_group`` **or** ``on_field`` (dispatched by node type)
    2. ``on_attribute`` for every attribute of that node (in iteration order)

    Root is treated as a group with *hdf_path* equal to ``""``.
    After full traversal, ``on_complete`` is called with the open root file.
    """

    def on_group(
        self,
        hdf_path: str,
        hdf_node: h5py.Group,
    ) -> None:
        """Called for every HDF5 group, including the root (path ``""``)."""

    def on_field(
        self,
        hdf_path: str,
        hdf_node: h5py.Dataset,
    ) -> None:
        """Called for every HDF5 dataset (field)."""

    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
    ) -> None:
        """Called for every attribute of every group and dataset.

        Parameters
        ----------
        hdf_path:
            Path of the *parent* node (no leading ``/``).
        attr_name:
            Name of the attribute.
        attr_value:
            Raw attribute value as returned by h5py.
        parent:
            The h5py group or dataset that owns this attribute.
        """

    def on_complete(self, root: h5py.File) -> None:
        """Called once after the full traversal, before the file is closed."""


class NexusFileHandler:
    """
    Walks a NeXus/HDF5 file and dispatches each node to a `NexusVisitor`.

    Parameters
    ----------
    nexus_file:
        Path to the NeXus file, a list whose first element is the path, or
        an already-open `h5py.File` (in which case set *is_in_memory_file*).
    is_in_memory_file:
        When ``True``, *nexus_file* is treated as an already-open
        `h5py.File` object (or compatible) rather than a file path.
    """

    def __init__(
        self,
        nexus_file: str | list | h5py.File,
        is_in_memory_file: bool = False,
    ) -> None:
        if nexus_file is None:
            local_dir = os.path.abspath(os.path.dirname(__file__))
            nexus_file = os.path.join(local_dir, "../data/201805_WSe2_arpes.nxs")
        self._nexus_file = nexus_file
        self._is_in_memory = is_in_memory_file

    def process(self, visitor: NexusVisitor) -> None:
        """Walk the NeXus file and dispatch each node to *visitor*.

        Opens the file (unless already open), performs a cycle-safe depth-first
        traversal, dispatches ``on_group`` / ``on_field`` / ``on_attribute`` for
        every node and attribute, and finally calls ``on_complete`` before
        closing the file.

        The ``get_inherited_hdf_nodes`` LRU cache is cleared after processing
        to avoid unbounded memory growth across successive calls.
        """
        from pynxtools.nexus.nexus import get_inherited_hdf_nodes

        if self._is_in_memory:
            root = self._nexus_file
            self._traverse(root, visitor)
        else:
            file_path = (
                self._nexus_file[0]
                if isinstance(self._nexus_file, list)
                else self._nexus_file
            )
            root = h5py.File(file_path, "r")
            try:
                self._traverse(root, visitor)
            finally:
                root.close()
                get_inherited_hdf_nodes.cache_clear()

    def _traverse(self, root: h5py.File, visitor: NexusVisitor) -> None:
        """Run the full traversal and call on_complete."""
        self._full_visit(root, root, "", visitor)
        visitor.on_complete(root)

    @staticmethod
    def _not_yet_visited(root: h5py.File, name: str) -> bool:
        """Return ``True`` if *name* is not an alias of an ancestor on the same path.

        Detects HDF5 hard links that would otherwise cause infinite recursion.
        """
        parts = name.split("/")
        for i in range(1, len(parts)):
            ancestor = "/".join(parts[:i])
            if root["/" + ancestor] == root["/" + name]:
                return False
        return True

    def _full_visit(
        self,
        root: h5py.File,
        hdf_node: h5py.Group | h5py.Dataset,
        name: str,
        visitor: NexusVisitor,
    ) -> None:
        """Depth-first, cycle-safe traversal.

        Dispatch order for each node:

        1. ``visitor.on_field`` **or** ``visitor.on_group``
        2. ``visitor.on_attribute`` for every attribute (in h5py iteration order)
        3. Recurse into children (groups only)
        """
        # Dispatch node
        if isinstance(hdf_node, h5py.Dataset):
            visitor.on_field(name, hdf_node)
        else:
            visitor.on_group(name, hdf_node)

        # Dispatch attributes after the node itself, before recursing into children
        for attr_name, attr_value in hdf_node.attrs.items():
            visitor.on_attribute(name, attr_name, attr_value, hdf_node)

        # Recurse into children
        if isinstance(hdf_node, h5py.Group):
            for ch_name, child in hdf_node.items():
                full_name = ch_name if not name else f"{name}/{ch_name}"
                if self._not_yet_visited(root, full_name):
                    self._full_visit(root, child, full_name, visitor)
