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
"""Parse human-readable composition infos from set of ELN string text fields."""

# pylint: disable=no-member,too-many-branches

import re
import numpy as np

from ase.data import chemical_symbols


def parse_human_readable_composition_case_one(symbol):
    """Handle specification of matrix or remainder element."""
    return ("define_matrix", symbol, None, None, None)


def parse_human_readable_composition_case_two(args, symbol):
    """Handle case element and at.-% composition, no comp. stdev."""
    if args[1] in ["rem", "remainder", "matrix"]:
        return ("define_matrix", symbol, None, None, None)
    composition = re.match(r"[-+]?(?:\d*\.*\d+)", args[1])
    if composition is not None:
        fraction = np.float64(composition[0])
        return ("add_element", symbol, fraction, None, "at.-%")
    return (None, None, None, None, None)


def parse_human_readable_composition_case_three(human_input, args, symbol):
    """Handle case element with different than default normalization, no comp. stdev."""
    composition = re.findall(r"[-+]?(?:\d*\.*\d+)", human_input)
    if len(composition) == 1:
        fraction = np.float64(composition[0])
        normalization = args[2]
        if normalization in ["%", "at%", "at-%", "at.-%"]:
            return ("add_element", symbol, fraction, None, "at.-%")
        if normalization in ["wt%", "wt-%", "wt.-%"]:
            return ("add_element", symbol, fraction, None, "wt.-%")
        if normalization == "ppm":
            return ("add_element", symbol, fraction / 1.0e4, None, "at.-%")
        if normalization == "ppb":
            return ("add_element", symbol, fraction / 1.0e7, None, "at.-%")
    return (None, None, None, None, None)


def parse_human_readable_composition_case_four(human_input, symbol):
    """Handle case at.-% normalization with comp. stdev."""
    composition = re.findall(r"[-+]?(?:\d*\.*\d+)", human_input)
    composition_error = human_input.count("+-")
    if (len(composition) == 2) and (composition_error == 1):
        fraction = np.float64(composition[0])
        error = np.float64(composition[1])
        return ("add_element", symbol, fraction, error, "at.-%")
    return (None, None, None, None, None)


def parse_human_readable_composition_case_five(human_input, args, symbol):
    """Handle case with different than standard normalization and comp. stdev."""
    composition = re.findall(r"[-+]?(?:\d*\.*\d+)", human_input)
    if (len(composition) == 2) and (human_input.count("+-") == 1):
        fraction = np.float64(composition[0])
        error = np.float64(composition[1])
        normalization = args[2]
        if normalization in ["%", "at%", "at-%", "at.-%"]:
            return ("add_element", symbol, fraction, error, "at.-%")
        if normalization in ["wt%", "wt-%", "wt.-%"]:
            return ("add_element", symbol, fraction, error, "wt.-%")
        if normalization == "ppm":
            return ("add_element", symbol, fraction / 1.0e4, error / 1.0e4, "at.-%")
        if normalization == "ppb":
            return ("add_element", symbol, fraction / 1.0e7, error / 1.0e7, "at.-%")
    return (None, None, None, None, None)


def parse_human_readable_composition_information(eln_input):
    """Identify instruction to parse from eln_input to define composition table."""
    args = eln_input.split(" ")
    if len(args) >= 1:
        element_symbol = args[0]
        # composition value argument fraction is always expected in percent
        # i.e. human should have written 98 instead 0.98!
        if (element_symbol != "X") and (element_symbol in chemical_symbols):
            # case: "Mo"
            if len(args) == 1:
                return parse_human_readable_composition_case_one(
                    element_symbol)
            # case: "Mo matrix" or "Mo 98.0", always assuming at.-%!
            if len(args) == 2:
                return parse_human_readable_composition_case_two(
                    args, element_symbol)
            # case: "Mo 98 wt.-%", selectable at.-%, ppm, ppb, or wt.-%!
            if len(args) == 3:
                return parse_human_readable_composition_case_three(
                    eln_input, args, element_symbol)
            # case: "Mo 98 +- 2", always assuming at.-%!
            if len(args) == 4:
                return parse_human_readable_composition_case_four(
                    eln_input, element_symbol)
            # case: "Mo 98 wt.-% +- 2", selectable at.-%, ppm, ppb, or wt.-%!
            if len(args) == 5:
                return parse_human_readable_composition_case_five(
                    eln_input, args, element_symbol)
    return (None, None, None, None, None)


def parse_composition_table(composition_list):
    """Check if all the entries in the composition list yield a valid composition table."""
    composition_table = {}
    # check that there are no contradictions or inconsistenc
    for entry in composition_list:
        instruction, element, composition, stdev, normalization \
            = parse_human_readable_composition_information(entry)
        # print(f"{instruction}, {element}, {composition}, {stdev}, {normalization}")

        if instruction == "add_element":
            if "normalization" not in composition_table:
                if normalization is not None:
                    composition_table["normalization"] = normalization
            else:
                # as the normalization model is already defined, all following statements
                # need to comply because we assume we are not allowed to mix atom and weight
                # percent normalization in a composition_table
                if normalization is not None:
                    if normalization != composition_table["normalization"]:
                        raise ValueError("Composition list is contradicting as it \
                                         mixes atom- with weight-percent normalization!")

            if element not in composition_table:
                composition_table[element] = (composition, stdev)
            else:
                raise ValueError("Composition list is incorrectly formatted as if has \
                                 at least multiple lines for the same element!")
            continue
        if instruction == "define_matrix":
            if element not in composition_table:
                composition_table[element] = (None, None)
                # because the fraction is unclear at this point
            else:
                raise ValueError("Composition list is contradicting as it includes \
                                 at least two statements what the matrix should be!")

    # determine remaining fraction
    total_fractions = 0.
    remainder_element = None
    for keyword, tpl in composition_table.items():
        if keyword != "normalization":
            if (tpl is not None) and (tpl != (None, None)):
                total_fractions += tpl[0]
            else:
                remainder_element = keyword
    # print(f"Total fractions {total_fractions}, remainder element {remainder_element}")
    if remainder_element is None:
        raise ValueError("Composition list inconsistent because either fractions for \
                         elements do not add up to 100. or no symbol for matrix defined!")

    if composition_table:  # means != {}
        composition_table[remainder_element] = (1.0e2 - total_fractions, None)
        # error propagation model required

    # document if reporting as percent or fractional values
    composition_table["percent"] = True

    return composition_table
