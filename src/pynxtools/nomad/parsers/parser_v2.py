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
NOMAD parser v2: annotation-based NeXus HDF5 parser using generated Python metainfo.

Replaces XML/NXDL schema resolution with:
- NexusSchemaResolver for HDF5→NXDL concept matching (variadic names, NXdata hints)
- _SectionIndex for Python annotation lookup (NeXusGroup.nx_class → SubSection)

Key differences from parser_v1:
- archive.data is the Entry/Arpes/Xps instance directly (no Root wrapper)
- One NomadVisitorV2 per NXentry; multi-NXentry files produce multiple archives
- No get_nxdl_doc() calls; no _rename_nx_for_nomad() calls
- No __field/__group suffixes in quantity names
- m_nx_data_path stored as a JSON dict directly on archive.data (the Entry instance)
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from typing import Any

import h5py
import numpy as np

try:
    from ase.data import chemical_symbols
    from nomad.atomutils import Formula
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.datamodel.results import ELN, Material, Results
    from nomad.metainfo import MSection, Package, SubSection
    from nomad.metainfo.util import MQuantity
    from nomad.parsing import MatchingParser
    from nomad.utils import get_logger
    from pint.errors import UndefinedUnitError

except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor
from pynxtools.nexus.nexus_tree import NexusNode
from pynxtools.nexus.schema_resolver import NexusSchemaResolver
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.root import Root
from pynxtools.nomad.parsers._field_io import extract_iuf_scalar, get_field_str
from pynxtools.units import ureg

# ---------------------------------------------------------------------------
# _SectionIndex: per-Section-class annotation lookup table
# ---------------------------------------------------------------------------


class _SectionIndex:
    """Annotation lookup tables for a single NOMAD Section class.

    At parse time, the visitor must answer two questions per HDF5 node:
    - "Which SubSection in this class matches an HDF5 group with NX_class='NXdetector'?"
    - "Which Quantity in this class matches an HDF5 field with concept name 'start_time'?"

    These lookups happen for every node in the file.  Scanning ``m_def.all_sub_sections``
    and inspecting each annotation on every call would be O(n) per node per depth level.
    This class pre-builds four dict-based indexes on first access, reducing all lookups
    to O(1) after the first call for a given Section class.

    The index is keyed by Section class (not instance) and cached in ``_cache``.  The
    entry for a given class is built exactly once and shared across all archives parsed
    in the same process lifetime.

    Attribute coverage (set in ``__init__``):

    ``nx_class_to_subsections``: dict[str, list[tuple]]
        Maps NX_class string → list of ``(python_name, SubSection, NeXusGroup)`` candidates,
        sorted by name specificity: "specified" (exact HDF5 name) first, then "partial"
        (prefix match), then "any" (wildcard).  Used by ``find_subsection()``.

    ``choice_subsections``: dict[tuple[str, str], tuple]
        Maps ``(group_name, nx_class)`` → ``(python_name, SubSection, NeXusChoice)`` for
        NXDL ``<choice>`` alternatives.  Used by ``find_choice_subsection()``.

    ``field_map``: dict[str, Quantity]
        Maps NXDL concept name (e.g. "DATA", "start_time") → Quantity.
        Built from ``NeXusField.name`` on each Quantity.

    ``attr_map``: dict[str, Quantity]
        Maps NXDL attribute concept name → Quantity for group-level attributes.
        Built from ``NeXusAttribute.name`` where ``parent_field`` is None.

    ``field_attr_map``: dict[str, Quantity]
        Maps ``"{field_concept}__{attr_name}"`` → Quantity for field-level attributes.
        Built from ``NeXusAttribute`` where ``parent_field`` is set.

    ``link_map``: dict[str, Quantity]
        Maps NXDL link name → Quantity(type=str) for ``<link>`` elements.
        Built from ``NeXusLink.name`` on each Quantity.
    """

    _cache: dict[type, _SectionIndex] = {}

    @classmethod
    def for_cls(cls, section_cls: Any) -> _SectionIndex:
        if section_cls not in cls._cache:
            cls._cache[section_cls] = cls(section_cls)
        return cls._cache[section_cls]

    def __init__(self, section_cls: Any) -> None:
        nx_map: dict[str, list] = defaultdict(list)
        choice_map: dict[tuple[str, str], tuple] = {}
        field_map: dict[str, Any] = {}
        attr_map: dict[str, Any] = {}
        field_attr_map: dict[str, Any] = {}
        link_map: dict[str, Any] = {}

        for subsection_name, sub in section_cls.m_def.all_sub_sections.items():
            group_annotation = sub.m_get_annotations("nexus_group")
            choice_annotation = sub.m_get_annotations("nexus_choice")
            if group_annotation:
                nx_map[group_annotation.nx_class].append(
                    (subsection_name, sub, group_annotation)
                )
            elif choice_annotation:
                key = (choice_annotation.group_name, choice_annotation.nx_class)
                choice_map[key] = (subsection_name, sub, choice_annotation)
            else:
                # Named concept SubSections carry NeXusGroup on the referenced
                # class's m_def rather than on the SubSection itself.
                try:
                    cls_annotation = sub.section_def.m_get_annotations("nexus_group")
                    if cls_annotation:
                        nx_map[cls_annotation.nx_class].append(
                            (subsection_name, sub, cls_annotation)
                        )
                except Exception:
                    pass

        _priority = {"specified": 0, "partial": 1, "any": 2}
        self.nx_class_to_subsections = {
            nx: sorted(cands, key=lambda t: _priority.get(t[2].name_type, 99))
            for nx, cands in nx_map.items()
        }
        self.choice_subsections = choice_map

        for qty in section_cls.m_def.all_quantities.values():
            field_annotation = qty.m_get_annotations("nexus_field")
            attr_annotation = qty.m_get_annotations("nexus_attribute")
            link_annotation = qty.m_get_annotations("nexus_link")
            if field_annotation:
                field_map[field_annotation.name] = qty
            elif attr_annotation:
                if attr_annotation.parent_field:
                    field_attr_map[
                        f"{attr_annotation.parent_field}__{attr_annotation.name}"
                    ] = qty
                else:
                    attr_map[attr_annotation.name] = qty
            elif link_annotation:
                link_map[link_annotation.name] = qty

        self.field_map = field_map
        self.attr_map = attr_map
        self.field_attr_map = field_attr_map
        self.link_map = link_map

    def find_subsection(
        self, nx_class: str, hdf_name: str
    ) -> tuple[str, SubSection, Any] | None:
        """Find best-matching SubSection for (nx_class, hdf_name)."""
        candidates = self.nx_class_to_subsections.get(nx_class, [])
        for subsection_name, sub, annotation in candidates:
            if annotation.name_type == "specified" and annotation.name == hdf_name:
                return subsection_name, sub, annotation
        for subsection_name, sub, annotation in candidates:
            if (
                annotation.name_type == "partial"
                and annotation.name
                and hdf_name.startswith(
                    annotation.name.replace("GROUPNAME", "").replace("NAME", "")
                )
            ):
                return subsection_name, sub, annotation
        for subsection_name, sub, annotation in candidates:
            if annotation.name_type == "any":
                return subsection_name, sub, annotation
        return None

    def find_choice_subsection(
        self, hdf_name: str, nx_class: str
    ) -> tuple[str, SubSection, Any] | None:
        return self.choice_subsections.get((hdf_name, nx_class))


# ---------------------------------------------------------------------------
# Application index: NX_class → Python class for all application definitions
# ---------------------------------------------------------------------------

# Indexed on first parse from the nexus_applications Package (the authoritative
# grouping of all generated application classes). Using the Package avoids
# re-scanning the filesystem at parse time and mirrors the way NOMAD's own
# entry-point system assembles application definitions.
#
# Keys:   NXDL nx_class string, e.g. "NXarpes"
# Values: the generated Python class, e.g. Arpes
# NX_class → Python class indexes built once from NOMAD's Package.registry.
# Any NOMAD package loaded via entry points that contains nexus_definition
# sections is included.
# In NOMAD context all NeXus packages are already in the registry when the
# parser runs (loaded via the nexus_base_classes / nexus_applications entry
# points configured in nomad.yaml).
_APP_INDEX: dict[str, type] | None = None
_BASE_CLS_BY_NX: dict[str, type | None] | None = None


def _build_nx_class_index() -> tuple[dict[str, type], dict[str, type | None]]:
    """Scan all nexus-annotated Packages in NOMAD's registry and build two indexes.

    Returns:
        app_index: nx_class → Python class for application/contributed sections
        base_index: nx_class → Python class for ALL sections with nexus_definition
    """

    app_index: dict[str, type] = {}
    base_index: dict[str, type | None] = {}
    for pkg in Package.registry.values():
        for sec_def in pkg.section_definitions:
            if sec_def.section_cls is None:
                continue
            ann = sec_def.m_get_annotations("nexus_definition")
            if ann is None:
                continue
            base_index[ann.nx_class] = sec_def.section_cls
            if ann.category in ("application", "contributed"):
                app_index[ann.nx_class] = sec_def.section_cls
    return app_index, base_index


def _get_app_index() -> dict[str, type]:
    """Return nx_class → Python class index for application/contributed definitions."""
    global _APP_INDEX, _BASE_CLS_BY_NX
    if _APP_INDEX is not None:
        return _APP_INDEX
    _APP_INDEX, _BASE_CLS_BY_NX = _build_nx_class_index()
    return _APP_INDEX


# ---------------------------------------------------------------------------
# Pre-scan visitor (stateless helper)
# ---------------------------------------------------------------------------


class _PrescanVisitor(NexusVisitor):
    """Lightweight prescan visitor that collects NXentry names and definitions.

    Does NOT create any archive sections — only reads definition fields from
    every NXentry group encountered at HDF5 root level.  Created once per file
    by NexusParserV2 before individual NomadVisitorV2 instances are dispatched.
    """

    def __init__(self) -> None:
        # {entry_hdf_name: application_definition_string or None}
        self.entry_definitions: dict[str, str | None] = {}

    def on_prescan_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        nx_class_raw = hdf_node.attrs.get("NX_class", b"")
        nx_class = (
            (
                nx_class_raw.decode()
                if isinstance(nx_class_raw, bytes)
                else str(nx_class_raw)
            )
            if nx_class_raw
            else ""
        )

        if nx_class != "NXentry":
            return

        # Only top-level NXentry groups (hdf_path has no "/" in it)
        if "/" in hdf_path:
            return

        defn: str | None = None
        defn_ds = hdf_node.get("definition")
        if defn_ds is not None and isinstance(defn_ds, h5py.Dataset):
            try:
                val = defn_ds[()]
                defn = val.decode() if isinstance(val, bytes) else str(val)
                defn = defn.strip() or None
            except Exception:
                pass

        self.entry_definitions[hdf_path] = defn

    # No-op implementations of abstract NexusVisitor methods — prescan only
    # needs on_prescan_group; the full traversal is not triggered for _PrescanVisitor.
    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        pass

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        pass

    def on_attribute(
        self, hdf_path: str, attr_name: str, attr_value: Any, parent: Any
    ) -> None:
        pass

    def on_complete(self, root: h5py.File) -> None:
        pass


# ---------------------------------------------------------------------------
# NomadVisitorV2: one instance per NXentry
# ---------------------------------------------------------------------------


class NomadVisitorV2(NexusVisitor):
    """Annotation-based NOMAD archive populator for one NXentry.

    One instance of this visitor handles exactly ONE NXentry group.
    ``NexusParserV2`` creates a separate ``NomadVisitorV2`` per NXentry and
    runs ``NexusFileHandler.process(visitor)`` for each one.

    Nodes that are not under the ``target_entry_name`` subtree are silently
    skipped.

    ``archive.data`` is set to the application class (e.g. ``Arpes``) or the
    generic ``Entry`` fallback when the NXentry group is first encountered.
    All deeper groups are resolved via _SectionIndex by their NX_class attribute.

    Uses NexusSchemaResolver for HDF5→NXDL concept matching and _SectionIndex
    for annotation-based Python quantity lookup. No XML access at parse time.
    """

    _SKIP_ATTRS: frozenset[str] = frozenset({"NX_class", "target"})

    def __init__(
        self,
        archive: EntryArchive,
        target_entry_name: str,
        entry_definition: str | None,
        nxs_fname: str,
        logger: Any,
    ) -> None:
        self._archive = archive
        self._target_entry_name = target_entry_name
        self._entry_definition = entry_definition  # e.g. "NXarpes"
        self._nxs_fname = nxs_fname
        self._logger = logger
        self._resolver = NexusSchemaResolver()

        # hdf_path → MSection (groups only, under the target entry)
        self._sections: dict[str, MSection] = {}
        # HDF5 path → archive path mapping for m_nx_data_path
        self._path_map: dict[str, str] = {}
        # hdf parent_path → (hdf_field_name, nxdl_concept_name), for on_attribute
        self._current_field_concept: dict[str, tuple[str, str]] = {}

        self.sample_class_refs: dict[str, list[MSection]] = {
            "NXsample": [],
            "NXsubstance": [],
            "NXsample_component": [],
        }

    # kept for test compatibility with the prescan API
    _entry_definitions: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Main traversal
    # ------------------------------------------------------------------

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        """Map an HDF5 group to a NOMAD Section and register it in _sections.

        Nodes not under the target NXentry are silently skipped.  When the
        target NXentry itself is encountered, ``archive.data`` is set to the
        resolved application class (e.g. ``Arpes``) or the generic ``Entry``.
        All deeper groups are resolved via _SectionIndex by their NX_class.
        """
        if hdf_path == "":
            if self._target_entry_name == "":
                # Root visitor: populate Root() with the NXroot group's own
                # attributes (file_name, creator, NeXus_version, ...).
                self._sections[hdf_path] = self._create_root_section()
            return

        group_name = hdf_path.rsplit("/", 1)[-1]
        parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""

        if not parent_path:
            # Top-level HDF5 group
            if group_name != self._target_entry_name:
                return  # Not our entry
            section = self._create_entry_section()
        else:
            if not hdf_path.startswith(self._target_entry_name + "/"):
                return  # Not under our entry
            parent_section = self._sections.get(parent_path)
            if parent_section is None:
                return
            nx_class_raw = hdf_node.attrs.get("NX_class", b"")
            nx_class = (
                (
                    nx_class_raw.decode()
                    if isinstance(nx_class_raw, bytes)
                    else str(nx_class_raw)
                )
                if nx_class_raw
                else ""
            )
            section = self._resolve_or_create_group(
                hdf_path, group_name, nx_class, parent_section
            )
            if section is not None:
                self._track_sample_refs(section, nx_class)

        if section is None:
            return
        self._sections[hdf_path] = section

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        """Populate a NOMAD Quantity from an HDF5 dataset.

        Uses NexusSchemaResolver to identify the NXDL concept (e.g. 'DATA' for a
        variadic NXdata field named 'intensity'), then looks up the matching Python
        Quantity via _SectionIndex. For NeXusLink quantities, stores the HDF5 target
        path string instead of data. For numeric arrays, stores the mean value.
        Records the HDF5→archive path mapping in self._path_map.
        """
        if (
            not hdf_path.startswith(self._target_entry_name + "/")
            and hdf_path != self._target_entry_name
        ):
            return

        field_name = hdf_path.rsplit("/", 1)[-1]
        parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""
        current = self._sections.get(parent_path)
        if current is None:
            return

        hint = _nxdata_hint(hdf_node, field_name)
        nexus_node = self._resolver.node_for(hdf_path, hdf_node, hint=hint)

        qty = self._find_quantity(current, field_name, nexus_node)
        if qty is None:
            return

        concept_name = nexus_node.name if nexus_node is not None else field_name
        self._current_field_concept[parent_path] = (field_name, concept_name)

        self._populate_field(qty, hdf_node, current, field_name, concept_name, hdf_path)

    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
    ) -> None:
        """Populate a NOMAD Quantity from an HDF5 attribute.

        NX_class and target are skipped (structural navigation only).
        Group-level attributes: resolved via NexusSchemaResolver then looked up
        in _SectionIndex.attr_map by concept name.
        Field-level attributes: looked up by key '{field_concept}__{attr_name}'
        in _SectionIndex.field_attr_map, where field_concept was set by on_field.
        """
        if attr_name in self._SKIP_ATTRS:
            return

        if isinstance(parent, h5py.Group):
            if hdf_path and not (
                hdf_path == self._target_entry_name
                or hdf_path.startswith(self._target_entry_name + "/")
            ):
                return
            current = self._sections.get(hdf_path)
            if current is None:
                return
            attr_node = self._resolver.attr_node_for(hdf_path, attr_name, parent)
            concept_name = attr_node.name if attr_node is not None else attr_name
            idx = _SectionIndex.for_cls(type(current))
            qty = idx.attr_map.get(concept_name) or idx.attr_map.get(attr_name)
        else:
            parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""
            if not (
                parent_path == self._target_entry_name
                or parent_path.startswith(self._target_entry_name + "/")
            ):
                return
            current = self._sections.get(parent_path)
            if current is None:
                return
            field_info = self._current_field_concept.get(parent_path)
            if field_info is None:
                return
            _hdf_field_name, field_concept_name = field_info
            attr_node = self._resolver.attr_node_for(hdf_path, attr_name, parent)
            attr_concept_name = attr_node.name if attr_node is not None else attr_name
            lookup_key = f"{field_concept_name}__{attr_concept_name}"
            idx = _SectionIndex.for_cls(type(current))
            qty = idx.field_attr_map.get(lookup_key)

        if qty is None:
            return

        self._populate_attribute(qty, attr_name, attr_value, current)

    def on_complete(self, root: h5py.File) -> None:
        """Store the HDF5→archive path map on archive.data after traversal."""
        entry = self._archive.data
        if entry is None:
            return
        try:
            m_nx_data_path_qty = entry.m_def.all_quantities.get("m_nx_data_path")
            if m_nx_data_path_qty is not None:
                entry.m_set(m_nx_data_path_qty, json.dumps(self._path_map))
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Section creation helpers
    # ------------------------------------------------------------------

    def _create_entry_section(self) -> MSection | None:
        """Create the Entry or application class and set as archive.data."""
        entry_cls = (
            _get_app_index().get(self._entry_definition or "")
            if self._entry_definition
            else None
        )
        if entry_cls is None:
            entry_cls = Entry

        new_entry = entry_cls()
        new_entry.__dict__["nx_name"] = self._target_entry_name
        self._archive.data = new_entry  # type: ignore[assignment]
        return new_entry

    def _create_root_section(self) -> MSection:
        """Create the Root section and set as archive.data (root visitor only)."""
        root_section = Root()
        self._archive.data = root_section  # type: ignore[assignment]
        return root_section

    def _resolve_or_create_group(
        self,
        hdf_path: str,
        group_name: str,
        nx_class: str,
        parent_section: MSection,
    ) -> MSection | None:
        """Find or create the NOMAD section for a non-NXentry HDF5 group."""
        idx = _SectionIndex.for_cls(type(parent_section))

        match = idx.find_subsection(nx_class, group_name) if nx_class else None
        if match:
            subsection_name, sub_def, ann = match
        else:
            choice = (
                idx.find_choice_subsection(group_name, nx_class) if nx_class else None
            )
            if choice:
                subsection_name, sub_def, ann = choice
            else:
                return None

        for existing in parent_section.m_get_sub_sections(sub_def):
            if existing.__dict__.get("nx_name") == group_name:
                return existing

        # Prefer the SubSection's specific class (e.g. XpsSample, ArpesInstrument)
        # over the generic NX base class.  The SubSection's section_def was chosen
        # by the application class to precisely match this group occurrence.
        # Fall back to the generic NX base class only if section_def is unavailable
        # or resolves to the same thing (e.g. for variadic base-class-only groups).
        try:
            sub_cls = sub_def.section_def.section_cls
        except Exception:
            sub_cls = None
        base_cls = _get_base_cls(nx_class) if nx_class else None
        if sub_cls is not None and (
            base_cls is None
            or (issubclass(sub_cls, base_cls) and sub_cls is not base_cls)
        ):
            final_cls: type | None = sub_cls
        elif base_cls is not None:
            final_cls = base_cls
        else:
            return None

        try:
            new_section = final_cls()
        except Exception:
            return None
        new_section.__dict__["nx_name"] = group_name
        parent_section.m_add_sub_section(sub_def, new_section)

        # Track in path map (entry-relative path)
        entry_prefix = self._target_entry_name + "/"
        rel_path = (
            hdf_path[len(entry_prefix) :]
            if hdf_path.startswith(entry_prefix)
            else hdf_path
        )
        self._path_map[rel_path] = _archive_path_for(new_section)
        return new_section

    # ------------------------------------------------------------------
    # Field / attribute population
    # ------------------------------------------------------------------

    def _find_quantity(
        self,
        current: MSection,
        hdf_field_name: str,
        nexus_node: NexusNode | None,
    ) -> Any | None:
        """Find the NOMAD Quantity for an HDF5 field in the current section.

        Priority:
        1. NeXusLink quantities — matched by link name == hdf_field_name (e.g. 'data').
        2. NexusNode concept name — e.g. NexusSchemaResolver says 'intensity' is the
           'DATA' concept, so we look up field_map['DATA'].
        3. Direct name fallback — for base-class-only files where no NexusNode is resolved;
           looks up field_map[hdf_field_name] directly.
        Returns None if no matching Quantity is found in this section.
        """
        idx = _SectionIndex.for_cls(type(current))

        link_qty = idx.link_map.get(hdf_field_name)
        if link_qty is not None:
            return link_qty

        if nexus_node is not None:
            qty = idx.field_map.get(nexus_node.name)
            if qty is not None:
                return qty

        return idx.field_map.get(hdf_field_name)

    def _populate_field(
        self,
        qty: Any,
        hdf_node: h5py.Dataset,
        current: MSection,
        hdf_field_name: str,
        concept_name: str,
        hdf_path: str,
    ) -> None:
        """Populate one NOMAD quantity from an HDF5 dataset."""
        link_ann = qty.m_get_annotations("nexus_link")
        if link_ann is not None:
            try:
                value = hdf_node.name
                if qty.use_full_storage:
                    value = MQuantity.wrap(value, hdf_field_name)
                current.m_set(qty, value)
            except Exception as e:
                self._logger.debug("Error setting link %s: %s", hdf_field_name, e)
            return

        if hdf_node.dtype.kind in "iufc" and hdf_node.dtype.itemsize > 8:
            self._logger.debug(
                "Precision %d too high for %s, skipping",
                hdf_node.dtype.itemsize,
                hdf_field_name,
            )
            return

        try:
            if hdf_node.dtype.kind in "iuf":
                if hdf_node.shape == ():
                    value = hdf_node[()]
                    if not np.isfinite(value):
                        return
                else:
                    value, _ = extract_iuf_scalar(hdf_node)
                    if not np.isfinite(float(value)):  # type: ignore[arg-type]
                        return
            elif hdf_node.dtype.kind == "c":
                value = (
                    hdf_node[(0,) * hdf_node.ndim]
                    if hdf_node.shape != ()
                    else hdf_node[()]
                )
                if not np.isfinite(value):
                    return
            elif np.issubdtype(hdf_node.dtype, np.bool_):
                raw = (
                    hdf_node[(0,) * hdf_node.ndim]
                    if hdf_node.shape != ()
                    else hdf_node[()]
                )
                value = bool(raw)
            else:
                value = get_field_str(hdf_node)
                if value is None:
                    return
        except Exception as e:
            self._logger.debug("Error reading field %s: %s", hdf_field_name, e)
            return

        unit = hdf_node.attrs.get("units", None)
        if unit is not None:
            try:
                unit_str = unit.decode() if isinstance(unit, bytes) else str(unit)
                if unit_str == "counts":
                    unit_str = "1"
                pint_unit = ureg.parse_units(unit_str)
                value = ureg.Quantity(value, pint_unit)
            except (ValueError, UndefinedUnitError, Exception):
                pass

        # Wrap scalar values in a 1-element array when the quantity expects an array.
        # NXDL often allows both scalar and array for fields like incident_energy.
        if qty.shape and not isinstance(value, (list, np.ndarray)):
            if isinstance(value, ureg.Quantity):
                value = ureg.Quantity(np.array([value.magnitude]), value.units)
            else:
                value = np.array([value])

        if qty.use_full_storage:
            value = MQuantity.wrap(value, hdf_field_name)

        try:
            current.m_set(qty, value)
        except Exception as e:
            self._logger.debug("Error setting field %s: %s", hdf_field_name, e)
            return

        # Record path mapping (entry-relative)
        entry_prefix = self._target_entry_name + "/"
        rel_path = (
            hdf_path[len(entry_prefix) :]
            if hdf_path.startswith(entry_prefix)
            else hdf_path
        )
        self._path_map[rel_path] = _archive_path_for(current) + "." + qty.name

        if qty.variable:
            name_qty = _SectionIndex.for_cls(type(current)).field_map.get(
                concept_name + "__name"
            )
            if name_qty is not None:
                try:
                    name_val = MQuantity.wrap(hdf_field_name, hdf_field_name + "__name")
                    current.m_set(name_qty, name_val)
                except Exception:
                    pass

    def _populate_attribute(
        self,
        qty: Any,
        attr_name: str,
        attr_value: Any,
        current: MSection,
    ) -> None:
        try:
            from nomad.metainfo import MEnum

            if isinstance(qty.type, MEnum):
                attribute = (
                    str(attr_value.tolist())
                    if isinstance(attr_value, np.ndarray)
                    else str(attr_value)
                )
            elif isinstance(attr_value, bytes):
                attribute = attr_value.decode("utf-8", errors="replace")
            elif isinstance(attr_value, np.ndarray):
                lst = attr_value.tolist()
                attribute = lst[0] if len(lst) == 1 else lst
            else:
                attribute = attr_value

            if qty.use_full_storage:
                attribute = MQuantity.wrap(attribute, attr_name)

            current.m_set(qty, attribute)
        except Exception as e:
            self._logger.debug("Error setting attribute %s: %s", attr_name, e)

    def _track_sample_refs(self, section: MSection, nx_class: str) -> None:
        if nx_class in self.sample_class_refs:
            self.sample_class_refs[nx_class].append(section)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_base_cls(nx_class: str) -> type | None:
    """Return the generated Python class for a given NX_class string.

    Looks up the class from NOMAD's loaded Package registry — no module
    imports or filesystem scanning.  Both indexes are built in one pass by
    _get_app_index(); calling it here ensures _BASE_CLS_BY_NX is populated.
    """
    if _BASE_CLS_BY_NX is None:
        _get_app_index()  # populates _BASE_CLS_BY_NX as a side effect
    if _BASE_CLS_BY_NX is None:
        return None
    return _BASE_CLS_BY_NX.get(nx_class)


def _nxdata_hint(hdf_node: h5py.Dataset, field_name: str) -> Any:
    """Detect NXdata signal/axis hint for a field."""
    try:
        parent = hdf_node.parent
        signal = parent.attrs.get("signal", b"")
        if isinstance(signal, bytes):
            signal = signal.decode()
        if signal == field_name:
            return "signal"
        axes_raw = parent.attrs.get("axes", None)
        if axes_raw is not None:
            if isinstance(axes_raw, bytes):
                axes_raw = axes_raw.decode()
            if isinstance(axes_raw, str) and axes_raw == field_name:
                return "axis"
            if isinstance(axes_raw, (np.ndarray, list)):
                if field_name in [
                    (a.decode() if isinstance(a, bytes) else str(a)) for a in axes_raw
                ]:
                    return "axis"
    except Exception:
        pass
    return None


def _archive_path_for(section: MSection) -> str:
    """Build a rough archive path string for a section (for path map values)."""
    parts = []
    s = section
    while s is not None:
        name = s.__dict__.get("nx_name") or type(s).__name__
        parts.append(name)
        s = getattr(s, "m_parent", None)
    return ".".join(reversed(parts))


# ---------------------------------------------------------------------------
# NexusParserV2
# ---------------------------------------------------------------------------


class NexusParserV2(MatchingParser):
    """NOMAD parser for NeXus files using Phase 2 generated Python metainfo.

    Produces one NOMAD archive entry per NXentry group.  Single-NXentry files
    produce one archive (``archive.data = Arpes()``).  Multi-NXentry files use
    NOMAD's child-archive mechanism: ``is_mainfile`` returns the additional entry
    names as child keys; NOMAD pre-creates the child archives; ``parse`` populates
    each one with a dedicated ``NomadVisitorV2`` instance.
    """

    creates_children = True

    def is_mainfile(
        self,
        filename: str,
        mime: str,
        buffer: bytes,
        decoded_buffer: str,
        compression: str | None = None,
    ) -> bool | list[str]:
        """Return list of child keys for every NeXus file (always includes 'root')."""
        if not super().is_mainfile(filename, mime, buffer, decoded_buffer, compression):
            return False

        try:
            prescan = _PrescanVisitor()
            NexusFileHandler(filename).prescan(prescan)
            entry_names = sorted(prescan.entry_definitions.keys())
        except Exception:
            return True

        if len(entry_names) == 0:
            return True

        # First entry → main archive; remaining entries + "root" → child archives.
        # "root" is always added so every NeXus file gets a grouping Root entry.
        return entry_names[1:] + ["root"]

    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger: Any = None,
        child_archives: dict[str, EntryArchive] | None = None,
    ) -> None:
        logger = logger or get_logger(__name__)
        nxs_fname = "/".join(mainfile.split("/")[6:]) or mainfile

        # Pre-scan to collect entry definitions
        prescan = _PrescanVisitor()
        NexusFileHandler(mainfile).prescan(prescan)
        entry_names = sorted(prescan.entry_definitions.keys())

        if not entry_names:
            logger.warning("No NXentry groups found in %s", nxs_fname)
            if archive.metadata is None:
                archive.metadata = EntryMetadata()
            archive.metadata.domain = "nexus"
            return

        # Build entry_name → archive mapping
        child_archives = child_archives or {}
        entry_archive_map: dict[str, EntryArchive] = {entry_names[0]: archive}
        for name in entry_names[1:]:
            if name in child_archives:
                entry_archive_map[name] = child_archives[name]

        handler = NexusFileHandler(mainfile)
        all_sample_refs: dict[str, list[MSection]] = {
            "NXsample": [],
            "NXsubstance": [],
            "NXsample_component": [],
        }

        # One visitor per entry; traverse the full file for each
        for entry_name, entry_archive in entry_archive_map.items():
            defn = prescan.entry_definitions.get(entry_name)
            visitor = NomadVisitorV2(
                archive=entry_archive,
                target_entry_name=entry_name,
                entry_definition=defn,
                nxs_fname=nxs_fname,
                logger=logger,
            )
            handler.process(visitor)

            for cls_name, refs in visitor.sample_class_refs.items():
                all_sample_refs[cls_name].extend(refs)

            self._set_entry_metadata(entry_archive, entry_name, defn, nxs_fname)

            # Chemical formula normalization
            self._normalize_results(entry_archive, visitor.sample_class_refs)

        # Create one Root (Experiment) archive per file that links all NXentry archives.
        if "root" in child_archives:
            root_archive = child_archives["root"]
            root_visitor = NomadVisitorV2(
                archive=root_archive,
                target_entry_name="",
                entry_definition=None,
                nxs_fname=nxs_fname,
                logger=logger,
            )
            handler.process(root_visitor)
            self._create_root_entry(
                root_archive,
                entry_names,
                prescan.entry_definitions,
                nxs_fname,
            )
            # Chemical formula normalization across all sub-entries
            self._normalize_results(root_archive, all_sample_refs)

    def _set_entry_metadata(
        self,
        archive: EntryArchive,
        entry_name: str,
        entry_definition: str | None,
        nxs_fname: str,
    ) -> None:
        if archive.metadata is None:
            archive.metadata = EntryMetadata()
        # Entry name = "{file stem} - {HDF5 NXentry group name}", e.g.
        # "201805_WSe2_arpes - entry". The raw HDF5 group name alone (often just
        # "entry"/"entry1") is identical across countless NeXus files and would
        # make NOMAD's entry list unreadable.
        if archive.metadata.entry_name is None:
            file_stem = os.path.splitext(os.path.basename(nxs_fname))[0]
            archive.metadata.entry_name = f"{file_stem} - {entry_name}"
        # Entry type = Python class name (e.g. "Arpes", "Xps")
        if archive.metadata.entry_type is None:
            cls_name = type(archive.data).__name__ if archive.data is not None else None
            archive.metadata.entry_type = cls_name or (entry_definition or "NeXus")
        archive.metadata.domain = "nexus"
        archive.metadata.readonly = True

    def _create_root_entry(
        self,
        root_archive: EntryArchive,
        entry_names: list[str],
        entry_definitions: dict[str, str | None],
        nxs_fname: str,
    ) -> None:
        """Populate the Root (Experiment) archive that groups all NXentries from this file."""

        # NomadVisitorV2 (target_entry_name="") already set root_archive.data to a
        # Root() populated with the NXroot HDF5 group's own attributes (file_name,
        # creator, NeXus_version, ...); reuse it instead of overwriting.
        root = root_archive.data if isinstance(root_archive.data, Root) else Root()
        root.m_entry_paths = list(entry_names)
        root_archive.data = root  # type: ignore[assignment]

        if root_archive.metadata is None:
            root_archive.metadata = EntryMetadata()
        file_stem = os.path.splitext(os.path.basename(nxs_fname))[0]
        root_archive.metadata.entry_name = f"{file_stem} (NeXus file)"
        root_archive.metadata.entry_type = "Experiment"
        root_archive.metadata.domain = "nexus"
        root_archive.metadata.readonly = True

        # Populate results.eln.methods with unique application class names.
        # Convert "NXxps" → "Xps" using the same nxdl_to_class_name() used by the generator.
        from pynxtools.nomad.converters._mapping import nxdl_to_class_name

        methods = sorted(
            {nxdl_to_class_name(d) for d in entry_definitions.values() if d is not None}
        )
        if methods:
            if root_archive.results is None:
                root_archive.results = Results()
            if root_archive.results.eln is None:
                root_archive.results.eln = ELN()
            root_archive.results.eln.methods = methods

    def _normalize_results(
        self, archive: EntryArchive, sample_refs: dict[str, list]
    ) -> None:
        if archive.results is None:
            archive.results = Results()
        if archive.results.material is None:
            archive.results.material = Material()

        formulas: set[str] = set()
        for sample in sample_refs.get("NXsample", []):
            val = getattr(sample, "chemical_formula", None)
            if val is not None:
                formulas.add(str(val))
        for substance in sample_refs.get("NXsubstance", []):
            val = getattr(substance, "molecular_formula_hill", None)
            if val is not None:
                formulas.add(str(val))

        if not formulas:
            return

        elements: set[str] = set()
        for formula_str in formulas:
            try:
                formula = Formula(formula_str)
                elements.update(formula.elements())
            except Exception:
                pass

        if elements:
            valid = [e for e in elements if e in chemical_symbols]
            archive.results.material.elements = valid
