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


class HspyRectRoiXraySummarySpectrum:
    """Representing the accumulated X-ray spectrum over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.program = NxObject(value="hyperspy")
        self.program_version = NxObject(value=hs.__version__)
        self.title = NxObject()
        self.long_name = NxObject()  # value='X-ray photon counts')
        self.counts = NxObject()
        self.photon_energy = NxObject()
        self.photon_energy_long_name = NxObject()  # value='X-ray energy')

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s1d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s1d.metadata['Signal']['signal_type'] == 'EDS_TEM', \
            'hspy_s3d is not a valid hyperspy generic instance !'
        assert hspy_s1d.data.ndim == 1, \
            'hspy_s3d is not a valid 1D dataset !'
        axes_dict = hspy_s1d.axes_manager.as_dictionary()
        required_axis_names = ['axis-0']
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + ' is unexpectedly not registered in the axes_manager !'
        required_keywords = ['_type', 'name', 'units', 'size', 'scale', 'offset']
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    'hspy_s1d axis ' + keyword + ' lacks ' + req_key + ' !'

            assert axes_dict[keyword]['_type'] == "UniformDataAxis", \
                keyword + ', this axis is not of type UniformDataAxis !'
            avail_axis_names.append(axes_dict[keyword]['name'])

        if np.all(np.sort(avail_axis_names) == np.sort(['Energy'])) is True:
            return True
        else:
            return False

    def parse(self, hspy_s1d):
        """Parse a hyperspy Signal1D stack instance into an NX default plottable."""
        self.title.value = hspy_s1d.metadata['General']['title']
        # self.long_name.value = hspy_s1d.metadata['Signal']['signal_type']
        self.long_name.value = hspy_s1d.metadata['General']['title']
        self.counts.value = hspy_s1d.data
        # ##MK::it seems that hspy is adaptive, uses numpy under the hood
        # though, so the .data instance is already a proper numpy dtype
        # therefore, an explicit call like this
        # np.asarray(hspy_s1d.data, np.uint32) is not necessary
        axes_dict = hspy_s1d.axes_manager.as_dictionary()
        for keyword, value in axes_dict.items():
            offset = np.float64(axes_dict[keyword]['offset'])
            scale = np.float64(axes_dict[keyword]['scale'])
            size = np.uint32(axes_dict[keyword]['size'])
            unit = str(axes_dict[keyword]['units'])
            # if axes_dict[keyword]['name'] == 'Energy':
            self.photon_energy.value = np.asarray(
                np.linspace(0., np.float64(size) * scale, num=size,
                            endpoint=True) + offset/2., np.float64)
            self.photon_energy.unit = unit
            self.photon_energy_long_name.value = 'Energy'


class HspyRectRoiXrayAllSpectra:
    """Representing a regular stack of X-ray spectra over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.program = NxObject(value="hyperspy")
        self.program_version = NxObject(value=hs.__version__)
        self.title = NxObject()
        self.long_name = NxObject()  # value='X-ray photon counts')
        self.counts = NxObject()
        self.xpos = NxObject()
        self.xpos_long_name = NxObject()
        self.ypos = NxObject()
        self.ypos_long_name = NxObject()
        self.photon_energy = NxObject()
        self.photon_energy_long_name = NxObject()  # value='X-ray energy')

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata['Signal']['signal_type'] == 'EDS_TEM', \
            'hspy_s3d is not a valid hyperspy generic instance !'
        assert hspy_s3d.data.ndim == 3, \
            'hspy_s3d is not a valid 3D dataset !'
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        required_axis_names = ['axis-0', 'axis-1', 'axis-2']
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + ' is unexpectedly not registered in the axes_manager !'
        required_keywords = ['_type', 'name', 'units', 'size', 'scale', 'offset']
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    'hspy_s3d axis ' + keyword + ' lacks ' + req_key + ' !'

            assert axes_dict[keyword]['_type'] == "UniformDataAxis", \
                keyword + ', this axis is not of type UniformDataAxis !'
            avail_axis_names.append(axes_dict[keyword]['name'])

        if np.all(np.sort(avail_axis_names) == np.sort(['y', 'x', 'X-ray energy'])) is True:
            return True
        else:
            return False

    def parse(self, hspy_s3d):
        """Parse a hyperspy Signal2D stack instance into an NX default plottable."""
        self.title.value = hspy_s3d.metadata['General']['title']
        # self.long_name.value = hspy_s3d.metadata['Signal']['signal_type']
        self.long_name.value = hspy_s3d.metadata['General']['title']
        self.counts.value = hspy_s3d.data  # hspy uses numpy and adapts ??
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        for keyword, value in axes_dict.items():
            offset = np.float64(axes_dict[keyword]['offset'])
            scale = np.float64(axes_dict[keyword]['scale'])
            size = np.uint32(axes_dict[keyword]['size'])
            unit = str(axes_dict[keyword]['units'])
            if axes_dict[keyword]['name'] == 'y':
                self.ypos.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.ypos.unit = unit
                self.ypos_long_name.value = 'y'
            elif axes_dict[keyword]['name'] == 'x':
                self.xpos.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.xpos.unit = unit
                self.xpos_long_name.value = 'x'
            else:  # axes_dict[keyword]['name'] == 'X-ray energy':
                self.photon_energy.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.photon_energy.unit = unit
                self.photon_energy_long_name.value = 'Energy'


class HspyRectRoiXrayMap:
    """Representing an X-ray composition map with metadata."""

    def __init__(self, hspy_clss):
        self.program = NxObject(value="hyperspy")
        self.program_version = NxObject(value=hs.__version__)
        self.title = NxObject()
        self.long_name = NxObject()
        self.counts = NxObject()
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
        self.title.value = hspy_s2d.metadata['General']['title']
        # self.long_name.value = hspy_s2d.metadata['Signal']['signal_type']
        self.long_name.value = hspy_s2d.metadata['General']['title']
        self.counts.value = hspy_s2d.data    # hspy uses numpy and adapts ??
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


class NxSpectrumSetEmXray:
    """Representing a set of X-ray spectra with metadata."""

    def __init__(self, hspy_list):
        self.stack_data = []  # the HspyRectRoiXrayAllSpectra
        self.summary_data = []  # the HspyRectRoiXraySummarySpectrum
        # ##MK::self.program = NxObject()
        # ##MK::self.program_version = NxObject(is_attr=True)
        # ##MK::self.element_names = NxObject()
        # ##MK::self.peak = {}
        self.composition_map = {}  # instances of HspyRectRoiXrayMap

        if self.is_an_implemented_case(hspy_list) is True:
            self.parse_hspy_instances(hspy_list)
            print('NxSpectrumSetEmXray successfully parsed hspy objects')
        else:
            print('NxSpectrumSetEmXray does not support these this hspy object set!')

    def is_an_implemented_case(self, hspy_list):
        """Check if signal instances in a list is a supported combination."""
        # an Xray analysis which this implementation supports should consist of
        # a rectangular ROI are currently supported, this ROI should have
        # one HAADF overview image
        # this HAADF image is read however by another, a NxImageSetAdf instance
        # of the em parser!
        # one SpectraStack cnts = f(y, x, energy)
        # one accumulated "sum" spectra cnts = f(energy)
        # an arbitrary number of single element X-ray maps cnts = f(y, x)
        cardinality_stack = 0
        cardinality_summary = 0
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.EDSTEMSpectrum) is True:
                assert hspy_clss.data.ndim in [1, 3], \
                    "Unexpectedly found unsupported-dimensional EDSTEMSpectrum!"
                if hspy_clss.data.ndim == 1:
                    cardinality_summary += 1
                elif hspy_clss.data.ndim == 3:
                    cardinality_stack += 1
                else:
                    continue
        if (cardinality_stack == 1) and (cardinality_summary == 1):
            return True
        else:
            return False

    def parse_hspy_instances(self, hspy_list):
        """Extract from hspy class instances what NOMAD OASIS understands."""
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.EDSTEMSpectrum) is True:
                ndim = hspy_clss.data.ndim
                if ndim == 1:
                    self.summary_data.append(
                        HspyRectRoiXraySummarySpectrum(hspy_clss))
                elif ndim == 3:
                    self.stack_data.append(
                        HspyRectRoiXrayAllSpectra(hspy_clss))
                else:
                    continue
            elif isinstance(hspy_clss, hs.signals.Signal2D) is True:
                ndim = hspy_clss.data.ndim
                if ndim == 2:
                    title = hspy_clss.metadata['General']['title']
                    if title != 'HAADF':
                        self.composition_map[title] = HspyRectRoiXrayMap(hspy_clss)
            else:
                continue

    def report(self, prefix: str, frame_id: int, template: dict) -> dict:
        """Enter data from the NX-specific representation into the template."""
        print('Skipping NxSpectrumSetEmXray reporting...')
        assert (0 <= len(self.stack_data)) and (len(self.stack_data) <= 1), \
            'More than one spectrum stack is currently not supported!'
        assert (0 <= len(self.summary_data)) and (len(self.summary_data) <= 1), \
            'More than one sum spectrum stack is currently not supported!'
        # for keyword, obj in self.composition_map.items():
        #     print('keyword')
        #     print(keyword)
        #     print('np.shape(obj.counts.value')
        #     print(np.shape(obj.counts.value))

        trg = prefix + "NX_SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray_" \
            + str(frame_id) + "]/"
        # template[trg + "program"] = 'hyperspy'
        # template[trg + "program/@version"] = hs.__version__
        # MISSING_DATA_MSG = "not in hspy metadata case specifically in original_metadata"
        # ##MK::!!!!!
        # ##MK::how to communicate that these data do not exist?
        # template[trg + "adf_outer_half_angle"] = np.float64(0.)
        # template[trg + "adf_outer_half_angle/@units"] = 'rad'
        # template[trg + "adf_inner_half_angle"] = np.float64(0.)
        # template[trg + "adf_inner_half_angle/@units"] = 'rad'
        prfx = trg + "DATA[stack]/"
        template[prfx + "@NX_class"] = "NXdata"
        # ##MK::usually this should be added by the dataconverter automatically
        template[prfx + "@long_name"] = self.stack_data[0].long_name.value
        template[prfx + "@signal"] = "counts"
        template[prfx + "@axes"] = ["ypos", "xpos", "photon_energy"]
        template[prfx + "@photon_energy_indices"] = 2
        template[prfx + "@xpos_indices"] = 1
        template[prfx + "@ypos_indices"] = 0
        template[prfx + "counts"] = self.stack_data[0].counts.value
        template[prfx + "photon_energy"] \
            = self.stack_data[0].photon_energy.value
        template[prfx + "photon_energy/@units"] \
            = self.stack_data[0].photon_energy.unit
        template[prfx + "xpos"] = self.stack_data[0].xpos.value
        template[prfx + "xpos/@units"] = self.stack_data[0].xpos.unit
        template[prfx + "ypos"] = self.stack_data[0].ypos.value
        template[prfx + "ypos/@units"] = self.stack_data[0].ypos.unit
        template[prfx + "title"] = self.stack_data[0].long_name.value
        # "X-ray spectra"

        prfx = trg + "DATA[summary]/"
        template[prfx + "@NX_class"] = "NXdata"
        # ##MK::usually this should be added by the dataconverter automatically
        template[prfx + "@long_name"] = self.summary_data[0].long_name.value
        template[prfx + "@signal"] = "counts"
        template[prfx + "@axes"] = ["photon_energy"]
        template[prfx + "@photon_energy_indices"] = 0
        template[prfx + "counts"] = self.summary_data[0].counts.value
        template[prfx + "photon_energy"] \
            = self.summary_data[0].photon_energy.value
        template[prfx + "photon_energy/@units"] \
            = self.summary_data[0].photon_energy.unit
        template[prfx + "title"] = self.summary_data[0].long_name.value
        # "Accumulated X-ray spectrum over ROI"

        # template[prfx + "program"] = self.program.value
        # template[prfx + "program/@version"] = self.program_version.value
        for keyword, xray_map in self.composition_map.items():
            prfx = trg + "PROCESS[indexing]/DATA[" + keyword.lower() + "]/"
            template[prfx + "@NX_class"] = "NXdata"
            # ##MK::usually this should be added by the dataconverter automatically
            template[prfx + "@long_name"] = xray_map.long_name.value
            template[prfx + "@signal"] = "counts"
            template[prfx + "@axes"] = ["ypos", "xpos"]
            template[prfx + "@xpos_indices"] = 1
            template[prfx + "@ypos_indices"] = 0
            template[prfx + "counts"] = xray_map.counts.value
            template[prfx + "xpos"] = xray_map.xpos.value
            template[prfx + "xpos/@units"] = xray_map.xpos.unit
            template[prfx + "ypos"] = xray_map.ypos.value
            template[prfx + "ypos/@units"] = xray_map.ypos.unit
            template[prfx + "title"] = xray_map.long_name.value
            # xray_map.title.value

        return template
