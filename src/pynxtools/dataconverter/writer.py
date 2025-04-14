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

import h5py
import numpy as np

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.exceptions import InvalidDictProvided
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    NxdlAttributeNotFoundError,
    get_node_at_nxdl_path,
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
def handle_dicts_entries(data, grp, entry_name, output_path, path):
    """Handle function for dictionaries found as value of the nexus file.

    Several cases can be encoutered:
    - Data to slice and place in virtual datasets
    - Concatenate dataset in one virtual dataset
    - Internal links
    - External links
    - compression label
    """
    if "link" in data:
        file, path = split_link(data, output_path)
    # generate virtual datasets from slices
    if "shape" in data.keys():
        layout = handle_shape_entries(data, file, path)
        grp.create_virtual_dataset(entry_name, layout)
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
        grp.create_virtual_dataset(entry_name, layout, fillvalue=0)
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
            grp.create_dataset(
                entry_name,
                data=data["compress"],
                compression="gzip",
                chunks=True,
                compression_opts=strength,
            )
        else:
            grp.create_dataset(entry_name, data=data["compress"])
    else:
        raise InvalidDictProvided(
            "A dictionary was provided to the template but it didn't"
            " fall into any of the know cases of handling"
            " dictionaries. This occured for: " + entry_name
        )
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
    """

    def __init__(
        self, data: dict = None, nxdl_f_path: str = None, output_path: str = None
    ):
        """Constructs the necessary objects required by the Writer class."""
        self.data = data
        self.nxdl_f_path = nxdl_f_path
        self.output_path = output_path
        self.output_nexus = h5py.File(self.output_path, "w")
        self.nxdl_data = ET.parse(self.nxdl_f_path).getroot()
        self.nxs_namespace = get_namespace(self.nxdl_data)

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
        for attr in elem.findall(f"{self.nxs_namespace}attribute"):
            name = attr.get("name")
            key = f"{path}/@{name}"
            if key in self.data:
                value = self.data[key]
                elem.attrib[name] = str(value) if isinstance(value, list) else value

        return elem.attrib

    def ensure_and_get_parent_node(self, path: str, undocumented_paths) -> h5py.Group:
        """Returns the parent if it exists for a given path else creates the parent group."""
        parent_path = path[0 : path.rindex("/")] or "/"
        parent_path_hdf5 = helpers.convert_data_dict_path_to_hdf5_path(parent_path)
        if not does_path_exist(parent_path, self.output_nexus):
            parent = self.ensure_and_get_parent_node(parent_path, undocumented_paths)
            grp = parent.create_group(parent_path_hdf5)

            attrs = self.__nxdl_to_attrs(parent_path)
            if attrs is not None:
                try:
                    grp.attrs["NX_class"] = attrs["type"]
                except KeyError as e:
                    raise NxdlAttributeNotFoundError(
                        f"NXDL attribute `type` not found for group {parent_path}.\n"
                        f"Hint: Follow the convention `fixednameVARIACKPART[fixedname_given_name]` "
                        f"with exact group name `fixednameVARIACKPART`in NXDL file."
                    ) from e

            return grp
        return self.output_nexus[parent_path_hdf5]

    def _put_data_into_hdf5(self):
        """Store data in hdf5 in in-memory file or file."""

        hdf5_links_for_later = []

        unit_and_attr = {}

        for path, d_value in self.data.items():
            if not is_not_data_empty(d_value):
                continue
            try:
                entry_name = helpers.get_name_from_data_dict_entry(
                    path[path.rindex("/") + 1 :]
                )
                if entry_name and entry_name.startswith("@"):
                    unit_and_attr[path] = d_value
                    continue

                # Handle field and group
                grp = self.ensure_and_get_parent_node(
                    path,
                    self.data.undocumented.keys(),
                )
                if isinstance(d_value, dict):
                    if "compress" in d_value.keys():
                        dataset = handle_dicts_entries(
                            d_value, grp, entry_name, self.output_path, path
                        )
                    else:
                        hdf5_links_for_later.append(
                            [d_value, grp, entry_name, self.output_path, path]
                        )
                else:
                    dataset = grp.create_dataset(entry_name, data=d_value)

            except InvalidDictProvided as exc:
                print(str(exc))
            except Exception as exc:
                raise IOError(
                    f"Unknown error occured writing the path: {path} "
                    f"with the following message: {str(exc)}\n"
                ) from exc

        for links in hdf5_links_for_later:
            dataset = handle_dicts_entries(*links)
            if dataset is None:
                # If target of a link is invalid to be linked
                del self.data[links[-1]]

        # Handle unit and attribute
        for path, d_value in unit_and_attr.items():
            if not is_not_data_empty(d_value):
                continue
            hdf5_path = helpers.convert_data_dict_path_to_hdf5_path(path)
            entry_name = helpers.get_name_from_data_dict_entry(
                path[path.rindex("/") + 1 :]
            )
            try:
                dataset_or_grp = self.ensure_and_get_parent_node(
                    path,
                    self.data.undocumented.keys(),
                )

            except KeyError as exc:
                logger.warning(
                    "No path '%s' available to attached Attribute.", hdf5_path
                )
                dataset_or_grp = None
            if dataset_or_grp is None:
                continue
            if path.endswith("/@units"):
                dataset_or_grp.attrs["units"] = d_value
            else:
                dataset_or_grp.attrs[entry_name[1:]] = d_value

    def write(self):
        """Writes the NeXus file with previously validated data from the reader with NXDL attrs."""
        try:
            self._put_data_into_hdf5()
        finally:
            self.output_nexus.close()
