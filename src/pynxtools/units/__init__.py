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
from typing import Optional, Dict, Any
from pint import UnitRegistry
from pint.errors import UndefinedUnitError, DefinitionSyntaxError

try:
    from nomad.units import ureg
except ImportError as exc:
    ureg = UnitRegistry(os.path.join(os.path.dirname(__file__), "default_en.txt"))


class NXUnitSet:
    """
    Maps from `NX_` tokens to dimensionality.

    - None  -> disables dimensionality check
    - '1'   -> dimensionless quantities
    - 'transformation' -> specially handled elsewhere
    """

    mapping: Dict[str, Optional[str]] = {
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

    _dimensionalities: Dict[str, Optional[Any]] = {}

    @staticmethod
    def normalize(value: str) -> str:
        """Normalize the given token to 'NX_' prefix form."""
        value = value.upper()
        if not value.startswith("NX_"):
            value = "NX_" + value
        return value

    @classmethod
    def is_nx_token(cls, value: str) -> bool:
        """Check if a given token is one of the known NX tokens."""
        return cls.normalize(value) in cls.mapping

    @classmethod
    def get_dimensionality(cls, token: str) -> Optional[Any]:
        """Get the dimensionality object for a given NX token."""
        token = cls.normalize(token)
        if token in cls._dimensionalities:
            return cls._dimensionalities[token]

        definition = cls.mapping.get(token)
        if definition is None or definition == "transformation":
            cls._dimensionalities[token] = None
        elif definition == "1":
            cls._dimensionalities[token] = ureg("").dimensionality
        else:
            try:
                cls._dimensionalities[token] = ureg.get_dimensionality(definition)
            except (UndefinedUnitError, DefinitionSyntaxError) as e:
                cls._dimensionalities[token] = None

        return cls._dimensionalities[token]

    @classmethod
    def matches(cls, expected_token: str, actual_unit: str) -> bool:
        """Check whether the actual unit matches the expected NX token by comparing dimensionalities."""
        if expected_token in ["NX_ANY", "NX_UNITLESS"]:
            return True

        expected_dim = cls.get_dimensionality(expected_token)
        if expected_dim is None:
            return True

        if expected_dim is "dimensionless" and actual_unit:
            return False

        try:
            actual_dim = (1 * ureg(actual_unit)).dimensionality
        except (UndefinedUnitError, DefinitionSyntaxError):
            return False

        return actual_dim == expected_dim
