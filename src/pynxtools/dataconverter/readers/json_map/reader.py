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
"""JSON mapping reader built on MultiFormatReader.

.. deprecated::
    The ``.mapping.json`` file format is deprecated.  Use a config file
    passed via the ``-c`` flag instead.  See the pynxtools documentation for
    the config file format used by all MultiFormatReader plugins.

The reader accepts a config file (``-c``) whose values use ``@data:`` tokens:

* ``"@data:a_level/field"`` — resolve path in the data dict
* ``"@attrs:my_attr"``      — resolve via ``get_attr()``
* ``"@eln:eln_path"``       — resolve from ELN data
* a literal value (string, number, bool): ``"NXoptical_spectroscopy"``
* a link/virtual-dataset dict: ``{"link": "...", "shape": "0:2"}``

For backward compatibility, ``.mapping.json`` files are still accepted but
will emit a ``DeprecationWarning`` and will be removed in a future release.
"""

import json
import logging
import pickle
import warnings
from typing import Any

import numpy as np
import xarray
import yaml
from mergedeep import merge

from pynxtools.dataconverter import hdfdict
from pynxtools.dataconverter.readers.multi.reader import (
    MultiFormatReader,
    fill_from_config,
)
from pynxtools.dataconverter.template import Template

logger = logging.getLogger("pynxtools")


def parse_slice(slice_string):
    """Converts slice strings to actual tuple sets of slices for index syntax."""
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


def convert_shapes_to_slice_objects(mapping):
    """Converts shape slice strings to slice objects for indexing."""
    for key in mapping:
        if isinstance(mapping[key], dict):
            if "shape" in mapping[key]:
                mapping[key]["shape"] = parse_slice(mapping[key]["shape"])


def get_map_from_partials(partials, template, data):
    """Takes a list of partials and returns a mapping dictionary."""
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
                )
                template_path = template_path + "/" + nx_name
        mapping[template_path] = path

    return mapping


def mapping_to_config(mapping: dict) -> dict:
    """Convert a json_map mapping dict to ``fill_from_config`` format.

    Values that are data paths (start with ``/``) are converted to
    ``@data:<path>`` tokens.  Literal values and link/shape dicts pass
    through unchanged.

    This makes ``.mapping.json`` files work with the ``fill_from_config``
    pipeline used by all MultiFormatReader plugins.
    """
    result = {}
    for k, v in mapping.items():
        if isinstance(v, str) and v.startswith("/"):
            result[k] = f"@data:{v[1:]}"
        else:
            result[k] = v
    return result


class JsonMapReader(MultiFormatReader):
    """A reader that takes a mapping json file and a data file/object to return a template."""

    supported_nxdls = ["NXtest", "*"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: dict = {}
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
        """Dispatch files via super(), then apply mapping or partials."""
        if objects:
            self.data = objects[0]
        result = super().read(
            template=template, file_paths=file_paths, objects=None, **kwargs
        )
        if self.partials and not self.config_dict:
            # Partials require the NXDL template for path resolution.
            mapping = get_map_from_partials(self.partials, template, self.data)
            convert_shapes_to_slice_objects(mapping)
            config = mapping_to_config(mapping)
            result.update(
                fill_from_config(config, self.get_entry_names(), self.callbacks)
            )
        elif not self.config_dict and not self.partials:
            hint = Template(
                {x: "/hierarchical/path/in/your/datafile" for x in (template or {})}
            )
            raise OSError(
                "Please supply a JSON mapping file: "
                " my_nxdl_map.mapping.json\n\n You can use this "
                "template for the required fields: \n" + str(hint)
            )
        return result

    def get_data(self, key: str, path: str) -> Any:
        """Resolve ``@data:path`` tokens by traversal into ``self.data``."""
        try:
            return get_val_nested_keystring_from_dict(path, self.data)
        except (KeyError, TypeError):
            return None

    def _handle_json_file(self, file_path: str) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            content = json.loads(f.read())
        if ".mapping" in file_path:
            msg = (
                "The .mapping.json format is deprecated and will be removed in a "
                "future release. Please use a config file via the -c flag instead. "
                "See the pynxtools documentation for the config file format."
            )
            logger.warning(msg)
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            # Convert shape strings to slice objects, then convert to
            # fill_from_config format. Pipeline step 6 resolves via get_data().
            convert_shapes_to_slice_objects(content)
            self.config_dict = mapping_to_config(content)
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


# This has to be set to allow the convert script to use this reader.
READER = JsonMapReader
