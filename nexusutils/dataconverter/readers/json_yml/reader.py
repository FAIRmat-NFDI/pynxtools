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
from typing import Tuple, Any, Callable, Dict, List
import os

from nexusutils.dataconverter.readers.base.reader import BaseReader


class YamlJsonReader(BaseReader):
    """A reader that takes a mapping json file and a data file/object to return a template."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls: List[str] = []
    extensions: Dict[str, Callable[[str], dict]] = {}

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             _: Tuple[Any] = None) -> dict:
        """
        Reads data from multiple files and passes them to the appropriate functions
        in the extensions dict.
        """

        sorted_paths = sorted(file_paths, key=lambda f: os.path.splitext(f)[1])
        for file_path in sorted_paths:
            extension = os.path.splitext(file_path)[1]
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

        template.update(self.extensions.get("default", lambda _: {})(""))

        return template


READER = YamlJsonReader
