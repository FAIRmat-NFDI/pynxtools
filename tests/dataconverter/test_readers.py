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
from importlib import import_module
from pathlib import Path
from typing import List

import pytest
from _pytest.mark.structures import ParameterSet
from importlib_metadata import entry_points

from pynxtools.dataconverter.convert import get_names_of_all_readers, get_reader
from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against


def get_reader_name_from_reader_object(reader) -> str:
    """Helper function to find the name of a reader given the reader object."""
    for reader_name in get_names_of_all_readers():
        gotten_reader = get_reader(reader_name)
        if reader.__name__ is gotten_reader.__name__:
            return reader_name
    return ""


def get_readers_file_names() -> List[str]:
    """Helper function to parametrize paths of all the reader Python files"""
    return sorted(glob.glob("pynxtools/dataconverter/readers/*/reader.py"))


def get_all_readers() -> List[ParameterSet]:
    """Scans through the reader list and returns them for pytest parametrization"""
    readers = []

    # Explicitly removing ApmReader and EmNionReader because we need to add test data
    for reader in [get_reader(x) for x in get_names_of_all_readers()]:
        if reader.__name__ in (
            "ApmReader",
            "EmOmReader",
            "EmSpctrscpyReader",
            "EmNionReader",
        ):
            readers.append(
                pytest.param(
                    reader, marks=pytest.mark.skip(reason="Missing test data.")
                )
            )
        else:
            readers.append(pytest.param(reader))

    return readers


@pytest.mark.parametrize("reader", get_all_readers())
def test_if_readers_are_children_of_base_reader(reader):
    """Test to verify that all readers are children of BaseReader"""
    if reader.__name__ != "BaseReader":
        assert isinstance(reader(), BaseReader)


@pytest.mark.parametrize("reader", get_all_readers())
def test_has_correct_read_func(reader, caplog):
    """Test if all readers have a valid read function implemented"""
    assert callable(reader.read)
    if reader.__name__ not in ["BaseReader"]:
        assert hasattr(reader, "supported_nxdls")

        reader_name = get_reader_name_from_reader_object(reader)
        def_dir = os.path.join(os.getcwd(), "pynxtools", "definitions")
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
                nxdl_file = os.path.join(dataconverter_data_dir, "NXtest.nxdl.xml")
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
<<<<<<< HEAD

            # This is a temporary fix because the json_yml example data
            # does not produce a valid entry.
            if not reader_name == "json_yml":
                with caplog.at_level(logging.WARNING):
                    validate_dict_against(
                        supported_nxdl, read_data, ignore_undocumented=True
                    )

                print(caplog.text)
=======
            assert validate_data_dict(template, read_data, root)


def get_reader_from_plugin(package_name, rader_name):
    reader_full_path = [
        file
        for file in glob.glob(f"{str(package_name)}/**", recursive=True)
        if file.endswith(f"{os.sep}reader.py")
    ][0]

    reader_spec = importlib.util.spec_from_file_location("reader", reader_full_path)
    reader_module = importlib.util.module_from_spec(reader_spec)
    reader_spec.loader.exec_module(reader_module)
    reader = getattr(reader_module, rader_name)
    return reader


def parametrize_data_for_single_plugin(plugin_name):
    """ """

    nxdl = ""
    reader = ""
    example_dir = ""
    plug_pkg = import_module(plugin_name)

    plugin_dir = Path(plug_pkg.__file__).parent.parent

    example_dir = plugin_dir / "examples"
    launch_file = plugin_dir / "launch.json"

    try:
        with open(launch_file, "r", encoding="utf-8") as f:
            launch_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Incorrect syntax in Json file {launch_file} {e}")
    except FileNotFoundError as e:
        print(f"Error reading {launch_file} {e}")

    for launch in launch_data["launch_data"]:
        nxdl = launch["nxdl"]
        reader = launch["reader"]
        reader = get_reader_from_plugin(plugin_dir, reader)
        # load reader
        plugin_name_json = launch["plugin_name"]
        lnch_example_dir = launch["example_dir"]
        example_dirs = glob.glob(str(example_dir / lnch_example_dir))
        for example_dir in example_dirs:
            assert (
                plugin_name_json == plugin_name
            ), f"Plugin name mismatch: '{plugin_name}' from pynxtools plugin entry_points and '{plugin_name_json}' from test_config.json"
            yield nxdl, reader, plugin_name, example_dir


def get_plugin_list():
    """ """
    plugin_list = list(
        map(
            lambda plg: plg.value.split(".")[0].replace("-", "_"),
            entry_points(group="pynxtools.reader"),
        )
    )
    return list(set(plugin_list))


def get_parametrized_data():
    """ """
    plugin_list = get_plugin_list()

    for plugin_name in plugin_list:
        print(f"**** Test for plugiin : {plugin_name} ****")
        try:
            yield from parametrize_data_for_single_plugin(plugin_name)
        except Exception as e:
            print(f"Unable to find test setup for {plugin_name} {e}")
            continue


def test_general_readers(tmp_path, caplog):
    total_plugins = len(get_plugin_list())
    tested_plugins = []
    # test plugin reader
    for nxdl, reader, plugin_name, example_data in list(get_parametrized_data()):
        test = ReaderTest(nxdl, reader, example_data, tmp_path, caplog)
        test.convert_to_nexus()
        test.check_reproducibility_of_nexus()
<<<<<<< HEAD
>>>>>>> 177afcb (Apparently everything works.)
=======
        tested_plugins.append(plugin_name)

    # Check if all plugins pass the test
    assert len(list(set(tested_plugins))) == total_plugins
>>>>>>> aa4b2bc (stm plugin passed.)
