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
"""Parser mapping content of specific image files on NeXus."""

import numpy as np
# from typing import Dict, Any, List

from pynxtools.dataconverter.readers.em.subparsers.image_tiff import TiffSubParser


class NxEmImagesSubParser:
    """Map content from different type of image files on an instance of NXem."""

    def __init__(self, entry_id: int = 1, input_file_name: str = ""):
        """Overwrite constructor of the generic reader."""
        if entry_id > 0:
            self.entry_id = entry_id
        else:
            self.entry_id = 1
        self.file_path = input_file_name
        self.cache = {"is_filled": False}

    def identify_image_type(self):
        """Identify if image matches known mime type and has content for which subparser exists."""
        # tech partner formats used for measurement
        img = TiffSubParser(f"{self.file_path}")
        if img.supported is True:
            return "tiff"
        return None

    def parse(self, template: dict) -> dict:
        image_parser_type = self.identify_image_type()
        if image_parser_type is None:
            print(f"{self.file_path} does not match any of the supported image formats")
            return template
        print(f"Parsing via {image_parser_type}...")
        # see also comments for respective nxs_pyxem parser
        # and its interaction with tech-partner-specific hfive_* subparsers

        if image_parser_type == "tiff":
            tiff = TiffSubParser(self.file_path)
            tiff.parse_and_normalize()
            self.process_into_template(tiff.tmp, template)
        else:  # none or something unsupported
            return template
        return template

    def process_into_template(self, inp: dict, template: dict) -> dict:
        debugging = False
        if debugging is True:
            for key, val in inp.items():
                if isinstance(val, dict):
                    for ckey, cval in val.items():
                        print(f"{ckey}, {cval}")
                else:
                    print(f"{key}, {val}")
        # TODO:: implement actual mapping on template
        # self.process_roi_overview(inp, template)
        return template
