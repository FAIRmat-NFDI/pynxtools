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
"""Definition of DREAM3D SIMPL filters and their controlled vocabulary."""

# pylint: disable=E1101

import numpy as np

from typing import Dict, Any, List


class DreamThreedFilter():
    """Description of a filter/plug-in from DREAM.3D."""

    def __init__(self, version="", name="", dct=None, **kwargs):
        # mandatory
        self.version = ""
        assert isinstance(version, str), "Argument version has to be a string!"
        # assert version != "", "Version mandatory!"
        self.version = version
        self.name = ""
        assert isinstance(name, str), "Argument name has to be a string!"
        # assert name != "", "Name mandatory!"
        self.name = name

        # optional
        self.human_label = ""
        if "human_label" in kwargs.keys():
            self.human_label = kwargs["human_label"]
        self.enabled = False
        if "enabled" in kwargs.keys():
            self.enabled = kwargs["enabled"]
        self.uuid = ""
        if "uuid" in kwargs.keys():
            self.uuid = kwargs["uuid"]

        # controlled flattened keywords
        self.terms = {}
        # if dct is not None:
        #     for key in dct.keys():
        #         self.terms[key] = "add something useful"
        print(f"DREAM.3D filter instance, version {self.version}, name {self.name}")

    def debug(self):
        """Offer functionality testing"""
        tmp = DreamThreedFilter(version="12", name="test")
