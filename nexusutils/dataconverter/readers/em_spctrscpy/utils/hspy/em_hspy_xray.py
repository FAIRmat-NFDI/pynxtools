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


class HspyRectRoiXrayAllSpectra:
    """Representing a regular stack of X-ray spectra over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject(value="hyperspy")
        self.meta["program_version"] = NxObject(value=hs.__version__)
        self.meta["title"] = NxObject()
        self.meta["long_name"] = NxObject()
        self.meta["counts"] = NxObject()
        self.meta["xpos"] = NxObject()
        self.meta["xpos_long_name"] = NxObject()
        self.meta["ypos"] = NxObject()
        self.meta["ypos_long_name"] = NxObject()
        self.meta["photon_energy"] = NxObject()
        self.meta["photon_energy_long_name"] = NxObject()
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s3d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s3d.metadata["Signal"]["signal_type"] == "EDS_TEM", \
            "hspy_s3d is not a valid hyperspy generic instance !"
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

        axes_as_expected_emd = np.all(
            np.sort(avail_axis_names) == np.sort(["y", "x", "X-ray energy"]))
        axes_as_expected_bcf = np.all(
            np.sort(avail_axis_names) == np.sort(["height", "width", "Energy"]))
        if (axes_as_expected_emd is False) and (axes_as_expected_bcf is True):
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s3d):
        """Parse a hyperspy Signal2D stack instance into an NX default plottable."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        self.meta["title"].value = hspy_s3d.metadata["General"]["title"]
        # self.long_name.value = hspy_s3d.metadata["Signal"]["signal_type"]
        self.meta["long_name"].value = hspy_s3d.metadata["General"]["title"]
        self.meta["counts"].value = hspy_s3d.data  # hspy uses numpy and adapts ??
        axes_dict = hspy_s3d.axes_manager.as_dictionary()
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])

            y_axis = (axes_dict[keyword]["name"] == "y") \
                or (axes_dict[keyword]["name"] == "height")
            x_axis = (axes_dict[keyword]["name"] == "x") \
                or (axes_dict[keyword]["name"] == "width")
            e_axis = (axes_dict[keyword]["name"] == "X-ray energy") \
                or (axes_dict[keyword]["name"] == "Energy")
            if y_axis is True:
                self.meta["ypos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["ypos"].unit = unit
                self.meta["ypos_long_name"].value = "y"  # ##MK::name y always!
            if x_axis is True:
                self.meta["xpos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["xpos"].unit = unit
                self.meta["xpos_long_name"].value = "x"  # ##MK::name x always!
            if e_axis is True:
                self.meta["photon_energy"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["photon_energy"].unit = unit
                self.meta["photon_energy_long_name"].value = "Energy"
                # ##MK::name Energy always!


class HspyRectRoiXraySummarySpectrum:
    """Representing the accumulated X-ray spectrum over a rectangular ROI."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject(value="hyperspy")
        self.meta["program_version"] = NxObject(value=hs.__version__)
        self.meta["title"] = NxObject()
        self.meta["long_name"] = NxObject()
        self.meta["counts"] = NxObject()
        self.meta["photon_energy"] = NxObject()
        self.meta["photon_energy_long_name"] = NxObject()
        self.is_valid = True

        self.is_supported(hspy_clss)
        self.parse(hspy_clss)

    def is_supported(self, hspy_s1d):
        """Check if the input has supported axes_manager and key metadata."""
        assert hspy_s1d.metadata["Signal"]["signal_type"] == "EDS_TEM", \
            "hspy_s3d is not a valid hyperspy generic instance !"
        assert hspy_s1d.data.ndim == 1, \
            "hspy_s3d is not a valid 1D dataset !"
        axes_dict = hspy_s1d.axes_manager.as_dictionary()
        required_axis_names = ["axis-0"]
        for req_key in required_axis_names:
            assert req_key in axes_dict.keys(), \
                req_key + " is unexpectedly not registered in the axes_manager !"
        required_keywords = ["_type", "name", "units", "size", "scale", "offset"]
        avail_axis_names = []
        for keyword in axes_dict.keys():
            for req_key in required_keywords:  # check if all required keys exist
                assert req_key in axes_dict[keyword].keys(), \
                    "hspy_s1d axis " + keyword + " lacks " + req_key + " !"

            assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                keyword + ", this axis is not of type UniformDataAxis !"
            avail_axis_names.append(axes_dict[keyword]["name"])

        axes_as_expected = np.all(
            np.sort(avail_axis_names) == np.sort(["Energy"]))
        if axes_as_expected is False:
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s1d):
        """Parse a hyperspy Signal1D stack instance into an NX default plottable."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        self.meta["title"].value = hspy_s1d.metadata["General"]["title"]
        # self.meta["long_name"].value = hspy_s1d.metadata["Signal"]["signal_type"]
        self.meta["long_name"].value = hspy_s1d.metadata["General"]["title"]
        self.meta["counts"].value = hspy_s1d.data
        # ##MK::it seems that hspy is adaptive, uses numpy under the hood
        # though, so the .data instance is already a proper numpy dtype
        # therefore, an explicit call like this
        # np.asarray(hspy_s1d.data, np.uint32) is not necessary
        axes_dict = hspy_s1d.axes_manager.as_dictionary()
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])
            # if axes_dict[keyword]["name"] == "Energy":
            self.meta["photon_energy"].value = np.asarray(
                np.linspace(0., np.float64(size) * scale, num=size,
                            endpoint=True) + offset / 2., np.float64)
            self.meta["photon_energy"].unit = unit
            self.meta["photon_energy_long_name"].value = "Energy"


class HspyRectRoiXrayMap:
    """Representing an X-ray composition map with metadata."""

    def __init__(self, hspy_clss):
        self.meta: Dict[str, NxObject] = {}
        self.meta["program"] = NxObject(value="hyperspy")
        self.meta["program_version"] = NxObject(value=hs.__version__)
        self.meta["title"] = NxObject()
        self.meta["long_name"] = NxObject()
        self.meta["counts"] = NxObject()
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

        axes_as_expected = np.all(
            np.sort(avail_axis_names) == np.sort(["y", "x"]))
        if axes_as_expected is False:
            print(__name__ + " as expected")
            self.is_valid = False

    def parse(self, hspy_s2d):
        """Parse a hyperspy Signal2D instance into an NX default plottable."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
        self.meta["title"].value = hspy_s2d.metadata["General"]["title"]
        # self.meta["long_name"].value = hspy_s2d.metadata["Signal"]["signal_type"]
        self.meta["long_name"].value = hspy_s2d.metadata["General"]["title"]
        self.meta["counts"].value = hspy_s2d.data    # hspy uses numpy and adapts ??
        axes_dict = hspy_s2d.axes_manager.as_dictionary()
        for keyword in axes_dict.keys():
            offset = np.float64(axes_dict[keyword]["offset"])
            scale = np.float64(axes_dict[keyword]["scale"])
            size = np.uint32(axes_dict[keyword]["size"])
            unit = str(axes_dict[keyword]["units"])
            if axes_dict[keyword]["name"] == "y":
                assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                    keyword + ", this x axis is not of type UniformDataAxis !"
                self.meta["ypos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["ypos"].unit = unit
                self.meta["ypos_long_name"].value = "y"
            else:  # axes_dict[keyword]["name"] == "x":
                assert axes_dict[keyword]["_type"] == "UniformDataAxis", \
                    keyword + ", this y axis is not of type UniformDataAxis !"
                self.meta["xpos"].value = np.asarray(
                    np.linspace(0., np.float64(size) * scale, num=size,
                                endpoint=True) + offset / 2., np.float64)
                self.meta["xpos"].unit = unit
                self.meta["xpos_long_name"].value = "x"


class NxSpectrumSetEmXray:
    """Representing a set of X-ray spectra with metadata."""

    def __init__(self, hspy_list):
        self.stack_data = []  # the HspyRectRoiXrayAllSpectra
        self.summary_data = []  # the HspyRectRoiXraySummarySpectrum
        self.composition_map = {}  # instances of HspyRectRoiXrayMap
        self.is_valid = True

        self.is_an_implemented_case(hspy_list)
        self.parse_hspy_instances(hspy_list)

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
        if cardinality_stack != 1:  # stack needed or (cardinality_summary == 1)
            self.is_valid = False

    def parse_hspy_instances(self, hspy_list):
        """Extract from hspy class instances what NOMAD OASIS understands."""
        if self.is_valid is False:
            pass
        print("\t" + __name__)
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
                    title = hspy_clss.metadata["General"]["title"]
                    if title != "HAADF":
                        self.composition_map[title] \
                            = HspyRectRoiXrayMap(hspy_clss)
            else:
                continue

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
        # for keyword, obj in self.composition_map.items():
        #     print(keyword)
        #     print("np.shape(obj.counts.value")
        #     print(np.shape(obj.counts.value))

        trg = prefix + "SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray" + str(frame_id) + "]/"
        # template[trg + "program"] = "hyperspy"
        # template[trg + "program/@version"] = hs.__version__
        # MISSING_DATA_MSG = "not in hspy metadata case specifically in original_metadata"
        # ##MK::!!!!!
        # ##MK::how to communicate that these data do not exist?
        # template[trg + "adf_outer_half_angle"] = np.float64(0.)
        # template[trg + "adf_outer_half_angle/@units"] = "rad"
        # template[trg + "adf_inner_half_angle"] = np.float64(0.)
        # template[trg + "adf_inner_half_angle/@units"] = "rad"
        if len(self.stack_data) == 1:
            prfx = trg + "stack/"
            template[prfx + "title"] = "Xray spectra stack"
            # template[prfx + "@long_name"] \
            #     = self.stack_data[0].meta["long_name"].value
            template[prfx + "@signal"] = "data_counts"
            template[prfx + "@axes"] \
                = ["axis_y", "axis_x", "axis_photon_energy"]
            template[prfx + "@AXISNAME_indices[axis_photon_energy_indices]"] = 2
            template[prfx + "@AXISNAME_indices[axis_x_indices]"] = 1
            template[prfx + "@AXISNAME_indices[axis_y_indices]"] = 0
            template[prfx + "DATA[data_counts]"] \
                = {"compress": self.stack_data[0].meta["counts"].value,
                   "strength": 1}
            template[prfx + "DATA[data_counts]/@units"] = ""
            template[prfx + "DATA[data_counts]/@long_name"] = "Photon counts (1)"
            template[prfx + "AXISNAME[axis_photon_energy]"] \
                = {"compress": self.stack_data[0].meta["photon_energy"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_photon_energy]/@units"] \
                = self.stack_data[0].meta["photon_energy"].unit
            template[prfx + "AXISNAME[axis_photon_energy]/@long_name"] \
                = "Photon energy (" + self.stack_data[0].meta["photon_energy"].unit + ")"
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
            template[prfx + "title"] = "Accumulated X-ray spectrum"
            # template[prfx + "@long_name"] \
            #     = self.summary_data[0].meta["long_name"].value
            template[prfx + "@signal"] = "data_counts"
            template[prfx + "@axes"] = ["axis_photon_energy"]
            template[prfx + "@AXISNAME_indices[axis_photon_energy_indices]"] = 0
            template[prfx + "DATA[data_counts]"] \
                = {"compress": self.summary_data[0].meta["counts"].value,
                   "strength": 1}
            template[prfx + "DATA[data_counts]/@units"] = ""
            template[prfx + "DATA[data_counts]/@long_name"] = "Photon counts (1)"
            template[prfx + "AXISNAME[axis_photon_energy]"] \
                = {"compress": self.summary_data[0].meta["photon_energy"].value,
                   "strength": 1}
            template[prfx + "AXISNAME[axis_photon_energy]/@units"] \
                = self.summary_data[0].meta["photon_energy"].unit
            template[prfx + "AXISNAME[axis_photon_energy]/@long_name"] \
                = "Photon energy (" \
                  + self.summary_data[0].meta["photon_energy"].unit + ")"

        # template[prfx + "program"] = self.program.value
        # template[prfx + "program/@version"] = self.program_version.value

        return template

        # skip the composition maps for the search sprint
        # for keyword, xray_map in self.composition_map.items():
        #     prfx = trg + "PROCESS[indexing]/PROCESS[" + keyword.lower() + "]/summary/"
        #     template[prfx + "title"] = "X-ray mapping for " + keyword
        #     # = xray_map.meta["long_name"].value
        #     # template[prfx + "@long_name"] = xray_map.meta["long_name"].value
        #     template[prfx + "@signal"] = "data_counts"
        #     template[prfx + "@axes"] = ["axis_y", "axis_x"]
        #     template[prfx + "@AXISNAME[axis_x_indices]"] = 1
        #     template[prfx + "@AXISNAME[axis_y_indices]"] = 0
        #     template[prfx + "DATA[data_counts]"] \
        #         = {"compress": xray_map.meta["counts"].value, "strength": 1}
        #     template[prfx + "DATA[data_counts]/@units"] = ""
        #     template[prfx + "DATA[data_counts]/@long_name"] = "Counts (1)"
        #     template[prfx + "AXISNAME[axis_x]"] \
        #         = {"compress": xray_map.meta["xpos"].value, "strength": 1}
        #     template[prfx + "AXISNAME[axis_x]/@units"] = xray_map.meta["xpos"].unit
        #     template[prfx + "AXISNAME[axis_x]/@long_name"] \
        #         = "x (" + xray_map.meta["xpos"].unit + ")"
        #     template[prfx + "AXISNAME[axis_y]"] \
        #         = {"compress": xray_map.meta["ypos"].value, "strength": 1}
        #     template[prfx + "AXISNAME[axis_y]/@units"] = xray_map.meta["ypos"].unit
        #     template[prfx + "AXISNAME[axis_y]/@long_name"] \
        #         = "y (" + xray_map.meta["ypos"].unit + ")"
