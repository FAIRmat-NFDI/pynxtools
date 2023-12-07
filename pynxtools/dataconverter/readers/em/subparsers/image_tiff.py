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
"""Derived image class to derive every tech-partner-specific TIFF subparser from."""

import mmap
import numpy as np
from typing import Dict
from PIL import Image
from PIL.TiffTags import TAGS

from pynxtools.dataconverter.readers.em.subparsers.image_base import ImgsBaseParser


class TiffReader(ImgsBaseParser):
    """Read Bruker Esprit H5"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp: Dict = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        self.tags: Dict = {}
        self.check_if_tiff()
        if self.supported is True:
            self.get_tags()

    def check_if_tiff(self):
        """Check if instance can at all be likely a TaggedImageFormat file via magic number."""
        self.supported = 0  # voting-based
        with open(self.file_path, 'rb', 0) as file:
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            magic = s.read(4)
            print(magic)
            # TODO::add magic number https://en.wikipedia.org/wiki/TIFF
            self.supported += 1
            if self.supported == 1:
                self.supported = True
            else:
                self.supported = False

    def get_tags(self):
        """Extract tags if present."""
        with Image.open(self.file_path, mode="r") as fp:
            self.tags = {TAGS[key] : fp.tag[key] for key in fp.tag_v2}
            for key, val in self.tags.items():
                print(f"{key}, {val}")
