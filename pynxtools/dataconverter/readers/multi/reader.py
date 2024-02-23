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
"""An example reader implementation for the DataConverter."""
import os
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import parse_flatten_json, parse_yml
from pynxtools.dataconverter.template import Template


def fill_wildcard_data_indices(config_file_dict, dims):
    """
    Replaces the wildcard data indices (*) with the respective dimension entries.
    """

    def get_vals_on_same_level(key):
        key = key.rsplit("/", 1)[0]
        for k, v in config_file_dict.items():
            if k.startswith(key):
                yield v

    for key, value in list(config_file_dict.items()):
        for dim in dims:
            new_key = key.replace("*", dim)
            new_val = value.replace("*", dim)

            if (
                new_key not in config_file_dict
                and new_val not in get_vals_on_same_level(new_key)
            ):
                config_file_dict[new_key] = new_val

        config_file_dict.pop(key)


@dataclass
class ParseJsonCallbacks:
    """
    Callbacks for dealing special keys in the json file.

    Args:
        attrs_callback (Callable[[str], Any]):
            The callback to retrieve attributes under the specified key.
        data_callback (Callable[[str], Any]):
            The callback to retrieve the data under the specified key.
        dims (List[str]):
            The dimension labels of the data. Defaults to None.
    """

    special_key_map = {
        "@attrs": lambda _, v: ParseJsonCallbacks.attrs_callback(v),
        "@link": lambda _, v: ParseJsonCallbacks.link_callback(v),
        "@data": lambda _, v: ParseJsonCallbacks.data_callback(v),
    }
    attrs_callback: Callable[[str], Any] = lambda v: v
    data_callback: Callable[[str], Any] = lambda v: v
    link_callback: Callable[[str], Any] = lambda v: {"link": v}
    dims: List[str] = field(default_factory=list)

    def apply_special_key(self, precursor, key, value):
        """
        Apply the special key to the value.
        """
        ParseJsonCallbacks.special_key_map.get(precursor, lambda _, v: v)(key, value)


def parse_json_config(
    file_path: str,
    callbacks: Optional[ParseJsonCallbacks] = None,
) -> dict:
    """
    Parses a json file and returns the data as a dictionary.
    """
    if callbacks is None:
        # Use default callbacks if none are explicitly provided
        callbacks = ParseJsonCallbacks()

    config_file_dict = parse_flatten_json(file_path)
    fill_wildcard_data_indices(config_file_dict, callbacks.dims)

    for key, value in config_file_dict.items():
        if not isinstance(value, str) or ":" not in value:
            continue

        precursor = value.split(":")[0]
        value = value[value.index(":") + 1 :]

        config_file_dict[key] = callbacks.apply_special_key(precursor, key, value)

    return config_file_dict


class MultiFormatReader(BaseReader):
    """
    A reader that takes a mapping json file and a data file/object to return a template.
    """

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls: List[str] = []
    extensions: Dict[str, Callable[[Any], dict]] = {
        ".yaml": parse_yml,
        ".yml": parse_yml,
    }
    kwargs: Optional[Dict[str, Any]] = None

    def __init__(self):
        self.extensions[".json"] = lambda fn: parse_json_config(
            fn,
            ParseJsonCallbacks(
                attrs_callback=self.get_attr,
                data_callback=self.get_data,
                dims=self.get_data_dims,
            ),
        )

    def setup_template(self) -> Dict[str, Any]:
        """
        Setups the initial data in the template.
        This may be used to set fixed information, e.g., about the reader.
        """
        return {}

    # pylint: disable=unused-argument
    def handle_objects(self, objects: Tuple[Any]) -> Dict[str, Any]:
        """
        Handles the objects passed into the reader.
        """
        return {}

    def get_attr(self, path: str) -> Any:
        """
        Returns an attributes from the given path.
        """
        return {}

    def get_data(self, path: str) -> Any:
        """
        Returns data from the given path.
        """
        return {}

    def get_data_dims(self, path: str) -> List[str]:
        """
        Returns the dimensions of the data from the given path.
        """
        return []

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
        **kwargs,
    ) -> dict:
        """
        Reads data from multiple files and passes them to the appropriate functions
        in the extensions dict.
        """
        template = Template()
        self.kwargs = kwargs

        def sort_keys(filename: str) -> str:
            """
            Makes sure to read json and yaml files last
            """
            ending = os.path.splitext(filename)[1]
            return ".zzzzz" if ending in (".json", ".yaml", ".yml") else ending

        sorted_paths = sorted(file_paths, key=sort_keys)
        for file_path in sorted_paths:
            extension = os.path.splitext(file_path)[1].lower()
            if extension not in self.extensions:
                print(
                    f"WARNING: "
                    f"File {file_path} has an unsupported extension, ignoring file."
                )
                continue
            if not os.path.exists(file_path):
                print(f"WARNING: File {file_path} does not exist, ignoring entry.")
                continue

            template.update(self.extensions.get(extension, lambda _: {})(file_path))

        template.update(self.setup_template())
        template.update(self.handle_objects(objects))

        return template


READER = MultiFormatReader
