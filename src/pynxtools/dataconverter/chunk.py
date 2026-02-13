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


# HDF5 data storage layout for HDF5 datasets is "contiguous" unless
# one wraps the payload for a dataconverter template into a dictionary with
# keyword "compress", causing chunked layout to be used

ALLOWED_COMPRESSION_FILTERS = ["gzip"]  # deflate
COMPRESSION_STRENGTH = 9
# integer values from 0 (effectively no), 1, ..., to at most 9 (strongest compression)
# using strongest compression is space efficient but can take substantially longer than
# using 1

# compressed payload is served as a dict with at least one keyword "compress",
# "strength" is optional keyword for that dictionary to overwrite the default
# COMPRESSION_STRENGTH
