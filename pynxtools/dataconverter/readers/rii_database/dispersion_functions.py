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
from typing import Callable, Dict, List, Optional
from numpy import sqrt
import pandas as pd

ModelNameCallback = Callable[[str, str], None]
ModelInfoCallback = Callable[["DispersionInfo", "ModelInput"], str]
SingleParamCallback = Callable[[str, str, float, str], None]
RepeatedParamCallback = Callable[[str, str, List[float], List[str]], None]
TableCallback = Callable[[str, str, pd.DataFrame], None]


@dataclass
class TemplateCallbacks:
    """Contains callbacks to write model infos into the nexus template"""

    add_model_name: ModelNameCallback
    add_model_info: ModelInfoCallback
    add_single_param: SingleParamCallback
    add_rep_param: RepeatedParamCallback


@dataclass
class ModelInput:
    """The input data and callbacks for the model functions"""

    dispersion_path: str
    coeffs: List[float]
    convert_to_n: bool
    callbacks: TemplateCallbacks
    wavelength_range: Optional[str] = None


@dataclass
class DispersionInfo:
    """Holds information about a dispersion"""

    name: str
    representation: str
    formula: str


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
        "tabulated nk": ["Wavelength", "n", "k"],
        "tabulated n": ["Wavelength", "n"],
        "tabulated k": ["Wavelength", "k"],
    }

    refractive_index = pd.read_table(
        StringIO(table_input.data), sep="\\s+", names=index_from[table_input.table_type]
    )
    refractive_index.set_index("Wavelength", inplace=True)

    refractive_index["refractive_index"] = 0 + 0j
    if "n" in refractive_index:
        refractive_index.loc[:, "refractive_index"] += refractive_index["n"]
    if "k" in refractive_index:
        refractive_index.loc[:, "refractive_index"] += 1j * refractive_index["k"]

    table_input.add_table(
        table_input.dispersion_path, table_input.nx_name, refractive_index
    )


def sellmeier_squared(model_input: ModelInput):
    """
    The Sellmeier formula (1) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Sellmeier")
    path = model_input.callbacks.add_model_info(
        DispersionInfo(
            "Sellmeier",
            "eps",
            "eps_inf + 1 + sum[A * lambda ** 2 / (lambda ** 2 - B ** 2)]",
        ),
        model_input,
    )

    model_input.callbacks.add_single_param(path, "eps_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_rep_param(path, "A", model_input.coeffs[1::2], [""])
    model_input.callbacks.add_rep_param(
        path, "B", model_input.coeffs[2::2], ["micrometer"]
    )


def sellmeier(model_input: ModelInput):
    """
    The Sellmeier-2 formula (2) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    for i in range(2, len(model_input.coeffs), 2):
        model_input.coeffs[i] = sqrt(model_input.coeffs[i])
    sellmeier_squared(model_input)


def polynomial(model_input: ModelInput):
    """
    The Polynomial formula (3) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Polynomial")
    path = model_input.callbacks.add_model_info(
        DispersionInfo("Polynomial", "eps", "eps_inf + sum[f * lambda ** e]"),
        model_input,
    )

    model_input.callbacks.add_single_param(path, "eps_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_rep_param(
        path,
        "f",
        model_input.coeffs[1::2],
        [f"1/micrometer^{e}" for e in model_input.coeffs[2::2]],
    )
    model_input.callbacks.add_rep_param(path, "e", model_input.coeffs[2::2], [""])


def sellmeier_polynomial(model_input: ModelInput):
    """
    The Sellmeier Polynomial formula (4) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Sellmeier")

    a_units = []
    # Check for valid parameters
    for exponent1 in model_input.coeffs[2:7:4]:
        if exponent1 not in [0, 2]:
            raise ValueError(f"e1 may only be 0 or 1 but is {exponent1}")
        a_units.append("" if exponent1 == 0 else "1/micrometer^2")

    path = model_input.callbacks.add_model_info(
        DispersionInfo(
            "Sellmeier",
            "eps",
            "eps_inf + sum[A * lambda ** e1 / (lambda ** 2 - B**e2)]",
        ),
        model_input,
    )

    model_input.callbacks.add_single_param(path, "eps_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_rep_param(path, "A", model_input.coeffs[1:6:4], a_units)
    model_input.callbacks.add_rep_param(
        path,
        "B",
        model_input.coeffs[3:8:4],
        [f"micrometer^(2/{e2})" for e2 in model_input.coeffs[4:9:4]],
    )
    model_input.callbacks.add_rep_param(path, "e1", model_input.coeffs[2:7:4], [""])
    model_input.callbacks.add_rep_param(path, "e2", model_input.coeffs[4:9:4], [""])

    # If there are just 9 parameters don't append polynomial part
    if len(model_input.coeffs) <= 9:
        return

    model_input.callbacks.add_model_name(
        model_input.dispersion_path,
        "Polynomial + Sellmeier (from RefractiveIndex.Info)",
    )
    path = model_input.callbacks.add_model_info(
        DispersionInfo("Polynomial", "eps", "sum[f * lambda ** e]"),
        model_input,
    )

    model_input.callbacks.add_rep_param(
        path,
        "f",
        model_input.coeffs[9::2],
        [f"1/micrometer^{e}" for e in model_input.coeffs[10::2]],
    )
    model_input.callbacks.add_rep_param(path, "e", model_input.coeffs[10::2], [""])


def cauchy(model_input: ModelInput):
    """
    The Cauchy formula (5) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Cauchy")
    path = model_input.callbacks.add_model_info(
        DispersionInfo("Cauchy", "n", "n_inf + sum[f * lambda ** e]"), model_input
    )

    model_input.callbacks.add_single_param(path, "n_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_rep_param(
        path,
        "f",
        model_input.coeffs[1::2],
        [f"1/micrometer^{e}" for e in model_input.coeffs[2::2]],
    )
    model_input.callbacks.add_rep_param(path, "e", model_input.coeffs[2::2], [""])


def gases(model_input: ModelInput):
    """
    The Gases dispersion formula (6) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Gases")
    path = model_input.callbacks.add_model_info(
        DispersionInfo("Gases", "n", "1 + n_inf + sum[A / (B - lambda ** (-2))]"),
        model_input,
    )

    model_input.callbacks.add_single_param(path, "n_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_rep_param(
        path, "A", model_input.coeffs[1::2], ["1/micrometer^2"]
    )
    model_input.callbacks.add_rep_param(
        path, "B", model_input.coeffs[2::2], ["1/micrometer^2"]
    )


def herzberger(model_input: ModelInput):
    """
    The Herzberger dispersion formula (6) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Herzberger")
    path = model_input.callbacks.add_model_info(
        DispersionInfo(
            "Herzberger",
            "n",
            "n_inf + C2 / (lambda ** 2 - B1) + "
            "C3 * (lambda ** 2 - B2) ** (-2) + "
            "sum[f * lambda ** e]",
        ),
        model_input,
    )

    f_coeffs = model_input.coeffs[3:6] + [0.0] * (3 - len(model_input.coeffs[3:6]))

    model_input.callbacks.add_single_param(path, "n_inf", model_input.coeffs[0], "")
    model_input.callbacks.add_single_param(
        path, "C2", model_input.coeffs[1], "micrometer^2"
    )
    model_input.callbacks.add_single_param(
        path, "C3", model_input.coeffs[2], "micrometer^4"
    )
    model_input.callbacks.add_single_param(path, "B1", 0.028, "micrometer^2")
    model_input.callbacks.add_single_param(path, "B2", 0.028, "micrometer^2")
    model_input.callbacks.add_rep_param(
        path, "f", f_coeffs, [f"1/micrometer^{e}" for e in [2, 4, 6]]
    )
    model_input.callbacks.add_rep_param(path, "e", [2, 4, 6], [""])


def retro(model_input: ModelInput):
    """
    The exotic formula (8) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Retro")
    path = model_input.callbacks.add_model_info(
        DispersionInfo(
            "Retro",
            "eps",
            "(lambda ** 2 * (2 * A + 2 * B + 2 * D * lambda ** 2 + 1) "
            "- C * (2 * A + 2 * D * lambda ** 2 + 1)) "
            "/ (C * (A + D * lambda ** 2 - 1) - "
            "lambda ** 2 * (A + B + D * lambda ** 2 - 1))",
        ),
        model_input,
    )

    names = ["eps_inf", "A", "B", "C", "D"]
    units = ["", "", "", "micrometer^2", "micrometer^(-2)"]

    model_input.coeffs += [0.0] * (len(names) - len(model_input.coeffs))

    for name, coeff, unit in zip(names, model_input.coeffs, units):
        model_input.callbacks.add_single_param(path, name, coeff, unit)


def exotic(model_input: ModelInput):
    """
    The exotic formula (9) from refractiveindex.info
    See https://refractiveindex.info/database/doc/Dispersion%20formulas.pdf
    for a reference.
    """
    model_input.callbacks.add_model_name(model_input.dispersion_path, "Exotic")
    path = model_input.callbacks.add_model_info(
        DispersionInfo(
            "Exotic",
            "eps",
            "eps_inf + C2 / (lambda ** 2 - C3) + "
            "C4 * (lambda - C5) / ((lambda - C5) ** 2 + C6)",
        ),
        model_input,
    )

    names = ["eps_inf"] + [f"C{i}" for i in range(2, 7)]
    units = ["", "micrometer^2", "micrometer^2", "", "micrometer", "micrometer^2"]
    model_input.coeffs += [0.0] * (len(names) - len(model_input.coeffs))

    for name, coeff, unit in zip(names, model_input.coeffs, units):
        model_input.callbacks.add_single_param(path, name, coeff, unit)


SUPPORTED_TABULAR_PARSERS = [f"tabulated {t}" for t in ["nk", "n", "k"]]


FORMULA_PARSERS: Dict[str, Callable[[ModelInput], None]] = {
    "formula 1": sellmeier_squared,
    "formula 2": sellmeier,
    "formula 3": polynomial,
    "formula 4": sellmeier_polynomial,
    "formula 5": cauchy,
    "formula 6": gases,
    "formula 7": herzberger,
    "formula 8": retro,
    "formula 9": exotic,
}
