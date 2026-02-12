from typing import Any, get_args

from anytree import Resolver

from pynxtools.dataconverter.nexus_tree import (
    NexusNode,
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


def test_correct_extension_of_tree():
    nxtest = generate_tree_from("NXtest")
    nxtest_extended = generate_tree_from("NXtest_extended")

    def get_node_fields(tree: NexusNode) -> list[tuple[str, Any]]:
        return list(
            filter(
                lambda x: (
                    not x[0].startswith("_")
                    and x[0] not in ("inheritance", "is_a", "parent_of", "nxdl_base")
                ),
                tree.__dict__.items(),
            )
        )

    def left_tree_in_right_tree(left_tree, right_tree):
        for left_child in left_tree.children:
            if left_child.name not in map(lambda x: x.name, right_tree.children):
                return False
            right_child = list(
                filter(lambda x: x.name == left_child.name, right_tree.children)
            )[0]
            if left_child.name == "definition":
                # Definition should be overwritten
                if not left_child.items == ["NXTEST", "NXtest"]:
                    return False
                if not right_child.items == ["NXtest_extended"]:
                    return False
                continue
            for field in get_node_fields(left_child):
                if field not in get_node_fields(right_child):
                    return False
            if not left_tree_in_right_tree(left_child, right_child):
                return False
        return True

    assert left_tree_in_right_tree(nxtest, nxtest_extended)

    resolver = Resolver("name", relax=True)
    extended_field = resolver.get(nxtest_extended, "ENTRY/extended_field")
    assert extended_field is not None
    assert extended_field.unit == "NX_ENERGY"
    assert extended_field.dtype == "NX_FLOAT"
    assert extended_field.optionality == "required"

    nxtest_field = resolver.get(nxtest, "ENTRY/extended_field")
    assert nxtest_field is None
