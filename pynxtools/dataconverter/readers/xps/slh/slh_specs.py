"""
Parser for reading XPS (X-ray Photoelectron Spectroscopy) metadata
from native Specs Lab Prodigy SLH format, to be passed to mpes nxdl
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

# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes

import re
import pandas as pd
from copy import copy
import sqlite3
from datetime import datetime
import numpy as np


class SlhMapperSpecs:
    """
    Class for restructuring .sle data file from
    specs vendor into python dictionary.
    """

    def __init__(self):
        self.parsers = [
            SlhProdigyParser,
        ]

        self.versions_map = {}
        for parser in self.parsers:
            supported_versions = parser.supported_versions
            for version in supported_versions:
                self.versions_map[version] = parser

        self.file = None

        self.raw_data: list = []
        self._xps_dict: dict = {}

        self._root_path = "/ENTRY[entry]"

    @property
    def data_dict(self) -> dict:
        """Getter property."""
        return self._xps_dict

    def _get_slh_version(self):
        """Get the Prodigy SLH version from the file."""
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        query = 'SELECT Value FROM Configuration WHERE Key=="Version"'
        version = cur.execute(query).fetchall()[0][0]
        version = version.split(".")
        version = version[0] + "." + version[1].split("-")[0]
        return version

    def _get_version(self, kind):
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        query_param = (kind,)
        query = "SELECT Value FROM Configuration WHERE Key=?"
        version = cur.execute(query, query_param).fetchall()[0][0].split(".")
        version = version[0] + "." + version[1].split("-")[0]
        return version

    def parse_file(self, file, **kwargs):
        """
        Parse the file using the parser that fits the Prodigy SLE version.
        Returns flat list of dictionaries containing one spectrum each.

        """
        self.file = file
        datamodel_version = self._get_version("Version")
        prodigy_version = self._get_version("AppVersion")

        parser = self.versions_map[datamodel_version]()
        self.raw_data = parser.parse_file(file, **kwargs)

        # file_key = f"{self._root_path}/Files"
        # self._xps_dict[file_key] = file

        # self.construct_data()

        return self.data_dict

    def construct_data(self):
        """Map SLH format to NXmpes-ready dict."""
        spectra = copy.deepcopy(self.raw_data)

        self._xps_dict["data"]: dict = {}

        key_map = {
            "user": [],
            "instrument": [],
            "source": [],
            "beam": [],
            "analyser": [],
            "collectioncolumn": [],
            "energydispersion": [],
            "detector": [],
            "manipulator": [],
            "calibration": [],
            "data": [],
            "region": [],
        }

        for spectrum in spectra:
            self._update_xps_dict_with_spectrum(spectrum, key_map)

    def _update_xps_dict_with_spectrum(self, spectrum, key_map):
        """
        Map one spectrum from raw data to NXmpes-ready dict.

        """
        # pylint: disable=too-many-locals
        group_parent = f'{self._root_path}/RegionGroup_{spectrum["group_name"]}'
        region_parent = f'{group_parent}/regions/RegionData_{spectrum["spectrum_type"]}'
        instrument_parent = f"{region_parent}/instrument"
        analyser_parent = f"{instrument_parent}/analyser"

        path_map = {
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
                    units = re.search(r"\[([A-Za-z0-9_]+)\]", spectrum_key).group(1)
                    mpes_key = spectrum_key.rsplit(" ", 1)[0]
                    self._xps_dict[f"{root}/{mpes_key}/@units"] = units
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]
                except AttributeError:
                    mpes_key = spectrum_key
                    self._xps_dict[f"{root}/{mpes_key}"] = spectrum[spectrum_key]

        self._xps_dict[f'{path_map["analyser"]}/name'] = spectrum["devices"][0]
        self._xps_dict[f'{path_map["source"]}/name'] = spectrum["devices"][1]


class SlhProdigyParser:
    """
    Generic parser without reading capabilities,
    to be used as template for implementing parsers for different versions.
    """

    supported_versions = ["0.6"]
    supported_prodigy_versions = ["1.2", "1.8", "1.9", "1.10", "1.11", "1.12", "1.13"]

    def __init__(self):
        self.con = ""
        self.data = pd.DataFrame()
        self.con = None

        keys_map = {
            "Udet": "detector_voltage",
            "Comment": "comments",
            "ElectronEnergy": "start_energy",
            "SpectrumID": "spectrum_id",
            "EpassOrRR": "pass_energy",
            "EnergyType": "x_units",
            "Samples": "n_values",
            "Wf": "workfunction",
            "Step": "step",
            "Ubias": "electron_bias",
            "DwellTime": "dwell_time",
            "NumScans": "total_scans",
            "LensMode": "lens_mode",
            "Timestamp": "time_stamp",
            "Entrance": "entrance_slit",
            "Exit": "exit_slit",
            "ScanMode": "scan_mode",
            "VoltageRange": "detector_voltage_range",
        }

        spectrometer_setting_map = {
            "Coil Current [mA]": "coil_current [mA]",
            "Pre Defl Y [nU]": "pre_deflector_y_current [nU]",
            "Pre Defl X [nU]": "pre_deflector_x_current [nU]",
            "L1 [nU]": "lens1_voltage [nU]",
            "L2 [nU]": "lens2_voltage [nU]",
            "Focus Displacement 1 [nu]": "focus_displacement_current [nU]",
            "Detector Voltage [V]": "detector_voltage [V]",
            "Bias Voltage Electrons [V]": "bias_voltage_electrons [V]",
            "Bias Voltage Ions [V]": "bias_voltage_ions [V]",
        }

        source_setting_map = {
            "anode": "source_label",
            "uanode": "source_voltage",
            "iemission": "emission_current",
            "ihv": "source_high_voltage",
            "ufilament": "filament_voltage",
            "ifilament": "filament_current",
            "DeviceExcitationEnergy": "excitation_energy",
            "panode": "anode_power",
            "temperature": "source_temperature",
        }

        self.sql_metadata_map = {
            "EnergyType": "x_units",
            "EpassOrRR": "pass_energy",
            "Wf": "workfunction",
            "Timestamp": "time_stamp",
            "Samples": "n_values",
            "ElectronEnergy": "start_energy",
            "Step": "step_size",
        }

        self.key_maps = [
            keys_map,
            spectrometer_setting_map,
            source_setting_map,
            self.sql_metadata_map,
        ]

        # =============================================================================
        #         self.value_map = {
        #             "x_units": self._change_energy_type,
        #             "time_stamp": self._convert_date_time,
        #         }
        # =============================================================================

        self.encoding = ["f", 4]

    def initiate_file_connection(self, file):
        """
        Initiate connection to SQLite DB.

        Parameters
        ----------
        file : str
            Filename of the parameter file.

        Returns
        -------
        None.

        """
        self.con = sqlite3.connect(file)

    def _close_con(self):
        """
        Close the database connection.

        Returns
        -------
        None.

        """
        self.con.close()

    def parse_file(self, file, **kwargs):
        """
        Parse the file's metadata into a flat list of dictionaries.


        Parameters
        ----------
        file : str
            Filepath of the SLE file to be read.

        Returns
        -------
        self.spectra
            Flat list of dictionaries containing measured
            metadata of one parameter each.

        """
        # initiate connection to sql file
        self.initiate_file_connection(file)

        # read and parse sle file
        param_df = self._get_parameter_metadata()
        # parameter_info = self._get_parameter_info()
        data = self._get_data_for_param_df(param_df)

        df = param_df.update(data)

        return data  # df.to_dict(orient="records")

    def _get_parameter_metadata(self):
        """

        Returns
        -------
        None.

        """
        cur = self.con.cursor()
        query = "SELECT * FROM 'ParameterHistory'"
        results = cur.execute(query).fetchall()

        columns = [
            "id",
            "name",
            "unique_device_name",
            "device",
            "measured_param",
            "base_time",
        ]
        df = pd.DataFrame(columns=columns)

        for result in results:
            new_row = {}
            for key, value in zip(columns, result):
                if key == "base_time":
                    # convert base time to time stamp
                    value = datetime.strptime(value, "%Y-%b-%d %H:%M:%S.%f")
                new_row[key] = value

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.set_index("id", drop=True, inplace=True)

        return df

    def _get_parameter_info(self):
        """

        Returns
        -------
        None.

        """
        parameter_info = []
        cur = self.con.cursor()
        query = "SELECT ID, DeviceType, Command, ReadablePar, Unit, Scaling, Representation FROM ParameterInfo"
        results = cur.execute(query).fetchall()

        columns = [
            "id",
            "device_type",
            "command",
            "readable_parameter",
            "unit",
            "scaling",
            "representation",
        ]

        for result in results:
            param_dict = {}
            for key, value in zip(columns, result):
                param_dict[key] = value

            parameter_info += [param_dict]
        return parameter_info

    def _get_data_for_param_df(self, param_df):
        data_df = pd.DataFrame()

        for ID, row in param_df.iterrows():
            cur = self.con.cursor()
            query = f"SELECT Observation, Offset_s FROM 'NumericalHistoryData' WHERE ID={ID}"
            data = cur.execute(query).fetchall()

            data = pd.DataFrame(data)
            data.columns = ["Observation", "Offset_s"]
            data["date_time"] = (
                pd.TimedeltaIndex(data.Offset_s, unit="s") + row["base_time"]
            )
            data = self._resample_df(data, interval="1s").reindex()
            print(data.head())
            data = data.to_dict(orient="list")

            data_df = pd.concat([data_df, pd.DataFrame([data])], ignore_index=True)

        return data_df

    def _resample_df(self, df, interval="1s"):
        df_resampled = df.copy()
        # Resample to 1s intervals

        df_resampled = df_resampled.resample(
            interval, on="date_time", label="right"
        ).mean()
        # If a value is not given, take the previous value
        df_resampled["Observation"] = df_resampled["Observation"].ffill()
        df_resampled["Offset_s"] = df_resampled["Offset_s"].ffill()

        return df_resampled

    def _check_encoding(self):
        """
        Check whether the binary data should be decoded float or double.

        Returns
        -------
        None.

        """
        cur = self.con.cursor()
        query = "SELECT LENGTH(Data),ChunkSize FROM CountRateData LIMIT 1"
        cur.execute(query)
        data, chunksize = cur.fetchall()[0]

        encodings_map = {
            "double": ["d", 8],
            "float": ["f", 4],
        }

        if data / chunksize == 4:
            self.encoding = encodings_map["float"]
        elif data / chunksize == 8:
            self.encoding = encodings_map["double"]
        else:
            print("This binary encoding is not supported.")

    def _convert_date_time(self, timestamp):
        """
        Convert the native time format to the one we decide to use.
        Returns datetime string in the format '%Y-%b-%d %H:%M:%S.%f'.

        """
        date_time = datetime.strptime(timestamp, "%Y-%b-%d %H:%M:%S.%f")
        date_time = datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        return date_time

    def _re_map_keys(self, dictionary, key_map):
        """
        Map the keys returned from the SQL table to the preferred keys for
        the parser output.

        """
        keys = list(key_map.keys())
        for k in keys:
            if k in dictionary.keys():
                dictionary[key_map[k]] = dictionary.pop(k)
        return dictionary

    def _drop_unused_keys(self, dictionary, keys_to_drop):
        """
        Remove any keys parsed from sle that are not needed

        Parameters
        ----------
        dictionary : dict
            Dictionary with data and metadata for a spectrum.
        keys_to_drop : list
            List of metadata keys that are not needed.

        Returns
        -------
        None.

        """
        for key in keys_to_drop:
            if key in dictionary.keys():
                dictionary.pop(key)

    def _re_map_values(self, dictionary):
        """
        Map the values returned from the SQL table to the preferred format.

        Parameters
        ----------
        dictionary : dict
            Dictionary with data and metadata for a spectrum.

        Returns
        -------
        dictionary : dict
            Dictionary with data and metadata for a spectrum with
            preferred keys for values.

        """
        for key, values in self.value_map.items():
            dictionary[key] = values(dictionary[key])
        return dictionary

    def _convert_to_common_format(self):
        """
        Reformat spectra into the format needed for the Converter object
        """
        maps = {}
        for key_map in self.key_maps:
            maps.update(key_map)
        for spec in self.spectra:
            self._re_map_keys(spec, maps)
            self._re_map_values(spec)
            self._drop_unused_keys(spec, self.keys_to_drop)
            spec["data"] = {}
            spec["data"]["x"] = self._get_energy_data(spec)

            channels = [
                key
                for key in spec
                if any(name in key for name in ["cps_ch_", "cps_calib"])
            ]

            for channel_key in channels:
                spec["data"][channel_key] = np.array(spec[channel_key])
            for channel_key in channels:
                spec.pop(channel_key)

            spec["y_units"] = "Counts per Second"


if __name__ == "__main__":
    from pathlib import Path

    def _parse_data(mapper, files, **kwargs):
        raw_data = []
        data = []

        for file in files:
            m = mapper()
            d = m.parse_file(file=file, **kwargs)
            data.append(d)
            raw_data.append(m.raw_data)

        return raw_data, data

    folder = Path(
        r"C:\Users\pielsticker\Lukas\FAIRMat\user_cases\Pielsticker_XPS_MPI-CEC\EX889_S1110_MgFe2O4_spent\slh"
    )
    files = [
        "20230824_xray.slh",
        # "EX889-890_nap_parameters.slh"
    ]
    files = [Path(folder, file) for file in files]
    mapper = SlhMapperSpecs
    raw_data, data = _parse_data(mapper, files)
    d = raw_data[0]
