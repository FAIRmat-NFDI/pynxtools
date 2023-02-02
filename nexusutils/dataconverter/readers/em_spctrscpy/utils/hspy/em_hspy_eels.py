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


class HspyRectRoiEelsAllSpectra:
    """Representing a regular stack of EELS spectra over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject(value="hyperspy")
        self.meta["program_version"] = NxObject(value=hs.__version__)
        self.meta["title"] = NxObject()
        self.meta["long_name"] = NxObject()  # value="counts")
        self.meta["counts"] = NxObject()
        self.meta["xpos"] = NxObject()
        self.meta["xpos_long_name"] = NxObject()
        self.meta["ypos"] = NxObject()
        self.meta["ypos_long_name"] = NxObject()
        self.meta["energy_loss"] = NxObject()
        self.meta["energy_loss_long_name"] = NxObject()
        # value="Electron energy loss")
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata["Signal"]["signal_type"] == "EELS", \
            "hspy_s3d is not a valid EELS hyperspy instance !"
        assert hspy_s3d.data.ndim == 3, \
            "hspy_s3d is not a valid 3D dataset !"
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        required_axis_names = ["axis-0", "axis-1", "axis-2"]
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + " is unexpectedly not registered in the axes_manager !"
        required_keywords = ["_type", "name", "units", "size", "scale", "offset"]
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    "hspy_s3d axis " + keyword + " lacks " + req_key + " !"

            assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                keyword + ", this axis is not of type UniformDataAxis !"
            avail_axis_names.append(axes_dict[keyword]["name"])

        print(np.sort(avail_axis_names))
        print(np.sort(["y", "x", "Energy loss"]))
        axes_as_expected = np.all(
            np.sort(avail_axis_names) == np.sort(["y", "x", "Energy loss"]))
        if axes_as_expected is False:
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s3d):
        """Parse a hyperspy Signal3D stack instance into an NX default plottable."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        # self.meta["title"].value = hspy_s3d.metadata["General"]["title"]
        self.meta["long_name"].value = hspy_s3d.metadata["Signal"]["signal_type"]
        # self.meta["long_name"].value = hspy_s3d.metadata["General"]["title"]
        self.meta["title"].value = hspy_s3d.metadata["Signal"]["signal_type"]
        self.meta["counts"].value = hspy_s3d.data  # hspy uses numpy and adapts ??
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])
            if axes_dict[keyword]["name"] == "y":
                self.meta["ypos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["ypos"].unit = unit
                self.meta["ypos_long_name"].value = "y"
            elif axes_dict[keyword]["name"] == "x":
                self.meta["xpos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["xpos"].unit = unit
                self.meta["xpos_long_name"].value = "x"
            else:  # axes_dict[keyword]["name"] == "Energy loss":
                self.meta["energy_loss"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["energy_loss"].unit = unit
                self.meta["energy_loss_long_name"].value = "Energy loss"


class HspyRectRoiEelsSummarySpectrum:
    """Represent/compute an accumulated EELS spectrum from hspy EELSSpectrum."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject(value="hyperspy")
        self.meta["program_version"] = NxObject(value=hs.__version__)
        self.meta["title"] = NxObject()
        self.meta["long_name"] = NxObject()  # value="Counts")
        self.meta["counts"] = NxObject()
        self.meta["energy_loss"] = NxObject()
        self.meta["energy_loss_long_name"] = NxObject()  # value="Energy loss")
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata["Signal"]["signal_type"] == "EELS", \
            "hspy_s3d is not a valid EELS hyperspy instance !"
        assert hspy_s3d.data.ndim == 3, \
            "hspy_s3d is not a valid 3D dataset !"
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        required_axis_names = ["axis-0", "axis-1", "axis-2"]
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + " is unexpectedly not registered in the axes_manager !"
        required_keywords = ["_type", "name", "units", "size", "scale", "offset"]
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    "hspy_s3d axis " + keyword + " lacks " + req_key + " !"

            assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                keyword + ", this axis is not of type UniformDataAxis !"
            avail_axis_names.append(axes_dict[keyword]["name"])

        print(np.sort(avail_axis_names))
        print(np.sort(["y", "x", "Energy loss"]))
        axes_as_expected = np.all(
            np.sort(avail_axis_names) == np.sort(["y", "x", "Energy loss"]))
        if axes_as_expected is False:
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s3d):
        """Summarize the spectra stack into a ROI summary spectrum."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        self.meta["long_name"].value = hspy_s3d.metadata["Signal"]["signal_type"]
        self.meta["title"].value = hspy_s3d.metadata["Signal"]["signal_type"]
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
        self.meta["counts"].value = np.zeros([shape[2]], np.uint32)
        for y_pixel in np.arange(0, shape[0]):
            for x_pixel in np.arange(1, shape[1]):
                self.meta["counts"].value \
                    += np.asarray(hspy_s3d.data[y_pixel, x_pixel, :], np.uint32)
        # seems that hspy is adaptive, uses numpy under the hood
        # though, so a hspy signal's .data member is already a proper numpy dtype
        # therefore, an explicit call like this
        # np.asarray(hspy_s1d.data, np.uint32) is not necessary
        # ##MK::on the contrary the above-mentioned observed cast to float32
        # means it might not be adaptive enough ??
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])
            if axes_dict[keyword]["name"] == "Energy loss":
                self.meta["energy_loss"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["energy_loss"].unit = unit
                self.meta["energy_loss_long_name"].value = "Energy loss"


class NxSpectrumSetEmEels:
    """Representing a set of EELS spectra with metadata."""

    def __init__(self, hspy_list):
        self.stack_data = []  # the HspyRectRoiEelsAllSpectra
        self.summary_data = []  # the HspyRectRoiEelsSummarySpectrum
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
        print("\t" + __name__)
        for hspy_clss in hspy_list:
            if isinstance(hspy_clss, hs.signals.EELSSpectrum) is True:
                assert hspy_clss.data.ndim in [3], \
                    "Unexpectedly found unsupported-dimensional EELSSpectrum!"
                if hspy_clss.data.ndim == 3:
                    self.stack_data.append(
                        HspyRectRoiEelsAllSpectra(hspy_clss))
                    self.summary_data.append(
                        HspyRectRoiEelsSummarySpectrum(hspy_clss))

    def report(self, prefix: str, frame_id: int, template: dict) -> dict:
        """Enter data from the NX-specific representation into the template."""
        if self.is_valid is False:
            print("\t" + __name__ + " reporting nothing!")
            return template
        print("\t" + __name__ + " reporting...")
        assert (len(self.stack_data) >= 0) and (len(self.stack_data) <= 1), \
            "More than one spectrum stack is currently not supported!"
        assert (len(self.summary_data) >= 0) and (len(self.summary_data) <= 1), \
            "More than one sum spectrum stack is currently not supported!"

        trg = prefix + "SPECTRUM_SET_EM_EELS[spectrum_set_em_eels" + str(frame_id) + "]/"
        if len(self.stack_data) == 1:
            # template[trg + "program"] = "hyperspy"
            # template[trg + "program/@version"] = hs.__version__
            prfx = trg + "stack/"
            template[prfx + "title"] = "EELS spectra stack"
            # template[prfx + "@long_name"] \
            #     = self.stack_data[0].meta["long_name"].value
            template[prfx + "@signal"] = "data_counts"
            template[prfx + "@axes"] = ["axis_y", "axis_x", "axis_energy_loss"]
            template[prfx + "@AXISNAME[axis_energy_loss_indices]"] = 2
            template[prfx + "@AXISNAME[axis_x_indices]"] = 1
            template[prfx + "@AXISNAME[axis_y_indices]"] = 0
            template[prfx + "DATA[data_counts]"] \
                = {"compress": self.stack_data[0].meta["counts"].value,
                   "strength": 1}
            template[prfx + "DATA[data_counts]/@units"] = ""
            template[prfx + "DATA[data_counts]/@long_name"] = "Signal (a.u.)"
            template[prfx + "AXISNAME[axis_energy_loss]"] \
                = {"compress": self.stack_data[0].meta["energy_loss"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_energy_loss]/@units"] \
                = self.stack_data[0].meta["energy_loss"].unit
            template[prfx + "AXISNAME[axis_energy_loss]/@long_name"] \
                = "Electron energy loss (" \
                  + self.stack_data[0].meta["energy_loss"].unit + ")"
            template[prfx + "AXISNAME[axis_x]"] \
                = {"compress": self.stack_data[0].meta["xpos"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_x]/@units"] \
                = self.stack_data[0].meta["xpos"].unit
            template[prfx + "AXISNAME[axis_x]/@long_name"] \
                = "x (" + self.stack_data[0].meta["xpos"].unit + ")"
            template[prfx + "AXISNAME[axis_y]"] \
                = {"compress": self.stack_data[0].meta["ypos"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_y]/@units"] \
                = self.stack_data[0].meta["ypos"].unit
            template[prfx + "AXISNAME[axis_y]/@long_name"] \
                = "y (" + self.stack_data[0].meta["ypos"].unit + ")"

        if len(self.summary_data) == 1:
            prfx = trg + "summary/"
            template[prfx + "title"] = "Accumulated EELS spectrum"
            # template[prfx + "@long_name"] \
            #     = self.summary_data[0].meta["long_name"].value
            template[prfx + "@signal"] = "data_counts"
            template[prfx + "@axes"] = ["axis_energy_loss"]
            template[prfx + "@AXISNAME[axis_energy_loss_indices]"] = 0
            template[prfx + "DATA[data_counts]"] \
                = {"compress": self.summary_data[0].meta["counts"].value,
                   "strength": 1}
            template[prfx + "DATA[data_counts]/@units"] = ""
            template[prfx + "DATA[data_counts]/@long_name"] = "Signal (a.u.)"
            template[prfx + "AXISNAME[axis_energy_loss]"] \
                = {"compress": self.summary_data[0].meta["energy_loss"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_energy_loss]/@units"] \
                = self.summary_data[0].meta["energy_loss"].unit
            template[prfx + "AXISNAME[axis_energy_loss]/@long_name"] \
                = "Electron energy loss (" \
                  + self.summary_data[0].meta["energy_loss"].unit + ")"

        return template
