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

import pytest

try:
    from nomad.metainfo import Section
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from typing import Any

from pynxtools.nomad.schema import nexus_metainfo_package
from pynxtools.nomad.utils import _rename_nx_for_nomad as rename_nx_for_nomad


@pytest.mark.parametrize(
    "path,value",
    [
        pytest.param("name", "pynxtools.nomad.schema"),
        pytest.param(rename_nx_for_nomad("NXobject") + ".name", "Object"),
        pytest.param(rename_nx_for_nomad("NXentry") + ".nx_kind", "group"),
        pytest.param(rename_nx_for_nomad("NXdetector") + ".real_time__field", "*"),
        pytest.param(rename_nx_for_nomad("NXentry") + ".DATA.nx_optional", True),
        pytest.param(rename_nx_for_nomad("NXentry") + ".DATA.nx_kind", "group"),
        pytest.param(rename_nx_for_nomad("NXentry") + ".DATA.nx_optional", True),
        pytest.param(
            rename_nx_for_nomad("NXdetector") + ".real_time__field.name",
            "real_time__field",
        ),
        pytest.param(
            rename_nx_for_nomad("NXdetector") + ".real_time__field.nx_type", "NX_NUMBER"
        ),
        pytest.param(
            rename_nx_for_nomad("NXdetector") + ".real_time__field.nx_units", "NX_TIME"
        ),
        pytest.param(rename_nx_for_nomad("NXarpes") + ".ENTRY.DATA.nx_optional", False),
        pytest.param(rename_nx_for_nomad("NXentry") + ".nx_category", "base"),
        pytest.param(
            rename_nx_for_nomad("NXdispersion_table")
            + ".refractive_index__field.nx_type",
            "NX_COMPLEX",
        ),
        pytest.param(
            rename_nx_for_nomad("NXdispersive_material")
            + ".ENTRY.dispersion_x."
            + "DISPERSION_TABLE.refractive_index__field.nx_type",
            "NX_COMPLEX",
        ),
        pytest.param(rename_nx_for_nomad("NXapm") + ".nx_category", "application"),
    ],
)
def test_assert_nexus_metainfo(path: str, value: Any):
    """
    Test the existence of nexus metainfo

    pytest.param('NXdispersive_material.inner_section_definitions[0].sub_sections[1].sub_section.inner_section_definitions[0].quantities[4].more["nx_type"]
    """
    current = nexus_metainfo_package
    for name in path.split("."):
        elements: list = []
        if name.endswith("__field"):
            sub_element_list = getattr(current, "quantities", None)
            if sub_element_list:
                elements += sub_element_list
        else:
            sub_element_list = getattr(current, "section_definitions", None)
            if sub_element_list:
                elements += sub_element_list
            sub_element_list = getattr(current, "sub_sections", None)
            if sub_element_list:
                elements += sub_element_list
            sub_element_list = getattr(current, "attributes", None)
            if sub_element_list:
                elements += sub_element_list
            sub_element_list = current.m_contents()
            if sub_element_list:
                elements += sub_element_list
        for content in elements:
            if getattr(content, "name", None) == name:
                current = content  # type: ignore
                if getattr(current, "sub_section", None):
                    current = current.section_definition
                break
        else:
            current = getattr(current, name, None)
        if current is None:
            assert False, f"{path} does not exist"

    if value == "*":
        assert current is not None, f"{path} does not exist"
    elif value is None:
        assert current is None, f"{path} does exist"
    else:
        assert current == value, f"{path} has wrong value"

    if isinstance(current, Section):
        assert current.nx_kind is not None
        for base_section in current.all_base_sections:
            assert base_section.nx_kind == current.nx_kind
