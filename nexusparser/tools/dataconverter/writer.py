"""The writer class for writing a Nexus file in accordance with a given NXDL."""

import re
import xml.etree.ElementTree as ET

import h5py
import numpy as np

from nexusparser.tools import read_nexus


def convert_data_converter_dict_to_nxdl_path_entry(entry) -> str:
    """
    Helper function to convert data converter style entry to NXDL style entry:
    ENTRY[entry] -> ENTRY
    """
    regex = r'(.*?)(?=\[)'
    results = re.search(regex, entry)
    return entry if results is None else results.group(1)


def convert_data_converter_dict_to_nxdl_path(path) -> str:
    """
    Helper function to convert data converter style path to NXDL style path:
    /ENTRY[entry]/sample -> /ENTRY/sample
    """
    nxdl_path = ''
    for entry in path.split('/')[1:]:
        nxdl_path += '/' + convert_data_converter_dict_to_nxdl_path_entry(entry)
    return nxdl_path


def get_name_from_data_dict_entry(entry) -> str:
    """
    Helper function to get entry name from data converter style entry:
    ENTRY[entry] -> entry
    """
    regex = r'(?<=\[)(.*?)(?=\])'
    results = re.search(regex, entry)
    return entry if results is None else results.group(1)


def convert_data_dict_path_to_hdf5_path(path) -> str:
    """
    Helper function to convert data converter style path to HDF5 style path:
    /ENTRY[entry]/sample -> /entry/sample
    """
    hdf5path = ''
    for entry in path.split('/')[1:]:
        hdf5path += '/' + get_name_from_data_dict_entry(entry)
    return hdf5path


def does_path_exist(path, h5py_obj) -> bool:
    """Returns true if the requested path exists in the given h5py object."""
    try:
        h5py_obj[convert_data_dict_path_to_hdf5_path(path)]  # pylint: disable=W0106
        return True
    except KeyError:
        return False


def is_data_empty(value) -> bool:
    """Returns True if value is an Numpy array or not None."""
    if isinstance(value, np.ndarray) or value is not None:
        return True
    return False


def get_namespace(element) -> str:
    """Extracts the namespace for elements in the NXDL"""
    return element.tag[element.tag.index("{"):element.tag.rindex("}") + 1]


class Writer:
    """
    The writer class for writing a Nexus file in accordance with a given NXDL.

    Attributes
    ----------
    data : dict
        dictionary containing the data to convert
    nxdl_path : str
        path to the nxdl file to use during conversion
    output_path : str
        path to the output Nexus file
    nxdl : dict
        stores xml data from given nxdl file to use during conversion
    """

    def __init__(self, data: dict = None, nxdl_path: str = None, output_path: str = None):
        """Constructs the necessary objects required by the Writer class."""
        self.data = data
        self.nxdl_path = nxdl_path
        self.output_path = output_path
        self.output_nexus = None
        self.data = data
        self.nxdl_name = re.search("NX[a-z]*(?=.nxdl.xml)", self.nxdl_path).group(0)
        self.nxdl_data = ET.parse(self.nxdl_path).getroot()
        self.nxs_namespace = get_namespace(self.nxdl_data)

    def __nxdl_to_attrs(self, path: str = '/') -> dict:
        """
        Return a dictionary of all the attributes at the given path in the NXDL and
        the required attribute values that were requested in the NXDL from the data.
        """
        path_nxdl = convert_data_converter_dict_to_nxdl_path(path)
        elem = self.nxdl_data
        elem = read_nexus.nxdl_to_attr_obj(f"{self.nxdl_name}:{path_nxdl}")

        # Remove the name attribute as we only use it to name the HDF5 entry
        if "name" in elem.attrib.keys():
            del elem.attrib["name"]

        # Fetch values for required attributes requested by the NXDL
        for attr_name in elem.findall(f"{self.nxs_namespace}attribute"):
            elem.attrib[attr_name.get('name')] = self.data[f"{path}/@{attr_name.get('name')}"] or ''

        return elem.attrib

    def ensure_and_get_parent_node(self, path) -> h5py.Group:
        """Returns the parent if it exists for a given path else creates the parent group."""
        parent_path = path[0:path.rindex('/')] or '/'
        parent_path_hdf5 = convert_data_dict_path_to_hdf5_path(parent_path)
        if not does_path_exist(parent_path, self.output_nexus):
            parent = self.ensure_and_get_parent_node(parent_path)
            grp = parent.create_group(parent_path_hdf5)
            attrs = self.__nxdl_to_attrs(parent_path)
            if attrs is not None:
                grp.attrs['NX_CLASS'] = attrs["type"]
            return grp
        return self.output_nexus[parent_path_hdf5]

    def write(self):
        """Writes the Nexus file with data from the reader and appropriate attrs."""
        self.output_nexus = h5py.File(self.output_path, "w")

        for path, value in self.data.items():
            if path[path.rindex('/') + 1:] == 'units':
                continue

            entry_name = get_name_from_data_dict_entry(path[path.rindex('/') + 1:])

            data = value if is_data_empty(value) else ""

            if entry_name[0] != "@":
                grp = self.ensure_and_get_parent_node(path)

                dataset = grp.create_dataset(entry_name, data=data)
                units_key = f"{path}/units"
                if units_key in self.data:
                    if self.data[units_key] is not None:
                        dataset.attrs["units"] = self.data[units_key]
                    else:
                        raise Exception(f"Units should be supplied for: {path}")
            else:
                dataset = self.ensure_and_get_parent_node(path)
                dataset.attrs[entry_name[1:]] = data

        self.output_nexus.close()
