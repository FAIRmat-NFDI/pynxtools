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
"""Constants and utilities used when parsing concepts from HDF5 files."""

from typing import Dict

IS_GROUP = 0
IS_REGULAR_DATASET = 1
IS_COMPOUND_DATASET = 2
IS_FIELD_IN_COMPOUND_DATASET = 3
IS_ATTRIBUTE = 4
VERSION_MANAGEMENT: Dict = {"tech_partner": [],
                            "schema_name": [], "schema_version": [],
                            "writer_name": [], "writer_version": []}


class Concept():
    def __init__(self, instance_name=None,
                 concept_name=None, value=None, dtype=None,
                 shape=None, unit_info=None, **kwargs):
        if instance_name is not None:
            if isinstance(instance_name, str):
                if len(instance_name) > 0:
                    self.name = instance_name
                else:
                    raise ValueError("instance_name must not be empty!")
            else:
                raise ValueError("instance_name has to be a string or None!")
        else:
            self.name = None
        if concept_name is not None:
            if isinstance(concept_name, str):
                if len(concept_name) > 0:
                    self.concept = concept_name
                else:
                    raise ValueError("concept_name must not be empty!")
            else:
                raise ValueError("concept_name has to be a string or None!")
        else:
            self.concept = None
        self.value = value
        self.dtype = dtype
        self.shape = shape
        if unit_info is not None:
            # unit existence, unit category, or specific unit statement
            if isinstance(unit_info, str):
                if len(unit_info) > 0:
                    # testing against pint
                    self.unit = unit_info
                else:
                    raise ValueError("unit_info must not be empty!")
            else:
                raise ValueError("unit_info has to be a string or None!")
        else:
            self.unit = None
        if "hdf_type" in kwargs.keys():
            if kwargs["hdf_type"] is not None:
                if isinstance(kwargs["hdf_type"], str):
                    if kwargs["hdf_type"] in ["group",
                                              "regular_dataset",
                                              "compound_dataset",
                                              "compound_dataset_entry",
                                              "attribute"]:
                        self.hdf = kwargs["hdf_type"]

    def report(self):
        members = vars(self)
        for key, val in members.items():
            print(f"{key}, type: {type(val)}, value: {val}")

# test = Concept("1/@Test", "*/@Test", 1, type(1), np.shape(1),
#                "UNITLESS", hdf_type="group")
# test.report()
