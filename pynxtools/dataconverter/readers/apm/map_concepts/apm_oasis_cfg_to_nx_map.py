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
"""Dict mapping values for a specifically configured NOMAD OASIS."""

# pylint: disable=line-too-long

# currently by virtue of design NOMAD OASIS specific examples show how different tools and
# services can be specifically coupled and implemented so that they work together
# currently we assume that the ELN provides all those pieces of information to instantiate
# a NeXus data artifact which technology-partner-specific files or database blobs can not
# deliver. Effectively a reader uses the eln_data.yaml generic ELN output to fill in these
# missing pieces of information while typically heavy data (tensors etc) are translated
# and written from the technology-partner files
# for large application definitions this can lead to a practical inconvenience:
# the ELN that has to be exposed to the user is complex and has many fields to fill in
# just to assure that all information are included in the ELN output and thus consumable
# by the dataconverter
# taking the perspective of a specific lab where a specific version of an ELN provided by
# or running in addition to NOMAD OASIS is used many pieces of information might not change
# or administrators do not wish to expose this via the end user ELN in an effort to reduce
# the complexity for end users and make entering of repetitiv information obsolete

# this is the scenario for which deployment_specific mapping shines
# parsing of deployment specific details in the apm reader is currently implemented
# such that it executes after reading generic ELN data (eventually available entries)
# in the template get overwritten

import datetime as dt

from pynxtools.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_ADEF_NAME, NX_APM_ADEF_VERSION


APM_OASIS_TO_NEXUS_CFG \
    = [("/ENTRY[entry*]/@version", f"{NX_APM_ADEF_VERSION}"),
       ("/ENTRY[entry*]/definition", f"{NX_APM_ADEF_NAME}"),
       ("/ENTRY[entry*]/operation_mode", "ignore", "operation_mode"),
       ("/ENTRY[entry*]/start_time", f"{dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')}")]


APM_PARAPROBE_EXAMPLE_TO_NEXUS_CFG \
    = [("/ENTRY[entry*]/CITE[cite*]/doi", "load_from", "doi"),
       ("/ENTRY[entry*]/CITE[cite*]/description", "load_from", "description")]
