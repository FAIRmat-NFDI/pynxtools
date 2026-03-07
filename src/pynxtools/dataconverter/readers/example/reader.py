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

"""An example reader implementation for the DataConverter."""

import json
import os
from typing import Any

import numpy as np

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader


class ExampleReader(MultiFormatReader):
    """An example reader implementation for the DataConverter."""

    supported_nxdls = ["NXtest"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: dict = {}
        self.extensions = {
            ".json": self.handle_json_file,
        }

    def handle_json_file(self, file_path: str) -> dict[str, Any]:
        """Reads the JSON test data into self.data."""
        with open(file_path, encoding="utf-8") as f:
            self.data = json.loads(f.read())
        return {}

    def setup_template(self) -> dict[str, Any]:
        """Fills the template from self.data using the NXDL template structure."""
        result: dict[str, Any] = {}

        # Generic fill: for every key in the NXDL template, look up data by field name.
        if self.nxdl_template is not None:
            for k in self.nxdl_template.keys():
                if k.startswith(
                    (
                        "/ENTRY[entry]/required_group",
                        "/ENTRY[entry]/specified_group",
                        "/ENTRY[entry]/any_groupGROUP[any_groupgroup]",
                        "/ENTRY[entry]/identified_calibration",
                        "/ENTRY[entry]/named_collection",
                    )
                ) or k in (
                    "/ENTRY[entry]/optional_parent/req_group_in_opt_group",
                    "/ENTRY[entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatrenames]",
                ) or k.startswith("/ENTRY[entry]/OPTIONAL_group"):
                    continue

                field_name = k[k.rfind("/") + 1 :]
                if field_name != "@units" and field_name in self.data:
                    result[k] = self.data[field_name]
                    if f"{field_name}_units" in self.data:
                        result[f"{k}/@units"] = self.data[f"{field_name}_units"]

        # Hardcoded paths not covered by the generic loop above
        result["/ENTRY[entry]/optional_parent/required_child"] = 1
        result["/ENTRY[entry]/optional_parent/req_group_in_opt_group/DATA[data]"] = [0, 1]
        result["/ENTRY[entry]/does/not/exist"] = "None"
        result["/ENTRY[entry]/required_group/description"] = "A test description"
        result["/ENTRY[entry]/required_group2/description"] = "A test description"
        result["/ENTRY[entry]/program_name"] = "None"

        # Internal link
        result["/ENTRY[entry]/test_link/internal_link"] = {
            "link": "/entry/nxodd_name/posint_value"
        }

        # External link
        result["/ENTRY[entry]/test_link/external_link"] = {
            "link": f"{os.path.dirname(__file__)}/../../../data/"
            "xarray_saved_small_calibration.h5:/axes/ax3"
        }

        # Virtual dataset concatenation
        my_path = str(f"{os.path.dirname(__file__)}/../../../data/")
        result["/ENTRY[entry]/test_virtual_dataset/concatenate_datasets"] = {
            "link": [
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax0",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax1",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax2",
            ]
        }

        # Virtual dataset slicing
        result["/ENTRY[entry]/test_virtual_dataset/sliced_dataset"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, 1, :, :],
        }
        result["/ENTRY[entry]/test_virtual_dataset/sliced_dataset2"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, :, :, 1],
        }
        result["/ENTRY[entry]/test_virtual_dataset/sliced_dataset3"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, :, :, 2:4],
        }

        # Compression
        result["/ENTRY[entry]/test_compression/not_to_compress"] = {
            "compress": "string not to be compressed"
        }
        result["/ENTRY[entry]/test_compression/compressed_data"] = {
            "compress": np.array([1, 2, 3, 4])
        }

        return result


# This has to be set to allow the convert script to use this reader.
READER = ExampleReader
