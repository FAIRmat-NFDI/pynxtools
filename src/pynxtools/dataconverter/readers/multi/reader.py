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

import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import (
    is_boolean,
    is_integer,
    is_number,
    parse_flatten_json,
    to_bool,
)
from pynxtools.dataconverter.template import Template

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


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

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
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
        "@eln": lambda _, v: ParseJsonCallbacks.eln_callback(v),
    }
    attrs_callback: Callable[[str], Any] = lambda v: v
    data_callback: Callable[[str], Any] = lambda v: v
    link_callback: Callable[[str], Any] = lambda v: {"link": v}
    eln_callback: Callable[[str], Any] = lambda v: v
    dims: Callable[[str], List[str]] = lambda _: []
    entry_name: str = "entry"

    def __post_init__(self):
        self.link_callback = lambda v: {
            "link": v.replace("/entry/", f"/{self.entry_name}/")
        }

    def apply_special_key(self, precursor, key, value):
        """
        Apply the special key to the value.
        """
        ParseJsonCallbacks.special_key_map.get(precursor, lambda _, v: v)(key, value)


def parse_json_config(
    file_path: str,
    entry_names: List[str],
    callbacks: Optional[ParseJsonCallbacks] = None,
) -> dict:
    """
    Parses a json file and returns the data as a dictionary.
    """

    def try_convert(value: str) -> Union[str, float, int, bool]:
        """
        Try to convert the value to float, int or bool.
        If not convertible returns the str itself.
        """

        if is_integer(value):
            return int(value)
        if is_number(value):
            return float(value)
        if is_boolean(value):
            return to_bool(value)

        return value

    if callbacks is None:
        # Use default callbacks if none are explicitly provided
        callbacks = ParseJsonCallbacks()

    config_file_dict = parse_flatten_json(file_path)
    fill_wildcard_data_indices(config_file_dict, callbacks.dims)

    optional_groups_to_remove: List[str] = []
    for entry_name in entry_names:
        callbacks.entry_name = entry_name
        for key, value in config_file_dict.items():
            key = key.replace("/ENTRY[entry]/", f"/ENTRY[{entry_name}]/")
            if not isinstance(value, str) or ":" not in value:
                continue

            prefix_part, value = value.split(":", 1)
            prefixes = re.findall(r"@(\w+)", prefix_part)

            if prefix_part.startswith("!"):
                optional_groups_to_remove.append(key)
                prefix_part = prefix_part[1:]

            for prefix in prefixes:
                config_file_dict[key] = callbacks.apply_special_key(prefix, key, value)

                # We found a match. Stop resolving other prefixes.
                if config_file_dict[key] is not None:
                    break

            last_value = prefix_part.rsplit(",", 1)[-1]
            if config_file_dict[key] is None and last_value[0] not in ("@", "?"):
                config_file_dict[key] = try_convert(last_value)

            if prefixes and config_file_dict[key] is None:
                del config_file_dict[key]
                logger.warning(
                    f"Could not find value for key {key} with value {value}.\n"
                    f"Tried prefixes: {prefixes}."
                )

    # remove groups that have main keys missing
    for main_key in optional_groups_to_remove:
        if config_file_dict.get(main_key) is None:
            group_to_delete = key.rsplit("/", 1)[0]
            logger.info(
                f"Main element {key} not provided. "
                f"Removing the parent group {group_to_delete}."
            )
            if key in config_file_dict.keys():
                if key.startswith(group_to_delete):
                    del config_file_dict[key]

    return config_file_dict


class MultiFormatReader(BaseReader):
    """
    A reader that takes a mapping json file and a data file/object to return a template.
    """

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls: List[str] = []
    extensions: Dict[str, Callable[[Any], dict]] = {}
    kwargs: Optional[Dict[str, Any]] = None
    overwrite_keys: bool = True
    processing_order: Optional[List[str]] = None

    def __init__(self, config_file: Optional[str] = None):
        self.callbacks = ParseJsonCallbacks(
            attrs_callback=self.get_attr,
            data_callback=self.get_data,
            eln_callback=self.get_eln_data,
            dims=self.get_data_dims,
        )
        self.config_file = config_file

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
        Should return None if the path does not exist.
        """
        return None

    def get_data(self, path: str) -> Any:
        """
        Returns data from the given path.
        Should return None if the path does not exist.
        """
        return None

    def get_eln_data(self, path: str) -> Any:
        """
        Returns data from the given eln path.
        Should return None if the path does not exist.
        """
        return {}

    def get_data_dims(self, path: str) -> List[str]:
        """
        Returns the dimensions of the data from the given path.
        """
        return []

    def get_entry_names(self) -> List[str]:
        """
        Returns a list of entry names which should be constructed from the data.
        Defaults to creating a single entry named "entry".
        """
        return ["entry"]

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
        self.kwargs = kwargs
        self.config_file = self.kwargs.get("config_file", self.config_file)
        self.overwrite_keys = self.kwargs.get("overwrite_keys", self.overwrite_keys)

        template = Template(overwrite_keys=self.overwrite_keys)

        def get_processing_order(path: str) -> Tuple[int, Union[str, int]]:
            """
            Returns the processing order of the file.
            """
            ext = os.path.splitext(path)[1]
            if self.processing_order is None or ext not in self.processing_order:
                return (1, ext)
            return (0, self.processing_order.index(ext))

        sorted_paths = sorted(file_paths, key=get_processing_order)
        for file_path in sorted_paths:
            extension = os.path.splitext(file_path)[1].lower()
            if extension not in self.extensions:
                logger.warning(
                    f"File {file_path} has an unsupported extension, ignoring file."
                )
                continue
            if not os.path.exists(file_path):
                logger.warning(f"File {file_path} does not exist, ignoring entry.")
                continue

            template.update(self.extensions.get(extension, lambda _: {})(file_path))

        template.update(self.setup_template())
        template.update(self.handle_objects(objects))
        if self.config_file is not None:
            template.update(
                parse_json_config(
                    self.config_file, self.get_entry_names(), self.callbacks
                )
            )

        return template


READER = MultiFormatReader
