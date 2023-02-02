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
"""Classes representing groups with NeXus-ish formatted data parsed from hspy."""

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
        # consistent across representations generated with different parsers
        # this demands adaptive strategies like the one above
        # in the example e.g. the Bruker HAADF image stores dimensions
        # as height and width, while digital micrograph and Velox EMD store
        # y and x... both names are useless without a coordinate system
        # so here discussions with vendors, hspy developers and community are
        # needed!
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
        # an Xray analysis which this implementation can support needs to be
        # a rectangular ROI. This ROI should have one HAADF overview image
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
        trg = prefix + "IMAGE_SET_EM_ADF[image_set_em_adf" + str(frame_id) + "]/"

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
            prfx = trg + "stack/"
            template[prfx + "title"] = "Annular dark field image stack"
            # template[prfx + "@long_name"] = self.data[0].meta["long_name"].value
            template[prfx + "@signal"] = "data_counts"
            template[prfx + "@axes"] = ["axis_image_identifier", "axis_y", "axis_x"]
            template[prfx + "@AXISNAME[axis_x_indices]"] = 2
            template[prfx + "@AXISNAME[axis_y_indices]"] = 1
            template[prfx + "@AXISNAME[axis_image_identifier]"] = 0
            template[prfx + "DATA[data_counts]"] \
                = {"compress": np.reshape(
                    np.atleast_3d(self.data[0].meta["intensity"].value),
                    (1,
                     np.shape(self.data[0].meta["intensity"].value)[0],
                     np.shape(self.data[0].meta["intensity"].value)[1])),
                    "strength": 1}
            # is the data layout correct?
            # I am pretty sure the last two have to be swopped also!!
            template[prfx + "DATA[data_counts]/@units"] = ""
            template[prfx + "DATA[data_counts]/@long_name"] = "Counts (a.u.)"
            template[prfx + "AXISNAME[axis_x]"] \
                = {"compress": self.data[0].meta["xpos"].value, "strength": 1}
            template[prfx + "AXISNAME[axis_x]/@units"] = self.data[0].meta["xpos"].unit
            template[prfx + "AXISNAME[axis_x]/@long_name"] \
                = "x (" + self.data[0].meta["xpos"].unit + ")"
            template[prfx + "AXISNAME[axis_y]"] \
                = {"compress": self.data[0].meta["ypos"].value, "strength": 1}
            template[prfx + "AXISNAME[axis_y]/@units"] = self.data[0].meta["ypos"].unit
            template[prfx + "AXISNAME[axis_y]/@long_name"] \
                = "y (" + self.data[0].meta["ypos"].unit + ")"
            template[prfx + "AXISNAME[axis_image_identifier]"] \
                = np.atleast_1d(np.uint32(frame_id))
            template[prfx + "AXISNAME[axis_image_identifier]/@units"] = ""
            template[prfx + "AXISNAME[axis_image_identifier]/@long_name"] \
                = "image identifier"

        return template
