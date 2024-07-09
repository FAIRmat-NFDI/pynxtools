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

import os
import re
from datetime import datetime

from pynxtools._build_wrapper import get_vcs_version
from pynxtools.definitions.dev_tools.globals.nxdl import get_nxdl_version

MAIN_BRANCH_NAME = "fairmat"


def _build_version(tag: str, distance: int, node: str, dirty: bool) -> str:
    """
    Builds the version string for a given set of git states.
    This resembles `no-guess-dev` + `node-and-date` behavior from setuptools_scm.
    """
    if distance == 0 and not dirty:
        return f"{tag}"

    dirty_appendix = datetime.now().strftime(".d%Y%m%d") if dirty else ""
    return f"{tag}.post1.dev{distance}+{node}{dirty_appendix}"


def format_version(version: str) -> str:
    """
    Formats the git describe version string into the local format.
    """
    version_parts = version.split("-")

    return _build_version(
        version_parts[0],
        int(version_parts[1]),
        version_parts[2],
        len(version_parts) == 4 and version_parts[3] == "dirty",
    )


def get_nexus_version() -> str:
    """
    The version of the Nexus standard and the NeXus Definition language
    based on git tags and commits
    """
    version = get_vcs_version()

    if version is not None:
        return format_version(version)

    version_file = os.path.join(os.path.dirname(__file__), "nexus-version.txt")

    if not os.path.exists(version_file):
        # We are in the limbo, just get the nxdl version from nexus definitions
        return format_version(get_nxdl_version())

    with open(version_file, encoding="utf-8") as vfile:
        return format_version(vfile.read().strip())


def get_nexus_version_hash() -> str:
    """
    Gets the git hash from the nexus version string
    """
    version = re.search(r"g([a-z0-9]+)", get_nexus_version())

    if version is None:
        return MAIN_BRANCH_NAME

    return version.group(1)
