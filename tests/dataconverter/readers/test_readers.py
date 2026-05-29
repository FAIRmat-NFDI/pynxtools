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
import shutil
import xml.etree.ElementTree as ET

import h5py
import numpy as np
import pytest
from _pytest.mark.structures import ParameterSet

from pynxtools.dataconverter.convert import get_names_of_all_readers, get_reader
from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against

_DATACONVERTER_DATA_DIR = os.path.join("tests", "data", "dataconverter")
_JSON_MAP_DIR = os.path.join(_DATACONVERTER_DATA_DIR, "readers", "json_map")


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


def _make_nxdl_template(nxdl: str) -> Template:
    """Parse an NXDL file and return a fresh Template."""
    def_dir = os.path.join(os.getcwd(), "src", "pynxtools", "definitions")
    if nxdl in ("NXtest", "*"):
        nxdl_file = os.path.join(
            os.getcwd(), "src", "pynxtools", "data", "NXtest.nxdl.xml"
        )
    elif nxdl == "NXroot":
        nxdl_file = os.path.join(def_dir, "base_classes", "NXroot.nxdl.xml")
    else:
        nxdl_file = os.path.join(def_dir, "contributed_definitions", f"{nxdl}.nxdl.xml")
    root = ET.parse(nxdl_file).getroot()
    template = Template()
    generate_template_from_nxdl(root, template)
    return template


@pytest.mark.parametrize("reader", get_all_readers())
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_if_readers_are_children_of_base_reader(reader):
    """Test to verify that all readers are children of BaseReader or MultiFormatReader"""
    if reader.__name__ != "BaseReader":
        assert isinstance(reader(), BaseReader) or isinstance(
            reader(), MultiFormatReader
        )


@pytest.mark.parametrize("reader", get_all_readers())
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_has_correct_read_func(reader, caplog):
    """Test if all readers have a valid read function implemented"""
    assert callable(reader.read)
    if reader.__name__ not in ["BaseReader"]:
        assert hasattr(reader, "supported_nxdls")

        reader_name = get_reader_name_from_reader_object(reader)
        dataconverter_data_dir = os.path.join("tests", "data", "dataconverter")

        reader_path = os.path.join(dataconverter_data_dir, "readers", reader_name)
        if not os.path.exists(reader_path):
            return

        input_files = sorted(glob.glob(os.path.join(reader_path, "*")))
        if not reader.supported_nxdls:
            # If there are no supported nxdls test against NXroot
            reader.supported_nxdls = ["NXroot"]
        for supported_nxdl in reader.supported_nxdls:
            template = _make_nxdl_template(supported_nxdl)

            if reader_name == "json_map":
                # Use the config-file path (-c flag) rather than the deprecated
                # .mapping.json format so this test exercises the current API.
                data_files = [
                    f for f in input_files if ".mapping" not in f and ".config" not in f
                ]
                config_file = os.path.join(reader_path, "data.config.json")
                r = reader()
                r.set_config_file(config_file)
                read_data = r.read(
                    template=Template(template), file_paths=tuple(data_files)
                )
            else:
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


def test_json_map_reader_with_config_file():
    """JsonMapReader works correctly with a config file via set_config_file() (-c flag)."""
    from pynxtools.dataconverter.readers.json_map.reader import JsonMapReader

    template = _make_nxdl_template("NXtest")
    reader = JsonMapReader()
    reader.set_config_file(os.path.join(_JSON_MAP_DIR, "data.config.json"))
    read_data = reader.read(
        template=Template(template),
        file_paths=(os.path.join(_JSON_MAP_DIR, "data.json"),),
    )
    assert isinstance(read_data, Template)


def test_json_map_reader_mapping_json_emits_deprecation_warning():
    """Using a .mapping.json file must emit a DeprecationWarning."""
    from pynxtools.dataconverter.readers.json_map.reader import JsonMapReader

    template = _make_nxdl_template("NXtest")
    with pytest.warns(DeprecationWarning, match=r"\.mapping\.json.*deprecated"):
        JsonMapReader().read(
            template=Template(template),
            file_paths=(
                os.path.join(_JSON_MAP_DIR, "data.json"),
                os.path.join(_JSON_MAP_DIR, "data.mapping.json"),
            ),
        )


def test_json_map_reader_hdf5_unpacker_decodes_text_bytes_only(tmp_path):
    """HDF5 text bytes are decoded to str while numeric data remains numeric.

    Uses a copy of the real arpes.nxs file which already contains naturally
    byte-string datasets (dtype=object, value=bytes).  A byte-string array
    dataset is added to the copy to cover the array decoding path.
    """
    from pynxtools.dataconverter.readers.json_map.reader import (
        unpack_hdf_dataset_for_json_map,
    )

    src = os.path.join("src", "pynxtools", "data", "201805_WSe2_arpes.nxs")
    nxs_copy = tmp_path / "arpes_bytes_test.nxs"
    shutil.copy(src, nxs_copy)

    # Add a byte-string array dataset that does not exist in the original file.
    with h5py.File(nxs_copy, "a") as h5f:
        h5f.create_dataset("entry/probe_labels", data=np.array([b"x-ray", b"uv"]))
        ds = h5f["entry/start_time"]
        ds[()] = np.bytes_("2018-05-01T08:00:00+02:00")  # Another byte-string scalar

    with h5py.File(nxs_copy, "r") as h5f:
        # Naturally byte-string scalar field (dtype=object, raw value is bytes)
        text_scalar = unpack_hdf_dataset_for_json_map(h5f["entry/definition"])
        # Naturally byte-string scalar used as a date string
        text_date = unpack_hdf_dataset_for_json_map(h5f["entry/end_time"])
        text_start_time = unpack_hdf_dataset_for_json_map(h5f["entry/start_time"])
        # Byte-string array we added above
        text_array = unpack_hdf_dataset_for_json_map(h5f["entry/probe_labels"])
        # Native integer scalar — must not be coerced
        int_scalar = unpack_hdf_dataset_for_json_map(h5f["entry/collection_time"])
        # Native float64 array — must not be coerced
        float_array = unpack_hdf_dataset_for_json_map(h5f["entry/data/energies"])

    # Byte scalars become plain Python str
    assert isinstance(text_scalar, str)
    assert text_scalar == "NXarpes"

    assert isinstance(text_start_time, str)
    assert text_start_time == "2018-05-01T08:00:00+02:00"

    assert isinstance(text_date, str)
    assert text_date == "2018-05-01T09:22:00+02:00"

    # Byte arrays become unicode ndarray
    assert isinstance(text_array, np.ndarray)
    assert text_array.dtype.kind == "U"
    assert np.array_equal(text_array, np.array(["x-ray", "uv"]))

    # Integer data unchanged
    assert int_scalar == 7200
    assert np.issubdtype(type(int_scalar), np.integer)

    # Float array unchanged
    assert isinstance(float_array, np.ndarray)
    assert np.issubdtype(float_array.dtype, np.floating)
