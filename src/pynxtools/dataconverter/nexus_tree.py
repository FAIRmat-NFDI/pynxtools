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
"""
Re-export shim for backward compatibility.

The canonical location for `NexusNode` and friends is now
`pynxtools.nexus.nexus_tree`.  Import from there in new code.

TODO: This shim exists only to avoid breaking external callers that import from
`pynxtools.dataconverter.nexus_tree`.  It should be removed in future versions
of the package.
"""

# ruff: noqa: F401
from pynxtools.nexus.nexus_tree import (
    NexusChoice,
    NexusEntity,
    NexusGroup,
    NexusNode,
    NexusType,
    NexusUnitCategory,
    generate_tree_from,
    populate_tree_from_parents,
)
