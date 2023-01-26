#!/usr/bin/env python3
"""Classes representing groups with NeXus-ish formatted data parsed from hspy."""

# -*- coding: utf-8 -*-
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

# pylint: disable=E1101

from typing import Dict

import numpy as np

import hyperspy.api as hs

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_nexus_base_classes \
    import NxObject


class HspyRectRoiAdfImage:
    """Representing a stack of annular dark field image(s) with metadata."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["long_name"] = NxObject()
        self.meta["intensity"] = NxObject()
        self.meta["image_id"] = NxObject()
        self.meta["xpos"] = NxObject()
        self.meta["xpos_long_name"] = NxObject()
        self.meta["ypos"] = NxObject()
        self.meta["ypos_long_name"] = NxObject()
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s2d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s2d.metadata["Signal"]["signal_type"] == "", \
            "hspy_s2d is not a valid hyperspy generic instance !"
        assert hspy_s2d.data.ndim == 2, \
            "hspy_s2d is not a valid 2D dataset !"
        axes_dict = hspy_s2d.axes_manager.as_dictionary()
        required_axis_names = ["axis-0", "axis-1"]
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + " is unexpectedly not registered in the axes_manager !"
        required_keywords = ["_type", "name", "units", "size", "scale", "offset"]
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    "hspy_s2d axis " + keyword + " lacks " + req_key + " !"
            assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                keyword + ", this axis is not of type UniformDataAxis !"
            avail_axis_names.append(axes_dict[keyword]["name"])

        axes_as_expected_emd \
            = np.all(np.sort(avail_axis_names) == np.sort(["y", "x"]))
        axes_as_expected_bcf \
            = np.all(np.sort(avail_axis_names) == np.sort(["height", "width"]))
        # ##MK::Adrien/Cecile"s BCF and EMD example contains at least one
        # such case where the hyperspy created view in metadata is not
        # consistent across representations generated with different parses
        # which demands adaptive strategies like the one above
        # in the example e.g. the Bruker HAADF image stores dimensions
        # as height and width, where digital micrograph and Velox EMD store
        # y and x... both names are useless without a coordinate system
        # so here discussions with vendors, hspy developers and community are
        # needed
        if (axes_as_expected_emd is False) and (axes_as_expected_bcf is False):
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s2d):
        """Parse a hyperspy Signal2D instance into an NX default plottable."""
        # self.long_name.value = hspy_s2d.metadata["Signal"]["signal_type"]
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        self.meta["long_name"].value = hspy_s2d.metadata["General"]["title"]
        self.meta["intensity"].value = hspy_s2d.data  # hspy uses numpy and adapts ??
        axes_dict = hspy_s2d.axes_manager.as_dictionary()
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])
            y_axis = (axes_dict[keyword]["name"] == "y") \
                or (axes_dict[keyword]["name"] == "height")
            x_axis = (axes_dict[keyword]["name"] == "x") \
                or (axes_dict[keyword]["name"] == "width")
            if y_axis is True:
                assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                    keyword + ", this x axis is not of type UniformDataAxis !"
                self.meta["ypos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["ypos"].unit = unit
                self.meta["ypos_long_name"].value = "y"  # ##MK::name y always!
            if x_axis is True:
                assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                    keyword + ", this y axis is not of type UniformDataAxis !"
                self.meta["xpos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["xpos"].unit = unit
                self.meta["xpos_long_name"].value = "x"  # ##MK::name x always!
            # ##MK::improve case handling
        self.is_valid = True


class NxImageSetEmAdf:
    """Representing a set of (HA)ADF images with metadata."""

    def __init__(self, hspy_list):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject()
        self.meta["program_version"] = NxObject(is_attr=True)
        self.meta["adf_inner_half_angle"] = NxObject()
        self.meta["adf_outer_half_angle"] = NxObject()
        # an NXdata object, here represented as an instance of HspyRectRoiAdfImage
        self.data = []
        self.is_valid = True

        self.is_an_implemented_case(hspy_list)
        self.parse_hspy_instances(hspy_list)

    def is_an_implemented_case(self, hspy_list):
        """Check if signal instances in a list is a supported combination."""
        # an Xray analysis which this implementation supports should consist of
        # a rectangular ROI are currently supported, this ROI should have
        # one HAADF overview image
        # one SpectraStack cnts = f(y, x, energy)
        # one accumulated "sum" spectra cnts = f(energy)
        # an arbitrary number of single element X-ray maps cnts = f(y, x)
        cardinality_adf = 0
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.Signal2D) is True:
                if hspy_clss.metadata["General"]["title"] == "HAADF":
                    cardinality_adf += 1
        if cardinality_adf != 1:
            self.is_valid = False

    def parse_hspy_instances(self, hspy_list):
        """Extract hspy class instances.

        These have to be mappable on NXem base classes
        if these are understood by NOMAD OASIS.
        """
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.Signal2D) is True:
                ndim = hspy_clss.data.ndim
                if ndim == 2:
                    if hspy_clss.metadata["General"]["title"] == "HAADF":
                        self.data.append(HspyRectRoiAdfImage(hspy_clss))
                        # if self.data[-1].is_valid is False:
                        #     self.is_valid = False

    def report(self, prefix: str, frame_id: int, template: dict) -> dict:
        """Enter data from the NX-specific representation into the template."""
        if self.is_valid is False:
            print("\t" + __name__ + " reporting nothing!")
            return template
        print("\t" + __name__ + " reporting...")
        assert (len(self.data) >= 0) and (len(self.data) <= 1), \
            "More than one spectrum stack is currently not supported!"
        trg = prefix + "NX_IMAGE_SET_EM_ADF[image_set_em_adf" + str(frame_id) + "]/"

        # template[trg + "program"] = "hyperspy"
        # template[trg + "program/@version"] = hs.__version__
        # MISSING_DATA_MSG = "not in hspy metadata case specifically in original_metadata"
        # ##MK::!!!!!
        # ##MK::how to communicate that these data do not exist?
        # template[trg + "adf_outer_half_angle"] = np.float64(0.)
        # template[trg + "adf_outer_half_angle/@units"] = "rad"
        # template[trg + "adf_inner_half_angle"] = np.float64(0.)
        # template[trg + "adf_inner_half_angle/@units"] = "rad"
        if len(self.data) == 1:
            prfx = trg + "DATA[adf]/"
            template[prfx + "@NX_class"] = "NXdata"
            # ##MK::usually this should be added by the dataconverter automatically
            template[prfx + "@long_name"] = self.data[0].meta["long_name"].value
            template[prfx + "@signal"] = "intensity"
            template[prfx + "@axes"] = ["ypos", "xpos"]
            template[prfx + "@xpos_indices"] = 1
            template[prfx + "@ypos_indices"] = 0
            template[prfx + "intensity"] \
                = {"compress": self.data[0].meta["intensity"].value}
            template[prfx + "intensity/@units"] = ""
            # but should be a 1 * n_y * n_x array and not a n_y * n_x array !!
            template[prfx + "image_id"] = np.uint32(frame_id)
            template[prfx + "xpos"] \
                = {"compress": self.data[0].meta["xpos"].value}
            template[prfx + "xpos/@units"] \
                = self.data[0].meta["xpos"].unit
            template[prfx + "ypos"] \
                = {"compress": self.data[0].meta["ypos"].value}
            template[prfx + "ypos/@units"] \
                = self.data[0].meta["ypos"].unit
            # template[prfx + "title"] = "ADF"

        return template
