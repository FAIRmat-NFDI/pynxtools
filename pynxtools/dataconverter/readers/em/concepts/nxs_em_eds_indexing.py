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
"""NXem_eds indexing instance data."""

from typing import Dict, List

from pynxtools.dataconverter.readers.em.concepts.nxs_object import NxObject


NX_EM_EDS_INDEXING_HDF_PATH = ["indexing/element_names-field",
                               "indexing/IMAGE_R_SET/PROCESS-group",
                               "indexing/IMAGE_R_SET/PROCESS/peaks-field",
                               "indexing/IMAGE_R_SET/description-field",
                               "indexing/IMAGE_R_SET/iupac_line_candidates-field",
                               "indexing/IMAGE_R_SET/PROCESS/weights-field",
                               "indexing/IMAGE_R_SET/PROCESS/weights-field",
                               "indexing/IMAGE_R_SET/image_twod/axis_x-field",
                               "indexing/IMAGE_R_SET/image_twod/axis_x@long_name-attribute",
                               "indexing/IMAGE_R_SET/image_twod/axis_y-field",
                               "indexing/IMAGE_R_SET/image_twod/axis_y@long_name-attribute",
                               "indexing/IMAGE_R_SET/image_twod/intensity-field",
                               "indexing/PEAK/ION/energy-field",
                               "indexing/PEAK/ION/energy_range-field",
                               "indexing/PEAK/ION/iupac_line_names-field"]


class NxEmEdsIndexing():
    def __init__(self):
        self.tmp: Dict = {}
        self.tmp["source"] = None
        for entry in NX_EM_EDS_INDEXING_HDF_PATH:
            if entry.endswith("-field") is True:
                self.tmp[entry[0:len(entry) - len("-field")]] = NxObject(eqv_hdf="dataset")
            elif entry.endswith("-attribute") is True:
                self.tmp[entry[0:len(entry) - len("-attribute")]] = NxObject(eqv_hdf="attribute")
            else:
                self.tmp[entry[0:len(entry) - len("-group")]] = NxObject(eqv_hdf="group")
