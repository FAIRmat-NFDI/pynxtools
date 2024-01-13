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

from typing import Dict

from pynxtools.dataconverter.readers.em.concepts.nxs_object import NxObject


NX_IMAGE_REAL_SPACE_SET_HDF_PATH = ["image_oned/axis_x-field",
                                    "image_oned/axis_x@long_name-attribute",
                                    "image_oned/intensity-field",
                                    "image_threed/axis_x-field",
                                    "image_threed/axis_x@long_name-attribute",
                                    "image_threed/axis_y-field",
                                    "image_threed/axis_y@long_name-attribute",
                                    "image_threed/axis_z-field",
                                    "image_threed/axis_z@long_name-attribute",
                                    "image_threed/intensity-field",
                                    "image_twod/axis_x-field",
                                    "image_twod/axis_x@long_name-attribute",
                                    "image_twod/axis_y-field",
                                    "image_twod/axis_y@long_name-attribute",
                                    "image_twod/intensity-field",
                                    "stack_oned/axis_image_identifier-field",
                                    "stack_oned/axis_image_identifier@long_name-attribute",
                                    "stack_oned/axis_x-field",
                                    "stack_oned/axis_x@long_name-attribute",
                                    "stack_oned/intensity-field",
                                    "stack_threed/axis_image_identifier-field",
                                    "stack_threed/axis_image_identifier@long_name-attribute",
                                    "stack_threed/axis_x-field",
                                    "stack_threed/axis_x@long_name-attribute",
                                    "stack_threed/axis_y-field",
                                    "stack_threed/axis_y@long_name-attribute",
                                    "stack_threed/axis_z-field",
                                    "stack_threed/axis_z@long_name-attribute",
                                    "stack_threed/intensity-field",
                                    "stack_twod/axis_image_identifier-field",
                                    "stack_twod/axis_image_identifier@long_name-attribute",
                                    "stack_twod/axis_x-field",
                                    "stack_twod/axis_x@long_name-attribute",
                                    "stack_twod/axis_y-field",
                                    "stack_twod/axis_y@long_name-attribute",
                                    "stack_twod/intensity-field"]


class NxImageRealSpaceSet():
    def __init__(self):
        self.tmp: Dict = {}
        self.tmp["source"] = None
        for entry in NX_IMAGE_REAL_SPACE_SET_HDF_PATH:
            if entry.endswith("-field"):
                self.tmp[entry[0:len(entry) - len("-field")]] = NxObject(eqv_hdf="dataset")
            elif entry.endswith("-attribute"):
                self.tmp[entry[0:len(entry) - len("-attribute")]] = NxObject(eqv_hdf="attribute")
            else:
                self.tmp[entry[0:len(entry) - len("-group")]] = NxObject(eqv_hdf="group")
