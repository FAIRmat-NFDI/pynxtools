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
"""Set of utility tools for parsing file formats used by atom probe."""

# pylint: disable=E1101

# ifes_apt_tc_data_modeling replaces now the previously here stored
# convenience functions which translated human-readable ion names into
# isotope_vector descriptions and vice versa as proposed by M. Kuehbach et al. in
# DOI: 10.1017/S1431927621012241 to the human-readable ion names which are use
# in P. Felfer et al."s atom probe toolbox
