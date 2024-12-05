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
"""Test cases for the helper functions used by the DataConverter."""

import logging
import os
import shutil
import xml.etree.ElementTree as ET
from typing import Optional

import h5py
import numpy as np
import pytest
from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against

import pytest
from pynxtools.dataconverter.readers.multi.reader import (
    fill_wildcard_data_indices,
    ParseJsonCallbacks,
    resolve_special_keys,
    fill_from_config,
    MultiFormatReader,
)

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.readers.utils import parse_yml

logger = logging.getLogger("pynxtools")

CONVERT_DICT = {
    "unit": "@units",
    "version": "@version",
    "user": "USER[user]",
    "instrument": "INSTRUMENT[instrument]",
    "detector": "DETECTOR[detector]",
    "sample": "SAMPLE[sample]",
}


@pytest.fixture
class MyDataReader(MultiFormatReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    supported_nxdls = ["NXsimple"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            ".hdf5": self.handle_hdf5_file,
            ".h5": self.handle_hdf5_file,
        }

    def set_config_file(self, file_path: str) -> Dict[str, Any]:
        if self.config_file is not None:
            logger.info(
                f"Config file already set. Replaced by the new file {file_path}."
            )
        self.config_file = file_path
        return {}

    def handle_hdf5_file(self, filepath) -> Dict[str, Any]:
        def recursively_read_group(group, path=""):
            result = {}
            for key, item in group.items():
                new_path = f"{path}/{key}" if path else key
                if isinstance(item, h5py.Group):
                    # Recursively read subgroups
                    result.update(recursively_read_group(item, new_path))
                elif isinstance(item, h5py.Dataset):
                    # Read datasets
                    result[new_path] = item[()]
            return result

        # Open the HDF5 file and read its contents
        with h5py.File(filepath, "r") as hdf:
            self.hdf5_data = recursively_read_group(hdf)

        return {}

    def handle_eln_file(self, file_path: str) -> Dict[str, Any]:
        self.eln_data = parse_yml(
            file_path,
            convert_dict=CONVERT_DICT,
            parent_key="/ENTRY[entry]",
        )

        return {}

    def get_attr(self, key: str, path: str) -> Any:
        """
        Get the metadata that was stored in the main file.
        """
        if self.hdf5_data is None:
            return None

        return self.hdf5_data.get(path)

    def get_eln_data(self, key: str, path: str) -> Any:
        """Returns data from the given eln path."""
        if self.eln_data is None:
            return None

        return self.eln_data.get(key)

    def get_data(self, key: str, path: str) -> Any:
        """Returns measurement data from the given hdf5 path."""
        if path.endswith(("x_values", "y_values")):
            return self.hdf5_data.get(f"data/{path}")
        else:
            logger.warning(f"No axis name corresponding to the path {path}.")


@pytest.mark.parametrize("config_file_dict, key, value, dims, expected_result", [])
def test_fill_wildcard_data_indices(
    config_file_dict, key, value, dims, expected_result
):
    result = fill_wildcard_data_indices(config_file_dict, key, value, dims)
    assert result == expected_result


def test_json_callbacks():
    result = None
    # assert result == expected_result


def test_resolve_special_keys(
    new_entry_dict: Dict[str, Any],
    key: str,
    value: Any,
    optional_groups_to_remove: List[str],
    optional_groups_to_remove_from_links: List[str],
    callbacks: ParseJsonCallbacks,
    suppress_warning: bool = False,
):
    result = None
    # assert result == expected_result


def test_fill_from_config(
    config_dict,
    entry_names,
    callbacks,
    suppress_warning,
):
    pass


@pytest.mark.parametrize("config_file_dict, key, value, dims, expected_result", [])
class test_multi_format_reader(MyDataReader, config_file):
    pass
    # assert result == expected_result
