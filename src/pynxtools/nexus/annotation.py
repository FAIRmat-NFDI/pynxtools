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
Annotation visitor for NeXus files.

`Annotator` implements `NexusVisitor` and provides the annotation
functionality of the ``read_nexus`` CLI tool: it logs schema documentation,
optionality strings, class paths, enumeration values, and NXdata axis/signal
information for every node in a NeXus file.

Three operating modes (controlled by constructor arguments):

* **Default** (both *d_inq_nd* and *c_inq_nd* are ``None``):
  Annotate every node and print the default-plottable summary.
* **-d / documentation mode** (*d_inq_nd* set):
  Annotate only the single node at the given HDF5 path.
* **-c / concept mode** (*c_inq_nd* set):
  Find all HDF5 nodes that satisfy an IS-A relation with the given
  NXDL concept path and log their paths.
"""

from __future__ import annotations

import re
import textwrap
from collections.abc import Callable
from typing import Any, Optional, Union

import h5py

from pynxtools.nexus.handler import NexusVisitor
from pynxtools.nexus.nexus import get_default_plottable
from pynxtools.nexus.nexus_tree import NexusNode, generate_tree_from
from pynxtools.nexus.nxdata import chk_nxdata_axis
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
    d_inq_nd:
        If set, only the node at this HDF5 path is annotated (``-d`` mode).
        Accepts paths with or without a leading ``/``.
    c_inq_nd:
        If set, collect all HDF5 paths whose schema IS-A the given NXDL
        concept path (``-c`` mode).  Results are logged in `on_complete`.
    parser:
        Optional callback invoked for every field and attribute that is
        present in the schema.  Used by the NOMAD parser (legacy interface).
    """

    def __init__(
        self,
        logger,
        d_inq_nd: str | None = None,
        c_inq_nd: str | None = None,
        parser: Callable | None = None,
    ) -> None:
        self.logger = logger
        self.d_inq_nd = d_inq_nd
        self.c_inq_nd = c_inq_nd
        self.parser = parser
        self.hdf_path_list_for_c_inq_nd: list[str] = []
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
        elif self.c_inq_nd is not None:
            self._handle_concept_query(hdf_path, hdf_node)

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        """Annotate a field or dispatch concept query."""
        if self._should_annotate(hdf_path):
            self._annotate_field(hdf_path, hdf_node)
        elif self.c_inq_nd is not None:
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
        if self.c_inq_nd is not None:
            for hdf_path in self.hdf_path_list_for_c_inq_nd:
                self.logger.info(hdf_path)
            return

        if self.d_inq_nd is None and self.parser is None:
            get_default_plottable(root, self.logger)

    # ------------------------------------------------------------------
    # Schema resolution — NexusNode-based
    # ------------------------------------------------------------------

    def _should_annotate(self, hdf_path: str) -> bool:
        """Return True if *hdf_path* should be annotated in the current mode."""
        if self.d_inq_nd is None and self.c_inq_nd is None:
            return True
        if self.d_inq_nd is not None and hdf_path in (
            self.d_inq_nd,
            self.d_inq_nd.lstrip("/"),
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
                    return (
                        definition.decode()
                        if isinstance(definition, bytes)
                        else str(definition)
                    )
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
        self, hdf_path: str, hdf_node: h5py.Group | h5py.Dataset
    ) -> NexusNode | None:
        """Return the NexusNode for *hdf_path*, or ``None`` if not in schema."""
        if not hdf_path:
            return None
        appdef = self._appdef_for(hdf_node)
        if appdef in ("NO NXentry found",):
            return None
        tree = self._get_tree(appdef)
        if tree is None:
            return None
        node_type = "field" if isinstance(hdf_node, h5py.Dataset) else "group"
        return tree.find_node_at_path(
            hdf_path, node_type=node_type, _cache=self._node_cache
        )

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
        return parent_node.search_add_child_for(attr_name)

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
        import logging

        self.logger.log(level, f"{det}{label:<{self._LW}}: {value}")

    def _emit_inheritance(self, det: str, node: NexusNode) -> None:
        """Emit a structured inheritance block with inline docs.

        Each level shows a precise concept path (e.g. ``NXinstrument/energy``
        for a field, ``NXinstrument`` for a base-class root).  The bare NXobject
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

        # NXdata axis/signal annotation (pure HDF5, no schema)
        chk_nxdata_axis(hdf_node, name, self.logger)

        val = (
            str(decode_if_string(hdf_node[()])).split("\n")
            if len(hdf_node.shape) <= 1
            else str(decode_if_string(hdf_node[0])).split("\n")
        )
        self._detail(
            det, "Value", f"{val[0]}{'...' if len(val) > 1 else ''}", level=10
        )  # DEBUG

        node = self._find_nexus_node(hdf_path, hdf_node)

        if node is None:
            self.logger.info(f"{det}<NOT IN SCHEMA>")
        else:
            opt_str = f"  [{node.optionality.upper()}]" if node.optionality else ""
            self._detail(det, "Concept", f"{node.concept_path}{opt_str}")
            self._emit_inheritance(det, node)

            for src, values in node.get_inheritance_enums():
                self._detail(det, "Enums", f"[{src}] {', '.join(values)}")

        if self.parser is not None:
            # Legacy NOMAD callback: still uses the old nxdl_path (list[ET.Element])
            # interface. This will be replaced when NomadVisitor is implemented.
            hdf_info = {"hdf_path": "/" + hdf_path, "hdf_node": hdf_node}
            from pynxtools.nexus.nexus import get_nxdl_doc

            _, nxdef, nxdl_path_doc = get_nxdl_doc(hdf_info, self.logger, doc=False)
            self.parser(
                {
                    "hdf_info": hdf_info,
                    "nxdef": nxdef,
                    "nxdl_path": nxdl_path_doc,
                    "val": val,
                    "logger": self.logger,
                }
            )

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
        import logging

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
        else:
            schema_tag = "  [NOT IN SCHEMA]"

        val = str(decode_if_string(attr_value)).split("\n")
        val_str = val[0] + ("..." if len(val) > 1 else "")
        self.logger.debug(f"{det}@{attr_name} = {val_str}{schema_tag}")

        if self.parser is not None and in_schema:
            # Legacy NOMAD callback: still uses the old nxdl_path interface.
            # This will be replaced when NomadVisitor is implemented.
            hdf_info = {"hdf_path": "/" + hdf_path, "hdf_node": parent}
            from pynxtools.nexus.nexus import get_nxdl_doc

            req_str, nxdef, nxdl_path = get_nxdl_doc(
                hdf_info, self.logger, doc=False, attr=attr_name
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

    # ------------------------------------------------------------------
    # File header (emitted at root group)
    # ------------------------------------------------------------------

    def _emit_file_header(self, root: h5py.Group) -> None:
        """Log a structured file-level header from HDF5 root attributes."""
        import os

        sep = "═" * 60
        self.logger.info(sep)
        fname = root.file.filename if hasattr(root, "file") else ""
        if fname:
            self.logger.info(f"{'NeXus file':<20}: {os.path.basename(fname)}")
            self.logger.info(f"{'Path':<20}: {fname}")
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
        """Collect HDF5 paths that satisfy IS-A relation with *c_inq_nd*."""
        from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nxdl_child
        from pynxtools.nexus.nexus import get_all_is_a_rel_from_hdf_node

        attributed_concept = self.c_inq_nd.split("@")
        attr = attributed_concept[1] if len(attributed_concept) > 1 else None

        elist = get_all_is_a_rel_from_hdf_node(hdf_node, "/" + hdf_path)
        if elist is None:
            return

        fnd_superclass = False
        fnd_superclass_attr = False

        for elem in reversed(elist):
            tmp_path = elem.get("nxdlbase").split(".nxdl")[0]
            con_path = "/NX" + tmp_path.split("NX")[-1] + elem.get("nxdlpath")

            if fnd_superclass or con_path == attributed_concept[0]:
                fnd_superclass = True

                if attr is None:
                    self.hdf_path_list_for_c_inq_nd.append(hdf_path)
                    break

                for attribute in hdf_node.attrs.keys():
                    attr_concept = get_nxdl_child(
                        elem, attribute, nexus_type="attribute", go_base=False
                    )
                    if attr_concept is not None and attr_concept.get(
                        "nxdlpath"
                    ).endswith(attr):
                        fnd_superclass_attr = True
                        self.hdf_path_list_for_c_inq_nd.append(
                            hdf_path + "@" + attribute
                        )
                        break

            if fnd_superclass_attr:
                break
