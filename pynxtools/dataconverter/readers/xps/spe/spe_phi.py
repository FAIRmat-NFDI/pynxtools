"""
Parser for reading XPS (X-ray Photoelectron Spectroscopy) data from
Specs Lab Prodigy XY exports, to be passed to mpes nxdl
(NeXus Definition Language) template.
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

# pylint: disable=too-many-lines,too-many-instance-attributes

import re
import copy
import datetime
import xarray as xr
import numpy as np

from pynxtools.dataconverter.readers.xps.reader_utils import (
    XPSMapper,
    check_uniform_step_width,
    get_minimal_step,
    construct_entry_name,
    construct_data_key,
    construct_detector_data_key,
)


class SpeMapperPhi(XPSMapper):
    """
    Class for restructuring .xy data file from
    Specs vendor into python dictionary.
    """

    config_file = "config_spe_phi.json"

    def __init__(self):
        super().__init__()
        self.write_channels_to_data = True

    def _select_parser(self):
        return SpeParser()

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the Specs XY parser.

        Parameters
        ----------
        file : TYPE
            DESCRIPTION.
        **kwargs : dict
            write_channels_to_data: bool
                If True, the spectra of each individual channel is
                written to the entry/data field in the MPES template.

        Returns
        -------
        dict
            Flattened dictionary to be passed to MPES template.

        """
        return super().parse_file(file, **kwargs)

    def construct_data(self):
        """Map TXT format to NXmpes-ready dict."""
        # pylint: disable=duplicate-code
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "user": [
                "user_name",
            ],
            "instrument": [
                "bias_box_mode",
                "instrument_model",
                "vendor",
                "sca_multiplier_voltage",
                "sca_multiplier_voltage/@units",
                "source_analyser_angle",
                "source_analyser_angle/@units",
            ],
            "source": [
                "scan_deflection_offset_x",
                "scan_deflection_offset_y",
                "scan_deflection_span_x",
                "scan_deflection_span_y",
                "xray_anode_material",
                "xray_anode_position",
                "xray_beam_diameter",
                "xray_beam_diameter/@units",
                "xray_beam_voltage",
                "xray_beam_voltage/@units",
                "xray_blanking_voltage",
                "xray_blanking_voltage/@units",
                "xray_condenser_lens_voltage",
                "xray_condenser_lens_voltage/@units",
                "xray_delay_factor_x",
                "xray_delay_factor_y",
                "xray_emission_control",
                "xray_emission_current",
                "xray_emission_current/@units",
                "xray_energy",
                "xray_energy/@units",
                "xray_filament_current",
                "xray_filament_current/@units",
                "xray_high_power",
                "xray_high_voltage",
                "xray_high_voltage/@units",
                "xray_interlace_interval",
                "xray_magnification_factor_x",
                "xray_magnification_factor_y",
                "xray_max_filament_current",
                "xray_max_filament_current/@units",
                "xray_monochromatized",
                "xray_objective_coil_current",
                "xray_objective_coil_current/@units",
                "xray_offset",
                "xray_offset/@units",
                "xray_power",
                "xray_power/@units",
                "xray_rotation",
                "xray_rotation/@units",
                "xray_spot_size",
                "xray_spot_size/@units",
                "xray_step_delay_read_beam",
                "xray_steps_per_diameter",
                "xray_stigmator_x",
                "xray_stigmator_y",
            ],
            "beam": [
                "xray_beam_diameter",
                "xray_beam_diameter/@units",
            ],
            "analyser": [
                "analyser_retardation_gain",
                "analyser_solid_angle",
                "analyser_solid_angle/@units",
                "analyser_work_function",
                "analyser_work_function/@units",
                "sxi_auto_contrast",
                "sxi_auto_contrast_high",
                "sxi_auto_contrast_low",
                "sxi_binding_energy",
                "sxi_binding_energy/@units",
                "sxi_display_mode",
                "sxi_filename",
                "sxi_lens2_voltage",
                "sxi_lens2_voltage/@units",
                "sxi_lens3_voltage",
                "sxi_lens3_voltage/@units",
                "sxi_lens4_voltage",
                "sxi_lens4_voltage/@units",
                "sxi_lens5_voltage",
                "sxi_lens5_voltage/@units",
                "sxi_lens_bias_voltage",
                "sxi_lens_bias_voltage/@units",
                "sxi_pass_energy",
                "sxi_pass_energy/@units",
                "sxi_persistence",
                "sxi_rotator",
                "sxi_rotator/@units",
                "sxi_sec_per_display",
                "sxi_shutter_bias",
                "sxi_shutter_bias_voltage",
                "sxi_shutter_bias_voltage/@units",
            ],
            "collectioncolumn": [
                "narrow_acceptance_angle",
            ],
            "energydispersion": [
                "energy_scan_mode",
            ],
            "detector": [
                "channel_1_info",
                "channel_2_info",
                "channel_3_info",
                "channel_4_info",
                "channel_5_info",
                "channel_6_info",
                "channel_7_info",
                "channel_8_info",
                "channel_9_info",
                "channel_10_info",
                "channel_11_info",
                "channel_12_info",
                "channel_13_info",
                "channel_14_info",
                "channel_15_info",
                "channel_16_info",
                "channel_17_info",
                "channel_18_info",
                "channel_19_info",
                "channel_20_info",
                "channel_21_info",
                "channel_22_info",
                "channel_23_info",
                "channel_24_info",
                "channel_25_info",
                "channel_26_info",
                "channel_27_info",
                "channel_28_info",
                "channel_29_info",
                "channel_30_info",
                "channel_31_info",
                "channel_32_info",
                "delay_before_acquire",
                "delay_before_acquire/@units",
                "detector_acquisition_time",
                "detector_acquisition_time/@units",
                "number_of_channels",
                "refresh_persistence",
                "survey_dwell_time",
                "survey_dwell_time/@units",
            ],
            "manipulator": [
                "stage_x",
                "stage_x/@units",
                "stage_y",
                "stage_y/@units",
                "stage_z",
                "stage_z/@units",
                "stage_azimuth",
                "stage_azimuth/@units",
                "stage_polar",
                "stage_polar/@units",
                "stage_current_rotation_speed",
                "stage_current_rotation_speed/@units",
            ],
            "defect_positioner": [
                "defect_positioner_alignment",
                "defect_positioner_comment",
                "defect_positioner_id",
                "defect_positioner_reference_image",
                "defect_positioner_rotation",
                "defect_positioner_rotation/@units",
                "defect_positioner_tilt",
                "defect_positioner_tilt/@units",
                "defect_positioner_u",
                "defect_positioner_u/@units",
                "defect_positioner_v",
                "defect_positioner_v/@units",
                "defect_positioner_x",
                "defect_positioner_x/@units",
                "defect_positioner_y",
                "defect_positioner_y/@units",
                "defect_positioner_z",
                "defect_positioner_z/@units",
            ],
            "c60_ion_gun": [
                "c60_ion_gun",
            ],
            "flood_gun": [
                "auto_flood_gun",
                "flood_gun_current",
                "flood_gun_current/@units",
                "flood_gun_energy",
                "flood_gun_energy/@units",
                "flood_gun_extractor",
                "flood_gun_extractor/@units",
                "flood_gun_filament_current",
                "flood_gun_filament_current/@units",
                "flood_gun_gain",
                "flood_gun_mode",
                "flood_gun_pulse_frequency",
                "flood_gun_pulse_length",
                "flood_gun_pulse_length/@units",
                "flood_gun_ramp_rate",
                "flood_gun_ramp_rate/@units",
                "flood_gun_time_per_step",
                "flood_gun_time_per_step/@units",
                "flood_gun_x_steering",
                "flood_gun_y_steering",
            ],
            "gcib": [
                "gcib_bend_voltage",
                "gcib_bend_voltage/@units",
                "gcib_cluster_size",
                "gcib_cluster_size/@units",
                "gcib_emission",
                "gcib_emission/@units",
                "gcib_energy_per_atom",
                "gcib_energy_per_atom/@units",
                "gcib_extractor",
                "gcib_extractor/@units",
                "gcib_focus",
                "gcib_focus/@units",
                "gcib_gas_pressure",
                "gcib_gas_pressure/@units",
                "gcib_high_voltage",
                "gcib_high_voltage/@units",
                "gcib_ionization",
                "gcib_ionization/@units",
                "gcib_magnet_current",
                "gcib_magnet_current/@units",
                "gcib_objective",
                "gcib_objective/@units",
                "gcib_raster_offset_x",
                "gcib_raster_offset_x/@units",
                "gcib_raster_offset_y",
                "gcib_raster_offset_y/@units",
                "gcib_raster_size_x",
                "gcib_raster_size_x/@units",
                "gcib_raster_size_y",
                "gcib_raster_size_y/@units",
                "gcib_sputter_rate",
                "gcib_sputter_rate/@units",
                "gcib_wien_filter_voltage",
                "gcib_wien_filter_voltage/@units",
            ],
            "neutral_ion_gun": [
                "auto_neutral_ion_source",
                "neutral_bend_voltage",
                "neutral_bend_voltage/@units",
                "neutral_condenser_lens_voltage",
                "neutral_condenser_lens_voltage/@units",
                "neutral_current",
                "neutral_current/@units",
                "neutral_deflection_bias",
                "neutral_deflection_bias/@units",
                "neutral_emission",
                "neutral_emission/@units",
                "neutral_energy",
                "neutral_energy/@units",
                "neutral_float_enabled",
                "neutral_float_voltage",
                "neutral_float_voltage/@units",
                "neutral_grid_voltage",
                "neutral_grid_voltage/@units",
                "neutral_ion",
                "neutral_ion_gun_gas_pressure",
                "neutral_ion_gun_gas_pressure/@units",
                "neutral_objective_lens_voltage",
                "neutral_objective_lens_voltage/@units",
                "neutral_raster_offset_x",
                "neutral_raster_offset_x/@units",
                "neutral_raster_offset_y",
                "neutral_raster_offset_y/@units",
                "neutral_raster_x",
                "neutral_raster_x/@units",
                "neutral_raster_y",
                "neutral_raster_y/@units",
                "neutral_rate",
                "neutral_rate/@units",
                "neutral_target_timed_on_time",
                "neutral_target_timed_on_time/@units",
            ],
            "sputter_gun": [
                "bend_voltage",
                "bend_voltage/@units",
                "condenser_lens_voltage",
                "condenser_lens_voltage/@units",
                "deflection_bias",
                "deflection_bias/@units",
                "float_enabled",
                "float_voltage",
                "float_voltage/@units",
                "grid_voltage",
                "grid_voltage/@units",
                "ion_gun_gas_pressure",
                "ion_gun_gas_pressure/@units",
                "ion_gun_mode",
                "objective_lens_voltage",
                "objective_lens_voltage/@units",
                "sputter_current",
                "sputter_current/@units",
                "sputter_emission",
                "sputter_emission/@units",
                "sputter_energy",
                "sputter_energy/@units",
                "sputter_ion",
                "sputter_raster_offset_x",
                "sputter_raster_offset_x/@units",
                "sputter_raster_offset_y",
                "sputter_raster_offset_y/@units",
                "sputter_raster_x",
                "sputter_raster_x/@units",
                "sputter_raster_y",
                "sputter_raster_y/@units",
                "sputter_rate",
                "sputter_rate/@units",
                "target_sputter_time",
                "target_sputter_time/@units",
            ],
            "sample": [],
            "process": [
                "deconvolution",
                "deconvolution_pass_energy",
                "deconvolution_pass_energy/@units",
                "energy_recalibration",
                "energy_reference_energy",
                "energy_reference_energy/@units",
                "energy_reference_peak",
                "intensity_calibration_coefficients",
                "intensity_recalibration",
            ],
            "data": [],
            "file": [
                "photo_filename",
                "software_version",
            ],
            "region": [
                "acquisition_file_date",
                "acquisition_filename",
                "experiment_id",
                "file_date",
                "file_description",
                "file_type",
                "image_size_x",
                "image_size_y",
                "no_spatial_areas",
                "no_spectral_regions",
                "no_spectral_regions_full",
                "sem_field_of_view",
                "spatial_area_definition",
                "spatial_area_description",
                "spatial_hr_photo_correction",
                "spectral_region_background",
                "spectral_region_background_full",
                "spectral_region_definition",
                "spectral_region_definition2",
                "spectral_region_definition2_full",
                "spectral_region_definition_full",
                "spectral_region_hero",
                "spectral_region_hero_full",
                "spectral_region_ir",
                "spectral_region_ir_full",
                "spectrum_id",
                "survey_num_of_cycles",
                "technique",
                "technique_ex",
                "tfc_parameters",
                "xps_scan_mode",
            ],
            "unused": [
                "peak_to_noise_ratio_state",
                "platform",
                "platen_id",
                "presputter",
                "register_image",
                "register_image_interval",
                "register_image_last",
                "register_image_mode",
            ],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals,duplicate-code
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["group_name"]}'
        region_parent = f'{group_parent}/regions/RegionData_{spectrum["region_name"]}'
        file_parent = f"{region_parent}/file_info"
        instrument_parent = f"{region_parent}/instrument"
        analyser_parent = f"{instrument_parent}/analyser"

        path_map = {
            "file_info": f"{file_parent}",
            "user": f"{region_parent}/user",
            "instrument": f"{instrument_parent}",
            "source": f"{instrument_parent}/source",
            "beam": f"{instrument_parent}/beam",
            "analyser": f"{analyser_parent}",
            "collectioncolumn": f"{analyser_parent}/collectioncolumn",
            "energydispersion": f"{analyser_parent}/energydispersion",
            "detector": f"{analyser_parent}/detector",
            "manipulator": f"{instrument_parent}/manipulator",
            "defect_positioner": f"{instrument_parent}/defect_positioner",
            "flood_gun": f"{instrument_parent}/flood_gun",
            "gcib": f"{instrument_parent}/gcib",
            "sputter_gun": f"{instrument_parent}/sputter_gun",
            "process": f"{instrument_parent}/process",
            "sample": f"{region_parent}/sample",
            "data": f"{region_parent}/data",
            "region": f"{region_parent}",
        }

        for grouping, spectrum_keys in key_map.items():
            root = path_map[str(grouping)]
            for spectrum_key in spectrum_keys:
                try:
                    mpes_key = spectrum_key
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]
                except KeyError:
                    pass

        if self.parser.export_settings["Transmission Function"]:
            path = f"{path_map['collectioncolumn']}/transmission_function"
            self._xps_dict[path] = spectrum["data"]["transmission_function"]
            self._xps_dict[f"{path}/units"] = spectrum["tf_units"]

        # Create keys for writing to data and detector
        entry = construct_entry_name(region_parent)
        scan_key = construct_data_key(spectrum)
        detector_data_key_child = construct_detector_data_key(spectrum)
        detector_data_key = f'{path_map["detector"]}/{detector_data_key_child}/counts'


# =============================================================================
#         x_units = spectrum["x_units"]
#         energy = np.array(spectrum["data"]["x"])
#         intensity = np.array(spectrum["data"]["y"])
#
#         if entry not in self._xps_dict["data"]:
#             self._xps_dict["data"][entry] = xr.Dataset()
#
#         # Write raw data to detector.
#         self._xps_dict[detector_data_key] = intensity
#
#         if not self.parser.export_settings["Separate Channel Data"]:
#             averaged_channels = intensity
#         else:
#             all_channel_data = [
#                 value
#                 for key, value in self._xps_dict.items()
#                 if detector_data_key.split("Channel_")[0] in key
#             ]
#             averaged_channels = np.mean(all_channel_data, axis=0)
#
#         if not self.parser.export_settings["Separate Scan Data"]:
#             averaged_scans = intensity
#         else:
#             all_scan_data = [
#                 value
#                 for key, value in self._xps_dict.items()
#                 if detector_data_key.split("Scan_")[0] in key
#             ]
#             averaged_scans = np.mean(all_scan_data, axis=0)
#
#         # Write to data in order: scan, cycle, channel
#
#         # Write averaged cycle data to 'data'.
#         self._xps_dict["data"][entry][scan_key.split("_")[0]] = xr.DataArray(
#             data=averaged_scans,
#             coords={x_units: energy},
#         )
#         if self.parser.export_settings["Separate Scan Data"]:
#             # Write average cycle data to 'data'.
#             self._xps_dict["data"][entry][scan_key] = xr.DataArray(
#                 data=averaged_channels,
#                 coords={x_units: energy},
#             )
#
#         if (
#             self.parser.export_settings["Separate Channel Data"]
#             and self.write_channels_to_data
#         ):
#             # Write channel data to 'data'.
#             channel_no = spectrum["channel_no"]
#             self._xps_dict["data"][entry][
#                 f"{scan_key}_chan{channel_no}"
#             ] = xr.DataArray(data=intensity, coords={x_units: energy})
# =============================================================================


class SpeParser:  # pylint: disable=too-few-public-methods
    """
    A parser for reading in PHI Versaprobe data in the .spe format.
    Tested with Software version SS 3.3.3.2
    """

    def __init__(self):
        """
        Construct the parser.

        """
        self.lines = []
        self.spectra = [
            {"spectrum_id": 0},
            {"spectrum_id": 1},
        ]
        self.metadata = PhiMetadata()

        self.settings_map = {
            "FileDesc": "file_description",
            "acq_filename": "acquisition_filename",
            "acq_file_date": "acquisition_file_date",
            "institution": "vendor",
            "operator": "user_name",
            "experiment_i_d": "experiment_id",
            "analyser_work_fcn": "analyser_work_function",
            "analyser_retard_gain": "analyser_retardation_gain",
            "reg_image_interval": "register_image_interval",
            "reg_image_mode": "register_image_mode",
            "reg_image_last": "register_image_last",
            "platen_i_d": "platen_id",
            "s_x_i_filename": "sxi_filename",
            "intensity_recal": "intensity_recalibration",
            "intensity_cal_coeff": "intensity_calibration_coefficients",
            "energy_recal": "energy_recalibration",
            "s_c_a_multiplier_voltage": "sca_multiplier_voltage",
            "C60IonGun": "c60_ion_gun",
            "t_f_c_parameters": "tfc_parameters",
            "image_size_x_y": "image_size",
            "float_volt": "float_voltage",
            "float_enable": "float_enabled",
            "grid_volt": "grid_voltage",
            "condensor_volt": "condenser_lens_voltage",
            "objective_volt": "objective_lens_voltage",
            "bend_volt": "bend_voltage",
            "neutral_float_volt": "neutral_float_voltage",
            "neutral_float_enable": "neutral_float_enabled",
            "neutral_grid_volt": "neutral_grid_voltage",
            "neutral_condensor_volt": "neutral_condenser_lens_voltage",
            "neutral_objective_volt": "neutral_objective_lens_voltage",
            "neutral_bend_volt": "neutral_bend_voltage",
            "analyser_mode": "energy_scan_mode",
            "surv_num_cycles": "survey_num_of_cycles",
            "surv_time_per_step": "survey_dwell_time",
            "no_spectral_reg_full": "no_spectral_regions_full",
            "no_spectral_region": "no_spectral_regions",
            "spectral_reg_def_full": "spectral_region_definition_full",
            "spectral_reg_def2_full": "spectral_region_definition2_full",
            "spectral_reg_background_full": "spectral_region_background_full",
            "spectral_reg_hero_full": "spectral_region_hero_full",
            "spectral_reg_i_r_full": "spectral_region_ir_full",
            "no_spectral_reg": "no_spectral_regions",
            "spectral_reg_def": "spectral_region_definition",
            "spectral_reg_def2": "spectral_region_definition2",
            "spectral_reg_background": "spectral_region_background",
            "spectral_reg_hero": "spectral_region_hero",
            "spectral_reg_i_r": "spectral_region_ir",
            "no_spatial_area": "no_spatial_areas",
            "spatial_area_def": "spatial_area_definition",
            "spatial_h_r_photo_cor": "spatial_hr_photo_correction",
            "xray_offset_in_um": "xray_offset",
            "xray_mag_factor": "xray_magnification_factor",
            "xray_rotation_in_deg": "xray_rotation",
            "xray_setting": "xray_settings",
            "neutralizer_current": "flood_gun_current",
            "neutralizer_energy": "flood_gun_energy",
            "flood_gun_filament": "flood_gun_filament_current",
            "detector _acq _time": "detector_acquisition_time",
            "number _of _channels": "number_of_channels",
            "stage_position": "stage_positions",
            "defect_positioner_i_d": "defect_positioner_id",
            "defect_positioner_aligment": "defect_positioner_alignment",
            "gcib_beam": "gcib_high_voltage",
            "gcib_wien": "gcib_wien_filter_voltage",
            "gcib_bend": "gcib_bend_voltage",
            "gcib_magnet": "gcib_magnet_current",
            "auto_e_gun_neut": "auto_flood_gun",
            "auto_ion_neut": "auto_neutral_ion_source",
        }

        self.keys_with_units = [
            "analyser_work_function",
            "source_analyser_angle",
            "analyser_solid_angle",
            "sca_multiplier_voltage",
            "delay_before_acquire",
            "sputter_current",
            "sputter_rate",
            "sputter_energy",
            "float_voltage",
            "target_sputter_time",
            "sputter_emission",
            "grid_voltage",
            "condenser_lens_voltage",
            "objective_lens_voltage",
            "bend_voltage",
            "deflection_bias",
            "ion_gun_gas_pressure",
            "sputter_emission",
            "deflection_bias",
            "neutral_current",
            "neutral_rate",
            "neutral_energy",
            "neutral_float_voltage",
            "neutral_grid_voltage",
            "neutral_condenser_lens_voltage",
            "neutral_objective_lens_voltage",
            "neutral_bend_voltage",
            "neutral_target_timed_on_time",
            "neutral_emission",
            "neutral_deflection_bias",
            "neutral_ion_gun_gas_pressure",
            "survey_dwell_time",
            "xray_anode_power",
            "xray_power",
            "xray_beam_voltage",
            "xray_beam_diameter",
            "xray_condenser_lens_voltage",
            "xray_objective_coil_current",
            "xray_blanking_voltage",
            "xray_filament_current",
            "xray_offset",
            "xray_rotation",
            "xray_emission_current",
            "xray_max_filament_current",
            "flood_gun_current",
            "flood_gun_energy",
            "flood_gun_extractor",
            "flood_gun_filament_current",
            "flood_gun_pulse_length",
            "flood_gun_time_per_step",
            "flood_gun_ramp_rate",
            "sxi_binding_energy",
            "sxi_pass_energy",
            "sxi_lens2_voltage",
            "sxi_lens3_voltage",
            "sxi_lens4_voltage",
            "sxi_lens5_voltage",
            "sxi_rotator",
            "sxi_lens_bias_voltage",
            "sxi_shutter_bias_voltage",
            "detector_acquisition_time",
            "stage_current_rotation_speed",
            "defect_positioner_u",
            "defect_positioner_v",
            "defect_positioner_x",
            "defect_positioner_y",
            "defect_positioner_z",
            "defect_positioner_tilt",
            "defect_positioner_rotation",
            "gcib_sputter_rate",
            "gcib_high_voltage",
            "gcib_ionization",
            "gcib_extractor",
            "gcib_wien_filter_voltage",
            "gcib_bend_voltage",
            "gcib_emission",
            "gcib_magnet_current",
            "gcib_focus",
            "gcib_objective",
            "gcib_focus",
            "gcib_gas_pressure",
            "gcib_cluster_size",
            "gcib_energy_per_atom",
            "deconvolution_pass_energy",
        ]

    def parse_file(self, file, **kwargs):
        """
        Parse the .xy file into a list of dictionaries.

        Parsed data is stored in the attribute 'self.data'.
        Each dictionary in the data list is a grouping of related
        attributes. The dictionaries are later re-structured into a
        nested dictionary that more closely resembles the domain logic.

        Parameters
        ----------
        file : str
            XPS data filepath.

        **kwargs : dict
            commentprefix : str
                Prefix for comments in xy file. The default is "#".
            n_headerlines: int
                number of header_lines in each data block.

        Returns
        -------
        list
            Flat list of dictionaries containing one spectrum each.

        """
        self.lines = self._read_lines(file)
        header, data = self._separate_header_and_data()

        self.parse_header_into_metadata(header)
        # self.parse_data_into_spectra(data)

        self.add_metadata_to_each_spectrum()

        return self.spectra

    def _read_lines(self, file):
        """
        Read in all lines from the file as a list of strings.

        Parameters
        ----------
        file : str
            XPS data filepath.

        Returns
        -------
        None.

        """
        lines = []
        with open(file, encoding="ISO-8859-1") as txt_file:  # "utf-8"
            for line in txt_file:
                lines += [line.strip()]

        return lines

    def _separate_header_and_data(self):
        """
        Separate header (with metadata) from data.

        Returns
        -------
        None.

        """
        in_header = False
        n_headerlines = 0

        for i, line in enumerate(self.lines):
            if "SOFH" in line:
                in_header = True

            elif "EOFH" in line:
                in_header = False
                break

            elif in_header:
                n_headerlines += 1

        header = self.lines[1 : n_headerlines + 1]
        data = self.lines[n_headerlines + 2 :]

        return header, data

    def parse_header_into_metadata(self, header):
        """
        Parse header into PHiMetadata dataclass.

        Parameters
        ----------
        header : str
            Header data for one spectrum as a String.

        """

        def map_keys(key, channel_count):
            """Maps key names for better identification of fields."""
            if key.startswith("neut"):
                key = key.replace("neut_", "neutral_")

            elif key.startswith("x_ray"):
                key = key.replace("x_ray", "xray")

            elif key.startswith("egun_neut"):
                key = key.replace("egun_neut", "flood_gun")

            elif key.startswith("sxi_lens"):
                key += "_voltage"

            elif key.startswith("channel _info"):
                key = f"channel_{channel_count}_info"
                channel_count += 1

            key_map = {
                "desc": "description",
                "defect_pos": "defect_positioner",
                "g_c_i_b": "gcib",
            }

            for old_key, new_key in key_map.items():
                if old_key in key:
                    key = key.replace(old_key, new_key)

            try:
                key = self.settings_map[key]
            except KeyError:
                pass

            return key, channel_count

        channel_count = 1
        datacls_fields = list(self.metadata.__dataclass_fields__.keys())

        unchanged_files = datacls_fields

        for line in header:
            try:
                key, value = line.split(": ")

            except ValueError:
                key = line.strip(": ")
                value = ""

            key = convert_pascal_to_snake(key)
            key, channel_count = map_keys(key, channel_count)

            if key in datacls_fields:
                field_type = type(getattr(self.metadata, key))

                if key in self.keys_with_units:
                    value, unit = self.extract_unit(key, value)
                    setattr(self.metadata, f"{key}_units", unit)
                    unchanged_files.remove(f"{key}_units")

                if not key.startswith("channel_"):
                    value = self.map_values(key, value, field_type)
                else:
                    value = _convert_channel_info(value)

                setattr(self.metadata, key, value)
                unchanged_files.remove(key)
            else:
                print(key, value)

        self.metadata.validate_types()
        if unchanged_files:
            # Make sure all metadata fields have been filled.
            raise AttributeError("Some keys were not updated!")

    def extract_unit(self, key, value):
        """
        Extract units for the metadata containing unit information.

        Example:
            analyser_work_function: 4.506 eV
            -> analyser_work_function: 4.506,
               analyser_work_function_units: eV,

        Parameters
        ----------
        key : str
            Key of the associated value.
        value : str
            Combined unit and value information.

        Returns
        -------
        value :
            value with units.
        unit : str
            Associated unit.


        """
        unit_map = {"seconds": "s", "uA": "micro-A", "(min)": "min"}
        special_cases = {
            "survey_dwell_time": "s",
            "xray_offset": "micro-m",
            "xray_rotation": "degree",
            "Percent": "%",
            "eV/atom": "eV",
        }
        unit_missing = {
            "grid_voltage": "V",
            "condenser_lens_voltage": "V",
            "objective_lens_voltage": "V",
            "bend_voltage": "V",
            "neutral_grid_voltage": "V",
            "neutral_condenser_lens_voltage": "V",
            "neutral_objective_lens_voltage": "V",
            "stage_current_rotation_speed": "degree/s",
            "neutral_bend_voltage": "V",
            "defect_positioner_u": "mm",
            "defect_positioner_v": "mm",
            "defect_positioner_x": "mm",
            "defect_positioner_y": "mm",
            "defect_positioner_z": "mm",
            "defect_positioner_tilt": "degree",
            "defect_positioner_rotation": "degree",
        }

        try:
            value, unit = value.split(" ")
        except ValueError:
            unit = ""
        if unit in unit_map:
            unit = unit_map[unit]
        if key in special_cases:
            unit = special_cases[key]
        if key in unit_missing:
            unit = unit_missing[key]

        return value, unit

    def map_values(self, key, value, field_type):
        """
        Map values to corresponding structure and field type.

        Parameters
        ----------
        key : str
            PhiMetadata dataclass key.
        value : str
            Original value.
        field_type : class
            Class to be mapped onto.

        Returns
        -------
        value
            Value of correct type and internal structure.

        """
        value_function_map = {
            "technique": _convert_experimental_technique,
            "technique_ex": _convert_experimental_technique,
            "file_type": _map_file_type,
            "file_date": _parse_datetime,
            "acquisition_file_date": _parse_datetime,
            "energy_reference": _convert_energy_referencing,
            "intensity_calibration_coefficients": _map_to_list,
            "energy_recalibration": _convert_bool,
            "scan_deflection_span": _map_to_xy,
            "scan_deflection_offset": _map_to_xy,
            "tfc_parameters": _map_to_list,
            "image_size": _map_to_xy,
            "float_enabled": _convert_bool,
            "sputter_raster": _map_to_xy_with_units,
            "sputter_raster_offset": _map_to_xy_with_units,
            "neutral_raster": _map_to_xy_with_units,
            "neutral_raster_offset": _map_to_xy_with_units,
            "energy_scan_mode": _convert_energy_scan_mode,
            "xray_source": _convert_xray_source_params,
            "xray_stigmator": _map_to_xy,
            "xray_magnification_factor": _map_to_xy,
            "xray_delay_factor": _map_to_xy,
            "xray_high_power": _convert_bool,
            "xray_emission_control": _convert_bool,
            "xray_settings": _convert_xray_source_settings,
            "sxi_auto_contrast": _convert_bool,
            "sxi_shutter_bias": _convert_bool,
            "stage_positions": _convert_stage_positions,
            "gcib_raster_size": _map_to_xy_with_units,
            "gcib_raster_offset": _map_to_xy_with_units,
            "auto_flood_gun": _convert_bool,
            "auto_neutral_ion_source": _convert_bool,
            "presputter": _convert_bool,
        }

        if key in value_function_map:
            map_fn = value_function_map[key]
            value = map_fn(value)
        return field_type(value)

    def add_metadata_to_each_spectrum(self):
        """
        Add flattened dict with PhiMetadata fields to each spectrum.

        """
        flattened_metadata = self._flatten_dict(self.metadata.dict())

        for spectrum in self.spectra:
            spectrum.update(flattened_metadata)

    def _flatten_dict(self, metadata_dict):
        """


        Parameters
        ----------
        metadata_dict : dict
            Metadata dict with PhiMetadata fields as keys.

        Returns
        -------
        flattened_dict : dict
            Flatted metadata_dict without any nested substructure.

        """

        def shorten_supkey(supkey):
            shortened_key_map = {
                "xray_source": "xray",
                "xray_settings": "xray",
                "stage_positions": "stage",
            }
            if supkey in shortened_key_map:
                return shortened_key_map[supkey]
            return supkey

        flattened_dict = {}

        for key, value in metadata_dict.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    supkey = shorten_supkey(key)
                    flattened_dict[f"{supkey}_{subkey}"] = subvalue
            else:
                flattened_dict[key] = value

        for key in flattened_dict.copy().keys():
            if "_units" in key:
                new_key = key.replace("_units", "/@units")
                flattened_dict[new_key] = flattened_dict.pop(key)

        return flattened_dict


def convert_pascal_to_snake(str_value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", str_value).lower()


def _map_file_type(value):
    """Map file_type to easily understandable values."""
    value = value.strip()
    file_type_map = {
        "SPECTRUM": "single_spectrum",
        "DEPTHPRO": "depth_profile",
    }

    if value in file_type_map:
        return file_type_map[value]
    return value


def _parse_datetime(value):
    """
    Parse datetime into a datetime.datetime object.

    Parameters
    ----------
    value : str
        String representation of the date in the format
        "%m/%d/%y.

    Returns
    -------
    date_object : str
        Datetime in ISO8601 format.

    """
    year, month, day = value.split(" ")
    date_object = datetime.datetime(year=int(year), month=int(month), day=int(day))

    return date_object.isoformat()


def _convert_bool(value):
    """Convert "yes", "no" to actual boooleans."""
    if value in ["yes", "Yes"]:
        return True
    if value in ["no", "No"]:
        return True
    return None


def _map_to_list(value):
    """Map all items in value to a list."""
    try:
        sep = ", " if ", " in value else " "
        values = value.split(sep)
        values = [float(value) for value in value.split(sep)]
    except ValueError:
        sep = ","
        values = value.split(sep)
        values = [float(value) for value in value.split(sep)]

    return values


def _map_to_xy(value):
    """Map items in value to a dictionary with keys x and y."""
    x, y = value.split(" ")
    return {"x": x, "y": y}


def _map_to_xy_with_units(value):
    """Map items in value to a dictionary with keys x ."""
    x, y, unit = value.split(" ")
    return {"x": x, "x_units": unit, "y": y, "y_units": unit}


def _convert_experimental_technique(value):
    """Map technique to the values defined in NXmpes."""
    measurement_types_map = {
        "XPS": "X-ray photoelectron spectroscopy (XPS)",
        "UPS": "ultraviolet photoelectron spectroscopy (UPS)",
        "ElectronSpectroscopy": "electron spectroscopy for chemical analysis (ESCA)",
        "NAPXPS": "near ambient pressure X-ray photoelectron spectroscopy (NAPXPS)",
        "ARXPS": "angle-resolved X-ray photoelectron spectroscopy (ARXPS)",
    }
    if value in measurement_types_map:
        return measurement_types_map[value]
    return value


def _convert_energy_referencing(value):
    """Map all items in energy_referencing to a dictionary."""
    peak, energy = value.split(" ")
    return {"peak": peak, "energy": energy, "energy_units": "eV"}


def _convert_energy_scan_mode(value):
    """Map energy_scan_mode to the values defined in NXmpes."""
    energy_scan_mode_map = {
        "FixedAnalyzerTransmission": "fixed_analyser_transmission",
        "FAT": "fixed_analyser_transmission",
        "FixedRetardationRatio": "fixed_retardation_ratio",
        "FRR": "fixed_retardation_ratio",
        "FixedEnergies": "fixed_energy",
        "fixed": "fixed_retardation_ratio",
        "Snapshot": "snapshot",
    }

    if value in energy_scan_mode_map:
        return energy_scan_mode_map[value]
    return value


def _convert_channel_info(value):
    """Split channel information into list."""
    channel_number, setting_a, setting_b = value.split(" ")
    return [int(setting_a), float(setting_b)]


def _convert_xray_source_params(value):
    """Map all items in xray_source_params to a dictionary."""
    label, energy, mono = value.split(" ")

    return {
        "anode_material": label,
        "energy": energy,
        "energy_units": "eV",
        "monochromatized": mono,
    }


def _convert_xray_source_settings(value):
    """Map all items in xray_source_settings to a dictionary."""
    (xray_settings) = re.split(r"(\d+)", value)

    unit_map = {"u": "micro-m", "KV": "kV"}

    for i, setting in enumerate(xray_settings):
        if setting in unit_map:
            xray_settings[i] = unit_map[setting]

    return {
        "spot_size": float(xray_settings[1]),
        "spot_size_units": xray_settings[2],
        "power": float(xray_settings[3]),
        "power_units": xray_settings[4],
        "high_voltage": float(xray_settings[5]),
        "high_voltage_units": xray_settings[6],
    }


def _convert_stage_positions(value):
    """Map all items in stage_positions to a dictionary."""
    x, y, z, azimuth, polar = value.split(" ")

    return {
        "x": x,
        "x_units": "mm",
        "y": y,
        "y_units": "mm",
        "z": z,
        "z_units": "mm",
        "azimuth": azimuth,
        "azimuth_units": "degree",
        "polar": polar,
        "polar_units": "degree",
    }


from dataclasses import dataclass
from dataclasses import field


@dataclass
class PhiMetadata:
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
    no_spectral_regions_full: int = 0
    spectral_region_definition_full: str = ""
    spectral_region_definition2_full: str = ""
    spectral_region_background_full: str = ""
    spectral_region_hero_full: str = ""
    spectral_region_ir_full: str = ""
    no_spectral_regions: int = 0
    spectral_region_definition: str = ""
    spectral_region_definition2: str = ""
    spectral_region_background: str = ""
    spectral_region_hero: str = ""
    spectral_region_ir: str = ""
    no_spatial_areas: int = 0
    spatial_area_definition: str = ""
    spatial_area_description: str = ""
    spatial_hr_photo_correction: str = ""

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


# %%
# file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\20240122_SBenz_102_20240122_SBenz_SnO2_10nm.spe"
# file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\20240122_SBenz_107_20240122_SBenz_SnO2_10nm_1.pro"

# file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\metadata.spe"
file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\metadata.pro"


if __name__ == "__main__":
    parser = SpeParser()
    d = parser.parse_file(file)
    d0 = d[0]
