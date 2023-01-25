#!/usr/bin/env python3
"""Set of utility tools for parsing file formats used by electron microscopy."""

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

# pylint: disable=E1101

import git


def get_repo_last_commit() -> str:
    """Identify the last commit to the repository."""
    repo = git.Repo(search_parent_directories=True)
    sha = str(repo.head.object.hexsha)
    if sha != "":
        return sha
    return "unknown git commit id or unable to parse git reverse head"
