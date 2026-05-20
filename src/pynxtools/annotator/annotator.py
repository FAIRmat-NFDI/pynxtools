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

import logging
import os
import re
import textwrap
from typing import Any

import h5py

from pynxtools.annotator.nxdata import chk_nxdata_axis
from pynxtools.nexus.handler import NexusVisitor
from pynxtools.nexus.nexus import get_default_plottable
from pynxtools.nexus.nexus_tree import NexusNode
from pynxtools.nexus.schema_resolver import NexusSchemaResolver
from pynxtools.nexus.utils import decode_if_string


class Annotator(NexusVisitor):
    """
    Visitor that annotates every node of a NeXus file with NXDL documentation.

    Implements the same ``on_group`` / ``on_field`` / ``on_attribute`` /
    ``on_complete`` interface as every other `NexusVisitor`, making it
    interchangeable with `ValidationVisitor` and `NomadVisitor`.

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
    """

    def __init__(
        self,
        logger,
        documentation: str | None = None,
        concept: str | None = None,
    ) -> None:
        self.logger = logger
        self.documentation = documentation
        self.concept = concept
        self._concept_matches: list[str] = []
        self._resolver = NexusSchemaResolver()

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

    def on_complete(self, root: h5py.File) -> None:
        """Post-traversal: log -c results or print the default plottable."""
        if self.concept is not None:
            for hdf_path in self._concept_matches:
                self.logger.info(hdf_path)
            return

        if self.documentation is None:
            get_default_plottable(root, self.logger)

    # ------------------------------------------------------------------
    # Dispatch documentation (``-d``) and concept (``-c``) mode
    # ------------------------------------------------------------------

    def _should_annotate(self, hdf_path: str) -> bool:
        """Return True if *hdf_path* should be annotated in the current mode."""
        if self.documentation is None and self.concept is None:
            return True
        if self.documentation is not None and hdf_path in (
            self.documentation,
            self.documentation.lstrip("/"),
        ):
            return True
        return False

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _depth(hdf_path: str) -> int:
        """Return nesting depth: 0=root, 1=/entry, 2=/entry/data, ..."""
        return 0 if not hdf_path else hdf_path.count("/")

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

        node = self._resolver.node_for(hdf_path, hdf_node)

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

        node = self._resolver.node_for(hdf_path, hdf_node, hint=nxdata_hint)

        if node is None:
            self.logger.info(f"{det}<NOT IN SCHEMA>")
        else:
            opt_str = f"  [{node.optionality.upper()}]" if node.optionality else ""
            self._detail(det, "Concept", f"{node.concept_path}{opt_str}")
            self._emit_inheritance(det, node)

            for src, values in node.get_inheritance_enums():
                self._detail(det, "Enums", f"[{src}] {', '.join(values)}")

    # Structural HDF5 attributes that carry no annotation value.
    _SKIP_ATTRS: frozenset = frozenset({"NX_class"})

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

        # @target is a blanket NeXus link convention (not per-concept in NXDL) —
        # always annotate it as a link regardless of whether a schema node exists.
        if attr_name == "target":
            val = str(decode_if_string(attr_value)).split("\n")
            val_str = val[0] + ("..." if len(val) > 1 else "")
            self.logger.debug(f"{det}@target = {val_str}  [NeXus link]")
            return

        attr_node = self._resolver.attr_node_for(hdf_path, attr_name, parent)
        in_schema = attr_node is not None
        if in_schema:
            opt_label = attr_node.optionality.upper()
            schema_tag = f"  [{opt_label}]" if opt_label else ""
        elif attr_name == "units" and isinstance(parent, h5py.Dataset):
            # @units on a field is valid whenever the field carries a unit category
            # in NXDL (e.g. NX_ENERGY). No explicit <attribute name="units"> child
            # exists in the schema XML — the constraint is expressed as the field
            # element's "units" XML attribute (e.g. units="NX_ENERGY").
            parent_node = self._resolver.node_for(hdf_path, parent)
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
        """Log a structured file-level header with the filename and all NXroot attributes.

        Each root attribute is annotated with its optionality from the NXroot base
        class schema, matching the format used for all other attributes in the output.
        """
        sep = "═" * 60
        # depth-0 detail indent: matches what _annotate_attribute uses for root-level nodes
        det = "  "
        self.logger.info(sep)
        fname = root.file.filename if hasattr(root, "file") else ""
        if fname:
            self._detail("", "NeXus file", os.path.basename(fname))
        self.logger.info("")
        self.logger.info("GROUP / [NXroot]")
        nxroot_tree = self._resolver.tree_for("NXroot")
        for attr_name, attr_value in root.attrs.items():
            if attr_name in self._SKIP_ATTRS:
                continue
            val_str = str(decode_if_string(attr_value)).split("\n")[0]
            attr_node = (
                nxroot_tree.best_child_for(attr_name, node_type="attribute")
                if nxroot_tree is not None
                else None
            )
            schema_tag = (
                f"  [{attr_node.optionality.upper()}]"
                if attr_node is not None
                else "  [NOT IN SCHEMA]"
            )
            self.logger.info(f"{det}@{attr_name} = {val_str}{schema_tag}")

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
            node = self._resolver.node_for(hdf_path, hdf_node)
            if node is None:
                return
            chain = [label for label, _ in node.get_inheritance_concept_paths()]
            if target not in chain:
                return

        if attr is None:
            self._concept_matches.append(hdf_path)
            return

        for attribute in hdf_node.attrs.keys():
            attr_node = self._resolver.attr_node_for(hdf_path, str(attribute), hdf_node)
            if attr_node is not None and attr_node.name == attr:
                self._concept_matches.append(hdf_path + "@" + str(attribute))
