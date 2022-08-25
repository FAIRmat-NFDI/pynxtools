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


class HspyRectRoiEelsAllSpectra:
    """Representing a regular stack of EELS spectra over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.program = NxObject(value="hyperspy")
        self.program_version = NxObject(value=hs.__version__)
        self.title = NxObject()
        self.long_name = NxObject()  # value='counts')
        self.counts = NxObject()
        self.xpos = NxObject()
        self.xpos_long_name = NxObject()
        self.ypos = NxObject()
        self.ypos_long_name = NxObject()
        self.energy_loss = NxObject()
        self.energy_loss_long_name = NxObject()  # value='Electron energy loss')
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata['Signal']['signal_type'] == 'EELS', \
            'hspy_s3d is not a valid EELS hyperspy instance !'
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

        print(np.sort(avail_axis_names))
        print(np.sort(['y', 'x', 'Energy loss']))
        axes_as_expected = np.all(np.sort(avail_axis_names)
                                  == np.sort(['y', 'x', 'Energy loss']))
        if axes_as_expected is False:
            print(__name__ + ' as expected')
            self.is_valid = False

    def parse(self, hspy_s3d):
        """Parse a hyperspy Signal3D stack instance into an NX default plottable."""
        if self.is_valid is False:
            pass
        print('\t' + __name__)
        self.title.value = hspy_s3d.metadata['General']['title']
        self.long_name.value = hspy_s3d.metadata['Signal']['signal_type']
        # self.long_name.value = hspy_s3d.metadata['General']['title']
        self.title.value = hspy_s3d.metadata['Signal']['signal_type']
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
            else:  # axes_dict[keyword]['name'] == 'Energy loss':
                self.energy_loss.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.energy_loss.unit = unit
                self.energy_loss_long_name.value = 'Energy loss'
                print('np.shape(self.energy_loss.value)')
                print(np.shape(self.energy_loss.value))


class HspyRectRoiEelsSummarySpectrum:
    """Represent/compute an accumulated EELS spectrum from hspy EELSSpectrum."""

    def __init__(self, hspy_clss):
        self.program = NxObject(value="hyperspy")
        self.program_version = NxObject(value=hs.__version__)
        self.title = NxObject()
        self.long_name = NxObject()  # value='Counts')
        self.counts = NxObject()
        self.energy_loss = NxObject()
        self.energy_loss_long_name = NxObject()  # value='Energy loss')
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata['Signal']['signal_type'] == 'EELS', \
            'hspy_s3d is not a valid EELS hyperspy instance !'
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

        print(np.sort(avail_axis_names))
        print(np.sort(['y', 'x', 'Energy loss']))
        axes_as_expected = np.all(np.sort(avail_axis_names)
                                  == np.sort(['y', 'x', 'Energy loss']))
        if axes_as_expected is False:
            print(__name__ + ' as expected')
            self.is_valid = False

    def parse(self, hspy_s3d):
        """Summarize the spectra stack into a ROI summary spectrum."""
        if self.is_valid is False:
            pass
        print('\t' + __name__)
        self.long_name.value = hspy_s3d.metadata['Signal']['signal_type']
        self.title.value = hspy_s3d.metadata['Signal']['signal_type']
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        # ##MK::assume for now that hspy arranges the axes such that the
        # Energy loss comes last, then we can iterate over
        # ##MK::at least in the example of DM3 files I found that the
        # EELSSpectrum.data array is float32 this should not be done
        # inspecting np.unique(hspy_s1d.data[y,x, :]) reveals there is a
        # cast from what was likely an uint(16?) to float32
        # ##MK::for now cast them back to uint32 and accumulate
        # instead it should be uint, so we have to be careful with not
        shape = np.shape(hspy_s3d.data)
        self.counts.value = np.zeros([shape[2]], np.uint32)
        for y in np.arange(0, shape[0]):
            for x in np.arange(1, shape[1]):
                self.counts.value \
                    += np.asarray(hspy_s3d.data[y, x, :], np.uint32)
        # ##MK::it seems that hspy is adaptive, uses numpy under the hood
        # though, so the .data instance is already a proper numpy dtype
        # therefore, an explicit call like this
        # np.asarray(hspy_s1d.data, np.uint32) is not necessary
        # ##MK::on the contrary the above-mentioned observed cast to float32
        # means it might not be adaptive enough ??
        for keyword, value in axes_dict.items():
            offset = np.float64(axes_dict[keyword]['offset'])
            scale = np.float64(axes_dict[keyword]['scale'])
            size = np.uint32(axes_dict[keyword]['size'])
            unit = str(axes_dict[keyword]['units'])
            if axes_dict[keyword]['name'] == 'Energy loss':
                self.energy_loss.value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset/2., np.float64)
                self.energy_loss.unit = unit
                self.energy_loss_long_name.value = 'Energy loss'
                print('np.shape(self.energy_loss.value)')
                print(np.shape(self.energy_loss.value))


class NxSpectrumSetEmEels:
    """Representing a set of EELS spectra with metadata."""

    def __init__(self, hspy_list):
        self.stack_data = []  # the HspyRectRoiEelsAllSpectra
        self.summary_data = []  # the HspyRectRoiEelsSummarySpectrum
        # ##MK::self.program = NxObject()
        # ##MK::self.program_version = NxObject(is_attr=True)
        # ##MK::self.element_names = NxObject()
        # ##MK::self.peak = {}
        self.is_valid = True

        self.is_an_implemented_case(hspy_list)
        self.parse_hspy_instances(hspy_list)

    def is_an_implemented_case(self, hspy_list):
        """Check if signal instances in a list is a supported combination."""
        # an EELS measurement which this implementation supports consist of
        # a rectangular ROI are currently supported, this ROI should have
        # one SpectrumStack cnts = f(y, x, energy loss)
        cardinality_stack = 0
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.EELSSpectrum) is True:
                assert hspy_clss.data.ndim in [3], \
                    "Unexpectedly found unsupported-dimensional EELSSpectrum!"
                if hspy_clss.data.ndim == 3:
                    cardinality_stack += 1
        if cardinality_stack != 1:
            self.is_valid = False

    def parse_hspy_instances(self, hspy_list):
        """Extract from hspy class instances what NOMAD OASIS understands."""
        if self.is_valid is False:
            pass
        print('\t' + __name__)
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.EELSSpectrum) is True:
                assert hspy_clss.data.ndim in [3], \
                    "Unexpectedly found unsupported-dimensional EELSSpectrum!"
                if hspy_clss.data.ndim == 3:
                    print('--->>>>>>>>>>>>>>')
                    self.stack_data.append(
                        HspyRectRoiEelsAllSpectra(hspy_clss))
                    self.summary_data.append(
                        HspyRectRoiEelsSummarySpectrum(hspy_clss))

    def report(self, prefix: str, frame_id: int, template: dict) -> dict:
        """Enter data from the NX-specific representation into the template."""
        if self.is_valid is False:
            print('\t' + __name__ + ' reporting nothing!')
            return template
        print('\t' + __name__ + ' reporting...')
        assert (0 <= len(self.stack_data)) and (len(self.stack_data) <= 1), \
            'More than one spectrum stack is currently not supported!'
        assert (0 <= len(self.summary_data)) and (len(self.summary_data) <= 1), \
            'More than one sum spectrum stack is currently not supported!'

        trg = prefix + "NX_SPECTRUM_SET_EM_EELS[spectrum_set_em_eels_" \
            + str(frame_id) + "]/"
        # template[trg + "program"] = 'hyperspy'
        # template[trg + "program/@version"] = hs.__version__
        prfx = trg + "DATA[stack]/"
        template[prfx + "@NX_class"] = "NXdata"
        # ##MK::usually this should be added by the dataconverter automatically
        template[prfx + "@long_name"] = self.stack_data[0].long_name.value
        template[prfx + "@signal"] = "counts"
        template[prfx + "@axes"] = ["ypos", "xpos", "energy_loss"]
        template[prfx + "@energy_loss_indices"] = 2
        template[prfx + "@xpos_indices"] = 1
        template[prfx + "@ypos_indices"] = 0
        template[prfx + "counts"] = self.stack_data[0].counts.value
        template[prfx + "energy_loss"] \
            = self.stack_data[0].energy_loss.value
        template[prfx + "energy_loss/@units"] \
            = self.stack_data[0].energy_loss.unit
        template[prfx + "xpos"] = self.stack_data[0].xpos.value
        template[prfx + "xpos/@units"] = self.stack_data[0].xpos.unit
        template[prfx + "ypos"] = self.stack_data[0].ypos.value
        template[prfx + "ypos/@units"] = self.stack_data[0].ypos.unit
        template[prfx + "title"] = self.stack_data[0].long_name.value

        prfx = trg + "DATA[summary]/"
        template[prfx + "@NX_class"] = "NXdata"
        # ##MK::usually this should be added by the dataconverter automatically
        template[prfx + "@long_name"] = self.summary_data[0].long_name.value
        template[prfx + "@signal"] = "counts"
        template[prfx + "@axes"] = ["energy_loss"]
        template[prfx + "@energy_loss_indices"] = 0
        template[prfx + "counts"] = self.summary_data[0].counts.value
        template[prfx + "energy_loss"] \
            = self.summary_data[0].energy_loss.value
        template[prfx + "energy_loss/@units"] \
            = self.summary_data[0].energy_loss.unit
        template[prfx + "title"] = self.summary_data[0].long_name.value

        return template
