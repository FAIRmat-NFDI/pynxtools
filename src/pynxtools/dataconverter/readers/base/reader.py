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
"""The abstract class off of which to implement readers."""

from abc import ABC, abstractmethod
from typing import Tuple, Any


class BaseReader(ABC):
    """
    The abstract class off of which to implement readers.

    The filename's prefix is the identifier. The '_reader.py' is snipped out.
    For this BaseReader with filename base_reader.py the ID  becomes 'base'

    For future reference:
    - Support links by setting the path in the template with the following object
       object = {"link": "/path/to/source/data"}
    """

    # pylint: disable=too-few-public-methods

    __name__ = "BaseReader"

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = [""]

    @abstractmethod
    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        return template


READER = BaseReader
