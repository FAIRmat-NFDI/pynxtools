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
"""Test cases for template class for the DataConverter"""

from .test_helpers import fixture_template  # pylint: disable=unused-import


def test_rename_entry(template):
    """Unit test for the rename entry function"""
    template.rename_entry("entry", "newentry")
    assert "/ENTRY[entry]/program_name" not in template.keys()


def test_add_entry(template):
    """Unit test for adding an entry to the template class."""
    template.add_entry("test_entry")
    assert "/ENTRY[entry]/program_name" in template.keys()
    assert "/ENTRY[test_entry]/program_name" in template.keys()
