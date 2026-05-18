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

# Backwards compatibility: helpers.validate_data_dict is defined directly in helpers.py as a lazy
# forwarder to break the circular import that would arise from an eager import here:
#   nexus.nexus_tree → dataconverter.helpers → (this __init__) → validation → nexus.nexus_tree
# Call _apply_monkey_patch() if the real function object is needed (e.g. identity checks).


def _apply_monkey_patch() -> None:
    """Replace the lazy forwarder with the real validate_data_dict from validation."""
    from pynxtools.dataconverter import helpers, validation

    helpers.validate_data_dict = validation.validate_data_dict  # type: ignore
