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

import ast
import logging
import os
import re
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

logger = logging.getLogger("pynxtools")


def fill_wildcard_data_indices(config_file_dict, key, value, dims):
    """
    Replaces the wildcard data indices (*) with the respective dimension entries.
    """

    def get_vals_on_same_level(key):
        key = key.rsplit("/", 1)[0]
        for k, v in config_file_dict.items():
            if k.startswith(key):
                yield v

    dim_dict = {}
    for dim in dims:
        new_key = key.replace("*", dim)
        new_val = value.replace("*", dim)

        if new_key not in config_file_dict and new_val not in get_vals_on_same_level(
            new_key
        ):
            dim_dict[new_key] = new_val

    return dim_dict


class ParseJsonCallbacks:
    """
    Callbacks for dealing with special keys in the json file.

    These callbacks are used to fill the template with (meta)data
    from different sources, defined in the special_key_map:
        "@attrs": instrument metadata from the experiment file
        "@link": used for linking (meta)data
        "@data": measurement data
        "@eln": ELN data not provided within the experiment file

    Args:
        attrs_callback (Callable[[str], Any]):
            The callback to retrieve attributes under the specified key.
        data_callback (Callable[[str], Any]):
            The callback to retrieve the data under the specified key.
        link_callback (Callable[[str], Any]):
            The callback to retrieve links under the specified key.
        eln_callback (Callable[[str], Any]):
            The callback to retrieve eln values under the specified key.
        dims (List[str]):
            The dimension labels of the data. Defaults to None.
        entry_name (str):
            The current entry name to use.
    """

    special_key_map: Dict[str, Callable[[str, str], Any]]
    entry_name: str
    dims: Callable[[str, str], List[str]]

    def __init__(
        self,
        attrs_callback: Optional[Callable[[str, str], Any]] = None,
        data_callback: Optional[Callable[[str, str], Any]] = None,
        link_callback: Optional[Callable[[str, str], Any]] = None,
        eln_callback: Optional[Callable[[str, str], Any]] = None,
        dims: Optional[Callable[[str, str], List[str]]] = None,
        entry_name: str = "entry",
    ):
        self.special_key_map = {
            "@attrs": attrs_callback if attrs_callback is not None else self.identity,
            "@link": link_callback if link_callback is not None else self.link_callback,
            "@data": data_callback if data_callback is not None else self.identity,
            "@eln": eln_callback if eln_callback is not None else self.identity,
        }

        self.dims = dims if dims is not None else lambda *_, **__: []
        self.entry_name = entry_name

    def link_callback(self, key: str, value: str) -> Dict[str, Any]:
        """
        Modify links to dictionaries with the correct entry name.
        """
        return {"link": value.replace("/entry/", f"/{self.entry_name}/")}

    def identity(self, _: str, value: str) -> str:
        """
        Returns the input value unchanged.

        This method serves as an identity function in case no callback is set.
        """
        return value

    def apply_special_key(self, precursor, key, value):
        """
        Apply the special key to the value.
        """
        return self.special_key_map.get(precursor, self.identity)(key, value)


def resolve_special_keys(
    new_entry_dict: Dict[str, Any],
    key: str,
    value: Any,
    optional_groups_to_remove: List[str],
    callbacks: ParseJsonCallbacks,
    suppress_warning: bool = False,
) -> None:
    """
    Resolves the special keys (denoted by "@") through the callbacks.

    Also takes care of the "!" notation, i.e., removes optional groups
    if a required sub-element cannot be filled.
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

    def parse_config_value(value: str) -> Tuple[str, Any]:
        """
        Separates the prefixes (denoted by "@") from the rest
        of the value.

        Parameters
        ----------
        value : str
            Config dict value.

        Returns
        -------
        Tuple[str, Any]
            Tuple like (prefix, path).

        """
        # Regex pattern to match @prefix:some_string
        pattern = r"(@\w+)(?::(.*))?"
        prefixes = re.findall(pattern, value)
        if not prefixes:
            return ("", value)
        return prefixes[0]

    # Handle non-keyword values
    if not isinstance(value, str) or "@" not in str(value):
        new_entry_dict[key] = value
        return

    prefixes: List[Tuple[str, str]] = []

    try:
        # Safely evaluate the string to a list
        list_value = ast.literal_eval(value.lstrip("!"))
        prefixes = [parse_config_value(v) for v in list_value]
    except (SyntaxError, ValueError):
        prefixes = [parse_config_value(value)]

    for prefix, path in prefixes:
        if not prefix.startswith("@"):
            new_entry_dict[key] = try_convert(path)
            break
        new_entry_dict[key] = callbacks.apply_special_key(prefix, key, path)

        # We found a match. Stop resolving other prefixes.
        if new_entry_dict[key] is not None:
            break

    if value.startswith("!") and new_entry_dict[key] is None:
        group_to_delete = key.rsplit("/", 1)[0]
        logger.info(
            f"Main element {key} not provided. "
            f"Removing the parent group {group_to_delete}."
        )
        optional_groups_to_remove.append(group_to_delete)
        return

    if prefixes and new_entry_dict[key] is None:
        del new_entry_dict[key]
        if not suppress_warning:
            logger.info(
                f"Could not find value for key {key} with value {value}.\n"
                f"Tried prefixes: {prefixes}."
            )

    # after filling, resolve links again:
    if isinstance(new_entry_dict.get(key), str) and new_entry_dict[key].startswith(
        "@link:"
    ):
        new_entry_dict[key] = {"link": new_entry_dict[key][6:]}


def fill_from_config(
    config_dict: Dict[str, Any],
    entry_names: List[str],
    callbacks: Optional[ParseJsonCallbacks] = None,
    suppress_warning: bool = False,
) -> dict:
    """
    Parses a config dictionary and returns the data as a dictionary.
    """

    def has_missing_main(key: str) -> bool:
        """
        Checks if a key starts with a name of a group that has
        to be removed because a required child is missing.
        """
        for optional_group in optional_groups_to_remove:
            if key.startswith(optional_group):
                return True
        return False

    def dict_sort_key(keyval: Tuple[str, Any]) -> bool:
        """
        The function to sort the dict by.
        This just sets False for keys starting with "!" to put them at the beginning.
        Besides, pythons sorted is stable, so this will keep the order of the keys
        which have the same sort key.
        """
        if isinstance(keyval[1], str):
            return not keyval[1].startswith("!")
        return True

    if callbacks is None:
        # Use default callbacks if none are explicitly provided
        callbacks = ParseJsonCallbacks()

    optional_groups_to_remove: List[str] = []
    new_entry_dict = {}
    for entry_name in entry_names:
        callbacks.entry_name = entry_name

        # Process '!...' keys first
        sorted_keys = dict(sorted(config_dict.items(), key=dict_sort_key))
        for key in sorted_keys:
            value = config_dict[key]
            key = key.replace("/ENTRY/", f"/ENTRY[{entry_name}]/")

            if has_missing_main(key):
                continue

            if "*" in key:
                dims = callbacks.dims(key, value)
                dim_data = fill_wildcard_data_indices(config_dict, key, value, dims)
                for k, v in dim_data.items():
                    resolve_special_keys(
                        dim_data,
                        k,
                        v,
                        optional_groups_to_remove,
                        callbacks,
                        suppress_warning,
                    )
                new_entry_dict.update(dim_data)
                continue

            resolve_special_keys(
                new_entry_dict,
                key,
                value,
                optional_groups_to_remove,
                callbacks,
                suppress_warning,
            )

    return new_entry_dict


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
    config_file: Optional[str] = None
    config_dict: Dict[str, Any]

    def __init__(self, config_file: Optional[str] = None):
        self.callbacks = ParseJsonCallbacks(
            attrs_callback=self.get_attr,
            data_callback=self.get_data,
            eln_callback=self.get_eln_data,
            dims=self.get_data_dims,
        )
        self.config_file = config_file
        self.config_dict = {}

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

    def get_attr(self, key: str, path: str) -> Any:
        """
        Returns an attributes from the given path.
        Should return None if the path does not exist.
        """
        return None

    def get_data(self, key: str, path: str) -> Any:
        """
        Returns data from the given path.
        Should return None if the path does not exist.
        """
        return None

    def get_eln_data(self, key: str, path: str) -> Any:
        """
        Returns data from the given eln path.
        Should return None if the path does not exist.
        """
        return {}

    def get_data_dims(self, key: str, path: str) -> List[str]:
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

    def post_process(self) -> None:
        """
        Do postprocessing after all files and config file are read.
        """

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Optional[Tuple[Any]] = None,
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
        if objects is not None:
            template.update(self.handle_objects(objects))

        if self.config_file is not None:
            self.config_dict = parse_flatten_json(
                self.config_file, create_link_dict=False
            )

        self.post_process()

        if self.config_dict:
            suppress_warning = kwargs.pop("suppress_warning", False)
            template.update(
                fill_from_config(
                    self.config_dict,
                    self.get_entry_names(),
                    self.callbacks,
                    suppress_warning=suppress_warning,
                )
            )

        return template


READER = MultiFormatReader
