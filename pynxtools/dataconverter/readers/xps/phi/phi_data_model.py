"""
Data model for Phi Versaprobe software (version SS 3.3.3.2).
"""
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
# pylint: disable=too-many-instance-attributes

from dataclasses import dataclass
from dataclasses import field

import numpy as np


@dataclass
class PhiDataclass:
    """Generic class to hold validation method."""

    def validate_types(self):
        ret = True
        for field_name, field_def in self.__dataclass_fields__.items():
            actual_type = type(getattr(self, field_name))
            if actual_type != field_def.type:
                print(f"\t{field_name}: '{actual_type}' instead of '{field_def.type}'")
                ret = False
        return ret

    def __post_init__(self):
        if not self.validate_types():
            raise ValueError("Wrong types")

    def dict(self):
        return self.__dict__.copy()


@dataclass
class PhiMetadata(PhiDataclass):
    """An object to store the PHI Versaprobe metadata."""

    platform: str = ""
    technique: str = ""
    technique_ex: str = ""
    file_type: str = ""
    file_description: str = ""
    software_version: str = ""
    instrument_model: str = ""
    acquisition_filename: str = ""
    file_date: str = ""
    acquisition_file_date: str = ""
    vendor: str = ""
    user_name: str = ""
    experiment_id: str = ""
    energy_reference: dict = field(default_factory=dict)

    analyser_work_function: str = ""
    analyser_work_function_units: str = "eV"
    analyser_retardation_gain: float = 0.0
    register_image: bool = False
    register_image_interval: int = 0
    register_image_mode: int = 0
    register_image_last: int = 0
    platen_id: str = ""  # what's that?
    photo_filename: str = ""  # what's that?
    sxi_filename: str = ""  # what's that?
    source_analyser_angle: float = 0.0  # unit
    source_analyser_angle_units: str = "degree"
    analyser_solid_angle: float = 0.0  # unit
    analyser_solid_angle_units: str = "degree"
    intensity_recalibration: bool = False
    intensity_calibration_coefficients: list = field(default_factory=list)
    energy_recalibration: bool = False
    scan_deflection_span: dict = field(default_factory=dict)  # what's that?
    scan_deflection_offset: dict = field(default_factory=dict)  # what's that?
    sca_multiplier_voltage: float = 0.0
    sca_multiplier_voltage_units: str = "V"
    narrow_acceptance_angle: bool = False
    refresh_persistence: int = 0
    peak_to_noise_ratio_state: bool = False
    delay_before_acquire: float = 0.0
    delay_before_acquire_units: str = "s"
    c60_ion_gun: str = ""
    bias_box_mode: int = 0
    tfc_parameters: list = field(default_factory=list)
    sem_field_of_view: float = 0.0
    image_size: dict = field(default_factory=dict)

    ion_gun_mode: str = ""
    sputter_ion: str = ""
    sputter_current: str = ""
    sputter_current_units: str = "A"
    sputter_rate: str = ""
    sputter_rate_units: str = "A/s"
    sputter_energy: str = ""
    sputter_energy_units: str = "eV"
    float_voltage: float = 0.0
    float_voltage_units: str = "V"
    float_enabled: bool = False
    grid_voltage: float = 0.0
    grid_voltage_units: str = "V"
    condenser_lens_voltage: float = 0.0
    condenser_lens_voltage_units: str = "V"
    objective_lens_voltage: float = 0.0
    objective_lens_voltage_units: str = "V"
    bend_voltage: float = 0.0
    bend_voltage_units: str = "V"
    sputter_raster: dict = field(default_factory=dict)
    sputter_raster_offset: dict = field(default_factory=dict)
    target_sputter_time: float = 0.0
    target_sputter_time_units: str = "s"
    sputter_emission: float = 0.0
    sputter_emission_units: str = "A"
    deflection_bias: float = 0.0
    deflection_bias_units: str = "V"
    ion_gun_gas_pressure: float = 0.0
    ion_gun_gas_pressure_units: str = "Pa"

    neutral_ion: str = ""
    neutral_current: float = 0.0
    neutral_current_units: str = "A"
    neutral_rate: float = 0.0
    neutral_rate_units: str = "A/s"
    neutral_energy: float = 0.0
    neutral_energy_units: str = "eV"
    neutral_float_voltage: float = 0.0
    neutral_float_voltage_units: str = "V"
    neutral_float_enabled: bool = False
    neutral_grid_voltage: float = 0.0
    neutral_grid_voltage_units: str = "V"
    neutral_condenser_lens_voltage: float = 0.0
    neutral_condenser_lens_voltage_units: str = "V"
    neutral_objective_lens_voltage: float = 0.0
    neutral_objective_lens_voltage_units: str = "V"
    neutral_bend_voltage: float = 0.0
    neutral_bend_voltage_units: str = "V"
    neutral_raster: dict = field(default_factory=dict)
    neutral_raster_offset: dict = field(default_factory=dict)
    neutral_target_timed_on_time: float = 0.0
    neutral_target_timed_on_time_units: str = "s"
    neutral_emission: float = 0.0
    neutral_emission_units: str = "A"
    neutral_deflection_bias: float = 0.0
    neutral_deflection_bias_units: str = "V"
    neutral_ion_gun_gas_pressure: float = 0.0
    neutral_ion_gun_gas_pressure_units: str = "Pa"

    xps_scan_mode: str = ""
    energy_scan_mode: str = ""
    survey_num_of_cycles: int = 0
    survey_dwell_time: float = 0.0
    survey_dwell_time_units: str = "s"

    no_depth_profile_data_cycles: int = 0
    no_pre_sputter_cycles: int = 0
    profiling_sputter_delay: float = 0.0
    profiling_sputter_delay_units: str = ""
    profiling_xray_off_during_sputter: bool = False
    profiling_source_blank_during_sputter: bool = False
    profiling_zalar_high_accuracy_interval: int = 0
    profiling_sample_rotation: str = ""
    profiling_depth_recalibration: bool = False
    profiling_sputter_mode: str = ""
    depth_calibration_definition: str = ""
    profiling_no_depth_regions: int = 0

    no_spectral_regions_full: int = 0
    no_spectral_regions: int = 0
    no_spatial_areas: int = 0

    xray_source: dict = field(default_factory=dict)
    xray_anode_position: int = 0
    xray_power: float = 0.0
    xray_power_units: str = "W"
    xray_beam_diameter: float = 0.0
    xray_beam_diameter_units: str = "m"
    xray_beam_voltage: float = 0.0
    xray_beam_voltage_units: str = "V"
    xray_condenser_lens_voltage: float = 0.0
    xray_condenser_lens_voltage_units: str = "V"
    xray_objective_coil_current: float = 0.0
    xray_objective_coil_current_units: str = "V"
    xray_blanking_voltage: float = 0.0
    xray_blanking_voltage_units: str = "V"
    xray_filament_current: float = 0.0
    xray_filament_current_units: str = "A"
    xray_stigmator: dict = field(default_factory=dict)
    xray_offset: float = 0.0
    xray_offset_units: str = "m"
    xray_magnification_factor: dict = field(default_factory=dict)
    xray_delay_factor: dict = field(default_factory=dict)  ## what are the keys?
    xray_rotation: float = 0.0
    xray_rotation_units: str = "degree"
    xray_high_power: bool = False
    xray_emission_control: bool = False
    xray_emission_current: float = 0.0
    xray_emission_current_units: str = "A"
    xray_step_delay_read_beam: int = 0
    xray_steps_per_diameter: float = 0.0
    xray_interlace_interval: int = 0
    xray_max_filament_current: float = 0.0
    xray_max_filament_current_units: str = "A"
    xray_settings: dict = field(default_factory=dict)

    flood_gun_mode: str = ""
    flood_gun_current: float = 0.0
    flood_gun_current_units: str = "A"
    flood_gun_energy: float = 0.0
    flood_gun_energy_units: str = "eV"
    flood_gun_extractor: float = 0.0
    flood_gun_extractor_units: str = "V"
    flood_gun_x_steering: float = 0.0
    flood_gun_y_steering: float = 0.0
    flood_gun_filament_current: float = 0.0
    flood_gun_filament_current_units: str = "A"
    flood_gun_pulse_length: float = 0.0
    flood_gun_pulse_length_units: str = "s"
    flood_gun_pulse_frequency: int = 0
    flood_gun_gain: int = 0
    flood_gun_time_per_step: float = 0.0
    flood_gun_time_per_step_units: str = "s"
    flood_gun_ramp_rate: float = 0.0
    flood_gun_ramp_rate_units: str = "A/s"

    sxi_persistence: int = 0
    sxi_sec_per_display: float = 0.0
    sxi_auto_contrast: bool = False
    sxi_auto_contrast_low: float = 0.0
    sxi_auto_contrast_high: float = 0.0
    sxi_binding_energy: float = 0.0
    sxi_binding_energy_units: str = "eV"
    sxi_pass_energy: float = 0.0
    sxi_pass_energy_units: str = "eV"
    sxi_lens2_voltage: float = 0.0
    sxi_lens2_voltage_units: str = "V"
    sxi_lens3_voltage: float = 0.0
    sxi_lens3_voltage_units: str = "V"
    sxi_lens4_voltage: float = 0.0
    sxi_lens4_voltage_units: str = "V"
    sxi_lens5_voltage: float = 0.0
    sxi_lens5_voltage_units: str = "V"
    sxi_rotator: float = 0.0
    sxi_rotator_units: str = ""
    sxi_lens_bias_voltage: float = 0.0
    sxi_lens_bias_voltage_units: str = "V"
    sxi_shutter_bias: bool = False
    sxi_shutter_bias_voltage: float = 0.0
    sxi_shutter_bias_voltage_units: str = "V"
    sxi_display_mode: int = 0
    detector_acquisition_time: float = 0.0
    detector_acquisition_time_units: str = "s"
    number_of_channels: int = 0
    channel_1_info: list = field(default_factory=list)
    channel_2_info: list = field(default_factory=list)
    channel_3_info: list = field(default_factory=list)
    channel_4_info: list = field(default_factory=list)
    channel_5_info: list = field(default_factory=list)
    channel_6_info: list = field(default_factory=list)
    channel_7_info: list = field(default_factory=list)
    channel_8_info: list = field(default_factory=list)
    channel_9_info: list = field(default_factory=list)
    channel_10_info: list = field(default_factory=list)
    channel_11_info: list = field(default_factory=list)
    channel_12_info: list = field(default_factory=list)
    channel_13_info: list = field(default_factory=list)
    channel_14_info: list = field(default_factory=list)
    channel_15_info: list = field(default_factory=list)
    channel_16_info: list = field(default_factory=list)
    channel_17_info: list = field(default_factory=list)
    channel_18_info: list = field(default_factory=list)
    channel_19_info: list = field(default_factory=list)
    channel_20_info: list = field(default_factory=list)
    channel_21_info: list = field(default_factory=list)
    channel_22_info: list = field(default_factory=list)
    channel_23_info: list = field(default_factory=list)
    channel_24_info: list = field(default_factory=list)
    channel_25_info: list = field(default_factory=list)
    channel_26_info: list = field(default_factory=list)
    channel_27_info: list = field(default_factory=list)
    channel_28_info: list = field(default_factory=list)
    channel_29_info: list = field(default_factory=list)
    channel_30_info: list = field(default_factory=list)
    channel_31_info: list = field(default_factory=list)
    channel_32_info: list = field(default_factory=list)
    stage_positions: dict = field(default_factory=dict)
    stage_current_rotation_speed: float = 0.0
    stage_current_rotation_speed_units: str = ""

    defect_positioner_id: int = 0
    defect_positioner_comment: str = ""
    defect_positioner_u: float = 0.0
    defect_positioner_u_units: str = "mm"
    defect_positioner_v: float = 0.0
    defect_positioner_v_units: str = "mm"
    defect_positioner_x: float = 0.0
    defect_positioner_x_units: str = "mm"
    defect_positioner_y: float = 0.0
    defect_positioner_y_units: str = "mm"
    defect_positioner_z: float = 0.0
    defect_positioner_z_units: str = "mm"
    defect_positioner_tilt: float = 0.0
    defect_positioner_tilt_units: str = "mm"
    defect_positioner_rotation: float = 0.0
    defect_positioner_rotation_units: str = "mm"
    defect_positioner_alignment: str = ""
    defect_positioner_reference_image: str = ""

    gcib_sputter_rate: float = 0.0
    gcib_sputter_rate_units: str = "A/s"
    gcib_high_voltage: float = 0.0
    gcib_high_voltage_units: str = "V"
    gcib_ionization: float = 0.0
    gcib_ionization_units: str = "V"
    gcib_extractor: float = 0.0
    gcib_extractor_units: str = "V"
    gcib_raster_size: dict = field(default_factory=dict)
    gcib_raster_offset: dict = field(default_factory=dict)
    gcib_wien_filter_voltage: float = 0.0
    gcib_wien_filter_voltage_units: str = "V"
    gcib_bend_voltage: float = 0.0
    gcib_bend_voltage_units: str = "V"
    gcib_emission: float = 0.0
    gcib_emission_units: str = "A"
    gcib_magnet_current: float = 0.0
    gcib_magnet_current_units: str = "A"
    gcib_objective: float = 0.0
    gcib_objective_units: str = ""
    gcib_focus: float = 0.0
    gcib_focus_units: str = ""
    gcib_gas_pressure: float = 0.0
    gcib_gas_pressure_units: str = ""
    gcib_cluster_size: float = 0.0
    gcib_cluster_size_units: str = ""
    gcib_energy_per_atom: float = 0.0
    gcib_energy_per_atom_units: str = ""

    deconvolution: bool = False
    deconvolution_pass_energy: float = 0.0
    deconvolution_pass_energy_units: str = ""
    auto_flood_gun: bool = False
    auto_neutral_ion_source: bool = False
    presputter: bool = False


@dataclass
class PhiSpectralRegion(PhiDataclass):
    """An object to store the PHI Versaprobe metadata."""

    full_region: bool = False
    region_id: int = 0
    region_definition: str = ""
    spectrum_type: str = ""
    region_definition2: str = ""
    region_background: str = ""
    region_hero: str = ""
    region_ir: str = ""
    n_values: int = 0
    energy: np.ndarray = field(default_factory=lambda: np.zeros(0))
    dwell_time: float = 0.0
    dwell_time_units: str = "s"
    pass_energy: float = 0.0
    pass_energy_units: str = "eV"


@dataclass
class PhiSpatialArea(PhiDataclass):
    """An object to store the PHI Versaprobe metadata."""

    area_id: int = 0
    area_definition: str = ""
    area_description: str = ""
    area_hr_photo_correction: str = ""
