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
from typing import Any, Callable, Dict, List, Optional, Tuple

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import parse_flatten_json, parse_yml
from pynxtools.dataconverter.template import Template


class MultiFormatReader(BaseReader):
    """
    A reader that takes a mapping json file and a data file/object to return a template.
    """

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls: List[str] = []
    extensions: Dict[str, Callable[[Any], dict]] = {
        ".json": parse_flatten_json,
        ".yaml": parse_yml,
        ".yml": parse_yml,
    }
    kwargs: Optional[Dict[str, Any]] = None

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

    def get_data(self, path: str) -> Dict[str, Any]:
        """
        Returns the data from the given path.
        """
        return {}

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
