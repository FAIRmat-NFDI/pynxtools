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
"""Configuration of the image_tiff_tfs subparser."""


TfsToNexusConceptMapping = {"System/Source/FEG": "cold_field_cathode_emitter"}


# "/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/start_time"
TIFF_TFS_TO_NEXUS_CFG = [('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/DETECTOR[detector*]/mode', 'load_from', 'Detectors/Mode'),
                         ('/ENTRY[entry*]/measurement/em_lab/DETECTOR[detector*]/local_name', 'load_from', 'Detectors/Name'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/APERTURE_EM[aperture_em*]/description', 'load_from', 'EBeam/Aperture'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/APERTURE_EM[aperture_em*]/value', 'load_from', 'EBeam/ApertureDiameter'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/APERTURE_EM[aperture_em*]/value/@units', 'm'),
                         ('/ENTRY[entry*]/measurement/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/beam_current', 'load_from', 'EBeam/BeamCurrent'),
                         ('/ENTRY[entry*]/measurement/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/beam_current/@units', 'A'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage', 'load_from', 'EBeam/HV'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage/@units', 'V'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_1', 'load_from_rad_to_deg', 'EBeam/StageTa'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_1/@units', 'deg'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_2', 'load_from_rad_to_deg', 'EBeam/StageTb'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_2/@units', 'deg'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/EBEAM_COLUMN[ebeam_column]/operation_mode', 'load_from', 'EBeam/UseCase'),
                         ('/ENTRY[entry*]/measurement/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/working_distance', 'load_from', 'EBeam/WD'),
                         ('/ENTRY[entry*]/measurement/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/working_distance/@units', 'm'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/event_type', 'load_from_lower_case', 'ETD/Signal'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/SCANBOX_EM[scanbox_em]/dwell_time', 'load_from', 'Scan/Dwelltime'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/SCANBOX_EM[scanbox_em]/dwell_time/@units', 's'),
                         ('/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/identifier', 'load_from', 'System/BuildNr'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/SCANBOX_EM[scanbox_em]/scan_schema', 'load_from', 'System/Scan'),
                         ('/ENTRY[entry*]/measurement/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/emitter_type', 'load_from', 'System/Source'),
                         ('/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/vendor', 'FEI'),
                         ('/ENTRY[entry*]/measurement/em_lab/FABRICATION[fabrication]/model', 'load_from', 'System/SystemType'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/event_type', 'load_from_lower_case', 'T1/Signal'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/event_type', 'load_from_lower_case', 'T2/Signal'),
                         ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/event_type', 'load_from_lower_case', 'T3/Signal')]
