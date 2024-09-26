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
"""The writer class for writing a NeXus file in accordance with a given NXDL."""

# pylint: disable=R0912

import copy
import logging
import xml.etree.ElementTree as ET
from typing import Optional

import h5py
import numpy as np
from docutils.core import publish_string

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.exceptions import InvalidDictProvided
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    NxdlAttributeNotFoundError,
    get_node_at_nxdl_path,
    get_inherited_nodes,
)

logger = logging.getLogger("pynxtools")  # pylint: disable=C0103


def does_path_exist(path, h5py_obj) -> bool:
    """Returns true if the requested path exists in the given h5py object."""
    try:
        h5py_obj[helpers.convert_data_dict_path_to_hdf5_path(path)]  # pylint: disable=W0106
        return True
    except KeyError:
        return False


def is_not_data_empty(value) -> bool:
    """Returns True if value is an Numpy array or not None."""
    if isinstance(value, np.ndarray) or value is not None:
        return True
    return False


def get_namespace(element) -> str:
    """Extracts the namespace for elements in the NXDL"""
    return element.tag[element.tag.index("{") : element.tag.rindex("}") + 1]


def split_link(data, output_path):
    """Handle the special syntax used in the reader for the dataset links.

    Split the file:path variable in two variables file and path.
    If multiple datasets are provided, the function returns two lists"""

    if not isinstance(data["link"], list):
        if ":" in data["link"]:
            file = data["link"].split(":", 1)[0]
            path = data["link"].split(":", 1)[1]
        elif ":" not in data["link"]:
            file = output_path
            path = data["link"]
    else:
        file = []
        path = []
        for dataset in data["link"]:
            if ":" in dataset:
                file.append(dataset.split(":", 1)[0])
                path.append(dataset.split(":", 1)[1])
            elif ":" not in data["link"]:
                file.append(output_path)
                path.append(dataset)

    return file, path


def handle_shape_entries(data, file, path):
    """slice generation via the key shape"""
    new_shape = []
    for dim, val in enumerate(data["shape"]):
        if isinstance(val, slice):
            start = val.start if val.start is not None else 0
            stop = (
                val.stop
                if val.stop is not None
                else h5py.File(file, "r")[path].shape[dim]
            )
            step = val.step if val.step is not None else 1
            new_shape.append(int((stop - start) / step))
    if not new_shape:
        new_shape = [1]
    layout = h5py.VirtualLayout(shape=tuple(new_shape), dtype=np.float64)
    vsource = h5py.VirtualSource(file, path, shape=h5py.File(file, "r")[path].shape)[
        data["shape"]
    ]
    layout[:] = vsource
    return layout


# pylint: disable=too-many-locals, inconsistent-return-statements
def handle_dicts_entries(data, grp, entry_name, output_path, path, docs):
    """Handle function for dictionaries found as value of the nexus file.

    Several cases can be encoutered:
    - Data to slice and place in virtual datasets
    - Concatenate dataset in one virtual dataset
    - Internal links
    - External links
    - compression label"""
    if "link" in data:
        file, path = split_link(data, output_path)
    # generate virtual datasets from slices
    if "shape" in data.keys():
        layout = handle_shape_entries(data, file, path)
        dataset = grp.create_virtual_dataset(entry_name, layout)
    # multiple datasets to concatenate
    elif "link" in data.keys() and isinstance(data["link"], list):
        total_length = 0
        sources = []
        for index, source_file in enumerate(file):
            vsource = h5py.VirtualSource(
                source_file,
                path[index],
                shape=h5py.File(source_file, "r")[path[index]].shape,
            )
            total_length += vsource.shape[0]
            sources.append(vsource)
        layout = h5py.VirtualLayout(shape=total_length, dtype=np.float64)
        offset = 0
        for vsource in sources:
            layout[offset : offset + vsource.shape[0]] = vsource
            offset += vsource.shape[0]
        dataset = grp.create_virtual_dataset(entry_name, layout, fillvalue=0)
    # internal and external links
    elif "link" in data.keys():
        if ":/" not in data["link"]:
            grp[entry_name] = h5py.SoftLink(path)  # internal link
        else:
            grp[entry_name] = h5py.ExternalLink(file, path)  # external link
    elif "compress" in data.keys():
        if not (isinstance(data["compress"], str) or np.isscalar(data["compress"])):
            strength = 9  # strongest compression is space efficient but can take long
            accept = (
                ("strength" in data.keys())
                and (isinstance(data["strength"], int))
                and (data["strength"] >= 0)
                and (data["strength"] <= 9)
            )
            if accept is True:
                strength = data["strength"]
            dataset = grp.create_dataset(
                entry_name,
                data=data["compress"],
                compression="gzip",
                chunks=True,
                compression_opts=strength,
            )
        else:
            dataset = grp.create_dataset(entry_name, data=data["compress"])
    else:
        raise InvalidDictProvided(
            "A dictionary was provided to the template but it didn't"
            " fall into any of the know cases of handling"
            " dictionaries. This occured for: " + entry_name
        )

    if docs:
        try:
            dataset.attrs["docs"] = docs
        except NameError:
            pass

    # Check whether link has been stabilished or not
    try:
        return grp[entry_name]
    except KeyError:
        logger.warning("No path '%s' available to be linked.", path)
        del grp[entry_name]
        return None


class Writer:
    """The writer class for writing a NeXus file in accordance with a given NXDL.

    Args:
        data (dict): Dictionary containing the data to convert.
        nxdl_f_path (str): Path to the nxdl file to use during conversion.
        output_path (str): Path to the output NeXus file.

    Attributes:
        data (dict): Dictionary containing the data to convert.
        nxdl_f_path (str): Path to the nxdl file to use during conversion.
        output_path (str): Path to the output NeXus file.
        output_nexus (h5py.File): The h5py file object to manipulate output file.
        nxdl_data (dict): Stores xml data from given nxdl file to use during conversion.
        nxs_namespace (str): The namespace used in the NXDL tags. Helps search for XML children.
        write_docs (bool): Write docs for the individual NeXus concepts as HDF5 attributes.
    """

    def __init__(
        self,
        data: dict = None,
        nxdl_f_path: str = None,
        output_path: str = None,
    ):
        """Constructs the necessary objects required by the Writer class."""
        self.data = data
        self.nxdl_f_path = nxdl_f_path
        self.output_path = output_path
        self.output_nexus = h5py.File(self.output_path, "w")
        self.nxdl_data = ET.parse(self.nxdl_f_path).getroot()
        self.nxs_namespace = get_namespace(self.nxdl_data)

        self.write_docs: bool = False
        self.docs_format: str = "default"

    def __nxdl_to_attrs(self, path: str = "/") -> dict:
        """
        Return a dictionary of all the attributes at the given path in the NXDL and
        the required attribute values that were requested in the NXDL from the data.

        If an NXDL attribute was not found, it returns None.
        """
        nxdl_path = helpers.convert_data_converter_dict_to_nxdl_path(path)

        try:
            elem = get_node_at_nxdl_path(nxdl_path, elem=copy.deepcopy(self.nxdl_data))
        except NxdlAttributeNotFoundError:
            return None

        # Remove the name attribute as we only use it to name the HDF5 entry
        if "name" in elem.attrib.keys():
            del elem.attrib["name"]

        # Fetch values for required attributes requested by the NXDL
        for attr_name in elem.findall(f"{self.nxs_namespace}attribute"):
            key = f"{path}/@{attr_name.get('name')}"
            if key in self.data:
                elem.attrib[attr_name.get("name")] = self.data[key]

        return elem.attrib

    def __nxdl_docs(self, path: str = "/") -> Optional[str]:
        """Get the NXDL docs for a path in the data."""

        def rst_to_html(rst_text: str) -> str:
            """
            Convert reStructuredText to HTML using Docutils.

            Args:
                rst_text (str): The input RST text to be converted.

            Returns:
                str: The resulting HTML content.
            """
            return publish_string(rst_text, writer_name="html").decode("utf-8")

        def extract_and_format_docs(elem: ET.Element) -> str:
            """Get the docstring for a given element in the NDXL tree."""
            docs_elements = elem.findall(f"{self.nxs_namespace}doc")
            if docs_elements:
                docs = docs_elements[0].text
                if self.docs_format != "default":
                    docs = publish_string(docs, writer_name=self.docs_format).decode(
                        "utf-8"
                    )
                print(docs.strip().replace("\\n", "\n"))
                return docs.strip().replace("\\n", "\n")
            return ""

        docs: str = ""

        if not self.write_docs:
            return None

        nxdl_path = helpers.convert_data_converter_dict_to_nxdl_path(path)

        if nxdl_path == "/ENTRY":
            # Special case for docs of application definition
            app_def_docs = extract_and_format_docs(self.nxdl_data)
            if app_def_docs:
                return app_def_docs

        _, _, elist = get_inherited_nodes(nxdl_path, elem=copy.deepcopy(self.nxdl_data))

        for elem in elist:
            if not docs:
                # Only use docs from superclasses if they are not extended.
                docs += extract_and_format_docs(elem)

        if not elist:
            # Handle docs for attributeS
            (_, inherited_nodes, _) = get_inherited_nodes(
                nxdl_path, elem=copy.deepcopy(self.nxdl_data)
            )
            attrs = inherited_nodes[-1].findall(f"{self.nxs_namespace}attribute")
            for attr in attrs:
                if attr.attrib["name"] == path.split("@")[-1]:
                    docs += extract_and_format_docs(attr)

        return docs

    def ensure_and_get_parent_node(self, path: str, undocumented_paths) -> h5py.Group:
        """Returns the parent if it exists for a given path else creates the parent group."""
        parent_path = path[0 : path.rindex("/")] or "/"
        parent_path_hdf5 = helpers.convert_data_dict_path_to_hdf5_path(parent_path)
        if not does_path_exist(parent_path, self.output_nexus):
            parent = self.ensure_and_get_parent_node(parent_path, undocumented_paths)
            grp = parent.create_group(parent_path_hdf5)

            attrs = self.__nxdl_to_attrs(parent_path)

            if attrs is not None:
                grp.attrs["NX_class"] = attrs["type"]

            docs = self.__nxdl_docs(parent_path)
            if docs:
                grp.attrs["docs"] = docs

            return grp
        return self.output_nexus[parent_path_hdf5]

    def _put_data_into_hdf5(self):
        """Store data in hdf5 in in-memory file or file."""

        hdf5_links_for_later = []

        def add_units_key(dataset, path):
            units_key = f"{path}/@units"
            if units_key in self.data.keys() and self.data[units_key] is not None:
                dataset.attrs["units"] = self.data[units_key]

        for path, value in self.data.items():
            docs = self.__nxdl_docs(path)

            try:
                if path[path.rindex("/") + 1 :] == "@units":
                    continue

                entry_name = helpers.get_name_from_data_dict_entry(
                    path[path.rindex("/") + 1 :]
                )
                if is_not_data_empty(value):
                    data = value
                else:
                    continue

                if entry_name[0] != "@":
                    grp = self.ensure_and_get_parent_node(
                        path, self.data.undocumented.keys()
                    )

                    if isinstance(data, dict):
                        if "compress" in data.keys():
                            dataset = handle_dicts_entries(
                                data, grp, entry_name, self.output_path, path, docs
                            )

                        else:
                            hdf5_links_for_later.append(
                                [data, grp, entry_name, self.output_path, path, docs]
                            )
                    else:
                        dataset = grp.create_dataset(entry_name, data=data)
                        if docs:
                            dataset.attrs["docs"] = docs

            except InvalidDictProvided as exc:
                print(str(exc))
            except Exception as exc:
                raise IOError(
                    f"Unknown error occured writing the path: {path} "
                    f"with the following message: {str(exc)}"
                ) from exc

        for links in hdf5_links_for_later:
            dataset = handle_dicts_entries(*links)
            if dataset is None:
                # If target of a link is invalid to be linked
                del self.data[links[-1]]

        for path, value in self.data.items():
            docs = self.__nxdl_docs(path)
            try:
                if path[path.rindex("/") + 1 :] == "@units":
                    continue

                entry_name = helpers.get_name_from_data_dict_entry(
                    path[path.rindex("/") + 1 :]
                )
                if is_not_data_empty(value):
                    data = value
                else:
                    continue

                if entry_name[0] != "@":
                    path_hdf5 = helpers.convert_data_dict_path_to_hdf5_path(path)

                    add_units_key(self.output_nexus[path_hdf5], path)
                else:
                    dataset = self.ensure_and_get_parent_node(
                        path, self.data.undocumented.keys()
                    )
                    dataset.attrs[entry_name[1:]] = data
                    if docs:
                        # Write docs for attributes like <attr>__docs
                        dataset.attrs[f"{entry_name[1:]}__docs"] = docs
            except Exception as exc:
                raise IOError(
                    f"Unknown error occured writing the path: {path} "
                    f"with the following message: {str(exc)}"
                ) from exc

    def write(self, write_docs: bool = False, docs_format: str = "default"):
        """
        Writes the NeXus file with previously validated data from the reader with NXDL attrs.

        Args:
            write_docs (bool): Write docs for the individual NeXus concepts as HDF5 attributes. The default is False.
        """
        self.write_docs = write_docs
        self.docs_format = docs_format
        try:
            self._put_data_into_hdf5()
        finally:
            self.output_nexus.close()
