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
    TiffTfsConcepts, TiffTfsToNeXusCfg, get_fei_parent_concepts, get_fei_childs
from pynxtools.dataconverter.readers.em.utils.image_utils import \
    sort_ascendingly_by_second_argument, if_str_represents_float


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
        tfs_parent_concepts = get_fei_parent_concepts()
        tfs_parent_concepts_byte_offset = {}
        for concept in tfs_parent_concepts:
            tfs_parent_concepts_byte_offset[concept] = None
        with open(self.file_path, 'rb', 0) as fp:
            s = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
            for concept in tfs_parent_concepts:
                pos = s.find(bytes(f"[{concept}]", "utf8"))  # != -1
                if pos != -1:
                    tfs_parent_concepts_byte_offset[concept] = pos
                else:
                    raise ValueError(f"Expected block with metadata for concept [{concept}] were not found !")
            print(tfs_parent_concepts_byte_offset)

            sequence = []  # decide I/O order in which metadata for childs of parent concepts will be read
            for key, value in tfs_parent_concepts_byte_offset.items():
                if value is not None:
                    sequence.append((key, value)) 
                    # tuple of parent_concept name and byte offset
            sequence = sort_ascendingly_by_second_argument(sequence)
            print(sequence)

            idx = 0
            for parent, byte_offset in sequence:
                pos_s = byte_offset
                pos_e = None
                if idx < len(sequence) - 1:
                    pos_e = sequence[idx + 1][1]
                else:
                    pos_e = np.iinfo(np.uint64).max
                idx += 1
                if pos_s is None or pos_e is None:
                    raise ValueError(f"Definition of byte boundaries for reading childs of [{parent}] was unsuccessful !")
                print(f"Search for [{parent}] in between byte offsets {pos_s} and {pos_e}")

                # fish metadata of e.g. the system section
                for term in get_fei_childs(parent):
                    s.seek(pos_s, 0)
                    pos = s.find(bytes(f"{term}=", "utf8"))
                    if pos < pos_e:  # check if pos_e is None
                        s.seek(pos, 0)
                        value = f"{s.readline().strip().decode('utf8').replace(f'{term}=', '')}"
                        self.tfs[f"{parent}/{term}"] = None
                        if isinstance(value, str):
                            if value != "":
                                if if_str_represents_float(value) is True:
                                    self.tfs[f"{parent}/{term}"] = np.float64(value)
                                elif value.isdigit() is True:
                                    self.tfs[f"{parent}/{term}"] = np.int64(value)
                                else:
                                    self.tfs[f"{parent}/{term}"] = value
                        else:
                            print(f"{parent}/{term} ---> {type(value)}")                
                    else:
                        pass
            for key, val in self.tfs.items():
                print(f"{key}, {val}")

    def parse_and_normalize(self):
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            print(f"Parsing via ThermoFisher-specific metadata...")
            self.get_metadata()
        else:
            print(f"{self.file_path} is not a ThermoFisher-specific "
                  f"TIFF file that this parser can process !")
