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
"""Igor binarywave file reader into NXmpes implementation for the DataConverter."""
from typing import List, Dict, Any
from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader
from nexusutils.dataconverter.readers.utils import parse_json, parse_yml


def read_igw(fname: str) -> Dict[str, Any]:
    """Parses igor binarywave files into a data template.

    Args:
        fname (str): The filename of the igw file.

    Returns:
        Dict[str, Any]: The template filled with the values from the igw file.
    """
    return {}


# pylint: disable=too-few-public-methods
class MpesIgorReader(YamlJsonReader):
    """HallReader implementation for the DataConverter
    to convert Hall data to Nexus."""

    supported_nxdls: List[str] = ["NXmpes"]
    extensions = {
        ".igw": read_igw,
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, None, None),
        ".yaml": lambda fname: parse_yml(fname, None, None),
    }


READER = MpesIgorReader