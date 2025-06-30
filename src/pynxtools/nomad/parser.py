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

from typing import Optional

import lxml.etree as ET
import numpy as np

DEBUG_PYNXTOOLS_WITH_NOMAD = False


try:
    from ase.data import chemical_symbols
    from nomad.atomutils import Formula
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.datamodel.data import EntryData
    from nomad.datamodel.results import Material, Results
    from nomad.metainfo import MEnum, MSection
    from nomad.metainfo.util import MQuantity, MSubSectionList, resolve_variadic_name
    from nomad.parsing import MatchingParser
    from nomad.utils import get_logger
    from pint.errors import UndefinedUnitError
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

import pynxtools.nomad.schema as nexus_schema
from pynxtools.nexus.nexus import HandleNexus
from pynxtools.nomad.utils import (
    FIELD_STATISTICS,
    REPLACEMENT_FOR_NX,
    get_quantity_base_name,
)
from pynxtools.nomad.utils import _rename_nx_for_nomad as rename_nx_for_nomad
from pynxtools.units import ureg


def _to_group_name(nx_node: ET.Element):
    """
    Normalise the given group name
    """
    # assuming always upper() is incorrect, e.g. NXem_msr is a specific one not EM_MSR!
    grp_nm = nx_node.attrib.get("name", nx_node.attrib["type"][2:].upper())

    return grp_nm


# noinspection SpellCheckingInspection
def _to_section(
    hdf_name: Optional[str],
    nx_def: str,
    nx_node: Optional[ET.Element],
    current: MSection,
    nx_root,
) -> MSection:
    """
    Args:
        hdf_name : name of the hdf group/field/attribute (None for definition)
        nx_def : application definition
        nx_node : node in the nxdl.xml
        current : current section in which the new entry needs to be picked up from

    Note that if the new element did not exist, it will be created

    Returns:
        tuple: the new subsection

    The strict mapping is available between metainfo and nexus:
        Group <-> SubSection
        Field <-> Quantity
        Attribute <-> SubSection.Attribute or Quantity.Attribute

    If the given nxdl_node is a Group, return the corresponding Section.
    If the given nxdl_node is a Field, return the Section contains it.
    If the given nxdl_node is an Attribute, return the associated Section or the
    Section contains the associated Quantity.
    """

    if hdf_name is None:
        nomad_def_name = nx_def
    elif nx_node.tag.endswith("group"):
        # it is a new group
        nomad_def_name = _to_group_name(nx_node)
    else:
        # no need to change section for quantities and attributes
        return current

    nomad_def_name = rename_nx_for_nomad(nomad_def_name, is_group=True)

    if current == nx_root:
        # for groups, get the definition from the package
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
        # for groups, get the definition from the package
        new_def = current.m_def.all_sub_sections[nomad_def_name]
        for section in current.m_get_sub_sections(new_def):
            if hdf_name is None or getattr(section, "nx_name", None) == hdf_name:
                return section
        current.m_create(new_def.section_def.section_cls)
        new_section = current.m_get_sub_section(new_def, -1)
        new_section.__dict__["nx_name"] = hdf_name

    return new_section


def _get_value(hdf_node):
    """
    Get value from hdf5 node
    """

    hdf_value = hdf_node[...]
    if str(hdf_value.dtype) == "bool":
        if len(hdf_value.shape) > 0:
            return bool(hdf_value.tolist()[0])
        return bool(hdf_value)
    if hdf_value.dtype.kind in "iufc":
        return hdf_value
    if len(hdf_value.shape) > 0:
        return str([i for i in hdf_value.astype(str)])
    return hdf_node[()].decode()


class NexusParser(MatchingParser):
    """
    NexusParser doc
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.archive: Optional[EntryArchive] = None
        self.nx_root = None
        self._logger = None
        self.nxs_fname: str = ""
        self._sample_class_refs = {
            "NXsample": [],
            "NXsubstance": [],
            "NXsample_component": [],
            "NXsample_component_set": [],
        }

    def _clear_class_refs(self):
        for key in self._sample_class_refs:
            self._sample_class_refs[key] = []

    def _collect_class(self, current: MSection):
        class_name = current.m_def.more.get("nx_type")
        if (
            class_name in self._sample_class_refs
            and current not in self._sample_class_refs[class_name]
        ):
            self._sample_class_refs[class_name].append(current)

    def _populate_data(
        self, depth: int, nx_path: list, nx_def: str, hdf_node, current: MSection, attr
    ):
        """
        Populate attributes and fields
        """
        if attr:
            # it is an attribute of either field or group
            nx_root = False
            if nx_path[0] == "/":
                nx_attr = nx_path[1]
                nx_parent = nx_attr.getparent()
                nx_root = True
            else:
                nx_attr = nx_path[depth]
                nx_parent = nx_path[depth - 1]

            if isinstance(nx_attr, str):
                if nx_attr != "units":
                    # no need to handle units here as all quantities have flexible units
                    pass
            else:
                # get the name of parent (either field or group) used to set attribute
                # required by the syntax of metainfo mechanism due to
                # variadic/template quantity names

                attr_name = nx_attr.get("name")  # could be 1D array, float or int
                attr_value = hdf_node.attrs[attr_name]
                current = _to_section(attr_name, nx_def, nx_attr, current, self.nx_root)
                try:
                    if nx_root or nx_parent.tag.endswith("group"):
                        parent_html_name = ""
                        parent_name = ""
                        parent_field_name = ""
                        parent_html_base_name = ""
                    else:
                        parent_html_name = rename_nx_for_nomad(
                            nx_path[-2].get("name"), is_field=True
                        )
                        parent_name = hdf_node.name.split("/")[-1]
                        parent_field_name = parent_html_name
                        parent_html_base_name = parent_html_name.split("__field")[0]
                    attribute_name = parent_html_base_name + "___" + attr_name
                    data_instance_name = parent_name + "___" + attr_name
                    metainfo_def = None
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
                                if (
                                    len(attr_list) == 1
                                    or attr_value.dtype.kind in "iufc"
                                ):
                                    attribute = attr_list[0]
                                else:
                                    attribute = str(attr_list)
                        if metainfo_def.use_full_storage:
                            attribute = MQuantity.wrap(attribute, data_instance_name)
                    except ValueError as exc:
                        self._logger.warning(
                            f"{current.m_def} has no suitable property for {parent_field_name} and {attr_name} as {attribute_name}",
                            target_name=attr_name,
                            exc_info=exc,
                        )
                    current.m_set(metainfo_def, attribute)
                    # if attributes are set before setting the quantity, a bug can cause them being set under a wrong variadic name
                    attribute.m_set_attribute("m_nx_data_path", hdf_node.name)
                    attribute.m_set_attribute("m_nx_data_file", self.nxs_fname)
                except Exception as e:
                    self._logger.warning(
                        f"error while setting attribute {data_instance_name} in {current.m_def} as {metainfo_def}",
                        target_name=attr_name,
                        exc_info=e,
                    )
        else:  # it is a field
            field = _get_value(hdf_node)

            # get the corresponding field name
            html_name = rename_nx_for_nomad(nx_path[-1].get("name"), is_field=True)
            data_instance_name = hdf_node.name.split("/")[-1] + "__field"
            field_name = html_name
            try:
                metainfo_def = resolve_variadic_name(
                    current.m_def.all_quantities, field_name
                )
                isvariadic = metainfo_def.variable
            except Exception as e:
                self._logger.warning(
                    f"error while setting field {data_instance_name} in {current.m_def} as no proper definition found for {field_name}",
                    target_name=field_name,
                    exc_info=e,
                )
                return

            # for data arrays only statistics if not all values NINF, Inf, or NaN
            field_stats = None
            if hdf_node[...].dtype.kind in "iufc":
                if isinstance(field, np.ndarray) and field.size > 1:
                    mask = np.isfinite(field)
                    if np.any(mask):
                        field_stats = [
                            func(field[mask] if ismask else field)
                            for func, ismask in zip(
                                FIELD_STATISTICS["function"],
                                FIELD_STATISTICS["mask"],
                            )
                        ]
                        field = field_stats[0]
                        if not np.isfinite(field):
                            self._logger.info(
                                "set NaN for field of an array",
                                target_name=field_name + "[" + data_instance_name + "]",
                            )
                            return
                    else:
                        return
                else:
                    if field.size == 1 and not np.isfinite(field):
                        self._logger.info(
                            "set NaN for field of a scalar",
                            target_name=field_name + "[" + data_instance_name + "]",
                        )
                        return

            # check if unit is given
            unit = hdf_node.attrs.get("units", None)

            pint_unit: Optional[ureg.Unit] = None
            if unit:
                try:
                    if unit != "counts":
                        pint_unit = ureg.parse_units(unit)
                    else:
                        pint_unit = ureg.parse_units("1")
                    field = ureg.Quantity(field, pint_unit)
                    if field_stats is not None:
                        for i in range(len(field_stats)):
                            if FIELD_STATISTICS["mask"][i]:
                                field_stats[i] = ureg.Quantity(
                                    field_stats[i], pint_unit
                                )

                except (ValueError, UndefinedUnitError):
                    pass

            if metainfo_def.use_full_storage:
                field = MQuantity.wrap(field, data_instance_name)
            elif metainfo_def.unit is None and pint_unit is not None:
                metainfo_def.unit = pint_unit

            # may need to check if the given unit is in the allowable list
            try:
                current.m_set(metainfo_def, field)
                field.m_set_attribute("m_nx_data_path", hdf_node.name)
                field.m_set_attribute("m_nx_data_file", self.nxs_fname)
                if isvariadic:
                    concept_basename = get_quantity_base_name(field.name)
                    instancename = get_quantity_base_name(data_instance_name)
                    name_metainfo_def = resolve_variadic_name(
                        current.m_def.all_quantities, concept_basename + "__name"
                    )
                    name_value = MQuantity.wrap(instancename, instancename + "__name")
                    current.m_set(name_metainfo_def, name_value)
                    name_value.m_set_attribute("m_nx_data_path", hdf_node.name)
                    name_value.m_set_attribute("m_nx_data_file", self.nxs_fname)
                if field_stats is not None:
                    concept_basename = get_quantity_base_name(field.name)
                    instancename = get_quantity_base_name(data_instance_name)
                    for suffix, stat in zip(
                        FIELD_STATISTICS["suffix"][1:],
                        field_stats[1:],
                    ):
                        stat_metainfo_def = resolve_variadic_name(
                            current.m_def.all_quantities, concept_basename + suffix
                        )
                        stat = MQuantity.wrap(stat, instancename + suffix)
                        current.m_set(stat_metainfo_def, stat)
                        stat.m_set_attribute("m_nx_data_path", hdf_node.name)
                        stat.m_set_attribute("m_nx_data_file", self.nxs_fname)
            except Exception as e:
                self._logger.warning(
                    "error while setting field",
                    target_name=field_name,
                    exc_info=e,
                )

    def _nexus_populate(self, params: dict, attr=None):  # pylint: disable=W0613
        """
        Walks through name_list and generate nxdl nodes
        (hdf_info, nx_def, nx_path, val, logger) = params
        """

        hdf_info: dict = params["hdf_info"]
        nx_def: str = params["nxdef"]
        nx_path: list = params["nxdl_path"]

        hdf_path: str = hdf_info["hdf_path"]
        hdf_node = hdf_info["hdf_node"]
        if nx_def is not None:
            nx_def = rename_nx_for_nomad(nx_def)

        if nx_path is None or nx_path == "/":
            return

        # current: MSection = _to_section(None, nx_def, None, self.nx_root)
        current = self.nx_root
        current.m_set_section_attribute("m_nx_data_path", "/")
        current.m_set_section_attribute("m_nx_data_file", self.nxs_fname)
        depth: int = 1
        current_hdf_path = ""
        for name in hdf_path.split("/")[1:]:
            nx_node = nx_path[depth] if depth < len(nx_path) else name
            current = _to_section(name, nx_def, nx_node, current, self.nx_root)
            self._collect_class(current)
            depth += 1
            if depth < len(nx_path):
                current_hdf_path = current_hdf_path + ("/" + name)
            if nx_node is not None and isinstance(nx_node, ET._Element):
                if nx_node.tag.endswith("group"):
                    current.m_set_section_attribute("m_nx_data_path", current_hdf_path)
                    current.m_set_section_attribute("m_nx_data_file", self.nxs_fname)
        self._populate_data(depth, nx_path, nx_def, hdf_node, current, attr)

    def get_sub_element_names(self, elem: MSection):
        return elem.m_def.all_aliases.keys()

    def get_sub_elements(self, elem: MSection, type_filter: str = None):
        e_list = self.get_sub_element_names(elem)
        filtered = []
        for elem_name in e_list:
            subelem = getattr(elem, elem_name, None)
            if subelem is None:
                continue
            if type_filter:
                if not (isinstance(subelem, (MSection, MSubSectionList))):
                    continue
                if isinstance(subelem, list):
                    if len(subelem) > 0:
                        nx_type = subelem[0].m_def.nx_type
                    else:
                        continue
                else:
                    nx_type = subelem.m_def.nx_type
                if nx_type != type_filter:
                    continue
            if not isinstance(subelem, list):
                subelem = [subelem]
            for individual in subelem:
                filtered.append(individual)
        return filtered

    def _get_chemical_formulas(self) -> set[str]:
        """
        Parses the descriptive chemical formula from a nexus entry.
        """
        material = self.archive.m_setdefault("results.material")
        element_set: set[str] = set()
        chemical_formulas: set[str] = set()

        # DEBUG added here 'sample' only to test that I think the root cause
        # of the bug is that when the appdef defines at the level of the HDF5
        # only sample the current logic does not resolve it is an NXsample thus
        # not entering ever the chemical formula parsing code and not populating
        # m_nx_data_file and m_nx_data_path variables
        for sample in self._sample_class_refs["NXsample"]:
            if sample.get("atom_types__field") is not None:
                atom_types = sample.atom_types__field
                if isinstance(atom_types, list):
                    for symbol in atom_types:
                        if symbol in chemical_symbols[1:]:
                            # chemical_symbol from ase.data is ['X', 'H', 'He', ...]
                            # but 'X' is not a valid chemical symbol just trick to
                            # have array indices matching element number
                            element_set.add(symbol)
                        else:
                            self._logger.warn(
                                f"Ignoring {symbol} as it is not for an element from the periodic table"
                            )
                elif isinstance(atom_types, str):
                    for symbol in atom_types.replace(" ", "").split(","):
                        if symbol in chemical_symbols[1:]:
                            element_set.add(symbol)
                material.elements = list(set(material.elements) | element_set)
                # given that the element list will be overwritten
                # in case a single chemical formula is found we do not add
                # a chemical formula here as this anyway be correct only
                # if len(materials.element) == 1 !
            if sample.get("chemical_formula__field") is not None:
                chemical_formulas.add(sample.chemical_formula__field)

        for class_ref in (
            "NXsample_component",
            "NXsample_component_set",
        ):
            for section in self._sample_class_refs[class_ref]:
                if section.get("chemical_formula__field") is not None:
                    chemical_formulas.add(section.chemical_formula__field)

        for substance in self._sample_class_refs["NXsubstance"]:
            if substance.get("molecular_formula_hill__field") is not None:
                chemical_formulas.add(substance.molecular_formula_hill__field)

        return chemical_formulas

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
            self._logger.warn("no chemical formula found")
        else:
            self._logger.warn(
                f"multiple chemical formulas found: {chemical_formulas}.\n"
                "Cannot build a comprehensive chemical formula for the entry, "
                "but will try to extract atomic elements."
            )
            for chem_formula in chemical_formulas:
                formula = Formula(chem_formula)
                material.elements = list(
                    set(material.elements) | set(formula.elements())
                )

        try:
            if material.chemical_formula_descriptive:
                formula = Formula(material.chemical_formula_descriptive)
                formula.populate(material, overwrite=True)
        except Exception as e:
            self._logger.warn("could not normalize material", exc_info=e)

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
        self._clear_class_refs()

        # if filename does not follow the pattern
        # .volumes/fs/<upload type>/<upload 2char>/<upoad>/<raw/arch>/[subdirs?]/<filename>
        self.nxs_fname = "/".join(mainfile.split("/")[6:]) or mainfile
        nexus_helper = HandleNexus(logger, mainfile)
        nexus_helper.process_nexus_master_file(self._nexus_populate)

        # TODO: domain experiment could also be registered
        if archive.metadata is None:
            archive.metadata = EntryMetadata()

        # Normalise experiment type
        # app_defs = str(self.nx_root).split("(")[1].split(")")[0].split(",")
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

        # Normalise element info
        if archive.results is None:
            archive.results = Results()
        results = archive.results

        if results.material is None:
            results.material = Material()

        chemical_formulas = self._get_chemical_formulas()
        self.normalize_chemical_formula(chemical_formulas)
