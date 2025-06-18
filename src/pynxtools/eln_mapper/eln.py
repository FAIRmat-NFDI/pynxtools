"""Define general structure of the ELN mapper."""

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

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Optional

import yaml

from pynxtools.dataconverter.helpers import convert_data_converter_dict_to_nxdl_path
from pynxtools.dataconverter.nexus_tree import (
    NexusEntity,
    NexusGroup,
    NexusNode,
    generate_tree_from,
)

logger = logging.getLogger("pynxtools")

NODES_TO_SKIP: list[str] = ["definition"]


def clean_filters(filter_list: Optional[list[str]]) -> Optional[list[str]]:
    """
    Clean list of filters by converting keys from data converter style path"
    to NXDL style path:
    /ENTRY[entry]/sample -> /ENTRY/sample
    """
    if filter_list is None:
        return None
    return [convert_data_converter_dict_to_nxdl_path(key) for key in filter_list]


def _should_skip_iteration(node: NexusNode, filter_list: Optional[list[str]]) -> bool:
    """Filter those nodes that are _not_ in filter_list.

    Parameters
    ----------
    node : NexusNode
        The node to investigate.
    """
    if filter_list is None:
        return False
    if node.get_path() in filter_list:
        return False
    return True


class ElnGenerator(ABC):
    def __init__(
        self,
        nxdl: str,
        output_file: Optional[str] = None,
        skip_top_levels: int = 0,
        optionality: Optional[str] = "required",
        filter: Optional[list[str]] = None,
    ) -> None:
        self.nxdl = nxdl
        self.output_file = output_file
        self.skip_top_levels = skip_top_levels
        self.optionality = optionality
        self.filter = clean_filters(filter)

        self.out_file = self._generate_output_file_name(output_file)
        self.recursive_dict: dict[str, Any] = {}

        if self.skip_top_levels == 1:
            logger.warning(
                f"The first level below NXentry of the NeXus tree "
                "are skipped, is this intentional?"
            )
        elif self.skip_top_levels > 1:
            logger.warning(
                f"The first {self.skip_top_levels - 1} levels of the NeXus tree "
                "are skipped, is this intentional?"
            )

    @abstractmethod
    def _generate_output_file_name(self, output_file: str):
        """
        Generate the output file name of the schema ELN generator.

        To be implemented by the different subclasses of ElnGenerator.
        """
        return ""

    def _generate_eln_header(self) -> dict:
        """
        Generate a header for YAML ELN.

        Returns the header section of the ELN, which is to be filled from
        the application definition.
        To be implemented by the different subclasses of ElnGenerator.
        """
        return self.recursive_dict

    @abstractmethod
    def _construct_group_structure(
        self,
        node: NexusGroup,
        recursive_dict: dict,
        recursion_level: int,
    ) -> bool:
        """
        Handle NeXus group.

        To be extended by the different subclasses of ElnGenerator. The return value indicates
        where the subclass should continue with this function after the super() call.
        """
        # Skip top levels in iteration
        if recursion_level <= self.skip_top_levels:
            self._recurse_tree(node, recursive_dict, recursion_level + 1)
            return False  # early exit

        if self.filter is not None and all(
            _should_skip_iteration(child, self.filter) for child in node.children
        ):
            if not node.children or not all(
                [child.type == "group" for child in node.children]
            ):
                self._recurse_tree(node, recursive_dict, recursion_level)
                return False  # early exit

        return True

    @abstractmethod
    def _construct_entity_structure(
        self, node: NexusEntity, recursive_dict: dict, recursion_level: int
    ) -> bool:
        """Handle NeXus field or attribute.

        To be extended by the different subclasses of ElnGenerator. The return value indicates
        where the subclass should continue with this function after the super() call.
        """
        # Skip top levels in iteration
        if recursion_level <= self.skip_top_levels:
            self._recurse_tree(node, recursive_dict, recursion_level + 1)
            return False  # early exit

        if self.filter is not None and _should_skip_iteration(node, self.filter):
            self._recurse_tree(node, recursive_dict, recursion_level + 1)
            return False  # early exit

        return True

    def _recurse_tree(
        self, node: NexusNode, recursive_dict: dict, recursion_level: int
    ) -> None:
        """Recurse the NeXus node and add the parsed elements to the recursive dict.

        Parameters
        ----------
        node : NexusNode
            NeXus node to recurse.
        recursive_dict : dict
            A dict that store hierarchical structure of schema ELN.
        recursion_level: int
            Recursion level in the tree, used to (optionally) skip upper levels like NXentry
        """

        def _handle_unknown_type(
            node: NexusNode, section_dict: dict, recursion_level: int
        ):
            # This should normally not happen if
            # the handling map includes all types allowed in NexusNode.type
            # Still, it's good to have a fallback
            # TODO: Raise error or log the issue?
            pass

        handling_map = {
            "group": self._construct_group_structure,
            "field": self._construct_entity_structure,
            "attribute": self._construct_entity_structure,
        }

        lvl_map = {
            "required": ("required",),
            "recommended": ("recommended", "required"),
            "optional": ("optional", "recommended", "required"),
        }

        for child in node.children:
            if child.name in NODES_TO_SKIP:
                continue
            if child.optionality not in lvl_map[self.optionality]:
                continue

            handling_map.get(child.type, _handle_unknown_type)(
                child, recursive_dict, recursion_level
            )

    def _write_yaml(self):
        """Write the final dict into a YAML file"""
        with open(self.out_file, mode="w", encoding="utf-8") as out_f:
            yaml.dump(self.recursive_dict, sort_keys=False, stream=out_f)
        logger.info(f"Schema ELN file {self.out_file} was created successfully.")

    def generate_eln(self) -> None:
        """Generate ELN file."""
        tree = generate_tree_from(self.nxdl, set_root_attr=False)

        top_level_section = self._generate_eln_header()
        self._recurse_tree(tree, top_level_section, recursion_level=0)
        if not self.recursive_dict:
            logger.error("Could not write YAML file as it would be empty!")
            return
        self._write_yaml()
