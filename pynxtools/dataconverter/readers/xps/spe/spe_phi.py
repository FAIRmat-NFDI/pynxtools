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
from dataclasses import fields
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
            "user": [],
            "instrument": [
                "work_function",
            ],
            "source": [
                "source_label",
            ],
            "beam": ["excitation_energy"],
            "analyser": ["analyser_name"],
            "collectioncolumn": ["lens_mode"],
            "energydispersion": [
                "scan_mode",
                "pass_energy",
            ],
            "detector": [
                "detector_voltage",
            ],
            "manipulator": [],
            "sample": ["target_bias"],
            "calibration": [],
            "data": [
                "x_units",
                "y_units",
                "n_values",
                "start_energy",
                "step_size",
                "dwell_time",
            ],
            "region": [
                "analysis_method",
                "spectrum_type",
                "dwell_time",
                "comments",
                "spectrum_id",
                "time_stamp",
                "scans",
                "spectrum_id",
                "cycle_no",
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
            "calibration": f"{instrument_parent}/calibration",
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

        x_units = spectrum["x_units"]
        energy = np.array(spectrum["data"]["x"])
        intensity = np.array(spectrum["data"]["y"])

        if entry not in self._xps_dict["data"]:
            self._xps_dict["data"][entry] = xr.Dataset()

        # Write raw data to detector.
        self._xps_dict[detector_data_key] = intensity

        if not self.parser.export_settings["Separate Channel Data"]:
            averaged_channels = intensity
        else:
            all_channel_data = [
                value
                for key, value in self._xps_dict.items()
                if detector_data_key.split("Channel_")[0] in key
            ]
            averaged_channels = np.mean(all_channel_data, axis=0)

        if not self.parser.export_settings["Separate Scan Data"]:
            averaged_scans = intensity
        else:
            all_scan_data = [
                value
                for key, value in self._xps_dict.items()
                if detector_data_key.split("Scan_")[0] in key
            ]
            averaged_scans = np.mean(all_scan_data, axis=0)

        # Write to data in order: scan, cycle, channel

        # Write averaged cycle data to 'data'.
        self._xps_dict["data"][entry][scan_key.split("_")[0]] = xr.DataArray(
            data=averaged_scans,
            coords={x_units: energy},
        )
        if self.parser.export_settings["Separate Scan Data"]:
            # Write average cycle data to 'data'.
            self._xps_dict["data"][entry][scan_key] = xr.DataArray(
                data=averaged_channels,
                coords={x_units: energy},
            )

        if (
            self.parser.export_settings["Separate Channel Data"]
            and self.write_channels_to_data
        ):
            # Write channel data to 'data'.
            channel_no = spectrum["channel_no"]
            self._xps_dict["data"][entry][
                f"{scan_key}_chan{channel_no}"
            ] = xr.DataArray(data=intensity, coords={x_units: energy})


# %%


def convert_pascal_to_snake(str_value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", str_value).lower()


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
        self.spectra = []
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
            "image_size_x_y": "image_size_xy",
            "float_volt": "float_voltage",
            "float_enable": "float_enabled",
            "grid_volt": "grid_voltage",
            "condensor_volt": "objective_lens_voltage",
            "objective_volt": "objective_lens_voltage",
            "bend_volt": "bend_voltage",
            "neutral_float_volt": "neutral_float_voltage",
            "neutral_float_enable": "neutral_float_enabled",
            "neutral_grid_volt": "neutral_grid_voltage",
            "neutral_condensor_volt": "neutral_condensor_lens_voltage",
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
            "spectral_reg_hero": "spectral_region_hero_full",
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
            "deflection_bias",
            "ion_gun_gas_pressure",
            "sputter_emission",
            "deflection_bias",
            "neutral_current",
            "neutral_rate",
            "neutral_float_voltage",
            "neutral_grid_voltage",
            "neutral_condensor_lens_voltage",
            "neutral_objective_lens_voltage",
            "neutral_bend_voltage",
            "neutral_gun_gas_pressure",
            "survey_dwell_time",
            "xray_anode_power",
            "xray_power",
            "xray_beam_diameter",
            "x_ray_condenser_lens_voltage",
            "xray_objective_coil_current",
            "xray_filament_current",
            "xray_offset",
            "xray_delay_factor",
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
            "sxi_lens_bias",
            "sxi_shutter_bias_voltage",
            "detector_acquisition_time",
            "stage_current_rotation_speed",
            "gcib_sputter_rate",
            "gcib_beam",
            "gcib_ionization",
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

        # self._add_metadata_to_each_spectrum()

        return self.metadata  # self.spectra

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
        Separate header (with metadata) from data for one measurement
        block

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

        header = self.lines[1:n_headerlines]
        data = self.lines[n_headerlines + 2 :]

        return header, data

    def parse_header_into_metadata(self, header):
        """
        Parse header into metadata dictionary.

        Parameters
        ----------
        header : str
            Header data for one spectrum as a String.

        Returns
        -------
        settings : list
            List of dicts with measurement settings for
            one spectrum each.

        """

        def map_keys(key, channel_count):
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
        datacls_fields = [datacls_field.name for datacls_field in fields(self.metadata)]

        for line in header:
            try:
                key, value = line.split(": ")
            except ValueError:
                key = line.strip(": ")
                value = ""

            key = convert_pascal_to_snake(key)
            key, channel_count = map_keys(key, channel_count)

            if key in datacls_fields:
                value = self.map_values(key, value)

                if key.startswith("channel_"):
                    value = _convert_channel_info(value)

                if key in self.keys_with_units:
                    value, unit = self.extract_unit(key, value)
                    setattr(self.metadata, f"{key}_units", unit)

                setattr(self.metadata, key, value)
                print(key, value)

    def extract_unit(self, key, value):
        """
        analyser_work_function: 4.506 eV
        -> analyser_work_function: 4.506,
           analyser_work_function_units: eV,
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
            "condensor_lens_voltage": "V",
            "objective_lens_voltage": "V",
            "bend_voltage": "V",
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

    def map_values(self, key, value):
        value_function_map = {
            # "file_date": _parse_datetime,
            # "acquisition_file_date": _parse_datetime,
            "energy_reference": _convert_energy_referencing,
            "intensity_calibration_coefficients": _map_to_list,
            "energy_recalibration": _convert_bool,
            "scan_deflection_span": _map_to_list,
            "scan_deflection_offset": _map_to_list,
            "tfc_parameters": _map_to_list,
            "image_size_xy": _map_to_xy,
            "float_enabled": _convert_bool,
            "sputter_raster": _map_to_xy_with_units,
            "sputter_raster_offset": _map_to_xy_with_units,
            "neutral_raster": _map_to_xy_with_units,
            "neutral_raster_offset": _map_to_xy_with_units,
            "energy_scan_mode": _convert_energy_scan_mode,
            "xray_source": _convert_xray_source_params,
            "xray_stigmator": _map_to_xy,
            "xray_magnification_factor": _map_to_xy,
            "x_ray_delay_factor": _map_to_xy,
            "xray_high_power": _convert_bool,
            "xray_emission_control": _convert_bool,
            "xray_settings": _convert_xray_source_settings,
            "sxi_auto_contrast": _convert_bool,
            "sxi_shutter_bias": _convert_bool,
            "stage_positions": _convert_stage_positions,
            "gcib_raster_size": _map_to_xy_with_units,
            "gcib_raster_size_offset": _map_to_xy_with_units,
            "auto_flood_gun": _convert_bool,
            "auto_neutral_ion_source": _convert_bool,
            "presputter": _convert_bool,
        }

        if key in value_function_map:
            map_fn = value_function_map[key]
            new_value = map_fn(value)
            return new_value
        return value


def _parse_datetime(date):
    """
    Parse datetime into a datetime.datetime object.

    Parameters
    ----------
    date : str
        String representation of the date in the format
        "%m/%d/%y %H:%M:%S".

    Returns
    -------
    date_object : datetime.datetime
        Datetime in datetime.datetime format.

    """
    if date.find("UTC"):
        date = date[: date.find("UTC")].strip()
    else:
        date = date.strip()

    date_object = datetime.strptime(date, "%m/%d/%y %H:%M:%S")

    return date_object


def _convert_bool(value):
    if value in ["yes", "Yes"]:
        return True
    if value in ["no", "No"]:
        return True
    return None


def _map_to_list(value):
    sep = ", " if ", " in value else " "
    values = value.split(sep)
    return list(values)


def _map_to_xy(value):
    x, y = value.split(" ")
    return {"x": x, "y": y}


def _map_to_xy_with_units(value):
    x, y, unit = value.split(" ")
    return {"x": x, "x_units": unit, "y": y, "y_units": unit}


def _convert_energy_referencing(value):
    peak, energy = value.split(" ")
    return {"peak": peak, "energy": energy, "energy_units": "eV"}


def _convert_energy_scan_mode(value):
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
    channel_number, setting_a, setting_b = value.split(" ")
    return [int(setting_a), float(setting_b)]


def _convert_xray_source_params(value):
    label, energy, mono = value.split(" ")

    return {
        "anode_material": label,
        "energy": energy,
        "energy_units": "eV",
        "monochromatized": mono,
    }


def _convert_xray_source_settings(value):
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
    file_date: str = ""  # datetime.datetime
    acquisition_file_date: str = ""  # datetime.datetime
    vendor: str = ""
    user_name: str = ""
    experiment_id: str = ""
    energy_reference: list = field(default_factory=list)

    analyser_work_function: str = ""
    analyser_work_function_units: str = ""
    analyser_retardation_gain: float = 0.0
    register_image: bool = False
    register_image_interval: int = 0
    register_image_mode: int = 0
    register_image_last: int = 0
    platen_id: str = ""  # what's that?
    photo_filename: str = ""  # what's that?
    sxi_filename: str = ""  # what's that?
    source_analyser_angle: float = 0.0  # unit
    source_analyser_angle_units: str = ""
    analyser_solid_angle: float = 0.0  # unit
    analyser_solid_angle_units: str = ""
    intensity_recalibration: bool = False
    intensity_calibration_coefficients: list = field(default_factory=list)
    energy_recalibration: bool = False
    scan_deflection_span: list = field(default_factory=list)  # what's that?
    scan_deflection_offset: list = field(default_factory=list)  # what's that?
    sca_multiplier_voltage: float = 0.0
    sca_multiplier_voltage_units: str = ""
    narrow_acceptance_angle: bool = False
    refresh_persistence: int = 0
    peak_to_noise_ratio_state: bool = False
    delay_before_acquire: float = 0.0
    delay_before_acquire_units: str = ""
    c60_ion_gun: str = ""
    bias_box_mode: int = 0
    tfc_parameters: list = field(default_factory=list)
    sem_field_of_view: float = 0.0
    image_size_xy: dict = field(default_factory=list)

    ion_gun_mode: str = ""
    sputter_ion: str = ""
    sputter_current: str = ""
    sputter_rate: str = ""
    sputter_energy: str = ""
    sputter_energy: str = ""
    float_voltage: float = 0.0
    float_voltage_units: str = ""
    float_enabled: bool = False
    grid_voltage: float = 0.0
    grid_voltage_units: str = ""
    condensor_lens_voltage: float = 0.0
    condensor_lens_voltage_units: str = ""
    condensor_lens_voltage: float = 0.0
    condensor_lens_voltage_units: str = ""
    objective_lens_voltage: float = 0.0
    objective_lens_voltage_units: str = ""
    bend_voltage: float = 0.0
    bend_voltage_units: str = ""
    sputter_raster: dict = field(default_factory=list)
    sputter_raster_offset: dict = field(default_factory=list)
    target_sputter_time: float = 0.0
    target_sputter_time_units: str = ""
    sputter_emission: float = 0.0
    sputter_emission_units: str = ""
    deflection_bias: float = 0.0
    deflection_bias_units: str = ""
    ion_gun_gas_pressure: float = 0.0
    ion_gun_gas_pressure_units: str = ""
    target_sputter_time: float = 0.0
    ion_gun_gas_pressure_units: str = ""

    neutral_ion: str = ""
    neutral_current: float = 0.0
    neutral_current_units: str = ""
    neutral_rate: float = 0.0
    neutral_rate_units: str = ""
    neutral_rate: float = 0.0
    neutral_rate_units: str = ""
    neutral_energy: float = 0.0
    neutral_energye_units: str = ""
    neutral_float_voltage: float = 0.0
    neutral_float_voltage_units: str = ""
    neutral_float_enabled: bool = False
    neutral_grid_voltage: float = 0.0
    neutral_grid_voltage_units: str = ""
    neutral_condensor_lens_voltage: float = 0.0
    neutral_condensor_lens_voltage_units: str = ""
    neutral_objective_lens_voltage: float = 0.0
    neutral_objective_lens_voltage_units: str = ""
    neutral_bend_voltage: float = 0.0
    neutral_bend_voltage_units: str = ""
    neutral_gun_gas_pressure: float = 0.0
    neutral_gun_gas_pressure_units: str = ""
    neutral_raster: dict = field(default_factory=list)
    neutral_raster_offset: dict = field(default_factory=list)
    neutral_target_timed_on_time: float = 0.0
    neutral_target_timed_on_time_units: str = ""
    neutral_emission: float = 0.0
    neutral_emission_units: str = ""
    neutral_deflection_bias: float = 0.0
    neutral_deflection_bias_units: str = ""
    neutral_ion_gun_gas_pressure: float = 0.0
    neutral_ion_gun_gas_pressure_units: str = ""

    xps_scan_mode: str = ""
    energy_scan_mode: str = ""
    survey_num_of_cycles: int = 0
    survey_dwell_time: int = 0
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
    spectral_region_background: str = ""
    spatial_area_definition: str = ""
    spatial_area_description: str = ""
    spatial_hr_photo_correction: str = ""

    xray_source: dict = field(default_factory=list)
    xray_anode_position: int = 0
    xray_power: float = 0.0
    xray_power_units: str = ""
    xray_beam_diameter: float = 0.0
    xray_beam_diameter_units: str = ""
    xray_beam_voltage: float = 0.0
    xray_beam_voltage_units: str = ""
    xray_condenser_lens_voltage: float = 0.0
    xray_condenser_lens_voltage_units: str = ""
    xray_objective_coil_current: float = 0.0
    xray_objective_coil_current_units: str = ""
    xray_blanking_voltage: float = 0.0
    xray_blanking_voltage_units: str = ""
    xray_filament_current: float = 0.0
    xray_filament_current_units: str = ""
    xray_stigmator: dict = field(default_factory=list)
    xray_offset: float = 0.0
    xray_offset_units: str = ""
    xray_filament_current: float = 0.0
    xray_filament_current_units: float = 0.0
    xray_stigmator: dict = field(default_factory=list)
    xray_magnification_factor: dict = field(default_factory=list)
    xray_magnification_factor_units: str = ""
    xray_delay_factor: dict = field(default_factory=list)  ## what are the keys?
    xray_delay_factor_units: str = ""
    xray_rotation: float = 0.0
    xray_rotation_units: str = ""
    xray_high_power: bool = False
    xray_emission_control: bool = False
    xray_emission_current: float = 0.0
    xray_rotation_units: str = ""
    xray_step_delay_read_beam: int = 0
    xray_steps_per_diameter: float = 0.0
    xray_interlace_interval: int = 0
    xray_max_filament_current: float = 0.0
    xray_settings: dict = field(default_factory=list)

    flood_gun_mode: str = ""
    flood_gun_current: float = 0.0
    flood_gun_current_units: str = ""
    flood_gun_energy: float = 0.0
    flood_gun_energy_units: str = ""
    flood_gun_extractor: float = 0.0
    flood_gun_extractor_units: str = ""
    flood_gun_x_steering: float = 0.0
    flood_gun_y_steering: float = 0.0
    flood_gun_filament_current: float = 0.0
    flood_gun_filament_current_units: str = ""
    flood_gun_pulse_length: float = 0.0
    flood_gun_pulse_length_units: str = ""
    flood_gun_pulse_frequency: int = 0
    flood_gun_gain: int = 0
    flood_gun_time_per_step: float = 0.0
    flood_gun_time_per_step_units: str = ""
    flood_gun_ramp_rate: float = 0.0
    flood_gun_ramp_rate_units: str = ""

    sxi_persistence: int = 0
    sxi_sec_per_display: float = 0.0
    sxi_auto_contrast: bool = False
    sxi_auto_contrast_low: float = 0.0
    sxi_auto_contrast_high: float = 0.0
    sxi_binding_energy: float = 0.0
    sxi_binding_energy_units: str = ""
    sxi_pass_energy: float = 0.0
    sxi_pass_energy_units: str = ""
    sxi_lens2_voltage: float = 0.0
    sxi_lens2_voltage_units: str = ""
    sxi_lens3_voltage: float = 0.0
    sxi_lens3_voltage_units: str = ""
    sxi_lens4_voltage: float = 0.0
    sxi_lens4_voltage_units: str = ""
    sxi_lens5_voltage: float = 0.0
    sxi_lens5_voltage_units: str = ""
    sxi_rotator: float = 0.0
    sxi_rotator_units: str = ""
    sxi_lens_bias_voltage: float = 0.0
    sxi_lens_bias_voltage_units: str = ""
    sxi_shutter_bias: bool = False
    sxi_shutter_bias_voltage: float = 0.0
    sxi_shutter_bias_voltage_units: str = ""
    sxi_display_mode: int = 0
    detector_acquisition_time: float = 0.0
    detector_acquisition_time_units: str = ""
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
    stage_positions: dict = field(default_factory=list)
    stage_current_rotation_speed: float = 0.0
    stage_current_rotation_speed_units: str = ""

    defect_positioner_id: int = 0
    defect_positioner_comment: int = 0
    defect_positioner_u: float = 0.0
    defect_positioner_u_units: str = ""
    defect_positioner_v: float = 0.0
    defect_positioner_v_units: str = ""
    defect_positioner_x: float = 0.0
    defect_positioner_x_units: str = ""
    defect_positioner_y: float = 0.0
    defect_positioner_y_units: str = ""
    defect_positioner_z: float = 0.0
    defect_positioner_z_units: str = ""
    defect_positioner_tilt: float = 0.0
    defect_positioner_tilt_units: str = ""
    defect_positioner_rotation: float = 0.0
    defect_positioner_rotation_units: str = ""
    defect_positioner_alignment: str = ""
    defect_positioner_reference_image: str = ""

    gcib_sputter_rate: float = 0.0
    gcib_sputter_rate_units: str = ""
    gcib_beam: float = 0.0
    gcib_beam_units: str = ""
    gcib_ionization: float = 0.0
    gcib_ionization_units: str = ""
    gcib_extractor: float = 0.0
    gcib_extractor_units: str = ""
    gcib_raster_size: float = 0.0
    gcib_raster_size_units: str = ""
    gcib_raster_offset: float = 0.0
    gcib_raster_offset_units: str = ""
    gcib_wien_filter_voltage: float = 0.0
    gcib_wien_filter_voltage_units: str = ""
    gcib_bend_voltage: float = 0.0
    gcib_bend_voltage_units: str = ""
    gcib_emission: float = 0.0
    gcib_emission_units: str = ""
    gcib_magnet_current: float = 0.0
    gcib_magnet_current_units: str = ""
    gcib_magnet_current: float = 0.0
    gcib_magnet_current_units: str = ""
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


# %%
# file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\20240122_SBenz_102_20240122_SBenz_SnO2_10nm.spe"

file = r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Benz_PHI_Versaprobe\metadata.spe"

if __name__ == "__main__":
    parser = SpeParser()
    d = parser.parse_file(file)
