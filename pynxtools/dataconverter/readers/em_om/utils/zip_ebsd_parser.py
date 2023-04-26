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
"""Parse Kikuchi pattern from a ZIP file without temporary copies of unpacked files."""

# pylint: disable=no-member,duplicate-code

# https://orix.readthedocs.io/en/stable/tutorials/inverse_pole_figures.html

# type: ignore

# from typing import Dict, Any, List

import re

import numpy as np

from zipfile37 import ZipFile

# import imageio.v3 as iio
from PIL import Image as pil

from pynxtools.dataconverter.readers.em_om.utils.em_nexus_plots import HFIVE_WEB_MAX_SIZE


class NxEmOmZipEbsdParser:
    """Parse *.zip EBSD data.

    """

    def __init__(self, file_name, entry_id):
        """Class wrapping zip parser."""
        # this is one example which should be extended to support reading of
        # EBSD pattern simulations and/or generic EBSD pattern in a zip file
        # frequently pattern are stored as individual images and then compressed
        # and uploaded to online repositories like zenodo
        # this rips these data out of their context, instead one should better
        # create an application definition which interfaces how a computer simulation
        # exports these pattern into a common format (e.g. some of the HDF5 variants)
        self.file_name = file_name
        self.entry_id = entry_id
        self.stack_meta = {}
        self.stack = []

    def parse_zip(self, template: dict) -> dict:
        """Parse content from *.zip format."""
        with ZipFile(self.file_name) as zip_file_hdl:
            # print(zip_file_hdl.namelist())
            # identify first the content in this archive
            # ASSUME that pattern have numeral components in their file name
            zip_content_table = {}
            for file in zip_file_hdl.namelist():
                keyword = str(np.uint64(re.sub('[^0-9]', '', file)))
                if len(keyword) > 0 and keyword not in zip_content_table:
                    zip_content_table[keyword] = file
                else:
                    print("WARNING::Automatically derived name is not unique!")
                    return template
            # not all content though qualifies as Kikuchi pattern
            # people can trick an algorithm always
            #     like camouflage an image file for a text file
            #     upload images which have not the same dimensions
            #     upload images which are for sure not Kikuchi pattern and in fact
            # the last point is highly relevant for NOMAD assume a public instance
            # one could easily inject here inappropriate or illegal material...

            # ASSUME first image specifies file type and dimensions for all pattern to come
            # ...here we immediately see how problematic custom directory structures
            # for storing research data are even if they were to contain only exactly
            # always data of expected format...
            self.stack_meta = {"fname": "",
                               "size": (0, 0),
                               "dtype": np.uint8,
                               "ftype": ""}
            # in pixel, use axisy and axisx for dimension scale axes
            # ASSUME slow axis is y, fast axis is x
            for keyword, value in zip_content_table.items():
                tmp = value.split(".")
                if (len(tmp) > 1) and (tmp[-1].lower() in ["bmp", "jpg", "png", "tiff"]):
                    # there are examples where people store Kikuchi diffraction pattern
                    # as lossy and lossless raster...
                    # pil supports reading of files in more formats but the above are
                    # the formats typically used for Kikuchi pattern
                    with zip_file_hdl.open(value) as file_hdl:
                        # ##MK::would be to not load the entire image but just shape tags
                        img = pil.open(file_hdl, "r")  # np.asarray(pil.open(file_hdl))
                        if img.mode != "L":
                            # https://stackoverflow.com/questions/1996577/
                            # how-can-i-get-the-depth-of-a-jpg-file
                            break
                        shp = (img.height, img.width)  # np.shape(img)
                        if (shp[0] > 0) and (shp[0] <= HFIVE_WEB_MAX_SIZE) \
                                and (shp[1] > 0) and (shp[1] <= HFIVE_WEB_MAX_SIZE):
                            # found the guiding image
                            self.stack_meta["size"] = (shp[0], shp[1])  # , 3)
                            self.stack_meta["fname"] = value
                            self.stack_meta["ftype"] = tmp[-1].lower()
                            self.stack_meta["dtype"] = np.uint8  # for mode "L"
                            # ##MK::bit depth and other constraints
                            break
                            # ##MK::at the moment not supporting > HFIVE_WEB_MAX_SIZE
                            # images but this is usually not required
            print(self.stack_meta)
            # ASSUME that the user has stored all other relevant images of the stack
            # with useful numeral names and that these have the same metadata
            # (size, filetype, dtype)
            identifier = 0
            self.stack = np.zeros((len(zip_content_table),
                                   self.stack_meta["size"][0],
                                   self.stack_meta["size"][1]),
                                  self.stack_meta["dtype"])
            for keyword, value in zip_content_table.items():
                tmp = value.split(".")
                if (len(tmp) > 1) and (tmp[-1].lower() == self.stack_meta["ftype"]):
                    with zip_file_hdl.open(value) as file_handle:
                        # img = np.asarray(pil.open(file_handle))
                        img = pil.open(file_handle, "r")
                        if (img.mode == "L") and (img.palette is None):
                            img = np.asarray(img, np.uint8)
                            # ##MK::for bitmap no need to discard alpha channels, check
                            # print(np.shape(img))
                            # img = img[:, :, 0:3]  # discard eventual alpha channels
                        else:
                            break

                        if (np.shape(img) == self.stack_meta["size"]) \
                                and (img.dtype == self.stack_meta["dtype"]):
                            self.stack[identifier, :, :] = img
                            # Kikuchi pattern may come as 8-bit (grayscale) RGBs
                            # or as simulated intensities (as floats)
                            # ASSUME here we load only images when [1, HFIVE_WEB_MAX_SIZE]
                            # and map eventual RGB bitmaps on intensities
                            identifier += 1
            # okay this is about the intensity but what about the dimension scale axes
            # with tiff these could be stored in the tiff tag image metadata
            # print(np.shape(self.kikuchi))
            # print(self.kikuchi)
        return template

    def parse_pattern_stack_default_plot(self, template: dict) -> dict:
        """Parse data for the Kikuchi image stack default plot."""
        print("Parse Kikuchi pattern stack default plot...")
        trg = f"/ENTRY[entry{self.entry_id}]/simulation/IMAGE_SET_EM_KIKUCHI" \
              f"[image_set_em_kikuchi]/stack"

        template[f"{trg}/title"] = str("Kikuchi diffraction pattern stack")
        template[f"{trg}/@signal"] = "data_counts"
        template[f"{trg}/@axes"] = ["axis_x", "axis_y"]
        template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(0)
        template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(1)

        trg = f"/ENTRY[entry{self.entry_id}]/simulation/IMAGE_SET_EM_KIKUCHI" \
              f"[image_set_em_kikuchi]/stack/data_counts"
        template[f"{trg}"] = {"compress": self.stack, "strength": 1}
        # 0 is y while 1 is x !
        template[f"{trg}/@long_name"] = "Signal"
        template[f"{trg}/@CLASS"] = "IMAGE"  # required by H5Web to plot RGB maps
        template[f"{trg}/@IMAGE_VERSION"] = "1.2"
        template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

        axes_names = [("axis_x", 1, "x-axis"), ("axis_y", 0, "y-axis")]
        for axis in axes_names:
            trg = f"/ENTRY[entry{self.entry_id}]/simulation/IMAGE_SET_EM_KIKUCHI" \
                  f"[image_set_em_kikuchi]/stack/{axis[0]}"
            axis_i = np.asarray(
                np.linspace(0, self.stack_meta["size"][axis[1]],
                            num=self.stack_meta["size"][axis[1]],
                            endpoint=True), np.float64)
            # overwrite with calibrated scale if available
            # i.e. when self.stack_meta["axis_x"] not None:
            template[f"{trg}"] = {"compress": axis_i, "strength": 1}
            template[f"{trg}/@long_name"] = f"Pixel coordinate along {axis[2]}"
            template[f"{trg}/@units"] = "px"
        return template

    def parse(self, template: dict) -> dict:
        """Parse NOMAD OASIS relevant data and metadata from a ZIP file."""
        print("Parsing EBSD data generic-style for a ZIP example...")
        print(self.file_name)
        print(f"{self.entry_id}")
        self.parse_zip(template)
        self.parse_pattern_stack_default_plot(template)
        return template
