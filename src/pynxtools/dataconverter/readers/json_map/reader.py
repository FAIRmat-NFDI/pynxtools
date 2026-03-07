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
"""JSON mapping reader built on MultiFormatReader."""

import json
import pickle
from typing import Any

import numpy as np
import xarray
import yaml
from mergedeep import merge

from pynxtools.dataconverter import hdfdict
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.template import Template


def parse_slice(slice_string):
    """Converts slice strings to actual tuple sets of slices for index syntax"""
    slices = slice_string.split(",")
    for index, item in enumerate(slices):
        values = item.split(":")
        slices[index] = slice(*[None if x == "" else int(x) for x in values])
    return np.index_exp[tuple(slices)]


def get_val_nested_keystring_from_dict(keystring, data):
    """
    Fetches data from the actual data dict using path strings without a leading '/':
        'path/to/data/in/dict'
    """
    if isinstance(keystring, list | dict):
        return keystring

    current_key = keystring.split("/")[0]
    if isinstance(data[current_key], dict | hdfdict.LazyHdfDict):
        return get_val_nested_keystring_from_dict(
            keystring[keystring.find("/") + 1 :], data[current_key]
        )
    if isinstance(data[current_key], xarray.DataArray):
        return data[current_key].values
    if isinstance(data[current_key], xarray.core.dataset.Dataset):
        raise NotImplementedError(
            "Xarray datasets are not supported. You can only use xarray dataarrays."
        )

    return data[current_key]


def get_attrib_nested_keystring_from_dict(keystring, data):
    """
    Fetches all attributes from the data dict using path strings without a leading '/':
        'path/to/data/in/dict'
    """
    if isinstance(keystring, list | dict):
        return keystring

    key_splits = keystring.split("/")
    parents = key_splits[:-1]
    target = key_splits[-1]
    for key in parents:
        data = data[key]

    return data[target + "@"] if target + "@" in data.keys() else None


def is_path(keystring):
    """Checks whether a given value in the mapping is a mapping path or just data"""
    return isinstance(keystring, str) and len(keystring) > 0 and keystring[0] == "/"


def fill_undocumented(mapping, template, data):
    """Fill the extra paths provided in the map file that are not in the NXDL"""
    for path, value in mapping.items():
        if is_path(value):
            template["undocumented"][path] = get_val_nested_keystring_from_dict(
                value[1:], data
            )
            fill_attributes(path, value[1:], data, template)
        else:
            template["undocumented"][path] = value


def fill_documented(template, mapping, template_provided, data):
    """Fill the needed paths that are explicitly mentioned in the NXDL"""
    for req in ("required", "optional", "recommended"):
        for path in template_provided[req]:
            try:
                map_str = mapping[path]
                if is_path(map_str):
                    template[path] = get_val_nested_keystring_from_dict(
                        map_str[1:], data
                    )
                    fill_attributes(path, map_str[1:], data, template)
                else:
                    template[path] = map_str

                del mapping[path]
            except KeyError:
                pass


def fill_attributes(path, map_str, data, template):
    """Fills in the template all attributes found in the data object"""
    attribs = get_attrib_nested_keystring_from_dict(map_str, data)
    if attribs:
        for key, value in attribs.items():
            template[path + "/@" + key] = value


def convert_shapes_to_slice_objects(mapping):
    """Converts shape slice strings to slice objects for indexing"""
    for key in mapping:
        if isinstance(mapping[key], dict):
            if "shape" in mapping[key]:
                mapping[key]["shape"] = parse_slice(mapping[key]["shape"])


def get_map_from_partials(partials, template, data):
    """Takes a list of partials and returns a mapping dictionary to fill partials in our template"""
    mapping: dict = {}
    for partial in partials:
        path = ""
        template_path = ""
        for part in partial.split("/")[1:]:
            path = path + "/" + part
            attribs = get_attrib_nested_keystring_from_dict(path[1:], data)
            if template_path + "/" + part in template.keys():
                template_path = template_path + "/" + part
            else:
                nx_name = (
                    f"{attribs['NX_class'][2:].upper()}[{part}]"
                    if attribs and "NX_class" in attribs
                    else part
                )  # pylint: disable=line-too-long
                template_path = template_path + "/" + nx_name
        mapping[template_path] = path

    return mapping


class JsonMapReader(MultiFormatReader):
    """A reader that takes a mapping json file and a data file/object to return a template."""

    supported_nxdls = ["NXtest", "*"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: dict = {}
        self.mapping: dict | None = None
        self.partials: list = []
        self.extensions = {
            ".json": self._handle_json_file,
            ".pickle": self._handle_pickle_file,
            ".yaml": self._handle_yaml_file,
            ".hdf5": self._handle_hdf5_file,
            ".h5": self._handle_hdf5_file,
            ".nxs": self._handle_hdf5_file,
        }

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] | None = None,
        **kwargs,
    ) -> dict:
        """Sets up data from objects before delegating to MultiFormatReader."""
        if objects:
            self.data = objects[0]
        # Pass objects=None so MultiFormatReader does not re-call handle_objects
        return super().read(
            template=template, file_paths=file_paths, objects=None, **kwargs
        )

    def _handle_json_file(self, file_path: str) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            content = json.loads(f.read())
        if ".mapping" in file_path:
            self.mapping = content
        else:
            self.data = content
        return {}

    def _handle_pickle_file(self, file_path: str) -> dict[str, Any]:
        with open(file_path, "rb") as f:  # type: ignore[assignment]
            self.data = pickle.load(f)  # type: ignore[arg-type]
        return {}

    def _handle_yaml_file(self, file_path: str) -> dict[str, Any]:
        with open(file_path) as f:
            merge(self.data, yaml.safe_load(f))
        return {}

    def _handle_hdf5_file(self, file_path: str) -> dict[str, Any]:
        hdf = hdfdict.load(file_path)
        hdf.unlazy()
        merge(self.data, dict(hdf))
        if "entry@" in self.data and "partial" in self.data["entry@"]:
            self.partials.extend(self.data["entry@"]["partial"])
        return {}

    def setup_template(self) -> dict[str, Any]:
        """Builds the output template using the mapping and the NXDL template."""
        mapping = self.mapping
        if mapping is None:
            if self.partials:
                mapping = get_map_from_partials(
                    self.partials, self.nxdl_template, self.data
                )
            else:
                hint = Template(
                    {x: "/hierarchical/path/in/your/datafile" for x in self.nxdl_template}
                )
                raise OSError(
                    "Please supply a JSON mapping file: "
                    " my_nxdl_map.mapping.json\n\n You can use this "
                    "template for the required fields: \n" + str(hint)
                )

        # Build a result Template pre-populated with the NXDL structure so that
        # fill_documented routes each path to the correct optionality sub-dict.
        result = Template(self.nxdl_template)
        convert_shapes_to_slice_objects(mapping)
        fill_documented(result, mapping, self.nxdl_template, self.data)
        fill_undocumented(mapping, result, self.data)
        return result


# This has to be set to allow the convert script to use this reader.
READER = JsonMapReader
