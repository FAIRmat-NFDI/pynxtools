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

    mapping: dict[str, str | None] = {
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

    # Default storage unit per `NX_` unit category, used as `Quantity.unit` for
    # generated metainfo. Dimensionless categories map to "dimensionless" so that
    # `unit` and `dimensionality` stay consistent (and a subclass overriding only
    # `dimensionality` does not inherit an incompatible `unit` from its base
    # quantity). `None` means the category has no meaningful dimensionality check
    # at all (e.g. 'NX_ANY', 'NX_TRANSFORMATION').
    default_unit: dict[str, str | None] = {
        "NX_ANGLE": "radian",
        "NX_ANY": None,
        "NX_AREA": "m ** 2",
        "NX_CHARGE": "coulomb",
        "NX_COUNT": "dimensionless",
        "NX_CROSS_SECTION": "m ** 2",
        "NX_CURRENT": "ampere",
        "NX_DIMENSIONLESS": "dimensionless",
        "NX_EMITTANCE": "m * radian",
        "NX_ENERGY": "joule",
        "NX_FLUX": "1 / second / m ** 2",
        "NX_FREQUENCY": "hertz",
        "NX_LENGTH": "m",
        "NX_MASS": "kilogram",
        "NX_MASS_DENSITY": "kilogram / m ** 3",
        "NX_MOLECULAR_WEIGHT": "kilogram / mol",
        "NX_PERIOD": "second",
        "NX_PER_AREA": "1 / m ** 2",
        "NX_PER_LENGTH": "1 / m",
        "NX_POWER": "watt",
        "NX_PRESSURE": "pascal",
        "NX_PULSES": "dimensionless",
        "NX_SCATTERING_LENGTH_DENSITY": "1 / m ** 2",
        "NX_SOLID_ANGLE": "steradian",
        "NX_TEMPERATURE": "kelvin",
        "NX_TIME": "second",
        "NX_TIME_OF_FLIGHT": "second",
        "NX_TRANSFORMATION": None,
        "NX_UNITLESS": "dimensionless",
        "NX_VOLTAGE": "volt",
        "NX_VOLUME": "m ** 3",
        "NX_WAVELENGTH": "m",
        "NX_WAVENUMBER": "1 / m",
    }

    _dimensionalities: dict[str, Any | None] = {}
    _default_units: dict[str, str | None] = {}

    @classmethod
    def get_default_unit(cls, nx_unit: str) -> str | None:
        """
        Get the default storage unit for a given NeXus unit category or example.

        Mirrors :meth:`get_dimensionality`: if `nx_unit` is a recognized `NX_`
        unit category, its default unit from `default_unit` is used ('dimensionless'
        for dimensionless categories, `None` for categories without a meaningful
        dimensionality check, e.g. 'NX_ANY', 'NX_TRANSFORMATION'). Otherwise
        `nx_unit` is treated as a concrete example unit given directly in the
        NXDL (e.g. 'eV', 'mm') and is used as-is if it is a valid pint unit.

        Args:
            nx_unit (str): The NeXus unit category or a specific unit string.

        Returns:
            Optional[str]: A pint-parsable unit string, or None if undefined.
        """
        if nx_unit in cls._default_units:
            return cls._default_units[nx_unit]

        if nx_unit in cls.mapping:
            result = cls.default_unit.get(nx_unit)
        else:
            try:
                ureg(nx_unit)
                result = nx_unit
            except (UndefinedUnitError, DefinitionSyntaxError):
                result = None

        cls._default_units[nx_unit] = result
        return result

    @classmethod
    def get_dimensionality(cls, nx_unit: str) -> Any | None:
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

        actual_dim = ureg.Quantity(1, unit).to_base_units().dimensionality

        return actual_dim == expected_dim
