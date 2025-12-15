import pytest

from pynxtools.units import NXUnitSet


@pytest.mark.parametrize(
    "unit_category,unit,expected",
    [
        ("NX_LENGTH", "meter", True),
        ("NX_LENGTH", "m", True),
        ("NX_LENGTH", "second", False),
        ("NX_TEMPERATURE", "kelvin", True),
        ("NX_TEMPERATURE", "celsius", True),  # offset unit
        ("NX_TEMPERATURE", "degC", True),  # alias
        ("NX_TEMPERATURE", "second", False),
        ("NX_ANY", "meter", True),
        ("NX_ANY", "", True),  # empty allowed
        ("NX_ANY", "foobar", False),  # unknown unit not allowed for NX_ANY
        ("NX_LENGTH", "foobar", False),  # unknown unit not allowed
        ("NX_LENGTH", "pixel", True),  # pixel is accepted as length
        ("NX_DIMENSIONLESS", "", True),
        ("NX_DIMENSIONLESS", "meter", False),
        ("NX_UNITLESS", "", True),
        ("NX_UNITLESS", "meter", False),
    ],
)
def test_matches(unit_category, unit, expected):
    assert NXUnitSet.matches(unit_category, unit) == expected
