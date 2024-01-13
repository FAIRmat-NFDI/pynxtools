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
"""NXem spectrum set (element of a labelled property graph) to store instance data."""

from typing import Dict, List

from pynxtools.dataconverter.readers.em.concepts.nxs_object import NxObject


NX_SPECTRUM_SET_HDF_PATH: List = ["collection-group",
                                  "collection/axis_energy-field",
                                  "collection/axis_energy@long_name-attribute",
                                  "collection/axis_scan_point_id-field",
                                  "collection/axis_scan_point_id@long_name-attribute",
                                  "collection/intensity-field",
                                  "collection/intensity@long_name-attribute",
                                  "PROCESS-group",
                                  "PROCESS/detector_identifier-field",
                                  "PROCESS/mode-field",
                                  "PROCESS/PROGRAM-group",
                                  "PROCESS/source-group",
                                  "spectrum_zerod/axis_energy-field",
                                  "spectrum_zerod/axis_energy@long_name-attribute",
                                  "spectrum_zerod/intensity-field",
                                  "spectrum_zerod/intensity@long_name-attribute",
                                  "spectrum_oned/axis_energy-field",
                                  "spectrum_oned/axis_energy@long_name-attribute",
                                  "spectrum_oned/axis_x-field",
                                  "spectrum_oned/axis_x@long_name-attribute",
                                  "spectrum_oned/intensity-field",
                                  "spectrum_oned/intensity@long_name-attribute",
                                  "spectrum_threed/axis_energy-field",
                                  "spectrum_threed/axis_energy@long_name-attribute",
                                  "spectrum_threed/axis_x-field",
                                  "spectrum_threed/axis_x@long_name-attribute",
                                  "spectrum_threed/axis_y-field",
                                  "spectrum_threed/axis_y@long_name-attribute",
                                  "spectrum_threed/axis_z-field",
                                  "spectrum_threed/axis_z@long_name-attribute",
                                  "spectrum_threed/intensity-field",
                                  "spectrum_threed/intensity@long_name-attribute",
                                  "spectrum_twod/axis_energy-field",
                                  "spectrum_twod/axis_energy@long_name-attribute",
                                  "spectrum_twod/axis_x-field",
                                  "spectrum_twod/axis_x@long_name-attribute",
                                  "spectrum_twod/axis_y-field",
                                  "spectrum_twod/axis_y@long_name-attribute",
                                  "spectrum_twod/intensity-field",
                                  "spectrum_twod/intensity@long_name-attribute"]


class NxSpectrumSet():
    def __init__(self):
        self.tmp: Dict = {}
        self.tmp["source"] = None
        for entry in NX_SPECTRUM_SET_HDF_PATH:
            if entry.endswith("-field") is True:
                self.tmp[entry[0:len(entry) - len("-field")]] = NxObject(eqv_hdf="dataset")
            elif entry.endswith("-attribute") is True:
                self.tmp[entry[0:len(entry) - len("-attribute")]] = NxObject(eqv_hdf="attribute")
            else:
                self.tmp[entry[0:len(entry) - len("-group")]] = NxObject(eqv_hdf="group")
