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
"""Test for the NeXus app."""

import pytest

try:
    import nomad  # noqa: F401
except ImportError:
    pytest.skip(
        "Skipping NOMAD app tests because nomad-lab is not installed",
        allow_module_level=True,
    )

from pynxtools.nomad.apps import nexus_app


def test_nexus_app_basic_properties():
    """Verify basic metadata of the NeXus app."""
    app = nexus_app.app

    assert app.label == "NeXus"
    assert app.path == "nexusapp"
    assert app.category == "Experiment"


def test_nexus_app_locked_filters():
    """Ensure required locked filters are defined and well-formed."""
    app = nexus_app.app

    assert "section_defs.definition_qualified_name" in app.filters_locked
    assert isinstance(
        app.filters_locked["section_defs.definition_qualified_name"], list
    )
    assert len(app.filters_locked["section_defs.definition_qualified_name"]) == 1


def test_nexus_app_columns():
    """Check that a representative result column is configured correctly."""
    app = nexus_app.app

    definition_column = next(col for col in app.columns if col.title == "Definition")

    assert definition_column.selected is True
    assert "data.ENTRY" in definition_column.search_quantity


def test_nexus_app_menu_contains_elements_section():
    """Validate presence and structure of the Elements menu section."""
    app = nexus_app.app

    elements_menu = next(item for item in app.menu.items if item.title == "Elements")

    assert elements_menu.size.name == "XXL"
    assert any(
        item.__class__.__name__ == "MenuItemPeriodicTable"
        for item in elements_menu.items
    )


def test_nexus_app_dashboard_widgets():
    """Ensure the dashboard contains a valid periodic table widget."""
    dashboard = nexus_app.app.dashboard

    assert len(dashboard.widgets) > 0

    periodic_table = next(w for w in dashboard.widgets if w.type == "periodic_table")
    assert periodic_table.search_quantity == "results.material.elements"
    assert periodic_table.layout
