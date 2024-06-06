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
"""A Template object to control and separate template paths according to optionality"""

import copy
import json
import re
from typing import Set

from pynxtools.dataconverter import helpers


class Template(dict):
    """A Template object to control and separate template paths according to optionality"""

    def __init__(self, template=None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(template, Template):
            self.optional: dict = copy.deepcopy(template["optional"])
            self.recommended: dict = copy.deepcopy(template["recommended"])
            self.required: dict = copy.deepcopy(template["required"])
            self.undocumented: dict = copy.deepcopy(template["undocumented"])
            self.optional_parents: list = copy.deepcopy(template["optional_parents"])
            self.lone_groups: dict = copy.deepcopy(template["lone_groups"])
        else:
            self.optional: dict = {}
            self.recommended: dict = {}
            self.required: dict = {}
            self.undocumented: dict = {}
            self.optional_parents: list = []
            self.lone_groups: list = []
            if isinstance(template, dict):
                self.undocumented: dict = copy.deepcopy(template)

    def get_accumulated_dict(self):
        """Returns a dictionary of all the optionalities merged into one."""
        return {
            **self.optional,
            **self.recommended,
            **self.required,
            **self.undocumented,
        }

    def __repr__(self):
        """Returns a unique string representation for the Template object."""
        return self.get_accumulated_dict().__repr__()

    def __str__(self):
        """Returns a readable string representation for the Template object."""
        accumulated_dict = self.get_accumulated_dict()
        for key, data in accumulated_dict.items():
            if data is None:
                accumulated_dict[key] = "None"
            else:
                accumulated_dict[key] = data.__str__()
        return json.dumps(accumulated_dict, indent=4, sort_keys=True)

    def __setitem__(self, k, v):
        """Handles how values are set within the Template object."""
        if k.startswith("/"):
            if v is None:
                return

            if k in self.recommended:
                self.recommended[k] = v
            elif k in self.required:
                self.required[k] = v
            elif k in self.optional:
                self.optional[k] = v
            else:
                self.undocumented[k] = v
        elif k == "lone_groups":
            self.lone_groups.append(v)
        else:
            raise KeyError(
                "You cannot add non paths to the root template object. "
                'Place them appropriately e.g. template["optional"]'
                '["/ENTRY[entry]/data/path"]'
            )

    def keys(self):
        """Returns the list of keys stored in the Template object."""
        return (
            list(self.optional.keys())
            + list(self.recommended.keys())
            + list(self.required.keys())
            + list(self.undocumented.keys())
        )

    def items(self):
        """Returns a list of tuples of key, value stored in the Template object."""
        return sorted(self.get_accumulated_dict().items())

    def __iter__(self):
        return dict.__iter__(self.get_accumulated_dict())

    def get_optionality(self, optionality):
        """Returns the dictionary for given optionality"""
        if optionality == "optional":
            return self.optional
        if optionality == "recommended":
            return self.recommended
        if optionality == "required":
            return self.required
        if optionality == "undocumented":
            return self.undocumented
        return self.required

    def get_documented(self):
        """Returns a dictionary of all the optionalities merged into one."""
        return {**self.optional, **self.recommended, **self.required}

    def __contains__(self, k):
        """
        Supports in operator for the nested Template keys
        """
        return any(
            [
                k in self.optional,
                k in self.recommended,
                k in self.undocumented,
                k in self.required,
            ]
        )

    def get(self, key: str, default=None):
        """Proxies the get function to our internal __getitem__"""
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, k):
        """Handles how values are accessed from the Template object."""
        # Try setting item in all else throw error. Does not append to default.
        if k in ("optional_parents", "lone_groups"):
            return getattr(self, k)
        if k.startswith("/"):
            if k in self.optional:
                return self.optional[k]
            if k in self.recommended:
                return self.recommended[k]
            if k in self.required:
                return self.required[k]
            return self.undocumented.get(k)
        if k in ("required", "optional", "recommended", "undocumented"):
            return self.get_optionality(k)
        raise KeyError(
            "Only paths starting with '/' or one of [optional_parents, "
            "lone_groups, required, optional, recommended, undocumented] can be used."
        )

    def clear(self):
        """Clears all data stored in the Template object."""
        for del_dict in (
            self.optional,
            self.recommended,
            self.required,
            self.undocumented,
        ):
            del_dict.clear()

    def rename_entry(self, old_name: str, new_name: str, deepcopy=True):
        """Rename all entries under old name to new name."""
        for internal_dict in (
            self.optional,
            self.recommended,
            self.required,
            self.undocumented,
        ):
            keys = list(internal_dict.keys())
            for key in keys:
                entry_name = helpers.get_name_from_data_dict_entry(key.split("/")[1])

                entry_search_term = f"{entry_name}]"
                rest_of_path = key[
                    key.index(entry_search_term) + len(entry_search_term) :
                ]
                if entry_name == old_name:
                    value = internal_dict[key] if deepcopy else None
                    internal_dict[f"/ENTRY[{new_name}]{rest_of_path}"] = value
                    del internal_dict[key]

    def get_all_entry_names(self) -> Set[str]:
        """
        Get all entry names in the template.

        Returns:
            Set[str]: A set of entry names.
        """
        entry_names = set()
        for key in self:
            entry_name_match = re.search(r"\/ENTRY\[([a-zA-Z0-9_\.]+)\]", key)
            if entry_name_match is not None:
                entry_names.add(entry_name_match.group(1))
        return entry_names

    def update(self, template):
        """Merges second template to original
        or updates values from a dictionary if the type of :code:`template` is dict"""
        if isinstance(template, Template):
            for optionality in ("optional", "recommended", "required", "undocumented"):
                self.get_optionality(optionality).update(
                    template.get_optionality(optionality)
                )
        else:
            for key, value in template.items():
                self[key] = value

    def add_entry(self, entry_name):
        """Add the whole NXDL again with a new HDF5 name for the template."""
        template = Template(self)
        template.rename_entry("entry", entry_name, False)
        self.update(template)

    def __delitem__(self, key):
        """Delete a dictionary key or template key"""
        if key in self.optional.keys():
            del self.optional[key]

        elif key in self.required.keys():
            del self.required[key]

        elif key in self.recommended.keys():
            del self.recommended[key]
        elif key in self.undocumented.keys():
            del self.undocumented[key]
        else:
            raise KeyError(f"{key} does not exist.")
