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
"""The writer class for writing a Nexus file in accordance with a given NXDL."""

import copy
import logging
import sys
import xml.etree.ElementTree as ET

import h5py
import numpy as np

from nexusparser.tools.dataconverter import helpers
from nexusparser.tools import nexus

logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


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
    return element.tag[element.tag.index("{"):element.tag.rindex("}") + 1]


def handle_dicts_entries(data, grp, entry_name):
    """Handke function for dictionaries found as value of the nexus file.

Several cases can be encoutered:
- Internal links
- External links
- Virtual data set
"""
    if 'internal_link' in data.keys():
        grp[entry_name] = h5py.SoftLink(
            helpers.convert_data_dict_path_to_hdf5_path(data['internal_link']))
    elif 'external_link' in data.keys():
        grp[entry_name] = h5py.ExternalLink(data['external_link'],
                                            data['path_to_dataset']
                                            )
    elif 'source_file_path' in data.keys():
        total_length = 0
        sources = []
        for index, source_file in enumerate(data['source_file_path']):
            dataset_entry_key = data['dataset_path'][index]
            lenght = h5py.File(source_file, 'r')[data['dataset_path'][index]].shape
            vsource = h5py.VirtualSource(source_file, dataset_entry_key, shape=lenght)
            total_length += vsource.shape[0]
            sources.append(vsource)
        layout = h5py.VirtualLayout(shape=total_length,
                                    dtype=np.float64)
        offset = 0
        for vsource in sources:
            length = vsource.shape[0]
            layout[offset:offset + length] = vsource
            offset += length
        grp.create_virtual_dataset(entry_name, layout, fillvalue=0)
    elif 'technique' in data.keys():
        if data['technique'] == 'ellipsometry':
            my_angles = h5py.File(data['path'], 'r')['/my_test_vds'][:, 1]
            unique_angles, counts = np.unique(my_angles, return_counts=True)
            layout = h5py.VirtualLayout(shape=(counts[0],), dtype=np.float64)
            initial = 0
            for index, angle in enumerate(unique_angles):
                vsource = h5py.VirtualSource(data['path'], '/my_test_vds', shape=(my_angles.shape[0], 6))[initial:initial + counts[index], 2]
                layout[:] = vsource
                grp.create_virtual_dataset(f"psi_{angle}_vds", layout, fillvalue=0)

                vsource = h5py.VirtualSource(data['path'], '/my_test_vds', shape=(my_angles.shape[0], 6))[initial:initial + counts[index], 3]
                layout[:] = vsource
                grp.create_virtual_dataset(f"delta_{angle}_vds", layout, fillvalue=0)

                vsource = h5py.VirtualSource(data['path'], '/my_test_vds', shape=(my_angles.shape[0], 6))[initial:initial + counts[index], 0]
                layout[:] = vsource
                grp.create_virtual_dataset(f"wavelenght_{angle}_vds", layout, fillvalue=0)
                initial += counts[index]


class Writer:
    """The writer class for writing a Nexus file in accordance with a given NXDL.

    Args:
        data (dict): Dictionary containing the data to convert.
        nxdl_path (str): Path to the nxdl file to use during conversion.
        output_path (str): Path to the output Nexus file.

    Attributes:
        data (dict): Dictionary containing the data to convert.
        nxdl_path (str): Path to the nxdl file to use during conversion.
        output_path (str): Path to the output Nexus file.
        output_nexus (h5py.File): The h5py file object to manipulate output file.
        nxdl_data (dict): Stores xml data from given nxdl file to use during conversion.
        nxs_namespace (str): The namespace used in the NXDL tags. Helps search for XML children.
    """

    def __init__(self, data: dict = None, nxdl_path: str = None, output_path: str = None):
        """Constructs the necessary objects required by the Writer class."""
        self.data = data
        self.nxdl_path = nxdl_path
        self.output_path = output_path
        self.output_nexus = h5py.File(self.output_path, "w")
        self.nxdl_data = ET.parse(self.nxdl_path).getroot()
        self.nxs_namespace = get_namespace(self.nxdl_data)

    def __nxdl_to_attrs(self, path: str = '/') -> dict:
        """
        Return a dictionary of all the attributes at the given path in the NXDL and
        the required attribute values that were requested in the NXDL from the data.
        """
        nxdl_path = helpers.convert_data_converter_dict_to_nxdl_path(path)
        elem = copy.deepcopy(nexus.get_node_at_nxdl_path(nxdl_path, elem=self.nxdl_data))
        if elem is None:
            raise Exception(f"Attributes were not found for {path}. "
                            "Please check this entry in the template dictionary.")

        # Remove the name attribute as we only use it to name the HDF5 entry
        if "name" in elem.attrib.keys():
            del elem.attrib["name"]

        # Fetch values for required attributes requested by the NXDL
        for attr_name in elem.findall(f"{self.nxs_namespace}attribute"):
            elem.attrib[attr_name.get('name')] = self.data[f"{path}/@{attr_name.get('name')}"] or ''

        return elem.attrib

    def ensure_and_get_parent_node(self, path: str, undocumented_paths) -> h5py.Group:
        """Returns the parent if it exists for a given path else creates the parent group."""
        parent_path = path[0:path.rindex('/')] or '/'
        parent_path_hdf5 = helpers.convert_data_dict_path_to_hdf5_path(parent_path)
        parent_undocumented_paths = [path[0:path.rindex("/")] or "/" for path in undocumented_paths]
        if not does_path_exist(parent_path, self.output_nexus):
            parent = self.ensure_and_get_parent_node(parent_path, parent_undocumented_paths)
            grp = parent.create_group(parent_path_hdf5)
            if path not in undocumented_paths:
                attrs = self.__nxdl_to_attrs(parent_path)
                if attrs is not None:
                    grp.attrs['NX_class'] = attrs["type"]
            return grp
        return self.output_nexus[parent_path_hdf5]

    def write(self):
        """Writes the Nexus file with previously validated data from the reader with NXDL attrs."""
        for path, value in self.data.items():
            try:
                if path[path.rindex('/') + 1:] == '@units':
                    continue

                entry_name = helpers.get_name_from_data_dict_entry(path[path.rindex('/') + 1:])

                data = value if is_not_data_empty(value) else "NOT_PROVIDED"

                if entry_name[0] != "@":
                    grp = self.ensure_and_get_parent_node(path, self.data.undocumented.keys())

                    if isinstance(data, dict):
                        handle_dicts_entries(data, grp, entry_name)
                    else:
                        dataset = grp.create_dataset(entry_name, data=data)
                        units_key = f"{path}/@units"

                        if units_key in self.data.keys() and self.data[units_key] is not None:
                            dataset.attrs["units"] = self.data[units_key]
                        else:
                            dataset.attrs["units"] = "NOT_PROVIDED"
                else:
                    dataset = self.ensure_and_get_parent_node(path, self.data.undocumented.keys())
                    dataset.attrs[entry_name[1:]] = data
            except Exception as exception:
                raise Exception(f"Unkown error occured writing the path: {path} "
                                f"with the following message: {str(exception)}")

        self.output_nexus.close()
