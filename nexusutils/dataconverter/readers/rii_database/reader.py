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
"""Convert refractiveindex.info yaml files to nexus"""
from typing import List, Tuple, Any, Dict
import logging
import pandas as pd
import yaml

from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader
import nexusutils.dataconverter.readers.rii_database.dispersion_functions as dispersion
from nexusutils.dataconverter.readers.utils import parse_json


def read_yml_file(filename: str) -> Dict[Any, Any]:
    """Reads a yml file from disk"""
    with open(filename, 'r', encoding='utf-8') as yml:
        yml_file = yaml.load(
            yml,
            yaml.SafeLoader,
        )

    return yml_file


def read_metadata(yml_file: dict) -> Dict[str, Any]:
    """Reads metadata from a dispersion yaml file"""
    entries: Dict[str, Any] = {}
    if "REFERENCES" in yml_file:
        pass

    if "COMMENTS" in yml_file:
        pass
    return entries


def read_dispersion(filename: str, identifier: str = 'dispersion_x') -> Dict[str, Any]:
    """Reads a rii dispersion from a yaml file"""
    entries: Dict[str, Any] = {}

    def add_table(path: str, nx_name: str, daf: pd.DataFrame):
        disp_path = f'{path}/DISPERSION_TABLE[{nx_name}]'

        if f'{path}/refractive_index' in entries:
            entries[f'{disp_path}/refractive_index'] += daf['refractive_index'].values
            return

        entries[f'{path}/model_name'] = 'Table'
        entries[f'{disp_path}/model_name'] = 'Table'
        entries[f'{disp_path}/convention'] = 'n + ik'
        entries[f'{disp_path}/wavelength'] = daf.index.values
        entries[f'{disp_path}/wavelength/@units'] = 'micrometer'
        entries[f'{disp_path}/refractive_index'] = daf['refractive_index'].values

    def add_model_name(path: str, name: str):
        entries[f'{path}/model_name'] = name

    def add_model_info(path: str, name: str, representation: str, formula: str):
        disp_path = f'{path}/DISPERSION_FUNCTION[{name.lower()}]'

        entries[f'{disp_path}/model_name'] = name
        entries[f'{disp_path}/formula'] = formula
        entries[f'{disp_path}/representation'] = representation
        entries[f'{disp_path}/convention'] = 'n + ik'
        entries[f'{disp_path}/wavelength_identifier'] = 'lambda'
        entries[f'{disp_path}/wavelength_identifier/@units'] = 'micrometer'

        return disp_path

    def add_single_param(path: str, name: str, value: float, unit: str):
        entries[f'{path}/DISPERSION_SINGLE_PARAMETER[{name}]/name'] = name
        entries[f'{path}/DISPERSION_SINGLE_PARAMETER[{name}]/value'] = value
        entries[f'{path}/DISPERSION_SINGLE_PARAMETER[{name}]/value/@units'] = unit

    def add_rep_param(path: str, name: str, values: List[float], units: List[str]):
        if not units:
            raise ValueError('Units must be specified')

        entries[f'{path}/DISPERSION_REPEATED_PARAMETER[{name}]/name'] = name
        entries[f'{path}/DISPERSION_REPEATED_PARAMETER[{name}]/values'] = values
        if len(units) > 1:
            entries[f'{path}/DISPERSION_REPEATED_PARAMETER[{name}]/parameter_units'] = units
        entries[f'{path}/DISPERSION_REPEATED_PARAMETER[{name}]/values/@units'] = units[0]

    yml_file = read_yml_file(filename)
    dispersion_path = f'/ENTRY[entry]/{identifier}'

    model_input = dispersion.ModelInput(
        dispersion_path, [],
        add_model_name, add_model_info, add_single_param, add_rep_param
    )
    table_input = dispersion.TableInput(dispersion_path, '', '', '', add_table)
    for dispersion_relation in yml_file["DATA"]:
        if dispersion_relation['type'] in dispersion.SUPPORTED_TABULAR_PARSERS:
            table_input.table_type = dispersion_relation['type']
            table_input.data = dispersion_relation['data']
            table_input.nx_name = 'dispersion_table'
            dispersion.tabulated(table_input)
            continue

        if dispersion_relation['type'] in dispersion.FORMULA_PARSERS:
            coeffs = list(map(float, dispersion_relation['coefficients'].split()))
            model_input.coeffs = coeffs
            dispersion.FORMULA_PARSERS[dispersion_relation['type']](model_input)
            continue

        raise NotImplementedError(f'No parser for type {dispersion_relation["type"]}')

    # Only read metadata for the ordinary axis
    # as this should be the same for all axes
    if identifier == 'dispersion_x':
        entries.update(read_metadata(yml_file))

    return entries


def fill_dispersion_in(template: Dict[str, Any]):
    """
    Replaces dispersion_x and dispersion_y keys with filenames as their value
    with the parsed dispersion values.
    """
    keys = [f'dispersion_{axis}' for axis in ['y', 'z']]

    for key in keys:
        if key in template:
            template.update(read_dispersion(template[key], identifier=key))
            del template[key]


def parse_json_w_fileinfo(filename: str) -> Dict[str, Any]:
    """
    Reads json key/value pairs and additionally replaces dispersion_x and _y keys
    with their parsed dispersion values.
    """
    template = parse_json(filename)
    fill_dispersion_in(template)

    return template


def handle_objects(objects: Tuple[Any]) -> Dict[str, Any]:
    """Handle objects and generate template entries from them"""
    if objects is None:
        return {}

    template = {}

    for obj in objects:
        if not isinstance(obj, dict):
            logging.warning("Ignoring unknown object of type %s", type(obj))
            continue

        template.update(obj)

    fill_dispersion_in(template)

    return template


def appdef_defaults() -> Dict[str, Any]:
    """Fills default entries which are comment for the application
    definition. Like appdef version and name"""
    entries: Dict[str, Any] = {}

    entries['/ENTRY[entry]/definition/@version'] = '0.0.1'
    entries['/ENTRY[entry]/definition/@url'] = ''
    entries['/ENTRY[entry]/definition'] = 'NXdispersive_material'

    return entries


# pylint: disable=too-few-public-methods
class RiiReader(YamlJsonReader):
    """
    Converts refractiveindex.info yaml files to nexus
    """

    supported_nxdls = ["NXdispersive_material"]
    extensions = {
        ".yml": read_dispersion,
        ".yaml": read_dispersion,
        ".json": parse_json_w_fileinfo,
        "default": lambda _: appdef_defaults(),
        "objects": handle_objects
    }


READER = RiiReader
