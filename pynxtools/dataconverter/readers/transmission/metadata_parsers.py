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
"""Functions for reading metadata values from Perkin Ellmer files"""
from datetime import datetime

# The min & max wavelength the instrument can measure
MIN_WAVELENGTH = 190.
MAX_WAVELENGTH = 3350.


def read_start_date(metadata: list) -> str:
    """Reads the start date from the metadata"""
    century = str(datetime.now().year // 100)
    formated_date = metadata[3].replace("/", "-")
    return f"{century}{formated_date}T{metadata[4]}000Z"


def read_sample_attenuator(metadata: list) -> int:
    """Reads the sample attenuator from the metadata"""
    return int(metadata[47].split()[0].split(":")[1])


def read_ref_attenuator(metadata: list) -> int:
    """Reads the sample attenuator from the metadata"""
    return int(metadata[47].split()[1].split(":")[1])


def read_uv_monochromator_range(metadata: list) -> list:
    """Reads the uv monochromator range from the metadata"""
    monochromator_change = float(metadata[41])
    return [MIN_WAVELENGTH, monochromator_change]


def read_visir_monochromator_range(metadata: list) -> list:
    """Reads the visir monochromator range from the metadata"""
    monochromator_change = float(metadata[41])
    return [monochromator_change, MAX_WAVELENGTH]


def get_d2_range(metadata: list) -> list:
    """Reads the D2 lamp range from the metadata"""
    lamp_change = float(metadata[42])
    return [MIN_WAVELENGTH, lamp_change]


def get_halogen_range(metadata: list) -> list:
    """Reads the halogen lamp range from the metadata"""
    lamp_change = float(metadata[42])
    return [lamp_change, MAX_WAVELENGTH]
