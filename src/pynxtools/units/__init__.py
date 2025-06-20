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
"""A unit registry for NeXus units"""

import os
from typing import Any, Optional

from pint import UnitRegistry
from pint.errors import DefinitionSyntaxError, DimensionalityError, UndefinedUnitError

try:
    from nomad.units import ureg
except ImportError as exc:
    ureg = UnitRegistry(os.path.join(os.path.dirname(__file__), "default_en.txt"))


class NXUnitSet:
    """
    Maps from `NX_` unit_categories (or unit examples) to dimensionality.

    - None  -> disables dimensionality check
    - '1'   -> dimensionless quantities
    - 'transformation' -> specially handled elsewhere
    """

    mapping: dict[str, Optional[str]] = {
        "NX_ANGLE": "[angle]",
        "NX_ANY": None,
        "NX_AREA": "[area]",
        "NX_CHARGE": "[charge]",
        "NX_COUNT": "1",
        "NX_CROSS_SECTION": "[area]",
        "NX_CURRENT": "[current]",
        "NX_DIMENSIONLESS": "1",
        "NX_EMITTANCE": "[length] * [angle]",
        "NX_ENERGY": "[energy]",
        "NX_FLUX": "1 / [time] / [area]",
        "NX_FREQUENCY": "[frequency]",
        "NX_LENGTH": "[length]",
        "NX_MASS": "[mass]",
        "NX_MASS_DENSITY": "[mass] / [volume]",
        "NX_MOLECULAR_WEIGHT": "[mass] / [substance]",
        "NX_PERIOD": "[time]",
        "NX_PER_AREA": "1 / [area]",
        "NX_PER_LENGTH": "1 / [length]",
        "NX_POWER": "[power]",
        "NX_PRESSURE": "[pressure]",
        "NX_PULSES": "1",
        "NX_SCATTERING_LENGTH_DENSITY": "1 / [area]",
        "NX_SOLID_ANGLE": "[angle] * [angle]",
        "NX_TEMPERATURE": "[temperature]",
        "NX_TIME": "[time]",
        "NX_TIME_OF_FLIGHT": "[time]",
        "NX_TRANSFORMATION": "transformation",
        "NX_UNITLESS": "1",
        "NX_VOLTAGE": "[energy] / [current] / [time]",
        "NX_VOLUME": "[volume]",
        "NX_WAVELENGTH": "[length]",
        "NX_WAVENUMBER": "1 / [length]",
    }

    _dimensionalities: dict[str, Optional[Any]] = {}

    @classmethod
    def get_dimensionality(cls, nx_unit: str) -> Optional[Any]:
        """
        Get the dimensionality object for a given NeXus unit category or example.

        Args:
            nx_unit (str): The NeXus unit category or a specific unit string.

        Returns:
            Optional[Any]: The dimensionality object, '1' for dimensionless,
                or None if undefined.
        """
        if nx_unit in cls._dimensionalities:
            return cls._dimensionalities[nx_unit]

        definition = cls.mapping.get(nx_unit)
        if definition == "1":
            cls._dimensionalities[nx_unit] = ureg("").dimensionality
        elif definition is None:
            try:
                quantity = 1 * ureg(nx_unit)
                if quantity.dimensionality == ureg("").dimensionality:
                    cls._dimensionalities[nx_unit] = ureg("").dimensionality
                else:
                    cls._dimensionalities[nx_unit] = quantity.dimensionality
            except (UndefinedUnitError, DefinitionSyntaxError):
                cls._dimensionalities[nx_unit] = None
        elif definition == "transformation":
            cls._dimensionalities[nx_unit] = None

        else:
            try:
                cls._dimensionalities[nx_unit] = ureg.get_dimensionality(definition)
            except (UndefinedUnitError, DefinitionSyntaxError) as e:
                cls._dimensionalities[nx_unit] = None

        return cls._dimensionalities[nx_unit]

    @classmethod
    def matches(cls, unit_category: str, unit: str) -> bool:
        """
        Check whether the actual unit matches the expected unit category or example.

        This is determined by comparing dimensionalities. Special handling is
        included for NX_ANY (accepts any valid unit or empty string) and for
        dimensionless cases.

        Args:
            unit_category (str): The expected NeXus unit category.
            unit (str): The actual unit string to validate.

        Returns:
            bool: True if the actual unit matches the expected dimensionality;
                False otherwise.
        """

        def is_valid_unit(unit: str):
            """Check if unit is generally valid."""
            if not unit:
                return False
            try:
                ureg(unit)
                return True
            except (
                UndefinedUnitError,
                DefinitionSyntaxError,
                AttributeError,
                DimensionalityError,
            ):
                return False

        if unit_category in ("NX_ANY"):
            # Note: we allow empty string units here
            return is_valid_unit(unit) or unit == ""

        expected_dim = cls.get_dimensionality(unit_category)

        if expected_dim is None and not unit:
            return True

        if str(expected_dim) == "dimensionless":
            return True if not unit else False

        # At this point, we expect a valid unit.
        if not is_valid_unit(unit):
            return False

        # Workaround for pixels as units in transformations
        if ureg.Unit(unit) == ureg.Unit("pixel") and str(expected_dim) == "[length]":
            return True

        actual_dim = (1 * ureg(unit)).dimensionality

        return actual_dim == expected_dim
