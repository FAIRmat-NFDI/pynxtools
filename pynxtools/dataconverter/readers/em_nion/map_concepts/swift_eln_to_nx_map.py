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
"""Dict mapping custom schema instances from eln_data.yaml file on concepts in NXem."""

# pylint: disable=no-member,line-too-long

# releasing line-too-long restriction to avoid having line breaks in the mapping table
# made the experience that when having a widescreen working with the mapping table
# as single-line instructions is more convenient to read and parsable by human eye

# there are several issues with the current design of how data from the eln_data.yaml are passed
# some quantities from a custom schema instance end up as list of dictionaries, like here
# aperture and user, however in this mapping approach they would demand concept-specific
# modifiers to be picked up by, currently the em_spctrscpy, em_om, apm examples individually
# parse relevant quantities for each section which makes the code difficult to read and
# unnecessarily lengthy, with em_nion we would like to test if instead we can use
# a set of mapping tables whereby to read content from a custom schema instance eln_data.yaml
# results file directly into the template which the em_nion reader has to fill and pass
# then to the data converter

NxEmElnInput = {"IGNORE": {"fun": "load_from_dict_list", "terms": "em_lab/detector"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/ebeam_column/aberration_correction/applied"},
                "IGNORE": {"fun": "load_from_dict_list", "terms": "em_lab/ebeam_column/aperture_em"},
                "/ENTRY[entry*]/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/emitter_type": {"fun": "load_from", "terms": "em_lab/ebeam_column/electron_source/emitter_type"},
                "/ENTRY[entry*]/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage/@units": {"fun": "load_from", "terms": "em_lab/ebeam_column/electron_source/voltage/unit"},
                "/ENTRY[entry*]/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage": {"fun": "load_from", "terms": "em_lab/ebeam_column/electron_source/voltage/value"},
                "/ENTRY[entry*]/em_lab/FABRICATION[fabrication]/capabilities": {"fun": "load_from", "terms": "em_lab/fabrication/capabilities"},
                "/ENTRY[entry*]/em_lab/FABRICATION[fabrication]/identifier": {"fun": "load_from", "terms": "em_lab/fabrication/identifier"},
                "/ENTRY[entry*]/em_lab/FABRICATION[fabrication]/model": {"fun": "load_from", "terms": "em_lab/fabrication/model"},
                "/ENTRY[entry*]/em_lab/FABRICATION[fabrication]/vendor": {"fun": "load_from", "terms": "em_lab/fabrication/vendor"},
                "/ENTRY[entry*]/em_lab/instrument_name": {"fun": "load_from", "terms": "em_lab/instrument_name"},
                "/ENTRY[entry*]/em_lab/location": {"fun": "load_from", "terms": "em_lab/location"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/beam_current/unit"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/beam_current/value"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/beam_current_description"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/magnification"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/semi_convergence_angle/unit"},
                "IGNORE": {"fun": "load_from", "terms": "em_lab/optical_system_em/semi_convergence_angle/value"},
                "/ENTRY[entry*]/em_lab/stage_lab/description": {"fun": "load_from", "terms": "em_lab/stage_lab/description"},
                "/ENTRY[entry*]/em_lab/stage_lab/name": {"fun": "load_from", "terms": "em_lab/stage_lab/name"},
                "/ENTRY[entry*]/@version": {"fun": "load_from", "terms": "entry/attr_version"},
                "/ENTRY[entry*]/definition": {"fun": "load_from", "terms": "entry/definition"},
                "/ENTRY[entry*]/end_time": {"fun": "load_from", "terms": "entry/end_time"},
                "/ENTRY[entry*]/experiment_description": {"fun": "load_from", "terms": "entry/experiment_description"},
                "/ENTRY[entry*]/experiment_identifier": {"fun": "load_from", "terms": "entry/experiment_identifier"},
                "/ENTRY[entry*]/PROGRAM[program*]/program": {"fun": "load_from", "terms": "entry/program"},
                "/ENTRY[entry*]/PROGRAM[program*]/program/@version": {"fun": "load_from", "terms": "entry/program__attr_version"},
                "/ENTRY[entry*]/start_time": {"fun": "load_from", "terms": "entry/start_time"},
                "IGNORE": {"fun": "load_from_list_of_dict", "terms": "user"}}

# NeXus concept specific mapping tables which require special treatment as the current
# NOMAD OASIS custom schema implementation delivers them as a list of dictionaries instead
# of a directly flattenable list of keyword, value pairs

NxApertureEmFromListOfDict = {"/ENTRY[entry*]/em_lab/EBEAM_COLUMN[ebeam_column]/APERTURE_EM[aperture_em*]/name": {"fun": "load_from", "terms": "name"},
                              "/ENTRY[entry*]/em_lab/EBEAM_COLUMN[ebeam_column]/APERTURE_EM[aperture_em*]/value": {"fun": "load_from", "terms": "value"}}

NxUserFromListOfDict = {"/ENTRY[entry*]/USER[user*]/name": {"fun": "load_from", "terms": "name"},
                        "/ENTRY[entry*]/USER[user*]/affiliation": {"fun": "load_from", "terms": "affiliation"},
                        "/ENTRY[entry*]/USER[user*]/address": {"fun": "load_from", "terms": "address"},
                        "/ENTRY[entry*]/USER[user*]/email": {"fun": "load_from", "terms": "email"},
                        "/ENTRY[entry*]/USER[user*]/orcid": {"fun": "load_from", "terms": "orcid"},
                        "/ENTRY[entry*]/USER[user*]/orcid_platform": {"fun": "load_from", "terms": "orcid_platform"},
                        "/ENTRY[entry*]/USER[user*]/telephone_number": {"fun": "load_from", "terms": "telephone_number"},
                        "/ENTRY[entry*]/USER[user*]/role": {"fun": "load_from", "terms": "role"},
                        "/ENTRY[entry*]/USER[user*]/social_media_name": {"fun": "load_from", "terms": "social_media_name"},
                        "/ENTRY[entry*]/USER[user*]/social_media_platform": {"fun": "load_from", "terms": "social_media_platform"}}

NxDetectorListOfDict = {"/ENTRY[entry*]/em_lab/DETECTOR[detector*]/local_name": {"fun": "load_from", "terms": "local_name"}}

# atom_types is a good example for specific cases where one cannot just blindly map
# the list that comes from the custom schema ELN instance, because
# people may enter invalid types of atoms (which would generate problems in NOMAD OASIS)
# and for NeXus we would like to have a "string of a comma-separated list of element names"

NxSample = {"IGNORE": {"fun": "load_from", "terms": "sample/atom_types"},
            "/ENTRY[entry*]/sample/description": {"fun": "load_from", "terms": "sample/description"},
            "/ENTRY[entry*]/sample/method": {"fun": "load_from", "terms": "sample/method"},
            "/ENTRY[entry*]/sample/name": {"fun": "load_from", "terms": "sample/name"},
            "/ENTRY[entry*]/sample/preparation_date": {"fun": "load_from", "terms": "sample/preparation_date"},
            "/ENTRY[entry*]/sample/sample_history": {"fun": "load_from", "terms": "sample/sample_history"},
            "/ENTRY[entry*]/sample/short_title": {"fun": "load_from", "terms": "sample/short_title"},
            "/ENTRY[entry*]/sample/thickness": {"fun": "load_from", "terms": "sample/thickness/value"},
            "/ENTRY[entry*]/sample/thickness/@units": {"fun": "load_from", "terms": "sample/thickness/unit"}}
