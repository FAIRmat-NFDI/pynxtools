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
"""A writer for writing dispersion models into a corresponding NXdata entry"""
import re
from typing import Set, Any, Dict
import numpy as np
from scipy.interpolate import interp1d

from nexusutils.dataconverter.readers.rii_database.formula_parser.parser import (
    transformation_formula_parser,
)


class NXdataWriter:
    """Extracts/calculates data and writes it to the NXdata entry"""

    def __init__(
        self,
        entries: Dict[str, Any],
        dispersion_path: str,
        single_params: Dict[str, Dict[str, float]],
        repeated_params: Dict[str, Dict[str, np.ndarray]],
    ):
        self.entries = entries
        self.dispersion_path = dispersion_path
        self.single_params = single_params
        self.repeated_params = repeated_params

        self.table_dispersions = self.get_dispersion_names("DISPERSION_TABLE")
        self.func_dispersions = self.get_dispersion_names("DISPERSION_FUNCTION")

    def get_dispersion_names(self, group_name: str):
        """Get all dispersion names of a group"""
        names = set()
        for entry in self.entries:
            if entry.startswith(f"{self.dispersion_path}/{group_name}"):
                names.add(re.search(rf"{group_name}\[([^\]]+)\]", entry).group(1))

        return names

    def get_wavelength_index(self, table_dispersion: str):
        """Get the wavelength and refractive index for a tabular dispersion"""
        wavelength = self.entries[
            f"{self.dispersion_path}/DISPERSION_TABLE[{table_dispersion}]/wavelength"
        ]
        refractive_index = self.entries[
            f"{self.dispersion_path}/DISPERSION_TABLE[{table_dispersion}]/refractive_index"
        ]

        return wavelength, refractive_index

    def get_index(self, wavelength: np.ndarray, func_dispersion: str):
        """
        Get the refractive index of a functional dispersion for a given wavelength array
        """
        x_axis_name = self.entries[
            (
                f"{self.dispersion_path}/DISPERSION_FUNCTION[{func_dispersion}]"
                "/wavelength_identifier"
            )
        ]
        dfpath = f"{self.dispersion_path}/DISPERSION_FUNCTION[{func_dispersion}]"
        formula = self.entries[f"{dfpath}/formula"]

        return transformation_formula_parser(
            x_axis_name,
            wavelength,
            self.single_params.get(dfpath, {}),
            self.repeated_params.get(dfpath, {}),
        ).parse(formula)

    def add_func_dispersions(self, wavelength: np.ndarray, func_dispersions: Set[str]):
        """Sum the refractive indices of functional dispersions"""
        disp_type, refractive_index = self.get_index(wavelength, func_dispersions.pop())
        for func_dispersion in func_dispersions:
            disp_type2, refractive_index2 = self.get_index(wavelength, func_dispersion)
            if disp_type2 != disp_type:
                raise ValueError("Incompatible dispersions")
            refractive_index += refractive_index2

        return disp_type, refractive_index

    def get_wavelength_range(
        self, func_dispersions: Set[str], no_points: int = 500
    ) -> np.ndarray:
        """Get the provided or default wavelength range for a functional dispersion"""
        min_wavelength = -np.inf
        max_wavelength = np.inf
        for func_dispersion in func_dispersions:
            base_path = f"{self.dispersion_path}/DISPERSION_FUNCTION[{func_dispersion}]"
            if f"{base_path}/wavelength_min" in self.entries:
                new_min = self.entries[f"{base_path}/wavelength_min"]
                min_wavelength = new_min if new_min > min_wavelength else min_wavelength

            if f"{base_path}/wavelength_max" in self.entries:
                new_max = self.entries[f"{base_path}/wavelength_max"]
                max_wavelength = new_max if new_max < max_wavelength else max_wavelength

        return np.linspace(
            0.4 if min_wavelength < 0 else min_wavelength,
            1.0 if max_wavelength == np.inf else max_wavelength,
            no_points,
        )

    def write_nx_data(self, wavelength: np.ndarray, refractive_index: np.ndarray):
        """Writes an NXdata group"""
        path = self.dispersion_path
        self.entries[f"{path}/@default"] = "plot"
        self.entries[f"{path}/plot/@axes"] = "wavelength"
        self.entries[f"{path}/plot/@signal"] = "refractive_index"
        self.entries[f"{path}/plot/@auxiliary_signals"] = "extinction"
        self.entries[f"{path}/plot/wavelength"] = wavelength
        self.entries[f"{path}/plot/wavelength/@units"] = "micrometer"
        self.entries[f"{path}/plot/refractive_index"] = refractive_index.real
        self.entries[f"{path}/plot/extinction"] = refractive_index.imag

    def write_func_dispersions_entries(self):
        """Write the functional dispersion entries to the dict"""
        wavelength = self.get_wavelength_range(self.func_dispersions)
        disp_type, refractive_index = self.add_func_dispersions(
            wavelength, self.func_dispersions
        )

        if disp_type == "eps":
            refractive_index = np.emath.sqrt(refractive_index)

        self.write_nx_data(wavelength, refractive_index)

    def write_table_func_dispersions_entries(self):
        """Write the tabular and functional dispersion entries to the dict"""
        wavelength, refractive_index = self.get_wavelength_index(
            self.table_dispersions.pop()
        )
        disp_type, refractive_index_func = self.add_func_dispersions(
            wavelength, self.func_dispersions
        )

        if disp_type == "eps":
            raise ValueError(
                "Incompatible dispersions detected: Tabular and eps-based function"
            )

        self.write_nx_data(wavelength, refractive_index + refractive_index_func)

    def write_table_dispersions_entries(self):
        """Write tabular dispersion entries to the dict"""
        wlen, rindex = self.get_wavelength_index(self.table_dispersions.pop())
        min_wlen = min(wlen)
        max_wlen = max(wlen)
        interpolations = [interp1d(wlen, rindex)]
        for table_dispersion in self.table_dispersions:
            wlen, rindex = self.get_wavelength_index(table_dispersion)
            min_wlen = min(wlen) if min(wlen) > min_wlen else min_wlen
            max_wlen = max(wlen) if max(wlen) < max_wlen else max_wlen
            interpolations.append(interp1d(wlen, rindex))

        wavelength = np.linspace(min_wlen, max_wlen, 500)
        refractive_index = np.zeros(wavelength.shape, np.cdouble)
        for interp in interpolations:
            refractive_index += interp(wavelength)

        self.write_nx_data(wavelength, refractive_index)

    def write_entries(self):
        """Write the NXdata entries to the dict"""
        if len(self.table_dispersions) == 1 and self.func_dispersions:
            self.write_table_func_dispersions_entries()
            return self.entries

        if len(self.table_dispersions) == 0 and self.func_dispersions:
            self.write_func_dispersions_entries()
            return self.entries

        if self.func_dispersions:
            raise ValueError("Unexpected number of dispersions.")

        if not self.table_dispersions:
            raise ValueError("No valid dispersions found.")

        self.write_table_dispersions_entries()
        return self.entries
