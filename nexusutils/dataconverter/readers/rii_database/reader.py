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
import logging

from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader
from nexusutils.dataconverter.readers.rii_database.dispersion_reader import (
    DispersionReader,
)
from nexusutils.dataconverter.readers.utils import parse_json


class RiiReader(YamlJsonReader):
    """
    Converts refractiveindex.info yaml files to nexus
    """

    supported_nxdls = ["NXdispersive_material"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extensions = {
            ".yml": self.read_dispersion,
            ".yaml": self.read_dispersion,
            ".json": self.parse_json_w_fileinfo,
            "default": lambda _: self.appdef_defaults(),
            "objects": self.handle_objects,
        }

    def read_dispersion(self, filename: str):
        """Reads the dispersion from the give filename"""
        download_bibtex = self.kwargs.get('download_bibtex', False)
        return DispersionReader(download_bibtex).read_dispersion(filename)

    def appdef_defaults(self) -> Dict[str, Any]:
        """Fills default entries which are comment for the application
        definition. Like appdef version and name"""
        entries: Dict[str, Any] = {}

        entries["/ENTRY[entry]/definition/@version"] = "0.0.1"
        entries["/ENTRY[entry]/definition/@url"] = ""
        entries["/ENTRY[entry]/definition"] = "NXdispersive_material"

        entries["/@default"] = "entry"
        entries["/ENTRY[entry]/@default"] = "dispersion_x"

        return entries

    def fill_dispersion_in(self, template: Dict[str, Any]):
        """
        Replaces dispersion_x and dispersion_y keys with filenames as their value
        with the parsed dispersion values.
        """
        keys = [f"dispersion_{axis}" for axis in ["y", "z"]]

        for key in keys:
            if key in template:
                template.update(
                    DispersionReader().read_dispersion(template[key], identifier=key)
                )
                del template[key]

    def parse_json_w_fileinfo(self, filename: str) -> Dict[str, Any]:
        """
        Reads json key/value pairs and additionally replaces dispersion_x and _y keys
        with their parsed dispersion values.
        """
        template = parse_json(filename)
        self.fill_dispersion_in(template)

        return template

    def handle_objects(self, objects: Tuple[Any]) -> Dict[str, Any]:
        """Handle objects and generate template entries from them"""
        if objects is None:
            return {}

        template = {}

        for obj in objects:
            if not isinstance(obj, dict):
                logging.warning("Ignoring unknown object of type %s", type(obj))
                continue

            template.update(obj)

        self.fill_dispersion_in(template)

        return template


READER = RiiReader
