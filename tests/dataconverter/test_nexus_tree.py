from typing import get_args

from pynxtools.dataconverter.nexus_tree import (
    NexusType,
    NexusUnitCategory,
    generate_tree_from,
)
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_app_defs_names,
    get_nx_attribute_type,
    get_nx_units,
)


def test_parsing_of_all_appdefs():
    """All appdefs are parsed to a tree without raising an error"""
    appdefs = get_app_defs_names()
    for appdef in appdefs:
        generate_tree_from(appdef)


def test_if_all_units_are_present():
    reference_units = get_nx_units()
    pydantic_literal_values = get_args(NexusUnitCategory)

    assert set(reference_units) == set(pydantic_literal_values)


def test_if_all_types_are_present():
    reference_types = get_nx_attribute_type()
    pydantic_literal_values = get_args(NexusType)

    assert set(reference_types) == set(pydantic_literal_values)
