#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
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
Annotation visitor for NeXus files.

`Annotator` implements `NexusVisitor` and provides the annotation
functionality of the ``read_nexus`` CLI tool: it logs schema documentation,
optionality strings, class paths, enumeration values, and NXdata axis/signal
information for every node in a NeXus file.

Three operating modes (controlled by constructor arguments):

* **Default** (both *documentation* and *concept* are ``None``):
  Annotate every node and print the default-plottable summary.
* **-d / documentation mode** (*documentation* set):
  Annotate only the single node at the given HDF5 path.
* **-c / concept mode** (*concept* set):
  Find all HDF5 nodes that satisfy an IS-A relation with the given
  NXDL concept path and log their paths.
"""

from __future__ import annotations

import contextlib
import logging
import os
import re
import textwrap
from collections.abc import Callable
from typing import Any, Optional, Union

import h5py

from pynxtools.annotator.nxdata import chk_nxdata_axis
from pynxtools.nexus.handler import NexusVisitor
from pynxtools.nexus.nexus import get_default_plottable
from pynxtools.nexus.nexus_tree import NexusNode, generate_tree_from
from pynxtools.nexus.utils import decode_if_string


class Annotator(NexusVisitor):
    """
    Visitor that annotates every node of a NeXus file with NXDL documentation.

    Implements the same ``on_group`` / ``on_field`` / ``on_attribute`` /
    ``on_complete`` interface as every other `NexusVisitor`, making it
    interchangeable with `ValidationVisitor` and future visitors.

    Parameters
    ----------
    logger:
        Logger used for all output.
    documentation:
        If set, only the node at this HDF5 path is annotated (``-d`` mode).
        Accepts paths with or without a leading ``/``.
    concept:
        If set, collect all HDF5 paths whose schema IS-A the given NXDL
        concept path (``-c`` mode).  Results are logged in `on_complete`.
    parser:
        Optional callback invoked for every field and attribute that is
        present in the schema.  Used by the NOMAD parser (legacy interface).
    """

    def __init__(
        self,
        logger,
        documentation: str | None = None,
        concept: str | None = None,
        parser: Callable | None = None,
    ) -> None:
        self.logger = logger
        self.documentation = documentation
        self.concept = concept
        self.parser = parser
        self._concept_matches: list[str] = []
        # Per-appdef NexusNode tree cache and path→node lookup cache
        self._tree_cache: dict[str, NexusNode | None] = {}
        self._node_cache: dict[str, NexusNode | None] = {}

    # ------------------------------------------------------------------
    # NexusVisitor interface
    # ------------------------------------------------------------------

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        """Annotate a group or dispatch concept query."""
        if self._should_annotate(hdf_path):
            self._annotate_group(hdf_path, hdf_node)
        elif self.concept is not None:
            self._handle_concept_query(hdf_path, hdf_node)

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        """Annotate a field or dispatch concept query."""
        if self._should_annotate(hdf_path):
            self._annotate_field(hdf_path, hdf_node)
        elif self.concept is not None:
            self._handle_concept_query(hdf_path, hdf_node)

        elif self.parser is not None:
            val = (
                str(decode_if_string(hdf_node[()])).split("\n")
                if len(hdf_node.shape) <= 1
                else str(decode_if_string(hdf_node[0])).split("\n")
            )

            # Legacy NOMAD callback: still uses the old nxdl_path (list[ET.Element])
            # interface. This will be replaced when NomadVisitor is implemented.
            hdf_info = {"hdf_path": "/" + hdf_path, "hdf_node": hdf_node}
            from pynxtools.nexus.nexus import get_nxdl_doc

            _, nxdef, nxdl_path_doc = get_nxdl_doc(hdf_info, doc=False)
            self.parser(
                {
                    "hdf_info": hdf_info,
                    "nxdef": nxdef,
                    "nxdl_path": nxdl_path_doc,
                    "val": val,
                    "logger": self.logger,
                }
            )

    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
    ) -> None:
        """Annotate an attribute (default / -d mode only; -c mode ignores attributes)."""
        if self._should_annotate(hdf_path):
            self._annotate_attribute(hdf_path, attr_name, attr_value, parent)

        elif self.parser is not None:
            attr_node = self._find_attr_node(hdf_path, attr_name, parent)
            in_schema = attr_node is not None
            if in_schema:
                val = str(decode_if_string(attr_value)).split("\n")

                # Legacy NOMAD callback: still uses the old nxdl_path interface.
                # This will be replaced when NomadVisitor is implemented.
                hdf_info = {"hdf_path": "/" + hdf_path, "hdf_node": parent}
                from pynxtools.nexus.nexus import get_nxdl_doc

                req_str, nxdef, nxdl_path = get_nxdl_doc(
                    hdf_info, doc=False, attr=attr_name
                )
                if req_str and "NOT IN SCHEMA" not in req_str and "None" not in req_str:
                    self.parser(
                        {
                            "hdf_info": hdf_info,
                            "nxdef": nxdef,
                            "nxdl_path": nxdl_path,
                            "val": val,
                            "logger": self.logger,
                        },
                        attr=attr_name,
                    )

    def on_complete(self, root: h5py.File) -> None:
        """Post-traversal: log -c results or print the default plottable."""
        if self.parser:
            return

        if self.concept is not None:
            for hdf_path in self._concept_matches:
                self.logger.info(hdf_path)
            return

        if self.documentation is None:
            get_default_plottable(root, self.logger)

    # ------------------------------------------------------------------
    # Schema resolution — NexusNode-based
    # ------------------------------------------------------------------

    def _should_annotate(self, hdf_path: str) -> bool:
        """Return True if *hdf_path* should be annotated in the current mode."""
        if self.parser:
            return False
        if self.documentation is None and self.concept is None:
            return True
        if self.documentation is not None and hdf_path in (
            self.documentation,
            self.documentation.lstrip("/"),
        ):
            return True
        return False

    @staticmethod
    def _appdef_for(hdf_node: h5py.Group | h5py.Dataset) -> str:
        """Walk up the HDF5 path to find the NXentry and return its ``definition`` attribute."""
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

    def _get_tree(self, appdef: str) -> NexusNode | None:
        """Return (and cache) the NexusNode tree for *appdef*."""
        if appdef not in self._tree_cache:
            try:
                self._tree_cache[appdef] = generate_tree_from(appdef)
            except Exception:
                self._tree_cache[appdef] = None
        return self._tree_cache[appdef]

    def _find_nexus_node(
        self,
        hdf_path: str,
        hdf_node: h5py.Group | h5py.Dataset,
        hint: str | None = None,
    ) -> NexusNode | None:
        """Return the NexusNode for *hdf_path*, or ``None`` if not in schema.

        Path segments are resolved one at a time.  For each intermediate group
        we read the actual ``NX_class`` attribute from the HDF5 file and pass
        it to :meth:`~pynxtools.nexus.nexus_tree.NexusNode.best_child_for` so
        that variadic schema groups (e.g. ``DETECTOR[NXdetector]``,
        ``DATA[NXdata]``, ``COLLECTION[NXcollection]``) are disambiguated
        deterministically instead of relying on ``set`` iteration order.

        The *hint* (``'signal'`` or ``'axis'``) is forwarded to
        ``best_child_for`` for the **last** path segment so that the
        NXdata ambiguity between the ``DATA`` (signal) and ``AXISNAME``
        (axis) concept nodes is resolved from the HDF5 file content.
        """
        if not hdf_path:
            return None
        if hdf_path in self._node_cache:
            return self._node_cache[hdf_path]
        appdef = self._appdef_for(hdf_node)
        if appdef in ("NO NXentry found",):
            return None
        tree = self._get_tree(appdef)
        if tree is None:
            return None
        node_type = "field" if isinstance(hdf_node, h5py.Dataset) else "group"

        h5file = hdf_node.file
        segments = [s for s in hdf_path.split("/") if s]
        current: NexusNode = tree

        for i, seg in enumerate(segments):
            cache_key = "/".join(segments[: i + 1])
            if cache_key in self._node_cache:
                cached = self._node_cache[cache_key]
                if cached is None:
                    return None
                current = cached
                continue

            is_last = i == len(segments) - 1
            seg_node_type = node_type if is_last else "group"

            # Look up the real NX_class of HDF5 groups (both intermediate AND last)
            # so we can pin the schema child selection to the correct NX class and
            # avoid the non-determinism from equally-scoring variadic nodes.
            nx_class: str | None = None
            if seg_node_type == "group":
                try:
                    h5_grp = h5file["/" + "/".join(segments[: i + 1])]
                    if isinstance(h5_grp, h5py.Group):
                        raw = h5_grp.attrs.get("NX_class", b"")
                        nx_class = decode_if_string(raw) or None
                except KeyError:
                    pass

            seg_hint = hint if is_last else None
            child = current.best_child_for(
                seg, node_type=seg_node_type, nx_class=nx_class, hint=seg_hint
            )
            # Fall back to unconstrained search if the class-constrained one
            # finds nothing (e.g. the group has no NX_class attribute).
            if child is None and nx_class is not None:
                child = current.best_child_for(
                    seg, node_type=seg_node_type, hint=seg_hint
                )

            self._node_cache[cache_key] = child
            if child is None:
                return None
            current = child

        return current

    def _find_attr_node(
        self,
        hdf_path: str,
        attr_name: str,
        parent_hdf: h5py.Group | h5py.Dataset,
    ) -> NexusNode | None:
        """Return the NexusNode for attribute *attr_name* on the node at *hdf_path*."""
        parent_node = self._find_nexus_node(hdf_path, parent_hdf)
        if parent_node is None:
            return None
        return parent_node.best_child_for(attr_name, node_type="attribute")

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _depth(hdf_path: str) -> int:
        """Return nesting depth: 0=root, 1=/entry, 2=/entry/data, ..."""
        return 0 if not hdf_path else hdf_path.count("/") + 1

    # Label width for detail lines — keeps the colon column aligned within a block.
    _LW = 10

    def _detail(self, det: str, label: str, value: str, level: int = 20) -> None:
        """Emit one labelled detail line at the given log level."""
        self.logger.log(level, f"{det}{label:<{self._LW}}: {value}")

    def _emit_inheritance(self, det: str, node: NexusNode) -> None:
        """Emit a structured inheritance block with inline docs.

        Each level shows a precise concept path (e.g. ``NXinstrument/energy``
        for a field, ``NXdetector`` for a base-class root).  The bare NXobject
        root is suppressed; named NXobject entries are shown.
        """
        levels = node.get_inheritance_concept_paths()

        if not levels:
            return

        sub = det + "  "  # indent for source names
        doc_det = sub + "  "  # indent for doc text

        self.logger.info(f"{det}{'Inheritance':<{self._LW}}:")
        for concept_label, doc_text in levels:
            self.logger.info(f"{sub}{concept_label}")
            if doc_text:
                normalized = re.sub(r"\s+", " ", doc_text).strip()
                if normalized:
                    prefix = f"{doc_det}{'Doc':<{self._LW}}: "
                    cont = " " * len(prefix)
                    self.logger.info(
                        textwrap.fill(
                            normalized,
                            width=100,
                            initial_indent=prefix,
                            subsequent_indent=cont,
                        )
                    )

    # ------------------------------------------------------------------
    # Annotation methods
    # ------------------------------------------------------------------

    def _annotate_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        """Emit a structured block for a GROUP node."""
        if not hdf_path:
            self._emit_file_header(hdf_node)
            return

        depth = self._depth(hdf_path)
        ind = "  " * depth  # node header indent
        det = ind + "  "  # detail lines indent

        nx_class = hdf_node.attrs.get("NX_class", "")
        n_members = len(hdf_node)
        class_tag = f" [{nx_class}]" if nx_class else ""

        # Blank line before every group for visual separation
        self.logger.info("")
        self.logger.info(f"{ind}GROUP /{hdf_path}{class_tag}  ({n_members} members)")

        node = self._find_nexus_node(hdf_path, hdf_node)

        if node is None:
            self.logger.info(f"{det}<NOT IN SCHEMA>")
            return

        opt_str = f"  [{node.optionality.upper()}]" if node.optionality else ""
        self._detail(det, "Concept", f"{node.concept_path}{opt_str}")
        self._emit_inheritance(det, node)

        for src, values in node.get_inheritance_enums():
            self._detail(det, "Enums", f"[{src}] {', '.join(values)}")

    def _annotate_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        """Emit a structured block for a FIELD node."""
        depth = self._depth(hdf_path)
        ind = "  " * depth
        det = ind + "  "

        name = hdf_path.rsplit("/", maxsplit=1)[-1]
        self.logger.info(
            f"{ind}FIELD /{hdf_path}  shape={hdf_node.shape}  dtype={hdf_node.dtype}"
        )

        # NXdata axis/signal annotation — also returns a hint for schema lookup.
        # Pass self.logger so the debug messages appear in the caller's log.
        nxdata_hint = chk_nxdata_axis(hdf_node, name, indent=det, logger=self.logger)

        val = (
            str(decode_if_string(hdf_node[()])).split("\n")
            if len(hdf_node.shape) <= 1
            else str(decode_if_string(hdf_node[0])).split("\n")
        )
        self._detail(
            det, "Value", f"{val[0]}{'...' if len(val) > 1 else ''}", level=10
        )  # DEBUG

        node = self._find_nexus_node(hdf_path, hdf_node, hint=nxdata_hint)

        if node is None:
            self.logger.info(f"{det}<NOT IN SCHEMA>")
        else:
            opt_str = f"  [{node.optionality.upper()}]" if node.optionality else ""
            self._detail(det, "Concept", f"{node.concept_path}{opt_str}")
            self._emit_inheritance(det, node)

            for src, values in node.get_inheritance_enums():
                self._detail(det, "Enums", f"[{src}] {', '.join(values)}")

    # Structural HDF5 attributes that carry no annotation value
    _SKIP_ATTRS: frozenset = frozenset({"NX_class", "target"})

    def _annotate_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
    ) -> None:
        """Emit a DEBUG line for an attribute; skip structural HDF5 attributes."""
        if not hdf_path or attr_name in self._SKIP_ATTRS:
            return

        depth = self._depth(hdf_path)
        ind = "  " * depth
        det = ind + "  "

        attr_node = self._find_attr_node(hdf_path, attr_name, parent)
        in_schema = attr_node is not None
        if in_schema:
            opt_label = attr_node.optionality.upper()
            schema_tag = f"  [{opt_label}]" if opt_label else ""
        elif attr_name == "units" and isinstance(parent, h5py.Dataset):
            # @units on a field is valid whenever the field carries a unit category
            # in NXDL (e.g. NX_ENERGY). No explicit <attribute name="units"> child
            # exists in the schema XML — the constraint is expressed as the field
            # element's "units" XML attribute (e.g. units="NX_ENERGY").
            parent_node = self._find_nexus_node(hdf_path, parent)
            unit_cat = (
                getattr(parent_node, "unit", "") if parent_node is not None else ""
            )
            if unit_cat:
                schema_tag = f"  [UNIT: {unit_cat}]"
                in_schema = True
            else:
                schema_tag = "  [NOT IN SCHEMA]"
        else:
            schema_tag = "  [NOT IN SCHEMA]"

        val = str(decode_if_string(attr_value)).split("\n")
        val_str = val[0] + ("..." if len(val) > 1 else "")
        self.logger.debug(f"{det}@{attr_name} = {val_str}{schema_tag}")

    # ------------------------------------------------------------------
    # File header (emitted at root group)
    # ------------------------------------------------------------------

    def _emit_file_header(self, root: h5py.Group) -> None:
        """Log a structured file-level header from HDF5 root attributes."""
        sep = "═" * 60
        self.logger.info(sep)
        fname = root.file.filename if hasattr(root, "file") else ""
        if fname:
            self.logger.info(f"{'NeXus file':<20}: {os.path.basename(fname)}")
        for key in ("file_time", "HDF5_Version", "h5py_version", "nexusformat_version"):
            val = root.attrs.get(key)
            if val is not None:
                self.logger.info(f"{key:<20}: {decode_if_string(val)}")
        self.logger.info(sep)

    # ------------------------------------------------------------------
    # Concept query (-c mode)
    # ------------------------------------------------------------------

    def _handle_concept_query(
        self,
        hdf_path: str,
        hdf_node: h5py.Group | h5py.Dataset,
    ) -> None:
        """Collect HDF5 paths whose schema IS-A *concept*.

        Two query forms are supported:

        **Bare class name** (e.g. ``NXbeam``):
            Matches HDF5 *groups* whose ``NX_class`` attribute equals *concept*
            exactly.  Fields are not matched — a field carries no ``NX_class``
            attribute and its class membership can only be determined from schema
            context.  Full IS-A chain traversal for base classes (e.g. querying
            ``NXobject`` to match all groups) is not yet supported.

        **Appdef path** (e.g. ``NXarpes/ENTRY/INSTRUMENT/analyser``):
            Matches both groups and fields whose schema concept path (resolved
            against the file's application definition) includes *concept* in its
            inheritance chain.  Requires the file to declare an application
            definition via the ``definition`` field in its NXentry group.

        .. note::
            Querying fields in base-class-only files (no application definition)
            is not yet supported.  Only groups can be matched via their
            ``NX_class`` attribute in that case.
        """
        parts = self.concept.split("@")
        target = parts[0]
        attr = parts[1] if len(parts) > 1 else None

        # Bare class name (e.g. "NXbeam"): match groups by HDF5 NX_class attribute.
        # generate_tree_from only supports application definitions, so full IS-A
        # chain traversal for base classes (e.g. querying "NXobject" to find all
        # groups) is not yet implemented. Exact class match only.
        if "/" not in target and isinstance(hdf_node, h5py.Group):
            nx_class = decode_if_string(hdf_node.attrs.get("NX_class", b""))
            if nx_class != target:
                return
        else:
            node = self._find_nexus_node(hdf_path, hdf_node)
            if node is None:
                return
            chain = [label for label, _ in node.get_inheritance_concept_paths()]
            if target not in chain:
                return

        if attr is None:
            self._concept_matches.append(hdf_path)
            return

        for attribute in hdf_node.attrs.keys():
            attr_node = self._find_attr_node(hdf_path, str(attribute), hdf_node)
            if attr_node is not None and attr_node.name == attr:
                self._concept_matches.append(hdf_path + "@" + str(attribute))
