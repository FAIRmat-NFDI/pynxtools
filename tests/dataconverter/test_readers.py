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
import logging
import os
import xml.etree.ElementTree as ET

import pytest
from _pytest.mark.structures import ParameterSet

from pynxtools.dataconverter.convert import get_names_of_all_readers, get_reader
from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against


def get_reader_name_from_reader_object(reader) -> str:
    """Helper function to find the name of a reader given the reader object."""
    for reader_name in get_names_of_all_readers():
        gotten_reader = get_reader(reader_name)
        if reader.__name__ is gotten_reader.__name__:
            return reader_name
    return ""


def get_readers_file_names() -> list[str]:
    """Helper function to parametrize paths of all the reader Python files"""
    return sorted(glob.glob("pynxtools/dataconverter/readers/*/reader.py"))


def get_all_readers() -> list[ParameterSet]:
    """Scans through the reader list and returns them for pytest parametrization"""
    readers = []

    for reader in [get_reader(x) for x in get_names_of_all_readers()]:
        readers.append(pytest.param(reader))

    return readers


@pytest.mark.parametrize("reader", get_all_readers())
def test_if_readers_are_children_of_base_reader(reader):
    """Test to verify that all readers are children of BaseReader or MultiFormatReader"""
    if reader.__name__ != "BaseReader":
        assert isinstance(reader(), BaseReader) or isinstance(
            reader(), MultiFormatReader
        )


@pytest.mark.parametrize("reader", get_all_readers())
def test_has_correct_read_func(reader, caplog):
    """Test if all readers have a valid read function implemented"""
    assert callable(reader.read)
    if reader.__name__ not in ["BaseReader"]:
        assert hasattr(reader, "supported_nxdls")

        reader_name = get_reader_name_from_reader_object(reader)
        def_dir = os.path.join(os.getcwd(), "src", "pynxtools", "definitions")
        dataconverter_data_dir = os.path.join("tests", "data", "dataconverter")

        reader_path = os.path.join(dataconverter_data_dir, "readers", reader_name)
        if not os.path.exists(reader_path):
            return

        input_files = sorted(glob.glob(os.path.join(reader_path, "*")))
        if not reader.supported_nxdls:
            # If there are no supported nxdls test against NXroot
            reader.supported_nxdls = ["NXroot"]
        for supported_nxdl in reader.supported_nxdls:
            if supported_nxdl in ("NXtest", "*"):
                nxdl_file = os.path.join(
                    os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"
                )
            elif supported_nxdl == "NXroot":
                nxdl_file = os.path.join(def_dir, "base_classes", "NXroot.nxdl.xml")
            else:
                nxdl_file = os.path.join(
                    def_dir, "contributed_definitions", f"{supported_nxdl}.nxdl.xml"
                )

            root = ET.parse(nxdl_file).getroot()
            template = Template()
            generate_template_from_nxdl(root, template)

            read_data = reader().read(
                template=Template(template), file_paths=tuple(input_files)
            )

            if supported_nxdl == "*":
                supported_nxdl = "NXtest"

            assert isinstance(read_data, Template)

            # This is a temporary fix because the json_yml example data
            # does not produce a valid entry.
            if not reader_name == "json_yml":
                with caplog.at_level(logging.WARNING):
                    validate_dict_against(
                        supported_nxdl, read_data, ignore_undocumented=True
                    )

                print(caplog.text)
