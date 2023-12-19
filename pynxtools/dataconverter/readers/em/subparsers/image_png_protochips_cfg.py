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
"""Configuration of the image_png_protochips subparser."""


PNG_PROTOCHIPS_TO_NEXUS_CFG = [('/ENTRY[entry*]/measurement/em_lab/STAGE_LAB[stage_lab]/alias', 'load_from', 'MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.Name'),
                               ('/ENTRY[entry*]/measurement/em_lab/STAGE_LAB[stage_lab]/design', 'heating_chip'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_1', 'load_from', 'MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.A'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/tilt_2', 'load_from', 'MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.B'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/position', 'load_from_concatenate', ['MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.X',
                                                                                                                                                                                                'MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.Y',
                                                                                                                                                                                                'MicroscopeControlImageMetadata.ActivePositionerSettings.PositionerSettings.[*].Stage.Z']),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/current', 'load_from', 'MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HeatingCurrent'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/current/@units', 'A'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/power', 'load_from', 'MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HeatingPower'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/power/@units', 'W'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/voltage', 'load_from', 'MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HeatingVoltage'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/HEATER[heater]/voltage/@units', 'V'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor2]/value', 'load_from', 'MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HolderPressure'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor2]/value/@units', 'torr'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor2]/measurement', 'pressure'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor1]/value', 'load_from', 'MicroscopeControlImageMetadata.AuxiliaryData.AuxiliaryDataCategory.[*].DataValues.AuxiliaryDataValue.[*].HolderTemperature'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor1]/value/@units', '°C'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/STAGE_LAB[stage_lab]/SENSOR[sensor1]/measurement', 'temperature'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/EBEAM_COLUMN[ebeam_column]/electron_source/voltage', 'load_from', 'MicroscopeControlImageMetadata.MicroscopeSettings.AcceleratingVoltage'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/EBEAM_COLUMN[ebeam_column]/DEFLECTOR[beam_blanker1]/state', 'load_from', 'MicroscopeControlImageMetadata.MicroscopeSettings.BeamBlankerState'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/camera_length', 'load_from', 'MicroscopeControlImageMetadata.MicroscopeSettings.CameraLengthValue'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/magnification', 'load_from', 'MicroscopeControlImageMetadata.MicroscopeSettings.MagnificationValue'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/event_type', 'As tested with AXON 10.4.4.21, 2021-04-26T22:51:28.4539893-05:00 not included in Protochips PNG metadata'),
                               ('/ENTRY[entry*]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/EVENT_DATA_EM[event_data_em*]/em_lab/DETECTOR[detector*]/mode', 'As tested with AXON 10.4.4.21, 2021-04-26T22:51:28.4539893-05:00 not included in Protochips PNG metadata'),
                               ('/ENTRY[entry*]/measurement/em_lab/DETECTOR[detector*]/local_name', 'As tested with AXON 10.4.4.21, 2021-04-26T22:51:28.4539893-05:00 not included in Protochips PNG metadata')]
