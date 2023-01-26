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
from io import StringIO
import pandas as pd
import yaml
from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader


def read_dispersion(filename: str) -> Dict[str, Any]:
    """Reads rii dispersions from yaml files"""
    entries: Dict[str, Any] = {}

    def tabulated_nk(data: str):
        daf = pd.read_table(
            StringIO(data),
            sep='\\s+',
            names=['Wavelength', 'n', 'k']
        )
        daf["Wavelength"] = daf["Wavelength"] * 1000
        daf.set_index("Wavelength", inplace=True)

        bpath = f'{dispersion_path}/DISPERSION_TABLE[dispersion_table]'

        entries[f'{dispersion_path}/model_name'] = 'Table'
        entries[f'{bpath}/model_name'] = 'Table'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength'] = daf.index
        entries[f'{bpath}/wavelength/@units'] = 'micrometer'
        entries[f'{bpath}/refractive_index'] = daf['n'] + 1j * daf['k']

    def tabulated_n(data: str):
        daf = pd.read_table(
            StringIO(data),
            sep="\\s+",
            names=["Wavelength", "n"],
        )
        daf["Wavelength"] = daf["Wavelength"] * 1000
        daf.set_index("Wavelength", inplace=True)

        bpath = f'{dispersion_path}/DISPERSION_TABLE[dispersion_table]'

        entries[f'{dispersion_path}/model_name'] = 'Table'
        entries[f'{bpath}/model_name'] = 'Table'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength'] = daf.index
        entries[f'{bpath}/wavelength/@units'] = 'micrometer'
        entries[f'{bpath}/refractive_index'] = daf['n']

    def tabulated_k(data: str):
        daf = pd.read_table(
            StringIO(data),
            sep="\\s+",
            names=["Wavelength", "k"],
        )
        daf["Wavelength"] = daf["Wavelength"] * 1000
        daf.set_index("Wavelength", inplace=True)

        bpath = f'{dispersion_path}/DISPERSION_TABLE[dispersion_table]'

        entries[f'{dispersion_path}/model_name'] = 'Table'
        entries[f'{bpath}/model_name'] = 'Table'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength'] = daf.index
        entries[f'{bpath}/wavelength/@units'] = 'micrometer'
        entries[f'{bpath}/refractive_index'] = 1j * daf['k']

    def sellmeier_squared(coeffs: List[float]):
        squared_coeffs = list(map(lambda x: x**2, coeffs[2::2]))
        sellmeier(squared_coeffs)

    def sellmeier(coeffs: List[float]):
        bpath = f'{dispersion_path}/DISPERSION_FUNCTION[sellmeier]'

        entries[f'{dispersion_path}/model_name'] = 'Sellmeier'
        entries[f'{bpath}/formula'] = (
            'eps = eps_inf + 1 + sum[A * lambda ** 2 / (lambda ** 2 - B)]'
        )
        entries[f'{bpath}/model_name'] = 'Sellmeier'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength_identifier'] = 'lambda'
        entries[f'{bpath}/wavelength_identifier/@units'] = 'micrometer'
        entries[f'{bpath}/representation'] = 'eps'
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/name'] = ['eps_inf']
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/value'] = coeffs[0]
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/value/@units'] = ['']
        entries[f'{bpath}/REPEATED_PARAMS[A]/name'] = 'A'
        entries[f'{bpath}/REPEATED_PARAMS[A]/values'] = coeffs[1::2]
        entries[f'{bpath}/REPEATED_PARAMS[A]/values/@units'] = ''
        entries[f'{bpath}/REPEATED_PARAMS[B]/name'] = 'B'
        entries[f'{bpath}/REPEATED_PARAMS[B]/values'] = coeffs[2::2]
        entries[f'{bpath}/REPEATED_PARAMS[B]/values/@units'] = 'micrometer**2'

    def polynomial(coeffs: List[float]):
        bpath = f'{dispersion_path}/DISPERSION_FUNCTION[polynomial]'

        entries[f'{dispersion_path}/model_name'] = 'Polynomial'
        entries[f'{bpath}/formula'] = 'eps = eps_inf + sum[f * lambda ** e]'
        entries[f'{bpath}/model_name'] = 'Polynomial'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength_identifier'] = 'lambda'
        entries[f'{bpath}/wavelength_identifier/@units'] = 'micrometer'
        entries[f'{bpath}/representation'] = 'eps'
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/name'] = ['eps_inf']
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/value'] = coeffs[0]
        entries[f'{bpath}/SINGLE_PARAMS[eps_inf]/value/@units'] = ['']
        entries[f'{bpath}/REPEATED_PARAMS[f]/name'] = 'f'
        entries[f'{bpath}/REPEATED_PARAMS[f]/values'] = coeffs[1::2]
        entries[f'{bpath}/REPEATED_PARAMS[f]/units'] = (
            [f'1/micrometer^{e}' for e in coeffs[2::2]]
        )
        entries[f'{bpath}/REPEATED_PARAMS[f]/values/@units'] = (
            entries[f'{bpath}/REPEATED_PARAMS[f]/units']
        )
        entries[f'{bpath}/REPEATED_PARAMS[e]/name'] = 'e'
        entries[f'{bpath}/REPEATED_PARAMS[e]/values'] = coeffs[2::2]
        entries[f'{bpath}/REPEATED_PARAMS[e]/values/@units'] = ''

    def sellmeier_polynomial(coeffs: List[float]):
        bpath_poly = f'{dispersion_path}/DISPERSION_FUNCTION[polynomial]'
        bpath_sellmeier = f'{dispersion_path}/DISPERSION_FUNCTION[sellmeier]'

        entries[f'{dispersion_path}/model_name'] = (
            'Polynomial + Sellmeier (from RefractiveIndex.Info)'
        )
        entries[f'{bpath_poly}/formula'] = 'eps_inf + sum[f * lambda ** e]'
        entries[f'{bpath_poly}/model_name'] = 'Polynomial'
        entries[f'{bpath_poly}/convention'] = 'n + ik'
        entries[f'{bpath_poly}/wavelength_identifier'] = 'lambda'
        entries[f'{bpath_poly}/wavelength_identifier/@units'] = 'micrometer'
        entries[f'{bpath_poly}/representation'] = 'eps'
        entries[f'{bpath_poly}/SINGLE_PARAMS[eps_inf]/name'] = ['eps_inf']
        entries[f'{bpath_poly}/SINGLE_PARAMS[eps_inf]/value'] = coeffs[0]
        entries[f'{bpath_poly}/SINGLE_PARAMS[eps_inf]/value/@units'] = ['']
        entries[f'{bpath_poly}/REPEATED_PARAMS[f]/name'] = 'f'
        entries[f'{bpath_poly}/REPEATED_PARAMS[f]/values'] = coeffs[9::2]
        entries[f'{bpath_poly}/REPEATED_PARAMS[f]/units'] = (
            [f'1/micrometer^{e}' for e in coeffs[10::2]]
        )
        entries[f'{bpath_poly}/REPEATED_PARAMS[f]/values/@units'] = (
            entries[f'{bpath_poly}/REPEATED_PARAMS[f]/units']
        )
        entries[f'{bpath_poly}/REPEATED_PARAMS[e]/name'] = 'e'
        entries[f'{bpath_poly}/REPEATED_PARAMS[e]/values'] = coeffs[10::2]
        entries[f'{bpath_poly}/REPEATED_PARAMS[e]/values/@units'] = ''

        # TODO: This model doesn't make to much sense. e1 should be restricted
        # to 0 or 2, otherwise the units do not match. The formula should be
        # corrected to reflect this.
        entries[f'{bpath_sellmeier}/formula'] = (
            'eps = sum[A * lambda ** e1 / (lambda ** 2 - B**e2)]'
        )
        entries[f'{bpath_sellmeier}/model_name'] = 'Sellmeier'
        entries[f'{bpath_sellmeier}/convention'] = 'n + ik'
        entries[f'{bpath_sellmeier}/wavelength_identifier'] = 'lambda'
        entries[f'{bpath_sellmeier}/wavelength_identifier/@units'] = 'micrometer'
        entries[f'{bpath_sellmeier}/representation'] = 'eps'
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[A]/name'] = 'A'
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[A]/values'] = coeffs[1:6:4]
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[A]/values/@units'] = ''
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[B]/name'] = 'B'
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[B]/values'] = coeffs[3:8:4]
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[B]/units'] = (
            [f'1/micrometer^(2/{e2})' for e2 in coeffs[4:9:4]]
        )
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[B]/values/@units'] = (
            entries[f'{bpath_sellmeier}/REPEATED_PARAMS[B]/units'][0]
        )
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e1]/name'] = 'e1'
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e1]/values'] = coeffs[2:7:4]
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e1]/values/@units'] = ''
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e2]/name'] = 'e2'
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e2]/values'] = coeffs[4:9:4]
        entries[f'{bpath_sellmeier}/REPEATED_PARAMS[e2]/values/@units'] = ''

    def cauchy(coeffs: List[float]):
        bpath = f'{dispersion_path}/DISPERSION_FUNCTION[cauchy]'

        entries[f'{dispersion_path}/model_name'] = 'Cauchy'
        entries[f'{bpath}/formula'] = (
            'n = n_inf + sum[f * lambda ** e]'
        )
        entries[f'{bpath}/model_name'] = 'Cauchy'
        entries[f'{bpath}/convention'] = 'n + ik'
        entries[f'{bpath}/wavelength_identifier'] = 'lambda'
        entries[f'{bpath}/wavelength_identifier/@units'] = 'micrometer'
        entries[f'{bpath}/representation'] = 'eps'
        entries[f'{bpath}/SINGLE_PARAMS[n_inf]/name'] = ['n_inf']
        entries[f'{bpath}/SINGLE_PARAMS[n_inf]/value'] = coeffs[0]
        entries[f'{bpath}/SINGLE_PARAMS[n_inf]/value/@units'] = ['']
        entries[f'{bpath}/REPEATED_PARAMS[f]/name'] = 'f'
        entries[f'{bpath}/REPEATED_PARAMS[f]/values'] = coeffs[1::2]
        entries[f'{bpath}/REPEATED_PARAMS[f]/units'] = (
            [f'1/micrometer^{e}' for e in coeffs[1::2]]
        )
        entries[f'{bpath}/REPEATED_PARAMS[f]/values/@units'] = '1/micrometer'
        entries[f'{bpath}/REPEATED_PARAMS[e]/name'] = 'e'
        entries[f'{bpath}/REPEATED_PARAMS[e]/values'] = coeffs[2::2]
        entries[f'{bpath}/REPEATED_PARAMS[e]/values/@units'] = ''

    def gases(coeffs: List[float]):
        pass

    def herzberger(coeffs: List[float]):
        pass

    def retro(coeffs: List[float]):
        pass

    def exotic(coeffs: List[float]):
        pass

    yml_file = yaml.load(
        filename,
        yaml.SafeLoader,
    )

    dispersion_path = '/ENTRY[entry]/dispersion_x'

    tabular_parsers = {
        'tabluated nk': tabulated_nk,
        'tabulated n': tabulated_n,
        'tabulated k': tabulated_k,
    }

    formula_parsers = {
        'formula 1': sellmeier_squared,
        'formula 2': sellmeier,
        'formula 3': polynomial,
        'formula 4': sellmeier_polynomial,
        'formula 5': cauchy,
        'formula 6': gases,
        'formula 7': herzberger,
        'formula 8': retro,
        'formula 9': exotic,
    }

    for dispersion_relation in yml_file["DATA"]:
        if dispersion_relation['type'] in tabular_parsers:
            tabular_parsers[dispersion_relation['type']](dispersion_relation['data'])
            continue

        if dispersion_relation['type'] in formula_parsers:
            coeffs = list(map(float, dispersion_relation['coefficients'].split()))
            formula_parsers[dispersion_relation['type']](coeffs)
            continue

        raise NotImplementedError(f'No parser for type {dispersion_relation["type"]}')

    return entries


def handle_objects(objects: Tuple[Any]) -> Dict[str, Any]:
    """Handle objects and generate template entries from them"""

    return {}


def appdef_defaults() -> Dict[str, Any]:
    """Fills default entries which are comment for the application
    definition. Like appdef version and name"""
    entries: Dict[str, Any] = {}

    entries['/entry/definition/@version'] = '0.0.1'
    entries['/entry/definition/@url'] = ''
    entries['/entry/definition/'] = 'NXdispersive_material'

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
        "default": lambda _: appdef_defaults(),
        "objects": handle_objects
    }


READER = RiiReader
