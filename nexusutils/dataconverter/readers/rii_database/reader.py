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
"""Convert refractiveindex.info yaml files to nexus"""
from typing import Tuple, Any, Dict
from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader


def read_dispersion(filename: str) -> Dict[str, Any]:
    """Reads rii dispersions from yaml files"""

    return {}


def handle_objects(objects: Tuple[Any]) -> Dict[str, Any]:
    """Handle objects and generate template entries from them"""

    return {}


# pylint: disable=too-few-public-methods
class RiiReader(YamlJsonReader):
    """
    Converts refractiveindex.info yaml files to nexus
    """

    supported_nxdls = ["NXdispersive_material"]
    extensions = {
        ".yml": read_dispersion,
        ".yaml": read_dispersion,
        "objects": handle_objects
    }


READER = RiiReader
