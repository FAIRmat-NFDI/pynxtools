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
"""Dict mapping custom schema instances from eln_data.yaml file on concepts in NXapm."""

NxApmElnInput = {"IGNORE": {"fun": "load_from_dict_list", "terms": "em_lab/detector"},
                 "IGNORE": {"fun": "load_from", "terms": "em_lab/ebeam_column/aberration_correction/applied"},
                 "IGNORE": {"fun": "load_from_dict_list", "terms": "em_lab/ebeam_column/aperture_em"},
                 "/ENTRY[entry*]/PROGRAM[program2]/program": {"fun": "load_from", "terms": "atom_probe/control_software_program"},
                 "/ENTRY[entry*]/PROGRAM[program2]/program/@version": {"fun": "load_from", "terms": "atom_probe/control_software_program__attr_version"},
                 "/ENTRY[entry*]/experiment_identifier": {"fun": "load_from", "terms": "entry/experiment_identifier"},
                 "/ENTRY[entry*]/start_time": {"fun": "load_from", "terms": "entry/start_time"},
                 "/ENTRY[entry*]/end_time": {"fun": "load_from", "terms": "entry/end_time"},
                 "/ENTRY[entry*]/run_number": {"fun": "load_from", "terms": "entry/run_number"},
                 "/ENTRY[entry*]/operation_mode": {"fun": "load_from", "terms": "entry/operation_mode"},
                 "/ENTRY[entry*]/experiment_description": {"fun": "load_from", "terms": "entry/experiment_description"},
                 "IGNORE": {"fun": "load_from", "terms": "sample/alias"},
                 "/ENTRY[entry*]/sample/grain_diameter": {"fun": "load_from", "terms": "sample/grain_diameter/value"},
                 "/ENTRY[entry*]/sample/grain_diameter/@units": {"fun": "load_from", "terms": "sample/grain_diameter/unit"},
                 "/ENTRY[entry*]/sample/grain_diameter_error": {"fun": "load_from", "terms": "sample/grain_diameter_error/value"},
                 "/ENTRY[entry*]/sample/grain_diameter_error/@units": {"fun": "load_from", "terms": "sample/grain_diameter_error/unit"},
                 "/ENTRY[entry*]/sample/heat_treatment_quenching_rate": {"fun": "load_from", "terms": "sample/heat_treatment_quenching_rate/value"},
                 "/ENTRY[entry*]/sample/heat_treatment_quenching_rate/@units": {"fun": "load_from", "terms": "sample/heat_treatment_quenching_rate/unit"},
                 "/ENTRY[entry*]/sample/heat_treatment_quenching_rate_error": {"fun": "load_from", "terms": "sample/heat_treatment_quenching_rate_error/value"},
                 "/ENTRY[entry*]/sample/heat_treatment_quenching_rate_error/@units": {"fun": "load_from", "terms": "sample/heat_treatment_quenching_rate_error/unit"},
                 "/ENTRY[entry*]/sample/heat_treatment_temperature": {"fun": "load_from", "terms": "sample/heat_treatment_temperature/value"},
                 "/ENTRY[entry*]/sample/heat_treatment_temperature/@units": {"fun": "load_from", "terms": "sample/heat_treatment_temperature/unit"},
                 "/ENTRY[entry*]/sample/heat_treatment_temperature_error": {"fun": "load_from", "terms": "sample/heat_treatment_temperature_error/value"},
                 "/ENTRY[entry*]/sample/heat_treatment_temperature_error/@units": {"fun": "load_from", "terms": "sample/heat_treatment_temperature_error/unit"},
                 "/ENTRY[entry*]/specimen/name": {"fun": "load_from", "terms": "specimen/name"},
                 "/ENTRY[entry*]/specimen/preparation_date": {"fun": "load_from", "terms": "specimen/preparation_date"},
                 "IGNORE": {"fun": "load_from", "terms": "specimen/sample_history"},
                 "/ENTRY[entry*]/specimen/alias": {"fun": "load_from", "terms": "specimen/alias"},
                 "/ENTRY[entry*]/specimen/is_polycrystalline": {"fun": "load_from", "terms": "specimen/is_polycrystalline"},
                 "/ENTRY[entry*]/specimen/description": {"fun": "load_from", "terms": "specimen/description"},
                 "/ENTRY[entry*]/atom_probe/FABRICATION[fabrication]/identifier": {"fun": "load_from", "terms": "atom_probe/fabrication_identifier"},
                 "/ENTRY[entry*]/atom_probe/FABRICATION[fabrication]/model": {"fun": "load_from", "terms": "atom_probe/fabrication_model"},
                 "/ENTRY[entry*]/atom_probe/FABRICATION[fabrication]/vendor": {"fun": "load_from", "terms": "atom_probe/fabrication_vendor"},
                 "/ENTRY[entry*]/atom_probe/analysis_chamber/pressure": {"fun": "load_from", "terms": "atom_probe/analysis_chamber_pressure/value"},
                 "/ENTRY[entry*]/atom_probe/analysis_chamber/pressure/@units": {"fun": "load_from", "terms": "atom_probe/analysis_chamber_pressure/unit"},
                 "/ENTRY[entry*]/atom_probe/control_software/PROGRAM[program1]/program": {"fun": "load_from", "terms": "atom_probe/control_software_program"},
                 "/ENTRY[entry*]/atom_probe/control_software/PROGRAM[program1]/program/@version": {"fun": "load_from", "terms": "atom_probe/control_software_program__attr_version"},
                 "/ENTRY[entry*]/atom_probe/field_of_view": {"fun": "load_from", "terms": "atom_probe/field_of_view/value"},
                 "/ENTRY[entry*]/atom_probe/field_of_view/@units": {"fun": "load_from", "terms": "atom_probe/field_of_view/unit"},
                 "/ENTRY[entry*]/atom_probe/flight_path_length": {"fun": "load_from", "terms": "atom_probe/flight_path_length/value"},
                 "/ENTRY[entry*]/atom_probe/flight_path_length/@units": {"fun": "load_from", "terms": "atom_probe/flight_path_length/unit"},
                 "/ENTRY[entry*]/atom_probe/instrument_name": {"fun": "load_from", "terms": "atom_probe/instrument_name"},
                 "/ENTRY[entry*]/atom_probe/ion_detector/model": {"fun": "load_from", "terms": "atom_probe/ion_detector_model"},
                 "/ENTRY[entry*]/atom_probe/ion_detector/name": {"fun": "load_from", "terms": "atom_probe/ion_detector_name"},
                 "/ENTRY[entry*]/atom_probe/ion_detector/serial_number": {"fun": "load_from", "terms": "atom_probe/ion_detector_serial_number"},
                 "/ENTRY[entry*]/atom_probe/ion_detector/type": {"fun": "load_from", "terms": "atom_probe/ion_detector_type"},
                 "/ENTRY[entry*]/atom_probe/local_electrode/name": {"fun": "load_from", "terms": "atom_probe/local_electrode_name"},
                 "/ENTRY[entry*]/atom_probe/location": {"fun": "load_from", "terms": "atom_probe/location"},
                 "/ENTRY[entry*]/atom_probe/REFLECTRON[reflectron]/applied": {"fun": "load_from", "terms": "atom_probe/reflectron_applied"},
                 "/ENTRY[entry*]/atom_probe/stage_lab/base_temperature": {"fun": "load_from", "terms": "atom_probe/stage_lab_base_temperature/value"},
                 "/ENTRY[entry*]/atom_probe/stage_lab/base_temperature/@units": {"fun": "load_from", "terms": "atom_probe/stage_lab_base_temperature/unit"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/detection_rate": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_detection_rate/value"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/detection_rate/@units": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_detection_rate/unit"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/initial_radius": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_initial_radius/value"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/initial_radius/@units": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_initial_radius/unit"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/shank_angle": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_shank_angle/value"},
                 "/ENTRY[entry*]/atom_probe/specimen_monitoring/shank_angle/@units": {"fun": "load_from", "terms": "atom_probe/specimen_monitoring_shank_angle/unit"},
                 "/ENTRY[entry*]/atom_probe/status": {"fun": "load_from", "terms": "atom_probe/status"},
                 "/ENTRY[entry*]/atom_probe/pulser/pulse_fraction": {"fun": "load_from", "terms": "atom_probe/pulser/pulse_fraction"},
                 "/ENTRY[entry*]/atom_probe/pulser/pulse_frequency": {"fun": "load_from", "terms": "atom_probe/pulser/pulse_frequency/value"},
                 "/ENTRY[entry*]/atom_probe/pulser/pulse_frequency/@units": {"fun": "load_from", "terms": "atom_probe/pulser/pulse_frequency/unit"},
                 "/ENTRY[entry*]/atom_probe/pulser/pulse_mode": {"fun": "load_from", "terms": "atom_probe/pulser/pulse_mode"},
                 "/ENTRY[entry*]/atom_probe/ranging/PROGRAM[program1]/program": {"fun": "load_from", "terms": "atom_probe/ranging/program"},
                 "/ENTRY[entry*]/atom_probe/ranging/PROGRAM[program1]/program/@version": {"fun": "load_from", "terms": "atom_probe/ranging/program__attr_version"},
                 "/ENTRY[entry*]/atom_probe/reconstruction/PROGRAM[program1]/program": {"fun": "load_from", "terms": "atom_probe/reconstruction/program"},
                 "/ENTRY[entry*]/atom_probe/reconstruction/PROGRAM[program1]/program/@version": {"fun": "load_from", "terms": "atom_probe/reconstruction/program__attr_version"},
                 "/ENTRY[entry*]/atom_probe/reconstruction/crystallographic_calibration": {"fun": "load_from", "terms": "atom_probe/reconstruction/crystallographic_calibration"},
                 "/ENTRY[entry*]/atom_probe/reconstruction/parameter": {"fun": "load_from", "terms": "atom_probe/reconstruction/parameter"},
                 "/ENTRY[entry*]/atom_probe/reconstruction/protocol_name": {"fun": "load_from", "terms": "atom_probe/reconstruction/protocol_name"}}

# NeXus concept specific mapping tables which require special treatment as the current
# NOMAD OASIS custom schema implementation delivers them as a list of dictionaries instead
# of a directly flattenable list of keyword, value pairs

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

# LEAP6000 can use up to two lasers and voltage pulsing (both at the same time?)
NxPulserFromListOfDict = {"/ENTRY[entry*]/atom_probe/pulser/SOURCE[source*]/name": {"fun": "load_from", "terms": "name"},
                          "/ENTRY[entry*]/atom_probe/pulser/SOURCE[source*]/power": {"fun": "load_from", "terms": "power"},
                          "/ENTRY[entry*]/atom_probe/pulser/SOURCE[source*]/pulse_energy": {"fun": "load_from", "terms": "pulse_energy"},
                          "/ENTRY[entry*]/atom_probe/pulser/SOURCE[source*]/wavelength": {"fun": "load_from", "terms": "wavelength"}}
