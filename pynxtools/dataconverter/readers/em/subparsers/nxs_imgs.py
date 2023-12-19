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
from PIL import Image

from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs import TfsTiffSubParser
from pynxtools.dataconverter.readers.em.subparsers.image_png_protochips import ProtochipsPngSetSubParser
from pynxtools.dataconverter.readers.em.utils.hfive_web_utils import hfive_web_decorate_nxdata


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
        # img = TfsTiffSubParser(f"{self.file_path}")
        # if img.supported is True:
        #     return "single_tiff_tfs"
        img = ProtochipsPngSetSubParser(f"{self.file_path}")
        if img.supported is True:
            return "set_of_zipped_png_protochips"
        return None

    def parse(self, template: dict) -> dict:
        image_parser_type = self.identify_image_type()
        if image_parser_type is None:
            print(f"{self.file_path} does not match any of the supported image formats")
            return template
        print(f"Parsing via {image_parser_type}...")
        # see also comments for respective nxs_pyxem parser
        # and its interaction with tech-partner-specific hfive_* subparsers

        if image_parser_type == "single_tiff_tfs":
            tiff = TfsTiffSubParser(self.file_path, self.entry_id)
            tiff.parse_and_normalize()
            tiff.process_into_template(template)
        elif image_parser_type == "set_of_zipped_png_protochips":
            pngs = ProtochipsPngSetSubParser(self.file_path, self.entry_id)
            pngs.parse_and_normalize()
            pngs.process_into_template(template)
        # else:
            # TODO::add here specific content parsers for other tech partner
            # or other custom parsing of images
        return template
