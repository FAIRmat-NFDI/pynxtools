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


class Template(dict):
    """A Template object to control and separate template paths according to optionality"""

    def __init__(self, template=None, **kwargs):
        super(Template, self).__init__(**kwargs)
        self.iteration_index = 0
        if template is None:
            self.optional: dict = {}
            self.recommended: dict = {}
            self.required: dict = {}
            self.optional_parents: list = []
        else:
            self.optional: dict = copy.deepcopy(template["optional"])
            self.recommended: dict = copy.deepcopy(template["recommended"])
            self.required: dict = copy.deepcopy(template["required"])
            self.optional_parents: list = copy.deepcopy(template["optional_parents"])

    def get_accumulated_dict(self):
        """Returns a dictionary of all the optionalities merged into one."""
        return {**self.optional, **self.recommended, **self.required}

    def __repr__(self):
        """Returns a unique string representation for the Template object."""
        return self.get_accumulated_dict().__repr__()

    def __str__(self):
        """Returns a readable string representation for the Template object."""
        accumulated_dict = self.get_accumulated_dict()
        accumulated_dict.update((key, "None") for key in accumulated_dict)
        return json.dumps(accumulated_dict, indent=4, sort_keys=True)

    def __setitem__(self, k, v):
        """Handles how values are set within the Template object."""
        if k.startswith("/"):
            if k in self.optional:
                self.optional[k] = v
            elif k in self.recommended:
                self.recommended[k] = v
            elif k in self.required:
                self.required[k] = v
            else:
                raise KeyError("You can only set already existing paths.")
        else:
            raise KeyError("You cannot add non paths to the root template object. "
                           "Place them appropriately e.g. template[\"optional\"]")

    def keys(self):
        """Returns the list of keys stored in the Template object."""
        return list(self.optional.keys()) + \
            list(self.recommended.keys()) + \
            list(self.required.keys())

    def items(self):
        """Returns a list of tuples of key, value stored in the Template object."""
        return self.get_accumulated_dict().items()

    def __iter__(self):
        return iter(self.keys())

    def get_optionality(self, optionality):
        """Returns the dictionary for given optionality"""
        if optionality == "optional":
            return self.optional
        if optionality == "recommended":
            return self.recommended
        if optionality == "required":
            return self.required
        return self.required

    def __getitem__(self, k):
        """Handles how values are accessed from the Template object."""
        # Try setting item in all else throw error. Does not append to default.
        if k in ("optional", "recommended", "required"):
            return self.get_optionality(k)
        if k == "optional_parents":
            return self.optional_parents
        if k.startswith("/"):
            try:
                return self.optional[k]
            except KeyError:
                try:
                    return self.recommended[k]
                except KeyError:
                    return self.required[k]
        raise KeyError("You can only set keys to the internal dicts using "
                       "e.g. template.optional[\"/path\"] = value")

    def clear(self):
        """Clears all data stored in the Template object."""
        for del_dict in (self.optional, self.recommended, self.required):
            del_dict.clear()

    def add_entry(self):
        """Add the whole NXDL again with a new HDF5 name for the template."""
        # TODO: Implement
