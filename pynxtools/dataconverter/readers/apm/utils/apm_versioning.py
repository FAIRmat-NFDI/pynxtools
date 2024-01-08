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


NX_APM_ADEF_NAME = "NXapm"
NX_APM_ADEF_VERSION = "nexus-fairmat-proposal successor of " \
                      "9636feecb79bb32b828b1a9804269573256d7696"
# based on https://fairmat-experimental.github.io/nexus-fairmat-proposal
NX_APM_EXEC_NAME = "pynxtools/dataconverter/readers/apm/reader.py"
NX_APM_EXEC_VERSION = get_repo_last_commit()

# numerics
MASS_SPECTRUM_DEFAULT_BINNING = 0.01  # u
NAIVE_GRID_DEFAULT_VOXEL_SIZE = 1.  # nm
