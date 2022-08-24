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

# from typing import Tuple, Any

import numpy as np

import hyperspy.api as hs

from nexusparser.tools.dataconverter.readers.em.utils.em_nexus_base_classes \
    import NxObject


class HspyRectRoiAdfImage:
    """Representing a stack of annular dark field image(s) with metadata."""

    def __init__(self, hspy_clss):
        self.long_name = NxObject()
        self.intensity = NxObject()
        self.image_id = NxObject()
        self.xpos = NxObject()
        self.xpos_long_name = NxObject()
        self.ypos = NxObject()
        self.ypos_long_name = NxObject()

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s2d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s2d.metadata['Signal']['signal_type'] == '', \
            'hspy_s2d is not a valid hyperspy generic instance !'
        assert hspy_s2d.data.ndim == 2, \
            'hspy_s2d is not a valid 2D dataset !'
        axes_dict = hspy_s2d.axes_manager.as_dictionary()
        required_axis_names = ['axis-0', 'axis-1']
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + ' is unexpectedly not registered in the axes_manager !'
        required_keywords = ['_type', 'name', 'units', 'size', 'scale', 'offset']
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    'hspy_s2d axis ' + keyword + ' lacks ' + req_key + ' !'
            assert axes_dict[keyword]['_type'] == "UniformDataAxis", \
                keyword + ', this axis is not of type UniformDataAxis !'
            avail_axis_names.append(axes_dict[keyword]['name'])

        if np.all(np.sort(avail_axis_names) == np.sort(['y', 'x'])) is True:
            return True
        else:
            return False

    def parse(self, hspy_s2d):
        """Parse a hyperspy Signal2D instance into an NX default plottable."""
        self.long_name.value = hspy_s2d.metadata['Signal']['signal_type']
        self.intensity.value = np.asarray(hspy_s2d.data, np.float64)
        axes_dict = hspy_s2d.axes_manager.as_dictionary()
        for keyword, value in axes_dict.items():
            offset = np.float64(axes_dict[keyword]['offset'])
            scale = np.float64(axes_dict[keyword]['scale'])
            size = np.uint32(axes_dict[keyword]['size'])
            unit = str(axes_dict[keyword]['units'])
            if axes_dict[keyword]['name'] == 'y':
                assert axes_dict[keyword]['_type'] == "UniformDataAxis", \
                    keyword + ', this x axis is not of type UniformDataAxis !'
                self.ypos.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.ypos.unit = unit
                self.ypos_long_name.value = 'y'
            else:  # axes_dict[keyword]['name'] == 'x':
                assert axes_dict[keyword]['_type'] == "UniformDataAxis", \
                    keyword + ', this y axis is not of type UniformDataAxis !'
                self.xpos.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.xpos.unit = unit
                self.xpos_long_name.value = 'x'


class NxImageSetEmAdf:
    """Representing a set of (HA)ADF images with metadata."""

    def __init__(self, hspy_list):
        self.program = NxObject()
        self.program_version = NxObject(is_attr=True)
        self.adf_inner_half_angle = NxObject()
        self.adf_outer_half_angle = NxObject()
        # an NXdata object, here represented as an instance of HspyRectRoiAdfImage
        self.data = []

        if self.is_an_implemented_case(hspy_list) is True:
            self.parse_hspy_instances(hspy_list)
            print('NxImageSetEmAdf successfully parsed hspy objects')
        else:
            print('NxImageSetEmAdf does not support these this hspy object set!')

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
                if hspy_clss.metadata['General']['title'] == 'HAADF':
                    cardinality_adf += 1
        if cardinality_adf == 1:
            return True
        else:
            return False

    def parse_hspy_instances(self, hspy_list):
        """Extract hspy class instances.

        These have to be mappable on NXem base classes
        if these are understood by NOMAD OASIS.
        """
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.Signal2D) is True:
                ndim = hspy_clss.data.ndim
                if ndim == 2:
                    if hspy_clss.metadata['General']['title'] == 'HAADF':
                        self.data.append(HspyRectRoiAdfImage(hspy_clss))

    def report(self, prefix: str, frame_id: int, template: dict) -> dict:
        """Enter data from the NX-specific representation into the template."""
        trg = prefix + "NX_IMAGE_SET_EM_ADF[image_set_em_adf_" + str(frame_id) + "]/"
        template[trg + "program"] = 'hyperspy'
        template[trg + "program/@version"] = hs.__version__
        # MISSING_DATA_MSG = "not in hspy metadata case specifically in original_metadata"
        # ##MK::!!!!!
        # ##MK::how to communicate that these data do not exist?
        # template[trg + "adf_outer_half_angle"] = np.float64(0.)
        # template[trg + "adf_outer_half_angle/@units"] = 'rad'
        # template[trg + "adf_inner_half_angle"] = np.float64(0.)
        # template[trg + "adf_inner_half_angle/@units"] = 'rad'
        trg += "DATA[adf]/"
        template[trg + "@long_name"] = self.data[0].long_name.value
        template[trg + "@signal"] = "intensity"
        template[trg + "@axes"] = ["ypos", "xpos"]
        template[trg + "@ypos_indices"] = np.uint32(0)
        template[trg + "@xpos_indices"] = np.uint32(1)
        template[trg + "intensity"] = self.data[0].intensity.value
        # but should be a 1 * n_y * n_x array and not a n_y * n_x array !!
        template[trg + "image_id"] = np.uint32(frame_id)
        template[trg + "ypos"] = self.data[0].ypos.value
        template[trg + "ypos/@units"] = self.data[0].ypos.unit
        template[trg + "xpos"] = self.data[0].xpos.value
        template[trg + "xpos/@units"] = self.data[0].xpos.unit
        template[trg + "title"] = "ADF"
        return template
