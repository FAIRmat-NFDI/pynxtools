"""
XRD file parser collection.
"""

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

from typing import Dict, Tuple, Optional, List

from pathlib import Path
import warnings
import xml.etree.ElementTree as ET  # for XML parsing
from pynxtools.dataconverter.helpers import (
    transform_to_intended_dt,
    remove_namespace_from_tag,
)
from pynxtools.dataconverter.readers.xrd.xrd_helper import feed_xrdml_to_template


def fill_slash_sep_dict_from_nested_dict(
    parent_path: str, nested_dict: dict, slash_sep_dict: dict
):
    """Convert a nested dict into slash separated dict.

    Extend slash_sep_dict by key (slash separated key) from nested dict.

    Parameters
    ----------
    parent_path : str
        Parent path to be appended at the starting of slash separated key.
    nested_dict : dict
        Dict nesting other dict.
    slash_sep_dict : dict
        Plain dict to be extended by key value generated from nested_dict.
    """
    for key, val in nested_dict.items():
        slash_sep_path = parent_path + key
        if isinstance(val, dict):
            fill_slash_sep_dict_from_nested_dict(slash_sep_path, val, slash_sep_dict)
        else:
            slash_sep_dict[slash_sep_path] = val


class IgnoreNodeTextWarning(Warning):
    """Special class to warn node text skip."""


class XRDMLParser:
    """Parser for xrdml file with the help of other XRD library e.g. panalytical_xml."""

    def __init__(self, file_path):
        """Construct XRDMLParser obj.

        Parameters
        ----------
        file_path : str
            Path of the file.
        """
        # In future it can be utilised later it different versions of file
        # self.__version = None
        self.__xrd_dict = {}
        self.__file_path = file_path
        self.xrdml_version: str = ""
        self.xml_root = ET.parse(self.__file_path).getroot()
        self.find_version()
        # Important note for key-val pair separator list: preceding elements have precedence on the
        # on the following elements
        self.key_val_pair_sprtr = (";", ",")
        # Important note for key-val separator list: preceding elements have precedence on the
        # on the following elements
        self.key_val_sprtr = ("=", ":")

    def find_version(self):
        """To find xrdml file version."""
        schema_loc = "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        # str: 'http://www.xrdml.com/XRDMeasurement/1.5
        version = self.xml_root.get(schema_loc).split(" ")[0]
        self.xrdml_version = version.split("/")[-1]

    def get_slash_separated_xrd_dict(self):
        """Return a dict with slash separated key and value from xrd file.

        The key is the slash separated string path for nested xml elements.

        Returns
        -------
        dict:
            Dictionary where key maps xml nested elements by slash separated str.
        """
        # To navigate different functions in future according to some parameters
        # such as version, and data analysis module from panalytical_xml
        self.handle_with_panalytical_module()
        return self.__xrd_dict

    def handle_with_panalytical_module(self):
        """Handeling XRDml file by parsing xml file and Pnanalytical_xml parser

        Panalytical module extends and constructs some array data from experiment settings
        comes with xml file.
        """
        self.parse_each_elm(parent_path="/", xml_node=self.xml_root)
        nested_data_dict: Dict[str, any] = {}
        # Note: To use panalytical lib
        # Extract other numerical data e.g. 'hkl', 'Omega', '2Theta', CountTime etc
        # using panalytical_xml module
        # parsed_data = XRDMLFile(self.__file_path)
        # nested_data_dict = parsed_data.scan.ddict
        fill_slash_sep_dict_from_nested_dict("/", nested_data_dict, self.__xrd_dict)

    def process_node_text(self, parent_path, node_txt) -> None:
        """Processing text of node

        Parameters
        ----------
        parent_path : str
            Starting str of the key when forming a string key.
        node_txt : str
            text from node.

        Returns
        ------
        None
        """
        key_val_pairs = []
        # get key-val pair
        for sep in self.key_val_pair_sprtr:
            if sep in node_txt:
                key_val_pairs.extend(node_txt.split(sep))
                break
        # Separate key-val, build full path and
        # store them in dict
        if key_val_pairs:
            for key_val in key_val_pairs:
                for k_v_sep in self.key_val_sprtr:
                    if k_v_sep in key_val:
                        key, val = key_val.split(k_v_sep)
                        key = key.replace(" ", "")
                        self.__xrd_dict["/".join([parent_path, key])] = val
                        break
        # Handling array data comes as node text
        else:
            try:
                self.__xrd_dict[parent_path] = transform_to_intended_dt(node_txt)
            except ValueError:
                warnings.warn(
                    f"Element text {node_txt} is ignored from parseing!",
                    IgnoreNodeTextWarning,
                )

    def parse_each_elm(
        self,
        parent_path,
        xml_node,
        multi_childs_tag: str = "",
        tag_extensions: Optional[List[int]] = None,
    ):
        """Check each xml element and send the element to intended function.

        Parameters
        ----------
        parent_path : str
            Path to be in the starting of the key composing from element e.g. '/'.
        xml_node : XML.Element
            Any element except process instruction nodes.
        multi_childs_tag : str
            Tag that is available on several child nodes.
        tag_extension : List[int]
            List of extension of the child tag if there are several childs having the same
            tag.

        Returns
        ------
        None
        """

        tag = remove_namespace_from_tag(xml_node.tag)
        # Take care of special node of 'entry' tag
        if tag == "entry":
            parent_path = self.parse_entry_elm(
                parent_path, xml_node, multi_childs_tag, tag_extensions
            )
        else:
            parent_path = self.parse_general_elm(
                parent_path, xml_node, multi_childs_tag, tag_extensions
            )

        _, multi_childs_tag = self.has_multi_childs_with_same_tag(xml_node)
        # List of tag extensions for child nodes which have the same tag.
        tag_extensions = [0]
        for child in iter(xml_node):
            if child is not None:
                self.parse_each_elm(
                    parent_path, child, multi_childs_tag, tag_extensions
                )

    def has_multi_childs_with_same_tag(
        self, parent_node: ET.Element
    ) -> Tuple[bool, str]:
        """Check for multiple childs that have the same tag.

        Parameter:
        ----------
        parent_node : ET.Element
            Parent node that might has multiple childs with the same tag.

        Returns:
        --------
        Tuple[bool, str]
            (true if multiple childs with the same tag, tag).
        """
        tag: str = None
        for child in iter(parent_node):
            temp_tag = remove_namespace_from_tag(child.tag)
            if tag is None:
                tag = temp_tag
            else:
                if tag == temp_tag:
                    return (True, tag)

        return (False, "")

    def parse_general_elm(
        self, parent_path, xml_node, multi_childs_tag, tag_extensions: List[int]
    ):
        """Handle general element except entry element.
        Parameters
        ----------
        parent_path : str
            Path to be in the starting of the key composing from element e.g. '/'.
        xml_node : XML.Element
            Any element except process instruction and entry nodes.
        multi_childs_tag : str
            Tag that is available on several siblings.
        tag_extension : List[int]
            List of extension of the shiblings tag if there are several shiblings having
            the same tag.

        Returns
        -------
        None
        """

        tag = remove_namespace_from_tag(xml_node.tag)
        if tag == multi_childs_tag:
            new_ext = tag_extensions[-1] + 1
            tag = tag + "_" + str(new_ext)
            tag_extensions.append(new_ext)

        if parent_path == "/":
            parent_path = parent_path + tag
        else:
            # New parent path ends with element tag
            parent_path = "/".join([parent_path, tag])

        node_attr = xml_node.attrib
        if node_attr:
            for key, val in node_attr.items():
                # Some attr has namespace
                key = remove_namespace_from_tag(key)
                key = key.replace(" ", "_")
                path_extend = "/".join([parent_path, key])
                self.__xrd_dict[path_extend] = val

        node_txt = xml_node.text
        if node_txt:
            self.process_node_text(parent_path, node_txt)

        return parent_path

    def parse_entry_elm(
        self,
        parent_path: str,
        xml_node: ET.Element,
        multi_childs_tag: str,
        tag_extensions: List[int],
    ):
        """Handle entry element.

        Parameters
        ----------
        parent_path : str
            Path to be in the starting of the key composing from element e.g. '/'.
        xml_node : XML.Element
            Any entry node.
        multi_childs_tag : str
            Tag that is available on several siblings.
        tag_extension : List[int]
            List of extension of the shiblings tag if there are several shiblings having
            the same tag.

        Returns
        -------
        str:
            Parent path.
        """

        tag = remove_namespace_from_tag(xml_node.tag)

        if tag == multi_childs_tag:
            new_ext = tag_extensions[-1] + 1
            tag_extensions.append(new_ext)
            tag = tag + "_" + str(new_ext)

        if parent_path == "/":
            parent_path = "/" + tag
        else:
            # Parent path ends with element tag
            parent_path = "/".join([parent_path, tag])

        node_attr = xml_node.attrib
        if node_attr:
            for key, val in node_attr.items():
                # Some attributes have namespace
                key = remove_namespace_from_tag(key)
                path_extend = "/".join([parent_path, key])
                self.__xrd_dict[path_extend] = val

        # In entry element text must get special care on it
        node_txt = xml_node.text
        if node_txt:
            self.process_node_text(parent_path, node_txt)

        return parent_path


class FormatParser:
    """A class to identify and parse different file formats."""

    def __init__(self, file_path):
        """Construct FormatParser obj.

        Parameters
        ----------
        file_path : str
            XRD file to be parsed.

        Returns
        -------
        None
        """
        self.file_path = file_path
        self.file_parser = XRDMLParser(self.file_path)
        # termilnological name of file to read config file
        self.file_term = "xrdml_" + self.file_parser.xrdml_version

    def get_file_format(self):
        """Identifies the format of a given file.

        Returns:
        --------
        str:
            The file extension of the file.
        """
        file_extension = "".join(Path(self.file_path).suffixes)
        return file_extension

    def parse_xrdml(self):
        """Parses a Panalytical XRDML file.

        Returns
        -------
        dict
            A dictionary containing the parsed XRDML data.
        """
        return self.file_parser.get_slash_separated_xrd_dict()

    def parse_panalytical_udf(self):
        """Parse the Panalytical .udf file.

        Returns
        -------
        None
            Placeholder for parsing .udf files.
        """

    def parse_bruker_raw(self):
        """Parse the Bruker .raw file.

        Returns
        None
        """

    def parse_bruker_xye(self):
        """Parse the Bruker .xye file.

        Returns
        None
        """

    # pylint: disable=import-outside-toplevel
    def parse_and_populate_template(self, template, config_dict, eln_dict):
        """Parse xrd file into dict and fill the template.

        Parameters
        ----------
        template : Template
            NeXus template generated from NeXus application definitions.
        xrd_file : str
            Name of the xrd file.
        config_dict : dict
            A dict geenerated from python
        eln_dict : dict
            A dict generatd from eln yaml file.
        Returns:
        None
        """

        xrd_dict = self.parse()
        if len(config_dict) == 0 and self.file_parser.xrdml_version == "1.5":
            from pynxtools.dataconverter.readers.xrd.config import xrdml

            config_dict = xrdml
        feed_xrdml_to_template(
            template,
            xrd_dict,
            eln_dict,
            file_term=self.file_term,
            config_dict=config_dict,
        )

    def parse(self):
        """Parses the file based on its format.

        Returns:
        dict
            A dictionary containing the parsed data.

        Raises:
            ValueError: If the file format is unsupported.
        """
        file_format = self.get_file_format()
        slash_sep_dict = {}
        if file_format == ".xrdml":
            slash_sep_dict = self.parse_xrdml()
        # elif file_format == ".udf":
        #     return self.parse_panalytical_udf()
        # elif file_format == ".raw":
        #     return self.parse_bruker_raw()
        # elif file_format == ".xye":
        #     return self.parse_bruker_xye()
        # else:
        #     raise ValueError(f"Unsupported file format: {file_format}")
        return slash_sep_dict


def parse_and_fill_template(template, xrd_file, config_dict, eln_dict):
    """Parse xrd file and fill the template with data from that file.

    Parameters
    ----------
    template : Template[dict]
        Template gnenerated from nxdl definition.
    xrd_file : str
        Name of the xrd file with extension
    config_dict : Dict
        Dictionary from config.json or similar file.
    eln_dict : Dict
        Plain and '/' separated dictionary from yaml for ELN.
    """

    format_parser = FormatParser(xrd_file)
    format_parser.parse_and_populate_template(template, config_dict, eln_dict)
