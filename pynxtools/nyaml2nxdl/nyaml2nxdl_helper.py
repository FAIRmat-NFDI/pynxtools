#!/usr/bin/env python3
"""Main file of yaml2nxdl tool.
Users create NeXus instances by writing a YAML file
which details a hierarchy of data/metadata elements

"""
# -*- coding: utf-8 -*-
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


# Yaml library does not except the keys (escapechar "\t" and yaml separator ":")
# So the corresponding value is to skip them and
# and also carefull about this order
ESCAPE_CHAR_DICT = {":": "\':\'",
                    "\t": "    "}


def get_yaml_escape_char_dict():
    """Get escape char and the way to hide them."""
    return ESCAPE_CHAR_DICT


def get_yaml_escape_char_reverter_dict():
    """To revert yaml escape char in xml constructor from yaml."""
    temp_dict = {}
    for key, val in ESCAPE_CHAR_DICT.items():
        temp_dict[val] = key
    return temp_dict


def type_check(nx_type):
    """
        Check for nexus type if type is NX_CHAR get '' or get as it is.
    """

    if nx_type in ['NX_CHAR', '']:
        nx_type = ''
    else:
        nx_type = f"({nx_type})"
    return nx_type


def get_node_parent_info(tree, node):
    """
    Return tuple of (parent, index) where:
    parent = node of parent within tree
    index = index of node under parent
    """

    parent_map = {c: p for p in tree.iter() for c in p}
    parent = parent_map[node]
    return parent, list(parent).index(node)


def cleaning_empty_lines(line_list):
    """
        Cleaning up empty lines on top and bottom.
    """

    if not isinstance(line_list, list):
        line_list = line_list.split('\n') if '\n' in line_list else ['']

    # Clining up top empty lines
    while True:
        if line_list[0].strip():
            break
        line_list = line_list[1:]
    # Clining bottom empty lines
    while True:
        if line_list[-1].strip():
            break
        line_list = line_list[0:-1]

    return line_list
