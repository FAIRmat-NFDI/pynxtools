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
"""Utility tool constants and versioning."""

# pylint: disable=no-member

from pynxtools.dataconverter.readers.shared.shared_utils \
    import get_repo_last_commit


NX_EM_NION_ADEF_NAME = "NXem"
NX_EM_NION_ADEF_VERSION = "nexus-fairmat-proposal successor of " \
                          "9636feecb79bb32b828b1a9804269573256d7696"
# based on https://fairmat-experimental.github.io/nexus-fairmat-proposal
NX_EM_NION_EXEC_NAME = "dataconverter/reader/em_nion/reader.py"
NX_EM_NION_EXEC_VERSION = get_repo_last_commit()

NX_EM_NION_SWIFT_NAME = "nionswift"
NX_EM_NION_SWIFT_VERSION = "0.16.8"
