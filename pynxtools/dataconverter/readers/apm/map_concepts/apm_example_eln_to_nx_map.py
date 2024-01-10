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


APM_EXAMPLE_OTHER_TO_NEXUS \
    = [("/ENTRY[entry*]/run_number", "load_from", "entry/run_number"),
       ("/ENTRY[entry*]/start_time", "load_from", "entry/start_time"),
       ("/ENTRY[entry*]/end_time", "load_from", "entry/end_time"),
       ("/ENTRY[entry*]/operation_mode", "load_from", "entry/operation_mode"),
       ("/ENTRY[entry*]/experiment_description", "load_from", "entry/experiment_description"),
       ("/ENTRY[entry*]/sample/method", "experiment"),
       ("/ENTRY[entry*]/sample/alias", "load_from", "sample/alias"),
       ("/ENTRY[entry*]/sample/grain_diameter", "load_from", "sample/grain_diameter/value"),
       ("/ENTRY[entry*]/sample/grain_diameter/@units", "load_from", "sample/grain_diameter/unit"),
       ("/ENTRY[entry*]/sample/grain_diameter_error", "load_from", "sample/grain_diameter_error/value"),
       ("/ENTRY[entry*]/sample/grain_diameter_error/@units", "load_from", "sample/grain_diameter_error/unit"),
       ("/ENTRY[entry*]/sample/heat_treatment_temperature", "load_from", "sample/heat_treatment_temperature/value"),
       ("/ENTRY[entry*]/sample/heat_treatment_temperature/@units", "load_from", "sample/heat_treatment_temperature/unit"),
       ("/ENTRY[entry*]/sample/heat_treatment_temperature_error", "load_from", "sample/heat_treatment_temperature_error/value"),
       ("/ENTRY[entry*]/sample/heat_treatment_temperature_error/@units", "load_from", "sample/heat_treatment_temperature_error/unit"),
       ("/ENTRY[entry*]/sample/heat_treatment_quenching_rate", "load_from", "sample/heat_treatment_quenching_rate/value"),
       ("/ENTRY[entry*]/sample/heat_treatment_quenching_rate/@units", "load_from", "sample/heat_treatment_quenching_rate/unit"),
       ("/ENTRY[entry*]/sample/heat_treatment_quenching_rate_error", "load_from", "sample/heat_treatment_quenching_rate_error/value"),
       ("/ENTRY[entry*]/sample/heat_treatment_quenching_rate_error/@units", "load_from", "sample/heat_treatment_quenching_rate_error/unit"),
       ("/ENTRY[entry*]/sample/description", "load_from", "sample/description"),
       ("/ENTRY[entry*]/specimen/method", "experiment"),
       ("/ENTRY[entry*]/specimen/alias", "load_from", "specimen/alias"),
       ("/ENTRY[entry*]/specimen/preparation_date", "load_from", "specimen/preparation_date"),
       ("/ENTRY[entry*]/specimen/description", "load_from", "specimen/description"),
       ("/ENTRY[entry*]/specimen/is_polycrystalline", "load_from", "specimen/is_polycrystalline"),
       ("/ENTRY[entry*]/specimen/is_amorphous", "load_from", "specimen/is_amorphous"),
       ("/ENTRY[entry*]/specimen/initial_radius", "load_from", "specimen/initial_radius/value"),
       ("/ENTRY[entry*]/specimen/initial_radius/@units", "load_from", "specimen/initial_radius/unit"),
       ("/ENTRY[entry*]/specimen/shank_angle", "load_from", "specimen/shank_angle/value"),
       ("/ENTRY[entry*]/specimen/shank_angle/@units", "load_from", "specimen/shank_angle/unit"),
       ("/ENTRY[entry*]/measurement/instrument/instrument_name", "load_from", "atom_probe/instrument_name"),
       ("/ENTRY[entry*]/measurement/instrument/location", "load_from", "atom_probe/location"),
       ("/ENTRY[entry*]/measurement/instrument/FABRICATION[fabrication]/vendor", "load_from", "atom_probe/fabrication_vendor"),
       ("/ENTRY[entry*]/measurement/instrument/FABRICATION[fabrication]/model", "load_from", "atom_probe/fabrication_model"),
       ("/ENTRY[entry*]/measurement/instrument/FABRICATION[fabrication]/identifier", "load_from", "atom_probe/fabrication_identifier"),
       ("/ENTRY[entry*]/measurement/instrument/reflectron/status", "load_from", "atom_probe/reflectron_status"),
       ("/ENTRY[entry*]/measurement/instrument/local_electrode/name", "load_from", "atom_probe/local_electrode_name"),
       ("/ENTRY[entry*]/measurement/instrument/pulser/pulse_mode", "load_from", "atom_probe/pulser/pulse_mode"),
       ("/ENTRY[entry*]/measurement/instrument/analysis_chamber/flight_path", "load_from", "atom_probe/nominal_flight_path/value"),
       ("/ENTRY[entry*]/measurement/instrument/analysis_chamber/flight_path/@units", "load_from", "atom_probe/nominal_flight_path/unit"),
       ("/ENTRY[entry*]/measurement/instrument/status", "load_from", "atom_probe/status"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/control/evaporation_control", "load_from", "atom_probe/evaporation_control"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/control/target_detection_rate", "load_from", "atom_probe/target_detection_rate"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/control/target_detection_rate/@units", "ions/pulse"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/pulser/pulse_frequency", "load_from", "atom_probe/pulser/pulse_frequency/value"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/pulser/pulse_frequency/@units", "load_from", "atom_probe/pulser/pulse_frequency/unit"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/pulser/pulse_fraction", "load_from", "atom_probe/pulser/pulse_fraction"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/analysis_chamber/chamber_pressure", "load_from", "atom_probe/chamber_pressure/value"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/analysis_chamber/chamber_pressure/@units", "load_from", "atom_probe/chamber_pressure/unit"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/stage_lab/base_temperature", "load_from", "atom_probe/base_temperature/value"),
       ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/stage_lab/base_temperature/@units", "load_from", "atom_probe/base_temperature/unit"),
       ("/ENTRY[entry*]/atom_probe/ranging/PROGRAM[program1]/program", "load_from", "ranging/program"),
       ("/ENTRY[entry*]/atom_probe/ranging/PROGRAM[program1]/program/@version", "load_from", "ranging/program_version"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/PROGRAM[program1]/program", "load_from", "reconstruction/program"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/PROGRAM[program1]/program/@version", "load_from", "reconstruction/program_version"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/protocol_name", "load_from", "reconstruction/protocol_name"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/crystallographic_calibration", "load_from", "reconstruction/crystallographic_calibration"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/parameter", "load_from", "reconstruction/parameter"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/field_of_view", "load_from", "reconstruction/field_of_view/value"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/field_of_view/@units", "load_from", "reconstruction/field_of_view/unit"),
       ("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/path", "load_from", "workflow/raw_dat_file"),
       ("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/checksum", "sha256", "workflow/raw_dat_file"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/path", "load_from", "workflow/hit_dat_file"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/checksum", "sha256", "workflow/hit_dat_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/path", "load_from", "workflow/recon_cfg_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/checksum", "sha256", "workflow/recon_cfg_file")]

"""
# depending on the case some of these are populated by the I/O logic resolver
# some of them will be loaded by the ELN parser
APM_EXAMPLE_WORKFLOW_TO_NEXUS \
    = [("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/type", "file"),
       ("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/path", "load_from", "workflow/raw_dat_file"),
       ("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/checksum", "sha256", "workflow/raw_dat_file"),
       ("/ENTRY[entry*]/atom_probe/raw_data/SERIALIZED[serialized]/algorithm", "SHA256"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/type", "file"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/path", "load_from", "workflow/hit_dat_file"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/checksum", "sha256", "workflow/hit_dat_file"),
       ("/ENTRY[entry*]/atom_probe/hit_finding/SERIALIZED[serialized]/algorithm", "SHA256"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/type", "file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/path", "load_from", "workflow/recon_cfg_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/checksum", "sha256", "workflow/recon_cfg_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/config/algorithm", "SHA256"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/results/type", "file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/results/path", "load_from", "workflow/recon_res_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/results/checksum", "sha256", "workflow/recon_res_file"),
       ("/ENTRY[entry*]/atom_probe/reconstruction/results/algorithm", "SHA256"),
       ("/ENTRY[entry*]/atom_probe/ranging/SERIALIZED[serialized]/type", "file"),
       ("/ENTRY[entry*]/atom_probe/ranging/SERIALIZED[serialized]/path", "load_from", "workflow/range_dat_file"),
       ("/ENTRY[entry*]/atom_probe/ranging/SERIALIZED[serialized]/checksum", "sha256", "workflow/range_dat_file"),
       ("/ENTRY[entry*]/atom_probe/ranging/SERIALIZED[serialized]/algorithm", "SHA256")]
"""

# NeXus concept specific mapping tables which require special treatment as the current
# NOMAD OASIS custom schema implementation delivers them as a list of dictionaries instead
# of a directly flattenable list of key, value pairs


APM_EXAMPLE_USER_TO_NEXUS \
    = [("/ENTRY[entry*]/USER[user*]/name", "load_from", "name"),
       ("/ENTRY[entry*]/USER[user*]/affiliation", "load_from", "affiliation"),
       ("/ENTRY[entry*]/USER[user*]/address", "load_from", "address"),
       ("/ENTRY[entry*]/USER[user*]/email", "load_from", "email"),
       ("/ENTRY[entry*]/USER[user*]/orcid", "load_from", "orcid"),
       ("/ENTRY[entry*]/USER[user*]/orcid_platform", "load_from", "orcid_platform"),
       ("/ENTRY[entry*]/USER[user*]/telephone_number", "load_from", "telephone_number"),
       ("/ENTRY[entry*]/USER[user*]/role", "load_from", "role"),
       ("/ENTRY[entry*]/USER[user*]/social_media_name", "load_from", "social_media_name"),
       ("/ENTRY[entry*]/USER[user*]/social_media_platform", "load_from", "social_media_platform")]

# LEAP6000 can use up to two lasers and voltage pulsing (both at the same time?)
# ("/ENTRY[entry*]/measurement/instrument/pulser/SOURCE[source*]/name", "load_from", "atom_probe/pulser/source_name"),
# ("/ENTRY[entry*]/measurement/instrument/pulser/SOURCE[source*]/wavelength", "load_from", "atom_probe/pulser/source_wavelength/value"),
# ("/ENTRY[entry*]/measurement/instrument/pulser/SOURCE[source*]/wavelength/@units", "load_from", "atom_probe/pulser/source_wavelength/unit"),
# ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/pulser/SOURCE[source*]/pulse_energy", "load_from", "atom_probe/pulser/source_pulse_energy/value"),
# ("/ENTRY[entry*]/measurement/event_data_apm_set/EVENT_DATA_APM[event_data_apm]/instrument/pulser/SOURCE[source*]/pulse_energy/@units", "load_from", "atom_probe/pulser/source_pulse_energy/unit"),
