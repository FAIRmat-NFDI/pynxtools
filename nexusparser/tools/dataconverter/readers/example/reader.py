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
import os
from typing import Tuple, Any
import json

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXtest"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        data: dict = {}

        if not file_paths:
            raise Exception("No input files were given to Example Reader.")

        for file_path in file_paths:
            file_extension = file_path[file_path.rindex("."):]
            with open(file_path, "r") as input_file:
                if file_extension == ".json":
                    data = json.loads(input_file.read())

        for k in template.keys():
            # The entries in the template dict should correspond with what the dataconverter
            # outputs with --generate-template for a provided NXDL file
            field_name = k[k.rfind("/") + 1:]
            if field_name != "@units":
                template[k] = data[field_name]
                if f"{field_name}_units" in data.keys() and f"{k}/@units" in template.keys():
                    template[f"{k}/@units"] = data[f"{field_name}_units"]

        # Add non template key
        template["/ENTRY[entry]/does/not/exist"] = "None"
        template["/ENTRY[entry]/program_name"] = "None"

        # internal links
        my_int_link_dict = {"link": "/entry/NXODD_name/posint_value"}
        template["/ENTRY[entry]/test_link/internal_link"] = my_int_link_dict

        # external links
        my_ext_link_dict = {"link":
                            f"{os.path.dirname(__file__)}/../../../../../tests/"
                            f"data/tools/dataconverter/readers/mpes/"
                            f"xarray_saved_small_calibration.h5:/axes/ax3"
                            }
        template["/ENTRY[entry]/test_link/external_link"] = my_ext_link_dict

        # virtual datasets concatenation
        my_path = str(f"{os.path.dirname(__file__)}/../../../../../tests/"
                      f"data/tools/dataconverter/readers/mpes")
        my_datasets = {"link":
                       [f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax0",
                        f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax1",
                        f"{my_path}/xarray_saved_small_calibration.h5:/axes/ax2"
                        ]
                       }
        template["/ENTRY[entry]/test_virtual_dataset/concatenate_datasets"] = my_datasets

        # sh = h5py.File(file_names_to_concatenate[0], 'r')[entry_key].shape
        # layout = h5py.VirtualLayout(shape=(len(file_names_to_concatenate),) + sh,
        #                             dtype=np.float64)

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
