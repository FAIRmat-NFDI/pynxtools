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
"""Test cases for readers used for the DataConverter"""

import glob
import importlib
import os
from typing import List
import xml.etree.ElementTree as ET

import pytest

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
from nexusparser.tools.dataconverter.convert import generate_template_from_nxdl
from nexusparser.tools.dataconverter.helpers import validate_data_dict


def get_reader(reader_path: str = None) -> BaseReader:
    """Helper function to get the reader object from it's given name"""
    spec = importlib.util.spec_from_file_location(  # type: ignore[attr-defined]
        "reader.py", reader_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[attr-defined]
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module.READER  # type: ignore[attr-defined]


def get_readers() -> List:
    """Helper function for parametrizing reader objects"""
    readers = []
    for reader_filename in get_readers_file_names():
        readers.append(get_reader(reader_filename))
    return readers


def get_readers_file_names() -> List[str]:
    """Helper function to parametrize paths of all the reader Python files"""
    return glob.glob("nexusparser/tools/dataconverter/readers/*/reader.py")


@pytest.mark.parametrize("reader", get_readers())
def test_if_readers_are_children_of_base_reader(reader):
    """Test to verify that all readers are children of BaseReader"""
    if reader.__name__ != "BaseReader":
        assert isinstance(reader(), BaseReader)


@pytest.mark.parametrize("reader", get_readers())
def test_has_correct_read_func(reader):
    """Test if all readers have a valid read function implemented"""
    assert callable(reader.read)
    if reader.__name__ != "BaseReader":
        assert hasattr(reader, "supported_nxdls")

        reader_name = reader.__name__[:reader.__name__.rindex("Reader")].lower()

        nexus_appdef_dir = os.path.join(os.getcwd(), "nexusparser", "definitions", "applications")
        dataconverter_data_dir = os.path.join("tests", "data", "tools", "dataconverter")

        input_files = glob.glob(os.path.join(dataconverter_data_dir, "readers", reader_name, "*"))

        for supported_nxdl in reader.supported_nxdls:
            if supported_nxdl == "NXtest":
                nxdl_file = os.path.join(dataconverter_data_dir, "NXtest.nxdl.xml")
            else:
                nxdl_file = os.path.join(nexus_appdef_dir, f"{supported_nxdl}.nxdl.xml")

            root = ET.parse(nxdl_file).getroot()
            template = {}
            generate_template_from_nxdl(root, template)

            read_data = reader().read(template=dict(template), file_paths=tuple(input_files))

            assert isinstance(read_data, dict)
            assert validate_data_dict(template, read_data, root)
