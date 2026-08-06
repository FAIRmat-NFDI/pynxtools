import pytest

from pynxtools.units import NXUnitSet, ureg


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


@pytest.mark.parametrize(
    "unit_category,expected",
    [
        ("NX_ANGLE", "radian"),
        ("NX_AREA", "m ** 2"),
        ("NX_CHARGE", "coulomb"),
        ("NX_COUNT", "dimensionless"),
        ("NX_CROSS_SECTION", "barn"),
        ("NX_CURRENT", "ampere"),
        ("NX_DIMENSIONLESS", "dimensionless"),
        ("NX_EMITTANCE", "nm * rad"),
        ("NX_ENERGY", "eV"),
        ("NX_FLUX", "1 / second / cm ** 2"),
        ("NX_FREQUENCY", "hertz"),
        ("NX_LENGTH", "m"),
        ("NX_MASS", "gram"),
        ("NX_MASS_DENSITY", "gram / m ** 3"),
        ("NX_MOLECULAR_WEIGHT", "gram / mol"),
        ("NX_PERIOD", "second"),
        ("NX_PER_AREA", "1 / m ** 2"),
        ("NX_PER_LENGTH", "1 / m"),
        ("NX_POWER", "watt"),
        ("NX_PRESSURE", "mbar"),
        ("NX_PULSES", "dimensionless"),
        ("NX_SCATTERING_LENGTH_DENSITY", "1 / m ** 2"),
        ("NX_SOLID_ANGLE", "steradian"),
        ("NX_TEMPERATURE", "kelvin"),
        ("NX_TIME", "second"),
        ("NX_TIME_OF_FLIGHT", "second"),
        ("NX_UNITLESS", "dimensionless"),
        ("NX_VOLTAGE", "volt"),
        ("NX_VOLUME", "m ** 3"),
        ("NX_WAVELENGTH", "angstrom"),
        ("NX_WAVENUMBER", "1 / angstrom"),
    ],
)
def test_get_default_unit(unit_category, expected):
    assert ureg(NXUnitSet.get_default_unit(unit_category)) == ureg(expected)


@pytest.mark.parametrize("unit_category", ["NX_ANY", "NX_TRANSFORMATION"])
def test_get_default_unit_none_for_unconstrained_categories(unit_category):
    assert NXUnitSet.get_default_unit(unit_category) is None
