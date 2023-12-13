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

# pylint: disable=no-member,too-few-public-methods


from typing import Dict

from pynxtools.dataconverter.readers.em.concepts.nxs_object import NxObject


NX_EM_SPECTRUM_SET_HDF_PATH = [
   "PROCESS-group",
   "PROCESS/detector_identifier-field",
   "PROCESS/source-group",
   "PROCESS/source/algorithm-field",
   "PROCESS/source/checksum-field",
   "PROCESS/source/path-field",
   "PROCESS/source/type-field",
   "stack-group",
   "stack/axis_energy-field",
   "stack/axis_energy@long_name-attribute",
   "stack/axis_x-field",
   "stack/axis_x@long_name-attribute",
   "stack/axis_y-field",
   "stack/axis_y@long_name-attribute",
   "stack/intensity-field",
   "stack/intensity@long_name-attribute",
   "stack/title-field",
   "stack@axes-attribute",
   "stack@AXISNAME_indices-attribute",
   "stack@long_name-attribute",
   "stack@signal-attribute",
   "summary-group",
   "summary/axis_energy-field",
   "summary/axis_energy@long_name-attribute",
   "summary/title-field",
   "summary@axes-attribute",
   "summary@AXISNAME_indices-attribute",
   "summary@long_name-attribute",
   "summary@signal-attribute"]
# this one needs an update !


class NxEmSpectrumSet():
    def __init__(self):
        self.tmp: Dict = {}
        for entry in NX_EM_SPECTRUM_SET_HDF_PATH:
            if entry.endswith("-field") is True:
                self.tmp[entry[0:len(entry)-len("-field")]] = NxObject(eqv_hdf="dset")
            elif entry.endswith("-attribute") is True:
                self.tmp[entry[0:len(entry)-len("-attribute")]] = NxObject(eqv_hdf="attr")
            else:
                self.tmp[entry[0:len(entry)-len("-group")]] = NxObject(eqv_hdf="grp")
