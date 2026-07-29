# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Test cases for template class for the DataConverter"""

from .test_helpers import fixture_template  # pylint: disable=unused-import


def test_rename_entry(template):
    """Unit test for the rename entry function"""
    template.rename_entry("entry", "new_entry")
    assert "/ENTRY[entry]/program_name" not in template.keys()


def test_add_entry(template):
    """Unit test for adding an entry to the template class."""
    template.add_entry("test_entry")
    assert "/ENTRY[entry]/program_name" in template.keys()
    assert "/ENTRY[test_entry]/program_name" in template.keys()
