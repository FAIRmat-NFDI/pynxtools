# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
from pynxtools.nomad.apps.app_v2 import nexus_app_v2, schema


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


# ---------------------------------------------------------------------------
# App v2 configuration
# ---------------------------------------------------------------------------


def test_nexus_app_v2_schema():
    """App v2 must reference the correct Entry class."""
    assert schema == "pynxtools.nomad.metainfo.base_classes.Entry"
    filters = nexus_app_v2.app.filters_locked
    assert "section_defs.definition_qualified_name" in filters
    assert filters["section_defs.definition_qualified_name"] == [schema]


def test_nexus_app_v2_basic_properties():
    """App v2 must have correct label, path, and category."""
    app = nexus_app_v2.app
    assert app.label == "NeXus v2"
    assert app.path == "nexusappv2"
    assert app.category == "Experiment"


def test_nexus_app_v2_locked_filters():
    """Ensure required locked filters are defined and well-formed."""
    app = nexus_app_v2.app

    assert "section_defs.definition_qualified_name" in app.filters_locked
    assert isinstance(
        app.filters_locked["section_defs.definition_qualified_name"], list
    )
    assert len(app.filters_locked["section_defs.definition_qualified_name"]) == 1


def test_nexus_app_v2_columns():
    """Check that a representative result column is configured correctly."""
    app = nexus_app_v2.app

    definition_column = next(col for col in app.columns if col.title == "Definition")

    assert definition_column.selected is True
    print(definition_column.search_quantity)
    assert "data.definition" in definition_column.search_quantity


def test_nexus_app_v2_menu_contains_elements_section():
    """Validate presence and structure of the Elements menu section."""
    app = nexus_app_v2.app

    elements_menu = next(item for item in app.menu.items if item.title == "Elements")

    assert elements_menu.size.name == "XXL"
    assert any(
        item.__class__.__name__ == "MenuItemPeriodicTable"
        for item in elements_menu.items
    )


def test_nexus_app_v2_dashboard_widgets():
    """Ensure the dashboard contains a valid periodic table widget."""
    dashboard = nexus_app.app.dashboard

    assert len(dashboard.widgets) > 0

    periodic_table = next(w for w in dashboard.widgets if w.type == "periodic_table")
    assert periodic_table.search_quantity == "results.material.elements"
    assert periodic_table.layout


def test_nexus_app_v2_search_quantities_resolve():
    """Every column/menu-item/dashboard-widget path qualified with our own
    schema must resolve to a real quantity or subsection on Entry."""
    from pynxtools.nomad.metainfo.base_classes.entry import Entry

    suffix = f"#{schema}"

    def resolves(path: str) -> bool:
        """Walk a "data.xyz[*].abc" search_quantity path against the Entry's own
        metainfo definition, following subsections and stripping `[*]`."""
        # `path` is relative to the archive ("data.xyz").
        segments = path.split(".")
        assert segments[0] == "data"
        cls = Entry
        for segment in segments[1:]:
            if cls is None:
                return False
            name = segment[:-3] if segment.endswith("[*]") else segment
            m_def = cls.m_def
            if name in m_def.all_sub_sections:
                cls = m_def.all_sub_sections[name].sub_section.section_cls
            elif name in m_def.all_quantities:
                cls = None
            else:
                return False
        return True

    def as_quantity_str(value) -> str | None:
        """MenuItemTerms.search_quantity is a plain str; MenuItemHistogram.x is
        an Axis wrapping one in its own `.search_quantity` field."""
        if isinstance(value, str):
            return value
        return getattr(value, "search_quantity", None)

    def menu_paths(items) -> list[str]:
        """Collect search_quantity paths from a Menu's items,
        recursing into nested Menus."""
        found = []
        for item in items:
            search_quantity = as_quantity_str(
                getattr(item, "search_quantity", None)
            ) or as_quantity_str(getattr(item, "x", None))
            if search_quantity and search_quantity.endswith(suffix):
                found.append(search_quantity[: -len(suffix)])
            nested = getattr(item, "items", None)
            if nested:
                found.extend(menu_paths(nested))
        return found

    app = nexus_app_v2.app
    paths = [
        col.search_quantity[: -len(suffix)]
        for col in app.columns
        if col.search_quantity and col.search_quantity.endswith(suffix)
    ]
    paths.extend(menu_paths(app.menu.items))
    paths.extend(
        w.search_quantity[: -len(suffix)]
        for w in app.dashboard.widgets
        if w.search_quantity and w.search_quantity.endswith(suffix)
    )

    assert paths, "expected at least one schema-qualified search_quantity"
    unresolved = [p for p in paths if not resolves(p)]
    assert not unresolved, f"unresolved search_quantity paths: {unresolved}"
