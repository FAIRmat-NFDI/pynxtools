"""This is a code that performs several tests on nexus tool"""
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

import difflib
import logging
import os

import lxml.etree as ET
import numpy as np
import pytest

from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_inherited_nodes,
    get_node_at_nxdl_path,
    get_nx_attribute_type,
    get_nx_classes,
    get_nx_units,
)
from pynxtools.nexus.nexus import HandleNexus, decode_if_string

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "string_obj, decode, expected",
    [
        # Test with np.ndarray of bytes (fixed-length)
        (
            np.array([b"fixed1", b"fixed2"], dtype="S10"),
            True,
            np.array(["fixed1", "fixed2"], dtype="U7"),
        ),
        (
            np.array([b"fixed1   ", b"fixed2   "], dtype="S10"),
            False,
            np.array([b"fixed1   ", b"fixed2   "], dtype="S10"),
        ),
        # Variable-length byte arrays
        (
            np.array([b"var1", b"var2", b"var3"]),
            True,
            np.array(["var1", "var2", "var3"], dtype="U4"),
        ),
        (
            np.array([b"var1", b"var2", b"var3"]),
            False,
            np.array([b"var1", b"var2", b"var3"], dtype="S4"),
        ),
        # Empty arrays
        (np.array([], dtype=object), True, np.array([], dtype=object)),
        (np.array([], dtype=object), False, np.array([], dtype=object)),
        # Numpy array with non-byte elements
        (np.array([1, 2, 3]), True, np.array([1, 2, 3])),
        (np.array([1, 2, 3]), False, np.array([1, 2, 3])),
        # Numpy array with mixed types
        (
            np.array([b"bytes", "string"], dtype=object),
            True,
            np.array(["bytes", "string"], dtype="U6"),
        ),
        (
            np.array([b"bytes", "string"], dtype=object),
            False,
            np.array([b"bytes", "string"], dtype=object),
        ),
        # Test with lists of bytes and strings
        ([b"bytes", "string"], True, ["bytes", "string"]),
        ([b"bytes", "string"], False, [b"bytes", "string"]),
        ([b"bytes", b"more_bytes", "string"], True, ["bytes", "more_bytes", "string"]),
        (
            [b"bytes", b"more_bytes", "string"],
            False,
            [b"bytes", b"more_bytes", "string"],
        ),
        ([b"fixed", b"length", b"strings"], True, ["fixed", "length", "strings"]),
        ([b"fixed", b"length", b"strings"], False, [b"fixed", b"length", b"strings"]),
        # Test with nested lists
        ([[b"nested1"], [b"nested2"]], True, [["nested1"], ["nested2"]]),
        ([[b"nested1"], [b"nested2"]], False, [[b"nested1"], [b"nested2"]]),
        # Test with bytes
        (b"single", True, "single"),
        (b"single", False, b"single"),
        # Empty byte string
        (b"", True, ""),
        (b"", False, b""),
        # Test with str
        ("single", True, "single"),
        ("single", False, "single"),
        # Test with non-decodable data types
        (123, True, 123),
        (123, False, 123),
        (None, True, None),
        (None, False, None),
        # Numpy array with nested structure
        (
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
            True,
            np.array([["nested1"], ["nested2"]], dtype="U7"),
        ),
        (
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
            False,
            np.array([[b"nested1"], [b"nested2"]], dtype="S7"),
        ),
    ],
)
def test_decode_if_string(string_obj, decode, expected):
    result = decode_if_string(elem=string_obj, decode=decode)

    # Handle np.ndarray outputs
    if isinstance(expected, np.ndarray):
        assert isinstance(result, np.ndarray), (
            f"Expected ndarray, but got {type(result)}"
        )
        assert (result == expected).all(), (
            f"Failed for {string_obj} with decode={decode}"
        )
    # Handle list outputs
    elif isinstance(expected, list):
        assert isinstance(result, list), f"Expected list, but got {type(result)}"
    # Handle all other cases
    else:
        assert result == expected, f"Failed for {string_obj} with decode={decode}"


def test_get_nexus_classes_units_attributes():
    """Check the correct parsing of a separate list for:
    Nexus classes (base_classes)
    Nexus units (memberTypes)
    Nexus attribute type (primitiveTypes)
    the tested functions can be found in nexus.py file"""

    # Test 1
    nexus_classes_list = get_nx_classes()

    assert "NXbeam" in nexus_classes_list

    # Test 2
    nexus_units_list = get_nx_units()
    assert "NX_TEMPERATURE" in nexus_units_list

    # Test 3
    nexus_attribute_list = get_nx_attribute_type()
    assert "NX_FLOAT" in nexus_attribute_list


def test_nexus(tmp_path):
    """
    The nexus test function
    """
    dirpath = os.path.join(os.path.dirname(__file__), "../data/nexus")
    example_data = os.path.join(
        os.getcwd(), "src", "pynxtools", "data", "201805_WSe2_arpes.nxs"
    )

    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(tmp_path, "nexus_test.log"), "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, example_data, None, None)

    default_print_options = {
        "edgeitems": 3,
        "threshold": 1000,
        "precision": 8,
        "linewidth": 75,
    }

    np.set_printoptions(**default_print_options)
    nexus_helper.process_nexus_master_file(None)

    with open(os.path.join(tmp_path, "nexus_test.log"), encoding="utf-8") as logfile:
        log = logfile.readlines()
    with open(
        os.path.join(dirpath, "Ref_nexus_test.log"),
        encoding="utf-8",
    ) as ref_file:
        ref = ref_file.readlines()

    if log != ref:
        differences = list(
            difflib.unified_diff(
                ref, log, fromfile="reference", tofile="actual", lineterm=""
            )
        )
        diff_report = "\n".join(differences)
        if diff_report:
            pytest.fail(f"Log output does not match reference:\n{diff_report}")
        pytest.fail(
            f"Log output does not match reference even though each individual line matches."
        )


def test_get_node_at_nxdl_path():
    """Test to verify if we receive the right XML element for a given NXDL path"""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nxdl_file_path = os.path.join(local_dir, "../../src/pynxtools/data/NXtest.nxdl.xml")

    elem = ET.parse(nxdl_file_path).getroot()

    node = get_node_at_nxdl_path("/ENTRY/NXODD_name", elem=elem)
    assert node.attrib["type"] == "NXdata"
    assert node.attrib["name"] == "NXODD_name"

    node = get_node_at_nxdl_path("/ENTRY/NXODD_name/anamethatRENAMES", elem=elem)
    assert node.attrib["type"] == "NX_INT"
    assert node.attrib["name"] == "anamethatRENAMES"
    assert node.attrib["nameType"] == "partial"
    assert node.attrib["units"] == "NX_UNITLESS"

    node = get_node_at_nxdl_path("/ENTRY/NXODD_name/float_value", elem=elem)
    assert node.attrib["type"] == "NX_FLOAT"
    assert node.attrib["name"] == "float_value"
    assert not node.attrib.get("nameType")

    node = get_node_at_nxdl_path("/ENTRY/NXODD_name/AXISNAME/long_name", elem=elem)
    assert node.attrib["name"] == "long_name"

    node = get_node_at_nxdl_path("/ENTRY/NXODD_name/group_attribute", elem=elem)
    assert node.attrib["name"] == "group_attribute"

    node = get_node_at_nxdl_path("/ENTRY/optional_parent", elem=elem)
    assert node.attrib["name"] == "optional_parent"
    assert node.attrib["optional"] == "true"

    node = get_node_at_nxdl_path("/ENTRY/optional_parent/required_child", elem=elem)
    assert node.attrib["name"] == "required_child"
    assert node.attrib["type"] == "NX_INT"
    assert node.attrib["required"] == "true"

    node = get_node_at_nxdl_path("/ENTRY/USER/affiliation", elem=elem)
    assert node.attrib["name"] == "affiliation"


def test_get_inherited_nodes():
    """Test to verify if we receive the right XML element list for a given NXDL path."""
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nxdl_file_path = os.path.join(
        local_dir,
        "../../src/pynxtools/definitions/contributed_definitions/NXiv_temp.nxdl.xml",
    )
    elem = ET.parse(nxdl_file_path).getroot()
    (_, _, elem_list) = get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT", elem=elem
    )
    assert len(elem_list) == 4

    (_, _, elem_list) = get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller", elem=elem
    )
    assert len(elem_list) == 6

    (_, _, elem_list) = get_inherited_nodes(
        nxdl_path="/ENTRY/INSTRUMENT/ENVIRONMENT/voltage_controller",
        nx_name="NXiv_temp",
    )
    assert len(elem_list) == 6


def test_c_option(tmp_path):
    """
    To check -c option from IV_temp.nxs.
    """
    local_path = os.path.dirname(__file__)
    path_to_ref_files = os.path.join(local_path, "../data/nexus/")

    ref_file = os.path.join(path_to_ref_files, "Ref1_c_option_test.log")
    tmp_file = os.path.join(tmp_path, "c_option_1_test.log")

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(tmp_file, "w")

    with open(ref_file, encoding="utf-8") as ref_f:
        ref = ref_f.readlines()

    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    nexus_helper = HandleNexus(logger, None, None, "/NXbeam")
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()

    assert tmp == ref

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, None, None, "/NXdetector/data")
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == "INFO: entry/instrument/analyser/data\n"

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, None, None, "/NXdata@signal")
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == "INFO: entry/data@signal\n"


def test_d_option(tmp_path):
    """
    To check -d option for default NXarpes test data file.
    """
    tmp_file = os.path.join(tmp_path, "d_option_1_test.log")

    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(tmp_file, "w")

    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, None, "/entry/instrument/analyser/data", None)
    nexus_helper.process_nexus_master_file(None)

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()

    assert (
        tmp[0]
        == "DEBUG: ===== FIELD (//entry/instrument/analyser/data): "
        + '<HDF5 dataset "data": shape (80, 146, 195), type "<f4">\n'
    )
