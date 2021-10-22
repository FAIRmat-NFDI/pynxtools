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

from nomad.metainfo import Section, Quantity, Package

from nomad.datamodel.metainfo.public import section_single_configuration_calculation as SCC


m_package = Package(
    name='nexus_nomadmetainfo_json',
    description='None')


# We extend the existing common definition of a section "single configuration calculation"
class NexusSCC(SCC):
    # We alter the default base class behavior to add all definitions to the existing
    # base class instead of inheriting from the base class
    m_def = Section(extends_base_section=True)

    # We define an additional nexus quantity. Use the prefix x_<parsername>_ to denote
    # non common quantities.
    x_nexus_magic_value = Quantity(type=int, description='The magic value from a magic source.')


m_package.__init_metainfo__()
