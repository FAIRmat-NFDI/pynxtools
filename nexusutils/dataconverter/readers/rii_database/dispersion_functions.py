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
"""Implementation for refractiveindex.info dispersion functions"""
from io import StringIO
from dataclasses import dataclass
from typing import Callable, List
import pandas as pd

ModelNameCallback = Callable[[str, str], None]
ModelInfoCallback = Callable[[str, str, str, str], str]
SingleParamCallback = Callable[[str, str, float, str], None]
RepeatedParamCallback = Callable[[str, str, List[float], List[str]], None]
TableCallback = Callable[[str, str, pd.DataFrame], None]


@dataclass
class ModelInput:
    """The input data and callbacks for the model functions"""
    dispersion_path: str
    coeffs: List[float]
    add_model_name: ModelNameCallback
    add_model_info: ModelInfoCallback
    add_single_param: SingleParamCallback
    add_rep_param: RepeatedParamCallback

@dataclass
class TableInput:
    """The input data and callbacks for tabular dispersions"""
    dispersion_path: str
    nx_name: str
    table_type: str
    data: str
    add_table: TableCallback


def tabulated(table_input: TableInput):
    """
    Parsing for tabulated dispersions from refractiveindex.info
    """
    index_from = {
        'tabulated nk': ['Wavelength', 'n', 'k'],
        'tabulated n': ["Wavelength", "n"],
        'tabulated k': ["Wavelength", "k"],
    }

    daf = pd.read_table(
        StringIO(table_input.data),
        sep='\\s+',
        names=index_from[table_input.table_type]
    )
    daf.set_index("Wavelength", inplace=True)

    daf['refractive_index'] = 0 + 0j
    if 'n' in daf:
        daf.loc[:, 'refractive_index'] += daf['n']
    if 'k' in daf:
        daf.loc[:, 'refractive_index'] += 1j * daf['n']

    table_input.add_table(table_input.dispersion_path, table_input.nx_name, daf)

def sellmeier_squared(model_input: ModelInput):
    """
    The Sellmeier-2 formula (2) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    for i in range(2, len(model_input.coeffs), 2):
        model_input.coeffs[i] = model_input.coeffs[i] ** 2
    sellmeier(model_input)

def sellmeier(model_input: ModelInput):
    """
    The Sellmeier formula (1) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Sellmeier')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Sellmeier',
        'eps',
        'eps = eps_inf + 1 + sum[A * lambda ** 2 / (lambda ** 2 - B)]'
    )

    model_input.add_single_param(path, 'eps_inf', model_input.coeffs[0], '')
    model_input.add_rep_param(path, 'A', model_input.coeffs[1::2], [''])
    model_input.add_rep_param(path, 'B', model_input.coeffs[2::2], ['micrometer**2'])

def polynomial(model_input: ModelInput):
    """
    The Polynomial formula (3) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Polynomial')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Polynomial',
        'eps',
        'eps = eps_inf + sum[f * lambda ** e]'
    )

    model_input.add_single_param(path, 'eps_inf', model_input.coeffs[0], '')
    model_input.add_rep_param(
        path, 'f', model_input.coeffs[1::2], [f'1/micrometer^{e}' for e in model_input.coeffs[2::2]]
    )
    model_input.add_rep_param(path, 'e', model_input.coeffs[2::2], [''])

def sellmeier_polynomial(model_input: ModelInput):
    """
    The Sellmeier Polynomial formula (4) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Polynomial + Sellmeier (from RefractiveIndex.Info)')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Polynomial',
        'eps',
        'eps = eps_inf + sum[f * lambda ** e]'
    )

    model_input.add_single_param(path, 'eps_inf', model_input.coeffs[0], '')
    model_input.add_rep_param(
        path, 'f', model_input.coeffs[9::2],
        [f'1/micrometer^{e}' for e in model_input.coeffs[10::2]]
    )
    model_input.add_rep_param(path, 'e', model_input.coeffs[10::2], [''])

    # Check for valid parameters
    for exp1 in model_input.coeffs[2:7:4]:
        if exp1 not in [0, 2]:
            raise ValueError(f'e1 may only be 0 or 1 but is {exp1}')

    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Sellmeier',
        'eps',
        'eps = sum[A * lambda ** e1 / (lambda ** 2 - B**e2)]'
    )

    model_input.add_rep_param(path, 'A', model_input.coeffs[1:6:4], [''])
    model_input.add_rep_param(
        path, 'B', model_input.coeffs[3:8:4],
        [f'1/micrometer^(2/{e2})' for e2 in model_input.coeffs[4:9:4]]
    )
    model_input.add_rep_param(path, 'e1', model_input.coeffs[2:7:4], [''])
    model_input.add_rep_param(path, 'e2', model_input.coeffs[4:9:4], [''])

def cauchy(model_input: ModelInput):
    """
    The Cauchy formula (5) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Cauchy')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Cauchy',
        'n',
        'n = n_inf + sum[f * lambda ** e]'
    )

    model_input.add_single_param(path, 'n_inf', model_input.coeffs[0], '')
    model_input.add_rep_param(
        path, 'f', model_input.coeffs[1::2], [f'1/micrometer^{e}' for e in model_input.coeffs[2::2]]
    )
    model_input.add_rep_param(path, 'e', model_input.coeffs[2::2], [''])

def gases(model_input: ModelInput):
    """
    The Gases dispersion formula (6) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Gases')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Gases',
        'n',
        'n = 1 + n_inf + sum[A / (B - lambda ** (-2))]'
    )

    model_input.add_single_param(path, 'n_inf', model_input.coeffs[0], '')
    model_input.add_rep_param(path, 'A', model_input.coeffs[1::2], ['1/micrometer^2'])
    model_input.add_rep_param(path, 'B', model_input.coeffs[2::2], ['1/micrometer^2'])

def herzberger(model_input: ModelInput):
    """
    The Herzberger dispersion formula (6) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Herzberger')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Herzberger',
        'n',
        'n = 1 + n_inf + sum[A / (B - lambda ** (-2))]'
    )

    model_input.add_single_param(path, 'n_inf', model_input.coeffs[0], '')
    model_input.add_single_param(path, 'C2', model_input.coeffs[1], 'micrometer^2')
    model_input.add_single_param(path, 'C3', model_input.coeffs[2], 'micrometer^4')
    model_input.add_rep_param(
        path, 'f', model_input.coeffs[3:6], [f'1/micrometer^{e}' for e in [2, 4, 6]]
    )
    model_input.add_rep_param(path, 'e', [2, 4, 6], [''])

def retro(model_input: ModelInput):
    """
    The exotic formula (8) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Retro')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Retro',
        'eps',
        '(eps ** 2 - 1) / (eps + 2) = '
        'eps_inf + C2 * lambda ** 2 / (lambda ** 2 - C3) + C4 * lambda ** 2'
    )

    names = ['eps_inf'] + [f'C{i}' for i in range(1, 5)]
    units = ['', '', 'micrometer^2', 'micrometer^(-2)']

    for name, coeff, unit in zip(names, model_input.coeffs, units):
        model_input.add_single_param(path, name, coeff, unit)


def exotic(model_input: ModelInput):
    """
    The exotic formula (9) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.add_model_name('Exotic')
    path = model_input.add_model_info(
        model_input.dispersion_path,
        'Exotic',
        'eps',
        'eps = eps_inf + C2 / (lambda ** 2 - C3) + '
        'C4 * (lambda - C5) / ((lambda - C5) ** 2 + C6)'
    )

    names = ['eps_inf'] + [f'C{i}' for i in range(1, 7)]
    units = [''] + [f'micrometer{e}' for e in ['^2', '^2', '', '', '^2']]

    for name, coeff, unit in zip(names, model_input.coeffs, units):
        model_input.add_single_param(path, name, coeff, unit)
