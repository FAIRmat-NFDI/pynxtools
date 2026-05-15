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
Unified NeXus file handler.

`NexusFileHandler` walks an HDF5/NeXus file and dispatches each node to a
`NexusVisitor` implementation. Callers choose *what to do* per node by
supplying the right visitor; the handler owns only traversal and file I/O.

Visitor interface
-----------------
Every visitor must implement four abstract hooks:

* ``on_group(hdf_path, hdf_node)`` - called for every HDF5 group, including the
  root (whose *hdf_path* is an empty string ``""``).
* ``on_field(hdf_path, hdf_node)`` - called for every HDF5 dataset.
* ``on_attribute(hdf_path, attr_name, attr_value, parent)`` - called for every
  attribute of every group and dataset, **after** the node itself has been
  dispatched.
* ``on_complete(root)`` - called once after the full traversal.

Two optional hooks have default no-op implementations and may be overridden:

* ``on_broken_link(hdf_path, link)`` - called when a soft or external link
  cannot be resolved (target missing or external file unreachable).  The broken
  node is skipped; traversal continues with the next sibling.
* ``on_external_link(hdf_path, link)`` - called when an external link is first
  encountered, *before* the handler opens the external file and recurses into
  its target subtree.  Nodes from the external subtree are visited with the same
  *hdf_path* prefix as the link itself (e.g. a link at ``"entry/ext"`` whose
  target is a group with child ``"value"`` results in a call
  ``on_field("entry/ext/value", ...)``).

Link traversal
--------------
* **Soft links** - resolved via ``h5py``; broken links dispatch ``on_broken_link``
  and are otherwise skipped.
* **Hard links** - followed transparently; a cycle guard prevents infinite
  recursion when a hard-linked descendant is an ancestor of itself.
* **External links** - the external file is opened in a separate ``h5py.File``
  context; broken external links dispatch ``on_broken_link`` and are skipped.
  If a visitor needs to distinguish broken soft links from broken external links
  it can inspect the type of the *link* argument passed to ``on_broken_link``.

Supported visitor use-cases:

* **Annotation** - `nexus.annotation.Annotator`
* **Validation** - `dataconverter.validation.ValidationVisitor`
* **NOMAD parsing** - `nomad.parser.NomadVisitor`

Migration note
--------------
The legacy `HandleNexus` class in `nexus.nexus` is a thin wrapper around
`NexusFileHandler` + `Annotator`.  It is kept for backward
compatibility and will be deprecated in a future release.
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

import h5py

logger = logging.getLogger("pynxtools")


class NexusVisitor(ABC):
    """
    Abstract base class for NeXus file visitors.

    Subclasses must implement the four abstract hooks below.  Hooks that are not
    meaningful for a given visitor should be implemented as ``pass``.  Two
    additional optional hooks (``on_broken_link``, ``on_external_link``) have
    default no-op implementations and may be overridden as needed.

    Hook call order for each node:

    1. ``on_group`` **or** ``on_field`` (dispatched by node type)
    2. ``on_attribute`` for every attribute of that node (in iteration order)
    3. Recursion into children (groups only)

    Special cases:

    * Root is treated as a group with *hdf_path* equal to ``""``.
    * Broken soft/external links dispatch ``on_broken_link`` instead of the
      normal group/field hook; the node is then skipped.
    * External links additionally dispatch ``on_external_link`` *before*
      the handler opens the external file.
    * After the full traversal, ``on_complete`` is called with the open root.
    """

    @abstractmethod
    def on_group(
        self,
        hdf_path: str,
        hdf_node: h5py.Group,
    ) -> None:
        """Called for every HDF5 group, including the root (path ``""``)."""

    @abstractmethod
    def on_field(
        self,
        hdf_path: str,
        hdf_node: h5py.Dataset,
    ) -> None:
        """Called for every HDF5 dataset (field)."""

    @abstractmethod
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

    @abstractmethod
    def on_complete(self, root: h5py.File) -> None:
        """Called once after the full traversal, before the file is closed."""

    def on_broken_link(
        self,
        hdf_path: str,
        link: h5py.SoftLink | h5py.ExternalLink,
    ) -> None:
        """Called when a soft or external link cannot be resolved.

        The default implementation does nothing.  Override in visitors that
        need to report broken links (e.g. ``ValidationVisitor``).
        """

    def on_external_link(
        self,
        hdf_path: str,
        link: h5py.ExternalLink,
    ) -> None:
        """Called when an external link is first encountered, before the handler
        attempts to open the external file and recurse into it.

        The default implementation does nothing.
        """


class NexusFileHandler:
    """
    Walks a NeXus/HDF5 file and dispatches each node to a `NexusVisitor`.

    Parameters
    ----------
    nxs_file:
        Path to the NeXus file, a list whose first element is the path, or
        an already-open `h5py.File` (in which case set *is_open*).
    is_open:
        When ``True``, *nxs_file* is treated as an already-open
        `h5py.File` object (or compatible) rather than a file path.
    """

    def __init__(
        self,
        nxs_file: str | h5py.File | Path,
        is_open: bool = False,
    ) -> None:
        if nxs_file is None:
            local_dir = os.path.abspath(os.path.dirname(__file__))
            nxs_file = os.path.join(local_dir, "../data/201805_WSe2_arpes.nxs")
            logger.info(
                "No NeXus file provided; using bundled ARPES example file: %s",
                Path(nxs_file).name,
            )
        self._nxs_file = nxs_file
        self._is_in_memory = is_open

    def process(self, visitor: NexusVisitor) -> None:
        """Walk the NeXus file and dispatch each node to *visitor*.

        Opens the file (unless already open), performs a cycle-safe depth-first
        traversal, dispatches ``on_group`` / ``on_field`` / ``on_attribute`` for
        every node and attribute, and finally calls ``on_complete`` before
        closing the file.

        The ``_get_inherited_hdf_nodes`` LRU cache (legacy XML-element lookup,
        used only by the NOMAD parser callback path) is cleared after processing
        to avoid unbounded memory growth across successive calls.  This import
        and ``cache_clear`` call will be removed when NomadVisitor is implemented.
        """
        from pynxtools.nexus.nexus import _get_inherited_hdf_nodes

        if self._is_in_memory:
            root = self._nxs_file
            self._traverse(root, visitor)
        else:
            file_path = (
                self._nxs_file[0]
                if isinstance(self._nxs_file, list)
                else self._nxs_file
            )
            root = h5py.File(file_path, "r")
            try:
                self._traverse(root, visitor)
            finally:
                root.close()
                _get_inherited_hdf_nodes.cache_clear()

    def _traverse(self, root: h5py.File, visitor: NexusVisitor) -> None:
        """Run the full traversal and call on_complete."""
        self._full_visit(root, root, "", visitor)
        visitor.on_complete(root)

    @staticmethod
    def _not_yet_visited(root: h5py.File, name: str) -> bool:
        """Return ``True`` if *name* is not an alias of an ancestor on the same path.

        Detects HDF5 hard links that would otherwise cause infinite recursion.
        When traversing an external file the path names are relative to the main
        file, so the ancestor paths may not exist in *root* — in that case the
        paths are definitely not cycles and the method returns ``True``.
        """
        parts = name.split("/")
        for idx in range(1, len(parts)):
            ancestor = "/".join(parts[:idx])
            try:
                if root["/" + ancestor] == root["/" + name]:
                    return False
            except (KeyError, ValueError):
                pass
        return True

    def _traverse_external(
        self,
        hdf_path: str,
        link: h5py.ExternalLink,
        visitor: NexusVisitor,
    ) -> None:
        """Open *link*'s target file and recursively visit its subtree.

        If the external file cannot be opened (missing, wrong format, etc.) the
        visitor's ``on_broken_link`` hook is called and traversal is skipped.
        """
        try:
            ext_root = h5py.File(link.filename, "r")
        except Exception:
            visitor.on_broken_link(hdf_path, link)
            return
        try:
            target = ext_root.get(link.path)
            if target is None:
                visitor.on_broken_link(hdf_path, link)
                return
            self._full_visit(ext_root, target, hdf_path, visitor)
        finally:
            ext_root.close()

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

        # Recurse into children — inspect link types explicitly so that broken
        # soft links and external links can be dispatched to the visitor rather
        # than crashing (h5py returns None for a broken soft link in .items()).
        if isinstance(hdf_node, h5py.Group):
            for child_name in hdf_node:
                full_name = child_name if not name else f"{name}/{child_name}"
                link = hdf_node.get(child_name, getlink=True)

                if isinstance(link, h5py.SoftLink):
                    child = hdf_node.get(child_name)  # None when target is missing
                    if child is None:
                        visitor.on_broken_link(full_name, link)
                        continue
                    if self._not_yet_visited(root, full_name):
                        self._full_visit(root, child, full_name, visitor)

                elif isinstance(link, h5py.ExternalLink):
                    visitor.on_external_link(full_name, link)
                    self._traverse_external(full_name, link, visitor)

                else:  # HardLink (or any future link type)
                    child = hdf_node[child_name]
                    if self._not_yet_visited(root, full_name):
                        self._full_visit(root, child, full_name, visitor)
