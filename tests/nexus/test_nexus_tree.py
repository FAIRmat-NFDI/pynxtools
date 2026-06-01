from typing import Any, get_args

import pytest
from anytree import Resolver

from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_app_defs_names,
    get_nx_attribute_type,
    get_nx_units,
)
from pynxtools.nexus.nexus_tree import (
    NexusChoice,
    NexusNode,
    NexusType,
    NexusUnitCategory,
    generate_tree_from,
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


# ---------------------------------------------------------------------------
# NexusChoice resolution tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "nx_class,expected_nx_class",
    [
        ("NXoff_geometry", "NXoff_geometry"),
        ("NXcylindrical_geometry", "NXcylindrical_geometry"),
        (None, "NXoff_geometry"),  # no nx_class hint → first child
    ],
)
def test_best_child_for_choice_with_group_type(nx_class, expected_nx_class):
    """best_child_for with node_type='group' descends into NexusChoice."""
    tree = generate_tree_from("NXdetector")
    result = tree.best_child_for("pixel_shape", node_type="group", nx_class=nx_class)
    assert result is not None, f"Expected a node for nx_class={nx_class!r}"
    assert not isinstance(result, NexusChoice), "Must not return the choice itself"
    assert result.nx_type == "group"
    assert getattr(result, "nx_class", None) == expected_nx_class


def test_best_child_for_choice_without_type_filter():
    """best_child_for with no node_type filter also descends into NexusChoice."""
    tree = generate_tree_from("NXdetector")
    result = tree.best_child_for("pixel_shape")
    assert result is not None
    assert not isinstance(result, NexusChoice)
    assert result.nx_type == "group"


def test_required_groups_does_not_include_choice_alternatives():
    """required_groups must not add both alternatives of a choice as individually required."""
    tree = generate_tree_from("NXdetector")
    req = tree.required_groups()
    # pixel_shape and detector_shape are optional choices; neither alternative should appear
    assert not any("pixel_shape" in r or "detector_shape" in r for r in req)
