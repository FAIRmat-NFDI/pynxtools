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
from typing import Tuple, List

from nexusparser.tools.dataconverter.readers.base_reader import BaseReader


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXspe"]

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        metadata: List[str] = []

        for file_path in file_paths:
            file_extension = file_path[file_path.rindex("."):]
            with open(file_path, "r") as input_file:
                if file_extension == ".metadata_extension":
                    metadata = input_file.read().split("\n")

        for value in metadata:
            # The entries in the template dict should correspond with what the dataconverter
            # outputs with --generate-template for a provided NXDL file
            template[f"/entry/instrument/metadata/{value}"] = value

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
