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
"""MultiFormatReader: base class for file-format-dispatching NeXus readers."""

import ast
import logging
import os
import re
from collections.abc import Callable
from typing import Any, Union

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import (
    is_boolean,
    is_integer,
    is_number,
    parse_flatten_json,
    parse_yml,
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
        if isinstance(value, str):
            new_val = value.replace("*", dim)
        elif isinstance(value, list):
            new_val = [val.replace("*", dim) for val in value]
        else:
            new_val = value

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
        dims (list[str]):
            The dimension labels of the data. Defaults to None.
        entry_name (str):
            The current entry name to use.
    """

    special_key_map: dict[str, Callable[[str, str], Any]]
    entry_name: str
    dims: Callable[[str, str], list[str]]

    def __init__(
        self,
        attrs_callback: Callable[[str, str], Any] | None = None,
        data_callback: Callable[[str, str], Any] | None = None,
        link_callback: Callable[[str, str], Any] | None = None,
        eln_callback: Callable[[str, str], Any] | None = None,
        dims: Callable[[str, str], list[str]] | None = None,
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

    def link_callback(self, key: str, value: str) -> dict[str, Any]:
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
    new_entry_dict: dict[str, Any],
    key: str,
    value: Any,
    optional_groups_to_remove: list[str],
    callbacks: ParseJsonCallbacks,
    suppress_warning: bool = False,
) -> None:
    """
    Resolves the special keys (denoted by "@") through the callbacks.

    Also takes care of the "!" notation, i.e., removes optional groups
    if a required sub-element cannot be filled.
    """

    def try_convert(value: str) -> str | float | int | bool:
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

    def parse_config_value(value: str) -> tuple[str, Any]:
        """
        Separates the prefixes (denoted by "@") from the rest
        of the value.

        Parameters
        ----------
        value : str
            Config dict value.

        Returns
        -------
        tuple[str, Any]
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

    prefixes: list[tuple[str, str]] = []

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
    config_dict: dict[str, Any],
    entry_names: list[str],
    callbacks: ParseJsonCallbacks | None = None,
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

    def dict_sort_key(keyval: tuple[str, Any]) -> bool:
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

    optional_groups_to_remove: list[str] = []
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

                for k, v in dim_data.copy().items():
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
    Base class for readers that dispatch input files by extension and populate
    a NeXus template from the read data, optionally guided by a JSON config file.

    Pipeline executed by ``read()`` in order:

    1. **objects** — ``handle_objects(objects)`` is called first so in-memory
       data is available to all subsequent steps.
    2. **files** — each input file is dispatched to the matching handler in
       ``self.extensions`` (sorted by ``processing_order`` if set).
    3. **static data** — ``setup_template()`` returns a dict/Template of entries
       that do not originate from input files (reader metadata, hard-coded values).
    4. **config file** — if ``self.config_file`` is set, it is parsed into
       ``self.config_dict``.
    5. **post-processing** — ``post_process()`` may modify ``self.config_dict``
       or other instance attributes (like ``self.eln_data`` or ``self.data``) or
       may returns a dict/Template of entries to update the template.
    6. **config fill** — ``fill_from_config()`` resolves ``@attrs``/``@data``/
       ``@eln``/``@link`` tokens in ``self.config_dict`` via callbacks and
       updates the template.

    Subclasses must set ``supported_nxdls`` and define ``self.extensions`` in
    ``__init__``.  All other hook methods are optional.

    Built-in handlers (register in ``self.extensions`` to activate):

    * ``handle_eln_file`` — parses YAML/JSON ELN files via ``parse_yml``;
      respects ``CONVERT_DICT`` and ``REPLACE_NESTED`` class attributes.
    * ``set_config_file`` — stores the path of a JSON config file.

    Built-in callbacks (override to customize):

    * ``get_attr(key, path)`` — retrieve instrument metadata.
    * ``get_data(key, path)`` — retrieve measurement data.
    * ``get_eln_data(key, path)`` — reads from ``self.eln_data`` populated by
      ``handle_eln_file``; override if a different ELN source is needed.
    * ``get_data_dims(key, path)`` — return axis names for wildcard expansion.
    """

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls: list[str] = []
    # Type annotation only — each instance gets its own dict in __init__.
    extensions: dict[str, Callable[[Any], dict]]
    kwargs: dict[str, Any] | None = None
    overwrite_keys: bool = True
    config_file: str | None = None

    # Override in subclasses to control how handle_eln_file maps keys.
    CONVERT_DICT: dict[str, str] = {}
    REPLACE_NESTED: dict[str, str] = {}

    def __init__(self, config_file: str | None = None):
        self.callbacks = ParseJsonCallbacks(
            attrs_callback=self.get_attr,
            data_callback=self.get_data,
            eln_callback=self.get_eln_data,
            dims=self.get_data_dims,
        )
        self.config_file = config_file
        self.config_dict: dict[str, Any] = {}
        self.eln_data: dict[str, Any] = {}
        # Instance-level dict — avoids shared mutable class attribute.
        # Subclasses override this in their own __init__.
        self.extensions: dict[str, Callable[[Any], dict]] = {}
        self.processing_order: list[str] | None = None

    # ------------------------------------------------------------------
    # Built-in file handlers — register in self.extensions to activate.
    # ------------------------------------------------------------------

    def handle_eln_file(self, file_path: str) -> dict[str, Any]:
        """
        Parse a YAML/JSON ELN file into ``self.eln_data``.

        Uses ``parse_yml`` with the class-level ``CONVERT_DICT`` and
        ``REPLACE_NESTED`` mappings.  The result is available to ``get_eln_data``
        automatically.  Subclasses may override this method or simply set
        ``CONVERT_DICT`` / ``REPLACE_NESTED`` at class level.
        """
        entry_name = self.get_entry_names()[0]
        self.eln_data = parse_yml(
            file_path,
            convert_dict=dict(self.CONVERT_DICT),
            replace_nested=dict(self.REPLACE_NESTED),
            parent_key=f"/ENTRY[{entry_name}]",
        )
        return {}

    def set_config_file(self, file_path: str) -> dict[str, Any]:
        """
        Register a JSON config file to drive ``@attrs``/``@data``/``@eln`` mapping.

        If a config file was already set, a warning is logged and the new path
        replaces the old one.
        """
        if self.config_file is not None:
            logger.warning(f"Config file already set. Replaced by {file_path}.")
        self.config_file = file_path
        return {}

    # ------------------------------------------------------------------
    # Hook methods — override in subclasses as needed.
    # ------------------------------------------------------------------

    def setup_template(self) -> dict[str, Any]:
        """
        Return static, hard-coded entries to add to the template.

        Called after all input files have been dispatched but before any
        config-file processing.  Use this for entries whose values are
        known at class-definition time — reader metadata, fixed units,
        constant calibration values, etc.

        **Contract**: this method must NOT access the NXDL template structure
        (there is no reference to it) and must NOT access data read from input
        files (``self.data`` or equivalent).  Any logic that depends on either
        belongs in ``read()`` or ``post_process()``.
        """
        return {}

    def handle_objects(self, objects: tuple[Any]) -> dict[str, Any]:  # pylint: disable=unused-argument
        """
        Handle in-memory Python objects passed alongside input files.

        Called *before* file dispatch so that object data is available to
        extension handlers.  Return a dict to add entries to the template,
        or an empty dict if data is stored on ``self`` for later use.
        """
        return {}

    def get_attr(self, key: str, path: str) -> Any:
        """
        Return instrument metadata from ``path`` for the ``@attrs`` config token.

        ``key`` is the resolved NeXus template path; ``path`` is the part after
        ``@attrs:``.  Return ``None`` if the path does not exist.
        """
        return None

    def get_data(self, key: str, path: str) -> Any:
        """
        Return measurement data from ``path`` for the ``@data`` config token.

        ``key`` is the resolved NeXus template path; ``path`` is the part after
        ``@data:``.  Return ``None`` if the path does not exist.
        """
        return None

    def get_eln_data(self, key: str, path: str) -> Any:
        """
        Return ELN metadata for the ``@eln`` config token.

        By default reads from ``self.eln_data`` populated by ``handle_eln_file``.
        Uses ``path`` when provided (i.e. ``@eln:some/path``), otherwise falls
        back to ``key`` (i.e. bare ``@eln``).  Return ``None`` if not found.
        """
        if not self.eln_data:
            return None
        return self.eln_data.get(path or key)

    def get_data_dims(self, key: str, path: str) -> list[str]:
        """
        Return axis names for wildcard (``*``) expansion in the config file.

        Override when the config uses ``AXISNAME[*]`` / ``@data:*.data``
        notation to expand multiple axes automatically.
        """
        return []

    def get_entry_names(self) -> list[str]:
        """
        Return the list of NeXus entry names to write.

        Each name causes ``/ENTRY/`` in the config file to be replaced by
        ``/ENTRY[<name>]/``.  Override for multi-entry datasets.
        """
        return ["entry"]

    def post_process(self) -> dict[str, Any] | None:
        """
        Post-process after files are read and the config file is parsed.

        May modify ``self.config_dict`` (or other instance attributes like
        ``self.eln_data`` or ``self.data``) in-place (e.g. to add dynamic entries
        for multi-detector setups) and/or return a dict of template entries to
        add before ``fill_from_config`` runs.  Return ``None`` or ``{}`` if
        no additional entries are needed.
        """
        return None

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] | None = None,
        **kwargs,
    ) -> dict:
        """
        Execute the MultiFormatReader pipeline and return a filled Template.

        See the class docstring for the full pipeline description.
        """
        self.kwargs = kwargs
        self.config_file = self.kwargs.get("config_file", self.config_file)
        self.overwrite_keys = self.kwargs.get("overwrite_keys", self.overwrite_keys)

        template = Template(template=template, overwrite_keys=self.overwrite_keys)

        # 1. Objects — before file dispatch so handlers can build on them.
        if objects is not None:
            template.update(self.handle_objects(objects))

        # 2. Files — dispatch each input file to its registered handler.
        def get_processing_order(path: str) -> tuple[int, str | int]:
            ext = os.path.splitext(path)[1]
            if self.processing_order is None or ext not in self.processing_order:
                return (1, ext)
            return (0, self.processing_order.index(ext))

        for file_path in sorted(file_paths or [], key=get_processing_order):
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

        # 3. Static data not derived from input files.
        template.update(self.setup_template())

        # 4. Config file.
        if self.config_file is not None:
            self.config_dict = parse_flatten_json(
                self.config_file, create_link_dict=False
            )

        # 5. Post-processing.
        post_result = self.post_process()
        if post_result:
            template.update(post_result)

        # 6. Fill template from config dict via @-token callbacks.
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
