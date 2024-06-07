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
"""An example reader implementation for the DataConverter."""

import json
import os
from typing import Any, Tuple

import numpy as np

from pynxtools.dataconverter.readers.base.reader import BaseReader


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXtest"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        data: dict = {}

        if not file_paths:
            raise IOError("No input files were given to Example Reader.")

        for file_path in file_paths:
            file_extension = file_path[file_path.rindex(".") :]
            with open(file_path, "r", encoding="utf-8") as input_file:
                if file_extension == ".json":
                    data = json.loads(input_file.read())

        for k in template.keys():
            # The entries in the template dict should correspond with what the dataconverter
            # outputs with --generate-template for a provided NXDL file
            if (
                k.startswith("/ENTRY[entry]/required_group")
                or k == "/ENTRY[entry]/optional_parent/req_group_in_opt_group"
                or k.startswith("/ENTRY[entry]/OPTIONAL_group")
            ):
                continue

            field_name = k[k.rfind("/") + 1 :]
            if field_name != "@units":
                template[k] = data[field_name]
                if f"{field_name}_units" in data.keys():
                    template[f"{k}/@units"] = data[f"{field_name}_units"]

        template["required"]["/ENTRY[entry]/optional_parent/required_child"] = 1
        template["optional"][
            "/ENTRY[entry]/optional_parent/req_group_in_opt_group/DATA[data]"
        ] = [0, 1]

        # Add non template key
        template["/ENTRY[entry]/does/not/exist"] = "None"
        template["/ENTRY[entry]/required_group/description"] = "A test description"
        template["/ENTRY[entry]/required_group2/description"] = "A test description"
        template["/ENTRY[entry]/program_name"] = "None"

        # internal links
        template["/ENTRY[entry]/test_link/internal_link"] = {
            "link": "/entry/nxodd_name/posint_value"
        }

        # external links
        template[("/ENTRY[entry]/test_link/external_link")] = {
            "link": f"{os.path.dirname(__file__)}/../../../data/"
            "xarray_saved_small_calibration.h5:/axes/ax3"
        }

        # virtual datasets concatenation
        my_path = str(f"{os.path.dirname(__file__)}/../../../data/")
        my_datasets = {
            "link": [
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax0",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax1",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax2",
            ]
        }
        template["/ENTRY[entry]/test_virtual_dataset/concatenate_datasets"] = (
            my_datasets
        )

        # virtual datasets slicing
        my_path = str(f"{os.path.dirname(__file__)}/../../../data/")
        template[("/ENTRY[entry]" "/test_virtual" "_dataset/sliced" "_dataset")] = {
            "link": (
                f"{my_path}/xarray_saved_small_" "calibration.h5:/binned/BinnedData"
            ),
            "shape": np.index_exp[:, 1, :, :],
        }
        template[("/ENTRY[entry]" "/test_virtual" "_dataset/slic" "ed_dataset2")] = {
            "link": (
                f"{my_path}/xarray_saved_small" "_calibration.h5:/binned/BinnedData"
            ),
            "shape": np.index_exp[:, :, :, 1],
        }
        template[("/ENTRY[entry]" "/test_virtual" "_dataset/slic" "ed_dataset3")] = {
            "link": (
                f"{my_path}/xarray_saved_small" "_calibration.h5:/binned/BinnedData"
            ),
            "shape": np.index_exp[:, :, :, 2:4],
        }

        # compression
        my_compression_dict = {"compress": "string not to be compressed"}
        template["/ENTRY[entry]/test_compression/not_to_compress"] = my_compression_dict
        my_compression_dict2 = {"compress": np.array([1, 2, 3, 4])}
        template["/ENTRY[entry]/test_compression/compressed_data"] = (
            my_compression_dict2
        )

        # sh = h5py.File(file_names_to_concatenate[0], 'r')[entry_key].shape
        # layout = h5py.VirtualLayout(shape=(len(file_names_to_concatenate),) + sh,
        #                             dtype=np.float64)

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
