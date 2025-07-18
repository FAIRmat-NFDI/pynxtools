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

import numpy as np
import pytest

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template


def alter_dict(data_dict: Template, key: str, value: object):
    """Helper function to alter a single entry in dict for parametrize."""
    if data_dict is not None:
        internal_dict = Template(data_dict)
        internal_dict[key] = value
        return internal_dict

    return None


@pytest.fixture(name="template")
def fixture_template():
    """pytest fixture to use the same template in all tests"""
    nxdl_root = ET.parse("src/pynxtools/data/NXtest.nxdl.xml").getroot()

    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)
    return template


@pytest.mark.usefixtures("template")
@pytest.fixture(name="filled_test_data")
def fixture_filled_test_data(template, tmp_path):
    """pytest fixture to setup a filled in template."""

    # Copy original measurement file to tmp dir,
    # because h5py.ExternalLink is modifying it while
    # linking the nxs file.
    shutil.copy(
        os.path.join(
            os.getcwd(), "src", "pynxtools", "data", "xarray_saved_small_calibration.h5"
        ),
        tmp_path,
    )

    template.clear()
    template[
        "/ENTRY[my_entry]/NXODD_name[nxodd_name]/anamethatRENAMES[anamethatichangetothis]"
    ] = 2
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value"] = 2.0
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/float_value/@units"] = "nm"
    template["/ENTRY[my_entry]/optional_parent/required_child"] = 1
    template["/ENTRY[my_entry]/optional_parent/optional_child"] = 1
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/bool_value"] = True
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value"] = 2
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/int_value/@units"] = "eV"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value"] = 2
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/number_value/@units"] = "eV"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value"] = np.array(
        [1, 2, 3], dtype=np.int8
    )
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/posint_value/@units"] = "kg"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/char_value"] = "just chars"
    template["/ENTRY[my_entry]/definition"] = "NXtest"
    template["/ENTRY[my_entry]/definition/@version"] = "2.4.6"
    template["/ENTRY[my_entry]/program_name"] = "Testing program"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/type"] = "2nd type"
    template["/ENTRY[my_entry]/NXODD_name[nxodd_name]/date_value"] = (
        "2022-01-22T12:14:12.05018+00:00"
    )
    template["/ENTRY[my_entry]/required_group/description"] = "An example description"
    template["/ENTRY[my_entry]/required_group2/description"] = "An example description"
    template["/ENTRY[my_entry]/does/not/exist"] = "random"
    template["/ENTRY[my_entry]/links/ext_link"] = {
        "link": f"{tmp_path}/xarray_saved_small_calibration.h5:/axes/ax3"
    }
    return template


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("2.4E-23", 2.4e-23),
        ("28", 28),
        ("45.98", 45.98),
        ("test", "test"),
        (["59", "3.00005", "498E-36"], np.array([59.0, 3.00005, 4.98e-34])),
        ("23 34 444 5000", np.array([23.0, 34.0, 444.0, 5000.0])),
        ("xrd experiment", "xrd experiment"),
        (None, None),
    ],
)
def test_transform_to_intended_dt(input_data, expected_output):
    """Transform to possible numerical method."""
    result = helpers.transform_to_intended_dt(input_data)

    # Use pytest.approx for comparing floating-point numbers
    if isinstance(expected_output, np.ndarray):
        np.testing.assert_allclose(result, expected_output, rtol=1e-3)
    elif isinstance(expected_output, float):
        assert result == pytest.approx(expected_output, rel=1e-5)
    else:
        assert result == expected_output


@pytest.mark.parametrize(
    "nxdl_path,expected",
    [
        pytest.param(
            "/ENTRY/definition/@version",
            ["/ENTRY[entry]/definition/@version"],
            id="path-exists-in-dict",
        ),
        pytest.param("/RANDOM/does/not/@exist", [], id="path-does-not-exist-in-dict"),
    ],
)
def test_path_in_data_dict(nxdl_path, expected, template):
    """Unit test for helper function to check if an NXDL path exists in the reader dictionary."""
    assert helpers.path_in_data_dict(nxdl_path, tuple(template.keys())) == expected


def test_atom_type_extractor_and_hill_conversion():
    """
    Test atom type extractor and conversion to hill
    """

    test_chemical_formula = "(C38H54S4)n(NaO2)5(CH4)NH3B"
    expected_atom_types = ["C", "H", "B", "N", "Na", "O", "S"]

    atom_list = helpers.extract_atom_types(test_chemical_formula)

    assert expected_atom_types == atom_list


def test_writing_of_root_attributes(caplog):
    """
    Tests if all root attributes are populated
    """
    template = Template()
    filename = "my_nexus_file.nxs"
    with caplog.at_level(logging.WARNING):
        helpers.add_default_root_attributes(template, filename)
        helpers.write_nexus_def_to_entry(template, "entry", "NXtest")
        helpers.write_nexus_def_to_entry(template, "entry1", "NXtest")

    assert "" == caplog.text

    keys_added = template.keys()
    assert "/@NX_class" in keys_added
    assert template["/@NX_class"] == "NXroot"
    assert "/@file_name" in keys_added
    assert template["/@file_name"] == filename
    assert "/@file_time" in keys_added
    assert "/@file_update_time" in keys_added
    assert "/@NeXus_repository" in keys_added
    assert "/@NeXus_release" in keys_added
    assert "/@HDF5_Version" in keys_added
    assert "/@h5py_version" in keys_added
    assert "/ENTRY[entry]/definition" in keys_added
    assert "/ENTRY[entry]/definition/@version" in keys_added
    assert "/ENTRY[entry1]/definition" in keys_added
    assert "/ENTRY[entry1]/definition/@version" in keys_added


def test_warning_on_root_attribute_overwrite(caplog):
    """
    A warning is emitted when a root attribute is overwritten
    by pynxtools.
    """
    template = Template()
    template["/@NX_class"] = "NXwrong"
    filname = "my_nexus_file.nxs"
    with caplog.at_level(logging.WARNING):
        helpers.add_default_root_attributes(template, filname)
    error_text = (
        "The NXroot entry '/@NX_class' (value: NXwrong) should not be changed by the reader. "
        "This is overwritten by the actually used value 'NXroot'"
    )
    assert error_text in caplog.text

    assert "/@NX_class" in template.keys()
    assert template["/@NX_class"] == "NXroot"


def test_warning_on_definition_changed_by_reader(caplog):
    template = Template()
    template["/ENTRY[entry]/definition"] = "NXwrong"
    with caplog.at_level(logging.WARNING):
        helpers.write_nexus_def_to_entry(template, "entry", "NXtest")

    error_text = (
        "The entry '/ENTRY[entry]/definition' (value: NXtest) should not be changed by the reader. "
        "This is overwritten by the actually used value 'NXwrong'"
    )
    assert error_text in caplog.text

    assert "/ENTRY[entry]/definition" in template.keys()
    assert template["/ENTRY[entry]/definition"] == "NXtest"
