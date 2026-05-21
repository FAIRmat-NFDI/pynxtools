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

from typing import Any

import h5py
import numpy as np

DEBUG_PYNXTOOLS_WITH_NOMAD = False

from pynxtools.annotator.nxdata import chk_nxdata_axis
from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor
from pynxtools.nexus.nexus_tree import NexusField, NexusGroup, NexusNode
from pynxtools.nexus.schema_resolver import NexusSchemaResolver
from pynxtools.nexus.utils import decode_if_string

try:
    from ase.data import chemical_symbols
    from nomad.atomutils import Formula
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.datamodel.data import EntryData
    from nomad.datamodel.results import Material, Results
    from nomad.metainfo import MEnum, MSection
    from nomad.metainfo.util import MQuantity, resolve_variadic_name
    from nomad.parsing import MatchingParser
    from nomad.utils import get_logger
    from pint import Unit
    from pint.errors import UndefinedUnitError
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

import pynxtools.nomad.schema_packages.schema as nexus_schema
from pynxtools.definitions.dev_tools.utils.nxdl_utils import decode_or_not
from pynxtools.nomad import FIELD_STATISTICS, get_quantity_base_name
from pynxtools.nomad import _rename_nx_for_nomad as rename_nx_for_nomad
from pynxtools.units import ureg


# noinspection SpellCheckingInspection
def _to_section(
    hdf_name: str | None,
    nx_def: str,
    nx_node: NexusNode | None,
    current: MSection,
    nx_root,
) -> MSection:
    """
    Navigate to (or create) the NOMAD MSection for the given NXDL node.

    Args:
        hdf_name : name of the HDF5 group (None for the definition root)
        nx_def   : application definition name (NOMAD-renamed)
        nx_node  : NexusNode for this element; pass None for the definition root
        current  : the parent MSection to search within
        nx_root  : the top-level nx_root MSection (for the ENTRY look-up)

    Returns:
        The MSection for the group, or *current* unchanged for fields/attributes.

    The strict mapping between metainfo and NeXus:
        Group  <-> SubSection
        Field  <-> Quantity          (no section change needed)
        Attribute <-> Quantity.Attribute  (no section change needed)
    """
    if hdf_name is None:
        # Definition root
        nomad_def_name = nx_def
    elif isinstance(nx_node, NexusGroup):
        # Group: derive the NOMAD sub-section name from the schema node.
        # Use the schema name when available; fall back to stripping the NX prefix.
        schema_name = nx_node.name if nx_node.name else nx_node.nx_class[2:].upper()
        nomad_def_name = schema_name
    else:
        # Field or attribute: no section change needed
        return current

    nomad_def_name = rename_nx_for_nomad(nomad_def_name, is_group=True)

    if current == nx_root:
        # Root level: look up or create the ENTRY sub-section
        new_def = current.m_def.all_sub_sections["ENTRY"]
        for section in current.m_get_sub_sections(new_def):
            if hdf_name is None or getattr(section, "nx_name", None) == hdf_name:
                return section
        cls = getattr(nexus_schema, nx_def, None)
        sec = cls()
        new_def_spec = sec.m_def.all_sub_sections[nomad_def_name]
        sec.m_create(new_def_spec.section_def.section_cls)
        new_section = sec.m_get_sub_section(new_def_spec, -1)
        current.ENTRY.append(new_section)
        new_section.__dict__["nx_name"] = hdf_name
    else:
        new_def = current.m_def.all_sub_sections[nomad_def_name]
        for section in current.m_get_sub_sections(new_def):
            if hdf_name is None or getattr(section, "nx_name", None) == hdf_name:
                return section
        current.m_create(new_def.section_def.section_cls)
        new_section = current.m_get_sub_section(new_def, -1)
        new_section.__dict__["nx_name"] = hdf_name

    return new_section


def _get_field_str(hdf_node: h5py.Dataset):
    """Get scalar string or stringified string array from an h5py.Dataset."""
    if h5py.check_string_dtype(hdf_node.dtype) is not None and hdf_node.dtype in (
        "S",
        "U",
        "O",
    ):
        hdf_value = hdf_node[()]

        if hdf_node.shape == ():
            if isinstance(hdf_value, bytes):
                return str(hdf_value.decode("utf-8"))
            return str(hdf_value)
        else:

            def decode_array(arr):
                # recursion unpack, convert, and flatten
                result = []
                for value in arr:
                    if isinstance(value, (np.ndarray, list)):
                        result.append(decode_array(value))
                    else:
                        result.append(str(decode_or_not(value)))
                return result

            return str(decode_array(hdf_value))


def _get_field_stats_iuf_chunked(hdf_node, use_welford: bool = False) -> dict:
    """
    Get field stats when hdf_node uses chunked storage layout
    """
    stats: dict = {}
    # with chunked-based storage summary statistics cannot be computed anymore with single
    # numpy calls, instead chunks are iterated over and here two approaches shown
    # i) double-precision naive mean (default, can face numerical robustness issues)
    # ii) Welford's algorithm which theoretically is more accurate but also much slower

    # np.mean and np.std internally promote to float(ing) when fed with "iu" typed data
    # but not so e.g. when fed dtype=np.float32 typed data, therefore here we use double
    # precision accumulators explicitly
    # we could also use a np.float128 accumulator to counter robustness issues
    # but that would make the code slower as float128 and beyond is emulated in software
    stats["__min"] = np.float64(+np.inf)
    stats["__max"] = np.float64(-np.inf)
    # required inits with use_welford == True
    n = np.int64(0)
    mean = np.float64(0.0)
    # M2 = np.float64(0.0)
    # required inits with use_welford == False
    mean_sum = np.float64(0.0)

    if not use_welford:  # naive route the default because is faster than Welford
        for chunk in hdf_node.iter_chunks():
            slab = hdf_node[chunk]  # decompresses automatically
            values = slab[np.isfinite(slab)]
            number_of_values = values.size
            if number_of_values > 0:
                stats["__min"] = np.minimum(stats["__min"], values.min())
                stats["__max"] = np.maximum(stats["__max"], values.max())

                mean_sum += np.sum(values, dtype=np.float64)
                n += np.int64(number_of_values)
        mean_result = mean_sum / np.float64(n) if n > 0 else np.float64(np.nan)
    else:
        for chunk in hdf_node.iter_chunks():
            slab = hdf_node[chunk]
            values = slab[np.isfinite(slab)]
            # copies ok, because chunks are typically in MB size range
            # irrespective of the hdf_node total size

            if values.size > 0:
                stats["__min"] = np.minimum(stats["__min"], values.min())
                stats["__max"] = np.maximum(stats["__max"], values.max())
                # true element-wise Welford update more precise but substantially slower
                # @njit, i.e. numba could make this faster but add third-party deps
                for x in values:  # inherently sequential Welford algorithm
                    value = np.float64(x)
                    n += np.int64(1)
                    delta = value - mean
                    mean += delta / np.float64(n)
                    # delta2 = value - mean
                    # M2 += delta * delta2
        mean_result = mean if n > 0 else np.float64(np.nan)

    # need to cast to correct return type
    if hdf_node.dtype.kind in "iu":
        stats["__mean"] = np.asarray(mean_result, dtype=hdf_node.dtype).item()
        stats["__min"] = np.asarray(stats["__min"], dtype=hdf_node.dtype).item()
        stats["__max"] = np.asarray(stats["__max"], dtype=hdf_node.dtype).item()
    else:  # f, always return float64
        stats["__mean"] = mean_result
        stats["__min"] = np.float64(stats["__min"])
        stats["__max"] = np.float64(stats["__max"])

    stats["__size"] = np.int64(np.size(hdf_node))
    stats["__ndim"] = np.uint8(np.ndim(hdf_node))

    return stats


def _get_field_stats_iuf_contiguous(hdf_node) -> dict:
    """
    Get field stats when hdf_node uses contiguous storage layout
    """
    stats: dict = {}

    stats["__min"] = np.float64(+np.inf)
    stats["__max"] = np.float64(-np.inf)
    n = np.int64(0)
    sum = np.float64(0.0)

    field = hdf_node[...]  # unpacking all data
    mask = np.isfinite(field)
    n_values = np.count_nonzero(mask)
    if n_values > 0:
        stats["__min"] = np.minimum(stats["__min"], np.min(field[mask]))
        stats["__max"] = np.maximum(stats["__max"], np.max(field[mask]))

        sum = np.sum(field[mask], dtype=np.float64)
        n += np.int64(n_values)
        mean_result = sum / np.float64(n) if n > 0 else np.float64(np.nan)
    else:
        mean_result = np.float64(np.nan)

    # need to cast to correct return type
    if hdf_node.dtype.kind in "iu":
        stats["__mean"] = np.asarray(mean_result, dtype=hdf_node.dtype).item()
        stats["__min"] = np.asarray(stats["__min"], dtype=hdf_node.dtype).item()
        stats["__max"] = np.asarray(stats["__max"], dtype=hdf_node.dtype).item()
    else:  # f, always return float64, possibly promoting
        stats["__mean"] = mean_result
        stats["__min"] = np.float64(stats["__min"])
        stats["__max"] = np.float64(stats["__max"])

    stats["__size"] = np.int64(np.size(hdf_node))
    stats["__ndim"] = np.uint8(np.ndim(hdf_node))

    return stats


class NomadVisitor(NexusVisitor):
    """
    Specialized NexusVisitor that populates a NOMAD archive from a NeXus/HDF5 file.

    Implements the full visitor interface, maintaining a ``_sections`` cache
    (``hdf_path → MSection``) that is populated in ``on_group``.  ``on_field``
    and ``on_attribute`` look up their parent section from the cache rather than
    re-walking the full HDF5 path on every callback.

    ``_populate_data`` (previously on ``NexusParser``) lives here so that all
    archive-population logic is co-located with the traversal state.

    ``hdf_path`` is used throughout with no leading "/".
    """

    _SKIP_ATTRS: frozenset = frozenset({"NX_class", "target"})

    def __init__(self, nx_root: MSection, nxs_fname: str, logger) -> None:
        self._nx_root = nx_root
        self._nxs_fname = nxs_fname
        self._logger = logger
        # MSections for HDF5 group in hdf_path
        self._sections: dict[str, MSection] = {}
        self._resolver = NexusSchemaResolver()
        self.sample_class_refs: dict[str, list] = {
            "NXsample": [],
            "NXsubstance": [],
            "NXsample_component": [],
        }

    # ------------------------------------------------------------------
    # NexusVisitor interface
    # ------------------------------------------------------------------

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        """Navigate to (or create) the NOMAD section for this HDF5 group."""
        if hdf_path == "":
            # Root group — anchor the nx_root section
            self._nx_root.m_set_section_attribute("m_nx_data_path", "/")
            self._nx_root.m_set_section_attribute("m_nx_data_file", self._nxs_fname)
            self._sections[""] = self._nx_root
            return

        node = self._resolver.node_for(hdf_path, hdf_node)
        if node is None:
            return

        appdef = self._resolver.appdef_for(hdf_node)
        nxdef_nomad = rename_nx_for_nomad(appdef) if appdef else None

        parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""
        parent_section = self._sections.get(parent_path)
        if parent_section is None:
            # Parent group was undocumented; skip this subtree
            return

        group_name = hdf_path.rsplit("/", 1)[-1]
        section = _to_section(
            group_name, nxdef_nomad, node, parent_section, self._nx_root
        )
        self._collect_class(section)
        section.m_set_section_attribute("m_nx_data_path", "/" + hdf_path)
        section.m_set_section_attribute("m_nx_data_file", self._nxs_fname)
        self._sections[hdf_path] = section

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        """Populate the NOMAD quantity for this HDF5 dataset."""
        field_name = hdf_path.rsplit("/", 1)[-1]
        nxdata_hint = chk_nxdata_axis(hdf_node, field_name)
        node = self._resolver.node_for(hdf_path, hdf_node, hint=nxdata_hint)
        if node is None:
            return

        parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""
        current = self._sections.get(parent_path)
        if current is None:
            return

        self._populate_field(node, hdf_node, current)

    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
    ) -> None:
        """Populate the NOMAD quantity attribute for this HDF5 attribute."""
        if attr_name in self._SKIP_ATTRS:
            return

        attr_node = self._resolver.attr_node_for(hdf_path, attr_name, parent)
        if attr_node is None:
            return

        # For a group attribute the MSection is the group itself;
        # for a field attribute it is the group that contains the field.
        if isinstance(parent, h5py.Group):
            current = self._sections.get(hdf_path)
        else:
            parent_path = hdf_path.rsplit("/", 1)[0] if "/" in hdf_path else ""
            current = self._sections.get(parent_path)
        if current is None:
            return

        self._populate_attribute(attr_node, attr_name, attr_value, parent, current)

    def on_complete(self, root: h5py.File) -> None:
        pass

    # ------------------------------------------------------------------
    # Internal helpers (previously on NexusParser)
    # ------------------------------------------------------------------

    def _collect_class(self, current: MSection) -> None:
        class_name = current.m_def.more.get("nx_type")
        if (
            class_name in self.sample_class_refs
            and current not in self.sample_class_refs[class_name]
        ):
            self.sample_class_refs[class_name].append(current)

    def _populate_field(
        self,
        node: NexusNode,
        hdf_node: h5py.Dataset,
        current: MSection,
    ) -> None:
        """Populate one NOMAD quantity from an HDF5 field dataset."""
        field_name = rename_nx_for_nomad(node.name, is_field=True)
        data_instance_name = hdf_node.name.split("/")[-1] + "__field"

        try:
            metainfo_def = resolve_variadic_name(
                current.m_def.all_quantities, field_name
            )
            is_variadic = metainfo_def.variable
        except Exception as e:
            self._logger.warning(
                f"error while setting field {data_instance_name} in {current.m_def} as no proper definition found for {field_name}",
                target_name=field_name,
                exc_info=e,
            )
            return

        # Metainfo does not support precision higher than i8, u8, f8, c16
        if hdf_node.dtype.kind in "iufc" and hdf_node.dtype.itemsize > 8:
            self._logger.warning(
                f"error while setting field {data_instance_name} in {current.m_def} precision {hdf_node.dtype.itemsize} too high for {field_name}"
            )
            return

        field_stats: dict = {}  # stats built from finite iuf arrays

        # Metainfo does not support precision higher than i8, u8, f8, c16
        # TODO: is f2 supported ? maybe silently promote to f4 or f8, maybe downcast higher
        # precision floating and complex to highest supported precision floating and complex respectively
        # TODO: emit a warning in the case of hdf_node.dtype.kind in "fc" when hdf_node.dtype.itemsize < 4
        # (e.g. when one is hitting the half-precision floats that were introduced with HDF5 2.0).
        # TODO warn in case of facing arbitrary objects or structs"
        if hdf_node.dtype.kind in "iuf":
            if hdf_node.shape != ():  # non-scalar, compute stats
                if hdf_node.chunks is not None:  # iterate over hyperslabs (chunks)
                    field_stats = _get_field_stats_iuf_chunked(hdf_node)
                else:  # load entire contiguous storage layout dataset at once
                    field_stats = _get_field_stats_iuf_contiguous(hdf_node)

                for suffix in FIELD_STATISTICS:
                    if not np.isfinite(field_stats.get(suffix, np.nan)):
                        self._logger.info(
                            f"found {suffix} non existent or not finite for integer, unsigned, or floating value",
                            target_name=field_name + "[" + data_instance_name + "]",
                        )
                        return
            
                field = field_stats["__mean"]
            else:  # scalar, no stats
                field = hdf_node[()]
                if not np.isfinite(field):
                    self._logger.info(
                        "found non-finite integer, unsigned, or floating scalar",
                        target_name=field_name + "[" + data_instance_name + "]",
                    )
                    return
        # TODO: make a second optimization round for complex numbers
        # we have not faced though high volume examples with complex numbers yet
        elif hdf_node.dtype.kind in "c":
            if hdf_node.shape != ():
                field = hdf_node[(0,) * hdf_node.ndim]
            else:
                field = hdf_node[()]
            if not np.isfinite(field):
                self._logger.info(
                    "found non finite complexfloating value",
                    target_name=field_name + "[" + data_instance_name + "]",
                )
                return
        elif np.issubdtype(hdf_node.dtype, np.bool_):
            if hdf_node.shape != ():
                field = bool(hdf_node[(0,) * hdf_node.ndim])
            else:
                field = bool(hdf_node[()])
        else:  # strings
            field = _get_field_str(hdf_node)
            if field is None:
                self._logger.info(
                    "found data of an unsupported type",
                    target_name=field_name + "[" + data_instance_name + "]",
                )
                return

        # check if unit is given
        unit = hdf_node.attrs.get("units", None)

        pint_unit: Unit | None = None
        if unit:
            try:
                if unit != "counts":
                    pint_unit = ureg.parse_units(unit)
                else:
                    pint_unit = ureg.parse_units("1")
                field = ureg.Quantity(field, pint_unit)
                if hdf_node.dtype.kind in "iuf" and hdf_node.shape != ():
                    for suffix in FIELD_STATISTICS:
                        if FIELD_STATISTICS[suffix]["mask"]:
                            field_stats[suffix] = ureg.Quantity(
                                field_stats[suffix], pint_unit
                            )

            except (ValueError, UndefinedUnitError):
                pass

        if metainfo_def.use_full_storage:
            field = MQuantity.wrap(field, data_instance_name)
        elif metainfo_def.unit is None and pint_unit is not None:
            metainfo_def.unit = pint_unit

        try:
            current.m_set(metainfo_def, field)
            field.m_set_attribute("m_nx_data_path", hdf_node.name)
            field.m_set_attribute("m_nx_data_file", self._nxs_fname)
            if is_variadic:
                concept_basename = get_quantity_base_name(field.name)
                instance_name = get_quantity_base_name(data_instance_name)
                name_metainfo_def = resolve_variadic_name(
                    current.m_def.all_quantities, concept_basename + "__name"
                )
                name_value = MQuantity.wrap(instance_name, instance_name + "__name")
                current.m_set(name_metainfo_def, name_value)
                name_value.m_set_attribute("m_nx_data_path", hdf_node.name)
                name_value.m_set_attribute("m_nx_data_file", self._nxs_fname)
            if hdf_node.dtype.kind in "iuf" and hdf_node.shape != ():
                for suffix in FIELD_STATISTICS:
                    if suffix != "__mean":
                        concept_basename = get_quantity_base_name(field.name)
                        instance_name = get_quantity_base_name(data_instance_name)
                        stat_metainfo_def = resolve_variadic_name(
                            current.m_def.all_quantities, concept_basename + suffix
                        )
                        stat = MQuantity.wrap(
                            field_stats[suffix], instance_name + suffix
                        )
                        current.m_set(stat_metainfo_def, stat)
        except Exception as e:
            self._logger.warning(
                "error while setting field",
                target_name=field_name,
                exc_info=e,
            )

    def _populate_attribute(
        self,
        attr_node: NexusNode,
        attr_name: str,
        attr_value: Any,
        parent: h5py.Group | h5py.Dataset,
        current: MSection,
    ) -> None:
        """Populate one NOMAD quantity attribute from an HDF5 attribute."""
        # Build the NOMAD metainfo quantity name for this attribute.
        # Convention (matching schema.py _create_attributes):
        #   group attribute → "___" + attr_name
        #   field attribute → field_schema_name + "___" + attr_name
        if isinstance(parent, h5py.Group):
            # Group attribute: no parent field prefix
            parent_html_base_name = ""
            parent_name = ""
        else:
            # Field attribute: parent is the h5py.Dataset
            parent_field_node = attr_node.parent
            parent_html_base_name = rename_nx_for_nomad(
                parent_field_node.name, is_field=True
            ).split("__field")[0]
            parent_name = parent.name.split("/")[-1]

        attribute_name = parent_html_base_name + "___" + attr_name
        data_instance_name = parent_name + "___" + attr_name

        metainfo_def = None
        try:
            try:
                metainfo_def = resolve_variadic_name(
                    current.m_def.all_quantities, attribute_name
                )
                attribute = attr_value
                # TODO: get unit from attribute <xxx>_units
                if isinstance(metainfo_def.type, MEnum):
                    if isinstance(attr_value, np.ndarray):
                        attribute = str(attr_value.tolist())
                    else:
                        attribute = str(attr_value)
                elif not isinstance(attr_value, str):
                    if isinstance(attr_value, np.ndarray):
                        attr_list = attr_value.tolist()
                        if len(attr_list) == 1 or attr_value.dtype.kind in "iufc":
                            attribute = attr_list[0]
                        else:
                            attribute = str(attr_list)
                if metainfo_def.use_full_storage:
                    attribute = MQuantity.wrap(attribute, data_instance_name)
            except ValueError as exc:
                self._logger.warning(
                    f"{current.m_def} has no suitable property for {parent_html_base_name} and {attr_name} as {attribute_name}",
                    target_name=attr_name,
                    exc_info=exc,
                )
                return
            current.m_set(metainfo_def, attribute)
            # attributes must be set after their parent quantity to avoid a
            # variadic-name mismatch bug in the metainfo layer
            attribute.m_set_attribute("m_nx_data_path", parent.name)
            attribute.m_set_attribute("m_nx_data_file", self._nxs_fname)
        except Exception as e:
            self._logger.warning(
                f"error while setting attribute {data_instance_name} in {current.m_def} as {metainfo_def}",
                target_name=attr_name,
                exc_info=e,
            )


class NexusParser(MatchingParser):
    """
    NexusParser doc
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.archive: EntryArchive | None = None
        self.nx_root = None
        self._logger = None
        self.nxs_fname: str = ""

    def _get_chemical_formulas(
        self, sample_class_refs: dict
    ) -> tuple[set[str], set[str]]:
        """
        Parses the descriptive chemical formula and a set of elements from a NeXus entry.
        """
        element_set: set[str] = set()
        chemical_formulas: set[str] = set()

        for sample in sample_class_refs["NXsample"]:
            if sample.get("atom_types__field") is not None:
                atom_types = sample.atom_types__field
                if isinstance(atom_types, list):
                    for symbol in atom_types:
                        if symbol in chemical_symbols[1:]:
                            element_set.add(symbol)
                        else:
                            self._logger.warn(
                                f"Ignoring {symbol} as it is not for an element from the periodic table"
                            )
                elif isinstance(atom_types, str):
                    for symbol in atom_types.replace(" ", "").split(","):
                        if symbol in chemical_symbols[1:]:
                            element_set.add(symbol)
                        else:
                            self._logger.warn(
                                f"Ignoring {symbol} as it is not for an element from the periodic table"
                            )
            if sample.get("chemical_formula__field") is not None:
                chemical_formulas.add(sample.chemical_formula__field)

        for section in sample_class_refs["NXsample_component"]:
            if section.get("chemical_formula__field") is not None:
                chemical_formulas.add(section.chemical_formula__field)

        for substance in sample_class_refs["NXsubstance"]:
            if substance.get("molecular_formula_hill__field") is not None:
                chemical_formulas.add(substance.molecular_formula_hill__field)

        return chemical_formulas, element_set

    def normalize_chemical_formula(self, chemical_formulas) -> None:
        """
        Normalizes the descriptive chemical formula into different
        representations of chemical formula if it is a valid description.
        """
        material = self.archive.m_setdefault("results.material")

        # TODO: Properly deal with multiple chemical formulas for a single entry
        if len(chemical_formulas) == 1:
            material.chemical_formula_descriptive = chemical_formulas.pop()
        elif not chemical_formulas:
            self._logger.warn("No chemical formula found")
            return
        else:
            self._logger.warn(
                f"Multiple chemical formulas found: {chemical_formulas}.\n"
                "Cannot build a comprehensive chemical formula for the entry, "
                "but will try to extract atomic elements."
            )
            for chem_formula in chemical_formulas:
                formula = Formula(chem_formula)
                material.elements = sorted(
                    set(material.elements) | set(formula.elements())
                )

        try:
            if material.chemical_formula_descriptive:
                formula = Formula(material.chemical_formula_descriptive)
                formula.populate(material, overwrite=True)
        except Exception as e:
            self._logger.warn(
                "Could not normalize chemical formula(s) in Material", exc_info=e
            )

    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: dict[str, EntryArchive] = None,
    ) -> None:
        if DEBUG_PYNXTOOLS_WITH_NOMAD:
            import debugpy  # will connect to debugger if in debug mode

            debugpy.debug_this_thread()
            # now one can anywhere place a manual breakpoint like e.g. so
            # debugpy.breakpoint()

        self.archive = archive
        self.nx_root = nexus_schema.Root()  # type: ignore # pylint: disable=no-member
        self.archive.data = self.nx_root
        self._logger = logger if logger else get_logger(__name__)

        # if filename does not follow the pattern
        # .volumes/fs/<upload type>/<upload 2char>/<upload>/<raw/arch>/[subdirs?]/<filename>
        self.nxs_fname = "/".join(mainfile.split("/")[6:]) or mainfile

        visitor = NomadVisitor(self.nx_root, self.nxs_fname, self._logger)
        NexusFileHandler(mainfile).process(visitor)

        # TODO: domain experiment could also be registered
        if archive.metadata is None:
            archive.metadata = EntryMetadata()

        # Normalize experiment type
        app_def_list = set()
        try:
            app_entries = getattr(self.nx_root, "ENTRY")
            for entry in app_entries:
                try:
                    app = entry.definition__field
                    app_def_list.add(rename_nx_for_nomad(app) if app else "Generic")
                except (AttributeError, TypeError):
                    pass
        except (AttributeError, TypeError):
            pass
        if len(app_def_list) == 0:
            app_def = "Experiment"
        else:
            app_def = (
                ", ".join(app_def_list)
                + " Experiment"
                + ("" if len(app_def_list) == 1 else "s")
            )
        if archive.metadata.entry_type is None:
            archive.metadata.entry_type = app_def
            archive.metadata.domain = "nexus"
        archive.metadata.readonly = True

        # Normalize element info
        if archive.results is None:
            archive.results = Results()
        results = archive.results

        chemical_formulas, element_set = self._get_chemical_formulas(
            visitor.sample_class_refs
        )

        if element_set:
            if results.material is None:
                results.material = Material()
            results.material.elements = sorted(
                set(results.material.elements) | element_set
            )

        if chemical_formulas and results.material is None:
            if results.material is None:
                results.material = Material()
            self.normalize_chemical_formula(chemical_formulas)
