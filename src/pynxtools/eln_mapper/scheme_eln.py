"""This module intended to generate schema eln which usually randeredto NOMAD."""

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

from typing import Any, Dict

import lxml.etree as ET
import yaml

from pynxtools.dataconverter.helpers import remove_namespace_from_tag
from pynxtools.eln_mapper.eln import retrieve_nxdl_file

NEXUS_TYPE_TO_NUMPY_TYPE = {
    "NX_CHAR": {
        "convert_typ": "str",
        "component_nm": "StringEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "NX_BOOLEAN": {
        "convert_typ": "bool",
        "component_nm": "BoolEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "NX_DATE_TIME": {
        "convert_typ": "Datetime",
        "component_nm": "DateTimeEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "NX_FLOAT": {
        "convert_typ": "np.float64",
        "component_nm": "NumberEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "NX_INT": {
        "convert_typ": "int",
        "component_nm": "NumberEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "NX_NUMBER": {
        "convert_typ": "np.float64",
        "component_nm": "NumberEditQuantity",
        "default_unit_display": "<No Default unit>",
    },
    "<NO FILED TYPE>": {
        "convert_typ": "<NO FILED TYPE>",
        "component_nm": "<No Edit Quantity>",
        "default_unit_display": "<No Default unit>",
    },
}


def construct_field_structure(fld_elem, quntities_dict):
    """Construct field structure such as unit, value.
    Parameters
    ----------
    elem : _type_
        _description_
    quntities_dict : _type_
        _description_
    """
    elm_attr = fld_elem.attrib
    fld_nm = elm_attr["name"].lower()
    quntities_dict[fld_nm] = {}
    fld_dict = quntities_dict[fld_nm]

    # handle type
    if "type" in elm_attr:
        nx_fld_typ = elm_attr["type"]
    else:
        nx_fld_typ = "NX_CHAR"

    if nx_fld_typ in NEXUS_TYPE_TO_NUMPY_TYPE:
        cov_fld_typ = NEXUS_TYPE_TO_NUMPY_TYPE[nx_fld_typ]["convert_typ"]

    fld_dict["type"] = cov_fld_typ
    if "units" in elm_attr:
        fld_dict["unit"] = f"<hint: {elm_attr['units']}>"
        fld_dict["value"] = "<ADD default value>"

    # handle m_annotation
    m_annotation = {
        "m_annotations": {
            "eln": {
                "component": NEXUS_TYPE_TO_NUMPY_TYPE[nx_fld_typ]["component_nm"],
                "defaultDisplayUnit": (
                    NEXUS_TYPE_TO_NUMPY_TYPE[nx_fld_typ]["default_unit_display"]
                ),
            }
        }
    }
    fld_dict.update(m_annotation)

    # handle description
    construct_decription(fld_elem, fld_dict)


def construct_decription(elm: ET._Element, concept_dict: Dict) -> None:
    """Collect doc from concept doc."""
    desc_text = ""
    for child_elm in elm:
        tag = remove_namespace_from_tag(child_elm.tag)
        if tag == "doc":
            desc_text = child_elm.text
            desc_text = " ".join([x.strip() for x in desc_text.split("\n")])
            break

    concept_dict["description"] = desc_text


def construct_group_structure(grp_elm: ET._Element, subsections: Dict) -> None:
    """To construct group structure as follows:
    <group_name>:
        section:
            m_annotations:
                eln:
                    overview: true

    Parameters
    ----------
    elm : ET._Element
        Group element
    subsections : Dict
        Dict to include group recursively
    """

    default_m_annot = {"m_annotations": {"eln": {"overview": True}}}

    elm_attrib = grp_elm.attrib
    grp_desig = ""
    if "name" in elm_attrib:
        grp_desig = elm_attrib["name"].capitalize()
    elif "type" in elm_attrib:
        grp_desig = elm_attrib["type"][2:].capitalize()

    subsections[grp_desig] = {}
    grp_dict = subsections[grp_desig]

    # add setion in group
    grp_dict["section"] = {}
    section = grp_dict["section"]
    section.update(default_m_annot)

    # pass the grp elment for recursive search
    scan_xml_element_recursively(grp_elm, section)


def _should_skip_iteration(elm: ET._Element) -> bool:
    """Define some elements here that should be skipped.

    Parameters
    ----------
    elm : ET._Element
        The element to investigate to skip
    """
    attr = elm.attrib
    elm_type = ""
    if "type" in attr:
        elm_type = attr["type"]
        if elm_type in ["NXentry"]:
            return True
    return False


def scan_xml_element_recursively(
    nxdl_element: ET._Element,
    recursive_dict: Dict,
    root_name: str = "",
    reader_name: str = "<READER_NAME>",
    is_root: bool = False,
) -> None:
    """Scan xml elements, and pass the element to the type of element handaler.

    Parameters
    ----------
    nxdl_element : ET._Element
        This xml element that will be scanned through the descendants.
    recursive_dict : Dict
        A dict that store hierarchical structure of scheme eln.
    root_name : str, optional
        Name of root that user want to see to name their application, e.g. MPES,
        by default 'ROOT_NAME'
    reader_name : Prefered name of the reader.
    is_root : bool, optional
        Declar the elment as root or not, by default False
    """

    if is_root:
        # Note for later: crate a new function to handle root part
        nxdl = "NX<NAME>.nxdl"
        recursive_dict[root_name] = {
            "base_sections": [
                "nomad.datamodel.metainfo.eln.NexusDataConverter",
                "nomad.datamodel.data.EntryData",
            ]
        }

        m_annotations: Dict = {
            "m_annotations": {
                "template": {"reader": reader_name, "nxdl": nxdl},
                "eln": {"hide": []},
            }
        }

        recursive_dict[root_name].update(m_annotations)

        recursive_dict = recursive_dict[root_name]

    # Define quantities for taking care of field
    quantities: Dict = None
    subsections: Dict = None
    for elm in nxdl_element:
        tag = remove_namespace_from_tag(elm.tag)
        # To skip NXentry group but only consider the child elments
        if _should_skip_iteration(elm):
            scan_xml_element_recursively(elm, recursive_dict)
            continue
        if tag == "field":
            if quantities is None:
                recursive_dict["quantities"] = {}
                quantities = recursive_dict["quantities"]
            construct_field_structure(elm, quantities)
        if tag == "group":
            if subsections is None:
                recursive_dict["sub_sections"] = {}
                subsections = recursive_dict["sub_sections"]
            construct_group_structure(elm, subsections)


def get_eln_recursive_dict(recursive_dict: Dict, nexus_full_file: str) -> None:
    """Develop a recursive dict that has hierarchical structure of scheme eln.

    Parameters
    ----------
    recursive_dict : Dict
        A dict that store hierarchical structure of scheme eln.
    nexus_full_file : str
        Full path of NeXus file e.g. <full_path>/paNXmpes.nxdl.xml
    """

    nxdl_root = ET.parse(nexus_full_file).getroot()
    root_name = (
        nxdl_root.attrib["name"][2:] if "name" in nxdl_root.attrib else "<ROOT_NAME>"
    )
    recursive_dict["definitions"] = {"name": "<ADD PREFERED NAME>", "sections": {}}
    sections = recursive_dict["definitions"]["sections"]

    scan_xml_element_recursively(nxdl_root, sections, root_name=root_name, is_root=True)


def generate_scheme_eln(nexus_def: str, eln_file_name: str = None) -> None:
    """Generate schema eln that should go to Nomad while running the reader.
    The output file will be <eln_file_name>.scheme.archive.yaml

    Parameters
    ----------
    nexus_def : str
        Name of nexus definition e.g. NXmpes
    eln_file_name : str
        Name of output file e.g. mpes

    Returns:
        None
    """

    file_parts: list = []
    out_file_ext = "scheme.archive.yaml"
    raw_name = ""
    out_file = ""

    nxdl_file = retrieve_nxdl_file(nexus_def)

    if eln_file_name is None:
        # raw_name from e.g. /<path>/NXmpes.nxdl.xml
        raw_name = nxdl_file.split("/")[-1].split(".")[0][2:]
        out_file = ".".join([raw_name, out_file_ext])
    else:
        file_parts = eln_file_name.split(".")
        if len(file_parts) == 1:
            raw_name = file_parts[0]
            out_file = ".".join([raw_name, out_file_ext])
        elif len(file_parts) == 4 and ".".join(file_parts[1:]) == out_file_ext:
            out_file = eln_file_name
        elif nexus_def[0:2] == "NX":
            raw_name = nexus_def[2:]
            out_file = ".".join([raw_name, out_file_ext])
        else:
            raise ValueError("Check for correct NeXus definition and output file name.")

    recursive_dict: Dict[str, Any] = {}
    get_eln_recursive_dict(recursive_dict, nxdl_file)

    with open(out_file, mode="w", encoding="utf-8") as out_f:
        yaml.dump(recursive_dict, sort_keys=False, stream=out_f)
