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
"""Configuration defaults of the dataconverter."""

COMPRESSION_FILTER = "gzip"  # deflate
COMPRESSION_STRENGTH = 9  # strongest compression is space efficient but can take long

# compressed payload is served as a dict with at least one keyword "compress",
# optional keywords that can be used to overwrite defaults are "filter", and "strength"
