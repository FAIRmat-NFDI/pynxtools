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

from pynxtools.dataconverter.readers.base.reader import BaseReader

_EXCLUDED_PREFIXES = (
    "/ENTRY[entry]/required_group",
    "/ENTRY[entry]/specified_group",
    "/ENTRY[entry]/any_groupGROUP[any_groupgroup]",
    "/ENTRY[entry]/identified_calibration",
    "/ENTRY[entry]/named_collection",
    "/ENTRY[entry]/OPTIONAL_group",
)
_EXCLUDED_KEYS = frozenset(
    (
        "/ENTRY[entry]/optional_parent/req_group_in_opt_group",
        "/ENTRY[entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatrenames]",
    )
)


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    supported_nxdls = ["NXtest"]

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] = None,
        **_,
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary."""
        data: dict = {}

        if not file_paths:
            raise OSError("No input files were given to Example Reader.")

        for file_path in file_paths:
            if file_path.endswith(".json"):
                with open(file_path, encoding="utf-8") as f:
                    data = json.loads(f.read())

        for k in template.keys():
            if k.startswith(_EXCLUDED_PREFIXES) or k in _EXCLUDED_KEYS:
                continue
            field_name = k[k.rfind("/") + 1:]
            if field_name != "@units" and field_name in data:
                template[k] = data[field_name]
                if f"{field_name}_units" in data:
                    template[f"{k}/@units"] = data[f"{field_name}_units"]

        template["/ENTRY[entry]/optional_parent/required_child"] = 1
        template["/ENTRY[entry]/optional_parent/req_group_in_opt_group/DATA[data]"] = [
            0,
            1,
        ]
        template["/ENTRY[entry]/does/not/exist"] = "None"
        template["/ENTRY[entry]/required_group/description"] = "A test description"
        template["/ENTRY[entry]/required_group2/description"] = "A test description"
        template["/ENTRY[entry]/program_name"] = "None"

        # Internal link
        template["/ENTRY[entry]/test_link/internal_link"] = {
            "link": "/entry/nxodd_name/posint_value"
        }

        # External link
        template["/ENTRY[entry]/test_link/external_link"] = {
            "link": f"{os.path.dirname(__file__)}/../../../data/"
            "xarray_saved_small_calibration.h5:/axes/ax3"
        }

        # Virtual dataset concatenation
        my_path = str(f"{os.path.dirname(__file__)}/../../../data/")
        template["/ENTRY[entry]/test_virtual_dataset/concatenate_datasets"] = {
            "link": [
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax0",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax1",
                f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax2",
            ]
        }

        # Virtual dataset slicing
        template["/ENTRY[entry]/test_virtual_dataset/sliced_dataset"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, 1, :, :],
        }
        template["/ENTRY[entry]/test_virtual_dataset/sliced_dataset2"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, :, :, 1],
        }
        template["/ENTRY[entry]/test_virtual_dataset/sliced_dataset3"] = {
            "link": f"{my_path}/xarray_saved_small_calibration.h5:/binned/BinnedData",
            "shape": np.index_exp[:, :, :, 2:4],
        }

        # Compression
        template["/ENTRY[entry]/test_compression/not_to_compress"] = {
            "compress": "string not to be compressed"
        }
        template["/ENTRY[entry]/test_compression/compressed_data"] = {
            "compress": np.array([1, 2, 3, 4])
        }

        return template


# This has to be set to allow the convert script to use this reader.
READER = ExampleReader
