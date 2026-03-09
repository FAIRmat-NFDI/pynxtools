"""
Public API for the pynxtools.nexus package.

Primary entry points:

* `NexusFileHandler` – walks a NeXus/HDF5 file and dispatches each node to a
  `NexusVisitor` implementation.
* `NexusVisitor` – base class for visitor implementations.
* `Annotator` – annotates every node with NXDL documentation
  (used by the ``read_nexus`` CLI).
"""
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

from pynxtools.nexus.annotation import Annotator
from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor

__all__ = [
    "NexusFileHandler",
    "NexusVisitor",
    "Annotator",
]
