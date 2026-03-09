#
# Copyright The pynxtools Authors.
#
# This file is part of pynxtools.
# See https://github.com/FAIRmat-NFDI/pynxtools for further info.
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
