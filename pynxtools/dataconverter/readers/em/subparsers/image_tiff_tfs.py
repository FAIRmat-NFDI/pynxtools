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
"""Subparser for harmonizing ThermoFisher-specific content in TIFF files."""

import mmap
import numpy as np
from typing import Dict
from PIL import Image
from PIL.TiffTags import TAGS

from pynxtools.dataconverter.readers.em.subparsers.image_tiff import TiffSubParser
from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs_cfg import \
    tfs_section_names, tfs_section_details
from pynxtools.dataconverter.readers.em.utils.image_utils import \
    sort_tuple, if_str_represents_float


class TfsTiffSubParser(TiffSubParser):
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp: Dict = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.tags: Dict = {}
        self.supported = False
        self.check_if_tiff()
        self.tfs: Dict = {}

    def check_if_tiff_tfs(self):
        """Check if resource behind self.file_path is a TaggedImageFormat file."""
        self.supported = 0  # voting-based
        with open(self.file_path, 'rb', 0) as file:
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            magic = s.read(4)
            if magic == b'II*\x00':  # https://en.wikipedia.org/wiki/TIFF
                self.supported += 1

        with Image.open(self.fiele_path, mode="r") as fp:
            tfs_keys = [34682]
            for tfs_key in tfs_keys:
                if tfs_key in fp.tag_v2:
                    if len(fp.tag[tfs_key]) == 1:
                        self.supported += 1  # found TFS-specific tag
        if self.supported == 2:
            self.supported = True
        else:
            self.supported = False

    def get_metadata(self):
        """Extract metadata in TFS specific tags if present."""
        print("Reporting the tags found in this TIFF file...")
        # for an overview of tags
        # https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml
        # with Image.open(self.file_path, mode="r") as fp:
        #     self.tags = {TAGS[key] : fp.tag[key] for key in fp.tag_v2}
        #     for key, val in self.tags.items():
        #         print(f"{key}, {val}")
        tfs_section_offsets = {}
        with open(self.file_path, 'rb', 0) as fp:
            s = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
            for section_name in tfs_section_names:
                pos = s.find(bytes(section_name, "utf8"))  # != -1
                tfs_section_offsets[section_name] = pos
            print(tfs_section_offsets)

            # define search offsets
            tpl = []
            for key, value in tfs_section_offsets.items():
                tpl.append((key, value))
            tpl = sort_tuple(tpl)
            print(tpl)

            # exemplar parsing of specific TFS section content into a dict
            # here for section_name == "[System]":
            pos_s = None
            pos_e = None
            for idx in np.arange(0, len(tpl)):
                if tpl[idx][0] != "[System]":
                    continue
                else:
                    pos_s = tpl[idx][1]
                    if idx <= len(tpl) - 1:
                        pos_e = tpl[idx + 1][1]
                    break
            print(f"Search for [System] in between byte offsets {pos_s} and {pos_e}")
            if pos_s is None or pos_e is None:
                raise ValueError(f"Search for [System] was unsuccessful !")

            # fish metadata of e.g. the system section
            for term in tfs_section_details["[System]"]:
                s.seek(pos_s, 0)
                pos = s.find(bytes(term, "utf8"))
                if pos < pos_e:  # check if pos_e is None
                    s.seek(pos, 0)
                    value = f"{s.readline().strip().decode('utf8').replace(f'{term}=', '')}"
                    if value != "":
                        if if_str_represents_float(value) is True:
                            self.tfs[f"system/{term}"] = np.float64(value)
                        elif value.isdigit() is True:
                            self.tfs[f"system/{term}"] = np.int64(value)
                        else:
                            self.tfs[f"system/{term}"] = None
                else:
                    pass
            print(self.tfs)

    def parse_and_normalize(self):
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            print(f"Parsing via ThermoFisher-specific metadata...")
            self.get_metadata()
        else:
            print(f"{self.file_path} is not a ThermoFisher-specific "
                  f"TIFF file that this parser can process !")
