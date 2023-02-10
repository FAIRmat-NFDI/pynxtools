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
"""A dispersion reader for reading dispersion data from a rii yaml file"""
from typing import List, Any, Dict
import numpy as np
import pandas as pd
import yaml

from nexusutils.dataconverter.readers.rii_database.nx_data_writer import NXdataWriter
import nexusutils.dataconverter.readers.rii_database.dispersion_functions as dispersion


class DispersionReader:
    """Reads a rii dispersion from a yml file"""

    def __init__(self):
        self.entries: Dict[str, Any] = {}
        self.single_params: Dict[str, Dict[str, float]] = {}
        self.repeated_params: Dict[str, Dict[str, np.ndarray]] = {}

    def add_table(self, path: str, nx_name: str, tabular_data: pd.DataFrame):
        """Adds a tabular dataframe to the nexus entries dict"""
        disp_path = f"{path}/DISPERSION_TABLE[{nx_name}]"

        if f"{disp_path}/refractive_index" in self.entries:
            if not np.array_equal(
                self.entries[f"{disp_path}/wavelength"], tabular_data.index.values
            ):
                raise ValueError(
                    "Trying to add tabular dispersions with different wavelength ranges"
                )
            self.entries[f"{disp_path}/refractive_index"] += tabular_data[
                "refractive_index"
            ].values
            return

        self.entries[f"{path}/model_name"] = "Table"
        self.entries[f"{disp_path}/model_name"] = "Table"
        self.entries[f"{disp_path}/convention"] = "n + ik"
        self.entries[f"{disp_path}/wavelength"] = tabular_data.index.values
        self.entries[f"{disp_path}/wavelength/@units"] = "micrometer"
        self.entries[f"{disp_path}/refractive_index"] = tabular_data[
            "refractive_index"
        ].values

    def add_model_name(self, path: str, name: str):
        """Adds a model name to the nexus entries dict"""
        self.entries[f"{path}/model_name"] = name

    def add_model_info(
        self,
        dispersion_info: dispersion.DispersionInfo,
        model_input: dispersion.ModelInput,
    ):
        """Adds a model info the the nexus entries dict"""
        disp_path = (
            f"{model_input.dispersion_path}/"
            f"DISPERSION_FUNCTION[{dispersion_info.name.lower()}]"
        )

        if model_input.wavelength_range:
            self.add_wavelength_bounds(disp_path, model_input.wavelength_range)

        self.entries[f"{disp_path}/model_name"] = dispersion_info.name
        representation = dispersion_info.representation
        formula = dispersion_info.formula
        if dispersion_info.representation == "eps" and model_input.convert_to_n:
            representation = "n"
            formula = f"sqrt({dispersion_info.formula})"
        self.entries[f"{disp_path}/formula"] = f"{representation} = {formula}"
        self.entries[f"{disp_path}/representation"] = representation
        self.entries[f"{disp_path}/convention"] = "n + ik"
        self.entries[f"{disp_path}/wavelength_identifier"] = "lambda"
        self.entries[f"{disp_path}/wavelength_identifier/@units"] = "micrometer"

        return disp_path

    def add_single_param(self, path: str, name: str, value: float, unit: str):
        """
        Adds a single parameter to the nexus entries dict and the internal
        single_params dict.
        """
        self.entries[f"{path}/DISPERSION_SINGLE_PARAMETER[{name}]/name"] = name
        self.entries[f"{path}/DISPERSION_SINGLE_PARAMETER[{name}]/value"] = value
        self.entries[f"{path}/DISPERSION_SINGLE_PARAMETER[{name}]/value/@units"] = unit

        single_param_path = self.single_params.setdefault(path, {})
        single_param_path[name] = value

    def add_rep_param(
        self, path: str, name: str, values: List[float], units: List[str]
    ):
        """
        Adds a repeated parameter to the nexus entries dict and the internal
        repeated_params dict
        """
        if not units:
            raise ValueError("Units must be specified")

        self.entries[f"{path}/DISPERSION_REPEATED_PARAMETER[{name}]/name"] = name
        self.entries[f"{path}/DISPERSION_REPEATED_PARAMETER[{name}]/values"] = values
        if len(units) > 1:
            self.entries[
                f"{path}/DISPERSION_REPEATED_PARAMETER[{name}]/parameter_units"
            ] = units
        self.entries[
            f"{path}/DISPERSION_REPEATED_PARAMETER[{name}]/values/@units"
        ] = units[0]

        repeated_param_path = self.repeated_params.setdefault(path, {})
        repeated_param_path[name] = np.array(values)

    def add_wavelength_bounds(self, path: str, bound_str: str):
        """Adds upper and lower wavelength bounds to the nexus entries dict"""
        lower, upper = list(map(float, bound_str.split()))
        self.entries[f"{path}/wavelength_min"] = lower
        self.entries[f"{path}/wavelength_min/@units"] = "micrometer"
        self.entries[f"{path}/wavelength_max"] = upper
        self.entries[f"{path}/wavelength_max/@units"] = "micrometer"

    def read_metadata(self, yml_file: dict):
        """Reads metadata from a dispersion yaml file"""
        if "REFERENCES" in yml_file:
            pass

        if "COMMENTS" in yml_file:
            pass

    def write_dispersions(
        self,
        yml_file: dict,
        table_input: dispersion.TableInput,
        model_input: dispersion.ModelInput,
    ):
        """Writes all dispersions from the dict into the entries dict"""

        def write_dispersion(
            dispersion_relation: Dict[str, Any],
            table_input: dispersion.TableInput,
            model_input: dispersion.ModelInput,
        ):
            """Writes a given dispersion relation into the entries dict"""

            type_to_nx_name = {
                "tabulated k": "dispersion_table_k",
                "tabulated n": "dispersion_table_n",
                "tabulated nk": "dispersion_table_nk",
            }
            if dispersion_relation["type"] in dispersion.SUPPORTED_TABULAR_PARSERS:
                table_input.table_type = dispersion_relation["type"]
                table_input.data = dispersion_relation["data"]
                table_input.nx_name = type_to_nx_name[dispersion_relation["type"]]
                dispersion.tabulated(table_input)
                return

            if dispersion_relation["type"] in dispersion.FORMULA_PARSERS:
                coeffs = list(map(float, dispersion_relation["coefficients"].split()))
                model_input.coeffs = coeffs
                model_input.wavelength_range = dispersion_relation.get(
                    "wavelength_range", None
                )
                dispersion.FORMULA_PARSERS[dispersion_relation["type"]](model_input)
                return

            raise NotImplementedError(
                f'No parser for type {dispersion_relation["type"]}'
            )

        def is_table_k_formula_n_disp(dispersion1: dict, dispersion2: dict):
            """Checks if the two dispersions are one tabular k formula and one formula n"""
            if "tabulated k" == dispersion1["type"] and dispersion2["type"].startswith(
                "formula"
            ):
                return True

            if "tabulated k" == dispersion2["type"] and dispersion1["type"].startswith(
                "formula"
            ):
                return True

            return False

        if len(yml_file["DATA"]) == 2 and is_table_k_formula_n_disp(*yml_file["DATA"]):
            model_input.convert_to_n = True

        for dispersion_relation in yml_file["DATA"]:
            write_dispersion(dispersion_relation, table_input, model_input)

    def read_dispersion(self, filename: str, identifier: str = "dispersion_x"):
        """Reads a dispersion from a yml input file"""
        with open(filename, "r", encoding="utf-8") as yml:
            yml_file = yaml.load(
                yml,
                yaml.SafeLoader,
            )
        dispersion_path = f"/ENTRY[entry]/{identifier}"

        # Only read metadata for the ordinary axis
        # as this should be the same for all axes
        if identifier == "dispersion_x":
            self.read_metadata(yml_file)

        self.write_dispersions(
            yml_file,
            dispersion.TableInput(dispersion_path, "", "", "", self.add_table),
            dispersion.ModelInput(
                dispersion_path,
                [],
                False,
                dispersion.TemplateCallbacks(
                    self.add_model_name,
                    self.add_model_info,
                    self.add_single_param,
                    self.add_rep_param,
                ),
            ),
        )

        self.entries = NXdataWriter(
            self.entries, dispersion_path, self.single_params, self.repeated_params
        ).write_entries()

        return self.entries
